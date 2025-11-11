# Purpose: save and review what you scraped before updating the DB.

# It takes the results list from scrape_sources.py and:
# - writes a CSV/JSON file to review/exports/
# - (e.g. definitions_2025-11-10.json)
# - optionally filters or formats the text
# - logs summary stats (e.g. “30 success, 5 not found, 2 errors”)

# Once you like the results, you can run a future apply_results.py (or add that function here) to push them to Supabase.


# used to print out soup element of website to understand structure
from pipelines.definitions.fetch_missing import read_markdown_list
from pipelines.definitions.scrape_sources import scrape_free_dictionary


def write_to_file(output_string, file_path):
    """
    Write a string to a file.

    Args:
        output_string (str): The string to be written to the file.
        file_path (str): The path to the file where the string will be written.

    Returns:
        None
    """
    try:
        with open(file_path, "w") as file:
            file.write(output_string)
        print(f"String successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def write_list_to_file(my_list, file_path):
    """
    Write a Python list to a file with each element on a new line.

    Args:
        my_list (list): The list to be written to the file.
        file_path (str): The path to the file where the list will be written.

    Returns:
        None
    """
    try:
        with open(file_path, "w") as file:
            for item in my_list:
                file.write(f"{item}\n")
        print(f"List successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def create_scraped_data_text_file(input_md, output_file, delay):
    """
    Scrapes Free Dictionary for the idioms of `idioms` list
    Waits 10 seconds between calls to not get 403 errors when crawling.
    Prints the process to the console as its crawling.
    Writes the results to file in the form:
    ```
    ['title_1, 'title_1_convert', 'definition_1']
    ['title_2, 'title_2_convert', 'definition_2']
    ['title_3, '', '']
    ```
    """
    data = []
    idioms = read_markdown_list(input_md)
    for idiom in idioms:
        free_dict_result = scrape_free_dictionary(idiom, delay)
        data.append([idiom, free_dict_result[0], free_dict_result[1]])
        print(free_dict_result[0])
    write_list_to_file(data, output_file)
    return data
