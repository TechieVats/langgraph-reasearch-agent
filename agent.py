from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

# --- Shared state between agents ---
class ResearchState(TypedDict):
    topic: str
    search_results: List[str]
    source_urls: List[str]
    summary: str
    quality_score: int

# --- LLM (free, fast) ---
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# --- Search tool ---
search_tool = TavilySearchResults(max_results=3)

# --- Agent 1: Researcher ---
def researcher_agent(state: ResearchState):
    print("\nResearcher agent: searching the web...")
    results = search_tool.invoke(state["topic"])
    content = [r["content"] for r in results]
    source = [r["url"] for r in results]
    print(f"   Found {len(content)} results.")
    return {"search_results": content,
            "source_urls": source}

# --- Agent 2: Summarizer ---
def summarizer_agent(state: ResearchState):
    print("Summarizer agent: reading and scoring results...")
    combined = "\n\n".join(state["search_results"])

    prompt = f"""You have these search results about '{state["topic"]}':

{combined}

1. Write a 3-sentence summary.
2. Score the quality of information from 1-10.

Format your response exactly like this:
SUMMARY: <your summary>
SCORE: <number only>"""

    response = llm.invoke(prompt)
    text = response.content

    summary = text.split("SUMMARY:")[1].split("SCORE:")[0].strip()
    score = int(text.split("SCORE:")[1].strip())
    return {"summary": summary, "quality_score": score,"source_urls": state["source_urls"]}

# --- Conditional: retry if quality is too low ---
def should_retry(state: ResearchState):
    if state["quality_score"] < 5:
        print("Low quality, retrying research...")
        return "low_quality"
    return "high_quality"

# --- Save results ---
def save_results(state: ResearchState):
    with open("results.txt", "w") as f:
        f.write(f"Topic: {state['topic']}\n")
        f.write(f"Quality Score: {state['quality_score']}/10\n\n")
        f.write(f"Summary:\n{state['summary']}\n")
        f.write("\nSources:\n")
        for i, url in enumerate(state["source_urls"], 1):
            f.write(f"{i}. {url}\n")
    print("Done! Results saved to results.txt")
    return state

# --- Build the graph ---
graph = StateGraph(ResearchState)

graph.add_node("researcher", researcher_agent)
graph.add_node("summarizer", summarizer_agent)
graph.add_node("save", save_results)

graph.set_entry_point("researcher")
graph.add_edge("researcher", "summarizer")
graph.add_conditional_edges(
    "summarizer",
    should_retry,
    {"low_quality": "researcher", "high_quality": "save"}
)
graph.add_edge("save", END)

app = graph.compile()

# --- Run ---
if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    result = app.invoke({
        "topic": topic,
        "search_results": [],
        "source_urls": [],
        "summary": "",
        "quality_score": 0
    })
    print(f"\nSummary:\n{result['summary']}")
    print(f"\nQuality Score: {result['quality_score']}/10")