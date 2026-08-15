"""
Fetch a REAL historical trend of GitHub repo creation for AI/LLM topics.

Instead of a single point-in-time snapshot, this queries how many repos
were CREATED per quarter for each topic since 2022 — giving you an actual
time series in one run, no need to wait weeks collecting daily snapshots.

Uses the public GitHub Search API. Works without auth at 10 requests/min;
if you hit rate limits, set a GITHUB_TOKEN env var (free personal access
token from github.com/settings/tokens, no special scopes needed) to get
30 requests/min.

Output: data/raw/github_repo_creation_by_quarter.csv
"""

import os
import time
import requests
import pandas as pd

TOPICS = ["chatgpt", "claude-ai", "gemini-ai", "llm", "generative-ai", "copilot"]
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

# Quarterly date ranges from Q1 2022 through today
QUARTERS = [
    ("2022-01-01", "2022-03-31"), ("2022-04-01", "2022-06-30"),
    ("2022-07-01", "2022-09-30"), ("2022-10-01", "2022-12-31"),
    ("2023-01-01", "2023-03-31"), ("2023-04-01", "2023-06-30"),
    ("2023-07-01", "2023-09-30"), ("2023-10-01", "2023-12-31"),
    ("2024-01-01", "2024-03-31"), ("2024-04-01", "2024-06-30"),
    ("2024-07-01", "2024-09-30"), ("2024-10-01", "2024-12-31"),
    ("2025-01-01", "2025-03-31"), ("2025-04-01", "2025-06-30"),
    ("2025-07-01", "2025-09-30"), ("2025-10-01", "2025-12-31"),
    ("2026-01-01", "2026-03-31"), ("2026-04-01", "2026-06-30"),
]


def fetch_repo_count(topic: str, start: str, end: str) -> int:
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    url = f"https://api.github.com/search/repositories?q=topic:{topic}+created:{start}..{end}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json().get("total_count", 0)


if __name__ == "__main__":
    rows = []
    sleep_time = 6.5 if not GITHUB_TOKEN else 2.1  # respect rate limits

    for topic in TOPICS:
        for start, end in QUARTERS:
            print(f"Fetching: topic={topic}, quarter={start[:7]}")
            try:
                count = fetch_repo_count(topic, start, end)
                rows.append({"topic": topic, "quarter_start": start, "repo_count": count})
            except requests.HTTPError as e:
                print(f"  Failed for {topic} {start}: {e}")
            time.sleep(sleep_time)

    df = pd.DataFrame(rows)
    out_path = "data/raw/github_repo_creation_by_quarter.csv"
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} rows to {out_path}")
    print(df.head(10))
