from pipelines.examples.scrape_sources import scrape_free_dictionary_examples


def scrape_examples(idioms: list[dict], delay: int):
    """
    Collect example-sentence scrape results without writing to the DB.

    idioms: [{'id': int, 'idiom': str}, ...]

    Returns a flat list of staging-ready rows:
    [
        {'idiom_id': int, 'job': 'example', 'content': 'one sentence', 'status': 'success'},
        {'idiom_id': int, 'job': 'example', 'content': 'another sentence', 'status': 'success'},
        {'idiom_id': int, 'job': 'example', 'content': '', 'status': 'not_found'},
        ...
    ]
    """
    results = []

    for row in idioms:
        idiom_id = row["id"]
        idiom_text = row["idiom"]

        print(f"🔍 Scraping examples for: {idiom_text}")
        res = scrape_free_dictionary_examples(idiom_text, delay)

        example_list = res.get("examples") or []
        status = res.get("status") or "error"

        if status == "success" and example_list:
            for example in example_list:
                results.append(
                    {
                        "idiom_id": idiom_id,
                        "job": "example",
                        "content": example.strip(),
                        "status": "success",
                    }
                )
            print(f"✅ Got {len(example_list)} examples for: {idiom_text}")

        else:
            # Add a single placeholder row for not_found/error
            results.append(
                {
                    "idiom_id": idiom_id,
                    "job": "example",
                    "content": "",
                    "status": status,
                }
            )
            print(f"⚠️ No examples found for: {idiom_text} ({status})")

    print(f"\n📊 scrape_examples: {len(results)} total rows collected")
    return results
