import json

"""
This script transforms and cleans JSON data from an input file and writes the processed data to a new JSON file.

Functions:
1. `transform_data(input_data)`: Transforms a list of dictionaries from the input data into a new format:
   - Assigns a unique `idiom_id` starting from 1.
   - Maps the "a search title" field to `example_title`.
   - Maps the "c examples" field to `examples`.
   - If the fields are not present, their values will be `None`.

2. `read_json_file(file_path)`: Reads and returns data from the specified JSON file.

3. `write_json_file(data, file_path)`: Writes the given data to the specified JSON file with an indentation of 4 spaces.

Usage:
1. Set the paths for the input JSON file (`input_file_path`) and the output JSON file (`output_file_path`).
2. Run the script to transform the data according to the `transform_data()` function and save the result to the output file.

Example:
If `examples.json` contains:
[
    {"a search title": "Title 1", "c examples": ["Example 1", "Example 2"]},
    {"a search title": "Title 2", "c examples": ["Example 3", "Example 4"]}
]
the output file `examples_fixed.json` will contain:
[
    {"idiom_id": 1, "example_title": "Title 1", "examples": ["Example 1", "Example 2"]},
    {"idiom_id": 2, "example_title": "Title 2", "examples": ["Example 3", "Example 4"]}
]

Requirements:
- The input JSON file should contain a list of dictionaries with keys "a search title" and "c examples".
- The output will be a list of dictionaries with keys `idiom_id`, `example_title`, and `examples`.
"""


def transform_data(input_data):
    transformed_data = []
    for idx, item in enumerate(input_data, start=1):
        transformed_item = {
            "idiom_id": idx,
            "example_title": item.get("a search title", None),
            "examples": item.get("c examples", None),
        }
        transformed_data.append(transformed_item)
    return transformed_data


def read_json_file(file_path):
    with open(file_path, "r") as json_file:
        return json.load(json_file)


def write_json_file(data, file_path):
    # with open(file_path, "w") as json_file:
    #     json.dump(data, json_file, indent=4)
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


def main():
    # Paths to the input and output JSON files
    input_file_path = "results/examples_results_1-1080.json"
    output_file_path = "results/examples_all.json"

    # Read data from the input file
    input_data = read_json_file(input_file_path)

    # Transform the data
    transformed_data = transform_data(input_data)

    # Write the transformed data to the output file
    write_json_file(transformed_data, output_file_path)

    print(f"Data has been transformed and written to {output_file_path}")


if __name__ == "__main__":
    main()
