# call your actual site scrapers — which you’ll move into scrapers/.

# Purpose: actually get the data.

# It imports and uses your scrapers/free_dictionary.py (and optionally Cambridge later).
# It should:
# - take a list of idioms (from fetch_missing)
# - call each source in order of priority
# - return a structured list like
# [{ "id": 1, "idiom": "spill the beans", "definition": "...", "source": "FreeDictionary", "status": "success" }]

# Later, you can make it handle retry logic, fallbacks, or multiple sources per idiom.


import time
from bs4 import BeautifulSoup
import requests


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
                        if header_text.find_next_sibling().findAll(text=True, recursive=False):
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
