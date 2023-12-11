import os
import json
import pandas as pd
import argparse

def process_json_files(input_folder, output_file):
    data_list = []

    for json_file in os.listdir(input_folder):
        if json_file.endswith('.json'):
            json_file_path = os.path.join(input_folder, json_file)

            with open(json_file_path, 'r') as file:
                json_data = json.load(file)

                if json_data.get('tolls'):
                    for toll in json_data['tolls']:
                        data = {
                            'unit': json_data['unit'],
                            'trip_id': json_file,
                            'toll_loc_id_start': toll.get('startTollLocId', ''),
                            'toll_loc_id_end': toll.get('endTollLocId', ''),
                            'toll_loc_name_start': toll.get('startTollLocName', ''),
                            'toll_loc_name_end': toll.get('endTollLocName', ''),
                            'toll_system_type': toll.get('tollSystemType', ''),
                            'entry_time': toll.get('entryTime', ''),
                            'exit_time': toll.get('exitTime', ''),
                            'tag_cost': toll.get('tagCost', ''),
                            'cash_cost': toll.get('cashCost', ''),
                            'license_plate_cost': toll.get('licensePlateCost', ''),
                        }
                        data_list.append(data)
                    print(f"Tolls found in file: {json_file}")
                else:
                    print(f"No tolls found in file: {json_file}")

    if data_list:
        df = pd.DataFrame(data_list)
        df.to_csv(output_file, index=False)
    else:
        print("No tolls found in any JSON files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract toll information from JSON files and transform to CSV.")
    parser.add_argument("--to_process", type=str, help="Path to the JSON responses folder.")
    parser.add_argument("--output_dir", type=str, help="Folder where the final transformed_data.csv will be stored.")
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    output_file = os.path.join(args.output_dir, 'transformed_data.csv')
    
    process_json_files(args.to_process, output_file)
