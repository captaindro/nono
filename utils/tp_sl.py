# utils/tp_sl.py

def compute_tp_sl(entry_price: float, settings: dict) -> tuple[float, float]:
    """
    Calcule le prix de Take Profit (TP) et Stop Loss (SL) à partir du prix d'entrée
    et des paramètres de volatilité dans settings.
    """
    vol_cfg = settings.get('volatility', {})
    use_dyn = vol_cfg.get('use_dynamic', False)
    mult   = vol_cfg.get('multiplier', 1.0)

    if use_dyn:
        # TODO : remplacer ce stub par un calcul réel de la volatilité
        # (e.g. via oracles Pyth/Switchboard ou données Helius)
        # ici on simule une volatilité de base de 5%
        base_vol = 0.05
        vol = base_vol * mult
    else:
        # volatilité statique de 10% si non-dynamique
        vol = 0.10

    tp_price = entry_price * (1 + vol)
    sl_price = entry_price * (1 - vol)
    return tp_price, sl_price
