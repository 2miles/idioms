import pprint
import json

"""
This script reads titles from a text file, creates a list of dictionaries from the titles, and exports the list to a JSON file.
It isolates the task of converting a list of titles into a specific JSON format, which can be useful for initial data preparation.

Functions:
1. `read_file_to_list(file_path)`: Reads lines from the specified text file, strips newline characters, and returns a list of titles.
2. `create_dict_list(words)`: Creates a list of dictionaries from a list of words. Each dictionary contains three keys: "a search title", "b found title", and "c examples".
3. `export_to_json(data, file_path)`: Exports the given data to a JSON file with an indentation of 4 spaces.

Usage:
1. Set the path to the input text file containing the titles (`file_path`).
2. Run the script to read the titles, create a list of dictionaries, and export the data to a JSON file.

Example:
If the text file contains:

Title 1
Title 2
Title 3

The output JSON file will contain:
[
    {"a search title": "Title 1", "b found title": None, "c examples": None},
    {"a search title": "Title 2", "b found title": None, "c examples": None},
    {"a search title": "Title 3", "b found title": None, "c examples": None}
]

Requirements:
- The input text file should contain one title per line.
"""


def read_file_to_list(file_path):
    """Reads lines from the specified text file and returns a list of titles."""
    with open(file_path, "r") as file:
        title_list = file.readlines()
        return [line.strip() for line in title_list]


def create_dict_list(words):
    """Creates a list of dictionaries from a list of words."""
    dict_list = []
    for word in words:
        dict_list.append(
            {"a search title": word, "b found title": None, "c examples": None}
        )
    return dict_list


def export_to_json(data, file_path):
    """Exports the given data to a JSON file."""
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def main():
    # Path to the input text file
    file_path = "titles_201-1200.txt"

    # Read titles from the file
    title_list = read_file_to_list(file_path)

    # Create a list of dictionaries from the titles
    dict_list = create_dict_list(title_list)

    # Export the list of dictionaries to a JSON file
    export_to_json(dict_list, "examples_rest_201_1200_empty.json")


if __name__ == "__main__":
    main()
