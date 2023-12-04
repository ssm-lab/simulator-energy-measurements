import csv


# Function to extract time from each line
# Function to extract time from each line
def extract_time(line):
    return line.split(": ")[1]  # Split by space and get the second part for time

# Read the input CSV file as a list of lines
with open('/home/yimoning/research/exp_data/trade_off_on_sim_step1/timestamps.csv', 'r') as infile:
    data = infile.readlines()

transformed_data = []

# Check if there's any newline character and strip it
data = [line.strip() for line in data if line.strip()]

for i in range(0, len(data), 4):  # Process every 4 lines into 1 row
    start_time = extract_time(data[i])
    sim_start_time = extract_time(data[i + 1])
    sim_end_time = extract_time(data[i + 2])
    end_time = extract_time(data[i + 3])
    transformed_data.append([start_time, sim_start_time, sim_end_time, end_time])

# Write the transformed data into a new CSV file
with open('/home/yimoning/research/exp_data/trade_off_on_sim_step1/transformed_timestamps.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['Start', 'sim_start', 'sim_end', 'End'])  # Write the header
    writer.writerows(transformed_data)  # Write the processed data
