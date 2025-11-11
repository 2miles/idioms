## The main flow

fetch_missing → scrape_sources → normalize → stage_results → (apply)

## ?

- Input (fetch phase): list of {id, idiom} that currently have definition IS NULL and haven’t exceeded attempt limits.
- Output (stage/review): list of {idiom_id, idiom, definition, source, status, notes}; status one of success | not_found | error.
- Apply (write-back): for each success, update idioms.definition, set definition_source_url, definition_scraped_at, and log an attempt.
