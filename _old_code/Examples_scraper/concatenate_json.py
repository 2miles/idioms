import json

"""
This script concatenates the contents of two JSON files into a single JSON file.

Functions:
1. `read_json_file(file_path)`: Reads and returns the data from the specified JSON file.
2. `write_json_file(data, file_path)`: Writes the given data to the specified JSON file with an indentation of 4 spaces.
3. `concatenate_json_files(file1_path, file2_path, output_file_path)`: 
   - Reads data from two JSON files.
   - Concatenates the lists from both files.
   - Writes the combined data to a new JSON file.

Usage:
1. Set the paths for the input JSON files (`file1_path` and `file2_path`) and the output JSON file (`output_file_path`).
2. Run the script to concatenate the JSON data from the two input files and save the result to the output file.

Requirements:
- Both input JSON files must contain lists of data.
- The script assumes that the data in both files is of type `list`.

Example:
If `file1_path` contains:
[
    {"id": 1, "value": "A"},
    {"id": 2, "value": "B"}
]
and `file2_path` contains:
[
    {"id": 3, "value": "C"},
    {"id": 4, "value": "D"}
]
the output file will contain:
[
    {"id": 1, "value": "A"},
    {"id": 2, "value": "B"},
    {"id": 3, "value": "C"},
    {"id": 4, "value": "D"}
]

"""


def read_json_file(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def write_json_file(data, file_path):
    # with open(file_path, "w") as json_file:
    #     json.dump(data, json_file, indent=4)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def concatenate_json_files(file1_path, file2_path, output_file_path):
    data1 = read_json_file(file1_path)
    data2 = read_json_file(file2_path)

    if isinstance(data1, list) and isinstance(data2, list):
        concatenated_data = data1 + data2
    else:
        raise ValueError("Both JSON files must contain a list of data.")

    write_json_file(concatenated_data, output_file_path)


def main():
    file1_path = "results/examples_results_1-1000.json"
    file2_path = "results/examples_results_1001-1080.json"
    output_file_path = "results/examples_results_1-1080.json"

    concatenate_json_files(file1_path, file2_path, output_file_path)
    print(f"Data has been concatenated and written to {output_file_path}")


if __name__ == "__main__":
    main()
