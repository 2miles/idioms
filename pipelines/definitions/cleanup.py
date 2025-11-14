from connectors.supabase import get_conn


def cleanup_applied_definitions():
    """
    Delete staged definition rows that have already been applied.
    """
    with get_conn() as conn, conn.cursor() as cur:
        # Optional: only delete for job='definition'
        cur.execute(
            """
            DELETE FROM staging_scrapes
            WHERE job = 'definition'
              AND review_status = 'applied';
            """
        )
        deleted = cur.rowcount
        conn.commit()

    print(f"🧹 Deleted {deleted} applied staging rows.")


if __name__ == "__main__":
    cleanup_applied_definitions()
