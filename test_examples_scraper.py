from pipelines.examples.scrape_sources import scrape_free_dictionary_examples

IDIOMS_TO_TEST = [
    "spill the beans",
    "go out on a limb",
    "hit the hay",
    "give me a break",
]

for idiom in IDIOMS_TO_TEST:
    print(f"\n🔍 Testing: {idiom}")
    res = scrape_free_dictionary_examples(idiom, delay=1)

    print("Status:", res["status"])
    print("Scraped title:", res["scraped_title"])
    print("Examples found:", len(res["examples"]))

    for ex in res["examples"]:
        print("  •", ex)
