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
freq_path = data_folder / "clean_business_claims_freq.csv"
sev_path = data_folder / "clean_business_claims_sev.csv"

#load data
business_claims_freq = pd.read_csv(freq_path)
business_claims_sev = pd.read_csv(sev_path)


sev_summarized = business_claims_sev.groupby('policy_id')['claim_amount'].sum().reset_index()


# 2. Merge only the claim_amount onto the frequency table
model_df = pd.merge(
    business_claims_freq, 
    sev_summarized, 
    on='policy_id', 
    how='left'
)
#model_df.to_csv("model_df.csv", index=False)
df=model_df
df['claim_amount'] = pd.to_numeric(df['claim_amount'], errors='coerce').fillna(0)
df['pure_premium'] = df['claim_amount'] / df['exposure']

# ── Select numeric variables ───────────────────────────────────────────────────
vars_to_plot = [
    'production_load', 'energy_backup_score', 'supply_chain_index',
    'avg_crew_exp', 'maintenance_freq', 'safety_compliance',
    'exposure', 'pure_premium'
]

data = df[vars_to_plot].copy()
cols = data.columns.tolist()
n_vars = len(cols)

# ── Build GGpairs-style plot ───────────────────────────────────────────────────
fig, axes = plt.subplots(n_vars, n_vars, figsize=(18, 16))
fig.patch.set_facecolor('#f8f9fa')

np.random.seed(42)

for i, row_var in enumerate(cols):
    for j, col_var in enumerate(cols):
        ax = axes[i, j]
        ax.set_facecolor('#ffffff')

        if i == j:
            # Diagonal: KDE density
            data[row_var].dropna().plot.kde(ax=ax, color='#2196F3', linewidth=2)
            ax.set_ylabel('')

        elif i < j:
            # Upper triangle: Pearson r + stars
            valid = pd.concat([data[col_var], data[row_var]], axis=1).dropna()
            r, p = stats.pearsonr(valid.iloc[:, 0], valid.iloc[:, 1])

            stars = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else ''
            color = plt.cm.RdBu_r((r + 1) / 2)

            ax.set_facecolor(color)
            fontsize = 8 + abs(r) * 16
            txt_color = 'white' if abs(r) > 0.4 else 'black'
            ax.text(0.5, 0.55, f'{r:.2f}', transform=ax.transAxes,
                    ha='center', va='center', fontsize=fontsize,
                    fontweight='bold', color=txt_color)
            ax.text(0.5, 0.25, stars, transform=ax.transAxes,
                    ha='center', va='center', fontsize=10, color=txt_color)

        else:
            # Lower triangle: scatter + regression line
            x = data[col_var].values
            y = data[row_var].values
            valid = ~(np.isnan(x) | np.isnan(y))
            x, y = x[valid], y[valid]

            if len(x) > 1000:
                idx = np.random.choice(len(x), 1000, replace=False)
                x_plot, y_plot = x[idx], y[idx]
            else:
                x_plot, y_plot = x, y

            ax.scatter(x_plot, y_plot, alpha=0.15, s=4, color='#455A64', rasterized=True)
            m, b = np.polyfit(x, y, 1)
            x_line = np.linspace(x.min(), x.max(), 100)
            ax.plot(x_line, m * x_line + b, color='#E53935', linewidth=1.5)

        if i == n_vars - 1:
            ax.set_xlabel(col_var, fontsize=8, rotation=15, ha='right')
        else:
            ax.set_xlabel('')
        if j == 0:
            ax.set_ylabel(row_var, fontsize=8, rotation=45, ha='right', labelpad=30)
        else:
            ax.set_ylabel('')

        ax.tick_params(labelsize=6)
        for spine in ax.spines.values():
            spine.set_edgecolor('#cccccc')

fig.suptitle(
    'Pairwise Correlation Matrix  |  Lower: scatter + regression  |  Diagonal: KDE  |  Upper: Pearson r  (* p<0.05  ** p<0.01  *** p<0.001)',
    fontsize=10, y=1.01, color='#333333'
)

plt.tight_layout()
plt.savefig('ggpairs_correlation.png', dpi=150, bbox_inches='tight')
print("✓ Done")