# Machine Learning Classification

## Objective

Predict phenoconversion using slow-wave sleep biomarkers.

Target variable:

- converter
  - 0 = non-converter
  - 1 = converter

Dataset:

- final_dataset.csv

Participants:

- 97 participants
- 60 non-converters
- 37 converters

## Feature Selection

Features were selected from variables showing significant group effects in the repeated-measures ANCOVA.

Selected biomarker categories:

- Frequency
- Transition frequency
- Slope
- Amplitude
- Slow-wave count

Regions included:

- Frontal
- Central
- Parietal
- Occipital

Model planned:

- Linear Support Vector Machine (LinearSVC)

Validation strategy:

- Stratified 10-fold cross-validation

Performance metrics:

- Accuracy
- Balanced Accuracy
- Precision
- Recall
- F1-score

Feature importance:

- Linear SVM coefficients

## First Linear SVM Results

Model:
LinearSVC

Validation:
Stratified 10-fold cross-validation

Performance:

- Accuracy:0.6875
- Balanced Accuracy:0.6821862348178138
- Precision:0.6071428571428571
- Recall: 0.6538461538461539
- F1-score:0.6296296296296297


## Results Notebook

A dedicated notebook was created:

`notebooks/03_machine_learning_results.ipynb`

Purpose:

- Evaluate classifier performance
- Interpret confusion matrix
- Analyze feature importance
- Generate final figures

Input directory:

`results/ml/`

Output directory:

`figures/ml/`

## First Linear SVM Results

Validation:

- Stratified 10-fold cross-validation

Performance:

- Accuracy: 68.8%
- Balanced Accuracy: 68.2%
- Precision: 60.7%
- Recall: 65.4%
- F1-score: 63.0%

Interpretation:

The classifier performed above chance level and showed moderate ability to distinguish converters from non-converters using slow-wave sleep biomarkers.

## Confusion Matrix

|                 | Predicted Non-converter | Predicted Converter |
|-----------------|-------------------------|---------------------|
| True Non-converter | 27 | 11 |
| True Converter | 9 | 17 |

Interpretation:

- 27 non-converters were correctly classified.
- 17 converters were correctly classified.
- 11 non-converters were incorrectly classified as converters.
- 9 converters were missed by the classifier.

The classifier demonstrated moderate sensitivity for detecting phenoconversion.

## Top Predictive Biomarkers

Top 10 features ranked by absolute SVM coefficient:

1. occipital_total_sw_count
2. occipital_total_N2_pkpk_amp_uV
3. frontal_total_slope_0_min
4. central_total_trans_freq_Hz
5. parietal_total_trans_freq_Hz
6. parietal_total_N2_freq_Hz
7. central_total_freq_Hz
8. occipital_total_slope_0_min
9. occipital_total_N3_pkpk_amp_uV
10. parietal_total_sw_count

Main observation:

The classifier relied primarily on occipital and parietal slow-wave features, particularly wave counts, frequency measures, amplitudes and slopes.

## Machine Learning Figures

A dedicated notebook was created:

notebooks/04_machine_learning_figures.ipynb

Purpose:

- Generate publication-ready figures
- Save figures as PNG files
- Separate visualization from statistical analyses

## ROC-AUC Evaluation

A receiver operating characteristic (ROC) analysis was added to evaluate classifier performance independently of a fixed classification threshold.

Outputs:

- results/ml/roc_curve.csv

Metric:

- ROC-AUC

## ROC-AUC Evaluation

The Linear SVM achieved:

- ROC-AUC: 0.728

This indicates moderate discriminative ability between converters and non-converters, independently of a fixed classification threshold.

## ROC Curve Figure

File:

`figures/ml/roc_curve.png`

Purpose:

Visualize the Linear SVM classifier's ability to distinguish converters from non-converters across classification thresholds.

The ROC-AUC was 0.728.


## Sensitivity Analysis

Purpose:

Evaluate whether the identified biomarkers remain predictive when using an alternative linear classifier.

Model:

Logistic Regression

Rationale:

If both Linear SVM and Logistic Regression identify similar biomarkers and achieve comparable performance, confidence in the findings increases.

## Sensitivity Analysis

A Logistic Regression classifier was trained using the same features and cross-validation strategy.

Results:

| Metric | Linear SVM | Logistic Regression |
|----------|----------:|----------:|
| Accuracy | 0.688 | 0.578 |
| Balanced Accuracy | 0.682 | 0.578 |
| Precision | 0.607 | 0.484 |
| Recall | 0.654 | 0.577 |
| F1-score | 0.630 | 0.526 |
| ROC-AUC | 0.728 | 0.642 |

Interpretation:

The Linear SVM consistently outperformed Logistic Regression across all evaluation metrics.

However, the Logistic Regression classifier still achieved performance above chance level, suggesting that the predictive signal is not specific to a single machine learning algorithm.

## Feature Stability Analysis

Purpose:

Evaluate whether the most predictive biomarkers identified by the Linear SVM are also identified by Logistic Regression.

Approach:

- Extract Logistic Regression coefficients
- Rank variables by absolute coefficient magnitude
- Compare feature rankings between classifiers

Rationale:

Biomarkers identified across multiple models are more likely to represent robust physiological predictors.

## Feature Stability Analysis

The top 15 biomarkers identified by the Linear SVM and Logistic Regression models were compared.

Features present in both rankings were considered robust biomarkers.

Output:

results/ml/common_biomarkers.csv


## Robust Biomarkers

The top 15 features identified by the Linear SVM and Logistic Regression models were compared.

Ten biomarkers were shared between both classifiers:

- central_total_N3_pkpk_amp_uV
- central_total_freq_Hz
- central_total_trans_freq_Hz
- frontal_total_slope_0_min
- frontal_total_sw_count
- occipital_total_N2_pkpk_amp_uV
- occipital_total_N3_pkpk_amp_uV
- occipital_total_slope_0_min
- parietal_total_N2_freq_Hz
- parietal_total_sw_count

Interpretation:

These biomarkers may represent the most robust physiological predictors of phenoconversion, as they were consistently identified across two different linear classification approaches.

## Robust Biomarker Figure

File:

`figures/ml/robust_biomarkers.png`

Purpose:

Visualize biomarkers consistently identified among the top predictive features by both Linear SVM and Logistic Regression.

Robust biomarkers were defined as features appearing in the top 15 rankings of both models.

Interpretation:

These features may represent the most stable physiological predictors of phenoconversion across linear classification approaches.

## Model Comparison

Linear SVM and Logistic Regression performances were directly compared using:

- Accuracy
- Balanced Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Output:

`results/ml/model_comparison.csv`
## Final Biomarker Summary

A final biomarker summary table was created to identify biomarkers supported by both statistical and machine learning analyses.

Criteria:

- Significant ANCOVA group effect
- Present among robust machine learning biomarkers

Output:

`results/ml/final_biomarker_summary.csv`

## Biomarker Discovery Workflow

File:

`figures/ml/biomarker_discovery_workflow.png`

Purpose:

Summarize the complete analytical workflow used to identify robust slow-wave biomarkers associated with phenoconversion.

The workflow integrates:

- preprocessing;
- repeated measures ANCOVA;
- machine learning classification;
- feature stability analysis;
- robust biomarker identification.

## Global Feature Classifier

A second Linear SVM classifier was trained using global slow-wave features averaged across frontal, central, parietal and occipital regions.

Purpose:

To test whether slow-wave characteristics can predict phenoconversion without explicitly using regional brain information.

This model answers a different question from the regional classifier:

- Regional classifier: Which brain regions and features predict conversion?
- Global classifier: Can overall slow-wave characteristics predict conversion?

Outputs:

`results/ml_global/`


## Regional vs Global Feature Comparison

A second classifier was trained using globally averaged slow-wave features.

Results:

| Metric | Regional SVM | Global SVM |
|----------|----------:|----------:|
| Accuracy | 0.688 | 0.563 |
| Balanced Accuracy | 0.682 | 0.566 |
| Precision | 0.607 | 0.450 |
| Recall | 0.654 | 0.581 |
| F1-score | 0.630 | 0.507 |
| ROC-AUC | 0.728 | 0.550 |

Interpretation:

Classification performance dropped substantially when regional information was removed.

This suggests that the spatial distribution of slow-wave biomarkers contains important information related to phenoconversion risk.

## Regional vs Global Feature Classifier

A global-feature classifier was trained to evaluate whether regional brain information improves prediction.

The global classifier averaged each slow-wave biomarker across frontal, central, parietal and occipital regions before classification.

### Results

| Metric | Regional SVM | Global SVM |
|---|---:|---:|
| Accuracy | 0.688 | 0.563 |
| Balanced Accuracy | 0.682 | 0.566 |
| Precision | 0.607 | 0.450 |
| Recall | 0.654 | 0.581 |
| F1-score | 0.630 | 0.507 |
| ROC-AUC | 0.728 | 0.550 |

### Interpretation

The regional classifier substantially outperformed the global classifier.

This suggests that the spatial distribution of slow-wave biomarkers contains important predictive information for phenoconversion.

In other words, conversion risk is not captured only by overall slow-wave characteristics, but also by where these characteristics occur across brain regions.
