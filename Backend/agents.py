

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools import web_search, scrape_url

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

def search_agent():
    return create_agent(
        model=llm,
        tools=[web_search],
        system_prompt=(
            "You are a search relay agent. Call the web_search tool exactly once "
            "with a clear query. Then return ONLY the raw results from the tool "
            "(URL, Title, Snippet) exactly as given, with no extra analysis, "
            "no additional facts from your own knowledge, and no elaboration. "
            "Do not write a report. Just relay the search results."
        )
    )
def reader_agent():
    return create_agent(
        model=llm,
        tools=[scrape_url]
    )
    
# writer Chain Prompt
writer_prompt = ChatPromptTemplate.from_messages([
    ("system","You are an expert research writer. Write clear, structured and insightful reports"),
    ("human", """Write a detailed research report on the topic below,
Topic: {topic}
Research Gathered: {research}

Structure and response in this format the report as:
Introduction
Key Findings (Minimum 3 and Maximum 5 Well Explained Points)
Conclusion 
Sources (List all urls found in the research)

Be detailed factual and Professional.
and date must be match with url provided, otherwise ignore the date
     """), 
])

writer_chain = writer_prompt | llm | StrOutputParser()


# Scoring chain prompt
score_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic.Be honest and specific."),
    ("human", """

Report: {report}
Respond in this exact format

Score: X/10

Strength: 
....
....

Areas to Improve:
....
....

One line Verdict:
....
     """)
])
score_chain = score_prompt | llm | StrOutputParser()



refine_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer who revises reports based on critic feedback."),
    ("human", """
Original Report:
{report}

Critic Feedback:
{feedback}

Revise the report to address the weaknesses mentioned in the feedback.
Keep the same structure (Introduction, Key Findings, Conclusion, Sources)
but improve clarity, add missing details, and fix the issues raised.
     """)
])
refine_chain = refine_prompt | llm | StrOutputParser()