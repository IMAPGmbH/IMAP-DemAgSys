"""
Phase 6: Styling Refinements & Final Polish
Modular implementation for the IMAP Democratic Agent System
"""
from typing import Dict, Any
from crewai import Task, Crew, Process


class Phase6Polish:
    """
    Phase 6: Styling Refinements & Final Polish
    
    Responsibilities:
    - Refine CSS styling and polish
    - Implement JavaScript for enhanced UX
    - Comprehensive testing across browsers/devices  
    - Final quality assurance and deployment prep
    - Create the final deliverable website
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self) -> Dict[str, Any]:
        """Execute Phase 6: Final Polish & Testing."""
        print("\n✨ === PHASE 6: FINAL POLISH & TESTING ===")
        print("Adding the final touches and ensuring everything works perfectly...")
        
        try:
            # Step 1: Refine CSS styling
            styling_result = self._refine_css_styling()
            
            # Step 2: Add JavaScript enhancements (if needed)
            js_result = self._implement_javascript_enhancements()
            
            # Step 3: Comprehensive testing
            testing_result = self._comprehensive_testing()
            
            # Step 4: Final quality check and deployment prep
            deployment_result = self._final_deployment_prep()
            
            # Update project metadata
            self.workflow_manager.project_metadata.update({
                "current_phase": 6,
                "phase_6_status": "complete",
                "styling_refined": styling_result["status"] == "success",
                "javascript_enhanced": js_result["status"] == "success", 
                "testing_complete": testing_result["status"] == "success",
                "deployment_ready": deployment_result["status"] == "success",
                "project_complete": True
            })
            self.workflow_manager._save_project_metadata()
            
            print("🎉 Phase 6 complete: Website is ready for the world!")
            
            return {
                "status": "success",
                "styling": styling_result,
                "javascript": js_result,
                "testing": testing_result,
                "deployment": deployment_result,
                "website_complete": True,
                "final_deliverable": self._create_final_deliverable_summary()
            }
            
        except Exception as e:
            print(f"❌ Phase 6 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _refine_css_styling(self) -> Dict[str, Any]:
        """Refine and polish CSS styling."""
        print("💅 Refining CSS styling and visual polish...")
        
        try:
            styling_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Refine and polish the CSS styling for final production quality.

YOUR TASK:
1. Polish CSS styling:
   - Refine typography scale and spacing
   - Perfect color usage and contrast
   - Smooth transitions and hover effects
   - Mobile responsiveness fine-tuning

2. Add finishing touches:
   - Subtle animations and micro-interactions
   - Focus states for accessibility
   - Loading optimizations

3. Code cleanup:
   - Remove unused CSS rules
   - Organize code structure
   - Add helpful comments

DEMOCRATIC SAFETY NET: If styling refinement fails 3 times,
Grok leads reflection on design philosophy and approach.

Update: src/css/style.css
""",
                expected_output="Production-ready CSS with polished styling and professional appearance",
                accessible_files=[str(self.project_structure.get("src", "") / "css" / "style.css")],
                focus_areas=["visual polish", "performance", "accessibility"],
                context_source="complete_website_structure"
            )
            
            result = self._execute_task_with_fallback(styling_task, "CSS Styling Refinement")
            return result
            
        except Exception as e:
            print(f"❌ CSS refinement failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _implement_javascript_enhancements(self) -> Dict[str, Any]:
        """Implement JavaScript enhancements for better UX."""
        print("⚡ Adding JavaScript enhancements...")
        
        try:
            js_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Implement JavaScript enhancements for improved user experience.

YOUR TASK:
1. Evaluate if JavaScript enhancements are needed for:
   - Mobile navigation (hamburger menu)
   - Smooth scrolling between sections
   - Interactive elements

2. If JavaScript is beneficial, implement:
   - Clean, performant JavaScript code
   - Progressive enhancement approach
   - Accessibility-friendly interactions

3. Performance considerations:
   - Minimal JavaScript footprint
   - No unnecessary dependencies

Create: src/js/script.js (if needed) and update HTML files
""",
                expected_output="JavaScript enhancements implemented or documented rationale for not needing them",
                accessible_files=[str(self.project_structure.get("src", ""))],
                focus_areas=["progressive enhancement", "performance", "simplicity"],
                context_source="complete_styled_website"
            )
            
            result = self._execute_task_with_fallback(js_task, "JavaScript Enhancement")
            return result
            
        except Exception as e:
            print(f"❌ JavaScript enhancement failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _comprehensive_testing(self) -> Dict[str, Any]:
        """Comprehensive testing across browsers and devices."""
        print("🧪 Running comprehensive testing...")
        
        try:
            testing_task = self.workflow_manager._create_atomic_task(
                agent_name="Tester",
                task_description="""
Perform comprehensive testing of the complete website.

YOUR TESTING RESPONSIBILITIES:
1. Functional Testing:
   - All navigation links work correctly
   - Page loading and rendering
   - Responsive design across screen sizes

2. Accessibility Testing:
   - WCAG 2.1 AA compliance check
   - Keyboard navigation
   - Color contrast verification

3. Performance Testing:
   - Page load speeds
   - CSS and JS optimization

4. Content Quality Assurance:
   - Spelling and grammar check
   - Content consistency
   - SEO basics (titles, descriptions)

Create comprehensive test report in: testing/final_test_report.md
""",
                expected_output="Complete test report with all issues identified and quality assessment",
                accessible_files=[str(self.project_structure.get("src", ""))],
                focus_areas=["quality assurance", "accessibility", "user experience"],
                context_source="complete_website_ready_for_testing"
            )
            
            result = self._execute_task_with_fallback(testing_task, "Comprehensive Testing")
            return result
            
        except Exception as e:
            print(f"❌ Comprehensive testing failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _final_deployment_prep(self) -> Dict[str, Any]:
        """Final deployment preparation and deliverable creation."""
        print("🚀 Preparing final deployment package...")
        
        try:
            deployment_task = self.workflow_manager._create_atomic_task(
                agent_name="Project Manager",
                task_description="""
Prepare the final deployment package and project deliverables.

YOUR FINAL DELIVERABLES:
1. Website Package:
   - Verify all files are in correct locations
   - Create deployment instructions
   - Create simple local server setup guide

2. Project Documentation:
   - Complete README.md for the website
   - Credit all AI agents and their contributions
   - Document the democratic decision-making process

3. Meta-Documentation:
   - Create summary of the IMAP system in action
   - Document what worked well vs. challenges

4. Quality Checklist:
   - Final file organization check
   - Documentation completeness

Create final deliverables in: deployment/ and docs/ directories
""",
                expected_output="Complete, deployment-ready website package with full documentation",
                accessible_files=[str(self.project_structure.get("src", ""))],
                focus_areas=["deployment readiness", "documentation", "project completion"],
                context_source="tested_website_ready_for_deployment"
            )
            
            result = self._execute_task_with_fallback(deployment_task, "Final Deployment Preparation")
            return result
            
        except Exception as e:
            print(f"❌ Deployment preparation failed: {e}")
            return {"status": "failed", "error": str(e)}
    
    def _create_final_deliverable_summary(self) -> Dict[str, Any]:
        """Create a summary of the final deliverable."""
        return {
            "website_location": str(self.project_structure.get("src", "")),
            "documentation_location": str(self.project_structure.get("docs", "")),
            "deployment_package": str(self.project_structure.get("deployment", "")),
            "project_structure": "Clean, organized IMAP structure",
            "agents_involved": list(self.agent_manager.agents.keys()),
            "ready_for_deployment": True,
            "ai_collaboration_demo": "Successfully demonstrates democratic AI workflow"
        }
    
    def _execute_task_with_fallback(self, task: Task, task_name: str, max_retries: int = 3) -> Dict[str, Any]:
        """Execute a task with democratic fallback."""
        print(f"🔄 Executing {task_name} (max {max_retries} attempts)")
        
        for attempt in range(max_retries):
            try:
                print(f"  Attempt {attempt + 1}/{max_retries}")
                
                # Choose appropriate agent
                if "Testing" in task_name:
                    agent = self.agent_manager.get_agent("Tester")
                elif "Project Manager" in str(task.description):
                    agent = self.agent_manager.get_agent("Project Manager")
                else:
                    agent = self.agent_manager.get_agent("Developer")
                
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=True
                )
                
                result = crew.kickoff()
                
                print(f"✅ {task_name} succeeded on attempt {attempt + 1}")
                return {
                    "status": "success",
                    "result": str(result),
                    "attempts": attempt + 1
                }
                
            except Exception as e:
                print(f"⚠️ {task_name} failed on attempt {attempt + 1}: {e}")
                
                if attempt == max_retries - 1:
                    print(f"🗳️ {task_name} failed {max_retries} times - FINAL DEMOCRATIC REFLECTION")
                    return self._trigger_final_reflection(task_name, str(e))
        
        return {"status": "failed", "error": f"{task_name} failed after {max_retries} attempts"}
    
    def _trigger_final_reflection(self, failed_task: str, error_details: str) -> Dict[str, Any]:
        """Trigger Grok's final democratic reflection."""
        print(f"\n🤔 === FINAL DEMOCRATIC REFLECTION ===")
        print(f"Failed Task: {failed_task}")
        
        try:
            from tools.team_voting_tool import trigger_democratic_decision_tool
            
            reflection_context = f"""
FINAL POLISH PHASE FAILURE:
Failed Task: {failed_task}
Error Details: {error_details}

QUESTIONS:
1. Should we ship the website as-is?
2. What is our definition of "done"?
3. Are we being too perfectionist?

GROK'S LEADERSHIP: Time for honest discussion about shipping vs. perfecting.
"""
            
            decision_id = trigger_democratic_decision_tool._run(
                conflict_type="performance_tradeoff",
                trigger_reason=f"Final task '{failed_task}' failed - ship vs. polish decision",
                context=reflection_context,
                participating_agents=self.agent_manager.get_participating_agents()
            )
            
            return {
                "status": "final_democratic_reflection",
                "reflection_decision_id": decision_id,
                "failed_task": failed_task,
                "next_action": "Democratic decision: Ship website as-is or continue"
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Could not trigger reflection: {e}",
                "fallback_action": "Ship website in current state"
            }