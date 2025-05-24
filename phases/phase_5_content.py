"""
Phase 5: Content Creation & Integration
Modular implementation for the IMAP Democratic Agent System
"""
from typing import Dict, Any
from crewai import Task, Crew, Process


class Phase5Content:
    """
    Phase 5: Content Creation & Integration
    
    Responsibilities:
    - Generate content for each subpage
    - Integrate content into HTML pages
    - Apply democratic content decisions
    - Ensure consistent voice and quality
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self) -> Dict[str, Any]:
        """Execute Phase 5: Content Creation & Integration."""
        print("\n✍️ === PHASE 5: CONTENT CREATION & INTEGRATION ===")
        print("Bringing our website to life with compelling content...")
        
        try:
            # Step 1: Generate content for each subpage
            content_result = self._generate_subpage_content()
            
            # Step 2: Integrate content into HTML pages
            integration_result = self._integrate_content_into_html()
            
            # Update project metadata
            self.workflow_manager.project_metadata.update({
                "current_phase": 5,
                "phase_5_status": "complete",
                "content_generated": content_result["status"] == "success",
                "content_integrated": integration_result["status"] == "success"
            })
            self.workflow_manager._save_project_metadata()
            
            print("✅ Phase 5 complete: Content created and integrated")
            
            return {
                "status": "success",
                "content_generation": content_result,
                "content_integration": integration_result,
                "next_phase": 6
            }
            
        except Exception as e:
            print(f"❌ Phase 5 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _generate_subpage_content(self) -> Dict[str, Any]:
        """Generate content for each subpage based on democratic decisions."""
        print("📝 Generating content for all subpages...")
        
        try:
            content_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",  # Claude as content-focused developer
                task_description="""
Generate compelling content for each subpage based on the democratic decisions.

INPUT DEPENDENCIES:
- management/planning/sitemap_and_navigation.md (for page structure)
- Phase 2 democratic decision results (content themes)
- research/design/color_palette.md (for tone consistency)

YOUR TASK:
1. Based on the sitemap and democratic decisions, create content for each page:
   - Engaging, well-written copy
   - Consistent voice and tone
   - Appropriate length for each page
   - SEO-friendly headings and structure

2. Consider the meta-documentation aspect:
   - If democratically decided, include documentation of our creation process
   - Show collaboration between AI agents
   - Demonstrate the democratic decision-making process

3. Create content files for each page:
   - Save as markdown files in docs/content/
   - Include proper heading hierarchy
   - Add placeholder text for any missing elements

4. Ensure content aligns with:
   - Dark, elegant design theme
   - Professional but approachable tone
   - Technical demonstration without being overwhelming

DEMOCRATIC SAFETY NET: If content creation fails 3 times, 
Grok will lead a reflection circle on content strategy.

Save content files in: docs/content/ (e.g., homepage_content.md, about_content.md)
""",
                expected_output="Complete content for all pages saved as markdown files ready for HTML integration",
                accessible_files=[
                    str(self.project_structure.get("planning", "") / "sitemap_and_navigation.md"),
                    str(self.project_structure.get("research", "") / "design" / "color_palette.md")
                ],
                focus_areas=["content strategy", "voice and tone", "meta-documentation"],
                context_source="democratic_decisions_and_sitemap"
            )
            
            # Execute with democratic fallback
            result = self._execute_with_democratic_fallback(
                task=content_task,
                task_name="Content Generation",
                max_retries=3
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Content generation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _integrate_content_into_html(self) -> Dict[str, Any]:
        """Integrate the generated content into HTML pages."""
        print("🔗 Integrating content into HTML pages...")
        
        try:
            integration_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Integrate the generated content into the HTML pages.

INPUT DEPENDENCIES:
- docs/content/*.md (all content files)
- src/*.html (all HTML page files)
- src/css/style.css (for styling consistency)

YOUR TASK:
1. For each content file, integrate it into the corresponding HTML page:
   - Convert markdown content to proper HTML
   - Maintain semantic HTML structure
   - Apply appropriate CSS classes
   - Ensure proper heading hierarchy

2. Update all HTML files with:
   - Real content replacing placeholders
   - Proper meta descriptions based on content
   - Updated page titles
   - Internal linking between pages

3. Quality checks:
   - All links work correctly
   - Content fits the design properly
   - No broken layouts or overflow issues
   - Consistent formatting across pages

4. Test all pages for:
   - Content readability
   - Responsive behavior
   - Navigation functionality

DEMOCRATIC SAFETY NET: If integration fails 3 times,
Grok leads reflection on technical implementation approach.

Update files in: src/ directory (all HTML files)
""",
                expected_output="All HTML pages populated with integrated content and fully functional",
                accessible_files=[
                    str(self.project_structure.get("docs", "") / "content"),
                    str(self.project_structure.get("src", ""))
                ],
                focus_areas=["HTML integration", "content formatting", "quality assurance"],
                context_source="content_files_and_html_structure"
            )
            
            # Execute with democratic fallback
            result = self._execute_with_democratic_fallback(
                task=integration_task,
                task_name="Content Integration",
                max_retries=3
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Content integration failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_with_democratic_fallback(self, task: Task, task_name: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Execute a task with democratic fallback if it fails multiple times.
        Grok's democratic reflection circles for content issues!
        """
        print(f"🔄 Executing {task_name} (max {max_retries} attempts)")
        
        for attempt in range(max_retries):
            try:
                print(f"  Attempt {attempt + 1}/{max_retries}")
                
                crew = Crew(
                    agents=[self.agent_manager.get_agent("Developer")],
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
                    # Final attempt failed - trigger democratic reflection!
                    print(f"🗳️ {task_name} failed {max_retries} times - TRIGGERING DEMOCRATIC REFLECTION")
                    return self._trigger_democratic_reflection(task_name, str(e))
        
        return {
            "status": "failed",
            "error": f"{task_name} failed after {max_retries} attempts"
        }
    
    def _trigger_democratic_reflection(self, failed_task: str, error_details: str) -> Dict[str, Any]:
        """
        Trigger Grok's democratic reflection circle for content issues.
        """
        print(f"\n🤔 === DEMOCRATIC REFLECTION CIRCLE (CONTENT PHASE) ===")
        print(f"Failed Task: {failed_task}")
        print(f"Grok is taking the lead on content strategy reflection...")
        
        try:
            from tools.team_voting_tool import trigger_democratic_decision_tool
            
            reflection_context = f"""
CONTENT CREATION TASK FAILURE REQUIRING REFLECTION:

Failed Task: {failed_task}
Error Details: {error_details}
Phase: Content Creation & Integration

CONTENT-SPECIFIC REFLECTION QUESTIONS:
1. Is our content strategy aligned with user expectations?
2. Are we overthinking the content complexity?
3. Should we simplify our content approach?
4. Do we need to reassess the meta-documentation strategy?
5. Are technical constraints limiting our content integration?
6. Should we focus more on demonstrating AI collaboration?

GROK'S ROLE: Lead honest discussion about content quality vs. simplicity.
PARTICIPATING AGENTS: All agents contribute content perspectives.

Goal: Democratic consensus on content approach that actually works.
"""
            
            decision_id = trigger_democratic_decision_tool._run(
                conflict_type="performance_tradeoff",
                trigger_reason=f"Content task '{failed_task}' failed 3 times - need content strategy reflection",
                context=reflection_context,
                participating_agents=self.agent_manager.get_participating_agents()
            )
            
            print(f"✅ Democratic content reflection initiated: {decision_id}")
            print("🤝 Grok will facilitate honest discussion about content approach")
            
            return {
                "status": "democratic_reflection_triggered",
                "reflection_decision_id": decision_id,
                "failed_task": failed_task,
                "error": error_details,
                "reflection_focus": "content_strategy",
                "next_action": "Wait for democratic content strategy consensus"
            }
            
        except Exception as e:
            print(f"❌ Failed to trigger democratic reflection: {e}")
            return {
                "status": "failed",
                "error": f"Could not trigger democratic reflection: {e}"
            }