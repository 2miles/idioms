import re
import time

from bs4 import BeautifulSoup
import requests


def _extract_examples(def_elem):
    """
    Extract ALL example sentences inside <div id="Definition">.

    Looks for:
      <div class="ds-list"> / <div class="ds-single">
        ...
        <span class="illustration">Example text...</span>

    Returns: list[str] of cleaned example sentences.
    """
    examples = []

    # Same blocks we used for definitions
    blocks = def_elem.find_all("div", class_=["ds-list", "ds-single"], recursive=True)

    for block in blocks:
        # For examples we don't clone/remove; we just *read* the illustration spans.
        for ill in block.find_all("span", class_="illustration"):
            text = ill.get_text(" ", strip=True)
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                examples.append(text)

    return examples


def scrape_free_dictionary_examples(idiom: str, delay: int = 10, max_retries: int = 2):
    """
    Scrape idioms.thefreedictionary.com for example sentences for a given idiom.

    Extracts ALL example sentences under <div id="Definition">, from
    <span class="illustration"> ... </span>.

    Returns:
        dict: {
            "searched_title": str,
            "scraped_title": str,
            "examples": list[str],
            "source_url": str,
            "status": str  # 'success', 'not_found', 'error', 'http_XXX'
        }
    """
    searched_title = idiom.strip()
    query = re.sub(r"\s+", "+", searched_title)
    url = f"https://idioms.thefreedictionary.com/{query}"

    result = {
        "searched_title": searched_title,
        "scraped_title": "",
        "examples": [],
        "source_url": url,
        "status": "error",
    }

    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, timeout=20)
        except requests.exceptions.RequestException as e:
            if attempt == max_retries:
                result["status"] = "error"
                print(f"❌ Error scraping examples for {searched_title}: {e}")
                time.sleep(delay)
                return result

            print(
                f"⚠️ Request error for examples of {searched_title}, "
                f"retrying... ({attempt+1}/{max_retries})"
            )
            time.sleep(delay * (attempt + 1))
            continue

        if response.status_code != 200:
            status_code = response.status_code
            result["status"] = f"http_{status_code}"
            print(f"⚠️ Failed ({status_code}) for examples of {searched_title}")
            time.sleep(delay)
            return result

        soup = BeautifulSoup(response.text, "html.parser")

        def_elem = soup.find(id="Definition")
        if not def_elem:
            result["status"] = "not_found"
            print(f"⚠️ No definition block found (for examples) for {searched_title}")
            time.sleep(delay)
            return result

        header = def_elem.find("h2")
        if header:
            result["scraped_title"] = header.get_text(strip=True)

        examples = _extract_examples(def_elem)

        if not examples:
            result["status"] = "not_found"
            print(f"⚠️ No examples found for {searched_title}")
            time.sleep(delay)
            return result

        result["examples"] = examples
        result["status"] = "success"

        print(f"✅ Scraped {len(examples)} example(s) for: {searched_title}")

        time.sleep(delay)
        return result

    result["status"] = "error"
    time.sleep(delay)
    return result
