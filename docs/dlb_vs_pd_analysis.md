# DLB versus Parkinson Analysis

## Objective

Evaluate whether slow-wave biomarkers differ between future DLB converters and future Parkinson converters.

## Groups

- DLB: n = 20
- Parkinson: n = 17

The Parkinson group includes both PD and PD-MCI participants.

## Methods

### Candidate biomarkers

The analysis focused on the 10 robust biomarkers identified in the primary conversion analysis.

### Statistical analysis

For each biomarker, an ANCOVA was performed:

Biomarker ~ Clinical Group + UPDRS-I + UPDRS-III

where:

- Clinical Group = DLB or Parkinson
- UPDRS-I and UPDRS-III were included as covariates.

False Discovery Rate (FDR) correction was applied.

### Effect sizes

Cohen's d was calculated for all biomarkers.

## Results

No biomarker survived FDR correction.

The strongest candidate biomarkers were:

| Biomarker | Cohen's d |
|------------|------------|
| occipital_total_N3_pkpk_amp_uV | -0.62 |
| occipital_total_N2_pkpk_amp_uV | -0.45 |

Future DLB converters tended to exhibit lower occipital slow-wave amplitudes than future Parkinson converters.

## Interpretation

These results suggest a possible occipital slow-wave signature associated with conversion subtype.

Because of the limited sample size, these findings should be considered exploratory.

## Final Figures

Final figures were generated to visualize:

- DLB versus Parkinson group distributions;
- candidate biomarker differences;
- ANCOVA p-value ranking.

Outputs:

- `figures/presentation/ancova/hist_dlb_vs_parkinson_occipital_total_N3_pkpk_amp_uV.png`
- `figures/presentation/ancova/hist_dlb_vs_parkinson_occipital_total_N2_pkpk_amp_uV.png`
- `figures/presentation/ancova/summary_dlb_vs_parkinson_ancova.png`
