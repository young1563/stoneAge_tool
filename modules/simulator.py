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
        
    # np.random.multinomial을 사용하여 모든 시행을 한 번에 계산 (성능 최적화)
    # n_draws번 뽑기를 n_trials번 반복했을 때의 각 등급별 획득 횟수를 행렬로 반환
    counts_matrix = np.random.multinomial(n_draws, p_values, size=n_trials)
    
    # 결과를 데이터프레임으로 변환
    return pd.DataFrame(counts_matrix, columns=grades)

def get_simulation_summary(df):
    """
    Calculate summary stats for the simulation.
    """
    summary = df.describe().T[['mean', 'min', 'max', 'std']]
    return summary
