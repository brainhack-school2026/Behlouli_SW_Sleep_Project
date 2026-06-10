from pathlib import Path
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.stats.anova as anova
from statsmodels.stats.multitest import multipletests


from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "final_dataset.csv"
RESULTS_DIR = PROJECT_ROOT / "results" / "ancova"


df = pd.read_csv(DATA_FILE)


# --------------------------------------------------
# Variables de base
# --------------------------------------------------

id_col = "filename"
group_col = "conversion_status"
covariates = [
    "UPDRS-I Total",
    "UPDRS-III Total -0.5",
]

regions = ["frontal", "central", "parietal", "occipital"]


# --------------------------------------------------
# Variables d'ondes lentes à tester
# --------------------------------------------------

slow_wave_variables = [
    "density_sw",
    "total_N2_sw_count",
    "total_N3_sw_count",
    "total_sw_count",
    "total_N2_sw_sec",
    "total_N3_sw_sec",
    "total_sw_sec",
    "total_trans_freq_Hz",
    "total_slope_min_max",
    "total_slope_0_min",
    "total_freq_Hz",
    "total_pkpk_amp_uV",
    "total_N2_freq_Hz",
    "total_N3_freq_Hz",
    "total_N2_trans_freq_Hz",
    "total_N3_trans_freq_Hz",
    "total_N2_slope_0_min",
    "total_N3_slope_0_min",
    "total_N2_pkpk_amp_uV",
    "total_N3_pkpk_amp_uV",
]


# --------------------------------------------------
# Fonction : transformer large -> long
# --------------------------------------------------

def make_long_dataset(df, variable):
    region_cols = {
        region: f"{region}_{variable}"
        for region in regions
    }

    needed_cols = (
        [id_col, group_col]
        + covariates
        + list(region_cols.values())
    )

    temp = df[needed_cols].copy()

    long_df = temp.melt(
        id_vars=[id_col, group_col] + covariates,
        value_vars=list(region_cols.values()),
        var_name="region",
        value_name="value",
    )

    long_df["region"] = (
        long_df["region"]
        .str.replace(f"_{variable}", "", regex=False)
    )

    long_df["variable"] = variable

    return long_df


# --------------------------------------------------
# Fonction : ANCOVA à mesures répétées
# --------------------------------------------------

def run_repeated_measures_ancova(long_df, variable):
    clean_df = long_df.dropna(
        subset=[
            "value",
            group_col,
            "region",
            *covariates,
        ]
    ).copy()

    formula = (
        'value ~ C(conversion_status) * C(region) '
        '+ Q("UPDRS-I Total") '
        '+ Q("UPDRS-III Total -0.5") '
        '+ C(filename)'
    )

    model = smf.ols(formula, data=clean_df).fit()

    table = anova.anova_lm(model, typ=2)
    table = table.reset_index().rename(columns={"index": "effect"})
    table["variable"] = variable

    return table, model, clean_df


# --------------------------------------------------
# Fonction : moyennes ajustées
# --------------------------------------------------

def adjusted_means(model, clean_df, variable):
    mean_updrs_1 = clean_df["UPDRS-I Total"].mean()
    mean_updrs_3 = clean_df["UPDRS-III Total -0.5"].mean()

    reference_filename = clean_df["filename"].iloc[0]

    prediction_grid = pd.DataFrame(
        [
            {
                "filename": reference_filename,
                "conversion_status": group,
                "region": region,
                "UPDRS-I Total": mean_updrs_1,
                "UPDRS-III Total -0.5": mean_updrs_3,
            }
            for group in clean_df["conversion_status"].unique()
            for region in regions
        ]
    )

    prediction_grid["adjusted_mean"] = model.predict(prediction_grid)
    prediction_grid["variable"] = variable

    return prediction_grid


# --------------------------------------------------
# Boucle principale
# --------------------------------------------------

all_anova_tables = []
all_adjusted_means = []

for variable in slow_wave_variables:
    print(f"Running repeated-measures ANCOVA for: {variable}")

    long_df = make_long_dataset(df, variable)

    table, model, clean_df = run_repeated_measures_ancova(
        long_df,
        variable
    )

    means = adjusted_means(
        model,
        clean_df,
        variable
    )

    all_anova_tables.append(table)
    all_adjusted_means.append(means)


anova_results = pd.concat(all_anova_tables, ignore_index=True)
adjusted_means_results = pd.concat(all_adjusted_means, ignore_index=True)


# --------------------------------------------------
# Correction FDR pour les effets de groupe
# --------------------------------------------------

group_effects = anova_results[
    anova_results["effect"] == "C(conversion_status)"
].copy()

reject, p_fdr, _, _ = multipletests(
    group_effects["PR(>F)"],
    method="fdr_bh"
)

group_effects["p_fdr"] = p_fdr
group_effects["significant_fdr"] = reject


# --------------------------------------------------
# Sauvegarde
# --------------------------------------------------

anova_results.to_csv(
    RESULTS_DIR / "repeated_measures_ancova_all_effects.csv",
    index=False
)

group_effects.to_csv(
    RESULTS_DIR / "repeated_measures_ancova_group_effects_fdr.csv",
    index=False
)

adjusted_means_results.to_csv(
    RESULTS_DIR / "adjusted_means_by_group_and_region.csv",
    index=False
)

print("\nDone.")
print("Saved results in:", RESULTS_DIR)
