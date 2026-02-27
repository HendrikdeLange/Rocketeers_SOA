# =============================================================================
# PURE PREMIUM MODEL — Business Claims
# =============================================================================
# Actuarial Approach : Frequency × Severity (two-part GLM)
#   • Frequency  : Poisson GLM  — expected claims per unit exposure
#   • Severity   : Gamma GLM    — expected claim amount given a claim occurred
#   • Pure Premium = Frequency × Severity
#
# A direct Tweedie GLM is also fitted as a cross-check.
#
# Variables
#   Response   : claim_count (frequency), claim_amount (severity)
#   Offset     : log(exposure)  — normalises for differing exposure periods
#   Categorical: solar_system, energy_backup_score, safety_compliance,
#                maintenance_freq
#   Continuous : production_load, supply_chain_index, avg_crew_exp
# =============================================================================

# ── 0. Dependencies ───────────────────────────────────────────────────────────
required_packages <- c("tidyverse", "tweedie", "statmod", "caret",
                       "gridExtra", "scales", "knitr")

for (pkg in required_packages) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg, repos = "https://cloud.r-project.org")
  }
  library(pkg, character.only = TRUE)
}

set.seed(42)

# ── 1. Load & Prepare Data ────────────────────────────────────────────────────
cat("\n========== 1. LOADING DATA ==========\n")

df <- read.csv("C:\\Users\\hendr\\OneDrive\\Documents\\Rocketeers_SOA\\model_data\\bussiness_claims_model_data.csv", stringsAsFactors = FALSE)
cat(sprintf("Loaded %s rows × %s columns\n", nrow(df), ncol(df)))

# --- Type conversions ---
df <- df %>%
  mutate(
    # Categorical factors (ordered where applicable)
    solar_system        = factor(solar_system,
                                 levels = c("Epsilon", "Helionis Cluster", "Zeta")),
    energy_backup_score = factor(energy_backup_score, levels = 1:5, ordered = TRUE),
    safety_compliance   = factor(safety_compliance,   levels = 1:5, ordered = TRUE),
    maintenance_freq    = factor(maintenance_freq,    levels = 0:6, ordered = TRUE),
    
    # Derived response
    pure_premium = claim_amount / exposure,   # actual PP for diagnostics
    has_claim    = as.integer(claim_count > 0)
  )

cat("\nClaim summary:\n")
cat(sprintf("  Policies          : %s\n", nrow(df)))
cat(sprintf("  Policies w/ claims: %s (%.1f%%)\n",
            sum(df$claim_count > 0),
            100 * mean(df$claim_count > 0)))
cat(sprintf("  Total exposure    : %.0f\n", sum(df$exposure)))
cat(sprintf("  Total claim amt   : R%s\n",
            format(sum(df$claim_amount), big.mark = ",")))
cat(sprintf("  Avg pure premium  : R%s\n",
            format(round(mean(df$pure_premium)), big.mark = ",")))

# ── 2. Train / Test Split (80/20) ─────────────────────────────────────────────
cat("\n========== 2. TRAIN / TEST SPLIT ==========\n")

train_idx <- createDataPartition(df$has_claim, p = 0.8, list = FALSE)
train     <- df[ train_idx, ]
test      <- df[-train_idx, ]

cat(sprintf("Train: %s rows | Test: %s rows\n", nrow(train), nrow(test)))

# ── 3. FREQUENCY MODEL — Poisson GLM ─────────────────────────────────────────
cat("\n========== 3. FREQUENCY MODEL (Poisson GLM) ==========\n")

freq_model <- glm(
  claim_count ~
    solar_system +
    production_load +
    energy_backup_score +
    supply_chain_index +
    avg_crew_exp +
    maintenance_freq +
    safety_compliance +
    offset(log(exposure)),          # <— critical: normalise for exposure
  family  = poisson(link = "log"),
  data    = train
)

cat("\nFrequency Model Summary:\n")
print(summary(freq_model))

# Overdispersion check
dispersion_ratio <- sum(residuals(freq_model, type = "pearson")^2) / freq_model$df.residual
cat(sprintf("\nDispersion ratio: %.3f  (>1 suggests overdispersion — consider quasi-Poisson)\n",
            dispersion_ratio))

# If overdispersed, refit with quasi-Poisson
if (dispersion_ratio > 1.5) {
  cat("Refitting with quasi-Poisson to account for overdispersion...\n")
  freq_model <- glm(
    claim_count ~
      solar_system +
      production_load +
      energy_backup_score +
      supply_chain_index +
      avg_crew_exp +
      maintenance_freq +
      safety_compliance +
      offset(log(exposure)),
    family = quasipoisson(link = "log"),
    data   = train
  )
}

# ── 4. SEVERITY MODEL — Gamma GLM (claims-only subset) ───────────────────────
cat("\n========== 4. SEVERITY MODEL (Gamma GLM) ==========\n")

# Gamma GLM requires strictly positive response values.
# Exclude the rare records where claim_count > 0 but claim_amount = 0
# (data quality issue — a claim event was recorded but no amount was captured).
train_claims_raw <- train %>% filter(claim_count > 0)
train_claims     <- train_claims_raw %>% filter(claim_amount > 0)

n_zero_amt <- nrow(train_claims_raw) - nrow(train_claims)
if (n_zero_amt > 0) {
  cat(sprintf("  Note: %s record(s) had claim_count > 0 but claim_amount = 0 — excluded from severity model.\n",
              n_zero_amt))
}
cat(sprintf("Severity training records: %s\n", nrow(train_claims)))

sev_model <- glm(
  (claim_amount / claim_count) ~    # average cost per claim
    solar_system +
    production_load +
    energy_backup_score +
    supply_chain_index +
    avg_crew_exp +
    maintenance_freq +
    safety_compliance,
  family  = Gamma(link = "log"),
  weights = claim_count,            # weight by number of claims
  data    = train_claims
)

cat("\nSeverity Model Summary:\n")
print(summary(sev_model))

# ── 5. TWEEDIE GLM (Direct Pure Premium — cross-check) ───────────────────────
cat("\n========== 5. TWEEDIE GLM (Direct Pure Premium) ==========\n")

# Estimate optimal Tweedie power (p) — compound Poisson range: 1 < p < 2
library(tweedie)
library(statmod)

xi_profile <- tweedie.profile(
  pure_premium ~
    solar_system +
    production_load +
    energy_backup_score +
    supply_chain_index +
    avg_crew_exp +
    maintenance_freq +
    safety_compliance,
  p.vec   = seq(1.2, 1.9, by = 0.1),
  link    = "log",
  weights = train$exposure,
  data    = train,
  do.plot = FALSE
)

best_p <- xi_profile$p.max
cat(sprintf("Optimal Tweedie power (p): %.2f\n", best_p))

tweedie_model <- glm(
  pure_premium ~
    solar_system +
    production_load +
    energy_backup_score +
    supply_chain_index +
    avg_crew_exp +
    maintenance_freq +
    safety_compliance,
  family  = tweedie(var.power = best_p, link.power = 0),   # link.power=0 → log link
  weights = train$exposure,
  data    = train
)

cat("\nTweedie Model Summary:\n")
print(summary(tweedie_model))

# ── 6. Generate Predictions ───────────────────────────────────────────────────
cat("\n========== 6. PREDICTIONS ==========\n")

# --- Frequency × Severity ---
# Frequency: predicted claims per unit of exposure (set offset=0 for rate)
test$freq_pred <- predict(freq_model,
                          newdata = test %>% mutate(exposure = 1),
                          type    = "response")

test$sev_pred  <- predict(sev_model,
                          newdata = test,
                          type    = "response")

# Pure Premium = Frequency rate × Severity
test$pp_freq_sev <- test$freq_pred * test$sev_pred

# --- Tweedie direct ---
test$pp_tweedie <- predict(tweedie_model, newdata = test, type = "response")

# --- Actual ---
test$pp_actual  <- test$pure_premium

cat("Sample predictions (first 10 rows):\n")
test %>%
  select(policy_id, solar_system, exposure, claim_amount, pp_actual,
         pp_freq_sev, pp_tweedie) %>%
  head(10) %>%
  mutate(across(where(is.numeric) & !c(exposure), ~ format(round(.), big.mark = ","))) %>%
  print()

# ── 7. Model Evaluation ───────────────────────────────────────────────────────
cat("\n========== 7. MODEL EVALUATION ==========\n")

# Weighted MAE & RMSE (weighted by exposure so larger exposures matter more)
wmae <- function(actual, predicted, weights) {
  sum(weights * abs(actual - predicted)) / sum(weights)
}
wrmse <- function(actual, predicted, weights) {
  sqrt(sum(weights * (actual - predicted)^2) / sum(weights))
}

w <- test$exposure

cat(sprintf("\n%-30s %15s %15s\n", "Metric", "Freq×Sev", "Tweedie"))
cat(strrep("-", 62), "\n")
cat(sprintf("%-30s %15s %15s\n", "Weighted MAE (R)",
            format(round(wmae(test$pp_actual, test$pp_freq_sev, w)), big.mark=","),
            format(round(wmae(test$pp_actual, test$pp_tweedie,  w)), big.mark=",")))
cat(sprintf("%-30s %15s %15s\n", "Weighted RMSE (R)",
            format(round(wrmse(test$pp_actual, test$pp_freq_sev, w)), big.mark=","),
            format(round(wrmse(test$pp_actual, test$pp_tweedie,  w)), big.mark=",")))
cat(sprintf("%-30s %15s %15s\n", "Mean Predicted PP (R)",
            format(round(weighted.mean(test$pp_freq_sev, w)), big.mark=","),
            format(round(weighted.mean(test$pp_tweedie,  w)), big.mark=",")))
cat(sprintf("%-30s %15s\n",      "Mean Actual PP (R)",
            format(round(weighted.mean(test$pp_actual, w)), big.mark=",")))

# Lift by decile
test <- test %>%
  mutate(decile = ntile(pp_freq_sev, 10))

lift_table <- test %>%
  group_by(decile) %>%
  summarise(
    policies        = n(),
    avg_actual_pp   = round(weighted.mean(pp_actual,  exposure)),
    avg_pred_pp     = round(weighted.mean(pp_freq_sev, exposure)),
    lift            = round(avg_actual_pp / weighted.mean(pp_actual, exposure) *
                              weighted.mean(test$pp_actual, test$exposure) /
                              weighted.mean(test$pp_actual, test$exposure), 3),
    .groups = "drop"
  )

cat("\nLift Table by Predicted Decile (Freq×Sev model):\n")
print(lift_table)

# ── 8. Rating Factor Relativities ────────────────────────────────────────────
cat("\n========== 8. RATING FACTOR RELATIVITIES ==========\n")

extract_relativities <- function(model, label) {
  coefs <- coef(model)
  data.frame(
    model    = label,
    variable = names(coefs),
    coef     = coefs,
    relativity = exp(coefs),
    row.names = NULL
  )
}

rel_freq <- extract_relativities(freq_model,    "Frequency")
rel_sev  <- extract_relativities(sev_model,     "Severity")
rel_tw   <- extract_relativities(tweedie_model, "Tweedie")

cat("\nFrequency Relativities:\n");  print(rel_freq,  row.names = FALSE)
cat("\nSeverity Relativities:\n");   print(rel_sev,   row.names = FALSE)
cat("\nTweedie Relativities:\n");    print(rel_tw,    row.names = FALSE)

# ── 9. Predict Pure Premium for ALL Policies ─────────────────────────────────
cat("\n========== 9. SCORING FULL PORTFOLIO ==========\n")

df$freq_rate      <- predict(freq_model,    newdata = df %>% mutate(exposure=1), type="response")
df$avg_claim_cost <- predict(sev_model,     newdata = df, type="response")
df$pp_freq_sev    <- df$freq_rate * df$avg_claim_cost
df$pp_tweedie     <- predict(tweedie_model, newdata = df, type="response")

# Annual premium estimate = pure premium × exposure
df$estimated_premium_freq_sev <- df$pp_freq_sev * df$exposure
df$estimated_premium_tweedie  <- df$pp_tweedie  * df$exposure

cat(sprintf("Portfolio total estimated premium (Freq×Sev): R%s\n",
            format(round(sum(df$estimated_premium_freq_sev)), big.mark=",")))
cat(sprintf("Portfolio total estimated premium (Tweedie) : R%s\n",
            format(round(sum(df$estimated_premium_tweedie)),  big.mark=",")))
cat(sprintf("Portfolio total actual claim amount         : R%s\n",
            format(round(sum(df$claim_amount)), big.mark=",")))

# ── 10. Export Results ────────────────────────────────────────────────────────
cat("\n========== 10. SAVING OUTPUTS ==========\n")

output <- df %>%
  select(policy_id, station_id, solar_system,
         production_load, energy_backup_score, supply_chain_index,
         avg_crew_exp, maintenance_freq, safety_compliance,
         exposure, claim_count, claim_amount,
         freq_rate, avg_claim_cost,
         pp_freq_sev, pp_tweedie,
         estimated_premium_freq_sev, estimated_premium_tweedie)

write.csv(output,       "pure_premium_predictions.csv", row.names = FALSE)
write.csv(rel_freq,     "relativities_frequency.csv",   row.names = FALSE)
write.csv(rel_sev,      "relativities_severity.csv",    row.names = FALSE)
write.csv(rel_tw,       "relativities_tweedie.csv",     row.names = FALSE)

# Save model objects
saveRDS(freq_model,    "model_frequency.rds")
saveRDS(sev_model,     "model_severity.rds")
saveRDS(tweedie_model, "model_tweedie.rds")

cat("Saved: pure_premium_predictions.csv\n")
cat("Saved: relativities_frequency.csv, relativities_severity.csv, relativities_tweedie.csv\n")
cat("Saved: model_frequency.rds, model_severity.rds, model_tweedie.rds\n")

# ── 11. Diagnostic Plots ──────────────────────────────────────────────────────
cat("\n========== 11. GENERATING DIAGNOSTIC PLOTS ==========\n")

pdf("pure_premium_diagnostics.pdf", width = 14, height = 10)

# Plot 1 — Actual vs Predicted (sample of 2000 for visibility)
plot_sample <- test %>% sample_n(min(2000, nrow(test)))
p1 <- ggplot(plot_sample, aes(x = pp_freq_sev, y = pp_actual)) +
  geom_point(alpha = 0.3, colour = "#2E75B6", size = 1) +
  geom_abline(slope = 1, intercept = 0, colour = "red", linewidth = 1) +
  scale_x_continuous(labels = label_comma(prefix = "R"), limits = c(0, quantile(plot_sample$pp_freq_sev, 0.99))) +
  scale_y_continuous(labels = label_comma(prefix = "R"), limits = c(0, quantile(plot_sample$pp_actual,   0.99))) +
  labs(title = "Actual vs Predicted Pure Premium",
       subtitle = "Frequency × Severity model | Red line = perfect fit",
       x = "Predicted PP (R)", y = "Actual PP (R)") +
  theme_minimal(base_size = 11)

# Plot 2 — Distribution of predicted PP by solar system
p2 <- ggplot(df, aes(x = pp_freq_sev, fill = solar_system)) +
  geom_density(alpha = 0.5) +
  scale_x_continuous(labels = label_comma(prefix = "R"),
                     limits = c(0, quantile(df$pp_freq_sev, 0.99))) +
  scale_fill_manual(values = c("#1F3864", "#2E75B6", "#FFC000")) +
  labs(title = "Distribution of Predicted Pure Premium by Solar System",
       x = "Predicted Pure Premium (R)", y = "Density", fill = "Solar System") +
  theme_minimal(base_size = 11)

# Plot 3 — Frequency relativities
rel_freq_plot <- rel_freq %>%
  filter(variable != "(Intercept)") %>%
  mutate(variable = gsub("solar_system|energy_backup_score|safety_compliance|maintenance_freq", "", variable))

p3 <- ggplot(rel_freq_plot, aes(x = reorder(variable, relativity), y = relativity)) +
  geom_col(fill = "#2E75B6", alpha = 0.85) +
  geom_hline(yintercept = 1, colour = "red", linetype = "dashed") +
  coord_flip() +
  labs(title = "Frequency Model — Relativities",
       subtitle = "Values >1 increase expected claim frequency; <1 decrease it",
       x = NULL, y = "Relativity") +
  theme_minimal(base_size = 11)

# Plot 4 — Severity relativities
rel_sev_plot <- rel_sev %>%
  filter(variable != "(Intercept)") %>%
  mutate(variable = gsub("solar_system|energy_backup_score|safety_compliance|maintenance_freq", "", variable))

p4 <- ggplot(rel_sev_plot, aes(x = reorder(variable, relativity), y = relativity)) +
  geom_col(fill = "#FFC000", alpha = 0.85) +
  geom_hline(yintercept = 1, colour = "red", linetype = "dashed") +
  coord_flip() +
  labs(title = "Severity Model — Relativities",
       subtitle = "Values >1 increase expected claim amount; <1 decrease it",
       x = NULL, y = "Relativity") +
  theme_minimal(base_size = 11)

# Plot 5 — Lift chart
p5 <- ggplot(lift_table, aes(x = decile)) +
  geom_line(aes(y = avg_actual_pp, colour = "Actual"),    linewidth = 1.2) +
  geom_line(aes(y = avg_pred_pp,   colour = "Predicted"), linewidth = 1.2, linetype = "dashed") +
  geom_point(aes(y = avg_actual_pp, colour = "Actual"),   size = 3) +
  geom_point(aes(y = avg_pred_pp,   colour = "Predicted"),size = 3) +
  scale_x_continuous(breaks = 1:10) +
  scale_y_continuous(labels = label_comma(prefix = "R")) +
  scale_colour_manual(values = c("Actual" = "#1F3864", "Predicted" = "#FFC000")) +
  labs(title = "Lift Chart — Predicted Pure Premium Deciles",
       subtitle = "Good model: predicted and actual lines track closely",
       x = "Predicted Risk Decile (1=Lowest, 10=Highest)",
       y = "Average Pure Premium (R)", colour = NULL) +
  theme_minimal(base_size = 11)

# Plot 6 — Tweedie vs Freq×Sev comparison
p6 <- ggplot(test %>% sample_n(min(2000, nrow(test))),
             aes(x = pp_freq_sev, y = pp_tweedie)) +
  geom_point(alpha = 0.3, colour = "#2E75B6", size = 1) +
  geom_abline(slope = 1, intercept = 0, colour = "red", linewidth = 1) +
  scale_x_continuous(labels = label_comma(prefix="R"), limits=c(0, quantile(test$pp_freq_sev,0.99))) +
  scale_y_continuous(labels = label_comma(prefix="R"), limits=c(0, quantile(test$pp_tweedie,0.99))) +
  labs(title = "Freq×Sev vs Tweedie Predictions",
       subtitle = "Cross-check: both models should broadly agree",
       x = "Freq×Sev PP (R)", y = "Tweedie PP (R)") +
  theme_minimal(base_size = 11)

grid.arrange(p1, p2, p3, p4, p5, p6, ncol = 2)
dev.off()

cat("Saved: pure_premium_diagnostics.pdf\n")

# ── 12. Scoring Function for New Business ─────────────────────────────────────
cat("\n========== 12. SCORING FUNCTION ==========\n")
cat("
# ---------------------------------------------------------------
# SCORING FUNCTION — use this to price new policies
# ---------------------------------------------------------------
score_pure_premium <- function(new_data,
                               freq_model, sev_model, tweedie_model) {
  # new_data must contain all feature columns (exposure not needed for PP rate)
  new_data$freq_rate      <- predict(freq_model,
                                     newdata = new_data %>% mutate(exposure=1),
                                     type    = 'response')
  new_data$avg_claim_cost <- predict(sev_model,     newdata = new_data, type='response')
  new_data$pp_freq_sev    <- new_data$freq_rate * new_data$avg_claim_cost
  new_data$pp_tweedie     <- predict(tweedie_model, newdata = new_data, type='response')
  return(new_data)
}

# Example — score a single new policy:
new_policy <- data.frame(
  solar_system        = factor('Epsilon', levels=c('Epsilon','Helionis Cluster','Zeta')),
  production_load     = 0.65,
  energy_backup_score = factor(3, levels=1:5, ordered=TRUE),
  supply_chain_index  = 0.50,
  avg_crew_exp        = 10,
  maintenance_freq    = factor(3, levels=0:6, ordered=TRUE),
  safety_compliance   = factor(4, levels=1:5, ordered=TRUE),
  exposure            = 1.0
)
scored <- score_pure_premium(new_policy, freq_model, sev_model, tweedie_model)
cat('Pure Premium (Freq x Sev): R', round(scored$pp_freq_sev), '\n')
cat('Pure Premium (Tweedie)   : R', round(scored$pp_tweedie),  '\n')
# ---------------------------------------------------------------
")

cat("\n========== DONE ==========\n")
cat("Models fitted and all outputs saved successfully.\n")