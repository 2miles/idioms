import argparse

from pipelines.definitions.stage_results import create_scraped_data_text_file


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Scrape idioms and definitions from online dictionaries."
    )
    parser.add_argument(
        "input_file",
        help="The markdown file containing the list of idioms.",
    )
    parser.add_argument("output_file", help="The output file to write the scraped data.")
    parser.add_argument(
        "--delay", type=int, default=10, help="Delay in seconds between each request."
    )
    args = parser.parse_args()

    # input_file = "incoming.md"
    # Reads list from md file `input_file` and creates a text data file `new_results.txt`
    # scrape_cambridge("dont put all your eggs in one basket", delay)

    # Reads list from md file `input_file` and creates a text data file `output_file`
    idioms_data = create_scraped_data_text_file(args.input_file, args.output_file, args.delay)
