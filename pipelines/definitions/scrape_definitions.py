from pipelines.definitions.scrape_sources import scrape_free_dictionary


def scrape_definitions(idioms: list[dict], delay: int):
    """
    Collect definition scrape results without writing to the DB.

    idioms: [{'id': int, 'idiom': str}, ...]
    returns: [
        {'idiom_id': int, 'job': 'definition', 'content': str, 'status': 'success'|'not_found'|'error'|'http_XXX'},
        ...
    ]
    """
    results = []

    for row in idioms:
        idiom_id = row["id"]
        idiom_text = row["idiom"]

        print(f"🔍 Scraping: {idiom_text} (id={idiom_id})")
        res = scrape_free_dictionary(idiom_text, delay)

        definition = (res.get("definition") or "").strip()
        status = res.get("status") or "error"

        # Build the staging payload shape
        results.append(
            {
                "idiom_id": idiom_id,
                "job": "definition",
                "content": definition,  # empty string if not_found/error
                "status": status,
            }
        )

        if status == "success" and definition:
            print(f"✅ Got definition for: {idiom_text}")
        elif status == "not_found":
            print(f"⚠️ No definition found for: {idiom_text}")
        else:
            print(f"⚠️ Skipped {idiom_text} ({status})")

    print(f"\n📊 scrape_definitions: {len(results)} results collected")
    return results
