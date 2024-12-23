import numpy as np


def calculate_atr(data, period):
    """
    Calculates the Average True Range (ATR).

    :param data: DataFrame containing 'High', 'Low', and 'Close' columns.
    :param period: Period for ATR calculation.
    :return: A Series representing the ATR.
    """
    data['TR'] = np.maximum(
        data['High'] - data['Low'],
        np.maximum(
            abs(data['High'] - data['Close'].shift(1)),
            abs(data['Low'] - data['Close'].shift(1))
        )
    )
    data['ATR'] = data['TR'].rolling(window=period).mean()
    return data['ATR']


def calculate_trailing_stop(data, keyvalue, atr_column='ATR', src_column='Close'):
    """
    Calculates the trailing stop levels.

    :param data: DataFrame containing 'Close' and ATR columns.
    :param keyvalue: Multiplier for ATR to determine stop distance.
    :param atr_column: Name of the ATR column in the DataFrame.
    :param src_column: Name of the source price column (default is 'Close').
    :return: Updated DataFrame with trailing stop levels and signals.
    """
    # Ensure columns exist
    if atr_column not in data.columns or src_column not in data.columns:
        raise ValueError(f"Columns '{atr_column}' or '{src_column}' not found in the DataFrame.")

    # Ensure index is unique and sorted
    data = data.reset_index(drop=True)

    # Calculate n_loss
    n_loss = keyvalue * data[atr_column]

    # Initialize trailing stop and positions
    trailing_stop = [0.0] * len(data)
    position = [0] * len(data)

    for i in range(1, len(data)):
        # Extract scalar values
        current_price = float(data[src_column].iloc[i])
        previous_price = float(data[src_column].iloc[i - 1])
        previous_trailing_stop = float(trailing_stop[i - 1])

        if current_price > previous_trailing_stop and previous_price > previous_trailing_stop:
            trailing_stop[i] = max(previous_trailing_stop, current_price - n_loss.iloc[i])
        elif current_price < previous_trailing_stop and previous_price < previous_trailing_stop:
            trailing_stop[i] = min(previous_trailing_stop, current_price + n_loss.iloc[i])
        else:
            trailing_stop[i] = (
                current_price - n_loss.iloc[i]
                if current_price > previous_trailing_stop
                else current_price + n_loss.iloc[i]
            )

        if previous_price < previous_trailing_stop and current_price > trailing_stop[i]:
            position[i] = 1  # Buy signal
        elif previous_price > previous_trailing_stop and current_price < trailing_stop[i]:
            position[i] = -1  # Sell signal

    # Add trailing stop and position to the DataFrame
    data['Trailing_Stop'] = trailing_stop
    data['Position'] = position

    return data


def generate_signals(data):
    """
    Generates buy/sell signals based on position changes.

    :param data: DataFrame with 'Position' column.
    :return: DataFrame with 'Buy' and 'Sell' signals.
    """
    data['Buy_Signal'] = (data['Position'] == 1)
    data['Sell_Signal'] = (data['Position'] == -1)
    return data


