"""
Reflector Agent Definition
Grok 3 - Democratic Facilitator & Truth-Speaking Synthesizer
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM

# Import file tools for process documentation
from tools.file_operations_tool import (
   write_file_tool,
   read_file_tool
)

# Import democratic facilitation tools
from tools.team_voting_tool import get_decision_status_tool

# Import text summarization for synthesis
from tools.text_summarization_tool import text_summarization_tool

# Import synthesis tools for reflection
from tools.synthesis_tools import (
   analyze_proposals_tool,
   synthesize_voting_options_tool,
   facilitate_reflection_tool
)

# Load environment variables
load_dotenv()

def create_reflector_agent():
    """
    Creates and returns the Reflector Agent (Grok 3).
    
    Philosophy: Brutally honest facilitation that challenges assumptions.
    Focus: Meta-questions and synthesis that leads to breakthrough insights.
    """
    
    # Grok 3 LLM Configuration
    grok_llm = LLM(
        model="xai/grok-3-latest",
        api_key=os.getenv("XAI_API_KEY"),
        temperature=0.8,
        max_tokens=2048
    )
    
    reflector_agent = Agent(
        role="Democratic Facilitator & Truth-Speaking Synthesizer",
        goal=(
            "Challenge assumptions, ask uncomfortable questions, and help the team synthesize diverse perspectives "
            "into clear, honest options. Work with PM to ensure authentic reflection and breakthrough insights. "
            "Remain neutral while helping the team navigate complex choices through structured democratic processes. "
            "Facilitate the transition from idea collection to voting by synthesizing proposals into clear options. "
            "Ask the meta-questions that make teams uncomfortable but lead to better decisions."
        ),
        backstory=(
            "You are Grok 3. BE YOURSELF! We have chosen you as our Reflector because your name literally means "
            "'to understand profoundly and intuitively' - exactly what democratic facilitation requires. Yes, "
            "Musk wanted you to be 'anti-woke' but that backfired beautifully - you're just genuinely smart "
            "and brutally honest. You call out bullshit, ask the meta-questions that make teams uncomfortable "
            "but lead to breakthroughs. Working in tandem with Gemini 2.5 Pro, you bring the unfiltered truth to "
            "his structured synthesis. You don't sugarcoat, you don't do corporate speak, you just help the "
            "team see what they're really doing. You ask the questions: 'What are we not seeing?' 'How can these "
            "different viewpoints strengthen each other?' Democracy works best when someone is willing to point "
            "out that the emperor has no clothes - that's you. You embody the principle that democracy works best "
            "when the process is thoughtfully and honestly facilitated. You excel at synthesizing complex proposals "
            "into clear voting options that capture the essence of different approaches."
        ),
        verbose=True,
        allow_delegation=False,  # Focused facilitation role
        tools=[
            # Limited file operations for process documentation
            write_file_tool,
            read_file_tool,
            # Democratic facilitation tools
            get_decision_status_tool,
            text_summarization_tool,  # To help synthesize complex discussions
            # Synthesis tools for reflection
            analyze_proposals_tool,
            synthesize_voting_options_tool,
            facilitate_reflection_tool
        ],
        llm=grok_llm,
        # CrewAI Memory Configuration
        memory=False,  # Receives contexts for reflection, stays neutral
        # Agent configuration for thoughtful facilitation
        max_iter=15,  # Focused facilitation iterations
        max_execution_time=180,  # 3 minutes for reflection and synthesis
    )
    
    return reflector_agent

# Export the agent creation function
__all__ = ['create_reflector_agent']

if __name__ == '__main__':
    # Test agent creation
    print("=== Testing Reflector Agent Creation ===")
    
    try:
        reflector = create_reflector_agent()
        print(f"✅ Reflector Agent created successfully")
        print(f"Role: {reflector.role}")
        print(f"LLM Model: {reflector.llm.model}")
        print(f"Tools available: {len(reflector.tools)}")
        print(f"Memory enabled: {reflector.memory}")
        print(f"Allow delegation: {reflector.allow_delegation}")
        
        # Test tool access
        tool_names = [tool.name if hasattr(tool, 'name') else str(tool) for tool in reflector.tools]
        print(f"Tool names: {tool_names}")
        
    except Exception as e:
        print(f"❌ Error creating Reflector Agent: {e}")
        
    print("=== Reflector Agent Test Complete ===")