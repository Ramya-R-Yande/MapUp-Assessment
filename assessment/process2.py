import os
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get TollGuru API key and URL from environment variables
API_KEY = os.getenv('TOLLGURU_API_KEY')
API_URL = os.getenv('TOLLGURU_API_URL')

def upload_to_tollguru(csv_folder, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through CSV files in the input folder
    for csv_file in os.listdir(csv_folder):
        if csv_file.endswith(".csv"):
            csv_path = os.path.join(csv_folder, csv_file)
            json_path = os.path.join(output_dir, f"{csv_file.replace('.csv', '.json')}")

            # Set up the API request
            url = f'{API_URL}/toll/v2/gps-tracks-csv-upload?mapProvider=osrm&vehicleType=5AxlesTruck'
            headers = {'x-api-key': API_KEY, 'Content-Type': 'text/csv'}

            # Send the request
            with open(csv_path, 'rb') as file:
                response = requests.post(url, data=file, headers=headers)

            # Save the JSON response
            with open(json_path, 'w') as json_file:
                json_file.write(response.text)

            print(f"Uploaded {csv_file} to TollGuru API. Response saved to {json_path}")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Upload GPS tracks to TollGuru API.")
    parser.add_argument("--to_process", required=True, help="Path to the CSV folder.")
    parser.add_argument("--output_dir", required=True, help="The folder where the resulting JSON files will be stored.")
    args = parser.parse_args()

    # Call the function to upload to TollGuru API
    upload_to_tollguru(args.to_process, args.output_dir)
