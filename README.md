# LangGraph Research Agent

A multi-agent research system built with LangGraph and Groq that searches
the web, summarizes findings, and automatically retries on low quality results.

## Agent Flow

```
START → [Researcher] → [Summarizer] → [Save] → END
              ↑               |
              |__ score < 5 __|
```

## What it does

- **Researcher Agent** — searches the web live using Tavily
- **Summarizer Agent** — reads results, writes a summary, scores quality 1-10
- **Auto retry** — if quality score is below 5, automatically retries research
- **Saves results** — final summary and score saved to results.txt

## Setup

1. Clone the repo
2. Install dependencies
```bash
pip install -r requirements.txt
```
3. Copy the env file
```bash
cp .env.example .env
```
4. Add your API keys to `.env`
```
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```

## Run

```bash
python agent.py
```

## Sample Output

```
Researcher agent: searching the web...
   Found 3 results.
Summarizer agent: reading and scoring results...
   Quality score: 8/10
Done! Results saved to results.txt

Summary:
The highest scorer in the IPL so far is Virat Kohli...

Quality Score: 8/10
```

## Tech Stack

| Tool | Purpose |
|------|---------|
| LangGraph | Multi-agent orchestration |
| LangChain | LLM framework |
| Groq | Fast LLM inference (llama-3.3-70b) |
| Tavily | Live web search |
| Python 3.11 | Language |
