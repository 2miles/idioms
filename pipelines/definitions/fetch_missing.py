# Purpose: decide which idioms need to be scraped.

# Eventually, this will:
# - connect to Supabase
# - run a query like SELECT id, idiom FROM idioms WHERE definition IS NULL
# - (optional) check your local state/scrape_attempts.json or DB table to skip over-attempted ones

# For now, it can just return your markdown list while you test the flow.

# You’ll later reuse this same structure for:
# - examples/fetch_missing.py (idioms with < N examples)
# - origins/fetch_missing.py (idioms missing origin_ai)


from bs4 import BeautifulSoup
import markdown2 as m2


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
            print("📥 Parsed items:", data)
            return data

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
