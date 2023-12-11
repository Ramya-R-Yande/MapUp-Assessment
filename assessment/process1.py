import pandas as pd
import argparse
from datetime import datetime, timedelta
import os

def extract_trips(input_file, output_dir):
    # Read the Parquet file
    df = pd.read_parquet(input_file)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Initialize variables for trip identification
    current_unit = None
    trip_number = 0
    current_trip_data = []

    # Function to save the current trip data to a CSV file
    def save_trip_data(unit, trip_number, trip_data):
        trip_df = pd.DataFrame(trip_data, columns=['latitude', 'longitude', 'timestamp'])
        trip_file_path = os.path.join(output_dir, f"{unit}_{trip_number}.csv")
        trip_df.to_csv(trip_file_path, index=False)
        print(f"Saved trip {trip_number} for unit {unit} to {trip_file_path}")

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        if current_unit is None or row['unit'] != current_unit:
            # Start a new trip for a new unit
            current_unit = row['unit']
            trip_number = 0
            current_trip_data = []

        if index > 0:
            # Calculate time difference with the previous row
            time_difference = datetime.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%SZ") - datetime.strptime(df.at[index - 1, 'timestamp'], "%Y-%m-%dT%H:%M:%SZ")

            if time_difference > timedelta(hours=7):
                # Start a new trip if time difference exceeds 7 hours
                save_trip_data(current_unit, trip_number, current_trip_data)
                trip_number += 1
                current_trip_data = []

        # Add current row to the trip data
        current_trip_data.append([row['latitude'], row['longitude'], row['timestamp']])

    # Save the last trip for the last unit
    if current_unit is not None:
        save_trip_data(current_unit, trip_number, current_trip_data)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Extract trips from GPS data in a Parquet file.")
    parser.add_argument("--to_process", required=True, help="Path to the Parquet file to be processed.")
    parser.add_argument("--output_dir", required=True, help="The folder to store the resulting CSV files.")
    args = parser.parse_args()

    # Call the function to extract trips
    extract_trips(args.to_process, args.output_dir)
