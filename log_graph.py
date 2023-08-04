# import matplotlib.pyplot as plt
# import numpy as np
# from datetime import datetime

# # Function to parse the log data and extract timestamps and latency values
# def parse_log_data(log_data):
#     timestamps = []
#     latencies = []
#     for line in log_data.strip().split('\n'):
#         parts = line.split(' - ')
#         timestamp_str = parts[0]
#         latency_str = parts[2].split(': ')[1].split(' seconds')[0]
        
#         timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
#         latency = float(latency_str)
        
#         timestamps.append(timestamp)
#         latencies.append(latency)
    
#     return timestamps, latencies

# # Read log data from the log file
# log_file = "lab_latency.log"
# with open(log_file, "r") as file:
#     log_data = file.read()

# # Parse the log data
# timestamps, latencies = parse_log_data(log_data)

# # Calculate the z-scores for latency values
# z_scores = np.abs((latencies - np.mean(latencies)) / np.std(latencies))

# # Define a threshold for outliers (e.g., 3 standard deviations)
# outlier_threshold = 3

# # Filter out data points with high z-scores (outliers)
# timestamps_filtered = [ts for i, ts in enumerate(timestamps) if z_scores[i] <= outlier_threshold]
# latencies_filtered = [lat for i, lat in enumerate(latencies) if z_scores[i] <= outlier_threshold]

# # Create the plot
# plt.figure(figsize=(12, 6))
# plt.scatter(timestamps_filtered, latencies_filtered, marker='o', label='Latency', color='blue', alpha=0.7)
# plt.xlabel('Timestamp (Days)')
# plt.ylabel('Latency (Seconds)')
# plt.title('Latency over Time of Vanishing Rod ')
# plt.xticks(rotation=45)
# plt.grid(True)

# # Perform polynomial regression for the line of best fit (using filtered data)
# z_filtered = np.polyfit(range(len(timestamps_filtered)), latencies_filtered, 3)
# p_filtered = np.poly1d(z_filtered)
# plt.plot(timestamps_filtered, p_filtered(range(len(timestamps_filtered))), label='Trend', color='red', linestyle='--')

# # Set y-axis to show integers only
# plt.locator_params(axis='y', integer=True)

# # Save the plot as an image in the 'images' folder (create the folder if it doesn't exist)
# output_folder = "latency_graph"
# output_file = f"{output_folder}/latency_graph.png"

# import os
# if not os.path.exists(output_folder):
#     os.makedirs(output_folder)

# plt.tight_layout()
# plt.legend()
# plt.savefig(output_file)
# plt.close()

# print(f"Graph saved as '{output_file}'")



# nagesh new graph code
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# Function to parse the log data and extract timestamps and latency values
def parse_log_data(log_data):
    timestamps = []
    latencies = []
    for line in log_data.strip().split('\n'):
        parts = line.split(' - ')
        timestamp_str = parts[0]
        latency_str = parts[2].split(': ')[1].split(' seconds')[0]
        
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
        latency = float(latency_str)
        
        timestamps.append(timestamp)
        latencies.append(latency)
    
    return timestamps, latencies

# Read log data from the log file
log_file = "lab_latency.log"
with open(log_file, "r") as file:
    log_data = file.read()

# Parse the log data
timestamps, latencies = parse_log_data(log_data)

# Convert timestamps to matplotlib dates for better formatting
timestamps_mpl = mdates.date2num(timestamps)

# Calculate the z-scores for latency values
z_scores = np.abs((latencies - np.mean(latencies)) / np.std(latencies))

# Define a threshold for outliers (e.g., 3 standard deviations)
outlier_threshold = 8

# Filter out data points with high z-scores (outliers)
timestamps_filtered = [ts for i, ts in enumerate(timestamps_mpl) if z_scores[i] <= outlier_threshold]
latencies_filtered = [lat for i, lat in enumerate(latencies) if z_scores[i] <= outlier_threshold]

# Create the plot
plt.figure(figsize=(12, 6))
plt.plot_date(timestamps_filtered, latencies_filtered, marker='', linestyle='-', color='blue', alpha=0.7)
plt.xlabel('Timestamp')
plt.ylabel('Latency (Seconds)')
plt.title('Latency over Time of Vanishing Rod')
plt.xticks(rotation=45)
plt.grid(True)

# Perform polynomial regression for the line of best fit (using filtered data)
z_filtered = np.polyfit(range(len(timestamps_filtered)), latencies_filtered, 3)
p_filtered = np.poly1d(z_filtered)
plt.plot(timestamps_filtered, p_filtered(range(len(timestamps_filtered))), label='Trend', color='red', linestyle='--')

# Set y-axis to show integers only
plt.locator_params(axis='y', integer=True)

# Set date format for x-axis ticks
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

# Save the plot as an image in the 'images' folder (create the folder if it doesn't exist)
output_folder = "latency_graph"
output_file = f"{output_folder}/latency_graph.png"

import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

plt.tight_layout()
plt.legend()
plt.savefig(output_file)
plt.close()

print(f"Graph saved as '{output_file}'")
