import yfinance as yf


def fetch_candle_data(symbol: str, interval: str = "1h", period: str = "1d"):
    """
    Fetches candle data for a given symbol and interval using Yahoo Finance.

    :param symbol: The stock/crypto symbol to fetch data for (e.g., 'AAPL').
    :param interval: Timeframe for the candles (e.g., '1m', '1h', '1d').
    :param period: Period of data to fetch (e.g., '1d', '5d', '1mo').
    :return: A DataFrame with candle data.
    """
    try:
        data = yf.download(tickers=symbol, interval=interval, period=period, progress=False)
        if data.empty:
            print(f"No data found for {symbol}.")
            return None
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    symbol = "AAPL"  # Replace with your desired symbol
    interval = "1h"  # Replace with your desired interval ('1m', '5m', '15m', '1h', '1d')
    period = "5d"  # Replace with your desired period ('1d', '5d', '1mo', '3mo', etc.)

    data = fetch_candle_data(symbol, interval, period)

    if data is not None:
        print(data.head())  # Display the first few rows of the data
