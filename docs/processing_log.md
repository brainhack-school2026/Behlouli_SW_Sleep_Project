# Processing Log

## Participant exclusion

Date: 2026-06-02

### Reason

Some participants were excluded before generating the final processed dataset.

### Exclusion list

The excluded participants are stored in:

`data/participants_to_exclude.csv`

### Participants excluded

- R57
- R78
- R101
- R148

### Implementation

The exclusion step was added to:

`src/formatchanging.py`

The exclusion is applied after forward-filling `ID participant` and before regional averaging.

### Expected result

Before exclusion:

- 101 participants

After exclusion:

- 97 participants

### Verification

After regenerating the dataset, the final dataset should have:

- 97 rows

The excluded participants should no longer appear in:

`data/processed/final_dataset.csv`

## 2026-06-03

### Machine Learning Preparation

Created machine learning analysis plan.

Objective:
Predict conversion status using slow-wave sleep biomarkers.

Dataset:
data/processed/final_dataset.csv

Participants:
97

Groups:
60 non-converters
37 converters

Planned classifier:
LinearSVC

Validation:
Stratified 10-fold cross-validation

### Added ROC-AUC evaluation

Purpose:

Assess the discriminative ability of the Linear SVM independently of a fixed classification threshold.

Outputs:

- roc_curve.csv
- roc_auc metric

### ROC curve figure

Generated the ROC curve figure for the Linear SVM classifier.

Output:

`figures/ml/roc_curve.png`

### Logistic Regression Sensitivity Analysis

Implemented an alternative linear classifier to evaluate the robustness of machine learning findings.

Output:

results/ml/logistic_regression_metrics.csv

### Logistic Regression Results

A Logistic Regression classifier was trained as a sensitivity analysis.

Main findings:

- Performance remained above chance.
- Linear SVM achieved superior classification performance.
- Results support the existence of a meaningful predictive signal within slow-wave sleep biomarkers.

### Logistic Regression Feature Importance

Extracted Logistic Regression coefficients and ranked variables according to absolute coefficient magnitude.

Output:

results/ml/logistic_regression_feature_importance.csv

### Logistic Regression Feature Importance

The machine learning script was updated to extract and save Logistic Regression coefficients.

Output:

`results/ml/logistic_regression_feature_importance.csv`

Purpose:

Compare the most important biomarkers identified by Linear SVM and Logistic Regression.

### Robust Biomarker Figure

Generated a figure showing biomarkers shared between the top Linear SVM and Logistic Regression feature rankings.

Output:

`figures/ml/robust_biomarkers.png`

### Model Comparison

Created a summary table and figure comparing Linear SVM and Logistic Regression performance.

Outputs:

- results/ml/model_comparison.csv
- figures/ml/model_comparison.png

### Global Feature Classifier

Created a global-feature Linear SVM classifier.

The model averages each slow-wave biomarker across frontal, central, parietal and occipital regions before classification.

Output directory:

`results/ml_global/`

### Regional vs Global Classifier Comparison

A global-feature Linear SVM classifier was compared with the regional Linear SVM classifier.

The global model used slow-wave biomarkers averaged across all four regions.

Main result:

- Regional SVM ROC-AUC: 0.728
- Global SVM ROC-AUC: 0.550

Interpretation:

Removing regional information substantially reduced classification performance, suggesting that regional slow-wave organization is important for predicting phenoconversion.

Outputs:

- `results/ml/regional_vs_global_comparison.csv`
- `figures/ml/regional_vs_global_comparison.png`
