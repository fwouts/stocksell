"""Python script that fetches the value of each stock and converts it to the target currency."""

import json
import urllib.request

STOCK_IDS = [
    "GOOG",
    "GOOGL",
]
CURRENCY = "AUD"

def fetch_usd_to_currency_rate():
    """Fetch the rate of conversion from USD to the target currency."""
    # http://www.apilayer.net/api/live?access_key=51848f53f82dad555be278f1a6fc3c0b&format=1
    conversion_url = "http://www.apilayer.net/api/live?access_key=51848f53f82dad555be278f1a6fc3c0b"
    with urllib.request.urlopen(conversion_url) as conversion_connection:
        conversion_data = json.loads(conversion_connection.read().decode())
        usd_to_currency_rate = conversion_data['quotes']['USD{}'.format(CURRENCY)]
        return usd_to_currency_rate

def fetch_value(usd_to_currency_rate, stock_id):
    """Fetch the value of each stock and convert it to the target currency."""
    stock_url = "https://finance.google.com/finance/info?q=NASDAQ:{}".format(stock_id)
    with urllib.request.urlopen(stock_url) as stock_connection:
        # Note that we need to remove the prefix "// ".
        stock_data = json.loads(stock_connection.read().decode()[3:])
        stock_value_usd = float(stock_data[0]["l"])
        # Round the converted value to two decimals.
        stock_value_target_currency = round(stock_value_usd * usd_to_currency_rate, 2)
        return stock_value_target_currency

def print_stock_values():
    """Print the value of each stock in the target currency."""
    usd_to_currency_rate = fetch_usd_to_currency_rate()
    for stock_id in STOCK_IDS:
        print("{}: {}{}".format(stock_id, CURRENCY, fetch_value(usd_to_currency_rate, stock_id)))

if __name__ == '__main__':
    print_stock_values()
