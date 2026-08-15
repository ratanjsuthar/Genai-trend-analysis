# The Generative AI Boom: A Data-Driven Look at Adoption & Job Market Impact (2022–2026)

> An end-to-end data analysis project tracking how generative AI tools (ChatGPT, Claude, Gemini, Copilot) rose in public interest, developer adoption, and job market demand — with an AI-augmented insight layer that mirrors how modern data analysis is evolving.

# Project Goal

Most "trend" projects stop at pretty charts. This one goes further: it asks whether public search interest, developer activity on GitHub, and job market demand for AI skills actually move together — and uses an LLM to generate plain-English insight summaries from the data, reflecting how AI-augmented analytics is becoming part of the standard data workflow.

## ❓ Questions This Project Answers

1. How has public search interest in major GenAI tools changed since 2022?
2. Did developer adoption on GitHub (stars, new repos, forks) track that same curve, lag it, or lead it?
3. Has demand for AI/GenAI-related skills in job postings grown proportionally?
4. Which tool is winning the "attention race" right now, and is the trend still accelerating or plateauing?

# Data Sources

| Source | Data | Access method |
|---|---|---|
| Google Trends | Search interest index (2022–present) for ChatGPT, Claude AI, Gemini, GitHub Copilot | `pytrends` (unofficial Google Trends API, no key needed) |
| GitHub REST API | Repo counts, stars, forks for AI/LLM-topic repositories over time | `requests` + GitHub API (optional token for rate limits) |
| Hacker News (via Algolia API) | Mention frequency of AI terms in tech discourse | Free public API, no key needed |
| Kaggle: Data Science & AI Job Postings | Skill demand, salary data for AI-related roles | Manual download from kaggle.com |

# Tech Stack

- **Python**: pandas, numpy for wrangling
- **Visualization**: matplotlib, seaborn, plotly (interactive)
- **APIs**: pytrends, requests
- **AI-augmented layer**: Anthropic API (Claude) to auto-generate written insights from summary statistics
- **Optional dashboard**: Streamlit

# Project Structure

```
genai-trends-analysis/
├── data/
│   ├── raw/              # untouched data straight from source
│   └── processed/        # cleaned, merged datasets
├── notebooks/             # exploratory analysis notebooks
├── src/                   # reusable Python scripts (collectors, cleaning, analysis)
├── visuals/                # exported chart images
├── reports/                # final written findings + AI-generated insight summaries
├── requirements.txt
└── README.md
```

# How to Run This Project

```bash
git clone https://github.com/<your-username>/genai-trends-analysis.git
cd genai-trends-analysis
pip install -r requirements.txt

# 1. Collect data
python src/fetch_google_trends.py
python src/fetch_github_trends.py
python src/fetch_hn_mentions.py

# 2. Clean & merge
python src/clean_and_merge.py

# 3. Explore
jupyter notebook notebooks/01_eda.ipynb
```

# Key Findings

*(Fill this in once analysis is complete — 3-5 bullet points with the most interesting, specific insights. This is the section recruiters actually read.)*

- Finding 1...
- Finding 2...
- Finding 3...

# What's Next

- Extend to more tools as they launch
- Build a live-updating Streamlit dashboard
- Add sentiment analysis on Hacker News discussion text

# Auth
 Ratan Lal J 

---
*Built as a portfolio project demonstrating end-to-end data analysis: data collection, cleaning, EDA, trend analysis, and AI-augmented reporting.*
