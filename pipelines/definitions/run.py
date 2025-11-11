import argparse
from pipelines.definitions.fetch_missing import fetch_missing_definitions
from pipelines.definitions.stage_results import create_scraped_data_text_file


def main():
    parser = argparse.ArgumentParser(
        description="Scrape idioms missing definitions from Supabase and stage new results."
    )
    parser.add_argument(
        "--limit", type=int, default=50, help="Maximum number of idioms to fetch and scrape."
    )
    parser.add_argument(
        "--delay", type=int, default=10, help="Delay in seconds between each scrape request."
    )
    args = parser.parse_args()

    # Step 1: fetch missing idioms directly from Supabase
    idioms = fetch_missing_definitions(limit=args.limit)
    print(f"📥 Fetched {len(idioms)} idioms missing definitions from database.")

    # Step 2: run the scraping stage on those idioms
    create_scraped_data_text_file(idioms, args.delay)


if __name__ == "__main__":
    main()
