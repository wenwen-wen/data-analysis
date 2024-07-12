import argparse
import os
import glob
import json
from leveldb_export import parse_leveldb_documents

def convert_to_json(input_folder, output_folder):
    files = glob.glob(f'{input_folder}/output-*')

    if len(files) == 0: return
    os.makedirs(output_folder, exist_ok=True)

    filecount = 0
    docscount = 0
    for file in files:
        print(f'Parsing {file}', end=' ')
        docs = list(parse_leveldb_documents(file))
        print(f'({len(docs)} docs)', end=' ')
        num = file.split('-')[-1]
        output_file = f"{output_folder}/file-{int(num):04d}.json"
        with open(output_file, 'w') as f:
            json.dump(docs, f)
        filecount += 1
        docscount += len(docs)
        print(f'Finished! (Saved to {output_file})')

    print(f'Parsed {filecount} files with {docscount} documents')
    print('Done')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert gcloud LevelDB files to JSON.")
    parser.add_argument("input_folder", help="Path to the input folder containing LevelDB files.")
    parser.add_argument("output_folder", help="Path to the output folder for JSON files.")
    args = parser.parse_args()

    if args.input_folder.endswith('/'):
        args.input_folder = args.input_folder[:-1]
    if args.output_folder.endswith('/'):
        args.output_folder = args.output_folder[:-1]
    convert_to_json(args.input_folder, args.output_folder)