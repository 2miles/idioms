# Idioms

Given a list of idioms, this program will aquire the definitions and append them to a csv file containig compilation of idiom data.

The output will be in three files. All the idioms, just the idioms with definitions, and just the idioms without definitions yet.

## first run:

```
python3 run_scraper.py
```

It is expecting a numbered markdown list of idioms named `incoming.md` to be in the directory.

It takes that list and scrapes free dictionary for all the definitions.
The output will be a `.txt` file representing the idioms data scraped.

## Then run:

```
python3 add_new_results.py
```

The output will be in the files `idioms.csv`, `idioms_complete_sorted.csv`, and `idioms_incomplet_sorted.csv`. They will be appended with the definitions in `incoming.md`.

Don't do the same list of words twice. It doesn't look for doubles and will just re-add them.
