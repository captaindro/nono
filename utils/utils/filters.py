import random

def is_honeypot(token_address: str) -> bool:
    return random.random() < 0.1

def has_enough_liquidity(token_address: str, min_liquidity: float = 1.0) -> bool:
    simulated_liquidity = random.uniform(0.1, 5.0)
    return simulated_liquidity >= min_liquidity

def get_token_score(token_address: str) -> int:
    score = 0
    if not is_honeypot(token_address):
        score += 1
    if has_enough_liquidity(token_address):
        score += 1
    return score