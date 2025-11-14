import json
from pipelines.examples.get_idioms import get_idioms_missing_examples


if __name__ == "__main__":
    rows = get_idioms_missing_examples(limit=20)
    with open("missing_examples.json", "w") as f:
        json.dump(rows, f, indent=2)

print("Wrote results to missing_examples.json")
