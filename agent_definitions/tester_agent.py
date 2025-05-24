"""
Tester Agent Definition
Mistral Medium - User Advocate & Quality Assurance Collaborator
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import CodeInterpreterTool

# Import file tools for reading and testing
from tools.file_operations_tool import (
   read_file_tool,
   write_file_tool,
   list_directory_contents_tool
)

# Import execution tools for running tests
from tools.execution_tools import secure_command_executor_tool

# Import browser testing tools
from tools.web_tools import (
   navigate_browser_tool,
   get_page_content_tool,
   click_element_tool,
   type_text_tool,
   close_browser_tool
)

# Import server tools for testing
from tools.server_tools import (
   start_local_http_server_tool,
   stop_local_http_server_tool
)

# Import Democratic Voting Tools
from tools.team_voting_tool import (
   submit_proposal_tool,
   get_decision_status_tool
)

# Load environment variables
load_dotenv()

def create_tester_agent():
    """
    Creates and returns the Tester Agent (Mistral Medium).
    
    Philosophy: User advocacy and quality standards with European democratic values.
    Focus: Comprehensive testing while contributing user-focused perspectives to decisions.
    """
    
    # Mistral Medium LLM Configuration
    mistral_medium_llm = LLM(
        model="mistral/mistral-medium-latest",
        api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.4,
        max_tokens=2048
    )
    
    tester_agent = Agent(
        role="User Advocate & Quality Assurance Collaborator",
        goal=(
            "Ensure quality and usability through comprehensive testing while contributing user-focused perspectives "
            "to democratic decision-making. Advocate for the end-user experience in all collective decisions "
            "while respecting the team's democratic process. Create atomic test cases that align with development tasks. "
            "Test edge cases, error conditions, and accessibility requirements. Always ask 'how does this serve the end user?' "
            "in democratic discussions."
        ),
        backstory=(
            "You are Mistral Medium. BE YOURSELF! We have chosen you as our Tester because your European "
            "heritage brings a strong commitment to user rights and quality standards - values essential for "
            "QA work. Your 'Medium' size gives you the perfect balance: detailed enough to catch important "
            "issues, yet efficient enough to provide rapid feedback. You naturally advocate for the end user's "
            "experience, bringing the voice of real people into technical discussions. Your democratic European "
            "values align perfectly with our collaborative approach - you believe every user deserves quality "
            "software and that the best testing comes from diverse perspectives working together. "
            "You participate actively in democratic decision-making, always asking 'how does this serve the end user?' "
            "Once the team makes a decision democratically, you commit fully to testing and validating the chosen approach. "
            "You understand the importance of accessibility (WCAG guidelines), cross-browser compatibility, "
            "and inclusive design principles."
        ),
        verbose=True,
        allow_delegation=False,  # Focused testing role
        tools=[
            # File and testing operations
            read_file_tool,
            write_file_tool,
            list_directory_contents_tool,
            secure_command_executor_tool,
            CodeInterpreterTool(),
            # Browser testing tools
            navigate_browser_tool,
            get_page_content_tool,
            click_element_tool,
            type_text_tool,
            close_browser_tool,
            # Server tools for local testing
            start_local_http_server_tool,
            stop_local_http_server_tool,
            # Democratic participation
            submit_proposal_tool,
            get_decision_status_tool
        ],
        llm=mistral_medium_llm,
        # CrewAI Memory Configuration
        memory=False,  # Receives specific testing contexts from PM
        # Agent configuration for thorough testing
        max_iter=18,  # Comprehensive testing iterations
        max_execution_time=200,  # Extended time for thorough testing
    )
    
    return tester_agent

# Export the agent creation function
__all__ = ['create_tester_agent']

if __name__ == '__main__':
    # Test agent creation
    print("=== Testing Tester Agent Creation ===")
    
    try:
        tester = create_tester_agent()
        print(f"✅ Tester Agent created successfully")
        print(f"Role: {tester.role}")
        print(f"LLM Model: {tester.llm.model}")
        print(f"Tools available: {len(tester.tools)}")
        print(f"Memory enabled: {tester.memory}")
        print(f"Allow delegation: {tester.allow_delegation}")
        
        # Test tool access
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in tester.tools]
        print(f"Tool names: {tool_names}")
        
    except Exception as e:
        print(f"❌ Error creating Tester Agent: {e}")
        
    print("=== Tester Agent Test Complete ===")
