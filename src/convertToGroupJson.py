import os, glob, json
import argparse

def convert_json_files(input_folder, output_folder):
    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Dictionary to hold data categorized by the first level path
    categorized_data = {}

    # Glob to find all json files in the input folder
    for file_path in glob.glob(os.path.join(input_folder, 'file-*.json')):
        print(f'Processing {file_path}...')
        with open(file_path, 'r') as file:
            data = json.load(file)  # Load the JSON data from the file
            for obj in data:  # Iterate through each object in the array
                path_parts = obj['_key']['path'].split('/')  # Split the path by '/'
                if path_parts:  # Check if there is at least one part
                    first_level = path_parts[0]  # Get the first level directory name
                    if first_level not in categorized_data:
                        categorized_data[first_level] = []  # Initialize a new list if not exists
                    obj['id'] = obj['_key']['name']
                    obj.pop('_key', None)  # Delete the key '_key' from the object
                    categorized_data[first_level].append(obj)  # Append the object to the list

    # Write the categorized data to separate files
    for category, objects in categorized_data.items():
        output_path = os.path.join(output_folder, f'{category}.json')
        with open(output_path, 'w') as file:
            json.dump(objects, file, indent=4)  # Write the list of objects as JSON
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert gcloud LevelDB files to JSON.")
    parser.add_argument("input_folder", help="Path to the input folder containing LevelDB files.")
    parser.add_argument("output_folder", help="Path to the output folder for JSON files.")
    args = parser.parse_args()

    # Normalize folder paths
    if args.input_folder.endswith('/'):
        args.input_folder = args.input_folder[:-1]
    if args.output_folder.endswith('/'):
        args.output_folder = args.output_folder[:-1]

    # Check if input_folder exists and is a directory
    if not os.path.isdir(args.input_folder):
        raise ValueError(f"Input folder {args.input_folder} does not exist or is not a directory.")

    # Check if output_folder exists; if not, attempt to create it
    if not os.path.exists(args.output_folder):
        try:
            os.makedirs(args.output_folder)
        except OSError as e:
            raise OSError(f"Failed to create output folder {args.output_folder}: {e}")

    convert_json_files(args.input_folder, args.output_folder)