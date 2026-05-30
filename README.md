# LangGraph Research Agent

A multi-agent research system built with LangGraph and Groq.

## What it does
- Agent 1 (Researcher): searches the web live using Tavily
- Agent 2 (Summarizer): reads results, writes a summary, scores quality
- If quality score is below 5, automatically retries research

## Agent Flow
Researcher → Summarizer → Save
                ↑              |
                |__ retry <5 __|

## Setup
pip install -r requirements.txt
cp .env.example .env
# Add your API keys to .env

## Run
python agent.py

## Tech used
LangGraph, LangChain, Groq (llama-3.3-70b), Tavily Search