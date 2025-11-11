import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pprint

"""
This script scrapes idiom examples from "https://idioms.thefreedictionary.com/" using Selenium WebDriver, 
and appends the results to a JSON file.

Functions:
1. `scrape_examples(results, search_titles)`: 
   - Initializes the WebDriver and navigates to the website.
   - Searches for each title in the search_titles list.
   - Extracts the found title and example sentences if available.
   - Appends the results to the provided results list.
2. `load_titles(file_path)`: Reads lines from the specified text file and returns a list of titles.
3. `append_to_json_file(results, json_file_path)`: Reads existing data from the JSON file, appends new results, and writes back to the JSON file.
4. `capitalize_first_letter(text)`: Capitalizes the first letter of the given text if it is not empty.

Usage:
1. Set the path to the input text file containing the titles (`titles_file`).
2. Run the script to scrape idiom examples for the titles and append the results to the specified JSON file.

Example:
If the text file contains:
Title 1
Title 2
Title 3
The output JSON file will be appended with:
[
    {"a search title": "Title 1", "b found title": "Found Title 1", "c examples": ["Example 1", "Example 2"]},
    {"a search title": "Title 2", "b found title": "Found Title 2", "c examples": ["Example 3", "Example 4"]},
    {"a search title": "Title 3", "b found title": "Found Title 3", "c examples": ["Example 5", "Example 6"]}
]

Requirements:
- The input text file should contain one title per line.
- Ensure the ChromeDriver is installed and the path is correctly specified.
"""


def scrape_examples(results, search_titles):
    """Scrapes idiom examples for the given search titles and appends the results to the results list."""
    driver_path = "/opt/homebrew/bin/chromedriver"

    for search_title in search_titles:
        # Initialize the WebDriver
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)

        result = {
            "a search title": search_title,
            "b found title": None,
            "c examples": None,
        }

        try:
            driver.get("https://idioms.thefreedictionary.com/")

            time.sleep(5)
            search_bar = driver.find_element(By.ID, "f1Word")

            search_bar.send_keys(search_title)
            time.sleep(5)
            search_bar.send_keys(Keys.RETURN)

            h1_element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".content-holder h1"))
            )

            h1_text = capitalize_first_letter(h1_element.text)
            result["b found title"] = h1_text

            illustration_elements = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "illustration"))
            )
            illustration_texts = [element.text for element in illustration_elements]
            print(illustration_texts)

            result["c examples"] = illustration_texts if illustration_texts else "null"

        except (NoSuchElementException, TimeoutException) as e:
            pass

        finally:
            results.append(result)
            driver.quit()

    pprint.pprint(results)


def load_titles(file_path):
    """Reads lines from the specified text file and returns a list of titles."""
    with open(file_path, "r") as file:
        result = [line.strip() for line in file]
    print(result)
    return result


def append_to_json_file(results, json_file_path):
    """Appends the given results to the specified JSON file."""
    try:
        with open(json_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    existing_data.extend(results)

    with open(json_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    print(f"Results have been appended to {json_file_path}")


def capitalize_first_letter(text):
    """Capitalizes the first letter of the given text if it is not empty."""
    if text:
        lowercased_text = text.lower()
        return lowercased_text[0].upper() + lowercased_text[1:]
    return text


def main():
    results = []
    titles_file = "./titles/titles_1001-1200.txt"
    titles = load_titles(titles_file)
    scrape_examples(results, titles)
    append_to_json_file(results, "./results/examples_results_1001-2000.json")


if __name__ == "__main__":
    main()
