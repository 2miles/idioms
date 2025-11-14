import re
import time
import requests
from bs4 import BeautifulSoup


def _clean_definition_text(text: str) -> str:
    """
    Normalize definition text:
    - collapse whitespace
    - strip leading list numbers like '1.' or '1)'
    """
    if not text:
        return ""

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove leading 1., 1), etc.
    text = re.sub(r"^\d+[\.\)]\s*", "", text)

    return text


# def _extract_definitions(def_elem):
#     """
#     Extract ALL definitions inside <div id="Definition">.

#     Returns a list like:
#     ["1. First meaning ...", "2. Second meaning ..."]
#     """
#     definitions = []

#     # Find all definition list blocks
#     blocks = def_elem.find_all("div", class_="ds-list", recursive=True)

#     for block in blocks:
#         # Clone the block so we can safely modify it
#         block_copy = BeautifulSoup(str(block), "html.parser")

#         # Remove all example sentences
#         for ill in block_copy.find_all("span", class_="illustration"):
#             ill.decompose()

#         # Get all text (including spans), in order
#         text = block_copy.get_text(" ", strip=True)

#         # Clean up repeated whitespace
#         text = re.sub(r"\s+", " ", text).strip()

#         # Must contain something meaningful
#         if len(text) > 2:
#             definitions.append(text)


#     return definitions
def _extract_definitions(def_elem):
    """
    Extract ALL definitions inside <div id="Definition">.

    - Supports both div.ds-list and div.ds-single
    - Strips out example spans: <span class="illustration">
    - Returns a list like ["1. First meaning ...", "2. Second meaning ..."]
    """
    definitions = []

    # ds-list = multiple definitions, ds-single = a single one
    blocks = def_elem.find_all("div", class_=["ds-list", "ds-single"], recursive=True)

    for block in blocks:
        # Make a mini-soup so we can safely mutate
        block_copy = BeautifulSoup(str(block), "html.parser")

        # Remove example sentences
        for ill in block_copy.find_all("span", class_="illustration"):
            ill.decompose()

        # Get all visible text from the definition block
        text = block_copy.get_text(" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()

        if text:
            definitions.append(text)

    return definitions


# def scrape_free_dictionary(idiom: str, delay: int = 10, max_retries: int = 2):
#     """
#     Scrape idioms.thefreedictionary.com for a given idiom.

#     Returns:
#         dict: {
#             "searched_title": str,
#             "scraped_title": str,
#             "definition": str,
#             "source_url": str,
#             "status": str  # 'success', 'not_found', 'error', or 'http_XXX'
#         }
#     """
#     searched_title = idiom.strip()
#     query = re.sub(r"\s+", "+", searched_title)
#     url = f"https://idioms.thefreedictionary.com/{query}"

#     result = {
#         "searched_title": searched_title,
#         "scraped_title": "",
#         "definition": "",
#         "source_url": url,
#         "status": "error",
#     }

#     # Simple retry loop for timeouts / transient issues
#     for attempt in range(max_retries + 1):
#         try:
#             response = requests.get(url, timeout=20)
#         except requests.exceptions.RequestException as e:
#             # Last attempt -> give up
#             if attempt == max_retries:
#                 result["status"] = "error"
#                 print(f"❌ Error scraping {searched_title}: {e}")
#                 time.sleep(delay)
#                 return result

#             # Backoff and retry
#             print(f"⚠️ Request error for {searched_title}, retrying... ({attempt+1}/{max_retries})")
#             time.sleep(delay * (attempt + 1))
#             continue

#         # Non-200 response
#         if response.status_code != 200:
#             status_code = response.status_code
#             result["status"] = f"http_{status_code}"
#             print(f"⚠️ Failed ({status_code}) for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Parse HTML
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Main definition container
#         def_elem = soup.find(id="Definition")
#         if not def_elem:
#             result["status"] = "not_found"
#             print(f"⚠️ No definition block found for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Idiom title
#         header = def_elem.find("h2")
#         if header:
#             result["scraped_title"] = header.get_text(strip=True)

#         # New structure: div.ds-list holds the mixed-content definition
#         ds_list = def_elem.find("div", class_="ds-list")
#         if not ds_list:
#             # Fallback: first div under Definition
#             ds_list = def_elem.find("div")

#         if not ds_list:
#             result["status"] = "not_found"
#             print(f"⚠️ No ds-list container found for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Grab all text inside ds-list, including spans, as a single string
#         raw_text = ds_list.get_text(" ", strip=True)
#         definition = _clean_definition_text(raw_text)

#         if not definition:
#             result["status"] = "not_found"
#             print(f"⚠️ Definition text empty for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Success 🎉
#         result["definition"] = definition
#         result["status"] = "success"
#         display_title = result["scraped_title"] or searched_title
#         print(f"✅ Scraped: {searched_title} → {display_title}")

#         time.sleep(delay)
#         return result

#     # We should never fall out of the loop without returning, but just in case:
#     time.sleep(delay)
#     return result


# def scrape_free_dictionary(idiom: str, delay: int = 10, max_retries: int = 2):
#     """
#     Scrape idioms.thefreedictionary.com for a given idiom.

#     Extracts ALL definition blocks under <div id="Definition">,
#     removes example sentences (<span class="illustration">),
#     preserves numbering (1., 2., etc.).

#     Returns:
#         dict: {
#             "searched_title": str,
#             "scraped_title": str,
#             "definition": str,           # combined text, "\n" joined
#             "definitions_list": list[str],
#             "source_url": str,
#             "status": str                # 'success', 'not_found', 'error', 'http_XXX'
#         }
#     """
#     searched_title = idiom.strip()
#     query = re.sub(r"\s+", "+", searched_title)
#     url = f"https://idioms.thefreedictionary.com/{query}"

#     result = {
#         "searched_title": searched_title,
#         "scraped_title": "",
#         "definition": "",
#         "definitions_list": [],
#         "source_url": url,
#         "status": "error",
#     }

#     # Retry loop for flaky site behavior
#     for attempt in range(max_retries + 1):
#         try:
#             response = requests.get(url, timeout=20)
#         except requests.exceptions.RequestException as e:
#             if attempt == max_retries:
#                 result["status"] = "error"
#                 print(f"❌ Error scraping {searched_title}: {e}")
#                 time.sleep(delay)
#                 return result

#             print(f"⚠️ Request error for {searched_title}, retrying... ({attempt+1}/{max_retries})")
#             time.sleep(delay * (attempt + 1))
#             continue

#         # Non-200 responses (e.g. 404)
#         if response.status_code != 200:
#             status_code = response.status_code
#             result["status"] = f"http_{status_code}"
#             print(f"⚠️ Failed ({status_code}) for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Parse HTML
#         soup = BeautifulSoup(response.text, "html.parser")

#         # Entire definition section
#         def_elem = soup.find(id="Definition")
#         if not def_elem:
#             result["status"] = "not_found"
#             print(f"⚠️ No definition block found for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Extract <h2> displayed title
#         header = def_elem.find("h2")
#         if header:
#             result["scraped_title"] = header.get_text(strip=True)

#         definitions = _extract_definitions(def_elem)

#         if not definitions:
#             result["status"] = "not_found"
#             print(f"⚠️ No definitions found for {searched_title}")
#             time.sleep(delay)
#             return result

#         # Populate result
#         result["definitions_list"] = definitions
#         result["definition"] = "\n".join(definitions)
#         result["status"] = "success"

#         print(f"✅ Scraped {len(definitions)} definition(s) for: {searched_title}")

#         time.sleep(delay)
#         return result

#     # Should not reach here
#     result["status"] = "error"
#     time.sleep(delay)
#     return result
import re
import time
import requests
from bs4 import BeautifulSoup


def scrape_free_dictionary(idiom: str, delay: int = 10, max_retries: int = 2):
    """
    Scrape idioms.thefreedictionary.com for a given idiom.

    Extracts ALL definition blocks under <div id="Definition">,
    removes example sentences (<span class="illustration">),
    preserves numbering (1., 2., etc.).

    Returns:
        dict: {
            "searched_title": str,
            "scraped_title": str,
            "definition": str,           # combined text, "\n" joined
            "definitions_list": list[str],
            "source_url": str,
            "status": str                # 'success', 'not_found', 'error', 'http_XXX'
        }
    """
    searched_title = idiom.strip()
    query = re.sub(r"\s+", "+", searched_title)
    url = f"https://idioms.thefreedictionary.com/{query}"

    result = {
        "searched_title": searched_title,
        "scraped_title": "",
        "definition": "",
        "definitions_list": [],
        "source_url": url,
        "status": "error",
    }

    # Retry loop for flaky site behavior
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, timeout=20)
        except requests.exceptions.RequestException as e:
            if attempt == max_retries:
                result["status"] = "error"
                print(f"❌ Error scraping {searched_title}: {e}")
                time.sleep(delay)
                return result

            print(f"⚠️ Request error for {searched_title}, retrying... ({attempt+1}/{max_retries})")
            time.sleep(delay * (attempt + 1))
            continue

        # Non-200 responses (e.g. 404)
        if response.status_code != 200:
            status_code = response.status_code
            result["status"] = f"http_{status_code}"
            print(f"⚠️ Failed ({status_code}) for {searched_title}")
            time.sleep(delay)
            return result

        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # Entire definition section
        def_elem = soup.find(id="Definition")
        if not def_elem:
            result["status"] = "not_found"
            print(f"⚠️ No definition block found for {searched_title}")
            time.sleep(delay)
            return result

        # Extract <h2> displayed title
        header = def_elem.find("h2")
        if header:
            result["scraped_title"] = header.get_text(strip=True)

        # Use helper to grab ALL definitions (ds-list + ds-single, no illustrations)
        definitions = _extract_definitions(def_elem)

        if not definitions:
            result["status"] = "not_found"
            print(f"⚠️ No definitions found for {searched_title}")
            time.sleep(delay)
            return result

        # Populate result
        result["definitions_list"] = definitions
        result["definition"] = "\n".join(definitions)
        result["status"] = "success"

        print(f"✅ Scraped {len(definitions)} definition(s) for: {searched_title}")

        time.sleep(delay)
        return result

    # Should not reach here
    result["status"] = "error"
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
