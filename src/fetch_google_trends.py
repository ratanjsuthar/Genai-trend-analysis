"""
Fetch Google Trends search-interest data for major GenAI tools.

No API key needed — uses pytrends, an unofficial wrapper around the public
Google Trends website.

Output: data/raw/google_trends.csv
"""

import time
import pandas as pd
from pytrends.request import TrendReq

# The tools we're tracking. Google Trends only allows 5 terms per request,
# so we batch and merge on the "isPartial" / date index.
KEYWORDS = ["ChatGPT", "Claude AI", "Gemini AI", "GitHub Copilot", "Midjourney"]
TIMEFRAME = "2022-01-01 2026-08-15"  # from GPT-3.5 era to today


def fetch_trends():
    pytrends = TrendReq(hl="en-US", tz=330)  # tz=330 -> IST offset in minutes

    pytrends.build_payload(
        kw_list=KEYWORDS,
        cat=0,
        timeframe=TIMEFRAME,
        geo="",  # worldwide; use "US", "IN" etc. to restrict to one country
        gprop="",
    )

    df = pytrends.interest_over_time()

    if df.empty:
        raise RuntimeError("No data returned — Google Trends may be rate-limiting you. Wait a few minutes and retry.")

    if "isPartial" in df.columns:
        df = df.drop(columns=["isPartial"])

    df = df.reset_index()  # turns the date index into a normal 'date' column
    return df


if __name__ == "__main__":
    print("Fetching Google Trends data for:", KEYWORDS)
    data = fetch_trends()

    out_path = "data/raw/google_trends.csv"
    data.to_csv(out_path, index=False)
    print(f"Saved {len(data)} rows to {out_path}")
    print(data.head())
