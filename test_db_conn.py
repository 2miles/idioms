import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
import os

"""
This script connects to a PostgreSQL database, tests the connection, and prints the results.

Usage:
1. Adjust the database connection parameters (`dbname`, `user`, `password`, `host`, and `port`) as needed.
2. Run the script to establish a connection to the PostgreSQL database and verify it by executing a simple query.

"""


def create_connection():
    try:
        # Connect to the PostgreSQL database
        conn_params = {
            "dbname": os.getenv("PG_DATABASE"),
            "user": os.getenv("PG_USER"),
            "password": os.getenv("PG_PASSWORD"),
            "host": os.getenv("PG_HOST"),
            "port": os.getenv("PG_PORT"),
        }
        # If the connection was successful, print the connection object
        conn = psycopg2.connect(**conn_params)
        print("Connection successful:", conn)
        return conn
    except OperationalError as e:
        # If an error occurs, print the error message
        print(f"Error: {e}")
        return None


def test_connection(conn):
    try:
        # Create a cursor object
        cur = conn.cursor()
        # Execute a simple query
        cur.execute("SELECT 1")
        # Fetch the result
        result = cur.fetchone()
        # Print the result
        print("Query result:", result)
        # Close the cursor
        cur.close()
    except Exception as e:
        # If an error occurs, print the error message
        print(f"Error executing query: {e}")


def main():
    # Load environment variables from .env file in the parent directory
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

    # Create a connection
    conn = create_connection()

    # Test the connection if it was successful
    if conn:
        test_connection(conn)
        # Close the connection
        conn.close()


if __name__ == "__main__":

    main()
