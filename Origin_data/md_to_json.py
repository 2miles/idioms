import re
import json
import os

"""
This script processes a Markdown file containing idiom origin information and updates a JSON
file with the parsed data.

If an entry with the same idiom_id already exists in the JSON file, it updates that entry;
otherwise, it appends a new entry. So you can run the script many times with multiple different
input markdown files to add to one large json file.

The markdown file is what I will use to write out the idiom origin information because it is
for the most part human readable. Then I will convert it to json using this script. The json will
then be used to insert all the data into the database.

The markdown need to be of this exact format including blank lines:


# "idiom_id": 4,

# "origin_title": "People in glass houses shouldn\u2019t throw stones",

# "origin":

The proverb "those who live in glass houses shouldn\u2019t throw stones" is often cited as originating in Chaucer\u2019s _Troilus and Criseyde_ written in 1385. It is an epic poem, written in Middle English, that tells the story of two tragic lovers against the backdrop of the Siege of Troy. It is sometimes cited as Chaucer\u2019s best work and is also considered to be the origin of the phrase "all good things must come to an end." In the poem, the proverb reads:

> ... who that hath a head of verre, From cast of stones ware him in the werre.

In 1651, George Herbert used the same phrase but in a way that\u2019s far more recognizable to the modern reader. It read:

> Whose house is of glass, must not throw stones at another.

The phrase was first used in America in "William & Mary Quarterly," a public journal published in Virginia. The quote, from Benjamin Franklin, read:

> Don\u2019t throw stones at your neighbors, if your own windows are glass.

By this time, the phrase is almost exactly that which is most commonly used today. This evolution from the 1300s to the 21st century is not unusual. Often idioms and proverbs change as the English language does.

# "idiom_id": 60,

# "origin_title": "The pot calling the kettle black",

# "origin":

The first appearance of this idiom is in Thomas Shelton\u2019s translation of *Don Quixote* in 1620. ...


The script performs the following tasks:
1. Reads and parses the Markdown file specified by `file_path`.
2. Extracts idiom ID and origin text from the Markdown content.
3. Loads existing data from a JSON file if it exists, or initializes a new list if the file does not exist.
4. Updates the JSON file by adding new entries or updating existing ones based on the idiom ID.
5. Writes the updated data back to the JSON file specified by `output_file_path`.

The resulting JSON file will contain a list of dictionaries, each representing an idiom with its `idiom_id` and `origin`.

JSON format:


[
    {
        "idiom_id": 4,
        "origin": "The proverb \"those who live in glass houses shouldn\u2019t throw stones\" is often cited as originating in Chaucer\u2019s _Troilus and Criseyde_ written in 1385. It is an epic poem, written in Middle English, that tells the story of two tragic lovers against the backdrop of the Siege of Troy. It is sometimes cited as Chaucer\u2019s best work and is also considered to be the origin of the phrase \"all good things must come to an end.\" In the poem, the proverb reads:\n\n> ... who that hath a head of verre, From cast of stones ware him in the werre.\n\nIn 1651, George Herbert used the same phrase but in a way that\u2019s far more recognizable to the modern reader. It read:\n\n> Whose house is of glass, must not throw stones at another.\n\nThe phrase was first used in America in \"William & Mary Quarterly,\" a public journal published in Virginia. The quote, from Benjamin Franklin, read:\n\n> Don\u2019t throw stones at your neighbors, if your own windows are glass.\n\nBy this time, the phrase is almost exactly that which is most commonly used today. This evolution from the 1300s to the 21st century is not unusual. Often idioms and proverbs change as the English language does."
    },
    {
        "idiom_id": 60,
        "origin": "The first appearance of this idiom is in Thomas Shelton\u2019s translation of _Don Quixote_ in 1620. The line reads:\n\n> You are like what \\[it\\] is said that the frying-pan said to the kettle, \"Avant, black-browes\".\n\nThese words are spoken by the protagonist whose growing frustrated with Sancho Panza, his servant. In the translation, the words are identified as a proverb that\u2019s used to redirect criticism on someone who plainly has the same faults, habits, or desires.\n\nA few years later, in 1639, the idiom appeared in John Clarke\u2019s _Paroemiologia Anglo-Latina_, a collection of proverbs. It wasn\u2019t until 1682 though, that the idiom neared the wording that\u2019s commonly used today. This is often the case with these colloquialisms. They start off hundreds of years ago with period-appropriate language and then evolve as the years pass to something that\u2019s more widespread and often easier to understand.\n\nIn _Some Fruits of Solitude in Reflections and Maxims_ by William Penn, the phrase \u201cis for the Pot to call the Kettle black\u201d comes after a passage about temperance, tyranny, and rebellion."
    }
]


This script allows you to aggregate and maintain idiom data across multiple runs, 
accommodating updates and new entries.

Usage:
1. Ensure the Markdown file (`file_path`) is correctly formatted.
2. Run the script to parse the Markdown file and update the JSON file.
3. The JSON file (`output_file_path`) will be updated with the new or modified idiom entries.

"""


# Function to parse the Markdown data
def parse_markdown_data(markdown_data):
    pattern = re.compile(
        r'# "idiom_id": (\d+),\n\n# "origin_title": ".*?",\n\n# "origin":\n\n(.*?)(?=\n\n# "idiom_id"|$)',
        re.DOTALL,
    )

    matches = pattern.findall(
        markdown_data + '\n\n# "idiom_id"'
    )  # Add end marker for last match

    if not matches:
        pattern = re.compile(
            r'# "idiom_id": (\d+),\n\n# "origin_title": ".*?",\n\n# "origin":\n\n(.*?)$',
            re.DOTALL,
        )
        matches = pattern.findall(markdown_data)

    data = [
        {"idiom_id": int(idiom_id), "origin": origin.strip()}
        for idiom_id, origin in matches
    ]
    return data


def main():
    # File paths
    file_path = "test_origin.md"
    output_file_path = "test_origin.json"

    # Read the content of the markdown file
    with open(file_path, "r", encoding="utf-8") as file:
        markdown_data = file.read()

    # Parse the data
    parsed_data = parse_markdown_data(markdown_data)

    # Read the existing JSON data if the file exists
    if os.path.exists(output_file_path):
        with open(output_file_path, "r", encoding="utf-8") as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = []

    # Convert existing data to a dictionary for easy lookup
    existing_data_dict = {entry["idiom_id"]: entry for entry in existing_data}

    # Update existing data with new data
    for new_entry in parsed_data:
        existing_data_dict[new_entry["idiom_id"]] = new_entry

    # Convert dictionary back to list
    updated_data = list(existing_data_dict.values())

    # Write the updated data back to the JSON file
    with open(output_file_path, "w", encoding="utf-8") as json_file:
        json.dump(updated_data, json_file, indent=4)

    print("Data has been successfully parsed and written to", output_file_path)


if __name__ == "__main__":
    main()
