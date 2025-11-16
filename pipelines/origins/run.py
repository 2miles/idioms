import argparse

from pipelines.origins.get_idioms import get_idioms_missing_origins
from pipelines.origins.scrape_origins import scrape_origins
from pipelines.origins.stage_origins import stage_origins


def run_pipeline(
    limit: int = 20,
    delay: int = 5,
    retry_rejected: bool = False,
):
    print("🚀 Starting origins pipeline...\n")

    idioms = get_idioms_missing_origins(limit=limit, retry_rejected=retry_rejected)
    if not idioms:
        print("✅ No idioms missing origins — nothing to generate.")
        return

    print(f"📥 Retrieved {len(idioms)} idioms to generate origins for.")

    results = scrape_origins(idioms, delay)

    summary = stage_origins(results)
    print(
        f"📦 Staged {summary['total']} rows "
        f"({summary['success']} success, {summary['rejected']} rejected)"
    )

    print("\n🏁 Origins pipeline complete.\n")


def main():
    parser = argparse.ArgumentParser(description="Run AI origin generation pipeline")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--delay", type=int, default=5, help="Delay between API calls (seconds)")
    parser.add_argument("--retry-rejected", action="store_true")

    args = parser.parse_args()

    run_pipeline(
        limit=args.limit,
        delay=args.delay,
        retry_rejected=args.retry_rejected,
    )


if __name__ == "__main__":
    main()
