import asyncio
from threading import Thread
from fetch_data import fetch_candle_data
from trading_algorithms import *
from discord_bot import send_discord_message

async def process_signals(data, symbol):
    for i, row in data.iterrows():
        buy_signal = row[('Buy_Signal', '')]
        sell_signal = row[('Sell_Signal', '')]

        from dotenv import load_dotenv

        # Load environment variables from .env
        load_dotenv()

        if bool(buy_signal):  # Explicitly convert to a boolean
            await send_discord_message(f"Buy signal for {symbol} at {row['Close']}")
        elif bool(sell_signal):  # Explicitly convert to a boolean
            await send_discord_message(f"Sell signal for {symbol} at {row['Close']}")
        else:
            await send_discord_message(f"No signal for {symbol}. Current data: {row.to_dict()}")


if __name__ == "__main__":
    # Fetch data
    symbol = "AAPL"
    interval = "1h"
    period = "5d"
    keyvalue = 3
    atr_period = 10

    data = fetch_candle_data(symbol, interval, period)

    if data is not None:
        # Calculate ATR
        data['ATR'] = calculate_atr(data, atr_period)

        # Calculate trailing stop and positions
        data = calculate_trailing_stop(data, keyvalue)

        # Generate signals
        data = generate_signals(data)

        # Process signals asynchronously
        asyncio.run(process_signals(data, symbol))

        # Display data for verification
        print(data.tail())
