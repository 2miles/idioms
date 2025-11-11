# takes raw, messy scraped text (which might have:
# - extra whitespace,
# - newlines,
# - non-breaking spaces,
# - inconsistent punctuation,
# - HTML tags,
# - duplicate phrasing,
# - or boilerplate like “Definition of ___ from The Free Dictionary”)

# and turns it into a clean, standardized string ready to store.


# Typical things to include in normalize.py

# Later on, you might add functions like:
# - clean_whitespace(def_text: str) -> str
# - remove_source_footers(def_text: str) -> str
# - strip_html(def_text: str) -> str
# - standardize_quotes(def_text: str) -> str
# - normalize_case(def_text: str) -> str
# - validate_length(def_text: str) -> bool (e.g., not too short/long)

# Then scrape_sources.py can call normalize.clean(definition) before returning the result list.


def clean_definition(text: str) -> str:
    # e.g., strip whitespace, remove weird headers
    return text.strip()
