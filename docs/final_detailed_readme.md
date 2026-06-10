# Regional Slow-Wave Biomarkers of Phenoconversion in Isolated REM Sleep Behavior Disorder

**BrainHack School 2026 Final Project**
**Maya Behlouli**
Center for Advanced Research in Sleep Medicine, Université de Montréal

> Can regional NREM slow-wave sleep biomarkers help predict phenoconversion in isolated REM Sleep Behavior Disorder?

---

## About Me

I am a Master's student in Neuroengineering with a background in neuroscience. My research focuses on sleep EEG biomarkers in isolated REM Sleep Behavior Disorder (iRBD), with a particular interest in understanding how sleep physiology can help characterize early neurodegenerative risk.

During BrainHack School, my goal was to transition from previous R-based and partially manual workflows toward a fully reproducible Python-based analysis pipeline using Git, GitHub, Jupyter notebooks, and machine learning tools.

---

## Project Summary

Isolated REM Sleep Behavior Disorder (iRBD) is a prodromal condition strongly associated with future alpha-synucleinopathies such as Parkinson's Disease (PD) and Dementia with Lewy Bodies (DLB).

Previous studies have shown that patients who later phenoconvert exhibit alterations in NREM slow-wave sleep characteristics. This project investigates whether regional slow-wave biomarkers can be used not only to describe group differences but also to support individual-level prediction of phenoconversion.

The project develops a reproducible workflow to process pre-extracted sleep EEG features, construct regional biomarkers, compare converters and non-converters, train interpretable classifiers, and identify robust physiological predictors.

---

## Introduction

iRBD is one of the strongest clinical predictors of future alpha-synucleinopathies. However, the timing and subtype of phenoconversion remain highly variable.

This raises an important question: can sleep EEG biomarkers provide early information about future neurodegeneration?

Slow waves during NREM sleep reflect large-scale cortical synchronization. Because neurodegenerative processes may alter cortical physiology before overt clinical symptoms emerge, slow-wave characteristics may serve as promising biomarkers of disease progression.

This project focuses on regional slow-wave biomarkers extracted from N2 and N3 sleep and evaluates whether their spatial organization across the brain improves prediction of phenoconversion.

---

## Main Objectives

1. Build a reproducible Python workflow for slow-wave EEG biomarker analysis.
2. Standardize the dataset into participant-level regional features.
3. Compare converters and non-converters using repeated-measures ANCOVA.
4. Train an interpretable machine learning classifier to predict conversion status.
5. Identify robust slow-wave biomarkers using model coefficients.
6. Test whether regional features outperform globally averaged features.
7. Explore whether future DLB and Parkinson converters show distinct slow-wave profiles.

---

## Tools

This project uses the following tools and technologies:

* **Git** and **GitHub** for version control and collaboration.
* **Python** for scripting and reproducible analyses.
* **Jupyter Notebooks** for transparent workflows and reporting.
* **pandas** and **NumPy** for data manipulation.
* **statsmodels** for ANCOVA and statistical modeling.
* **scikit-learn** for machine learning classification.
* **matplotlib** for scientific visualization.
* **Markdown** for project documentation.

These tools reflect the open-science and reproducibility principles emphasized during BrainHack School.

---

## Data

The dataset contains pre-extracted slow-wave EEG features from iRBD participants. The analyses begin from previously extracted slow-wave characteristics rather than raw EEG recordings.

After preprocessing and participant exclusions, the final dataset included:

| Group             | N  |
| ----------------- | -- |
| Non-converters    | 60 |
| DLB converters    | 20 |
| PD converters     | 9  |
| PD-MCI converters | 8  |

For the exploratory subtype analysis, PD and PD-MCI participants were combined:

| Group     | N  |
| --------- | -- |
| DLB       | 20 |
| Parkinson | 17 |

---

## Regional Feature Construction

Slow-wave features were averaged across homologous left and right electrodes to create four regional biomarkers:

| Region    | Electrodes |
| --------- | ---------- |
| Frontal   | F3 / F4    |
| Central   | C3 / C4    |
| Parietal  | P3 / P4    |
| Occipital | O1 / O2    |

This approach reduces dimensionality while preserving spatial information and allows testing whether conversion risk depends on regional slow-wave organization rather than global averages alone.

---

## Analysis Workflow

The workflow was designed to answer the research question at three complementary levels:

1. **Group-level differences** using repeated-measures ANCOVA.
2. **Individual-level prediction** using Linear SVM classification.
3. **Biomarker interpretation** using model coefficients, Logistic Regression, and regional-versus-global comparisons.

### Methods Overview

This figure summarizes the complete analytical workflow, from participant selection and regional feature construction to statistical analyses, machine learning classification, and biomarker interpretation.

---

## Project Deliverables

The final project includes:

* A documented and version-controlled GitHub repository.
* Python scripts for preprocessing, ANCOVA, and machine learning.
* Jupyter notebooks for quality control, visualization, and reporting.
* Repeated-measures ANCOVA results.
* Linear SVM and Logistic Regression analyses.
* Regional versus global classifier comparisons.
* Exploratory DLB versus Parkinson analyses.
* Publication-ready figures.
* Comprehensive Markdown documentation.

---

## Results

### Converter versus Non-Converter ANCOVA

Repeated-measures ANCOVA identified several slow-wave characteristics that differed significantly between converters and non-converters after controlling for UPDRS-I and UPDRS-III scores.

The strongest group effects involved:

* Slow-wave frequency
* Transition frequency
* Slope
* Amplitude
* Slow-wave counts

---

### Machine Learning Classification

A Linear Support Vector Machine (SVM) classifier was trained to predict conversion status using regional slow-wave biomarkers.

The model used standardized features, stratified cross-validation, and cross-validated predictions.

| Metric            | Value |
| ----------------- | ----- |
| Accuracy          | 0.688 |
| Balanced Accuracy | 0.682 |
| Precision         | 0.607 |
| Recall            | 0.654 |
| F1-score          | 0.630 |
| ROC-AUC           | 0.728 |

These results indicate that regional slow-wave biomarkers contain meaningful predictive information regarding future phenoconversion.

---

### Predictive Biomarkers

Feature coefficients extracted from the Linear SVM identified the biomarkers contributing most strongly to classification performance.

The most predictive features included:

* Slow-wave amplitude
* Frequency
* Transition frequency
* Slope
* Slow-wave counts

across frontal, central, parietal, and occipital regions.

To evaluate robustness, Logistic Regression was used as a complementary model. Biomarkers identified by both approaches were considered stronger candidates.

### Brain Map of Robust Biomarkers

This figure summarizes the most robust biomarkers and their anatomical distribution across cortical regions.

---

### Regional versus Global Comparison

To determine whether spatial information improves prediction, a second classifier was trained using globally averaged slow-wave features.

| Model               | ROC-AUC |
| ------------------- | ------- |
| Regional Linear SVM | 0.728   |
| Global Linear SVM   | 0.550   |

The regional model substantially outperformed the global model, suggesting that the spatial distribution of slow-wave biomarkers contains important predictive information.

---

### DLB versus Parkinson Exploratory Analysis

Among converters, an exploratory analysis compared future DLB converters with future Parkinson converters.

No biomarker survived False Discovery Rate (FDR) correction. However, the strongest candidate effects involved occipital slow-wave amplitude.

| Biomarker                      | Cohen's d |
| ------------------------------ | --------- |
| occipital_total_N3_pkpk_amp_uV | -0.62     |
| occipital_total_N2_pkpk_amp_uV | -0.45     |

Negative effect sizes indicate lower occipital slow-wave amplitude in future DLB converters compared with future Parkinson converters.

---

## Conclusions

### Can slow-wave biomarkers predict conversion?

Yes. Regional NREM slow-wave biomarkers contain information associated with future phenoconversion risk in iRBD. The Linear SVM achieved moderate predictive performance with a ROC-AUC of approximately 0.73.

### Does regional information matter?

Yes. Regional models clearly outperformed global models, indicating that spatial organization is an important component of predictive information.

### Which biomarkers appear most relevant?

The most robust biomarkers involved:

* Slow-wave amplitude
* Frequency
* Transition frequency
* Slope
* Slow-wave counts

across frontal, central, parietal, and occipital regions.

### What about DLB versus Parkinson?

The DLB versus Parkinson comparison remains exploratory. Although no biomarker survived FDR correction, occipital N2 and N3 amplitudes showed the largest effect sizes.

### Overall Conclusion

This project supports the hypothesis that sleep EEG biomarkers may help characterize prodromal neurodegeneration in iRBD and highlights the importance of regional slow-wave organization for predicting phenoconversion risk.

---

## Project Timeline (Python Date Format)

```python
project_start = "2026-01"
brainhack_school = "2026-02"
analysis_completion = "2026-03"
final_presentation = "2026-03"
```

---

## Guide to Reproducibility

### Clone the Repository

```bash
git clone <repository_url>
cd RBD_SW_sleep_conversion
```

### Create the Environment

```bash
conda env create -f environment.yml
conda activate RBD_SW_sleep_conversion
```

### Run the Main Pipeline

```bash
python src/run_pipeline.py
```

### Run Individual Analyses

Preprocessing and regional feature construction:

```bash
python src/formatchanging.py
```

Repeated-measures ANCOVA:

```bash
python src/repeated_measures_ancova.py
```

Regional machine learning classifier:

```bash
python src/train_classifier.py
```

Global feature classifier:

```bash
python src/train_classifier_global_features.py
```

### Explore Notebooks

Recommended order:

```text
notebooks/01_data_qc.ipynb
notebooks/02_quality_control.ipynb
notebooks/03_machine_learning_results.ipynb
notebooks/04_machine_learning_figures.ipynb
notebooks/05_final_biomarker_summary.ipynb
notebooks/06_presentation_figures.ipynb
notebooks/08_dlb_vs_pd_analysis.ipynb
```

---

## Documentation

| File                         | Description                                          |
| ---------------------------- | ---------------------------------------------------- |
| docs/data_processing.md      | Data preprocessing and regional feature construction |
| docs/statistical_analysis.md | ANCOVA and statistical methods                       |
| docs/machine_learning.md     | Machine learning pipeline                            |
| docs/dlb_vs_pd_analysis.md   | DLB versus Parkinson exploratory analysis            |
| docs/analysis_log.md         | Summary of completed analyses                        |
| docs/processing_log.md       | Processing notes                                     |

---

## Acknowledgements

I would like to thank the BrainHack School team and the Center for Advanced Research in Sleep Medicine for their support, mentorship, and feedback throughout this project.

---

## References

* BrainHack School project repository: `<repository_url>`
* scikit-learn documentation
* statsmodels documentation
* pandas documentation
* matplotlib documentation
* Relevant literature on iRBD, sleep EEG biomarkers, and alpha-synucleinopathies.
