from connectors.supabase import get_conn


def cleanup_applied_examples():
    """
    Delete staged example rows that have already been applied.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM staging_scrapes
            WHERE job = 'example'
              AND review_status = 'applied';
            """
        )
        deleted = cur.rowcount
        conn.commit()

    print(f"🧹 Deleted {deleted} applied example staging rows.")


if __name__ == "__main__":
    cleanup_applied_examples()
