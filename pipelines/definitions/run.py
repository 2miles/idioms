import argparse

from connectors.supabase import get_idioms_missing_definitions
from pipelines.definitions.scrape_definitions import scrape_definitions
from pipelines.definitions.stage_results import stage_definitions
from pipelines.definitions.apply_definitions import apply_definitions


def run_pipeline(
    limit: int = 50, delay: int = 10, apply: bool = False, retry_rejected: bool = False
):
    """
    Orchestrates the full 'definitions' pipeline:
    1. Fetch idioms missing definitions
    2. Scrape definitions
    3. Stage successful scrapes into staging_scrapes
    4. Optionally apply approved definitions
    """
    print("🚀 Starting definition pipeline...\n")

    idioms = get_idioms_missing_definitions(limit=limit, retry_rejected=retry_rejected)
    if not idioms:
        print("✅ No idioms missing definitions — nothing to scrape.")
        return
    print(f"📥 Retrieved {len(idioms)} idioms to scrape.")

    results = scrape_definitions(idioms, delay)

    summary = stage_definitions(results)
    print(
        f"📦 Staged {summary['total']} rows "
        f"({summary['success']} success, {summary['rejected']} rejected)"
    )

    if apply:
        apply_definitions()

    print("\n🏁 Pipeline complete.\n")


def main():
    parser = argparse.ArgumentParser(description="Run definition scraping pipeline")
    parser.add_argument(
        "--limit", type=int, default=50, help="Max number of idioms to fetch from DB"
    )
    parser.add_argument(
        "--delay", type=int, default=10, help="Delay (in seconds) between HTTP requests"
    )
    parser.add_argument(
        "--apply", action="store_true", help="Also apply approved definitions after staging"
    )
    parser.add_argument("--retry-rejected", action="store_true")
    args = parser.parse_args()

    run_pipeline(
        limit=args.limit, delay=args.delay, apply=args.apply, retry_rejected=args.retry_rejected
    )


if __name__ == "__main__":
    main()
