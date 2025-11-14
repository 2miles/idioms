from connectors.supabase import get_conn


def apply_definitions():
    """
    Apply approved staged definitions to idioms table, and mark them as applied.
    """
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            SELECT id, idiom_id, content
            FROM staging_scrapes
            WHERE job = 'definition'
              AND review_status = 'approved';
            """
        )
        rows = cur.fetchall()

        if not rows:
            print("⚠️ No approved definitions to apply.")
            return

        applied_count = 0

        for staging_id, idiom_id, definition in rows:
            # Tiny safety: skip empty content
            if not definition or not definition.strip():
                print(f"⚠️ Skipping empty definition for idiom_id={idiom_id}")
                continue

            # Update idioms table
            cur.execute(
                """
                UPDATE idioms
                SET definition = %s
                WHERE id = %s;
                """,
                (definition.strip(), idiom_id),
            )

            # Mark staging row as applied (for audit)
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

    print(f"✅ Applied {applied_count} approved definitions.")


if __name__ == "__main__":
    apply_definitions()
