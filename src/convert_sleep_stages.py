def convert_stage_to_standard(stage):
    """
    Convertit différents formats de stades de sommeil vers un format standard.

    Format standard utilisé :
    - W = Wake
    - N1 = Non-REM stage 1
    - N2 = Non-REM stage 2
    - N3 = Non-REM stage 3 / slow-wave sleep
    - REM = REM sleep
    - UNKNOWN = stade non reconnu
    """

    if stage is None:
        return "UNKNOWN"

    stage = str(stage).strip().upper()

    mapping = {
        "WAKE": "W",
        "W": "W",
        "0": "W",

        "N1": "N1",
        "1": "N1",
        "S1": "N1",

        "N2": "N2",
        "2": "N2",
        "S2": "N2",

        "N3": "N3",
        "3": "N3",
        "S3": "N3",
        "S4": "N3",
        "4": "N3",

        "REM": "REM",
        "R": "REM",
        "5": "REM",
    }

    return mapping.get(stage, "UNKNOWN")


def is_slow_wave_sleep(stage):
    """
    Retourne True si le stade correspond au sommeil lent profond.
    """

    standard_stage = convert_stage_to_standard(stage)
    return standard_stage == "N3"
