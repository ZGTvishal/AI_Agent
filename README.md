# AI Research Agent

A learning project for building a basic AI Agent using LangChain and LangGraph.
The agent helps with research tasks by searching the web, querying Wikipedia,
searching Google Scholar for academic papers, and saving results to a text file.

## What it does

- Takes a research query from the user
- Uses multiple tools to gather information (web search, Wikipedia, Google Scholar)
- Synthesises the results into a structured research response
- Saves the output to `research_output.txt`

## Models used

- **Google Gemma 4 31B** via Google AI Studio API (current)
- Previously tested with OpenAI GPT-4o-mini and Anthropic Claude

## Tech stack

- Python 3.13
- LangChain 0.3.25
- LangGraph 0.2.68
- LangChain Google GenAI 2.1.4
- Pydantic 2.x
- DuckDuckGo Search (ddgs)
- Wikipedia API
- Scholarly (Google Scholar scraper)

## Project structure

AI_Agent/
├── main.py              # Agent setup and execution
├── tools.py             # Tool definitions (search, wiki, scholar, save)
├── requirements.txt     # All dependencies
├── .env                 # API keys (not committed to Git)
└── research_output.txt  # Generated research outputs

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd AI_Agent
```

### 2. Create and activate a Conda environment (recommended)

```bash
conda create -n ai-agent python=3.13
conda activate ai-agent
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Key packages installed:

langchain==0.3.25
langchain-core==0.3.65
langchain-community==0.3.24
langchain-google-genai==2.1.4
langgraph==0.2.68
ddgs==9.11.4
scholarly==1.7.11
python-dotenv==1.2.2
pydantic==2.12.5
wikipedia==1.4.0

### 4. Set up your .env file

Create a `.env` file in the root of the project:

GEMMA_API_KEY=your_google_ai_studio_key_here

Get your free API key from [Google AI Studio](https://aistudio.google.com).

### 5. Run the agent

```bash
python main.py
```

You will be prompted to enter a research topic:

What can I help you research? Impact of AI on cognitive thinking

The agent will search the web, Wikipedia, and Google Scholar, then save
the structured output to `research_output.txt`.

## Important notes

- `scholarly` scrapes Google Scholar directly and may occasionally be
  rate-limited. If searches fail, wait a few minutes and retry.
- Tool names must be lowercase with no spaces to comply with the Google
  Gemini API's function naming rules.
- The E4B and E2B Gemma 4 models are not available via the API — they are
  on-device only. Use `gemma-4-31b-it` or `gemma-4-26b-a4b-it` for API access.

## .gitignore

Make sure your `.env` and output files are not committed:
.env
research_output.txt
pycache/
*.pyc

## Lessons learned building this

- LangChain 1.x and LangGraph 1.x have a completely different API from 0.3.x —
  pin your versions to avoid breaking changes mid-project.
- Google Gemini API rejects tool/function names with capital letters or spaces.
- The `duckduckgo_search` package was renamed to `ddgs` — use `ddgs` directly.
- `WikipediaQueryRun` has a known type annotation bug in newer versions of
  `langchain-community` — wrapping `WikipediaAPIWrapper` in a plain `Tool`
  avoids it.