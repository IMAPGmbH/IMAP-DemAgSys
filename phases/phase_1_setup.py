"""
Phase 1: Project Setup & Requirements Analysis (FIXED VERSION)
Gemini-freundliche Task-Aufteilung - 5 Mini-Tasks statt 1 Monster-Task
"""
from typing import Dict, Any
from pathlib import Path
from crewai import Task, Crew, Process
from tools.file_operations_tool import write_file_tool


class Phase1Setup:
    """
    Phase 1: Project Setup & Requirements Analysis (GEMINI-OPTIMIZED)
    
    Philosophy: Buddhist Middle Way - thorough analysis in efficient, digestible tasks
    
    Responsibilities (aufgeteilt in 5 separate Tasks):
    1. Analyze user requirements → requirements_analysis.md
    2. Create atomic task breakdown → atomic_task_breakdown.md  
    3. Generate research questions → research_questions.md
    4. Set up access policies → files_access.json
    5. Create context strategy → context_strategy.md
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self, user_requirements: str) -> Dict[str, Any]:
        """Execute Phase 1 with Gemini-friendly task splitting."""
        print("\n🎯 === PHASE 1: PROJECT SETUP (GEMINI-OPTIMIZED) ===")
        print(f"Project: {self.workflow_manager.project_name}")
        print(f"Strategy: 5 Mini-Tasks instead of 1 Monster-Task")
        print("🤖 Gemini will work in digestible chunks!")
        
        try:
            # Save user requirements first
            requirements_file = self.project_structure["requirements"] / "user_requirements.md"
            write_file_tool._run(str(requirements_file), user_requirements)
            
            # Execute 5 separate mini-tasks
            task_results = {}
            
            # Task 1: Requirements Analysis
            print("\n📋 Task 1/5: Requirements Analysis...")
            task_results["requirements"] = self._execute_requirements_analysis(user_requirements)
            
            # Task 2: Atomic Task Breakdown  
            print("\n🔨 Task 2/5: Atomic Task Breakdown...")
            task_results["atomic_tasks"] = self._execute_atomic_task_breakdown()
            
            # Task 3: Research Questions
            print("\n❓ Task 3/5: Research Questions...")
            task_results["research"] = self._execute_research_questions()
            
            # Task 4: Access Policies
            print("\n🔐 Task 4/5: Access Policies...")
            task_results["access"] = self._execute_access_policies()
            
            # Task 5: Context Strategy
            print("\n🧠 Task 5/5: Context Strategy...")
            task_results["context"] = self._execute_context_strategy()
            
            # Check if all tasks succeeded
            all_success = all(result.get("status") == "success" for result in task_results.values())
            
            if all_success:
                # Update project metadata
                self.workflow_manager.project_metadata.update({
                    "current_phase": 1,
                    "phase_1_status": "complete",
                    "phase_1_strategy": "gemini_friendly_task_splitting",
                    "tasks_completed": list(task_results.keys()),
                    "structure_utilized": True
                })
                self.workflow_manager._save_project_metadata()
                
                print("✅ Phase 1 complete: All 5 mini-tasks successful!")
                
                return {
                    "status": "success",
                    "strategy": "gemini_friendly_splitting", 
                    "task_results": task_results,
                    "next_phase": 2
                }
            else:
                failed_tasks = [task for task, result in task_results.items() 
                              if result.get("status") != "success"]
                print(f"❌ Phase 1 failed: Tasks {failed_tasks} unsuccessful")
                
                return {
                    "status": "partial_failure",
                    "failed_tasks": failed_tasks,
                    "task_results": task_results,
                    "next_phase": None
                }
            
        except Exception as e:
            print(f"❌ Phase 1 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _execute_requirements_analysis(self, user_requirements: str) -> Dict[str, Any]:
        """Task 1: Create requirements analysis document."""
        try:
            task = Task(
                description=f"""
Analyze the user requirements and create a structured requirements analysis document.

USER REQUIREMENTS:
{user_requirements}

YOUR TASK:
Create a comprehensive requirements analysis covering:
1. Project Overview
2. Design Specifications  
3. Functional Requirements
4. Content Strategy
5. Constraints & Assumptions

Save the analysis in: management/requirements/requirements_analysis.md

Follow Buddhist Middle Way: thorough analysis, efficient execution.
Keep it focused and structured. No need to return the full content - just confirm completion.
""",
                expected_output="Confirmation that requirements_analysis.md has been created with structured analysis",
                agent=self.agent_manager.get_agent("Project Manager")
            )
            
            crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            print("✅ Requirements analysis created")
            
            return {"status": "success", "result": str(result)}
            
        except Exception as e:
            print(f"❌ Requirements analysis failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _execute_atomic_task_breakdown(self) -> Dict[str, Any]:
        """Task 2: Create atomic task breakdown."""
        try:
            task = Task(
                description="""
Create a detailed atomic task breakdown for the website project.

INPUT: Read management/requirements/requirements_analysis.md for context

YOUR TASK:
Create atomic_task_breakdown.md with:
- Phase 0: Project Setup
- Phase 1: Content & Structure Definition  
- Phase 2: Design & Prototyping
- Phase 3: Frontend Development
- Phase 4: Content Generation & Integration
- Phase 5: Testing & Quality Assurance
- Phase 6: Deployment & Documentation

For each task specify: scope, required agents, dependencies, outputs, file access.

Save in: management/planning/atomic_task_breakdown.md
""",
                expected_output="Confirmation that atomic_task_breakdown.md has been created",
                agent=self.agent_manager.get_agent("Project Manager")
            )
            
            crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[task], 
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            print("✅ Atomic task breakdown created")
            
            return {"status": "success", "result": str(result)}
            
        except Exception as e:
            print(f"❌ Atomic task breakdown failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _execute_research_questions(self) -> Dict[str, Any]:
        """Task 3: Generate research questions."""
        try:
            task = Task(
                description="""
Generate research questions that may need to be addressed during the project.

YOUR TASK:
Create research_questions.md covering:
- Design & UX questions
- Technical Implementation questions  
- Content & Collaboration questions
- Deployment questions
- Project Management & Process questions

Save in: management/planning/research_questions.md
""",
                expected_output="Confirmation that research_questions.md has been created",
                agent=self.agent_manager.get_agent("Project Manager")
            )
            
            crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            print("✅ Research questions created")
            
            return {"status": "success", "result": str(result)}
            
        except Exception as e:
            print(f"❌ Research questions failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _execute_access_policies(self) -> Dict[str, Any]:
        """Task 4: Set up file access policies."""
        try:
            task = Task(
                description="""
Update the file access policies for all agents in the project.

YOUR TASK:
Update management/access_policies/files_access.json with:
- Agent role definitions
- Read/write permissions for each directory
- Access rules for specific file types
- General notes about permission refinement

Define access for: ProjectManager, DesignerAgent, DeveloperAgent, ContentAgent, QAAgent
""",
                expected_output="Confirmation that files_access.json has been updated",
                agent=self.agent_manager.get_agent("Project Manager")
            )
            
            crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            print("✅ Access policies updated")
            
            return {"status": "success", "result": str(result)}
            
        except Exception as e:
            print(f"❌ Access policies failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _execute_context_strategy(self) -> Dict[str, Any]:
        """Task 5: Create context strategy."""
        try:
            task = Task(
                description="""
Create the context strategy document for selective information management.

YOUR TASK:
Create context_strategy.md covering:
1. Guiding Principles (Need-to-Know)
2. Context Construction Techniques
3. Context Sources
4. Democratic Decision Context
5. Role of Agents in Context Management
6. Iteration and Refinement

Save in: management/contexts/context_strategy.md
""",
                expected_output="Confirmation that context_strategy.md has been created",
                agent=self.agent_manager.get_agent("Project Manager")
            )
            
            crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            print("✅ Context strategy created")
            
            return {"status": "success", "result": str(result)}
            
        except Exception as e:
            print(f"❌ Context strategy failed: {e}")
            return {"status": "failed", "error": str(e)}
