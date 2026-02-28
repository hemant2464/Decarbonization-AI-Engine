import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS

# 1. BUILD A NATIVE CREWAI TOOL (Bypasses all library conflicts!)
class SearchInput(BaseModel):
    query: str = Field(description="The search query.")

class InternetSearchTool(BaseTool):
    name: str = "Internet Search"
    description: str = "Use this tool to search the internet for current news and data."
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        # This is the actual engine doing the work
        results = DDGS().text(query, max_results=3)
        return str(list(results))

# Initialize your new custom tool
search_tool = InternetSearchTool()

# 2. SETUP LOCAL BRAIN
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "NA"

local_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

# 3. THE TEAM
researcher = Agent(
  role='Climate Tech Researcher',
  goal='Find 3 current market gaps in Indian renewable energy for 2026. Use the internet to find recent news and data.',
  backstory='Expert analyst from Kolkata focusing on decentralized solar.',
  llm=local_llm,
  tools=[search_tool], # <--- Pass your native tool here!
  verbose=True
)

writer = Agent(
  role='Startup Technical Writer',
  goal='Write a project pitch for a Data Engineering audience based on the research.',
  backstory='Specialist in making climate tech data sound exciting.',
  llm=local_llm,
  verbose=True
)

# 4. THE PLAN
task1 = Task(description="Search the web for current India solar gaps.", expected_output="3 bullet points with context.", agent=researcher)
task2 = Task(description="Write a 2-paragraph pitch.", expected_output="A 2-paragraph pitch.", agent=writer)

# 5. THE START
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=True
)

print("--- 🚀 STARTING THE CREW ---")
result = crew.kickoff()
print("--- ✅ DONE ---")
print(result)