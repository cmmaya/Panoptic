import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import math
def pointsPLP(initial_timestamp, final_timestamp):

    # Variables
    a = 1.5

    # Load deposits and withdrawals data from CSV files
    deposits_df = pd.read_csv('deposits.csv').fillna(0)  # Replace NaN with 0
    withdrawals_df = pd.read_csv('withdrawals.csv').fillna(0)  # Replace NaN with 0

    # Token name
    pool_name = withdrawals_df['pool'][0]
    token_0 = pool_name.split("-")[0].strip()
    token_1 = pool_name.split("-")[1].strip()

    # Filter withdrawals data for transactions before or equal to final_timestamp
    withdrawals_before_timestamp_token0 = withdrawals_df[
        (withdrawals_df['timestamp'] >= initial_timestamp) & (withdrawals_df['timestamp'] < final_timestamp) & (
                    withdrawals_df['token'] == token_0)]
    withdrawals_before_timestamp_token1 = withdrawals_df[
        (withdrawals_df['timestamp'] >= initial_timestamp) & (withdrawals_df['timestamp'] < final_timestamp) & (
                    withdrawals_df['token'] == token_1)]

    # Filter deposits data for transactions before or equal to final_timestamp
    deposits_before_timestamp_token0 = deposits_df[
        (deposits_df['timestamp'] >= initial_timestamp) & (deposits_df['timestamp'] < final_timestamp) & (
                    deposits_df['token'] == token_0)]
    deposits_before_timestamp_token1 = deposits_df[
        (deposits_df['timestamp'] >= initial_timestamp) & (deposits_df['timestamp'] < final_timestamp) & (
                    deposits_df['token'] == token_1)]

    # Group by 'owner_id' and sum the 'assets' for withdrawals
    withdrawals_sum_token0 = withdrawals_before_timestamp_token0.set_index('owner_id')['shares'].astype(np.float64).groupby('owner_id').sum().fillna(0)
    withdrawals_sum_token1 = withdrawals_before_timestamp_token1.set_index('owner_id')['shares'].astype(np.float64).groupby('owner_id').sum().fillna(0)

    # Group by 'owner_id' and sum the 'assets' for deposits
    deposits_sum_token0 = deposits_before_timestamp_token0.groupby('owner_id')['shares'].sum().fillna(0)  # Replace NaN with 0
    deposits_sum_token1 = deposits_before_timestamp_token1.groupby('owner_id')['shares'].sum().fillna(0)  # Replace NaN with 0

    # Find owner_ids present in both withdrawals_sum and deposits_sum
    common_owner_ids_token0 = withdrawals_sum_token0.index.intersection(deposits_sum_token0.index)
    common_owner_ids_token1 = withdrawals_sum_token1.index.intersection(deposits_sum_token1.index)

    # Subtract the balance (deposits - withdrawals) for common owner_ids
    net_balance_token0 = deposits_sum_token0
    net_balance_token1 = deposits_sum_token1

    for owner_id in common_owner_ids_token0:
        net_balance_token0[owner_id] = deposits_sum_token0[owner_id] - withdrawals_sum_token0[owner_id]

    for owner_id in common_owner_ids_token1:
        net_balance_token1[owner_id] = deposits_sum_token1[owner_id] - withdrawals_sum_token1[owner_id]

    total_net_balance = (net_balance_token0 + net_balance_token1) / 1e18

    # Assign points for 3 options
    points_token0 = net_balance_token0 * a 
    points_token0_op2 = net_balance_token0 * a / math.sqrt(net_balance_token0.values.sum()) 
    points_token0_op3 = net_balance_token0 * math.sqrt(a)  / net_balance_token0.values.sum()

    points_token1 = net_balance_token1 * a 
    points_token1_op2 = net_balance_token1 * a / math.sqrt(net_balance_token1.values.sum()) 
    points_token1_op3 = net_balance_token1 * math.sqrt(a) / net_balance_token1.values.sum() 

    total_points = (points_token0 + points_token1)
    total_points2 = (points_token0_op2 + points_token1_op2) 
    total_points3 = (points_token0_op3 + points_token1_op3) 

    # Merge data for both tokens into a single DataFrame
    result_df = pd.concat([
        pd.DataFrame({
            'owner_id': net_balance_token0.index,
            f'net_balance_{token_0}': net_balance_token0.values,
            f'points_{token_0}': points_token0.values
        }),
        pd.DataFrame({
            'owner_id': net_balance_token1.index,
            f'net_balance_{token_1}': net_balance_token1.values,
            f'points_{token_1}': points_token1.values
        }),
        pd.DataFrame({'total_points': total_points,
                      'total_points_2': total_points2})
    ], ignore_index=True)

    # Aggregate rows with the same 'owner_id' by summing up their values
    result_df = result_df.groupby('owner_id').sum().reset_index()

    # Check if the output file already exists
    output_file = 'output.csv'
    if os.path.exists(output_file):
        # Append the result to the existing output file
        existing_df = pd.read_csv(output_file)
        result_df = pd.concat([existing_df, result_df], ignore_index=True)
        result_df = result_df.groupby('owner_id').sum().reset_index()

    # Save the result to a CSV file
    result_df.to_csv(output_file, index=False)


    # First subplot
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    axs[0].scatter( total_net_balance.values, total_points.values)
    axs[0].set_xlabel('Liquidity')
    axs[0].set_ylabel('Points')
    axs[0].set_title('Option1: Liquidity vs points')
    axs[0].grid(True)
    axs[0].set_xscale('log')  # Set x-axis scale to log
    axs[0].set_yscale('log')  # Set y-axis scale to log

    # Second subplot
    axs[1].scatter( total_net_balance.values, total_points3.values)    
    axs[1].set_xlabel('Liquidity')
    axs[1].set_ylabel('Points')
    axs[1].set_title('Option3: Liquidity vs points')
    axs[1].grid(True)
    axs[1].set_xscale('log')  # Set x-axis scale to log
    axs[1].set_yscale('log')  # Set y-axis scale to log

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plot
    plt.show()


# Input timestamp
initial_timestamp = 1702543181
final_timestamp = 1710887346

pointsPLP(initial_timestamp, final_timestamp)

