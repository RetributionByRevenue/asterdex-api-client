# Asterdex Futures API Python Client

A simple Python client to interact with the Asterdex Futures API, as documented in `aster-finance-futures-api.md`. This script provides a basic framework for making both public and authenticated (signed) API requests.

## Features

-   **Easy-to-use Class**: A `AsterdexClient` class that encapsulates API interaction logic.
-   **HMAC-SHA256 Signing**: Automatically handles the creation of signatures for authenticated endpoints.
-   **Public Endpoints**: Example for accessing public data like server time.
-   **Signed Endpoints**: Examples for accessing user-specific data and performing trading actions:
    -   Get Account Information (`GET /fapi/v2/account`)
    -   Change Initial Leverage (`POST /fapi/v1/leverage`)
    -   Create New Order (`POST /fapi/v1/order`)

## Prerequisites

-   Python 3.x
-   `requests` library

## Installation & Setup

1.  **Get the script:**
    Download or clone the `asterdex_client.py` file.

2.  **Install dependencies:**
    Open your terminal and install the `requests` library.
    ```bash
    pip install requests
    ```

3.  **Configure API Keys:**
    Open the `asterdex_client.py` file and replace the placeholder values for `API_KEY` and `SECRET_KEY` with your actual keys from Asterdex.

    ```python
    # in asterdex_client.py
    if __name__ == '__main__':
        # --- IMPORTANT ---
        # Replace with your actual API Key and Secret Key
        API_KEY = "YOUR_API_KEY"
        SECRET_KEY = "YOUR_SECRET_KEY"
    ```

## Usage

To run the script and see the examples in action, execute it from your terminal:

```bash
python asterdex_client.py
```

By default, the script will only run the public request to get the server time. The signed requests (getting account info, changing leverage, creating an order) are commented out for safety.

To test the signed endpoints, you must first add your API keys and then uncomment the relevant sections in the `if __name__ == '__main__':` block at the bottom of the file.

### Example Output

```
--- Getting Server Time ---
Server time: 1672531200000
------------------------- 

--- Getting Account Information ---
Please replace 'YOUR_API_KEY' and 'YOUR_SECRET_KEY' with your actual keys.
------------------------- 

--- Changing Leverage (Example) ---
This is a real trading action.
Please provide valid API keys to change leverage.
------------------------- 

--- Creating a New Order (Example) ---
This is a live trading action and is commented out by default.
Please provide valid API keys to create an order.
------------------------- 
```

## API Functions

The `AsterdexClient` class includes the following methods:

-   `get_server_time()`: Fetches the exchange's current server time.
-   `get_account_info()`: Fetches your account balance and position information. (Signed)
-   `change_leverage(symbol, leverage)`: Sets the leverage for a given symbol. (Signed)
-   `create_order(...)`: Places a new order on the exchange. (Signed)

## ⚠️ Disclaimer

This script is for educational and demonstration purposes. Trading cryptocurrency futures involves significant risk. The author is not responsible for any financial losses incurred by using this script. Always test with small amounts or on a testnet if available. **Handle your API keys securely and never expose them in public repositories.**
