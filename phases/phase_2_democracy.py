"""
Phase 2: Democratic Content & Structure Definition
Modular implementation for the IMAP Democratic Agent System
"""
from typing import Dict, Any, List
from crewai import Task, Crew, Process
from tools.team_voting_tool import trigger_democratic_decision_tool, get_decision_status_tool
from tools.file_operations_tool import write_file_tool


class Phase2Democracy:
    """
    Phase 2: Democratic Content & Structure Definition
    
    Responsibilities:
    - Trigger democratic decision for website content
    - Facilitate team collaboration on structure
    - Document finalized content decisions
    - Create sitemap and navigation structure
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self) -> Dict[str, Any]:
        """Execute Phase 2: Democratic Content & Structure Definition."""
        print("\n🗳️ === PHASE 2: DEMOCRATIC CONTENT & STRUCTURE DEFINITION ===")
        print("Let's democratically decide what website to build!")
        
        try:
            # Step 1: Trigger democratic decision
            decision_result = self._trigger_content_decision()
            
            if decision_result["status"] != "success":
                return decision_result
                
            decision_id = decision_result["decision_id"]
            
            # Step 2: Monitor decision process
            final_decision = self._monitor_decision_process(decision_id)
            
            if final_decision["status"] != "success":
                return final_decision
            
            # Step 3: Document sitemap and navigation
            sitemap_result = self._create_sitemap_and_navigation(final_decision["decision_details"])
            
            # Update project metadata
            self.workflow_manager.project_metadata.update({
                "current_phase": 2,
                "phase_2_status": "complete", 
                "democratic_decision_id": decision_id,
                "final_content_decision": final_decision["decision_details"],
                "sitemap_created": sitemap_result["status"] == "success"
            })
            self.workflow_manager._save_project_metadata()
            
            print("✅ Phase 2 complete: Democratic content decisions made")
            
            return {
                "status": "success",
                "decision_id": decision_id,
                "content_decision": final_decision["decision_details"],
                "sitemap": sitemap_result,
                "next_phase": 3
            }
            
        except Exception as e:
            print(f"❌ Phase 2 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _trigger_content_decision(self) -> Dict[str, Any]:
        """Trigger the democratic decision for website content."""
        print("🚀 Triggering democratic decision for website content...")
        
        # Get participating agents (exclude Reflector for initial proposal phase)
        participating_agents = self.agent_manager.get_participating_agents(exclude_roles=["Reflector"])
        
        context = """
We need to democratically decide on the website content and structure.

Based on the requirements analysis, we need to decide:
1. Overall theme/topic of the website (consider the "meta" documentation suggestion)
2. Number and titles of subpages (3-5 recommended)
3. Basic content outline for each subpage
4. Navigation structure

Design constraints:
- Dark theme with purple/magenta accents
- Poppins font (Regular for body, Semibold for headings)
- Simple, elegant design
- Should demonstrate our AI collaboration skills

Consider the meta-aspect: documenting our own creation process could be a compelling theme.
"""
        
        try:
            decision_id = trigger_democratic_decision_tool._run(
                conflict_type="architecture_decision",
                trigger_reason="Democratic content and structure definition for website",
                context=context,
                participating_agents=participating_agents
            )
            
            print(f"✅ Democratic decision triggered: {decision_id}")
            return {
                "status": "success",
                "decision_id": decision_id
            }
            
        except Exception as e:
            print(f"❌ Failed to trigger democratic decision: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _monitor_decision_process(self, decision_id: str, max_iterations: int = 10) -> Dict[str, Any]:
        """Monitor the democratic decision process until completion."""
        print(f"👥 Monitoring democratic decision process: {decision_id}")
        
        for iteration in range(max_iterations):
            try:
                status = get_decision_status_tool._run(decision_id=decision_id)
                print(f"📊 Decision status (iteration {iteration + 1}): {status}")
                
                # Parse status and check if decision is complete
                if "completed" in status.lower() or "final" in status.lower():
                    print("✅ Democratic decision completed!")
                    return {
                        "status": "success",
                        "decision_details": status
                    }
                elif "failed" in status.lower() or "error" in status.lower():
                    print("❌ Democratic decision failed")
                    return {
                        "status": "failed",
                        "error": f"Decision process failed: {status}"
                    }
                
                # Wait between checks (in real implementation, this would be handled by the voting system)
                print(f"⏳ Decision in progress... waiting for completion")
                
            except Exception as e:
                print(f"⚠️ Error checking decision status: {e}")
        
        print("⏰ Decision process timeout")
        return {
            "status": "timeout",
            "error": "Decision process did not complete within expected time"
        }
    
    def _create_sitemap_and_navigation(self, decision_details: str) -> Dict[str, Any]:
        """Create sitemap and navigation based on democratic decision."""
        print("📋 Creating sitemap and navigation structure...")
        
        try:
            # Create PM task to document the sitemap
            sitemap_task = self.workflow_manager._create_atomic_task(
                agent_name="Project Manager",
                task_description=f"""
Based on the democratic decision results, create a formal sitemap and navigation structure.

DEMOCRATIC DECISION RESULTS:
{decision_details}

YOUR TASK:
1. Parse the democratic decision to extract:
   - Website theme/topic
   - Number and titles of subpages  
   - Basic content outline for each page
   - Navigation structure

2. Create a formal sitemap document with:
   - Page hierarchy
   - URL structure (e.g., index.html, about.html, etc.)
   - Navigation menu structure
   - Content outlines for each page

3. Save the sitemap in: management/planning/sitemap_and_navigation.md

Format the document clearly for use by the development and content teams.
""",
                expected_output="Complete sitemap and navigation structure saved in management/planning/sitemap_and_navigation.md",
                accessible_files=[],
                focus_areas=["sitemap creation", "navigation structure", "content organization"],
                context_source="democratic_decision_results"
            )
            
            # Execute sitemap creation
            sitemap_crew = Crew(
                agents=[self.agent_manager.get_agent("Project Manager")],
                tasks=[sitemap_task],
                process=Process.sequential,
                verbose=True
            )
            
            sitemap_result = sitemap_crew.kickoff()
            
            print("✅ Sitemap and navigation structure created")
            return {
                "status": "success",
                "result": str(sitemap_result)
            }
            
        except Exception as e:
            print(f"❌ Failed to create sitemap: {e}")
            return {
                "status": "failed", 
                "error": str(e)
            }