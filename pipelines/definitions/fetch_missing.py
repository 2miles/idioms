# Purpose: decide which idioms need to be scraped.

# Eventually, this will:
# - connect to Supabase
# - run a query like SELECT id, idiom FROM idioms WHERE definition IS NULL
# - (optional) check your local state/scrape_attempts.json or DB table to skip over-attempted ones


# You’ll later reuse this same structure for:
# - examples/fetch_missing.py (idioms with < N examples)
# - origins/fetch_missing.py (idioms missing origin_ai)

from connectors.supabase import get_idioms_missing_definitions


def fetch_missing_definitions(limit=100):
    """
    Fetch idioms from Supabase that are missing definitions.
    Returns a list of dicts: [{id, idiom}, ...]
    """
    return get_idioms_missing_definitions(limit)
