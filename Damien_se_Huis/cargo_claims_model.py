from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import statsmodels.api as sm
from statsmodels.genmod.families import Tweedie
from statsmodels.genmod.families.links import log as Log
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


warnings.filterwarnings('ignore')
base_path = Path(__file__).resolve().parent
data_folder = base_path.parent / "clean_data" / "csv_files"
freq_path = data_folder / "cargo_claims_freq.csv"
sev_path = data_folder / "cargo_claims_sev.csv"

#load data
cargo_claims_freq = pd.read_csv(freq_path)
cargo_claims_sev = pd.read_csv(sev_path)
print("data loaded")

sev_summarized = cargo_claims_sev.groupby('policy_id')['claim_amount'].sum().reset_index()
# 2. Merge only the claim_amount onto the frequency table
model_df = pd.merge(
    cargo_claims_freq, 
    sev_summarized, 
    on='policy_id', 
    how='left'
)
print("find here")
#model_df.to_csv("model_df.csv", index=False)

import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # non-interactive backend — prevents blocking
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

"""
def ggpairs_plot(df, figsize_scale=2.5, max_cols=15):
   
    # Drop high-cardinality ID-like columns and limit columns
    df = df.copy()
    
    # Auto-drop columns with too many unique values (likely IDs)
    df = df[[c for c in df.columns if df[c].nunique() < 50 or df[c].dtype in [np.float64, np.int64]]]
    
    # Cap columns to avoid memory blow-up
    if len(df.columns) > max_cols:
        print(f"Warning: Trimming to first {max_cols} columns. Pass max_cols= to override.")
        df = df.iloc[:, :max_cols]

    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    cols = num_cols + cat_cols
    n = len(cols)

    print(f"Plotting {n} columns: {cols}")

    fig, axes = plt.subplots(n, n, figsize=(figsize_scale * n, figsize_scale * n))
    if n == 1:
        axes = np.array([[axes]])
    fig.suptitle("Pairwise Plot (ggpairs style)", fontsize=14, y=1.01)

    for i, col_y in enumerate(cols):
        for j, col_x in enumerate(cols):
            ax = axes[i, j]
            x_is_num = col_x in num_cols
            y_is_num = col_y in num_cols

            try:
                if i == j:
                    # --- Diagonal ---
                    if x_is_num:
                        data = df[col_x].dropna()
                        ax.hist(data, bins=20, color='steelblue', alpha=0.7, density=True)
                        if len(data) > 1:
                            kde = stats.gaussian_kde(data)
                            xr = np.linspace(data.min(), data.max(), 200)
                            ax.plot(xr, kde(xr), color='navy', lw=1.5)
                    else:
                        vc = df[col_x].value_counts()
                        ax.bar(range(len(vc)), vc.values, color='steelblue', alpha=0.7)
                        ax.set_xticks(range(len(vc)))
                        ax.set_xticklabels(vc.index, rotation=45, ha='right', fontsize=7)

                elif i < j:
                    # --- Upper triangle ---
                    if x_is_num and y_is_num:
                        valid = df[[col_x, col_y]].dropna()
                        if len(valid) > 2:
                            r, p = stats.pearsonr(valid[col_x], valid[col_y])
                            color = 'darkred' if abs(r) > 0.5 else 'black'
                            ax.text(0.5, 0.5, f"r = {r:.2f}\np = {p:.3f}",
                                    ha='center', va='center', transform=ax.transAxes,
                                    fontsize=9, color=color)
                        ax.set_facecolor('#f9f9f9')
                    elif not x_is_num and y_is_num:
                        # x=cat, y=num: box per category
                        groups = [grp[col_y].dropna().values 
                                  for _, grp in df.groupby(col_x)]
                        cats = sorted(df[col_x].dropna().unique())
                        ax.boxplot(groups, patch_artist=True,
                                   boxprops=dict(facecolor='steelblue', alpha=0.5))
                        ax.set_xticks(range(1, len(cats) + 1))
                        ax.set_xticklabels(cats, rotation=45, fontsize=7)
                    elif x_is_num and not y_is_num:
                        # x=num, y=cat: horizontal box
                        groups = [grp[col_x].dropna().values 
                                  for _, grp in df.groupby(col_y)]
                        cats = sorted(df[col_y].dropna().unique())
                        ax.boxplot(groups, patch_artist=True, vert=False,
                                   boxprops=dict(facecolor='steelblue', alpha=0.5))
                        ax.set_yticks(range(1, len(cats) + 1))
                        ax.set_yticklabels(cats, fontsize=7)
                    else:
                        # both categorical: heatmap counts
                        ct = pd.crosstab(df[col_y], df[col_x])
                        ax.imshow(ct.values, aspect='auto', cmap='Blues')

                else:
                    # --- Lower triangle ---
                    if x_is_num and y_is_num:
                        valid = df[[col_x, col_y]].dropna()
                        ax.scatter(valid[col_x], valid[col_y], alpha=0.3, s=8, color='steelblue')
                        if len(valid) > 2:
                            m, b = np.polyfit(valid[col_x], valid[col_y], 1)
                            xr = np.linspace(valid[col_x].min(), valid[col_x].max(), 100)
                            ax.plot(xr, m * xr + b, color='red', lw=1.2)
                    elif not x_is_num and y_is_num:
                        cats = sorted(df[col_x].dropna().unique())
                        for k, (name, grp) in enumerate(df.groupby(col_x)):
                            ax.scatter([k] * len(grp), grp[col_y].dropna(),
                                       alpha=0.3, s=8)
                        ax.set_xticks(range(len(cats)))
                        ax.set_xticklabels(cats, rotation=45, fontsize=7)
                    elif x_is_num and not y_is_num:
                        cats = sorted(df[col_y].dropna().unique())
                        for k, (name, grp) in enumerate(df.groupby(col_y)):
                            ax.scatter(grp[col_x].dropna(), [k] * len(grp),
                                       alpha=0.3, s=8)
                        ax.set_yticks(range(len(cats)))
                        ax.set_yticklabels(cats, fontsize=7)
                    else:
                        ct = pd.crosstab(df[col_y], df[col_x])
                        ax.imshow(ct.values, aspect='auto', cmap='Greens')

            except Exception as e:
                ax.text(0.5, 0.5, f"err:\n{str(e)[:40]}",
                        ha='center', va='center', transform=ax.transAxes, fontsize=6)
                ax.set_facecolor('#ffe0e0')

            # Edge labels only
            if i == n - 1:
                ax.set_xlabel(col_x, fontsize=8)
            else:
                ax.set_xticklabels([])
            if j == 0:
                ax.set_ylabel(col_y, fontsize=8)
            else:
                ax.set_yticklabels([])

            ax.tick_params(labelsize=7)

    plt.tight_layout()
    out_path = base_path / "ggpairs_plot.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    plt.close()  # important: don't call plt.show() — it blocks in scripts
    print(f"Plot saved to {out_path}")

ggpairs_plot(model_df)
print("done")
"""
# ══════════════════════════════════════════════════════════════════════════════
# FULL MODEL SCRIPT — paste everything after the pd.merge(...)
# ══════════════════════════════════════════════════════════════════════════════
from sklearn.preprocessing import StandardScaler, LabelEncoder

# ── 1. PREP ───────────────────────────────────────────────────────────────────
model_df['claim_amount'] = model_df['claim_amount'].fillna(0)
model_df['has_claim']    = (model_df['claim_amount'] > 0).astype(int)

cat_cols = model_df.select_dtypes(exclude=[np.number]).columns.tolist()
le = LabelEncoder()
for col in cat_cols:
    model_df[col] = le.fit_transform(model_df[col].astype(str))

print("Columns:", model_df.columns.tolist())

# ── 2. SUBSETS & FEATURES ─────────────────────────────────────────────────────
claims_only   = model_df[model_df['has_claim'] == 1].copy()
freq_features = ['route_risk', 'pilot_experience', 'solar_radiation', 'exposure']
sev_features  = ['cargo_type', 'cargo_value', 'weight', 'exposure']

for col in ['cargo_value', 'weight']:
    upper = model_df[col].quantile(0.99)
    model_df[col]    = model_df[col].clip(upper=upper)
    claims_only[col] = claims_only[col].clip(upper=upper)

print("Outliers clipped at 99th pct for cargo_value and weight")
# ── 3. SCALE FEATURES ─────────────────────────────────────────────────────────
freq_scaler = StandardScaler()
sev_scaler  = StandardScaler()

freq_scaled = pd.DataFrame(
    freq_scaler.fit_transform(model_df[freq_features]),
    columns=freq_features,
    index=model_df.index
)
sev_scaled_claims = pd.DataFrame(
    sev_scaler.fit_transform(claims_only[sev_features]),
    columns=sev_features,
    index=claims_only.index
)
sev_scaled_all = pd.DataFrame(
    sev_scaler.transform(model_df[sev_features]),
    columns=sev_features,
    index=model_df.index
)

X_freq = sm.add_constant(freq_scaled)
X_sev  = sm.add_constant(sev_scaled_claims)

# ── CLEAN AFTER SCALING ───────────────────────────────────────────────────────
freq_scaled       = freq_scaled.replace([np.inf, -np.inf], np.nan).fillna(0)
sev_scaled_claims = sev_scaled_claims.replace([np.inf, -np.inf], np.nan).fillna(0)
sev_scaled_all    = sev_scaled_all.replace([np.inf, -np.inf], np.nan).fillna(0)

X_freq = sm.add_constant(freq_scaled)
X_sev  = sm.add_constant(sev_scaled_claims)
# ── 4. FREQUENCY MODEL ────────────────────────────────────────────────────────
freq_model = sm.GLM(
    model_df['has_claim'],
    X_freq,
    family=sm.families.Poisson()
).fit()
print(freq_model.summary())

# ── 5. SEVERITY MODEL ─────────────────────────────────────────────────────────
claim_scale = 1_000
sev_model = sm.GLM(
    claims_only['claim_amount'] / claim_scale,
    X_sev,
    family=sm.families.Gamma(link=sm.families.links.Log()),
    maxiter=200
).fit()
print(sev_model.summary())
print(f"Converged: {sev_model.converged}")

# ── 6. PURE PREMIUM ───────────────────────────────────────────────────────────
freq_pred = freq_model.predict(X_freq)
sev_pred  = sev_model.predict(sm.add_constant(sev_scaled_all)) * claim_scale

model_df['pure_premium'] = freq_pred * sev_pred

cap = model_df['pure_premium'].quantile(0.99)
model_df['pure_premium_capped'] = model_df['pure_premium'].clip(upper=cap)

print("\n── Raw Pure Premium ──")
print(model_df['pure_premium'].describe())
print("\n── Capped Pure Premium (99th pct) ──")
print(model_df['pure_premium_capped'].describe())

avg_claim = model_df[model_df['has_claim'] == 1]['claim_amount'].mean()
avg_freq  = model_df['has_claim'].mean()
naive_pp  = avg_freq * avg_claim
print(f"\nNaive pure premium (freq × avg severity): {naive_pp:,.2f}")
print(f"Model pure premium (median):              {model_df['pure_premium_capped'].median():,.2f}")
print(f"Model pure premium (mean):                {model_df['pure_premium_capped'].mean():,.2f}")


import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
# 1. PURE PREMIUM DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════
pp = model_df['pure_premium_capped']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Pure Premium Distribution", fontsize=14, fontweight='bold')

axes[0].hist(pp, bins=100, color='steelblue', alpha=0.8, edgecolor='none')
axes[0].set_xscale('log')
axes[0].set_xlabel('Pure Premium (log scale)')
axes[0].set_ylabel('Count')
axes[0].set_title('Distribution (log scale)')
axes[0].axvline(pp.median(), color='red',    linestyle='--', label=f'Median: {pp.median():,.0f}')
axes[0].axvline(pp.mean(),   color='orange', linestyle='--', label=f'Mean:   {pp.mean():,.0f}')
axes[0].legend()

bp_data = [
    model_df.loc[model_df['has_claim'] == 0, 'pure_premium_capped'],
    model_df.loc[model_df['has_claim'] == 1, 'pure_premium_capped']
]
axes[1].boxplot(bp_data, patch_artist=True, labels=['No Claim', 'Claim'],
                boxprops=dict(facecolor='steelblue', alpha=0.6))
axes[1].set_ylabel('Pure Premium')
axes[1].set_title('Pure Premium by Claim Status')
axes[1].set_yscale('log')

plt.tight_layout()
plt.savefig('pure_premium_distribution.png', dpi=150, bbox_inches='tight')
plt.show()
print("Done: pure_premium_distribution.png")

# ══════════════════════════════════════════════════════════════════════════════
# 2. LIFT CURVE + GINI + DOUBLE LIFT
# ══════════════════════════════════════════════════════════════════════════════
df_lift = model_df[['pure_premium_capped', 'claim_amount']].copy()
df_lift = df_lift.sort_values('pure_premium_capped', ascending=False).reset_index(drop=True)

n = len(df_lift)
df_lift['cum_pct_policies']     = (df_lift.index + 1) / n
df_lift['cum_pct_claim_amount'] = df_lift['claim_amount'].cumsum() / df_lift['claim_amount'].sum()
random_line = np.linspace(0, 1, n)

gini = 2 * np.trapezoid(df_lift['cum_pct_claim_amount'], df_lift['cum_pct_policies']) - 1
print(f"Gini Coefficient: {gini:.4f}")

df_lift2 = model_df[['pure_premium_capped', 'claim_amount']].copy()
df_lift2['decile'] = pd.qcut(df_lift2['pure_premium_capped'], q=10, labels=False) + 1
decile_summary = df_lift2.groupby('decile').agg(
    avg_predicted=('pure_premium_capped', 'mean'),
    avg_actual   =('claim_amount',        'mean')
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle("Model Validation", fontsize=14, fontweight='bold')

axes[0].plot(df_lift['cum_pct_policies'], df_lift['cum_pct_claim_amount'],
             color='steelblue', lw=2, label=f'Model (Gini = {gini:.3f})')
axes[0].plot([0, 1], [0, 1], 'k--', lw=1, label='Random')
axes[0].fill_between(df_lift['cum_pct_policies'],
                     df_lift['cum_pct_claim_amount'],
                     random_line, alpha=0.1, color='steelblue')
axes[0].set_xlabel('Cumulative % of Policies (sorted by predicted PP)')
axes[0].set_ylabel('Cumulative % of Actual Claims')
axes[0].set_title('Lorenz Curve (Lift)')
axes[0].legend()
axes[0].grid(alpha=0.3)

x = decile_summary['decile']
axes[1].plot(x, decile_summary['avg_predicted'], 'o-', color='steelblue',
             lw=2, label='Avg Predicted PP')
axes[1].plot(x, decile_summary['avg_actual'],    's--', color='orange',
             lw=2, label='Avg Actual Claim')
axes[1].set_xlabel('Predicted Pure Premium Decile')
axes[1].set_ylabel('Amount')
axes[1].set_title('Double Lift Chart (Predicted vs Actual by Decile)')
axes[1].legend()
axes[1].grid(alpha=0.3)
axes[1].set_xticks(x)

plt.tight_layout()
plt.savefig('model_validation.png', dpi=150, bbox_inches='tight')
plt.show()
print("Done: model_validation.png")