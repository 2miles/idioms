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


def scrape_examples(results, search_titles):
    """
    Scrapes example sentences for a list of search titles from theidioms.com website and appends the results to the provided list.
    This website is hard to scrape efficiently. They throw capchas at you randomly. And even if you do make it all the way through
    your list you only get results for about 30% of the input. So I stopped using this in favor of `examples_scraper_2.py`

    Args:
        results (list): A list to which the results will be appended. Each result is a dictionary containing the search title, found title, and examples.
        search_titles (list of str): A list of search titles to look for on theidioms.com.

    Functionality:
        - For each search title in the search_titles list, the function initializes a Chrome WebDriver and navigates to theidioms.com.
        - It searches for the given search title using the website's search bar.
        - If a search result is found, it navigates to the result page and extracts the title and example sentences.
        - The found title and examples are stored in a dictionary and appended to the results list.
        - If example sentences are not found, the corresponding dictionary entries remain `None`.
        - WebDriver is closed after processing each search title.

    Notes:
        - Requires ChromeDriver installed via Homebrew and accessible at "/opt/homebrew/bin/chromedriver".
        - Uses Selenium for web scraping. Ensure that the appropriate web driver is installed and compatible with your Chrome version.
        - Includes sleep intervals to allow for dynamic content loading, which can be adjusted as needed.

    Example:
        results = []
        search_titles = ["diamond in the rough", "break the ice"]
        scrape_examples(results, search_titles)
        # Results will contain dictionaries with search titles, found titles, and examples.

    Raises:
        NoSuchElementException: If a specified element is not found on the page.
        TimeoutException: If a page or element load exceeds the specified timeout.
    """

    # Path to the ChromeDriver installed via Homebrew
    driver_path = "/opt/homebrew/bin/chromedriver"

    for search_title in search_titles:
        # Initialize the WebDriver
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)

        # Initialize the result dictionary for the current search_title
        result = {
            "a search title": search_title,
            "b found title": None,  # Default value if not found
            "c examples": None,  # Default value if not found
        }

        try:
            # Navigate to the website
            driver.get("https://www.theidioms.com")

            # Locate the search bar element
            time.sleep(6)
            search_bar = driver.find_element(By.ID, "q")

            # Enter text into the search bar
            search_bar.send_keys(search_title)

            time.sleep(6)
            # Submit the search (press Enter)
            search_bar.send_keys(Keys.RETURN)

            # Wait for the results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.gs-title"))
            )

            # Locate the first 'a' element with the class 'gs-title'
            first_result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.gs-title"))
            )
            time.sleep(6)
            first_result.click()
            time.sleep(3)

            # Wait for the new page to load and locate the h1 element with id 'title'
            h1_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "title"))
            )

            # Get the text inside the h1 element
            h1_text = capitalize_first_letter(h1_element.text)
            result["b found title"] = h1_text

            # Locate the <h2> element with the text "Example Sentences"
            h2_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h2[text()='Example Sentences']")
                )
            )

            # Locate the <ol> element that follows the <h2> element
            ol_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//h2[text()='Example Sentences']/following-sibling::ol")
                )
            )

            # Find all <li> elements within the located <ol> element
            li_elements = ol_element.find_elements(By.TAG_NAME, "li")

            # Extract text from each <li> element and store in a list
            sentences = [li.text for li in li_elements]
            result["c examples"] = sentences if sentences else "null"

        except (NoSuchElementException, TimeoutException) as e:
            # If an error occurs, the default values remain unchanged
            pass

        finally:
            # Append the result dictionary to the results list
            results.append(result)

            # Ensure the WebDriver is closed
            driver.quit()

    # Print results
    pprint.pprint(results)


def load_titles(file_path):
    # Open the file and read lines into a list
    with open(file_path, "r") as file:
        # Read each line, strip newline characters, and store in a list
        result = [line.strip() for line in file]
    # Print the list to verify
    print(result)
    return result


def append_to_json_file(results, json_file_path):

    # Read existing data from the JSON file if it exists
    try:
        with open(json_file_path, "r") as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file does not exist, initialize an empty list
        existing_data = []

    # Append new results to the existing data
    existing_data.extend(results)

    # Write the updated data back to the JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    print(f"Results have been appended to {json_file_path}")


def capitalize_first_letter(text):
    # Check if the text is not empty
    if text:
        # Lowercase the entire string, then capitalize the first letter
        lowercased_text = text.lower()
        return lowercased_text[0].upper() + lowercased_text[1:]
    return text


if __name__ == "__main__":
    results = []
    titles_file = "titles_201-400.txt"
    titles = load_titles(titles_file)
    scrape_examples(results, titles)
    append_to_json_file(results, "examples_results_201-400.json")
