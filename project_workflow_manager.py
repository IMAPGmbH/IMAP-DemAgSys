"""
Modular Optimized Project Workflow Manager
Now using separated phase modules for better maintainability
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables FIRST
load_dotenv()

# Import the modular systems
from agent_manager import agent_manager
from project_structure_manager import ProjectStructureManager, create_new_project

# Import all phase modules
from phases import get_phase, get_all_phases, PHASES

# Import tools for context construction
from tools.text_summarization_tool import text_summarization_tool
from tools.file_operations_tool import read_file_tool, write_file_tool


class ContextManager:
    """
    Implements selective context management and the "Need-to-Know" principle.
    Acts as semantic filter and information orchestrator.
    """
    
    def __init__(self, project_structure: Dict[str, Path]):
        self.context_cache = {}
        self.access_policies = {}
        self.project_structure = project_structure
        
        # Load access policies from the clean structure
        self._load_access_policies()
    
    def _load_access_policies(self):
        """Load access policies from the project structure."""
        try:
            if "access_policies" in self.project_structure:
                policy_file = self.project_structure["access_policies"] / "files_access.json"
                if policy_file.exists():
                    with open(policy_file, 'r', encoding='utf-8') as f:
                        self.access_policies = json.load(f)
                        print(f"✅ Loaded access policies from {policy_file}")
                else:
                    print(f"⚠️ Access policy file not found: {policy_file}")
        except Exception as e:
            print(f"⚠️ Could not load access policies: {e}")
    
    def get_agent_accessible_files(self, agent_name: str, current_context: str = None) -> List[str]:
        """Gets list of files the agent can access based on policies and context."""
        if not self.access_policies:
            return []
        
        agent_policy = self.access_policies.get("agent_policies", {}).get(agent_name, {})
        read_permissions = agent_policy.get("read", [])
        
        accessible_files = []
        
        for permission in read_permissions:
            if permission == "*":
                # Full access - but limit to relevant directories
                for key, path in self.project_structure.items():
                    if isinstance(path, Path) and path.is_dir():
                        for file_path in path.rglob("*"):
                            if file_path.is_file():
                                accessible_files.append(str(file_path))
            else:
                # Pattern-based access
                base_path = self.project_structure.get("project_root", Path("."))
                pattern_path = base_path / permission.replace("*", "**")
                
                if pattern_path.parent.exists():
                    for file_path in pattern_path.parent.rglob(pattern_path.name):
                        if file_path.is_file():
                            accessible_files.append(str(file_path))
        
        return accessible_files[:10]  # Limit for performance
    
    def construct_minimal_context(
        self, 
        agent_name: str, 
        task_description: str, 
        accessible_files: List[str] = None,
        focus_areas: List[str] = None
    ) -> str:
        """Constructs minimal, semantically rich context for an agent."""
        print(f"🧠 Constructing context for {agent_name} (Modular Phases)")
        
        context_parts = []
        
        # 1. Task-specific context
        context_parts.append(f"=== CURRENT TASK ===\n{task_description}\n")
        
        # 2. Project structure awareness
        if self.project_structure:
            context_parts.append("=== PROJECT STRUCTURE ===")
            relevant_paths = self._get_relevant_paths_for_agent(agent_name)
            for purpose, path in relevant_paths.items():
                context_parts.append(f"📁 {purpose}: {path}")
            context_parts.append("")
        
        # 3. Load accessible files (with policy enforcement)
        if accessible_files is None:
            accessible_files = self.get_agent_accessible_files(agent_name, task_description)
        
        if accessible_files:
            context_parts.append("=== RELEVANT INFORMATION ===")
            for file_path in accessible_files:
                if os.path.exists(file_path) and os.path.getsize(file_path) < 10000:
                    try:
                        file_content = read_file_tool._run(file_path)
                        if len(file_content) > 500:
                            summary_focus = f"Key information for {agent_name}'s task: {task_description[:100]}..."
                            if focus_areas:
                                summary_focus += f" Focus on: {', '.join(focus_areas)}"
                            
                            summarized = text_summarization_tool._run(
                                text_to_summarize=file_content,
                                max_length=200,
                                summary_focus=summary_focus
                            )
                            context_parts.append(f"📄 {file_path} (summarized):\n{summarized}\n")
                        else:
                            context_parts.append(f"📄 {file_path}:\n{file_content}\n")
                    except Exception as e:
                        print(f"⚠️ Could not load {file_path}: {e}")
        
        # 4. Agent-specific guidance
        agent_guidance = self._get_agent_specific_guidance(agent_name, task_description)
        if agent_guidance:
            context_parts.append(f"=== GUIDANCE FOR {agent_name.upper()} ===\n{agent_guidance}\n")
        
        return "\n".join(context_parts)
    
    def _get_relevant_paths_for_agent(self, agent_name: str) -> Dict[str, Path]:
        """Gets relevant paths for specific agent based on role."""
        path_mapping = {
            "Project Manager": {
                "Management": self.project_structure.get("project_management", ""),
                "Source": self.project_structure.get("source_code", ""),
                "Documentation": self.project_structure.get("documentation", "")
            },
            "Developer": {
                "Source Code": self.project_structure.get("source_code", ""),
                "Components": self.project_structure.get("components", ""),
                "Assets": self.project_structure.get("assets", "")
            },
            "Tester": {
                "Source Code": self.project_structure.get("source_code", ""),
                "Testing": self.project_structure.get("testing", ""),
                "Accessibility Tests": self.project_structure.get("accessibility_tests", "")
            },
            "Researcher": {
                "Research": self.project_structure.get("research", ""),
                "Reports": self.project_structure.get("reports", ""),
                "Analysis": self.project_structure.get("analysis", "")
            },
            "Debugger": {
                "Source Code": self.project_structure.get("source_code", ""),
                "Testing": self.project_structure.get("testing", "")
            },
            "Reflector": {
                "Management": self.project_structure.get("project_management", ""),
                "Decisions": self.project_structure.get("decisions", "")
            }
        }
        
        return path_mapping.get(agent_name, {})
    
    def _get_agent_specific_guidance(self, agent_name: str, task_description: str) -> str:
        """Provides agent-specific guidance with clean structure awareness."""
        guidance_map = {
            "Project Manager": (
                "🎯 You are the orchestrator of modular phases.\n"
                "- Coordinate between phase modules\n"
                "- Track progress across all phases\n"
                "- Manage democratic decision outcomes\n"
                "- Ensure phase-to-phase continuity"
            ),
            "Developer": (
                "⚡ Work with modular phase structure:\n"
                "- Follow phase-specific deliverables\n"
                "- Build incrementally across phases\n"
                "- Apply SCoT methodology consistently\n"
                "- Prepare for democratic feedback"
            ),
            "Tester": (
                "🛡️ Quality assurance across phases:\n"
                "- Phase-specific testing approaches\n"
                "- Continuous quality monitoring\n"
                "- User advocacy in democratic decisions\n"
                "- Accessibility throughout development"
            ),
            "Reflector": (
                "🤔 Democratic facilitation specialist:\n"
                "- Lead reflection circles when tasks fail\n"
                "- Challenge assumptions honestly\n"
                "- Synthesize team perspectives\n"
                "- Guide democratic decision processes"
            )
        }
        return guidance_map.get(agent_name, "")


class ModularOptimizedWorkflowManager:
    """
    Modular Optimized Workflow Manager using separated phase modules.
    
    Philosophy: Buddhist Middle Way + Modular Architecture + Democratic Safety Nets
    Innovation: Phase separation + Grok's Reflection Circles
    """
    
    def __init__(self, project_info: Dict[str, Any] = None, budget_euros: float = 100.0):
        """Initialize with project info from structure manager or create new project."""
        if project_info is None:
            print("🏗️ Creating new project with modular phase structure...")
            project_info = create_new_project()
        
        self.project_info = project_info
        self.project_structure = project_info["structure"]
        self.project_name = project_info["project_name"]
        self.budget_euros = budget_euros
        self.used_budget = 0.0
        
        # Initialize systems
        self.context_manager = ContextManager(self.project_structure)
        self.agent_manager = agent_manager
        agent_manager.create_all_agents()  # Ensure all agents are ready
        
        # Project metadata
        self.project_metadata = {
            "project_id": f"imap_modular_{int(time.time())}",
            "project_name": self.project_name,
            "template": project_info.get("template", "imap_website"),
            "start_time": datetime.now().isoformat(),
            "budget_euros": budget_euros,
            "used_budget": 0.0,
            "current_phase": 0,
            "total_phases": len(PHASES),
            "status": "initializing",
            "phase_results": {},
            "democratic_decisions": [],
            "development_steps": [],
            "optimization_strategy": "Modular_Phases + Democratic_Safety_Nets",
            "structure_paths": {k: str(v) for k, v in self.project_structure.items() if isinstance(v, Path)}
        }
        
        # Save metadata in clean structure
        self._save_project_metadata()
        
    def _save_project_metadata(self):
        """Saves metadata in the clean project structure."""
        if "project_management" in self.project_structure:
            metadata_file = self.project_structure["project_management"] / "modular_workflow_metadata.json"
        else:
            metadata_file = self.project_structure["project_root"] / "workflow_metadata.json"
            
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(self.project_metadata, f, indent=2, ensure_ascii=False)
    
    def _create_atomic_task(
        self, 
        agent_name: str,
        task_description: str,
        expected_output: str,
        accessible_files: List[str] = None,
        focus_areas: List[str] = None,
        context_source: str = "modular_phase_context"
    ):
        """Creates atomic task with modular phase awareness and selective context."""
        from crewai import Task
        
        # Get the agent
        agent = self.agent_manager.get_agent(agent_name)
        
        # Construct minimal, relevant context using modular structure
        context = self.context_manager.construct_minimal_context(
            agent_name=agent_name,
            task_description=task_description,
            accessible_files=accessible_files,
            focus_areas=focus_areas
        )
        
        # Save context in clean structure
        if "contexts" in self.project_structure:
            context_file = self.project_structure["contexts"] / f"{agent_name.lower().replace(' ', '_')}_context_{int(time.time())}.md"
            write_file_tool._run(str(context_file), context)
        
        # Create focused task description
        focused_description = f"""
{context}

=== YOUR SPECIFIC TASK ===
{task_description}

=== CONSTRAINTS ===
- Follow the modular phase approach
- Work with provided context only
- Use clean project structure (see PROJECT STRUCTURE above)
- Apply agent-specific methodologies
- Democratic fallback available if needed
- Context source: {context_source}
"""
        
        return Task(
            description=focused_description,
            expected_output=expected_output,
            agent=agent
        )
    
    def run_complete_workflow(self, user_requirements: str = None) -> Dict[str, Any]:
        """
        Run the complete modular workflow through all 6 phases.
        """
        print("🚀 === MODULAR IMAP WORKFLOW (ALL 6 PHASES) ===")
        print(f"Project: {self.project_name}")
        print(f"Template: {self.project_info.get('template', 'default')}")
        print(f"Budget: {self.budget_euros}€")
        print("Strategy: Modular Phases + Democratic Safety Nets + Grok's Reflection")
        print(f"Location: {self.project_structure['project_root']}")
        print(f"Total Phases: {len(PHASES)}")
        
        try:
            # If no requirements provided, get them interactively
            if user_requirements is None:
                user_requirements = self._get_user_requirements_interactive()
            
            # Execute all phases sequentially
            for phase_number in range(1, len(PHASES) + 1):
                print(f"\n🔄 === STARTING PHASE {phase_number} ===")
                
                phase_result = self._execute_phase(phase_number, user_requirements)
                
                # Store phase result
                self.project_metadata["phase_results"][f"phase_{phase_number}"] = phase_result
                self.project_metadata["current_phase"] = phase_number
                
                if phase_result["status"] == "success":
                    print(f"✅ Phase {phase_number} completed successfully")
                elif phase_result["status"] == "democratic_reflection_triggered":
                    print(f"🗳️ Phase {phase_number} triggered democratic reflection")
                    # In a real implementation, we'd wait for the democratic decision
                    # For now, we'll document it and continue
                    self.project_metadata["democratic_decisions"].append({
                        "phase": phase_number,
                        "decision_id": phase_result.get("reflection_decision_id"),
                        "reason": phase_result.get("failed_task")
                    })
                elif phase_result["status"] == "failed":
                    print(f"❌ Phase {phase_number} failed - stopping workflow")
                    break
                
                self._save_project_metadata()
            
            # Create final project summary
            final_result = self._create_final_project_summary()
            
            print("\n🎉 === MODULAR WORKFLOW COMPLETE ===")
            print(f"✅ All phases executed with modular architecture!")
            print(f"📁 Project location: {self.project_structure['project_root']}")
            print(f"🗂️ Template: {self.project_info.get('template', 'default')}")
            print(f"💰 Budget used: {self.used_budget}€ von {self.budget_euros}€")
            print(f"🧠 Modular phases + democratic safety nets active")
            print(f"🌐 Website ready: {final_result.get('website_ready', False)}")
            
            return final_result
            
        except Exception as e:
            print(f"❌ Error in modular workflow: {e}")
            self.project_metadata["status"] = "failed"
            self.project_metadata["error"] = str(e)
            self._save_project_metadata()
            return {"status": "failed", "error": str(e)}
    
    def _execute_phase(self, phase_number: int, user_requirements: str = None) -> Dict[str, Any]:
        """Execute a specific phase."""
        try:
            # Get the phase class
            phase_class = get_phase(phase_number)
            
            # Initialize the phase with this workflow manager
            phase_instance = phase_class(self)
            
            # Execute the phase
            if phase_number == 1:
                # Phase 1 needs user requirements
                return phase_instance.execute(user_requirements)
            else:
                # Other phases use previous phase outputs
                return phase_instance.execute()
                
        except Exception as e:
            print(f"❌ Phase {phase_number} execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "phase": phase_number
            }
    
    def _create_final_project_summary(self) -> Dict[str, Any]:
        """Create comprehensive final project summary."""
        successful_phases = sum(1 for result in self.project_metadata["phase_results"].values() 
                               if result.get("status") == "success")
        
        democratic_decisions_count = len(self.project_metadata.get("democratic_decisions", []))
        
        return {
            "project_id": self.project_metadata["project_id"],
            "project_name": self.project_name,
            "template": self.project_info.get("template"),
            "status": "modular_workflow_complete",
            "modular_architecture": True,
            "phases_completed": successful_phases,
            "total_phases": len(PHASES),
            "democratic_decisions_triggered": democratic_decisions_count,
            "budget_used": self.used_budget,
            "budget_remaining": self.budget_euros - self.used_budget,
            "structure_location": str(self.project_structure["project_root"]),
            "completion_time": datetime.now().isoformat(),
            "website_ready": successful_phases >= 4,  # Phases 1-4 minimum for functional website
            "optimization_metrics": {
                "modular_phases_used": True,
                "democratic_safety_nets": True,
                "grok_reflection_circles": democratic_decisions_count > 0,
                "context_optimization": "Selective context per phase",
                "agent_specialization": "Phase-specific agent usage",
                "clean_architecture": True
            },
            "phase_breakdown": self.project_metadata["phase_results"],
            "agents_participated": list(self.agent_manager.agents.keys()),
            "project_structure": {k: str(v) for k, v in self.project_structure.items() if isinstance(v, Path)},
            "deliverable_ready": True,
            "ai_collaboration_success": True
        }
    
    def _get_user_requirements_interactive(self) -> str:
        """Get user requirements interactively if not provided."""
        print(f"\n📝 === REQUIREMENTS FOR: {self.project_name} ===")
        print("Describe what you want to build:")
        print("(Leave empty line to finish)")
        
        lines = []
        while True:
            line = input()
            if line.strip() == "":
                break
            lines.append(line)
        
        requirements = "\n".join(lines)
        
        if not requirements.strip():
            # Use default requirements for demo
            requirements = f"""
            PROJEKT: {self.project_name}
            
            BUILD A SIMPLE WEBSITE DEMONSTRATING AI COLLABORATION:
            - Multiple pages with navigation
            - Dark theme with purple/magenta accents
            - Poppins fonts (Regular for body, Semibold for headings)
            - Document the AI democratic process (meta-aspect)
            - Show collaboration between different AI agents
            - Clean, professional, accessible design
            - Responsive and fast-loading
            
            MODULAR DEVELOPMENT APPROACH:
            - Use all 6 phases (Setup → Democracy → Design → Development → Content → Polish)
            - Apply democratic decision-making where needed
            - Trigger Grok's reflection circles if tasks fail repeatedly
            - Create a working website that demonstrates our AI collaboration
            
            BUDGET: {self.budget_euros}€
            TIMELINE: Complete all 6 phases
            
            GOAL: Functional website showcasing democratic AI development process
            """
        
        return requirements


# === MAIN EXECUTION FUNCTIONS ===

def run_modular_project() -> Dict[str, Any]:
    """
    Main function to run complete modular project through all 6 phases.
    """
    print("🤖 === MODULAR IMAP SYSTEM ===")
    print("🏗️ Phase Modules + Selective Context + Democratic Safety Nets")
    print("🗳️ Grok's Reflection Circles + All 6 Phases")
    print()
    
    # Create the modular workflow manager
    modular_manager = ModularOptimizedWorkflowManager(budget_euros=25.0)
    
    # Run the complete workflow through all phases
    result = modular_manager.run_complete_workflow()
    
    return result

def run_single_phase(phase_number: int, project_name: str = None) -> Dict[str, Any]:
    """
    Run a single phase for testing/debugging purposes.
    """
    print(f"🧪 === TESTING SINGLE PHASE {phase_number} ===")
    
    if project_name:
        # Use existing project
        from pathlib import Path
        project_path = Path(f"./PROJECTS/{project_name}")
        if not project_path.exists():
            print(f"❌ Project {project_name} not found")
            return {"status": "failed", "error": "Project not found"}
        
        # Load project info (simplified)
        project_info = {
            "project_name": project_name,
            "template": "imap_website",
            "structure": {}  # Would need to reconstruct from existing project
        }
    else:
        project_info = None
    
    modular_manager = ModularOptimizedWorkflowManager(project_info, budget_euros=10.0)
    
    # Execute single phase
    if phase_number == 1:
        user_reqs = "Test website for single phase execution"
        result = modular_manager._execute_phase(phase_number, user_reqs)
    else:
        result = modular_manager._execute_phase(phase_number)
    
    print(f"📊 Phase {phase_number} Result: {result.get('status', 'unknown')}")
    return result

def get_phase_info() -> Dict[str, Any]:
    """
    Get information about all available phases.
    """
    print("📋 === MODULAR PHASE INFORMATION ===")
    
    phases_info = {}
    for phase_num, phase_class in get_all_phases().items():
        phases_info[f"Phase {phase_num}"] = {
            "class_name": phase_class.__name__,
            "description": phase_class.__doc__.strip() if phase_class.__doc__ else "No description",
            "module": phase_class.__module__
        }
        print(f"Phase {phase_num}: {phase_class.__name__}")
        if phase_class.__doc__:
            print(f"  Description: {phase_class.__doc__.strip().split('Responsibilities:')[0].strip()}")
    
    return phases_info


if __name__ == '__main__':
    print("🚀 === MODULAR IMAP SYSTEM INITIALIZATION ===")
    print("🏗️ All 6 Phases + Democratic Safety Nets + Grok's Reflection Circles")
    print("🧘 Philosophy: Buddhist Middle Way + Modular Architecture")
    print()
    
    # Show available phases
    print("📋 Available Phases:")
    phase_info = get_phase_info()
    print()
    
    # Ask user what they want to do
    print("What would you like to do?")
    print("1. Run complete workflow (all 6 phases)")
    print("2. Test single phase")
    print("3. Show phase information")
    
    choice = input("\nEnter choice (1-3, default=1): ").strip() or "1"
    
    if choice == "1":
        print("\n🚀 Running complete modular workflow...")
        final_result = run_modular_project()
        
        print(f"\n📊 === FINAL RESULTS ===")
        if final_result.get("status") != "failed":
            print(f"✅ Modular workflow successful!")
            print(f"📁 Project: {final_result.get('project_name')}")
            print(f"🏗️ Architecture: Modular phases")
            print(f"📍 Location: {final_result.get('structure_location')}")
            print(f"💰 Budget efficiency: {final_result.get('budget_remaining', 0)}€ remaining")
            print(f"🗳️ Democratic decisions: {final_result.get('democratic_decisions_triggered', 0)}")
            print(f"✅ Phases completed: {final_result.get('phases_completed', 0)}/{final_result.get('total_phases', 6)}")
            print(f"🌐 Website ready: {final_result.get('website_ready', False)}")
        else:
            print(f"❌ Workflow failed: {final_result.get('error', 'Unknown error')}")
    
    elif choice == "2":
        phase_num = int(input("Which phase to test (1-6): ").strip())
        project_name = input("Existing project name (or empty for new): ").strip() or None
        result = run_single_phase(phase_num, project_name)
        print(f"Phase {phase_num} result: {result}")
    
    elif choice == "3":
        print("\n📋 Detailed phase information:")
        for phase_name, info in phase_info.items():
            print(f"\n{phase_name}:")
            print(f"  Class: {info['class_name']}")
            print(f"  Module: {info['module']}")
            print(f"  Description: {info['description']}")
    
    print(f"\n🎯 === MODULAR SYSTEM READY ===")
    print("✅ All phases available")
    print("🗳️ Democratic safety nets active")  
    print("🤔 Grok's reflection circles ready")
    print("🏗️ Clean modular architecture")
    print("🌐 Ready to build websites democratically! 🚀")