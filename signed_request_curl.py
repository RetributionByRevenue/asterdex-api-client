import os
import time
import hmac
import hashlib
from urllib.parse import urlencode
from dotenv import load_dotenv
import subprocess
import json
import platform

load_dotenv()

class AsterdexTrader:
    BASE_URL = "https://fapi.asterdex.com"
    CURL_BINARY = "curl.exe" if platform.system() == "Windows" else "curl"

    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key

    def _get_signature(self, params):
        payload_string = urlencode(sorted(params.items()))
        return hmac.new(
            self.secret_key.encode('utf-8'),
            payload_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _execute_curl(self, curl_command):
        try:
            result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.PIPE)
            return json.loads(result)
        except subprocess.CalledProcessError as e:
            print(f"Error executing curl command: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from response: {e}")
            return None

    def placeTrade(self, symbol, side, order_type, quantity):
        ENDPOINT = "/fapi/v1/order"
        full_url = self.BASE_URL + ENDPOINT

        params_to_sign = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
            'timestamp': int(time.time() * 1000)
        }

        signature = self._get_signature(params_to_sign)
        final_request_body = f"{urlencode(sorted(params_to_sign.items()))}&signature={signature}"
        
        curl_command = f'''{self.CURL_BINARY} -s -H "X-MBX-APIKEY: {self.api_key}" -X POST "{full_url}" -d "{final_request_body}"'''
        return self._execute_curl(curl_command)

    def getPositionRisk(self):
        ENDPOINT = "/fapi/v2/positionRisk"
        full_url = self.BASE_URL + ENDPOINT

        params_to_sign = {
            'timestamp': int(time.time() * 1000)
        }

        signature = self._get_signature(params_to_sign)
        final_request_url = f"{full_url}?{urlencode(sorted(params_to_sign.items()))}&signature={signature}"

        curl_command = f'''{self.CURL_BINARY} -s -H "X-MBX-APIKEY: {self.api_key}" -X GET "{final_request_url}"'''
        return self._execute_curl(curl_command)

    def setLeverage(self, symbol, leverage):
        ENDPOINT = "/fapi/v1/leverage"
        full_url = self.BASE_URL + ENDPOINT

        params_to_sign = {
            'symbol': symbol,
            'leverage': leverage,
            'timestamp': int(time.time() * 1000)
        }

        signature = self._get_signature(params_to_sign)
        final_request_body = f"{urlencode(sorted(params_to_sign.items()))}&signature={signature}"

        curl_command = f'''{self.CURL_BINARY} -s -H "X-MBX-APIKEY: {self.api_key}" -X POST "{full_url}" -d "{final_request_body}"'''
        return self._execute_curl(curl_command)

    def getAccountInfo(self):
        ENDPOINT = "/fapi/v2/account"
        full_url = self.BASE_URL + ENDPOINT

        params_to_sign = {
            'timestamp': int(time.time() * 1000)
        }

        signature = self._get_signature(params_to_sign)
        final_request_url = f"{full_url}?{urlencode(sorted(params_to_sign.items()))}&signature={signature}"

        curl_command = f'''{self.CURL_BINARY} -s -H "X-MBX-APIKEY: {self.api_key}" -X GET "{final_request_url}"'''
        return self._execute_curl(curl_command)

    @staticmethod
    def getKlines(symbol, interval, limit=500):
        ENDPOINT = "/fapi/v1/klines"
        
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit
        }
        
        query_string = urlencode(params)
        full_url = f"{AsterdexTrader.BASE_URL}{ENDPOINT}?{query_string}"
        
        curl_command = f'''{AsterdexTrader.CURL_BINARY} -s -X GET "{full_url}"'''
        try:
            result = subprocess.check_output(curl_command, shell=True, stderr=subprocess.PIPE)
            return json.loads(result)
        except subprocess.CalledProcessError as e:
            print(f"Error executing curl command: {e}")
            print(f"Stderr: {e.stderr.decode()}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from response: {e}")
            return None


if __name__ == "__main__":
    # IMPORTANT: Replace with your actual API credentials
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Create an instance of the AsterdexTrader
    trader = AsterdexTrader(api_key=API_KEY, secret_key=SECRET_KEY)

    # --- How to call each function ---

    # 1. Get Klines (public endpoint)
    print("--- Getting Klines ---")
    klines = AsterdexTrader.getKlines("CAKEUSDT", "1m", 10)
    if klines:
        print(json.dumps(klines, indent=4))

    # 2. Get Position Risk
    print("\n--- Getting Position Risk ---")
    position_risk = trader.getPositionRisk()
    if position_risk:
        print(json.dumps(position_risk, indent=4))

    # 3. Set Leverage
    print("\n--- Setting Leverage ---")
    leverage_result = trader.setLeverage("CAKEUSDT", 10)
    if leverage_result:
        print(json.dumps(leverage_result, indent=4))

    '''
    # 4. Place a Trade
    print("\n--- Placing a Trade ---")
    trade_result = trader.placeTrade("CAKEUSDT", "BUY", "MARKET", "6")
    if trade_result:
        print(json.dumps(trade_result, indent=4))
    '''

    # 5. Get Account Info
    print("\n--- Getting Account Info ---")
    account_info = trader.getAccountInfo()
    if account_info:
        print(json.dumps(account_info, indent=4))
