from connectors.supabase import get_conn


def apply_origins():
    """
    Apply approved AI origins into idiom_origins_ai, and mark staging rows as applied.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, idiom_id, content
            FROM staging_scrapes
            WHERE job = 'origin'
              AND review_status = 'approved';
            """
        )
        rows = cur.fetchall()

        if not rows:
            print("⚠️ No approved origins to apply.")
            return

        applied_count = 0

        for staging_id, idiom_id, origin_text in rows:
            if not origin_text or not origin_text.strip():
                print(f"⚠️ Skipping empty origin for idiom_id={idiom_id}")
                continue

            # Insert or update final origin table
            cur.execute(
                """
                INSERT INTO idiom_origins_ai (idiom_id, origin_text, model)
                VALUES (%s, %s, %s)
                """,
                (idiom_id, origin_text.strip(), "gpt-5.1"),
            )

            # Mark staging row as applied
            cur.execute(
                """
                UPDATE staging_scrapes
                SET review_status = 'applied'
                WHERE id = %s;
                """,
                (staging_id,),
            )

            applied_count += 1

        conn.commit()

    print(f"✅ Applied {applied_count} AI origins.")


if __name__ == "__main__":
    apply_origins()
