from langchain_community.tools import WikipediaQueryRun
from ddgs import DDGS 
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool
import uuid
from datetime import datetime


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


save_tool = Tool(
    name="Save_txt_to_file",
    func=save_to_txt,
    description="Saves the research data to a custom file",
)

# search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=ddg_search,
    description="Search the web for information",
)


api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = WikipediaQueryRun(api_wrapper = api_wrapper)

