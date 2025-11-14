# Definitions Pipeline (Quick Guide)

A simple workflow for scraping, reviewing, and applying idiom definitions.

## 1. Scrape missing definitions

```bash
python3 -m pipelines.definitions.run
```

Scrapes definitions for idioms with no definition and inserts them into `staging_scrapes` table in Supabase with `review_status = 'pending'`.

## 2. Review and edit

Open `staging_scrapes` in the DB UI.

For each row:

- Edit content if needed.
- Set review_status = 'apprived' for the definition you want
- (Optional) set the status as 'rejected' if you dont like it.

Only rows marked apprived will be applied.

## 3. Apply approved definitions

```bash
python3 -m pipelines.definitions.apply_definitions
```

This:

- Copies each approved content into idioms.definition
- Marks the staging row review_status = 'applied'

## 4. Cleanup

Delete all applied staging rows

```bash
python3 -m pipelines.definitions.cleanup
```
