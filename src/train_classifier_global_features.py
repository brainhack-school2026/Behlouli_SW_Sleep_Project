"""
Global Slow-Wave Feature Classifier

Objective:
Train a classifier using global slow-wave features averaged across brain regions.

This model tests whether slow-wave characteristics can predict phenoconversion
without using regional brain information.

Input:
data/processed/final_dataset.csv

Output:
results/ml_global/

Author:
Maya Behlouli
"""

from pathlib import Path

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = PROJECT_ROOT / "data" / "processed" / "final_dataset.csv"
RESULTS_DIR = PROJECT_ROOT / "results" / "ml_global"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)


df = pd.read_csv(DATA_FILE)


base_features = [
    "total_trans_freq_Hz",
    "total_freq_Hz",
    "total_N3_trans_freq_Hz",
    "total_N3_freq_Hz",
    "total_N2_trans_freq_Hz",
    "total_N2_freq_Hz",
    "total_slope_min_max",
    "total_slope_0_min",
    "total_N2_slope_0_min",
    "total_pkpk_amp_uV",
    "total_N2_pkpk_amp_uV",
    "total_N3_pkpk_amp_uV",
    "total_sw_count",
    "total_N3_sw_count",
]

regions = [
    "frontal",
    "central",
    "parietal",
    "occipital",
]


global_feature_cols = []

for feature in base_features:

    regional_cols = [
        f"{region}_{feature}"
        for region in regions
    ]

    global_col = f"global_{feature}"

    df[global_col] = df[
        regional_cols
    ].mean(axis=1)

    global_feature_cols.append(global_col)


X = df[global_feature_cols]
y = df["converter"]


print("Initial X shape:", X.shape)
print("Initial y shape:", y.shape)

missing_per_feature = X.isna().sum()
print("\nMissing values per global feature:")
print(missing_per_feature[missing_per_feature > 0])


ml_data = pd.concat(
    [X, y],
    axis=1
).dropna()

X = ml_data[global_feature_cols]
y = ml_data["converter"]


print("\nFinal X shape:", X.shape)
print("Final y counts:")
print(y.value_counts())


model = Pipeline([
    ("scaler", StandardScaler()),
    (
        "classifier",
        LinearSVC(
            class_weight="balanced",
            max_iter=10000,
            random_state=42,
        )
    ),
])


cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42,
)


y_pred = cross_val_predict(
    model,
    X,
    y,
    cv=cv,
)

y_score = cross_val_predict(
    model,
    X,
    y,
    cv=cv,
    method="decision_function",
)


auc = roc_auc_score(
    y,
    y_score,
)

fpr, tpr, thresholds = roc_curve(
    y,
    y_score,
)


metrics = {
    "accuracy": accuracy_score(y, y_pred),
    "balanced_accuracy": balanced_accuracy_score(y, y_pred),
    "precision": precision_score(y, y_pred),
    "recall": recall_score(y, y_pred),
    "f1": f1_score(y, y_pred),
    "roc_auc": auc,
}


pd.Series(metrics).to_csv(
    RESULTS_DIR / "classification_metrics.csv"
)

pd.DataFrame(
    confusion_matrix(y, y_pred),
    index=[
        "true_non_converter",
        "true_converter",
    ],
    columns=[
        "pred_non_converter",
        "pred_converter",
    ],
).to_csv(
    RESULTS_DIR / "confusion_matrix.csv"
)

pd.DataFrame({
    "fpr": fpr,
    "tpr": tpr,
    "threshold": thresholds,
}).to_csv(
    RESULTS_DIR / "roc_curve.csv",
    index=False,
)


model.fit(X, y)

coef = (
    model
    .named_steps["classifier"]
    .coef_[0]
)

feature_importance = pd.DataFrame({
    "feature": global_feature_cols,
    "coefficient": coef,
    "abs_coefficient": abs(coef),
}).sort_values(
    "abs_coefficient",
    ascending=False,
)

feature_importance.to_csv(
    RESULTS_DIR / "feature_importance.csv",
    index=False,
)


print("\nGlobal Linear SVM metrics:")
for key, value in metrics.items():
    print(f"{key}: {value}")

print("\nConfusion matrix:")
print(confusion_matrix(y, y_pred))

print("\nClassification report:")
print(classification_report(y, y_pred))

print("\nTop global features:")
print(feature_importance.head(20))

print("\nDone.")
print("Saved global model outputs in:", RESULTS_DIR)
