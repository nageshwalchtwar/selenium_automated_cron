import matplotlib.pyplot as plt
from datetime import datetime

# Function to parse the log data and extract timestamps and log types
def parse_log_data(log_data):
    timestamps = []
    log_types = []
    for line in log_data.strip().split('\n'):
        parts = line.split(' - ')
        if len(parts) >= 3:
            timestamp_str = parts[0]
            log_type_str = parts[2].split(': ')[1]
            
            try:
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S,%f')
                log_types.append(log_type_str)
                timestamps.append(timestamp)
            except ValueError:
                # Ignore lines with incorrect timestamp format
                pass

    return timestamps, log_types

# Read log data from the log file
log_file = "lab_direction.log"
with open(log_file, "r") as file:
    log_data = file.read()

# Parse the log data
timestamps, log_types = parse_log_data(log_data)

# Create the plot
plt.figure(figsize=(12, 6))
for i, log_type in enumerate(set(log_types)):
    x = [timestamps[j] for j in range(len(timestamps)) if log_types[j] == log_type]
    y = [i] * len(x)
    plt.scatter(x, y, label=log_type, marker='o')

plt.yticks(range(len(set(log_types))), set(log_types))
plt.xlabel('Timestamp')
plt.title('Log Events over Time')
plt.legend(loc='best')
plt.xticks(rotation=45)
plt.grid(True)

# Save the plot as an image in the 'images' folder (create the folder if it doesn't exist)
output_folder = "direction_graph"
output_file = f"{output_folder}/log_events_graph.png"

import os
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

plt.tight_layout()
plt.savefig(output_file)
plt.close()

print(f"Graph saved as '{output_file}'")
