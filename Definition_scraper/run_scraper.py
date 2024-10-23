import requests
import time
import markdown2 as m2
from bs4 import BeautifulSoup
import argparse

"""
Scrapes Free Dictionary for the idioms in input list of the form:

```
1. Middle of the road
2. stick up your ass
3. up in the air
```
Waits 10 seconds between calls to not get 403 errors when crawling.
Prints the process to the console as its crawling.
Writes the results to file `new_results.txt` which is of the form:

```
['title_1, 'title_1_convert', 'definition_1']
['title_2, 'title_2_convert', 'definition_2']
['title_3, '', '']
```

"""


def read_markdown_list(file_path):
    """
    Read a markdown list and return an array of all the list items.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            markdown_content = file.read()
            html_content = m2.markdown(markdown_content)
            soup = BeautifulSoup(html_content, "html.parser")
            list_items = soup.find_all(["li"])
            data = [item.get_text(strip=True) for item in list_items]
            return data

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []


# used to print out soup element of website to understand structure
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


def scrape_free_dictionary(idiom, delay):
    """
    Returns `(title, definition)` pair scraped from idioms.freedictionary.com with `idiom` as the search term.
    """
    idiom = idiom.replace(" ", "+")
    url = f"https://idioms.thefreedictionary.com/{idiom}"
    response = requests.get(url)
    result = ("", "")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        def_elem = soup.find(id="Definition")
        # write_to_file(def_elem.prettify(), "def_pretty.txt")
        title = definition = ""
        if def_elem:
            data_src = def_elem.find(True, recursive=False)
            if data_src:
                header_text = soup.find("h2")
                if header_text:
                    title = header_text.text.strip()
                    # write_to_file(soup.find("h2").find_next_sibling(), "after_h2.txt")
                    # Get the text from the <div> element without including text from its sub-elements
                    if header_text.find_next_sibling():
                        if header_text.find_next_sibling().findAll(
                            text=True, recursive=False
                        ):
                            definition = header_text.find_next_sibling().findAll(
                                text=True, recursive=False
                            )[0]
                result = (title, definition)
            else:
                print("No definition found.")
        else:
            print("Parent element not found.")

    else:
        print(
            f"Failed to retrieve data for {idiom.replace(' ','+') }. Status code: {response.status_code}"
        )
    time.sleep(delay)
    return result


def scrape_cambridge(idiom, delay):
    """
    Returns `(title, definition)` pair scraped from dictionary.cmbridne.org with `idiom` as the search term.
    """
    idiom = idiom.replace(" ", "-")
    url = f"https://dictionary.cambridge.org/dictionary/english/{idiom}"
    response = requests.get(url)
    result = ("", "")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        def_elem = soup.find(class_="ddef_h")
        # write_to_file(def_elem.prettify(), "def_pretty.txt")
        title = definition = ""
        if def_elem:
            print(def_elem.prettify())
            # data_src = def_elem.find(True, recursive=False)
            # if data_src:
            #     header_text = soup.find("h2")
            #     if header_text:
            #         title = header_text.text.strip()
            #         # write_to_file(soup.find("h2").find_next_sibling(), "after_h2.txt")
            #         # Get the text from the <div> element without including text from its sub-elements
            #         if header_text.find_next_sibling():
            #             if header_text.find_next_sibling().findAll(
            #                 text=True, recursive=False
            #             ):
            #                 definition = header_text.find_next_sibling().findAll(
            #                     text=True, recursive=False
            #                 )[0]
            #     result = (title, definition)
            # else:
            #     print("No definition found.")
        else:
            print("Parent element not found.")

    else:
        print(
            f"Failed to retrieve data for {idiom.replace(' ','+') }. Status code: {response.status_code}"
        )
    time.sleep(delay)
    return result


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


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Scrape idioms and definitions from online dictionaries."
    )
    parser.add_argument(
        "input_file",
        help="The markdown file containing the list of idioms.",
    )
    parser.add_argument(
        "output_file", help="The output file to write the scraped data."
    )
    parser.add_argument(
        "--delay", type=int, default=10, help="Delay in seconds between each request."
    )
    args = parser.parse_args()

    # input_file = "incoming.md"
    # Reads list from md file `input_file` and creates a text data file `new_results.txt`
    # scrape_cambridge("dont put all your eggs in one basket", delay)

    # Reads list from md file `input_file` and creates a text data file `output_file`
    idioms_data = create_scraped_data_text_file(
        args.input_file, args.output_file, args.delay
    )
