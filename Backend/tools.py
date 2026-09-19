
from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
import os 
from tavily import TavilyClient
from rich import print

import requests
from bs4 import BeautifulSoup


tavily = TavilyClient(os.getenv(key="TAVILY_API_KEY"))

@tool 
def web_search(query:str)->str:
    """ You are able to search recent and reliable data from browser and retruns the only title, url and snippet based on query """
    result = tavily.search(query=query, search_depth="basic", max_results=3)

    output = []
    for i in result['results']:
        output.append(
            f"Title: {i['title']}\nURL: {i['url']}\nContent: {i['content'][:200]}...\n"
        )
    return "\n--------\n".join(output)

@tool 
def scrape_url(url:str)->str:
    """
        Scrape and return the cleanest text from a given URL for deeper analysis in English.
    """
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"}) 
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Remove unwanted elements
        for i in soup(["script", "style", "nav", "footer"]):
            i.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000] 
    except Exception as e:
        return f"Error scraping the URL: {e}"
    

