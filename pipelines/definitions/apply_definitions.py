def apply_definitions():
    """
    Placeholder for applying approved staged definitions to the idioms table.
    Currently just prints what it *would* do.
    """
    print("🧩 [Stub] apply_definitions() called — will later update idioms from staging_scrapes.")


# def apply_definitions():
#     """
#     Apply approved staged definitions to idioms table.
#     """
#     with get_conn() as conn, conn.cursor() as cur:
#         cur.execute(
#             """
#             SELECT id, idiom_id, content
#             FROM staging_scrapes
#             WHERE job = 'definition' AND review_status = 'approved';
#         """
#         )
#         rows = cur.fetchall()

#         for staging_id, idiom_id, definition in rows:
#             cur.execute(
#                 """
#                 UPDATE idioms
#                 SET definition = %s
#                 WHERE id = %s;
#             """,
#                 (definition, idiom_id),
#             )

#             cur.execute(
#                 """
#                 UPDATE staging_scrapes
#                 SET review_status = 'applied'
#                 WHERE id = %s;
#             """,
#                 (staging_id,),
#             )

#         conn.commit()

#     print(f"✅ Applied {len(rows)} approved definitions.")
