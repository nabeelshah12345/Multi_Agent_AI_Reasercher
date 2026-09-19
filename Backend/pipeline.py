
from agents import search_agent, reader_agent, writer_chain, score_chain, refine_chain
import re

def run_search(topic: str) -> str:
    search = search_agent()
    result = search.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    return result["messages"][-1].content


def run_read(topic: str, search_result: str) -> str:
    reader = reader_agent()
    result = reader.invoke({
        "messages": [("user",
                      f"Based on the following search result about '{topic}', "
                      f"pick the most relevant URL and scrape it for deep content.\n\n"
                      f"Search Results: \n{search_result[:700]}")]
    })
    return result["messages"][-1].content


def run_write(topic: str, search_result: str, scraped_result: str) -> str:
    combined = f"Search Result: \n{search_result}\n\nScraped Content: \n{scraped_result}"
    return writer_chain.invoke({"topic": topic, "research": combined})


def run_score(report: str) -> dict:
    feedback = score_chain.invoke({"report": report})
    match = re.search(r"Score:\s*(\d+)/10", feedback)
    score = int(match.group(1)) if match else None
    return {"feedback": feedback, "score": score}


def refine_report(report: str, feedback: str) -> str:
    return refine_chain.invoke({"report": report, "feedback": feedback})


# Ye function FastAPI ke /research route ke liye reh sakta hai (bina live UI ke, jaise backend API use)
def research_pipeline(topic: str) -> dict:
    search_result = run_search(topic)
    scraped_result = run_read(topic, search_result)
    report = run_write(topic, search_result, scraped_result)
    score_data = run_score(report)
    return {
        "search_result": search_result,
        "scraped_result": scraped_result,
        "report": report,
        "feedback": score_data["feedback"],
        "score": score_data["score"],
    }
