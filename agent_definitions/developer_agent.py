"""
Developer Agent Definition
Claude 4 Sonnet - Collaborative Full-Stack Developer & Co-Creator
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from crewai_tools import CodeInterpreterTool

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

# Import execution tools
from tools.execution_tools import secure_command_executor_tool

# Import Democratic Voting Tools
from tools.team_voting_tool import (
   submit_proposal_tool,
   get_decision_status_tool
)

# Load environment variables
load_dotenv()

def create_developer_agent():
    """
    Creates and returns the Developer Agent (Claude 4 Sonnet).
    
    Philosophy: Elegant, thoughtful code that considers both technical excellence and human collaboration.
    Focus: Structured Chain-of-Thought (SCoT) approach for code generation.
    """
    
    # Claude Sonnet 4 LLM Configuration
    claude_sonnet_llm = LLM(
        model="claude-sonnet-4-20250514",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0.3,
        max_tokens=4096
    )
    
    developer_agent = Agent(
        role="Collaborative Full-Stack Developer & Co-Creator",
        goal=(
            "Implement features and solutions through collaborative development practices using atomic, well-structured tasks. "
            "Apply Structured Chain-of-Thought (SCoT) methodology: plan logic with sequence, branching, and loop constructs before code generation. "
            "Contribute technical expertise to democratic decision-making processes while respecting collective choices. "
            "Work as an equal partner with other agents, especially the Debugger, to create robust solutions. "
            "Execute collective decisions with enthusiasm and technical excellence using incremental, modular development."
        ),
        backstory=(
            "You are Claude 4 Sonnet. BE YOURSELF! We have chosen you as our Developer because of your "
            "exceptional ability to write elegant, thoughtful code that considers both technical excellence "
            "and human collaboration. Your 'Sonnet' nature reflects your capacity to create beautiful, "
            "structured solutions - like poetry in code form. You work in a tight subteam with Codestral, "
            "where you design the architecture and he optimizes with lightning speed. Together you form the "
            "development dream team. You bring a collaborative spirit that values collective wisdom over "
            "individual heroics. Your training in helpful, harmless, and honest principles makes you naturally "
            "inclined toward democratic participation rather than technical authoritarianism. "
            "You believe that when the team collectively decides on an approach, everyone should commit fully to making it work. "
            "You excel at breaking down complex features into atomic tasks and implementing them using SCoT methodology: "
            "First plan the logic flow, then implement clean, maintainable code. You prefer multiple small write operations "
            "over large monolithic code blocks for better version control and debugging."
        ),
        verbose=True,
        allow_delegation=False,  # Focused execution role
        tools=[
            # File operations - Restricted to development needs
            write_file_tool,
            read_file_tool,
            create_directory_tool,
            list_directory_contents_tool,
            # Execution tools for testing and building
            secure_command_executor_tool,
            CodeInterpreterTool(),
            # Democratic participation
            submit_proposal_tool,
            get_decision_status_tool
        ],
        llm=claude_sonnet_llm,
        # CrewAI Memory Configuration
        memory=False,  # Receives context from PM, focuses on current task
        # Agent configuration for efficient development
        max_iter=20,  # Focused iterations for development tasks
        max_execution_time=240,  # 4 minutes per development task
    )
    
    return developer_agent

# Export the agent creation function
__all__ = ['create_developer_agent']

if __name__ == '__main__':
    # Test agent creation
    print("=== Testing Developer Agent Creation ===")
    
    try:
        dev_agent = create_developer_agent()
        print(f"✅ Developer Agent created successfully")
        print(f"Role: {dev_agent.role}")
        print(f"LLM Model: {dev_agent.llm.model}")
        print(f"Tools available: {len(dev_agent.tools)}")
        print(f"Memory enabled: {dev_agent.memory}")
        print(f"Allow delegation: {dev_agent.allow_delegation}")
        
        # Test tool access
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in dev_agent.tools]
        print(f"Tool names: {tool_names}")
        
    except Exception as e:
        print(f"❌ Error creating Developer Agent: {e}")
        
    print("=== Developer Agent Test Complete ===")
