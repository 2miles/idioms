# test_origin.py
import json
from pipelines.origins.scrape_origins import scrape_origins

# Replace this with any idiom you want to test
TEST_IDIOM = {
    "id": 9999,
    "idiom": "Waiting with bated breath",
    "definition": "To remain in a state of eager anticipation (of or for something).",
}


print("🧪 Testing origin generator with one idiom...\n")

# delay=0 so testing is instantaneous
results = scrape_origins([TEST_IDIOM], delay=0)

# Just take the first (and only) result
result = results[0]

# Write the generated origin to a file for inspection
with open("origin_test_output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\n📄 Saved output to origin_test_output.json\n")
print("Content:\n")
print(result["content"])
