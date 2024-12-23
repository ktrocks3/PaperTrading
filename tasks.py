import asyncio
from fetch_data import fetch_candle_data
from trading_algorithms import *
from discord_bot import send_discord_message

# Initialize position (e.g., start with 100 shares of the stock)
position = {"symbol": "AAPL", "quantity": 100, "last_action": None}


async def position_manager(action, symbol, current_price, signal_strength=1.0):
    """
    Manages the position by updating holdings and determining buy/sell quantities.

    :param action: "buy" or "sell"
    :param symbol: Stock symbol
    :param current_price: Current price of the stock
    :param signal_strength: Multiplier for the action (e.g., 0.5 for weak sell)
    """
    global position

    if action == "buy":
        # Calculate how much to buy (e.g., fixed budget of $500 per buy)
        budget = 500
        quantity = budget // current_price
        position["quantity"] += quantity
        position["last_action"] = "buy"
        await send_discord_message(
            f"Bought {quantity} shares of {symbol} at ${current_price:.2f}. Total position: {position['quantity']} shares."
        )

    elif action == "sell":
        # Calculate how much to sell based on signal strength
        quantity = int(position["quantity"] * signal_strength)  # Sell a percentage
        if quantity > 0:
            position["quantity"] -= quantity
            position["last_action"] = "sell"
            await send_discord_message(
                f"Sold {quantity} shares of {symbol} at ${current_price:.2f}. Remaining position: {position['quantity']} shares."
            )
        else:
            await send_discord_message(
                f"No shares to sell for {symbol}. Current position: {position['quantity']} shares."
            )


async def process_signals(data, symbol):
    global position

    for i, row in data.iterrows():
        buy_signal = row[('Buy_Signal', '')]
        sell_signal = row[('Sell_Signal', '')]

        current_price = row[('Close', 'AAPL')]  # Adjust column name as needed

        if bool(buy_signal):
            # Only buy if the last action wasn't also a buy
            if position["last_action"] != "buy":
                await position_manager("buy", symbol, current_price)
        elif bool(sell_signal):
            # Sell with a strength of 0.5 (weak signal) or 1.0 (strong signal)
            signal_strength = 0.5 if position["last_action"] == "sell" else 1.0
            await position_manager("sell", symbol, current_price, signal_strength)


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
