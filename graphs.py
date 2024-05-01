import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

def graphs():
    
    # Read the CSV file
    out = pd.read_csv("output-RM.csv")
    # Graph 1 ############

    _ , axs = plt.subplots(1, 2, figsize=(12, 5))

    # First subplot
    axs[0].scatter(out['stremia'], out['total_points_1'])
    axs[0].set_xlabel('Stremia')
    axs[0].set_ylabel('Points')
    axs[0].set_title('Stremia vs Points')
    axs[0].grid(True)
    axs[0].set_xscale('log')  # Set x-axis scale to log
    axs[0].set_yscale('log')  # Set y-axis scale to log

    # Second subplot
    axs[1].scatter(out['total_legs'], out['stremia'])
    axs[1].set_xlabel('Legs Amount')
    axs[1].set_ylabel('Stremia')
    axs[1].set_title('Leg Amount vs Stremia')
    axs[1].grid(True)
    axs[1].set_xscale('log')  # Set x-axis scale to log
    axs[1].set_yscale('log')  # Set y-axis scale to log

    # Adjust layout to prevent overlap
    plt.tight_layout()

    # Show plot
    plt.show()


    # Graph 2 ##########

    # Create the scatter plot
    plt.scatter(out['time'], out['total_points_1'], c=out['total_legs'], cmap='viridis')

    # Set labels and title
    plt.xlabel('Time')
    plt.ylabel('Total Points')
    plt.title('Time vs Total Points (Color: Total Legs)')
    plt.colorbar(label='Total Legs')

    # Set log scale for x and y axes
    plt.xscale('log')
    plt.yscale('log')

    # Show plot
    plt.show()


    # Graph 3 ##########

    # Create the scatter plot
    plt.scatter(out['time'], out['total_points_1'])

    # Set labels and title
    plt.xlabel('Time')
    plt.ylabel('Total Points')
    plt.title('Total points vs Time')

    # Set log scale for x and y axes
    plt.xscale('log')
    plt.yscale('log')

    # Show plot
    plt.show()

    ## Graph 4 ############

    # Drop rows with NaN values in 'time' or 'total_points_2'
    out_cleaned = out.dropna(subset=['time', 'total_points_2', 'total_legs'])

    # Create a meshgrid of time and total_points_2 values
    time_values = np.linspace(out_cleaned['time'].min(), out_cleaned['time'].max(), 100)
    total_points_values = np.linspace(out_cleaned['total_points_2'].min(), out_cleaned['total_points_2'].max(), 100)
    time_mesh, total_points_mesh = np.meshgrid(time_values, total_points_values)

    # Interpolate total_legs values for the meshgrid
    total_legs_mesh = griddata((out_cleaned['time'], out_cleaned['total_points_2']), out_cleaned['total_legs'], (time_mesh, total_points_mesh), method='linear')

    # Create the contour plot
    plt.figure(figsize=(10, 7))
    contour = plt.contourf(time_mesh, total_points_mesh, total_legs_mesh, cmap='viridis')

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Total Points')
    plt.title('Contour Plot: Liquidity vs Time vs Total Points')

    # Add colorbar
    plt.colorbar(contour, label='Liquidity')

    # Show plot
    plt.show()

graphs()