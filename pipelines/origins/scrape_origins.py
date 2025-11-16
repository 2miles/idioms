import os
import time
import requests

from dotenv import load_dotenv

load_dotenv()

# Use best model by default
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_ORIGIN_MODEL", "gpt-5.1")


def _build_origin_prompt(idiom: str, definition: str | None) -> str:
    """
    Builds a concise but highly descriptive prompt for GPT-5.1.
    Produces 1–3 short paragraphs of origin history.
    """
    base = f'Write an accurate and engaging historical origin for the idiom "{idiom}".\n\n'

    if definition:
        base += "Here is its meaning for context:\n" f"{definition}\n\n"

        # base += (
        #     "Requirements:\n"
        #     "- Length: 1–3 short paragraphs.\n"
        #     "- Explain when the expression entered English and how it evolved.\n"
        #     "- Include literal origins, figurative developments, and cultural influences.\n"
        #     "- If the exact origin is uncertain, outline the most credible theories or explicitly say that reliable evidence is limited \n"
        #     "- Avoid filler, clichés, or phrases like “this phrase means.”\n"
        #     "- Tone: concise, factual, slightly narrative — like a scholarly dictionary note.\n"
        #     "- Separate paragraphs with a blank line (\\n\\n)."
        # )
        base += (
            "Guidelines:\n"
            "- Write between 2 sentences and 4 paragraphs total.\n"
            "- If there is very little reliable historical information, use 2–3 concise sentences in a single short paragraph.\n"
            "- If there are multiple distinct historical stages, influences, or credible theories, use up to 3–4 short paragraphs to cover them.\n"
            "- Let the amount of trustworthy information determine the length; do NOT add filler just to reach a target length.\n"
            "- Explain when the expression entered English (if known), its literal and figurative evolution, and any cultural or literary influences.\n"
            "- If the precise origin is uncertain, explicitly say that evidence is limited and summarize the most credible theories without inventing new ones.\n"
            "- Avoid filler, clichés, and phrases like “this phrase means.”\n"
            "- Tone: concise, factual, and slightly narrative — like a scholarly dictionary note."
        )

    return base


def _call_openai_origin(prompt: str) -> dict:
    """
    Low-level call to OpenAI chat API using GPT-5.1.
    Returns {'status': ..., 'origin_text': ...}.
    """

    if not OPENAI_API_KEY:
        return {"status": "error", "origin_text": ""}

    try:
        resp = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You write concise, historically grounded etymology-style summaries.",
                    },
                    {"role": "user", "content": prompt},
                ],
                "max_completion_tokens": 600,  # Enough for a few paragraphs
                "temperature": 0.4,  # More factual, less creative drift
            },
            timeout=60,
        )

    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return {"status": "error", "origin_text": ""}

    if resp.status_code != 200:
        print(f"⚠️ OpenAI HTTP {resp.status_code}: {resp.text[:200]}")
        return {"status": f"http_{resp.status_code}", "origin_text": ""}

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ Unexpected OpenAI response format: {e}")
        return {"status": "error", "origin_text": ""}

    return {"status": "success", "origin_text": content}


def scrape_origins(idioms: list[dict], delay: int) -> list[dict]:
    """
    Generate AI origins for a list of idioms.

    idioms: [{'id': int, 'idiom': str, 'definition': str|None}, ...]

    Returns list of staging-style rows:
      [
        { 'idiom_id': int, 'job': 'origin', 'content': str, 'status': 'success'|'error'|'http_XXX' },
        ...
      ]
    """
    results = []

    for row in idioms:
        idiom_id = row["id"]
        idiom_text = row["idiom"]
        definition = row.get("definition")

        print(f"🧠 Generating origin for: {idiom_text}")
        prompt = _build_origin_prompt(idiom_text, definition)

        res = _call_openai_origin(prompt)
        origin_text = (res.get("origin_text") or "").strip()
        status = res.get("status") or "error"

        results.append(
            {
                "idiom_id": idiom_id,
                "job": "origin",
                "content": origin_text,
                "status": status,
            }
        )

        if status == "success" and origin_text:
            print(f"✅ Got origin for: {idiom_text}")
        else:
            print(f"⚠️ Failed to get origin for: {idiom_text} ({status})")

        time.sleep(delay)

    print(f"\n📊 scrape_origins: {len(results)} results collected")
    return results
