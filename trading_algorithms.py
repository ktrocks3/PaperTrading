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
    n_loss = keyvalue * data[atr_column]
    trailing_stop = [0] * len(data)
    position = [0] * len(data)  # 1 for buy, -1 for sell, 0 for neutral

    for i in range(1, len(data)):
        if data[src_column].iloc[i] > trailing_stop[i - 1] and data[src_column].iloc[i - 1] > trailing_stop[i - 1]:
            trailing_stop[i] = max(trailing_stop[i - 1], data[src_column].iloc[i] - n_loss.iloc[i])
        elif data[src_column].iloc[i] < trailing_stop[i - 1] and data[src_column].iloc[i - 1] < trailing_stop[i - 1]:
            trailing_stop[i] = min(trailing_stop[i - 1], data[src_column].iloc[i] + n_loss.iloc[i])
        else:
            trailing_stop[i] = data[src_column].iloc[i] - n_loss.iloc[i] if data[src_column].iloc[i] > trailing_stop[
                i - 1] else data[src_column].iloc[i] + n_loss.iloc[i]

        if data[src_column].iloc[i - 1] < trailing_stop[i - 1] and data[src_column].iloc[i] > trailing_stop[i]:
            position[i] = 1  # Buy
        elif data[src_column].iloc[i - 1] > trailing_stop[i - 1] and data[src_column].iloc[i] < trailing_stop[i]:
            position[i] = -1  # Sell

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


