"""
Phase 4: HTML Structure & Navigation Development
Modular implementation for the IMAP Democratic Agent System
"""
from typing import Dict, Any
from crewai import Task, Crew, Process


class Phase4Development:
    """
    Phase 4: HTML Structure & Navigation Development
    
    Responsibilities:
    - Develop HTML structure for homepage
    - Create subpage template
    - Implement navigation bar
    - Create HTML files for each subpage
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self) -> Dict[str, Any]:
        """Execute Phase 4: HTML Structure & Navigation Development."""
        print("\n🏗️ === PHASE 4: HTML STRUCTURE & NAVIGATION DEVELOPMENT ===")
        print("Building the structural foundation of our website...")
        
        try:
            # Step 1: Develop homepage HTML structure
            homepage_result = self._develop_homepage_structure()
            
            # Step 2: Create subpage template
            template_result = self._create_subpage_template()
            
            # Step 3: Implement navigation bar
            navigation_result = self._implement_navigation_bar()
            
            # Step 4: Create individual subpage files
            subpages_result = self._create_subpage_files()
            
            # Update project metadata
            self.workflow_manager.project_metadata.update({
                "current_phase": 4,
                "phase_4_status": "complete",
                "homepage_created": homepage_result["status"] == "success",
                "template_created": template_result["status"] == "success",
                "navigation_implemented": navigation_result["status"] == "success",
                "subpages_created": subpages_result["status"] == "success"
            })
            self.workflow_manager._save_project_metadata()
            
            print("✅ Phase 4 complete: HTML structure and navigation implemented")
            
            return {
                "status": "success",
                "homepage": homepage_result,
                "template": template_result,
                "navigation": navigation_result,
                "subpages": subpages_result,
                "next_phase": 5
            }
            
        except Exception as e:
            print(f"❌ Phase 4 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _develop_homepage_structure(self) -> Dict[str, Any]:
        """Develop HTML structure for the homepage."""
        print("🏠 Creating homepage HTML structure...")
        
        try:
            homepage_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Create the HTML structure for the homepage (index.html).

INPUT DEPENDENCIES:
- docs/design/wireframes/layout_concepts.md (for layout structure)
- management/planning/sitemap_and_navigation.md (for content structure)
- src/css/style.css (to ensure proper linking)

YOUR TASK:
1. Create a complete HTML5 document with:
   - Semantic HTML5 structure
   - Proper DOCTYPE and meta tags
   - Responsive viewport meta tag
   - Link to the CSS stylesheet
   - Proper title and meta descriptions

2. Include structural elements:
   - Header with navigation placeholder
   - Main content area
   - Footer (if applicable)
   - Semantic sections (hero, about, etc.)

3. Include accessibility features:
   - ARIA labels where appropriate
   - Proper heading hierarchy
   - Alt text placeholders for images

4. Create clean, maintainable code structure

IMPORTANT: If this task fails 3 times, a democratic reflection circle 
will be triggered under Grok's leadership to reassess our approach.

Save as: src/index.html
""",
                expected_output="Complete homepage HTML structure ready for content integration",
                accessible_files=[
                    str(self.project_structure.get("docs", "") / "design" / "wireframes" / "layout_concepts.md"),
                    str(self.project_structure.get("planning", "") / "sitemap_and_navigation.md")
                ],
                focus_areas=["HTML5 semantics", "accessibility", "clean structure"],
                context_source="design_and_sitemap_complete"
            )
            
            # Execute with retry logic and democratic fallback
            result = self._execute_with_democratic_fallback(
                task=homepage_task,
                task_name="Homepage HTML Creation",
                max_retries=3
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Homepage structure creation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _create_subpage_template(self) -> Dict[str, Any]:
        """Create a reusable subpage template."""
        print("📄 Creating subpage template...")
        
        try:
            template_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer", 
                task_description="""
Create a reusable HTML template for subpages.

INPUT DEPENDENCIES:
- src/index.html (for consistent structure)
- docs/design/wireframes/layout_concepts.md (for layout)

YOUR TASK:
1. Create subpage_template.html with:
   - Same base structure as homepage
   - Placeholder content areas
   - Consistent navigation
   - Title placeholder that can be easily replaced

2. Include comments for easy customization:
   - Where to change page title
   - Where to add page-specific content
   - Navigation highlighting instructions

3. Ensure template follows same accessibility standards

IMPORTANT: If this task fails 3 times, democratic reflection triggered.

Save as: src/subpage_template.html
""",
                expected_output="Reusable subpage template ready for content population",
                accessible_files=[str(self.project_structure.get("src", "") / "index.html")],
                focus_areas=["template design", "reusability", "consistency"],
                context_source="homepage_structure_complete"
            )
            
            result = self._execute_with_democratic_fallback(
                task=template_task,
                task_name="Subpage Template Creation",
                max_retries=3
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Subpage template creation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _implement_navigation_bar(self) -> Dict[str, Any]:
        """Implement the navigation bar with styling."""
        print("🧭 Implementing navigation bar...")
        
        try:
            nav_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Implement the navigation bar with HTML and CSS styling.

INPUT DEPENDENCIES:
- management/planning/sitemap_and_navigation.md (for nav structure)
- src/css/style.css (for styling)
- research/design/color_palette.md (for colors)

YOUR TASK:
1. Update HTML files (index.html, subpage_template.html) with:
   - Semantic navigation structure
   - Proper link hierarchy
   - Mobile-responsive navigation
   - ARIA navigation labels

2. Update CSS with navigation styles:
   - Navigation bar layout
   - Link styling and hover effects
   - Mobile hamburger menu (if needed)
   - Active page highlighting
   - Purple/magenta accent integration

3. Ensure cross-browser compatibility

IMPORTANT: If this task fails 3 times, Grok leads democratic reflection.

Update: src/index.html, src/subpage_template.html, src/css/style.css
""",
                expected_output="Complete navigation system with styling implemented",
                accessible_files=[
                    str(self.project_structure.get("planning", "") / "sitemap_and_navigation.md"),
                    str(self.project_structure.get("research", "") / "design" / "color_palette.md")
                ],
                focus_areas=["navigation UX", "responsive design", "accessibility"],
                context_source="design_and_structure_complete"
            )
            
            result = self._execute_with_democratic_fallback(
                task=nav_task,
                task_name="Navigation Implementation", 
                max_retries=3
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Navigation implementation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _create_subpage_files(self) -> Dict[str, Any]:
        """Create individual HTML files for each subpage."""
        print("📑 Creating individual subpage files...")
        
        try:
            subpages_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Create individual HTML files for each subpage based on the sitemap.

INPUT DEPENDENCIES:
- management/planning/sitemap_and_navigation.md (for page list)
- src/subpage_template.html (as base template)

YOUR TASK:
1. Read the sitemap to identify all required subpages
2. For each subpage:
   - Copy subpage_template.html
   - Update page title and meta descriptions
   - Add page-specific content placeholders
   - Ensure proper navigation highlighting
   - Save with appropriate filename (e.g., about.html, process.html)

3. Maintain consistent structure across all pages

IMPORTANT: If this task fails 3 times, democratic reflection under Grok.

Create files in: src/ directory
""",
                expected_output="All subpage HTML files created and ready for content",
                accessible_files=[
                    str(self.project_structure.get("planning", "") / "sitemap_and_navigation.md"),
                    str(self.project_structure.get("src", "") / "subpage_template.html")
                ],
                focus_areas=["file organization", "template usage", "consistency"],
                context_source="template_and_sitemap_complete"
            )
            
            result = self._execute_with_democratic_fallback(
                task=subpages_task,
                task_name="Subpage Files Creation",
                max_retries=3
            )
            
            return result
            
        except Exception as e:
            print(f"❌ Subpage files creation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _execute_with_democratic_fallback(self, task: Task, task_name: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Execute a task with democratic fallback if it fails multiple times.
        
        This is where Grok's democratic reflection circles come into play!
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
                    print(f"🗳️ {task_name} failed {max_retries} times - TRIGGERING DEMOCRATIC REFLECTION CIRCLE")
                    return self._trigger_democratic_reflection(task_name, str(e))
        
        return {
            "status": "failed",
            "error": f"{task_name} failed after {max_retries} attempts"
        }
    
    def _trigger_democratic_reflection(self, failed_task: str, error_details: str) -> Dict[str, Any]:
        """
        Trigger Grok's democratic reflection circle when dev tasks fail repeatedly.
        
        This is the democratic safety net! 🗳️
        """
        print(f"\n🤔 === DEMOCRATIC REFLECTION CIRCLE ===")
        print(f"Failed Task: {failed_task}")
        print(f"Triggering reflection under Grok's leadership...")
        
        try:
            from tools.team_voting_tool import trigger_democratic_decision_tool
            
            reflection_context = f"""
DEVELOPMENT TASK FAILURE REQUIRING REFLECTION:

Failed Task: {failed_task}
Error Details: {error_details}
Attempts: 3 (maximum reached)

REFLECTION QUESTIONS:
1. Why is this task repeatedly failing?
2. Are our requirements unclear or unrealistic?
3. Do we need to adjust our approach or tools?
4. Should we simplify this task or break it down further?
5. Are there missing dependencies or prerequisites?

PARTICIPATING AGENTS: All agents should contribute perspectives.
FACILITATOR: Grok (Reflector) will lead this democratic reflection.

Goal: Reach consensus on how to proceed with this blocked task.
"""
            
            decision_id = trigger_democratic_decision_tool._run(
                conflict_type="agent_disagreement",
                trigger_reason=f"Development task '{failed_task}' failed 3 times - democratic reflection needed",
                context=reflection_context,
                participating_agents=self.agent_manager.get_participating_agents()
            )
            
            print(f"✅ Democratic reflection circle initiated: {decision_id}")
            print("🤝 Grok will facilitate team reflection on this development blocker")
            
            return {
                "status": "democratic_reflection_triggered",
                "reflection_decision_id": decision_id,
                "failed_task": failed_task,
                "error": error_details,
                "next_action": "Wait for democratic reflection results before proceeding"
            }
            
        except Exception as e:
            print(f"❌ Failed to trigger democratic reflection: {e}")
            return {
                "status": "failed",
                "error": f"Could not trigger democratic reflection: {e}"
            }