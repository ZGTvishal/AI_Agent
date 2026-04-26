from typing import Optional
from langchain_community.tools import WikipediaQueryRun
from ddgs import DDGS 
from langchain_community.utilities import WikipediaAPIWrapper
from scholarly import scholarly
from langchain_core.tools import Tool
from langchain_core.tools import BaseTool
import uuid
from datetime import datetime
from langchain_community.retrievers import ArxivRetriever

retriever = ArxivRetriever(
    load_max_docs=10,
    get_full_documents=True,
)


def save_to_txt(data: str, filename:str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Rearch output --- \nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)
    
    return f"Data Successfully saved to {filename}"

def ddg_search(query: str) -> str:
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n".join([r["body"] for r in results])
    

def google_scholar_search(query: str) -> str:
    try:
        results = []
        search_results = scholarly.search_pubs(query)
        for i, paper in enumerate(search_results):
            if i >= 5:
                break
            title = paper["bib"].get("title", "No title")
            author = paper["bib"].get("author", "Unknown")
            year = paper["bib"].get("pub_year", "Unknown")
            abstract = paper["bib"].get("abstract", "No abstract available")
            results.append(
                f"Title: {title}\nAuthor: {author}\nYear: {year}\nAbstract: {abstract}"
            )
        return "\n---\n".join(results) if results else "No results found"
    except Exception as e:
        return f"Google Scholar search failed: {str(e)}"
    
def arxiv_search(query: str) -> str:
    retriever.invoke(query)



save_tool = Tool(
    name="save_to_file",
    func=save_to_txt,
    description="Saves the research data to a custom file",
)

google_tool = Tool(
    name="google_scholar",
    func= google_scholar_search,
    description="search the google scholar library for relevent papers"
)



search_tool = Tool(
    name="web_search",
    func=ddg_search,
    description="Search the web for information",
)

arxiv_tool = Tool(
    name = "arxiv_search",
    func=arxiv_search,
    description="search arxiv database and retrive 10 papers on the related topic"
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper = api_wrapper)



