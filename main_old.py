import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from google import genai
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_agent
from tools import search_tool, wiki_tool, save_tool



load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

API_KEY = os.getenv("GEMMA_API_KEY")
client = genai.Client(api_key=API_KEY)

#llm = ChatOpenAI(model="gpt-4o-mini")
#llm2 = ChatAnthropic(model="claude-3-5-sonnet-20241022")
llm = client.models.generate_content(model="gemma-4-E4B-it")


parser = PydanticOutputParser(pydantic_object=ResearchResponse)


tools = [search_tool, wiki_tool, save_tool]
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=f"""
    You are a research assistant that will help generate a research paper.
    Answer the user query and use necessary tools.
    Wrap the output in this format and provide no other text:
    {parser.get_format_instructions()}
    """
)

query = input("What can I help you research?")

raw_response = agent.invoke({"messages": [{"role": "user", "content": query}]})



try:
    structured_response = parser.parse(raw_response.get("output")[0]["text"])
    print(structured_response)
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)

