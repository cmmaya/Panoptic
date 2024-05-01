import pandas as pd
import math

# Define constants
token0_price = 8
token1_price = 10
a = 0.1
b = 0.1
c = 0.1
base_exponent = 1.2
time_conversion = 86400
time_chunk = 2
profit_threshold = 5
ITM_reward = 100
endurance_time = 15
endurance_points = 0

def rewardMechanism():
    """
    Calculates points for each trade from 'trades.csv'.

    Returns:
    - A list of points for each Token 
    """
    # Read the CSV file
    df = pd.read_csv("trades.csv")

    # Ensure that the required columns exist in the DataFrame
    required_columns = ['sender_id', 'pnl', 'payoff', 'is_closed', 'timestamp_open', 'timestamp_close']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the CSV file.")

    # Initialize all columns
    df['stremia_buyers_1'] = 0 
    df['stremia_buyers_2'] = 0
    df['hold_multiplier'] = 1
    df['ITM_buyers'] = 0
    df['points_based_1'] = 0
    df['points_based_2'] = 0
    df['endurance'] = 0
    df['stremia_multiplied_1'] = 0 
    df['stremia_multiplied_2'] = 0 
    df['total legs'] = 0 

    # Find time column
    df['time'] = (pd.to_datetime(df['timestamp_close']) - pd.to_datetime(df['timestamp_open'])).dt.total_seconds()

    # Multipler for longer positions
    for index, row in df.iterrows():
        if row['is_closed']:
            exponent = (row['time'] // time_chunk)
            df.at[index, 'hold_multiplier'] =  base_exponent ** exponent

    # Calculate 'stremia' for each row
    df['stremia'] = df['pnl'] - df['payoff']

    # Stremia reward for Sellers
    for index, row in df.iterrows():
        if row['stremia'] > 0:
            # Stremia multiplied
            # Option 1: Lj
            df.at[index, 'stremia_multiplied_1'] = a * row['stremia'] * token1_price * row['hold_multiplier']
            # Option 2: sqrt(Lj)/Sum(Lj)
            df.at[index, 'stremia_multiplied_2'] = a * math.sqrt(row['stremia']) * token1_price  *  row['hold_multiplier']

    # Stremia reward for buyers
    for index, row in df.iterrows():
        if row['is_closed']:
            if row['stremia'] < 0:
                # Option 1: Lj
                df.at[index, 'stremia_buyers_1'] = b * -1 * row['stremia'] * token1_price
                # Option 2: sqrt(Lj)/Sum(Lj)
                df.at[index, 'stremia_buyers_2'] = b * math.sqrt(-1 * row['stremia']) * token1_price
                # In the money reward for buyers
                profit = row['pnl'] * token1_price
                if profit > profit_threshold:
                    df.at[index, 'ITM_buyers'] = ITM_reward

    # Function to extract token price if it's a short or long leg dir
    def tokenLegValue(leg):
        return token0_price if leg == 'short' else (token1_price if leg == 'long' else 0)

    # Function to handle NaN values
    def handle_nan(value):
        return 0 if math.isnan(value) else value

    # Points based
    for index, row in df.iterrows():
        total_legs = sum(handle_nan(row.get(f'leg_amount{i}', 0)) * tokenLegValue(row.get(f'dir_leg{i}', '')) for i in range(1, 5))
        df.at[index, 'total_legs'] =  total_legs
        # Option 1: Lj 
        df.at[index, 'points_based_1'] =  total_legs * row['time'] * c
        # Option 2: sqrt(Lj)/Sum(Lj)
        df.at[index, 'points_based_2'] =  math.sqrt(total_legs) * row['time'] * c

    #Endurance points
    for index, row in df.iterrows():
        t =  (row['timestamp_close'] - row['timestamp_open']) / time_conversion
        if t > endurance_time:
            df.at[index, 'endurance'] =  endurance_points

    # Calculate total points for both options
    df['total_points_1'] = df['stremia_buyers_1'] + df['points_based_1'] + df['ITM_buyers'] + df['endurance'] + df['stremia_multiplied_1']
    df['total_points_2'] = df['stremia_buyers_2'] + df['points_based_2'] + df['ITM_buyers'] + df['endurance'] + df['stremia_multiplied_2']

    # Output 2 columns: 'sender_id' and 'points' to a new CSV file
    df[['sender_id', 'stremia', 'stremia_multiplied_1', 'stremia_multiplied_2', 'stremia_buyers_1', 'stremia_buyers_2', 'points_based_1', 'points_based_2', 'ITM_buyers', 'endurance', 'total_points_1', 'total_points_2', 'time', 'total_legs']].to_csv("output-RM.csv", index=False)

rewardMechanism()