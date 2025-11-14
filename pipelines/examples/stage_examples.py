from connectors.supabase import get_conn


def stage_examples(results):
    """
    Insert scraped examples into staging_scrapes.

    - Each example sentence becomes its own staging row.
    - Success rows are 'pending', others are 'rejected'.
    - NO ON CONFLICT, because examples allow multiple rows per idiom.

    Returns a summary dict.
    """
    with get_conn() as conn, conn.cursor() as cur:
        for row in results:
            review_status = "pending" if row["status"] == "success" else "rejected"

            cur.execute(
                """
                INSERT INTO staging_scrapes (idiom_id, job, content, status, review_status)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    row["idiom_id"],
                    "example",
                    row["content"],
                    row["status"],
                    review_status,
                ),
            )

        conn.commit()

    summary = {
        "success": sum(1 for r in results if r["status"] == "success"),
        "rejected": sum(1 for r in results if r["status"] != "success"),
        "total": len(results),
    }
    return summary
