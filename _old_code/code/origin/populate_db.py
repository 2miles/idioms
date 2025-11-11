import psycopg2
import json
from dotenv import load_dotenv
import os

"""
This script reads a JSON file containing idiom data and inserts or updates it into a PostgreSQL database table.

The JSON file should be in the following format:
[
    {
        "idiom_id": 4,
        "origin": "The proverb \"those who live in glass houses shouldn’t throw stones\" ..."
    },
    {
        "idiom_id": 60,
        "origin": "The first appearance of this idiom is in Thomas Shelton’s translation of *Don Quixote* in 1620. ..."
    }
]

The script performs the following steps:
1. Loads environment variables from a `.env` file located in the parent directory for database connection parameters.
2. Reads the JSON data from the specified file (`data.json`).
3. Connects to the PostgreSQL database using the credentials provided in the environment variables.
4. Inserts new records into the specified table or updates existing records if the `idiom_id` already exists.
5. Commits the transaction to save changes to the database.

The database table should have a unique constraint or primary key on the `idiom_id` column to ensure correct handling of conflicts.

Usage:
1. Ensure that the `.env` file is correctly configured with the database connection parameters.
2. Place the JSON file in the same directory or adjust the `json_file_path` variable as needed.
3. Run the script to update the database with the data from the JSON file.
"""


# Load environment variables from .env file in the parent directory
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

# Database connection parameters
conn_params = {
    "dbname": os.getenv("PG_DATABASE"),
    "user": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
}


# Function to insert data into the database
def insert_data_into_db(data, table_name):
    # Connect to the database
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    try:
        for entry in data:
            cur.execute(
                f"INSERT INTO {table_name} (idiom_id, origin) VALUES (%s, %s)",
                (entry["idiom_id"], entry["origin"]),
            )
        # Commit the transaction
        conn.commit()
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()


# Main function
def main():
    # Path to the JSON file
    json_file_path = "test_origin.json"
    table_name = "idiom_origin_test"

    # Read the JSON data from file
    with open(json_file_path, "r", encoding="utf-8") as file:
        json_data = json.load(file)

    # Insert the data into the database
    insert_data_into_db(json_data, table_name)


if __name__ == "__main__":
    main()
