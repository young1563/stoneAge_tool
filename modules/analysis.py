import numpy as np

def calculate_perceived_prob(p, n):
    """
    P = 1 - (1 - p)^n
    n = number of draws
    p = probability of single draw
    """
    return 1 - (1 - p)**n

def calculate_expected_draws(p):
    """
    Expected draws = 1/p
    """
    if p <= 0:
        return float('inf')
    return 1 / p

def calculate_expected_cost(p, price_per_draw):
    """
    Expected cost = Expected draws * Price per draw
    """
    return calculate_expected_draws(p) * price_per_draw

def generate_perceived_prob_table(p, n_range):
    """
    Generate a table of perceived probabilities for a range of draws.
    """
    results = []
    for n in n_range:
        prob = calculate_perceived_prob(p, n)
        results.append({
            "Draws (n)": n,
            "Perceived Prob (%)": prob * 100
        })
    return results
