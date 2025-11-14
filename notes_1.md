### Small local script to populate origins

```python
# generate_origins.py
import os, requests, time
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(os.getenv("DB_URL_SUPABASE_DEV"))
cur = conn.cursor()
cur.execute("SELECT id, idiom, meaning FROM idioms WHERE origin_ai IS NULL;")
rows = cur.fetchall()

for id, idiom, meaning in rows:
    prompt = f"Write a short (2–4 sentence) origin story for the idiom '{idiom}'. Be factual and concise, like an entry in a dictionary. If unknown, give a plausible historical explanation."
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
        json={
            "model": "gpt-5",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 150,
            "temperature": 0.7
        }
    )
    origin_text = resp.json()["choices"][0]["message"]["content"].strip()
    cur.execute("UPDATE idioms SET origin_ai = %s WHERE id = %s;", (origin_text, id))
    conn.commit()
    time.sleep(1.5)  # avoid rate limits

cur.close()
conn.close()
```

Run this once or in batches until all the itioms have been attempted.

(Maybe add a flag that creates a max number of idioms to limit the volume at any one time)

### Plan: Ai generated origins at sacale

#### 1. Add a nullable origin_ai column

In Supabase / Postgres:

```sql
ALTER TABLE idioms ADD COLUMN origin_ai TEXT;
```

#### 4. Optional refinements

- You can use temperature=0.3 if you want more factual consistency.
- Add a WHERE origin_ai IS NULL filter so you can rerun safely without overwriting.
- Later, you could add a “Regenerate” button in your admin panel to refresh individual entries.

#### 5. prompt example:

```python
prompt = f"""Write an accurate and engaging explanation of the likely origin and historical development of the idiom "{idiom}".
Treat it as a short reference-style article (2–4 paragraphs). Focus on when and how it entered English, its literal and figurative evolution, and any cultural influences.
If uncertain, describe the most credible theories. Tone: concise, factual, and slightly narrative — like a scholarly dictionary entry that’s enjoyable to read."""
```

#### 6. prompt headless style:

🧠 Prompt (headless style)

Write an accurate and engaging explanation of the likely origin and historical development of the idiom “{{idiom}}.”

- Treat it as a short reference-style article (2–4 paragraphs).
- Focus on when and how the expression entered English, its literal and figurative evolution, and any cultural or literary influences.
- If the precise origin is uncertain, describe the most credible theories and why they are plausible.
- Avoid filler, clichés, or phrases like “this phrase means.”
- Tone: concise, factual, and slightly narrative — like a scholarly dictionary entry that’s enjoyable to read.
