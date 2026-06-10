
## Project objective

The objective of this project is to investigate whether slow-wave sleep characteristics are associated with phenoconversion in idiopathic REM Sleep Behavior Disorder patients.

## Original dataset

The original dataset is stored in:

`data/raw/raw.xlsx`

The dataset originally contained:

- 781 rows
- 39 columns

Each row corresponded to a participant-electrode combination.

## Electrode selection

Only the following electrodes were retained:

| Region | Electrodes |
|---|---|
| Frontal | F3, F4 |
| Central | C3, C4 |
| Parietal | P3, P4 |
| Occipital | O1, O2 |

The following electrodes were excluded:

- F7R
- F7RC
- PzRC

## Regional averaging

For each participant, left and right electrodes were averaged within each region:

- Frontal = mean(F3, F4)
- Central = mean(C3, C4)
- Parietal = mean(P3, P4)
- Occipital = mean(O1, O2)

## Regional averaging

For each participant, left and right electrodes were averaged within each region:

- Frontal = mean(F3, F4)
- Central = mean(C3, C4)
- Parietal = mean(P3, P4)
- Occipital = mean(O1, O2)

This aggregation was applied to all slow-wave variables.

## Participant-level dataset

The data were transformed from:

`participant × electrode`

to:

`one row per participant`

The final processed dataset contains:

- 101 participants
- 116 columns

## Participant identifiers

Missing values in `ID participant` corresponded to repeated electrode rows for the same participant.

They were filled using forward fill:

```python
df["ID participant"] = df["ID participant"].ffill()

## Participant exclusion

A participant exclusion step was added before regional averaging.

The excluded participants are listed in:

`data/participants_to_exclude.csv`

This file contains one column:

`ID participant`

The exclusion is applied in:

`src/formatchanging.py`

This step is performed after forward-filling participant IDs and before computing regional averages, ensuring that all electrode-level rows belonging to excluded participants are removed.

After exclusion, the processed dataset should contain 97 participants.
