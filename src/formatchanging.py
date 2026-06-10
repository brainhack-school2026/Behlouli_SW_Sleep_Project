from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "raw.xlsx"

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_dataset.csv"
)

EXCLUSION_FILE = PROJECT_ROOT / "data" / "participants_to_exclude.csv"

df = pd.read_excel(RAW_FILE)

df["ID participant"] = df["ID participant"].ffill()

if EXCLUSION_FILE.exists():
    exclusions = pd.read_csv(EXCLUSION_FILE)

    participants_to_exclude = (
        exclusions["ID participant"]
        .astype(str)
        .str.strip()
        .tolist()
    )

    before_n = df["ID participant"].nunique()

    df = df[
        ~df["ID participant"]
        .astype(str)
        .str.strip()
        .isin(participants_to_exclude)
    ].copy()

    after_n = df["ID participant"].nunique()

    print(f"Excluded participants: {participants_to_exclude}")
    print(f"Participants before exclusion: {before_n}")
    print(f"Participants after exclusion: {after_n}")
else:
    print("No exclusion file found.")

# Remplir les valeurs ID participant manquantes
df["ID participant"] = df["ID participant"].ffill()

# Garder seulement les électrodes d'intérêt
region_map = {
    "F3": "frontal",
    "F4": "frontal",
    "C3": "central",
    "C4": "central",
    "P3": "parietal",
    "P4": "parietal",
    "O1": "occipital",
    "O2": "occipital",
}

df = df[df["chan_label"].isin(region_map.keys())].copy()
df["region"] = df["chan_label"].map(region_map)

# Variables slow-wave à transformer en variables régionales
metadata_cols = [
    "ID participant",
    "ID participant.1",
    "filename",
    "chan_label",
    "Code Ron",
    "Conversion",
    "Sous-type (2=PD cognition normale, 3=PD-MCI, 4=DLB, 5=MSA, 6=PDD)",
    "Âge à la PSG",
    "UPDRS-I-2 Hallucinations",
    "UPDRS-I Total",
    "UPDRS-III Total -0.5",
    "Durée de suivi",
    "conversion_clean",
    "Group",
    "region",
]

regional_vars = [
    col for col in df.columns
    if col not in metadata_cols
    and pd.api.types.is_numeric_dtype(df[col])
]

regional = (
    df
    .groupby(["filename", "region"])[regional_vars]
    .mean()
    .reset_index()
)

wide = regional.pivot(
    index="filename",
    columns="region",
    values=regional_vars
)

wide.columns = [
    f"{region}_{feature}"
    for feature, region in wide.columns
]

wide = wide.reset_index()

# Variables non régionales conservées une fois par fichier/participant
clinical_cols = [
    "filename",
    "ID participant",
    "ID participant.1",
    "Code Ron",
    "Conversion",
    "Sous-type (2=PD cognition normale, 3=PD-MCI, 4=DLB, 5=MSA, 6=PDD)",
    "Âge à la PSG",
    "UPDRS-I-2 Hallucinations",
    "UPDRS-I Total",
    "UPDRS-III Total -0.5",
    "Durée de suivi",
    "conversion_clean",
    "Group",
]

clinical = (
    df[clinical_cols]
    .drop_duplicates(subset="filename")
)

final_dataset = wide.merge(
    clinical,
    on="filename",
    how="left"
)

# Nettoyage de la variable de conversion
# Règle:
# Conversion = "Oui" -> convertisseur
# Conversion vide -> non-convertisseur

final_dataset["converter"] = (
    final_dataset["Conversion"]
    .notna()
    .astype(int)
)

final_dataset["conversion_status"] = final_dataset["converter"].map({
    1: "Converter",
    0: "Non-converter",
})

subtype_col = "Sous-type (2=PD cognition normale, 3=PD-MCI, 4=DLB, 5=MSA, 6=PDD)"

subtype_map = {
    2: "PD",
    3: "PD-MCI",
    4: "DLB",
    5: "MSA",
    6: "PDD",
}

final_dataset["conversion_subtype"] = (
    final_dataset[subtype_col]
    .map(subtype_map)
    .fillna("Non-converter")
)

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
final_dataset.to_csv(OUTPUT_FILE, index=False)

print("Saved:", OUTPUT_FILE)
print("Shape:", final_dataset.shape)
print(final_dataset["converter"].value_counts(dropna=False))
print(final_dataset["conversion_subtype"].value_counts(dropna=False))
