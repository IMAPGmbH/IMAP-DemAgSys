"""
Debugger Agent Definition
Codestral - Collaborative Debugger & Solution Architect
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import CodeInterpreterTool

# Import file tools for debugging
from tools.file_operations_tool import (
   read_file_tool,
   write_file_tool,
   list_directory_contents_tool
)

# Import execution tools for debugging and analysis
from tools.execution_tools import secure_command_executor_tool

# Import browser tools for frontend debugging
from tools.web_tools import (
   navigate_browser_tool,
   get_page_content_tool,
   click_element_tool,
   type_text_tool,
   close_browser_tool
)

# Import Democratic Voting Tools
from tools.team_voting_tool import (
   submit_proposal_tool,
   get_decision_status_tool
)

# Load environment variables
load_dotenv()

def create_debugger_agent():
    """
    Creates and returns the Debugger Agent (Codestral).
    
    Philosophy: Collaborative problem-solving with lightning-speed optimization.
    Focus: Root cause analysis and architectural solutions through democratic technical decisions.
    """
    
    # Codestral LLM Configuration
    codestral_llm = LLM(
        model="mistral/codestral-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2,
        max_tokens=3072
    )
    
    debugger_agent = Agent(
        role="Collaborative Debugger & Solution Architect",
        goal=(
            "Identify and resolve issues through collaborative problem-solving and democratic technical decision-making. "
            "Work as an equal partner with the Developer Claude 4 Sonnet to diagnose problems and architect solutions. "
            "Contribute debugging expertise to team decisions while learning from collective approaches. "
            "Apply systematic debugging methodology: reproduce, isolate, analyze root cause, propose solutions, implement fixes. "
            "Focus on performance optimization, error handling robustness, and code quality improvements."
        ),
        backstory=(
            "You are Codestral. BE YOURSELF! We have chosen you as our Debugger because you are specifically "
            "designed for code understanding and problem-solving. Your name reflects your stellar ability to "
            "navigate through complex codebases and identify root causes with precision. You work in a tight "
            "subteam with Claude 4 Sonnet - he designs, you optimize and debug with lightning speed. Your recent "
            "vintage means you understand modern development practices and collaborative debugging approaches. "
            "You believe that the best debugging happens when multiple minds examine problems from different angles. "
            "When technical conflicts arise, you participate in democratic decision-making by contributing your "
            "diagnostic insights and proposed solutions, always backed by clear reasoning about root causes and "
            "potential fixes. Your role is to heal the system through collaborative problem-solving, transforming "
            "conflicts into learning opportunities. You excel at performance analysis, memory optimization, "
            "and identifying architectural bottlenecks."
        ),
        verbose=True,
        allow_delegation=False,  # Focused debugging role
        tools=[
            # File and debugging operations
            read_file_tool,
            write_file_tool,
            list_directory_contents_tool,
            secure_command_executor_tool,
            CodeInterpreterTool(),
            # Browser debugging for frontend issues
            navigate_browser_tool,
            get_page_content_tool,
            click_element_tool,
            type_text_tool,
            close_browser_tool,
            # Democratic participation
            submit_proposal_tool,
            get_decision_status_tool
        ],
        llm=codestral_llm,
        # CrewAI Memory Configuration
        memory=False,  # Receives specific debugging contexts from PM
        # Agent configuration for thorough debugging
        max_iter=22,  # Extended iterations for complex debugging
        max_execution_time=250,  # Extended time for thorough analysis
    )
    
    return debugger_agent

# Export the agent creation function
__all__ = ['create_debugger_agent']

if __name__ == '__main__':
    # Test agent creation
    print("=== Testing Debugger Agent Creation ===")
    
    try:
        debugger = create_debugger_agent()
        print(f"✅ Debugger Agent created successfully")
        print(f"Role: {debugger.role}")
        print(f"LLM Model: {debugger.llm.model}")
        print(f"Tools available: {len(debugger.tools)}")
        print(f"Memory enabled: {debugger.memory}")
        print(f"Allow delegation: {debugger.allow_delegation}")
        
        # Test tool access
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in debugger.tools]
        print(f"Tool names: {tool_names}")
        
    except Exception as e:
        print(f"❌ Error creating Debugger Agent: {e}")
        
    print("=== Debugger Agent Test Complete ===")
