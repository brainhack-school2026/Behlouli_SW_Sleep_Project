"""
Machine Learning Classification

Objective:
Predict phenoconversion from slow-wave biomarkers.

Input:
data/processed/final_dataset.csv

Output:
results/ml/

Author:
Maya Behlouli

Project:
RBD_SW_sleep_conversion
"""

from pathlib import Path

import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
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
RESULTS_DIR = PROJECT_ROOT / "results" / "ml"
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

feature_cols = [
    f"{region}_{feature}"
    for region in regions
    for feature in base_features
]


X = df[feature_cols]
y = df["converter"]


print("Initial X shape:", X.shape)
print("Initial y shape:", y.shape)

missing_per_feature = X.isna().sum()
print("\nMissing values per feature:")
print(missing_per_feature[missing_per_feature > 0])


ml_data = pd.concat(
    [X, y],
    axis=1
).dropna()

X = ml_data[feature_cols]
y = ml_data["converter"]

print("\nFinal X shape:", X.shape)
print("Final y counts:")
print(y.value_counts())


cv = StratifiedKFold(
    n_splits=10,
    shuffle=True,
    random_state=42,
)


# ============================================================
# Linear SVM
# ============================================================

svm_model = Pipeline([
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


svm_y_pred = cross_val_predict(
    svm_model,
    X,
    y,
    cv=cv,
)

svm_y_score = cross_val_predict(
    svm_model,
    X,
    y,
    cv=cv,
    method="decision_function",
)

svm_auc = roc_auc_score(
    y,
    svm_y_score,
)

fpr, tpr, thresholds = roc_curve(
    y,
    svm_y_score,
)

pd.DataFrame({
    "fpr": fpr,
    "tpr": tpr,
    "threshold": thresholds,
}).to_csv(
    RESULTS_DIR / "roc_curve.csv",
    index=False,
)


svm_metrics = {
    "accuracy": accuracy_score(y, svm_y_pred),
    "balanced_accuracy": balanced_accuracy_score(y, svm_y_pred),
    "precision": precision_score(y, svm_y_pred),
    "recall": recall_score(y, svm_y_pred),
    "f1": f1_score(y, svm_y_pred),
    "roc_auc": svm_auc,
}

pd.Series(svm_metrics).to_csv(
    RESULTS_DIR / "classification_metrics.csv"
)

pd.DataFrame(
    confusion_matrix(y, svm_y_pred),
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


svm_model.fit(X, y)

svm_coef = (
    svm_model
    .named_steps["classifier"]
    .coef_[0]
)

svm_importance = pd.DataFrame({
    "feature": feature_cols,
    "coefficient": svm_coef,
    "abs_coefficient": abs(svm_coef),
}).sort_values(
    "abs_coefficient",
    ascending=False,
)

svm_importance.to_csv(
    RESULTS_DIR / "feature_importance.csv",
    index=False,
)


print("\nLinear SVM metrics:")
for key, value in svm_metrics.items():
    print(f"{key}: {value}")

print("\nLinear SVM confusion matrix:")
print(confusion_matrix(y, svm_y_pred))

print("\nLinear SVM classification report:")
print(classification_report(y, svm_y_pred))

print("\nTop Linear SVM features:")
print(svm_importance.head(20))


# ============================================================
# Logistic Regression sensitivity analysis
# ============================================================

log_model = Pipeline([
    ("scaler", StandardScaler()),
    (
        "classifier",
        LogisticRegression(
            class_weight="balanced",
            max_iter=10000,
            random_state=42,
        )
    ),
])


log_y_pred = cross_val_predict(
    log_model,
    X,
    y,
    cv=cv,
)

log_y_score = cross_val_predict(
    log_model,
    X,
    y,
    cv=cv,
    method="decision_function",
)

log_auc = roc_auc_score(
    y,
    log_y_score,
)

log_metrics = {
    "accuracy": accuracy_score(y, log_y_pred),
    "balanced_accuracy": balanced_accuracy_score(y, log_y_pred),
    "precision": precision_score(y, log_y_pred),
    "recall": recall_score(y, log_y_pred),
    "f1": f1_score(y, log_y_pred),
    "roc_auc": log_auc,
}

pd.Series(log_metrics).to_csv(
    RESULTS_DIR / "logistic_regression_metrics.csv"
)


log_model.fit(X, y)

log_coef = (
    log_model
    .named_steps["classifier"]
    .coef_[0]
)

log_importance = pd.DataFrame({
    "feature": feature_cols,
    "coefficient": log_coef,
    "abs_coefficient": abs(log_coef),
}).sort_values(
    "abs_coefficient",
    ascending=False,
)

log_importance.to_csv(
    RESULTS_DIR / "logistic_regression_feature_importance.csv",
    index=False,
)


print("\nLogistic Regression metrics:")
for key, value in log_metrics.items():
    print(f"{key}: {value}")

print("\nTop Logistic Regression features:")
print(log_importance.head(20))

print("\nDone.")
print("Saved ML outputs in:", RESULTS_DIR)
