import logging
import time

class Tracker:
    def __init__(self):
        # Positions actives, format {token_address: {txid, amount, buy_price, timestamp}}
        self.positions = {}

    def add_position(self, token_address, txid, amount, buy_price=None):
        self.positions[token_address] = {
            'txid': txid,
            'amount': amount,
            'buy_price': buy_price,
            'timestamp': time.time()
        }
        logging.info(f"📈 Position ajoutée pour {token_address}: {amount} tokens")

    def update_position(self, token_address, **kwargs):
        if token_address in self.positions:
            self.positions[token_address].update(kwargs)
            logging.info(f"🔄 Position mise à jour pour {token_address}")

    def remove_position(self, token_address):
        if token_address in self.positions:
            del self.positions[token_address]
            logging.info(f"❌ Position fermée pour {token_address}")

    def list_positions(self):
        return self.positions

    def check_take_profit_stop_loss(self, token_address, current_price, tp_ratio=1.1, sl_ratio=0.8):
        pos = self.positions.get(token_address)
        if not pos or not pos.get('buy_price'):
            return None

        buy_price = pos['buy_price']
        if current_price >= buy_price * tp_ratio:
            logging.info(f"🎯 Take profit atteint pour {token_address}")
            return "take_profit"
        elif current_price <= buy_price * sl_ratio:
            logging.info(f"⚠️ Stop loss atteint pour {token_address}")
            return "stop_loss"
        return None
