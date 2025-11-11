import json


def remove_duplicates_from_examples(examples):
    # Use a set to store unique sentences and remove duplicates
    seen_sentences = set()
    unique_examples = []
    removed_sentences = []  # Track removed sentences

    for example in examples:
        if example not in seen_sentences:
            seen_sentences.add(example)
            unique_examples.append(example)
        else:
            removed_sentences.append(example)

    return unique_examples, removed_sentences


def process_json_file(input_file_path, output_file_path):
    # Read the JSON file
    with open(input_file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    total_removed = 0

    # Process each idiom entry to remove duplicates in the "examples" list
    for idiom_entry in data:
        examples = idiom_entry.get("examples")

        if examples is None:
            print(
                f"Skipping idiom with title '{idiom_entry['example_title']}' because 'examples' is null."
            )
            continue

        unique_examples, removed_sentences = remove_duplicates_from_examples(examples)

        idiom_entry["examples"] = unique_examples

        # Output the number of removed duplicates and the removed sentences
        if removed_sentences:
            print(f"Idiom: {idiom_entry['example_title']}")
            print(f"Removed {len(removed_sentences)} duplicates:")
            for sentence in removed_sentences:
                print(f"  - {sentence}")
            total_removed += len(removed_sentences)
            print()  # New line for readability

    # Write the updated data back to a JSON file
    with open(output_file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Total duplicates removed: {total_removed}")


def main():
    input_file_path = "results/examples_all.json"  # Replace with your input file path
    output_file_path = "results/examples_all_no_dups.json"  # Replace with your desired output file path

    process_json_file(input_file_path, output_file_path)
    print(f"Processed file saved to {output_file_path}")


if __name__ == "__main__":
    main()
