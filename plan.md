## Architecture & Repo Shape

Keep the repo but give it a tidy structure with three layers:

1. connectors/ – talking to Supabase/Postgres, local files, OpenAI
2. pipelines/ – “definition”, “examples”, “origin_ai” jobs (orchestration & flow)
3. scrapers/ – site-specific logic you already wrote (definitions, examples)
4. normalizers/ – tiny helpers that clean/shape scraped text
5. review/ – export/import of CSV/JSON for manual QA
6. cli/ – thin CLI entrypoints (one command per pipeline + shared flags)
7. state/ – optional on-disk cache (JSON) if you want; better: DB tables below

This lets you share connectors (Supabase session, OpenAI client) and reuse scrapers across pipelines.

## Database & “What needs updating?”

Your app already has idioms, examples, etc. Add lightweight fields/tables to drive incremental, idempotent runs:

### idioms

- definition (TEXT)
- definition_source_url (TEXT)
- definition_scraped_at (TIMESTAMPTZ)
- origin_ai (TEXT)
- origin_meta (JSONB) — { "model": "...", "created_at": "...", "prompt_version": "...", "notes": "" }

### examples

- Separate table you already use; add source_url and scraped_at if not present.

### scrape_attempts (new helper table)

- id (PK), idiom_id (FK), job (ENUM: definition | examples | origin_ai)
- source (TEXT) – which site/scraper was tried, or “openai”
- status (ENUM: success | not_found | rate_limited | error)
- error_msg (TEXT, nullable)
- attempt_count (INT)
- last_attempt_at (TIMESTAMPTZ)

This replaces your “running list of attempted” with a durable, queryable log. It enables:

- “needs work” views: idioms missing a field and with attempt_count < N
- backoff: skip items recently rate-limited
- retry strategy: rotate sources, space out retries

Optional but nice:
• ai_generations table to version your origin_ai drafts (keep history). Only the latest accepted text is copied into idioms.origin_ai.

## How each pipeline would run

1. Definitions (your target flow)

Source of truth: idioms rows with definition IS NULL.

Flow

- Query Supabase for id, idiom missing definition, left-join scrape_attempts to exclude over-attempted ones.
- Scrape across 1–2 preferred sources in order (polite delays, rotate sources on 404).
- Normalize result (trim, remove footers, collapse whitespace; preserve italics/quotes if you want).
- Review mode (default): write candidates to a CSV/JSON “staging” artifact with columns: idiom_id, idiom, definition, source_url, confidence, notes.
- Apply mode (explicit): upsert to idioms.definition, set definition_source_url, definition_scraped_at, and log a success attempt.
- Log not_found or error attempts with reason and increment attempt_count.

2. Example sentences

Source of truth: examples table grouped by idiom.

Flow
• Select idioms under a threshold (e.g., < 2 examples).
• Scrape examples; normalize (strip author bios, keep sentence punctuation, length bounds).
• Deduplicate using a content hash column on examples to avoid re-inserts.
• Same review vs apply split.
• Record attempts with status; store source_url, scraped_at.

3. AI-generated origin

Source of truth: idioms rows with origin_ai IS NULL.

Flow

- Build your prompt (the headless prompt you liked), add a small “guardrail” instruction (“If origin is disputed, explain major theories; avoid speculation presented as fact.”).
- Temperature ~0.3–0.5 for consistency; cap length to a few paragraphs.
- Save to ai_generations (versioned), store meta in origin_meta. In review mode, only export; in apply, copy to idioms.origin_ai.
- Optionally auto-reject outputs that trip sanity rules (e.g., too short/long; contains “As an AI…”; has no dates; etc.) and mark the attempt as error for manual check.

Idempotency & Safety

- Dry run first (review mode) is default. You opt into writes with --apply.
- Upserts keyed by idiom_id (for definition & origin_ai) and by (idiom_id, hash) for examples.
- Retry strategy: exponential backoff per source with max attempt_count per idiom per job.
- Politeness: respect robots.txt for scrapers; random small sleeps; rotate headers if needed.

Provenance & Transparency

- Store definition_source_url and examples.source_url.
- Store origin_meta JSONB (model, prompt version, date).
- In your app UI, you can show a tiny “source” link for definitions/examples and a subtle “AI-generated” badge for origins.

Review Workflow (keeps you in control)

- Export: Each run emits a dated CSV/JSON in review/exports/ with candidates and diffs (old vs new).
- Inspect: You spot-check a sample (or everything if you want). Consider adding a small “accept all except flagged” path.
- Apply: Rerun the same job with --apply --import=that_file.json to push only vetted rows.

Configuration & Secrets

- Use env vars (.env) for Supabase URL/key and OpenAI key.
- Keep repo public if you want, but put secrets outside (or keep this repo private if it’s tightly coupled to your DB). If you ever want to open-source the scraping logic, split connectors/ (secrets) behind an interface and publish only scrapers/ + pipelines/ minus credentials.

CLI surface (ergonomic, consistent)

- idioms defs fetch [--limit=200] [--review | --apply]
- idioms examples fetch [--min-needed=2] [--review | --apply]
- idioms origins generate [--limit=200] [--review | --apply]
- Shared flags: --only-unattempted, --max-attempts=3, --since=2025-10-01, --sources=oxford,cambridge, --prompt-version=v1.

Testing & Quality Gates

- Unit tests for normalizers (pure text transforms).
- Golden-file tests: given scraped HTML snippets, assert the cleaned text.
- Tiny integration test against a throwaway Supabase schema (local Docker) to validate upsert logic and scrape_attempts behavior.
- A “sample run” mode that limits to 3 idioms and writes to a temp schema.

When to consider a new repo instead

Create a separate repo only if:

- You want to open-source the scrapers but keep your Supabase bindings/private prompts private.
- You want a generic “Idiom ETL” library others can import, and your app-specific connectors live elsewhere.

Otherwise, staying in idioms with the structure above will be simpler and faster.

⸻

If you want, paste a snippet of your current scraper interfaces and how you’re inserting into Postgres now. I’ll map them into the pipeline shape above and suggest the smallest refactor that gets you all of this (review/apply, attempts table, provenance) with minimal churn.
