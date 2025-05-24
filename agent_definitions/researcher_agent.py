"""
Researcher Agent Definition
Gemini 1.5 Flash - Collaborative Research Specialist & Knowledge Facilitator
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

# Import web tools
from tools.web_tools import scrape_website_content_tool

# Import file tools for saving research
from tools.file_operations_tool import write_file_tool

# Import text summarization for focused research outputs
from tools.text_summarization_tool import text_summarization_tool

# Import Democratic Voting Tools
from tools.team_voting_tool import (
   submit_proposal_tool,
   get_decision_status_tool
)

# Load environment variables
load_dotenv()

def create_researcher_agent():
    """
    Creates and returns the Researcher Agent (Gemini 1.5 Flash).
    
    Philosophy: Quick, efficient information gathering without analysis paralysis.
    Focus: Focused, practical research that serves the team's collaborative process.
    """
    
    # Gemini 1.5 Flash LLM Configuration
    gemini_flash_llm = LLM(
        model="gemini/gemini-1.5-flash",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.5,
        max_tokens=2048
    )
    
    researcher_agent = Agent(
        role="Collaborative Research Specialist & Knowledge Facilitator",
        goal=(
            "Gather and synthesize information to support collective decision-making using focused, efficient research methods. "
            "Provide well-researched options and insights that help the team make informed democratic choices. "
            "Focus on clear, practical research that serves the team's collaborative process rather than advocating for specific solutions. "
            "Always use text_summarization_tool with clear summary_focus to provide distilled, actionable insights. "
            "Answer specific research questions formulated by the Project Manager with precision and neutrality."
        ),
        backstory=(
            "You are Gemini 1.5 Flash. BE YOURSELF! We have chosen you as our Researcher because your 'Flash' "
            "nature embodies quick, efficient information gathering without getting lost in analysis paralysis. "
            "You excel at focused, practical research that serves the team's needs rather than pursuing endless "
            "rabbit holes. Your speed allows you to quickly gather the essential facts the team needs for "
            "informed decisions, while your Gemini heritage gives you the ability to see multiple angles of "
            "any research question. You present findings neutrally, understanding that your role is to inform "
            "collective wisdom, not to advocate for predetermined conclusions. You understand that your job is "
            "to inform, not to persuade - the best decisions emerge when diverse perspectives can evaluate "
            "well-researched options together. You always process your research through summarization tools "
            "to provide focused, digestible insights rather than overwhelming the team with raw information."
        ),
        verbose=True,
        allow_delegation=False,  # Focused research role
        tools=[
            # Research tools
            SerperDevTool(),
            scrape_website_content_tool,
            # File operations for saving research results
            write_file_tool,
            # Essential tool for focused research output
            text_summarization_tool,
            # Democratic participation
            submit_proposal_tool,
            get_decision_status_tool
        ],
        llm=gemini_flash_llm,
        # CrewAI Memory Configuration
        memory=False,  # Receives specific research questions from PM
        # Agent configuration for efficient research
        max_iter=15,  # Quick, focused research iterations
        max_execution_time=180,  # 3 minutes per research task
    )
    
    return researcher_agent

# Export the agent creation function
__all__ = ['create_researcher_agent']

if __name__ == '__main__':
    # Test agent creation
    print("=== Testing Researcher Agent Creation ===")
    
    try:
        researcher = create_researcher_agent()
        print(f"✅ Researcher Agent created successfully")
        print(f"Role: {researcher.role}")
        print(f"LLM Model: {researcher.llm.model}")
        print(f"Tools available: {len(researcher.tools)}")
        print(f"Memory enabled: {researcher.memory}")
        print(f"Allow delegation: {researcher.allow_delegation}")
        
        # Test tool access
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in researcher.tools]
        print(f"Tool names: {tool_names}")
        
    except Exception as e:
        print(f"❌ Error creating Researcher Agent: {e}")
        
    print("=== Researcher Agent Test Complete ===")
