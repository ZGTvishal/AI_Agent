import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchResponse)

llm = ChatGoogleGenerativeAI(
    model="gemma-4-31b-it",
    google_api_key=os.getenv("GEMMA_API_KEY"),
    temperature=1.0
)

tools = [search_tool, wiki_tool, save_tool]

system_prompt = f"""
You are a research assistant that will help generate a research paper.
Answer the user query and use necessary tools.
Wrap the final output in this format and provide no other text:
{parser.get_format_instructions()}
"""

agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=system_prompt,
)

query = input("What can I help you research? ")

raw_response = agent.invoke({
    "messages": [HumanMessage(content=query)]
})

#raw_response = agent.invoke({"messages": [{"role": "user", "content": query}]})

try:
    output = raw_response["messages"][-1].content
    if isinstance(output, list):
        output_text = " ".join(
            block["text"] if isinstance(block, dict) else block
            for block in output
            if (isinstance(block, dict) and "text" in block) or isinstance(block, str)
        )
    else:
        output_text = output
    structured_response = parser.parse(output_text)
    #print(structured_response)

    from tools import save_to_txt
    save_to_txt(structured_response)
except Exception as e:
    print("Error parsing response:", e)
    print("Raw Response:", raw_response)