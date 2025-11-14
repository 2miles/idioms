# Definitions Pipeline (Quick Guide)

A simple workflow for scraping, reviewing, and applying idiom definitions.

## 1. Scrape missing definitions

```bash
python3 -m pipelines.definitions.run
```

Scrapes definitions for idioms with no definition and inserts them into `staging_scrapes` table in Supabase with `review_status = 'pending'`.

## 2. Review and edit

Open `staging_scrapes` in the DB UI.

For each job = 'definition' row:

- Edit content if needed.
- Set review_status = 'apprived' for the definition you want
- (Optional) set the status as 'rejected' if you dont like it.

Only rows marked apprived will be applied.

## 3. Apply approved definitions

```bash
python3 -m pipelines.definitions.apply_definitions
```

This writes the approved definition into idioms.definition and marks the staging row as applied.

## 4. Cleanup

```bash
python3 -m pipelines.definitions.cleanup
```

Removes all applied definition rows from staging.

# Examples Pipeline (Quick Guide)

The workflow is nearly identical to the definitions pipeline, but examples may produce multiple rows per idiom.

## 1. Scrape missing examples

```bash
python3 -m pipelines.examples.run
```

Fetches idioms that have no entries in idioms_examples and scrapes one or more example sentences for each. Results are added to staging_scrapes with job = 'example'.

## 2. Review and edit

Open `staging_scrapes` in the DB UI and edit/review any examples.

## 3. Apply approved examples

```bash
python3 -m pipelines.exmaples.apply_examples
```

## 4. Cleanup

Delete all applied staging rows

```bash
python3 -m pipelines.examples.cleanup
```
