"""
Phase 1: Project Setup & Requirements Analysis
Modular implementation for the IMAP Democratic Agent System
"""
from typing import Dict, Any
from pathlib import Path
from crewai import Task, Crew, Process
from tools.file_operations_tool import write_file_tool


class Phase1Setup:
    """
    Phase 1: Project Setup & Requirements Analysis
    
    Responsibilities:
    - Analyze user requirements 
    - Create project structure
    - Generate atomic task breakdown
    - Set up access policies
    - Create context strategy
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self, user_requirements: str) -> Dict[str, Any]:
        """Execute Phase 1: Project Setup & Requirements Analysis."""
        print("\n🎯 === PHASE 1: PROJECT SETUP & REQUIREMENTS ANALYSIS ===")
        print(f"Project: {self.workflow_manager.project_name}")
        print(f"Structure: {self.workflow_manager.project_info.get('template', 'default')}")
        print(f"Budget: {self.workflow_manager.budget_euros}€")
        
        try:
            # Save user requirements in clean structure
            requirements_file = self.project_structure["requirements"] / "user_requirements.md"
            write_file_tool._run(str(requirements_file), user_requirements)
            
            # Create PM analysis task
            pm_analysis_task = self._create_pm_analysis_task(user_requirements)
            
            # Execute PM analysis
            pm_crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[pm_analysis_task],
                process=Process.sequential,
                verbose=True,
                memory=True
            )
            
            analysis_result = pm_crew.kickoff()
            
            # Update project metadata
            self.workflow_manager.project_metadata.update({
                "current_phase": 1,
                "phase_1_status": "complete",
                "phase_1_result": str(analysis_result),
                "structure_utilized": True
            })
            self.workflow_manager._save_project_metadata()
            
            print("✅ Phase 1 complete: Project setup and requirements analysis done")
            
            return {
                "status": "success", 
                "result": str(analysis_result),
                "structure_used": True,
                "next_phase": 2
            }
            
        except Exception as e:
            print(f"❌ Phase 1 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _create_pm_analysis_task(self, user_requirements: str) -> Task:
        """Create the PM analysis task with clean structure awareness."""
        return self.workflow_manager._create_atomic_task(
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
            accessible_files=[str(self.project_structure["requirements"] / "user_requirements.md")],
            focus_areas=["atomic task creation", "clean structure usage", "selective context planning"],
            context_source="pm_full_orchestration_clean_structure"
        )