import logging
import time

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[logging.StreamHandler()]
    )

def main():
    setup_logging()
    logging.info("🚀 Démarrage du bot NONO")

    # Exemple d'initialisation RPC/WebSocket
    try:
        # Remplace par ta vraie initialisation
        logging.info("🔗 Connexion RPC et WebSocket établie")
    except Exception as e:
        logging.error(f"❌ Erreur de connexion : {e}")

    # Heartbeat toutes les 30 secondes pour indiquer que le bot tourne
    while True:
        logging.info("💓 Bot en vie...")
        time.sleep(30)

if __name__ == "__main__":
    main()
