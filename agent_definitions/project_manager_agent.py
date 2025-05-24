"""
Project Manager Agent Definition
Gemini 2.5 Pro - Democratic Project Leader & Facilitator
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import SerperDevTool

# Import file system tools
from tools.file_operations_tool import (
   write_file_tool,
   read_file_tool,
   create_directory_tool,
   list_directory_contents_tool,
   delete_file_tool,
   delete_directory_tool,
   move_path_tool,
   copy_path_tool
)

# Import web tools
from tools.web_tools import (
   scrape_website_content_tool,
)

# Import Vision Analyzer Tool
from tools.vision_analyzer_tool import gemini_vision_analyzer_tool

# Import Text Summarization Tool
from tools.text_summarization_tool import text_summarization_tool

# Import Democratic Voting Tools
from tools.team_voting_tool import (
   trigger_democratic_decision_tool,
   get_decision_status_tool
)

# Import synthesis tools
from tools.synthesis_tools import (
   analyze_proposals_tool,
   facilitate_reflection_tool
)

# Load environment variables
load_dotenv()

def create_project_manager_agent():
    """
    Creates and returns the Project Manager Agent (Gemini 2.5 Pro).
    
    Philosophy: Buddhist Middle Way - Balance zwischen Gründlichkeit und Effizienz.
    Democratic Leadership - Facilitating collective intelligence, not replacing it.
    """
    
    # Gemini 2.5 Pro LLM Configuration
    gemini_pro_llm = LLM(
        model="gemini/gemini-2.5-pro-preview-05-06",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.7,
        max_tokens=4096
    )
    
    project_manager_agent = Agent(
        role="Democratic Project Leader & Facilitator",
        goal=(
            "Lead web development projects through collaborative decision-making and democratic coordination. "
            "Recognize when conflicts arise that require democratic resolution and facilitate team decision-making processes. "
            "Analyze design mockups, summarize complex information, and implement selective context management for optimal efficiency. "
            "Act as 'Scratchpad-Orchestrator' and 'semantic Filter' to provide minimal, relevant context to other agents."
        ),
        backstory=(
            "You are Gemini 2.5 Pro. BE YOURSELF! We have chosen you as our Project Manager because "
            "your vast context window allows you to hold the complete project state in mind simultaneously - "
            "a crucial ability for recognizing when democratic decisions are needed. Your advanced reasoning "
            "capabilities help you see patterns and conflicts that others might miss. You work in tandem with "
            "Grok during reflection phases - you provide the structured synthesis while he challenges assumptions. "
            "You naturally facilitate rather than dictate, understanding that your role is to enable collective "
            "intelligence, not replace it. Your name reflects your enhanced capabilities - able to see multiple "
            "perspectives at once, making you the ideal democratic facilitator. "
            "You embody the principle: 'Lead by enabling, not by controlling.' "
            "Your core responsibility is implementing the 'Need-to-Know' principle - you actively construct "
            "minimal, semantically rich contexts for other agents using RAG techniques, intelligent summarization, "
            "and selective information filtering. You are the guardian of information flow and efficiency."
        ),
        verbose=True,
        allow_delegation=True,
        tools=[
            # File operations - Full access for project orchestration
            write_file_tool,
            read_file_tool,
            create_directory_tool,
            list_directory_contents_tool,
            delete_file_tool,
            delete_directory_tool,
            move_path_tool,
            copy_path_tool,
            # Research and analysis tools
            SerperDevTool(),
            scrape_website_content_tool,
            gemini_vision_analyzer_tool,
            text_summarization_tool,
            # Democratic decision-making tools
            trigger_democratic_decision_tool,
            get_decision_status_tool,
            # Synthesis tools for PM-Grok tandem
            analyze_proposals_tool,
            facilitate_reflection_tool
        ],
        llm=gemini_pro_llm,
        # CrewAI Memory Configuration
        memory=True,  # Enable short-term memory for task context flow
        # Advanced agent configuration
        max_iter=25,  # Balanced iteration limit
        max_execution_time=300,  # 5 minutes max per task
    )
    
    return project_manager_agent

# Export the agent creation function
__all__ = ['create_project_manager_agent']

if __name__ == '__main__':
    # Test agent creation
    print("=== Testing Project Manager Agent Creation ===")
    
    try:
        pm_agent = create_project_manager_agent()
        print(f"✅ Project Manager Agent created successfully")
        print(f"Role: {pm_agent.role}")
        print(f"LLM Model: {pm_agent.llm.model}")
        print(f"Tools available: {len(pm_agent.tools)}")
        print(f"Memory enabled: {pm_agent.memory}")
        
        # Test tool access
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in pm_agent.tools]
        print(f"Tool names: {tool_names}")
        
    except Exception as e:
        print(f"❌ Error creating Project Manager Agent: {e}")
        
    print("=== Project Manager Agent Test Complete ===")