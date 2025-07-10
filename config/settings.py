# config/settings.py

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List, Optional


class Settings(BaseSettings):

    ENABLE_EMAIL_NOTIFICATIONS: bool = Field(default=False)
    EMAIL_SMTP_SERVER: str = Field(default="")
    EMAIL_SMTP_PORT: int = Field(default=587)
    EMAIL_USE_TLS: bool = Field(default=True)
    EMAIL_USERNAME: str = Field(default="")
    EMAIL_PASSWORD: str = Field(default="")
    EMAIL_FROM: str = Field(default="")
    EMAIL_TO: str = Field(default="")


    ###########################
    # 🔧 Environnement
    ###########################
    environment: str = Field("mainnet", description="Réseau actif : mainnet ou devnet")
    rpc_mode: str = Field("helius", description="Mode RPC : helius ou fast")
    simulate_only: bool = Field(False, description="Simulation uniquement, aucun achat réel")
    expert_mode: bool = Field(False, description="Active les logs experts")
    scraper_enabled: bool = Field(False, description="Active le scraping Pump.fun")
    base_path: str = Field(".", description="Chemin de base du projet (racine)")

    ###########################
    # 🔑 Helius
    ###########################
    hel_api_key: str = Field(..., description="Clé API Helius")
    rpc_helius: str = Field(..., description="Endpoint RPC Helius")
    ws_helius: str = Field(..., description="Endpoint WebSocket Helius")
    helius_webhook_url: str = Field(..., description="URL du webhook Helius")

    ###########################
    # 🔁 Retry / Scraper
    ###########################
    retry_delay_seconds: int = Field(15, description="Délai entre les tentatives")
    max_retries: int = Field(12, description="Nombre max de tentatives")
    scraper_interval_seconds: int = Field(3, description="Intervalle de scraping Pump.fun")
    SCRAPER_ENABLED: bool = Field(default=True)


    ###########################
    # 🔄 Jupiter
    ###########################
    jupiter_api_url: str = Field("https://quote-api.jup.ag", description="URL Jupiter API")
    jupiter_only_direct_routes: bool = Field(False, description="Limiter aux routes directes")
    quote_amount: float = Field(1.0, description="Montant en SOL utilisé pour la quote")
    slippage_bps: int = Field(50, description="Slippage toléré en bps (1% = 100)")

    ###########################
    # 💼 Wallet
    ###########################
    wallet_folder: str = Field("wallets", description="Dossier contenant les wallets")
    wallet_public_keys: List[str] = Field(..., description="Clés publiques des wallets")

    ###########################
    # 📊 Trading
    ###########################
    take_profit_multiplier: float = Field(1.3, description="Multiplicateur de prise de profit")
    stop_loss_multiplier: float = Field(0.6, description="Multiplicateur de stop loss")
    liquidity_threshold_sol: float = Field(0.1, description="Seuil de liquidité minimum")
    token_score_threshold: int = Field(50, description="Score minimum requis")
    force_buy_mode: bool = Field(True, description="Autorise l'achat même si non rugger")

    ###########################
    # 🪙 Pump.fun
    ###########################
    pumpfun_program_id: str = Field(..., description="Program ID de Pump.fun")

    ###########################
    # 📦 CSV Logs
    ###########################
    csv_log_file: str = Field("trades.csv", description="Fichier de log CSV")

    ###########################
    # 🔔 Notifications
    ###########################
    enable_webhook: bool = Field(True, description="Active les notifications webhook")
    discord_webhook_url: Optional[str] = Field(None, description="URL Webhook Discord")

    ###########################
    # 💳 Crédit & sécurité
    ###########################
    credit_limit: int = Field(500000, description="Limite de crédit Helius")


settings = Settings()
