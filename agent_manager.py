"""
Agent Manager - Central orchestration for modular agents
Manages creation, configuration, and coordination of all IMAP Democratic Agents
"""
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Import modular agent creation functions
from agent_definitions.project_manager_agent import create_project_manager_agent
from agent_definitions.developer_agent import create_developer_agent
from agent_definitions.researcher_agent import create_researcher_agent
from agent_definitions.tester_agent import create_tester_agent
from agent_definitions.debugger_agent import create_debugger_agent
from agent_definitions.reflector_agent import create_reflector_agent

# Load environment variables
load_dotenv()

class AgentManager:
    """
    Central manager for the IMAP Democratic Agent System.
    Implements modular agent creation and team coordination.
    
    Philosophy: Buddhist Middle Way - Balance zwischen Gründlichkeit und Effizienz.
    """
    
    def __init__(self):
        self.agents = {}
        self.agent_registry = {
            "Project Manager": create_project_manager_agent,
            "Developer": create_developer_agent,
            "Researcher": create_researcher_agent,
            "Tester": create_tester_agent,
            "Debugger": create_debugger_agent,
            "Reflector": create_reflector_agent
        }
        
        # Validate environment setup
        self._validate_environment()
        
    def _validate_environment(self):
        """Validates that all required API keys are present."""
        required_keys = {
            "GEMINI_API_KEY": ["Project Manager", "Researcher"],
            "ANTHROPIC_API_KEY": ["Developer"],
            "MISTRAL_API_KEY": ["Tester", "Debugger"],
            "XAI_API_KEY": ["Reflector"]
        }
        
        missing_keys = []
        for key, agents in required_keys.items():
            if not os.getenv(key):
                missing_keys.append(f"{key} (needed for: {', '.join(agents)})")
        
        if missing_keys:
            print("⚠️ WARNING: Missing API keys:")
            for missing in missing_keys:
                print(f"  - {missing}")
            print("Some agents may not function properly.")
        else:
            print("✅ All required API keys are configured")
    
    def create_agent(self, agent_name: str):
        """Creates a specific agent by name."""
        if agent_name not in self.agent_registry:
            raise ValueError(f"Unknown agent: {agent_name}. Available: {list(self.agent_registry.keys())}")
        
        if agent_name in self.agents:
            print(f"Agent '{agent_name}' already exists, returning existing instance")
            return self.agents[agent_name]
        
        try:
            print(f"Creating agent: {agent_name}")
            agent = self.agent_registry[agent_name]()
            self.agents[agent_name] = agent
            print(f"✅ Agent '{agent_name}' created successfully")
            return agent
        except Exception as e:
            print(f"❌ Failed to create agent '{agent_name}': {e}")
            raise
    
    def create_all_agents(self):
        """Creates all agents in the system."""
        print("🤖 === Creating IMAP Democratic Agent System ===")
        
        for agent_name in self.agent_registry.keys():
            try:
                self.create_agent(agent_name)
            except Exception as e:
                print(f"⚠️ Warning: Could not create {agent_name}: {e}")
        
        print(f"\n✅ Agent creation complete. Created {len(self.agents)}/{len(self.agent_registry)} agents")
        return self.agents
    
    def get_agent(self, agent_name: str):
        """Gets an existing agent or creates it if it doesn't exist."""
        if agent_name not in self.agents:
            return self.create_agent(agent_name)
        return self.agents[agent_name]
    
    def get_participating_agents(self, exclude_roles: List[str] = None) -> List[str]:
        """Returns list of agent names that can participate in democratic decisions."""
        exclude_roles = exclude_roles or []
        return [name for name in self.agent_registry.keys() if name not in exclude_roles]
    
    def should_trigger_democracy(self, context: str) -> tuple[bool, str, str]:
        """
        Analyzes context to determine if a democratic decision should be triggered.
        Returns: (should_trigger, conflict_type, reason)
        """
        context_lower = context.lower()

        # Architecture decisions
        if any(keyword in context_lower for keyword in ['framework', 'library', 'architecture', 'database', 'api design']):
            return True, "architecture_decision", "Framework or architecture choice detected"

        # Performance vs features
        if any(keyword in context_lower for keyword in ['performance', 'optimization', 'speed', 'memory']) and \
           any(keyword in context_lower for keyword in ['feature', 'functionality', 'requirement']):
            return True, "performance_tradeoff", "Performance vs features trade-off detected"

        # UX/UI decisions
        if any(keyword in context_lower for keyword in ['ui', 'ux', 'design', 'interface', 'user experience', 'layout']):
            return True, "ux_ui_direction", "UX/UI design decision detected"

        # Agent disagreements (when multiple suggestions are present)
        if context_lower.count('suggest') > 1 or context_lower.count('recommend') > 1:
            return True, "agent_disagreement", "Multiple conflicting suggestions detected"

        return False, "", ""
    
    def get_agent_stats(self) -> Dict:
        """Returns statistics about the agent system."""
        stats = {
            "total_agents": len(self.agent_registry),
            "created_agents": len(self.agents),
            "agent_models": {},
            "democratic_tools_count": 0,
            "specialized_teams": {
                "PM-Reflector Tandem": ["Project Manager", "Reflector"],
                "Development Team": ["Developer", "Debugger"],
                "Quality Assurance": ["Tester"],
                "Research": ["Researcher"]
            }
        }
        
        for name, agent in self.agents.items():
            if hasattr(agent, 'llm') and hasattr(agent.llm, 'model'):
                stats["agent_models"][name] = agent.llm.model
            
            # Count democratic tools
            if hasattr(agent, 'tools'):
                democratic_tools = [tool for tool in agent.tools
                                 if hasattr(tool, 'name') and ('democratic' in tool.name.lower() or
                                    'proposal' in tool.name.lower() or 'decision' in tool.name.lower() or
                                    'synthesis' in tool.name.lower() or 'reflection' in tool.name.lower())]
                stats["democratic_tools_count"] += len(democratic_tools)
        
        return stats
    
    def print_system_overview(self):
        """Prints a comprehensive overview of the agent system."""
        print("\n🏛️ === IMAP DEMOCRATIC AGENT SYSTEM OVERVIEW ===")
        
        stats = self.get_agent_stats()
        
        print(f"\n📊 System Statistics:")
        print(f"  • Total Agents Defined: {stats['total_agents']}")
        print(f"  • Successfully Created: {stats['created_agents']}")
        print(f"  • Democratic Tools: {stats['democratic_tools_count']}")
        
        print(f"\n🤖 Agent Models:")
        for agent_name, model in stats["agent_models"].items():
            print(f"  • {agent_name}: {model}")
        
        print(f"\n👥 Specialized Teams:")
        for team_name, members in stats["specialized_teams"].items():
            available_members = [m for m in members if m in self.agents]
            print(f"  • {team_name}: {', '.join(available_members)}")
        
        print(f"\n🗳️ Democratic Participants: {', '.join(self.get_participating_agents())}")
        
        print(f"\n🧘 Philosophy: Buddhist Middle Way - Balance zwischen Gründlichkeit und Effizienz")
        print(f"🤝 Governance: Democratic Decision-Making with Ranked Choice Voting")
        print(f"⚡ Optimization: Need-to-Know Information Flow & Selective Context Management")

# Global instance for easy access
agent_manager = AgentManager()

# Convenience functions for backward compatibility
def get_democratic_agents():
    """Returns dictionary of all created agents."""
    return agent_manager.agents

def get_participating_agents(exclude_roles: List[str] = None) -> List[str]:
    """Returns list of agent names that can participate in democratic decisions."""
    return agent_manager.get_participating_agents(exclude_roles)

def should_trigger_democracy(context: str) -> tuple[bool, str, str]:
    """Analyzes context to determine if a democratic decision should be triggered."""
    return agent_manager.should_trigger_democracy(context)

if __name__ == '__main__':
    print("🚀 === IMAP DEMOCRATIC AGENT SYSTEM INITIALIZATION ===")
    
    # Initialize all agents
    agents = agent_manager.create_all_agents()
    
    # Print system overview
    agent_manager.print_system_overview()
    
    # Test agent access
    print(f"\n🧪 === TESTING AGENT ACCESS ===")
    try:
        pm = agent_manager.get_agent("Project Manager")
        dev = agent_manager.get_agent("Developer")
        print(f"✅ Successfully accessed Project Manager and Developer agents")
        print(f"   PM Tools: {len(pm.tools)}")
        print(f"   Dev Tools: {len(dev.tools)}")
    except Exception as e:
        print(f"❌ Error accessing agents: {e}")
    
    print(f"\n🎯 === READY FOR DEMOCRATIC COLLABORATION ===")
    print(f"Budget allocated: 100€ (enough for ~15-20 websites)")
    print(f"First project: Transform requirements into interactive website")
    print(f"Let's show what democratic AI collaboration can achieve! 🚀")
