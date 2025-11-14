from connectors.supabase import get_conn


def apply_examples():
    """
    Apply approved staged example sentences to idioms_examples table,
    and mark staging rows as applied.
    """
    with get_conn() as conn, conn.cursor() as cur:
        # Fetch approved example rows
        cur.execute(
            """
            SELECT id, idiom_id, content
            FROM staging_scrapes
            WHERE job = 'example'
              AND review_status = 'approved';
            """
        )
        rows = cur.fetchall()

        if not rows:
            print("⚠️ No approved examples to apply.")
            return

        applied_count = 0

        for staging_id, idiom_id, example_text in rows:
            # Safety: skip empty example text
            if not example_text or not example_text.strip():
                print(f"⚠️ Skipping empty example for idiom_id={idiom_id}")
                continue

            # Insert into idioms_examples (NOT update)
            cur.execute(
                """
                INSERT INTO idioms_examples (idiom_id, example)
                VALUES (%s, %s);
                """,
                (idiom_id, example_text.strip()),
            )

            # Mark this staging row as applied
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

    print(f"✅ Applied {applied_count} approved examples.")


if __name__ == "__main__":
    apply_examples()
