# Asterdex Futures API curl Requester

A simple Python script (`signed_request_curl.py`) that demonstrates how to interact with the Asterdex Futures API using `curl` commands executed from Python. It provides a basic `AsterdexTrader` class to make both public and authenticated (signed) API requests.

This script is intended as a lightweight, dependency-minimal example of how to structure and sign API requests.

## Features

-   **`AsterdexTrader` Class**: A simple class to encapsulate API interaction logic.
-   **Secure Key Management**: Uses a `.env` file to keep your API keys out of the source code.
-   **HMAC-SHA256 Signing**: Automatically handles the creation of signatures for authenticated endpoints.
-   **Public and Signed Endpoints**: Provides methods for both public data and private account actions.
-   **Returns Dictionaries**: All API-calling methods return the JSON response as a Python dictionary.

## Prerequisites

-   Python 3.x
-   `curl` installed on your system. Windows 10 and higher uses curl.exe binary, while unix systems default to curl. 
-   `python-dotenv` library

## Installation & Setup

1.  **Get the script:**
    Download or clone the `signed_request_curl.py` file.

2.  **Install dependencies:**
    Open your terminal and install the required Python library.
    ```bash
    pip install python-dotenv
    ```

3.  **Configure API Keys:**
    Create a file named `.env` in the same directory as the script. Add your API Key and Secret Key to this file.

    **`.env` file structure:**
    ```
    # Your Asterdex API credentials
    API_KEY="YOUR_API_KEY"
    SECRET_KEY="YOUR_SECRET_KEY"
    ```
    The script will automatically load these keys. A `.gitignore` file is included to prevent you from accidentally committing your keys.

## Usage

The `signed_request_curl.py` script contains an `AsterdexTrader` class that you can use to make API calls. The main execution block at the bottom of the file (`if __name__ == "__main__":`) shows how to instantiate the class and call its methods.

To run the script and see the examples in action, execute it from your terminal:

```bash
python signed_request_curl.py
```

By default, the script will run the `getKlines` example. You can uncomment the other examples in the `if __name__ == "__main__":` block to test them.

### `AsterdexTrader` Class Methods

-   `getKlines(symbol, interval, limit=500)`: Fetches OHLC candlestick data. This is a public endpoint.
-   `placeTrade(symbol, side, order_type, quantity)`: Places a new order on the exchange. (Signed)
-   `getPositionRisk()`: Fetches your current position data. (Signed)
-   `setLeverage(symbol, leverage)`: Sets the leverage for a given symbol. (Signed)
-   `getAccountInfo()`: Fetches your account balance and information. (Signed)

### Example: How to Use the Class

```python
import os
from dotenv import load_dotenv

# Assuming AsterdexTrader class is in the same file or imported
# from signed_request_curl import AsterdexTrader

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Create an instance of the AsterdexTrader
    trader = AsterdexTrader(api_key=API_KEY, secret_key=SECRET_KEY)

    # --- How to call each function ---

    # 1. Get Klines (public endpoint)
    print("--- Getting Klines ---")
    klines = AsterdexTrader.getKlines("CAKEUSDT", "1m", 10)
    if klines:
        print(klines)

    # 2. Get Position Risk
    # print("\n--- Getting Position Risk ---")
    # position_risk = trader.getPositionRisk()
    # if position_risk:
    #     print(position_risk)

    # 3. Set Leverage
    # print("\n--- Setting Leverage ---")
    # leverage_result = trader.setLeverage("CAKEUSDT", 10)
    # if leverage_result:
    #     print(leverage_result)
        
    # 4. Place a Trade
    # print("\n--- Placing a Trade ---")
    # trade_result = trader.placeTrade("CAKEUSDT", "BUY", "MARKET", "6")
    # if trade_result:
    #     print(trade_result)

    # 5. Get Account Info
    # print("\n--- Getting Account Info ---")
    # account_info = trader.getAccountInfo()
    # if account_info:
    #     print(account_info)
```

## ⚠️ Disclaimer

This script is for educational and demonstration purposes. Trading cryptocurrency futures involves significant risk. The author is not responsible for any financial losses incurred by using this script. Always test with small amounts or on a testnet if available. **Handle your API keys securely and never expose them in public repositories.**
