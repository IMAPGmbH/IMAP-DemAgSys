"""
Phase 3: Design & Color Palette Creation
Modular implementation for the IMAP Democratic Agent System
"""
from typing import Dict, Any
from crewai import Task, Crew, Process


class Phase3Design:
    """
    Phase 3: Design & Color Palette Creation
    
    Responsibilities:
    - Research and select specific color palette
    - Research font implementation details  
    - Create basic wireframes/layout concepts
    - Develop initial CSS stylesheet
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
        self.context_manager = workflow_manager.context_manager
        self.project_structure = workflow_manager.project_structure
        
    def execute(self) -> Dict[str, Any]:
        """Execute Phase 3: Design & Color Palette Creation."""
        print("\n🎨 === PHASE 3: DESIGN & COLOR PALETTE CREATION ===")
        print("Creating the visual foundation for our website...")
        
        try:
            # Step 1: Research and create color palette
            color_result = self._create_color_palette()
            
            # Step 2: Research font implementation
            font_result = self._research_font_implementation()
            
            # Step 3: Create wireframes
            wireframe_result = self._create_wireframes()
            
            # Step 4: Develop initial CSS
            css_result = self._develop_initial_css()
            
            # Update project metadata
            self.workflow_manager.project_metadata.update({
                "current_phase": 3,
                "phase_3_status": "complete",
                "color_palette_created": color_result["status"] == "success",
                "font_research_done": font_result["status"] == "success", 
                "wireframes_created": wireframe_result["status"] == "success",
                "initial_css_created": css_result["status"] == "success"
            })
            self.workflow_manager._save_project_metadata()
            
            print("✅ Phase 3 complete: Design foundation established")
            
            return {
                "status": "success",
                "color_palette": color_result,
                "font_implementation": font_result,
                "wireframes": wireframe_result,
                "css_foundation": css_result,
                "next_phase": 4
            }
            
        except Exception as e:
            print(f"❌ Phase 3 failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "next_phase": None
            }
    
    def _create_color_palette(self) -> Dict[str, Any]:
        """Research and create specific color palette."""
        print("🎨 Creating color palette...")
        
        try:
            color_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",  # Claude as design-focused developer
                task_description="""
Research and create a specific color palette for the dark themed website.

REQUIREMENTS:
- Dark, almost black gray tones for backgrounds
- Vibrant purple/magenta accent colors  
- Professional, elegant appearance
- Good contrast for accessibility

YOUR TASK:
1. Research and select specific hex codes for:
   - Primary background (dark gray/black)
   - Secondary background (lighter dark gray)
   - Primary text color (light gray/white)
   - Primary accent color (purple/magenta)
   - Secondary accent color (lighter purple/magenta)
   - Border colors
   - Hover states

2. Ensure WCAG 2.1 AA contrast compliance
3. Create a comprehensive color palette document
4. Include usage guidelines for each color

Save in: research/design/color_palette.md
""",
                expected_output="Complete color palette with hex codes and usage guidelines saved in research/design/color_palette.md",
                accessible_files=[],
                focus_areas=["color theory", "accessibility", "dark theme design"],
                context_source="design_requirements"
            )
            
            color_crew = Crew(
                agents=[self.agent_manager.get_agent("Developer")],
                tasks=[color_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = color_crew.kickoff()
            print("✅ Color palette created")
            
            return {
                "status": "success",
                "result": str(result)
            }
            
        except Exception as e:
            print(f"❌ Color palette creation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _research_font_implementation(self) -> Dict[str, Any]:
        """Research Poppins font implementation details."""
        print("🔤 Researching font implementation...")
        
        try:
            font_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Research and document Poppins font implementation for the website.

REQUIREMENTS:
- Poppins Regular for body text
- Poppins SemiBold for headings
- Fast loading and reliable implementation

YOUR TASK:
1. Find the best way to include Poppins fonts:
   - Google Fonts CDN links
   - Font display optimization
   - Fallback fonts

2. Create CSS font-face declarations
3. Document font usage guidelines:
   - Font sizes for different heading levels
   - Line heights and spacing
   - Font weights available

4. Include performance considerations

Save in: research/design/font_implementation.md
""",
                expected_output="Complete font implementation guide with CDN links and CSS ready for use",
                accessible_files=[],
                focus_areas=["web fonts", "performance", "typography"],
                context_source="typography_requirements"
            )
            
            font_crew = Crew(
                agents=[self.agent_manager.get_agent("Developer")],
                tasks=[font_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = font_crew.kickoff()
            print("✅ Font implementation researched")
            
            return {
                "status": "success",
                "result": str(result)
            }
            
        except Exception as e:
            print(f"❌ Font research failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _create_wireframes(self) -> Dict[str, Any]:
        """Create basic wireframes and layout concepts."""
        print("📐 Creating wireframes...")
        
        try:
            wireframe_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Create basic wireframes and layout concepts for the website.

INPUT DEPENDENCIES:
- Check management/planning/sitemap_and_navigation.md for page structure
- Review democratic decision results for content requirements

YOUR TASK:
1. Create wireframes for:
   - Homepage layout
   - Standard subpage layout
   - Navigation bar design
   - Mobile responsive considerations

2. Define layout structure:
   - Header with navigation
   - Main content area
   - Footer (if needed)
   - Sidebar (if applicable)

3. Document layout decisions and rationale
4. Include responsive breakpoints

Since we can't create actual image files, create detailed ASCII wireframes 
and descriptive text layouts.

Save in: docs/design/wireframes/layout_concepts.md
""",
                expected_output="Detailed wireframes and layout concepts documented for development team",
                accessible_files=[str(self.project_structure.get("planning", "") / "sitemap_and_navigation.md")],
                focus_areas=["layout design", "user experience", "responsive design"],
                context_source="sitemap_and_content_structure"
            )
            
            wireframe_crew = Crew(
                agents=[self.agent_manager.get_agent("Developer")],
                tasks=[wireframe_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = wireframe_crew.kickoff()
            print("✅ Wireframes created")
            
            return {
                "status": "success",
                "result": str(result)
            }
            
        except Exception as e:
            print(f"❌ Wireframe creation failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _develop_initial_css(self) -> Dict[str, Any]:
        """Develop the initial CSS stylesheet."""
        print("💅 Developing initial CSS stylesheet...")
        
        try:
            css_task = self.workflow_manager._create_atomic_task(
                agent_name="Developer",
                task_description="""
Create the initial CSS stylesheet for the website.

INPUT DEPENDENCIES:
- research/design/color_palette.md (for colors)
- research/design/font_implementation.md (for fonts)
- docs/design/wireframes/layout_concepts.md (for layout)

YOUR TASK:
1. Create a comprehensive CSS file with:
   - CSS Reset/Normalize
   - Font imports and declarations
   - Color variable definitions (CSS custom properties)
   - Base typography styles
   - Layout structure (flexbox/grid)
   - Navigation bar styles
   - Responsive design basics

2. Include:
   - Mobile-first responsive approach
   - Hover and focus states
   - Accessibility considerations
   - Clean, maintainable code structure

3. Use modern CSS features:
   - CSS Grid and Flexbox
   - CSS Custom Properties (variables)
   - Logical properties where appropriate

Save as: src/css/style.css
""",
                expected_output="Complete CSS foundation ready for HTML implementation",
                accessible_files=[
                    str(self.project_structure.get("research", "") / "design" / "color_palette.md"),
                    str(self.project_structure.get("research", "") / "design" / "font_implementation.md")
                ],
                focus_areas=["CSS architecture", "responsive design", "accessibility"],
                context_source="design_research_complete"
            )
            
            css_crew = Crew(
                agents=[self.agent_manager.get_agent("Developer")],
                tasks=[css_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = css_crew.kickoff()
            print("✅ Initial CSS stylesheet created")
            
            return {
                "status": "success",
                "result": str(result)
            }
            
        except Exception as e:
            print(f"❌ CSS development failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }