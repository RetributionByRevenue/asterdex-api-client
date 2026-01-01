# Asterdex Futures API Python Client

A simple Python client to interact with the Asterdex Futures API, as documented in `aster-finance-futures-api.md`. This script provides a basic framework for making both public and authenticated (signed) API requests.

## Features

-   **Easy-to-use Class**: A `AsterdexClient` class that encapsulates API interaction logic.
-   **Secure Key Management**: Uses a `.env` file to keep your API keys out of the source code.
-   **HMAC-SHA256 Signing**: Automatically handles the creation of signatures for authenticated endpoints.
-   **Public Endpoints**: Examples for accessing public data:
    -   Get Server Time (`GET /fapi/v1/time`)
    -   Get Kline/Candlestick Data (`GET /fapi/v1/klines`)
-   **Signed Endpoints**: Examples for accessing user-specific data and performing trading actions:
    -   Get Account Information (`GET /fapi/v2/account`)
    -   Get Position Information (`GET /fapi/v2/positionRisk`)
    -   Change Initial Leverage (`POST /fapi/v1/leverage`)
    -   Create New Order (`POST /fapi/v1/order`)

## Prerequisites

-   Python 3.x
-   `requests` library
-   `python-dotenv` library

## Installation & Setup

1.  **Get the script:**
    Download or clone the `asterdex_client.py` file.

2.  **Install dependencies:**
    Open your terminal and install the required libraries.
    ```bash
    pip install requests python-dotenv
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

To run the script and see the examples in action, execute it from your terminal:

```bash
python asterdex_client.py
```

By default, the script will run public requests and show examples for signed requests. The signed actions that create or change data are commented out for safety.

To test the signed endpoints, you must first add your API keys to the `.env` file.

### Example Output

When you run the script with valid API keys, you can expect output similar to the following (values are for demonstration purposes):

```
--- Getting Server Time ---
Server time: 1767255000000
------------------------- 

--- Getting Kline/Candlestick Data ---
Attempting to get 500 1-hour candles for BTCUSDT...
Successfully retrieved 500 klines.
Last kline close time: 2026-01-01 12:00:00
Last kline close price: 87500.50
-------------------------

--- Getting Account Information ---
Successfully retrieved account information:
{'canTrade': True, 'totalWalletBalance': '152.50', 'totalUnrealizedProfit': '2.50', 'assets': [{'asset': 'USDT', 'walletBalance': '152.50', 'unrealizedProfit': '2.50'}]}
------------------------- 

--- Changing Leverage (Example) ---
This is a real trading action.
------------------------- 

--- Creating a New Order (Example) ---
This is a live trading action and is commented out by default.
------------------------- 

--- Getting Position Information ---
Attempting to get position information for all symbols...
Found 1 active position(s):
  - Symbol: BTCUSDT, Amount: 0.001, Entry Price: 86000.0, Side: LONG
------------------------- 
```

## API Functions

The `AsterdexClient` class includes the following methods:

-   `get_server_time()`: Fetches the exchange's current server time.
-   `get_klines(...)`: Fetches OHLC candlestick data.
-   `get_account_info()`: Fetches your account balance and information. (Signed)
-   `get_position_information()`: Fetches your current position data. (Signed)
-   `change_leverage(symbol, leverage)`: Sets the leverage for a given symbol. (Signed)
-   `create_order(...)`: Places a new order on the exchange. (Signed)

## ⚠️ Disclaimer

This script is for educational and demonstration purposes. Trading cryptocurrency futures involves significant risk. The author is not responsible for any financial losses incurred by using this script. Always test with small amounts or on a testnet if available. **Handle your API keys securely and never expose them in public repositories.**
