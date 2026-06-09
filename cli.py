import os
import time
import hmac
import hashlib
import logging
import argparse
import requests
from urllib.parse import urlencode

# ==========================================
# 1. LOGGING CONFIGURATION
# ==========================================
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler("logs/trading_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("TradingBot")

# ==========================================
# 2. API CLIENT LAYER
# ==========================================
class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str):
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret

    def _sign(self, params: dict) -> str:
        query_string = urlencode(params)
        return hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def place_order(self, symbol, side, order_type, quantity, price=None):
        endpoint = "/fapi/v1/order"
        payload = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        if order_type.upper() == "LIMIT":
            payload["timeInForce"] = "GTC"
            payload["price"] = price

        payload['signature'] = self._sign(payload)
        headers = {'X-MBX-APIKEY': self.api_key}
        
        url = f"{self.base_url}{endpoint}"
        response = requests.post(url, headers=headers, params=payload)
        response.raise_for_status()
        return response.json()

# ==========================================
# 3. COMMAND LINE INTERFACE (CLI) LAYER
# ==========================================
def main():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Bot")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True, choices=['BUY', 'SELL'])
    parser.add_argument("--type", required=True, choices=['MARKET', 'LIMIT'])
    parser.add_argument("--quantity", required=True, type=float)
    parser.add_argument("--price", type=float)
    args = parser.parse_args()

    # Get keys from the environment variables you just set
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        logger.error("Missing API Keys.")
        return

    logger.info(f"Order Request -> Symbol: {args.symbol} | Side: {args.side} | Type: {args.type} | Qty: {args.quantity} | Price: {args.price}")

    client = BinanceFuturesClient(api_key, api_secret)

    try:
        res = client.place_order(args.symbol, args.side, args.type, args.quantity, args.price)
        logger.info(f"SUCCESS! Order ID: {res.get('orderId')} | Status: {res.get('status')} | Executed Qty: {res.get('executedQty')}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API Error: {e.response.text if e.response else str(e)}")

if __name__ == "__main__":
    main()