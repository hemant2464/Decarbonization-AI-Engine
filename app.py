import os
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"

import streamlit as st
from crewai import Agent, Task, Crew, LLM

from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS

# 1. YOUR CUSTOM INTERNET TOOL
class SearchInput(BaseModel):
    query: str = Field(description="The search query.")

class InternetSearchTool(BaseTool):
    name: str = "Internet Search"
    description: str = "Use this tool to search the internet for current news and data."
    args_schema: type[BaseModel] = SearchInput

    def _run(self, query: str) -> str:
        results = DDGS().text(query, max_results=3)
        return str(list(results))

search_tool = InternetSearchTool()

# 2. THE WEB UI SETUP (Streamlit Magic)
st.set_page_config(page_title="The Decarbonization Stack Engine", page_icon="🌍")

st.title("🌍 The Decarbonization Stack: AI Agent")
st.markdown("Enter a specific renewable energy sector, and let your local AI Crew research and write a startup pitch.")

# This creates a text box on the website for you to type in
topic = st.text_input("Target Market / Topic:", value="Decentralized solar energy in the Republic of India")

# This creates the "Generate" button
if st.button("🚀 Generate Pitch"):
    
    # This shows a loading spinner on the website while the Mac thinks
    with st.spinner("The AI Crew is working... Check your VS Code terminal to watch them think!"):
        
        # 3. AGENT LOGIC (Running locally)
        os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
        os.environ["OPENAI_API_KEY"] = "NA"

        local_llm = LLM(
            model="ollama/llama3",
            base_url="http://localhost:11434"
        )

        # We pass the 'topic' from the website directly into the agent's goals
        researcher = Agent(
            role='Climate Tech Researcher',
            goal=f'Find 3 current market gaps in: {topic}. Use the internet to find recent news and data.',
            backstory='Expert analyst focusing on decarbonization and energy markets.',
            llm=local_llm,
            tools=[search_tool],
            verbose=True
        )

        writer = Agent(
            role='Startup Technical Writer',
            goal=f'Write a project pitch for a Data Engineering audience based on the research regarding {topic}.',
            backstory='Specialist in making climate tech data sound exciting and viable for startups.',
            llm=local_llm,
            verbose=True
        )

        task1 = Task(description=f"Search the web for current market gaps related to: {topic}.", expected_output="3 bullet points with context.", agent=researcher)
        task2 = Task(description="Write a 2-paragraph startup pitch based on the gaps found.", expected_output="A formatted 2-paragraph pitch.", agent=writer)

        crew = Crew(agents=[researcher, writer], tasks=[task1, task2], verbose=True)
        
        # Start the crew!
        result = crew.kickoff()
        
        # 4. PUSH RESULTS TO THE WEBSITE
        st.success("✅ Pitch Generated Successfully!")
        st.markdown("### Final Startup Pitch")
        st.write(result.raw)