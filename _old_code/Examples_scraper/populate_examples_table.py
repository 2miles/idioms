import json
import psycopg2
from dotenv import load_dotenv
import os

"""
This script reads example data from a JSON file and inserts it into a PostgreSQL database table.

Functions:
1. `load_json_data(file_path)`: Reads and returns the data from the specified JSON file.
2. `create_connection()`: Creates and returns a connection to the PostgreSQL database.
3. `insert_example_data(conn, example_data)`: Inserts example data into the `idiom_examples_test` table.

Usage:
1. Ensure the JSON file containing the example data is available at the specified path.
2. Ensure the PostgreSQL database connection parameters are set in a `.env` file.
3. Run the script to insert the example data into the database.

Requirements:
- The `.env` file should contain the following variables:
  - `PG_DATABASE`: Name of the PostgreSQL database.
  - `PG_USER`: Username for the PostgreSQL database.
  - `PG_PASSWORD`: Password for the PostgreSQL database.
  - `PG_HOST`: Host address for the PostgreSQL database.
  - `PG_PORT`: Port number for the PostgreSQL database.

Example:
If the JSON file contains:
[
    {
        "idiom_id": 1,
        "examples": [
            "Example sentence 1 for idiom 1",
            "Example sentence 2 for idiom 1"
        ]
    },
    {
        "idiom_id": 2,
        "examples": [
            "Example sentence 1 for idiom 2",
            "Example sentence 2 for idiom 2"
        ]
    }
]
the script will insert each example sentence into the `idiom_examples_test` table with the corresponding `idiom_id`.
"""


def load_json_data(file_path):
    """Reads and returns the data from the specified JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)


def create_connection():
    """Creates and returns a connection to the PostgreSQL database."""
    conn_params = {
        "dbname": os.getenv("PG_DATABASE"),
        "user": os.getenv("PG_USER"),
        "password": os.getenv("PG_PASSWORD"),
        "host": os.getenv("PG_HOST"),
        "port": os.getenv("PG_PORT"),
    }
    return psycopg2.connect(**conn_params)


def insert_example_data(conn, example_data):
    """Inserts example data into the `idiom_examples_test` table."""
    cur = conn.cursor()
    for item in example_data:
        if item["examples"] is not None:
            idiom_id = item["idiom_id"]
            for example in item["examples"]:
                # Debugging print statements
                print(f"Inserting idiom_id: {idiom_id}, example: {example}")
                cur.execute(
                    "INSERT INTO idiom_examples_test (idiom_id, example) VALUES (%s, %s)",
                    (idiom_id, example),
                )
    # Commit the transaction and close the cursor
    conn.commit()
    cur.close()


def main():
    # Load environment variables from .env file in the parent directory
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    json_file_path = "./results/examples.json"
    example_data = load_json_data(json_file_path)
    conn = create_connection()
    insert_example_data(conn, example_data)
    conn.close()


if __name__ == "__main__":
    main()
