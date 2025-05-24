"""
Integrated Optimized Project Workflow Manager
Now using modular project structure management for clean organization
"""
import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from dotenv import load_dotenv
from crewai import Task, Crew, Process

# Load environment variables FIRST
load_dotenv()

# Import the new modular systems
from agent_manager import agent_manager
from project_structure_manager import ProjectStructureManager, create_new_project

# Import tools for context construction
from tools.text_summarization_tool import text_summarization_tool
from tools.file_operations_tool import read_file_tool, write_file_tool, create_directory_tool

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
        """
        Gets list of files the agent can access based on policies and context.
        """
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
        """
        Constructs minimal, semantically rich context for an agent.
        Now uses clean project structure for better organization.
        """
        print(f"🧠 Constructing context for {agent_name} (Clean Structure)")
        
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
                if os.path.exists(file_path) and os.path.getsize(file_path) < 10000:  # Limit file size
                    try:
                        file_content = read_file_tool._run(file_path)
                        if len(file_content) > 500:  # Summarize long content
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
                "🎯 You are the central orchestrator with clean project structure.\n"
                "- Use management/ directory for all planning artifacts\n"
                "- Save contexts in management/contexts/ for other agents\n"
                "- Store decisions in management/decisions/\n"
                "- Coordinate file access via access policies\n"
                "- Follow Buddhist Middle Way: thorough but efficient"
            ),
            "Developer": (
                "⚡ Work in the organized src/ structure:\n"
                "- HTML files → src/html/\n"
                "- CSS files → src/css/\n"
                "- JavaScript → src/js/\n"
                "- Components → src/components/\n"
                "- Apply SCoT methodology with clean file organization"
            ),
            "Researcher": (
                "🔍 Use the research/ directory structure:\n"
                "- Reports → research/reports/\n"
                "- Analysis → research/analysis/\n"
                "- Competitive research → research/competitive_analysis/\n"
                "- Always summarize findings for other agents"
            ),
            "Tester": (
                "🛡️ Organize tests in testing/ structure:\n"
                "- Accessibility → testing/accessibility/\n"
                "- Performance → testing/performance/\n"
                "- Browser tests → testing/browser/\n"
                "- Unit tests → testing/unit/\n"
                "- Always test from user perspective"
            ),
            "Debugger": (
                "🔧 Focus on code quality in src/:\n"
                "- Review all src/ subdirectories\n"
                "- Document fixes in testing/ results\n"
                "- Work with Developer on optimization\n"
                "- Follow systematic debugging approach"
            ),
            "Reflector": (
                "🤔 Democratic facilitation with structure awareness:\n"
                "- Use management/decisions/ for decision tracking\n"
                "- Synthesize proposals from all agents\n"
                "- Challenge assumptions honestly\n"
                "- Work with PM for structured synthesis"
            )
        }
        return guidance_map.get(agent_name, "")

class IntegratedOptimizedWorkflowManager:
    """
    Integrated Optimized Workflow Manager using clean project structure.
    
    Philosophy: Buddhist Middle Way + Clean Organization
    Innovation: Modular structure + PM as Scratchpad-Orchestrator
    """
    
    def __init__(self, project_info: Dict[str, Any] = None, budget_euros: float = 100.0):
        """
        Initialize with project info from structure manager or create new project.
        """
        if project_info is None:
            print("🏗️ Creating new project with clean structure...")
            project_info = create_new_project()
        
        self.project_info = project_info
        self.project_structure = project_info["structure"]
        self.project_name = project_info["project_name"]
        self.budget_euros = budget_euros
        self.used_budget = 0.0
        
        # Initialize systems
        self.context_manager = ContextManager(self.project_structure)
        agent_manager.create_all_agents()  # Ensure all agents are ready
        
        # Project metadata
        self.project_metadata = {
            "project_id": f"imap_integrated_{int(time.time())}",
            "project_name": self.project_name,
            "template": project_info.get("template", "imap_website"),
            "start_time": datetime.now().isoformat(),
            "budget_euros": budget_euros,
            "used_budget": 0.0,
            "current_step": 0,
            "total_steps": 0,
            "status": "initializing",
            "decisions_made": [],
            "development_steps": [],
            "optimization_strategy": "Clean_Structure + Need_to_Know",
            "structure_paths": {k: str(v) for k, v in self.project_structure.items() if isinstance(v, Path)}
        }
        
        # Save metadata in clean structure
        self._save_project_metadata()
        
    def _save_project_metadata(self):
        """Saves metadata in the clean project structure."""
        if "project_management" in self.project_structure:
            metadata_file = self.project_structure["project_management"] / "integrated_workflow_metadata.json"
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
        context_source: str = "pm_constructed"
    ) -> Task:
        """
        Creates atomic task with clean structure awareness and selective context.
        """
        # Get the agent
        agent = agent_manager.get_agent(agent_name)
        
        # Construct minimal, relevant context using clean structure
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
- Follow the "Need-to-Know" principle
- Work with provided context only
- Use clean project structure (see PROJECT STRUCTURE above)
- Apply agent-specific methodologies
- Context source: {context_source}
"""
        
        return Task(
            description=focused_description,
            expected_output=expected_output,
            agent=agent
        )
    
    def phase_1_pm_requirements_analysis(self, user_requirements: str) -> Dict[str, Any]:
        """
        Phase 1: PM analyzes requirements using clean project structure.
        """
        print("\n🎯 === PHASE 1: PM REQUIREMENTS ANALYSIS (CLEAN STRUCTURE) ===")
        print(f"Project: {self.project_name}")
        print(f"Structure: {self.project_info.get('template', 'default')}")
        print(f"Budget: {self.budget_euros}€ | Used: {self.used_budget}€")
        
        # Save user requirements in clean structure
        requirements_file = self.project_structure["requirements"] / "user_requirements.md"
        write_file_tool._run(str(requirements_file), user_requirements)
        
        # PM task with clean structure awareness
        pm_analysis_task = self._create_atomic_task(
            agent_name="Project Manager",
            task_description=f"""
As the Project Manager, analyze requirements and create atomic task breakdown using the clean project structure.

USER REQUIREMENTS:
{user_requirements}

YOUR RESPONSIBILITIES (using clean structure):
1. REQUIREMENTS_ANALYSIS → Save in management/requirements/
2. ATOMIC_TASK_BREAKDOWN → Save in management/planning/
3. RESEARCH_QUESTIONS → Save in management/planning/research_questions.md
4. ACCESS_MATRIX → Update management/access_policies/files_access.json
5. CONTEXT_STRATEGY → Save in management/contexts/context_strategy.md

For each atomic task, specify:
- Exact scope and deliverables
- Required agent(s) and their structure paths
- Input dependencies from clean structure
- Expected output format and location
- File access permissions

Use the clean project structure effectively:
- Source code → src/ subdirectories
- Management → management/ subdirectories  
- Research → research/ subdirectories
- Testing → testing/ subdirectories

Follow Buddhist Middle Way: thorough analysis, efficient execution.
""",
            expected_output=(
                "Complete project analysis with atomic task breakdown saved in clean structure directories. "
                "Include task sequence, agent assignments, and updated file access matrix."
            ),
            accessible_files=[str(requirements_file)],
            focus_areas=["atomic task creation", "clean structure usage", "selective context planning"],
            context_source="pm_full_orchestration_clean_structure"
        )
        
        # Execute PM analysis
        pm_crew = Crew(
            agents=[agent_manager.get_agent("Project Manager")],
            tasks=[pm_analysis_task],
            process=Process.sequential,
            verbose=True,
            memory=True  # PM needs memory for orchestration
        )
        
        analysis_result = pm_crew.kickoff()
        
        # Update project metadata
        self.project_metadata["status"] = "requirements_analyzed_clean"
        self.project_metadata["pm_analysis_complete"] = True
        self.project_metadata["structure_utilized"] = True
        self._save_project_metadata()
        
        print("✅ Phase 1 complete: PM analyzed requirements using clean structure")
        return {"status": "success", "result": str(analysis_result), "structure_used": True}
    
    def run_integrated_workflow(self, user_requirements: str = None) -> Dict[str, Any]:
        """
        Runs the complete integrated workflow with clean structure and selective context.
        """
        print("🚀 === INTEGRATED IMAP WORKFLOW (CLEAN + OPTIMIZED) ===")
        print(f"Project: {self.project_name}")
        print(f"Template: {self.project_info.get('template', 'default')}")
        print(f"Budget: {self.budget_euros}€")
        print("Strategy: Clean Structure + Selective Context + Need-to-Know")
        print(f"Location: {self.project_structure['project_root']}")
        
        try:
            # If no requirements provided, get them interactively
            if user_requirements is None:
                user_requirements = self._get_user_requirements_interactive()
            
            # Phase 1: PM Requirements Analysis with Clean Structure
            phase1_result = self.phase_1_pm_requirements_analysis(user_requirements)
            
            # Additional phases would follow the same pattern...
            # For now, demonstrate the integrated approach
            
            # Final project summary
            final_result = {
                "project_id": self.project_metadata["project_id"],
                "project_name": self.project_name,
                "template": self.project_info.get("template"),
                "status": "phase_1_complete_integrated",
                "clean_structure": True,
                "optimization_strategy": "Clean Structure + Need-to-Know + Selective Context",
                "budget_used": self.used_budget,
                "budget_remaining": self.budget_euros - self.used_budget,
                "structure_location": str(self.project_structure["project_root"]),
                "completion_time": datetime.now().isoformat(),
                "efficiency_metrics": {
                    "clean_structure_used": True,
                    "context_files_created": len(list(self.project_structure.get("contexts", Path()).glob("*.md"))) if "contexts" in self.project_structure else 0,
                    "selective_contexts_used": True,
                    "memory_optimization": "Implemented with clean structure",
                    "token_usage": "Optimized via Need-to-Know + Clean Organization"
                },
                "phase_results": {
                    "phase_1": phase1_result
                },
                "project_structure": {k: str(v) for k, v in self.project_structure.items() if isinstance(v, Path)}
            }
            
            self.project_metadata.update(final_result)
            self._save_project_metadata()
            
            print("\n🎉 === INTEGRATED WORKFLOW PHASE 1 COMPLETE ===")
            print(f"✅ Clean project structure successfully utilized!")
            print(f"📁 Project location: {self.project_structure['project_root']}")
            print(f"🗂️ Template: {self.project_info.get('template', 'default')}")
            print(f"💰 Budget used: {self.used_budget}€ von {self.budget_euros}€")
            print(f"🧠 Clean structure + optimization active")
            
            return final_result
            
        except Exception as e:
            print(f"❌ Error in integrated workflow: {e}")
            self.project_metadata["status"] = "failed"
            self.project_metadata["error"] = str(e)
            self._save_project_metadata()
            return {"status": "failed", "error": str(e)}
    
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
            
            REQUIREMENTS:
            - Interactive web application
            - Modern, responsive design
            - User-friendly interface
            - Fast performance
            - Accessibility compliance (WCAG 2.1)
            - Clean, maintainable code
            
            BUDGET: {self.budget_euros}€
            TIMELINE: 1-2 days
            
            SPECIAL REQUIREMENTS:
            - Use clean project structure
            - Apply IMAP optimization principles
            - Implement selective context management
            """
        
        return requirements

# === MAIN EXECUTION FUNCTIONS ===

def run_integrated_project() -> Dict[str, Any]:
    """
    Main function to run integrated project with clean structure.
    """
    print("🤖 === INTEGRATED IMAP SYSTEM ===")
    print("🏗️ Clean Structure + Selective Context + Democratic Agents")
    print()
    
    # The project structure is created automatically by IntegratedOptimizedWorkflowManager
    # when no project_info is provided
    
    integrated_manager = IntegratedOptimizedWorkflowManager(budget_euros=15.0)
    result = integrated_manager.run_integrated_workflow()
    
    return result

if __name__ == '__main__':
    print("🚀 === INTEGRATED OPTIMIZED IMAP SYSTEM ===")
    print("🏗️ Modular Structure + Selective Context + Democratic Collaboration")
    print("🧘 Philosophy: Buddhist Middle Way + Clean Organization")
    print()
    
    # Run the integrated system
    final_result = run_integrated_project()
    
    print(f"\n📊 === INTEGRATION RESULTS ===")
    if final_result.get("status") != "failed":
        print(f"✅ Integration successful!")
        print(f"📁 Project: {final_result.get('project_name')}")
        print(f"🗂️ Template: {final_result.get('template')}")
        print(f"📍 Location: {final_result.get('structure_location')}")
        print(f"💰 Budget efficiency: {final_result.get('budget_remaining', 0)}€ remaining")
        print(f"🧠 Clean structure: {final_result.get('clean_structure', False)}")
    else:
        print(f"❌ Integration failed: {final_result.get('error', 'Unknown error')}")
    
    print(f"\n🎯 === READY FOR CLEAN, OPTIMIZED DEVELOPMENT ===")