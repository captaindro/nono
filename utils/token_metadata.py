import logging

logger = logging.getLogger("token_metadata")

async def get_token_metadata(token_address: str) -> dict:
    """
    Récupère les métadonnées d’un token.
    ⚠️ Version simplifiée — à remplacer par un vrai appel RPC ou Helius plus tard.
    """
    try:
        logger.debug(f"[METADATA] Récupération simulée pour {token_address}")
        return {
            "symbol": "MOCK",
            "name": "MockToken",
            "decimals": 9,
            "description": "Token simulé pour test.",
            "socials": []
        }
    except Exception as e:
        logger.error(f"[METADATA] Erreur lors de la récupération des métadonnées de {token_address} : {e}", exc_info=True)
        return {}
