import requests
import time
import hmac
import hashlib
from urllib.parse import urlencode
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# This script requires the 'requests' and 'python-dotenv' libraries.
# You can install them by running: pip install requests python-dotenv

class AsterdexClient:
    """
    A client for interacting with the Asterdex Futures API.
    """
    BASE_URL = "https://fapi.asterdex.com"

    def __init__(self, api_key=None, secret_key=None):
        """
        Initializes the AsterdexClient.

        Args:
            api_key (str): Your Asterdex API key.
            secret_key (str): Your Asterdex secret key.
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({'X-MBX-APIKEY': self.api_key})

    def _generate_signature(self, params):
        """
        Generates an HMAC SHA256 signature for the request.

        Args:
            params (dict): The parameters to sign.

        Returns:
            str: The generated signature.
        """
        query_string = urlencode(params)
        return hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

    def _make_request(self, method, path, params=None, signed=False):
        """
        Makes an API request.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            path (str): The API endpoint path.
            params (dict, optional): The request parameters. Defaults to None.
            signed (bool, optional): Whether the request should be signed. Defaults to False.

        Returns:
            dict: The JSON response from the API, or None if an error occurred.
        """
        if params is None:
            params = {}

        if signed:
            if not self.api_key or not self.secret_key:
                raise ValueError("API key and secret key are required for signed requests.")
            
            params['timestamp'] = int(time.time() * 1000)
            params['signature'] = self._generate_signature(params)

        url = self.BASE_URL + path
        
        try:
            response = self.session.request(method, url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {path}: {e}")
            if e.response:
                print(f"Response status code: {e.response.status_code}")
                print(f"Response content: {e.response.content.decode()}")
            return None

    # ----------------------------------------------------------------
    # Public Endpoints
    # ----------------------------------------------------------------

    def get_server_time(self):
        """
        Gets the current server time from the exchange.
        This is a public endpoint and does not require authentication.
        """
        return self._make_request('GET', '/fapi/v1/time')

    def get_klines(self, symbol, interval, limit=500):
        """
        Gets Kline/candlestick data for a symbol.
        This is a public endpoint.

        Args:
            symbol (str): The trading symbol (e.g., 'BTCUSDT').
            interval (str): The kline interval (e.g., '1m', '5m', '1h').
            limit (int, optional): The number of klines to retrieve. Defaults to 500.

        Returns:
            list: A list of kline/candlestick data.
        """
        params = {
            'symbol': symbol,
            'interval': interval,
            'limit': limit,
        }
        return self._make_request('GET', '/fapi/v1/klines', params=params, signed=False)

    # ----------------------------------------------------------------
    # Signed Endpoints (require API key and secret)
    # ----------------------------------------------------------------

    def get_account_info(self):
        """
        Gets account information.
        This is a signed USER_DATA endpoint.
        """
        return self._make_request('GET', '/fapi/v2/account', signed=True)

    def change_leverage(self, symbol, leverage):
        """
        Changes the initial leverage for a symbol.

        Args:
            symbol (str): The trading symbol (e.g., 'BTCUSDT').
            leverage (int): The target initial leverage (e.g., 1 to 125).

        Returns:
            dict: The leverage change response.
        """
        params = {
            'symbol': symbol,
            'leverage': leverage,
        }
        return self._make_request('POST', '/fapi/v1/leverage', params=params, signed=True)

    def create_order(self, symbol, side, order_type, quantity, price=None, time_in_force='GTC'):
        """
        Creates a new order.
        This is a signed TRADE endpoint (POST request).

        Args:
            symbol (str): The trading symbol (e.g., 'BTCUSDT').
            side (str): 'BUY' or 'SELL'.
            order_type (str): 'LIMIT', 'MARKET', 'STOP', etc.
            quantity (float): The quantity of the asset to trade.
            price (float, optional): The price for LIMIT orders. Defaults to None.
            time_in_force (str, optional): 'GTC', 'IOC', 'FOK'. Defaults to 'GTC'.

        Returns:
            dict: The order creation response.
        """
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price is required for LIMIT orders.")
            params['price'] = price
            params['timeInForce'] = time_in_force
        
        return self._make_request('POST', '/fapi/v1/order', params=params, signed=True)

    def get_position_information(self, symbol=None):
        """
        Gets current position information.
        This is a signed USER_DATA endpoint.

        Args:
            symbol (str, optional): The trading symbol (e.g., 'BTCUSDT'). 
                                    If None, information for all positions is returned.

        Returns:
            list: A list of position information.
        """
        params = {}
        if symbol:
            params['symbol'] = symbol
        
        return self._make_request('GET', '/fapi/v2/positionRisk', params=params, signed=True)


if __name__ == '__main__':
    # --- IMPORTANT ---
    # Load API keys from .env file
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Create a client instance
    # For public endpoints, you don't need to provide keys
    public_client = AsterdexClient()

    # For signed endpoints, you must provide your keys
    signed_client = AsterdexClient(api_key=API_KEY, secret_key=SECRET_KEY)

    # --- Example 1: Get Server Time (Public GET request) ---
    print("--- Getting Server Time ---")
    server_time = public_client.get_server_time()
    if server_time:
        print(f"Server time: {server_time['serverTime']}")
    print("-" * 25, "\n")

    # --- Example 2: Get Kline/Candlestick Data (Public GET request) ---
    print("--- Getting Kline/Candlestick Data ---")
    try:
        print("Attempting to get 500 1-hour candles for BTCUSDT...")
        klines = public_client.get_klines(symbol='BTCUSDT', interval='1h', limit=500)
        if klines:
            print(f"Successfully retrieved {len(klines)} klines.")
            # Print the close price of the last kline
            last_kline = klines[-1]
            print(f"Last kline close time: {datetime.fromtimestamp(last_kline[6]/1000)}")
            print(f"Last kline close price: {last_kline[4]}")
    except Exception as e:
        print(f"An error occurred while getting klines: {e}")
    print("-" * 25, "\n")

    # --- Example 3: Get Account Info (Signed GET request) ---
    # This will fail if you don't provide valid keys in your .env file.
    print("--- Getting Account Information ---")
    if not API_KEY or not SECRET_KEY or API_KEY == "YOUR_API_KEY":
        print("Please set your 'API_KEY' and 'SECRET_KEY' in the .env file.")
    else:
        account_info = signed_client.get_account_info()
        if account_info:
            print("Successfully retrieved account information:")
            print(account_info)
    print("-" * 25, "\n")


    # --- Example 4: Change Leverage (Signed POST request) ---
    print("--- Changing Leverage (Example) ---")
    # This is a real trading action.
    # To use it, uncomment the lines below.
    # if not API_KEY or not SECRET_KEY or API_KEY == "YOUR_API_KEY":
    #     print("Please set your API keys in the .env file to change leverage.")
    # else:
    #     try:
    #         print("Attempting to change leverage for BTCUSDT to 20x...")
    #         leverage_response = signed_client.change_leverage(
    #             symbol='BTCUSDT',
    #             leverage=20
    #         )
    #         if leverage_response:
    #             print("Leverage change response:")
    #             print(leverage_response)
    #     except Exception as e:
    #         print(f"An error occurred while changing leverage: {e}")
    print("-" * 25, "\n")


    # --- Example 5: Create a New Order (Signed POST request) ---
    print("--- Creating a New Order (Example) ---")
    print("This is a live trading action and is commented out by default.")
    
    # UNCOMMENT THE FOLLOWING LINES TO CREATE A REAL ORDER
    # if not API_KEY or not SECRET_KEY or API_KEY == "YOUR_API_KEY":
    #     print("Please set your API keys in the .env file to create an order.")
    # else:
    #     try:
    #         print("Attempting to create a new LIMIT BUY order...")
    #         # Example: Create a LIMIT BUY order for 0.01 BTC at a price of 20000 USDT
    #         order_response = signed_client.create_order(
    #             symbol='BTCUSDT',
    #             side='BUY',
    #             order_type='LIMIT',
    #             quantity=0.01,
    #             price=20000
    #         )
    #         if order_response:
    #             print("Order creation response:")
    #             print(order_response)
    #     except Exception as e:
    #         print(f"An error occurred while creating the order: {e}")
    print("-" * 25, "\n")

    # --- Example 6: Get Position Information (Signed GET request) ---
    print("--- Getting Position Information ---")
    if not API_KEY or not SECRET_KEY or API_KEY == "YOUR_API_KEY":
        print("Please set your API keys in the .env file to get position information.")
    else:
        try:
            print("Attempting to get position information for all symbols...")
            positions = signed_client.get_position_information()
            if positions is not None:
                # Filter for positions with a non-zero amount
                active_positions = [p for p in positions if float(p.get('positionAmt', 0)) != 0]
                if active_positions:
                    print(f"Found {len(active_positions)} active position(s):")
                    for pos in active_positions[:5]:
                        print(f"  - Symbol: {pos['symbol']}, "
                              f"Amount: {pos['positionAmt']}, "
                              f"Entry Price: {pos['entryPrice']}, "
                              f"Side: {'LONG' if float(pos['positionAmt']) > 0 else 'SHORT'}")
                else:
                    print("No active positions found.")
        except Exception as e:
            print(f"An error occurred while getting position information: {e}")
    print("-" * 25, "\n")
