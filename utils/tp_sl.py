# utils/tp_sl.py

def calculate_tp_sl(entry_price: float,
                    tp_multiplier: float = 1.1,
                    sl_multiplier: float = 0.8) -> tuple[float, float]:
    """
    Calcule les prix de Take Profit (TP) et Stop Loss (SL) à partir du prix d'entrée.
    
    - entry_price : prix d'achat
    - tp_multiplier : coefficient pour TP (ex. 1.1 pour +10%)
    - sl_multiplier : coefficient pour SL (ex. 0.8 pour -20%)
    
    Retourne un tuple (tp, sl).
    """
    tp = entry_price * tp_multiplier
    sl = entry_price * sl_multiplier
    return tp, sl
