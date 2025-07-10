import logging
from utils.jup_swap import execute_swap
from utils.logger import get_logger

logger = get_logger(__name__)

async def buy_token(token_info, amount, slippage_bps=50):
    """
    Achète un token en utilisant Jupiter Swap.
    
    Args:
        token_info (dict): Info token avec au minimum 'mint', 'symbol', 'name'.
        amount (int): Montant à acheter (en lamports ou unités selon token).
        slippage_bps (int): Slippage en basis points (ex: 50 = 0.5%)
    
    Returns:
        bool: True si achat réussi, False sinon.
    """
    try:
        logger.info(f"[buy_token] Tentative d'achat: {token_info['symbol']} ({token_info['mint']}) montant={amount}")
        # Swap token vers SOL (ou stablecoin de sortie)
        result = await execute_swap(
            input_mint=token_info['mint'],
            output_mint='So11111111111111111111111111111111111111112',
            amount=amount,
            slippage_bps=slippage_bps
        )
        if result:
            logger.info(f"[buy_token] Achat réussi pour {token_info['symbol']}")
            return True
        else:
            logger.warning(f"[buy_token] Achat échoué pour {token_info['symbol']}")
            return False
    except Exception as e:
        logger.error(f"[buy_token] Exception lors de l'achat: {e}")
        return False
