import numpy as np
import pandas as pd

def run_gacha_simulation(probs, n_draws, n_trials=1000):
    """
    Simulates gacha draws for multiple trials.
    Returns counts of each grade for each trial.
    """
    grades = list(probs.keys())
    p_values = list(probs.values())
    
    # Validation: Sum of probabilities should be 1.0 (approximately)
    total_p = sum(p_values)
    if not (0.999 <= total_p <= 1.001):
        # Normalize
        p_values = [p / total_p for p in p_values]
        
    results = []
    
    for _ in range(n_trials):
        draws = np.random.choice(grades, size=n_draws, p=p_values)
        unique, counts = np.unique(draws, return_counts=True)
        trial_res = dict(zip(unique, counts))
        # Fill missing grades with 0
        for grade in grades:
            if grade not in trial_res:
                trial_res[grade] = 0
        results.append(trial_res)
        
    return pd.DataFrame(results)

def get_simulation_summary(df):
    """
    Calculate summary stats for the simulation.
    """
    summary = df.describe().T[['mean', 'min', 'max', 'std']]
    return summary
