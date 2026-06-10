# Statistical Analysis

## Objective

The statistical objective is to compare slow-wave sleep characteristics between converters and non-converters while accounting for regional brain differences and clinical covariates.

## Analysis type

Repeated-measures ANCOVA was used.

## Model structure

For each slow-wave variable, the following model was estimated:

`value ~ group × region + UPDRS-I + UPDRS-III + participant`

## Factors

### Between-subject factor

- Group:
  - Converter
  - Non-converter

### Within-subject factor

- Region:
  - Frontal
  - Central
  - Parietal
  - Occipital

## Covariates

The following clinical variables were included as covariates:

- UPDRS-I Total
- UPDRS-III Total -0.5

These covariates were included because they may differ between converters and non-converters and could confound group differences in slow-wave characteristics.

## Repeated-measures structure

Each participant contributes multiple regional values. Therefore, participant identity was included in the model to account for repeated measurements within participants.

## Effects tested

For each slow-wave variable, the model tests:

1. Group effect  
   Whether converters differ from non-converters.

2. Region effect  
   Whether slow-wave values differ across brain regions.

3. Group × Region interaction  
   Whether group differences depend on brain region.

4. Covariate effects  
   Whether UPDRS-I or UPDRS-III explain variance in the slow-wave measure.

## Outputs

The script saves results in:

`results/ancova/`

Files generated:

- `repeated_measures_ancova_all_effects.csv`
- `repeated_measures_ancova_group_effects_fdr.csv`
- `adjusted_means_by_group_and_region.csv`

## Script

The analysis script is located at:

`src/repeated_measures_ancova.py`

To run the analysis:

```bash
python src/repeated_measures_ancova.py

## Final ANCOVA Visualizations

Presentation-ready ANCOVA visualizations were created for:

1. Converter versus non-converter comparisons.
2. DLB versus Parkinson exploratory comparisons.

Histograms were generated to show group distributions for selected biomarkers.

Summary barplots show the statistical strength of group effects using -log10 p-values.
