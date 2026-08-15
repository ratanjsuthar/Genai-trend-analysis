"""
Fetch monthly mention counts of AI tools in Hacker News story titles.

Uses the free HN Algolia Search API — no key needed, no rate-limit hassle.
Docs: https://hn.algolia.com/api

Output: data/raw/hn_mentions_by_month.csv
"""

import time
import requests
import pandas as pd

TERMS = ["ChatGPT", "Claude", "Gemini", "Copilot", "Midjourney"]

# Monthly windows from Jan 2022 to Aug 2026 (unix timestamps, UTC)
MONTHS = pd.date_range("2022-01-01", "2026-08-01", freq="MS")


def unix_range(month_start):
    start = int(month_start.timestamp())
    end = int((month_start + pd.offsets.MonthBegin(1)).timestamp())
    return start, end


def fetch_mentions(term: str, start_ts: int, end_ts: int) -> int:
    url = "https://hn.algolia.com/api/v1/search"
    params = {
        "query": term,
        "tags": "story",
        "numericFilters": f"created_at_i>={start_ts},created_at_i<{end_ts}",
        "hitsPerPage": 0,  # we only need the total count, not the actual stories
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("nbHits", 0)


if __name__ == "__main__":
    rows = []
    for term in TERMS:
        for month in MONTHS:
            start_ts, end_ts = unix_range(month)
            try:
                count = fetch_mentions(term, start_ts, end_ts)
                rows.append({"term": term, "month": month.strftime("%Y-%m"), "mention_count": count})
            except requests.HTTPError as e:
                print(f"Failed for {term} {month}: {e}")
            time.sleep(0.3)
        print(f"Done: {term}")

    df = pd.DataFrame(rows)
    out_path = "data/raw/hn_mentions_by_month.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")
