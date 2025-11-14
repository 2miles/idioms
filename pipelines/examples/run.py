# acts like the entry point for its pipeline (like your current run_scraper.py).
import argparse

from pipelines.examples.get_idioms import get_idioms_missing_examples
from pipelines.examples.scrape_examples import scrape_examples  # TODO: implement
from pipelines.examples.stage_examples import stage_examples  # TODO: implement
from pipelines.examples.apply_examples import apply_examples  # TODO: implement


def run_pipeline(
    limit: int = 50, delay: int = 10, apply: bool = False, retry_rejected: bool = False
):
    """
    Orchestrates the full 'examples' pipeline:
    1. Fetch idioms missing examples
    2. Scrape examples
    3. Stage successful scrapes into staging_scrapes
    4. Optionally apply approved examples
    """
    print("🚀 Starting examples pipeline...\n")

    idioms = get_idioms_missing_examples(limit=limit, retry_rejected=retry_rejected)
    if not idioms:
        print("✅ No idioms missing examples — nothing to scrape.")
        return
    print(f"📥 Retrieved {len(idioms)} idioms to scrape.")

    results = scrape_examples(idioms, delay)

    summary = stage_examples(results)
    print(
        f"📦 Staged {summary['total']} rows "
        f"({summary['success']} success, {summary['rejected']} rejected)"
    )

    if apply:
        apply_examples()

    print("\n🏁 Pipeline complete.\n")


def main():
    parser = argparse.ArgumentParser(description="Run example scraping pipeline")
    parser.add_argument(
        "--limit", type=int, default=50, help="Max number of idioms to fetch from DB"
    )
    parser.add_argument(
        "--delay", type=int, default=10, help="Delay (in seconds) between HTTP requests"
    )
    parser.add_argument("--retry-rejected", action="store_true")
    args = parser.parse_args()

    run_pipeline(limit=args.limit, delay=args.delay, retry_rejected=args.retry_rejected)


if __name__ == "__main__":
    main()
