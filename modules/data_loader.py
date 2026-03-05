import pandas as pd

def get_base_probs():
    """
    Returns base probabilities for different pet grades.
    Data extrapolated from stoneage_gacha_system_design.md
    """
    return {
        "SS": 0.000075,  # 0.0075%
        "S": 0.005,      # 0.5%
        "A": 0.05,       # 5%
        "B": 0.2,        # 20%
        "C": 0.744925,   # Remaining
    }

def get_pickup_probs():
    """
    Returns pickup probabilities.
    Data extrapolated from stoneage_gacha_system_design.md
    """
    return {
        "SS_Pickup": 0.0012,  # 0.12%
        "SS_Normal": 0.000075,
        "S": 0.005,
        "A": 0.05,
        "B": 0.2,
        "C": 0.743725,
    }

def get_level_progression():
    """
    Sample level progression for probabilities.
    X = Level, Y = SS Probability
    """
    data = {
        "Level": [1, 5, 10, 15, 20],
        "SS_Prob": [0.00005, 0.000075, 0.0001, 0.0002, 0.0005]
    }
    return pd.DataFrame(data)
