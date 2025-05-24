"""
Project Structure Manager
Handles clean, organized project creation and structure management
"""
import os
import re
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class ProjectStructureManager:
    """
    Manages clean, organized project structure under /PROJECTS/
    Supports different project templates and custom structures
    """
    
    def __init__(self, base_projects_dir: str = "./PROJECTS"):
        self.base_projects_dir = Path(base_projects_dir)
        self.base_projects_dir.mkdir(exist_ok=True)
        
    def sanitize_project_name(self, name: str) -> str:
        """
        Sanitizes project name for filesystem compatibility.
        """
        # Remove special characters, keep only alphanumeric, spaces, hyphens, underscores
        sanitized = re.sub(r'[^\w\s-]', '', name.strip())
        # Replace spaces with underscores, convert to uppercase for visibility
        sanitized = re.sub(r'\s+', '_', sanitized).upper()
        # Remove multiple underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        
        # Ensure it's not empty
        if not sanitized:
            sanitized = f"UNNAMED_PROJECT_{int(time.time())}"
            
        return sanitized
    
    def check_project_exists(self, project_name: str) -> bool:
        """Check if project already exists."""
        project_path = self.base_projects_dir / project_name
        return project_path.exists()
    
    def create_project_structure(self, project_name: str, template: str = "imap_website") -> Dict[str, Path]:
        """
        Creates clean, organized project structure based on template.
        
        Args:
            project_name: Name of the project
            template: Structure template to use ("imap_website", "api_project", "data_analysis", etc.)
        
        Returns:
            Dictionary with all important paths
        """
        sanitized_name = self.sanitize_project_name(project_name)
        
        # Handle existing projects
        if self.check_project_exists(sanitized_name):
            timestamp = int(time.time())
            sanitized_name = f"{sanitized_name}_{timestamp}"
            print(f"⚠️ Project exists, creating: {sanitized_name}")
        
        # Main project directory
        project_root = self.base_projects_dir / sanitized_name
        project_root.mkdir(parents=True, exist_ok=True)
        
        # Get structure based on template
        if template == "imap_website":
            structure = self._create_imap_website_structure(project_root)
        elif template == "api_project":
            structure = self._create_api_project_structure(project_root)
        elif template == "data_analysis":
            structure = self._create_data_analysis_structure(project_root)
        else:
            structure = self._create_default_structure(project_root)
        
        # Create all directories
        for name, path in structure.items():
            if isinstance(path, Path):
                path.mkdir(parents=True, exist_ok=True)
        
        # Create essential files
        self._create_essential_files(structure, sanitized_name, template)
        
        print(f"📁 Clean project structure created: {project_root}")
        print(f"📋 Template used: {template}")
        return structure
    
    def _create_imap_website_structure(self, project_root: Path) -> Dict[str, Path]:
        """Creates structure optimized for IMAP website projects."""
        return {
            # Main directories
            "project_root": project_root,
            "source_code": project_root / "src",
            "documentation": project_root / "docs", 
            "project_management": project_root / "management",
            "research": project_root / "research",
            "testing": project_root / "testing",
            "deployment": project_root / "deployment",
            
            # Source code subdirectories (web-specific)
            "html": project_root / "src" / "html",
            "css": project_root / "src" / "css", 
            "javascript": project_root / "src" / "js",
            "assets": project_root / "src" / "assets",
            "components": project_root / "src" / "components",
            "templates": project_root / "src" / "templates",
            
            # Assets subdirectories
            "images": project_root / "src" / "assets" / "images",
            "fonts": project_root / "src" / "assets" / "fonts",
            "icons": project_root / "src" / "assets" / "icons",
            
            # Management subdirectories (IMAP optimized)
            "requirements": project_root / "management" / "requirements",
            "planning": project_root / "management" / "planning", 
            "progress": project_root / "management" / "progress",
            "decisions": project_root / "management" / "decisions",
            "contexts": project_root / "management" / "contexts",
            "access_policies": project_root / "management" / "access_policies",
            
            # Research subdirectories
            "reports": project_root / "research" / "reports",
            "analysis": project_root / "research" / "analysis",
            "competitive_analysis": project_root / "research" / "competitive_analysis",
            
            # Testing subdirectories (web-focused)
            "unit_tests": project_root / "testing" / "unit",
            "integration_tests": project_root / "testing" / "integration",
            "accessibility_tests": project_root / "testing" / "accessibility",
            "performance_tests": project_root / "testing" / "performance",
            "browser_tests": project_root / "testing" / "browser",
            
            # Documentation subdirectories
            "user_docs": project_root / "docs" / "user",
            "developer_docs": project_root / "docs" / "developer",
            "deployment_docs": project_root / "docs" / "deployment"
        }
    
    def _create_api_project_structure(self, project_root: Path) -> Dict[str, Path]:
        """Creates structure optimized for API projects."""
        return {
            "project_root": project_root,
            "source_code": project_root / "src",
            "api": project_root / "src" / "api",
            "models": project_root / "src" / "models",
            "controllers": project_root / "src" / "controllers",
            "middleware": project_root / "src" / "middleware",
            "config": project_root / "config",
            "tests": project_root / "tests",
            "docs": project_root / "docs",
            "deployment": project_root / "deployment"
        }
    
    def _create_data_analysis_structure(self, project_root: Path) -> Dict[str, Path]:
        """Creates structure optimized for data analysis projects."""
        return {
            "project_root": project_root,
            "data": project_root / "data",
            "raw_data": project_root / "data" / "raw",
            "processed_data": project_root / "data" / "processed",
            "notebooks": project_root / "notebooks",
            "src": project_root / "src",
            "scripts": project_root / "scripts",
            "results": project_root / "results",
            "docs": project_root / "docs"
        }
    
    def _create_default_structure(self, project_root: Path) -> Dict[str, Path]:
        """Creates a basic default structure."""
        return {
            "project_root": project_root,
            "src": project_root / "src",
            "docs": project_root / "docs",
            "tests": project_root / "tests",
            "config": project_root / "config"
        }
    
    def _create_essential_files(self, structure: Dict[str, Path], project_name: str, template: str):
        """Creates essential project files based on template."""
        
        project_root = structure["project_root"]
        
        # Template-specific README
        if template == "imap_website":
            readme_content = self._create_imap_readme(project_name, structure)
        else:
            readme_content = self._create_default_readme(project_name, template)
        
        with open(project_root / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Project metadata
        metadata = {
            "project_name": project_name,
            "template": template,
            "created": datetime.now().isoformat(),
            "structure_version": "2.0_modular",
            "created_by": "IMAP_Democratic_Agent_System",
            "optimization_features": [
                "Selective_Context_Management",
                "Need_to_Know_Principle", 
                "Atomic_Task_Breakdown",
                "Democratic_Decision_Making",
                "Modular_Structure_Management"
            ],
            "structure_paths": {k: str(v) for k, v in structure.items() if isinstance(v, Path)}
        }
        
        with open(project_root / "project_metadata.json", 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Template-specific .gitignore
        gitignore_content = self._create_gitignore(template)
        with open(project_root / ".gitignore", 'w', encoding='utf-8') as f:
            f.write(gitignore_content)
        
        # Template-specific config files
        if template == "imap_website":
            self._create_imap_config_files(structure)
    
    def _create_imap_readme(self, project_name: str, structure: Dict[str, Path]) -> str:
        """Creates README specific to IMAP website projects."""
        return f"""# {project_name.replace('_', ' ').title()}

## Project Overview
Interactive website created with **IMAP Democratic Agent System** featuring optimized selective context management and collaborative AI development.

## 🏗️ Project Structure
```
{project_name}/
├── src/                    # Source code
│   ├── html/              # HTML files & templates
│   ├── css/               # Stylesheets (organized)
│   ├── js/                # JavaScript modules
│   ├── components/        # Reusable UI components
│   ├── templates/         # Template files
│   └── assets/            # Static assets
│       ├── images/        # Images & graphics
│       ├── fonts/         # Web fonts
│       └── icons/         # Icon files
├── management/            # IMAP Project Management
│   ├── requirements/      # Requirements analysis
│   ├── planning/          # Atomic task planning
│   ├── decisions/         # Democratic decisions
│   ├── contexts/          # Agent-specific contexts
│   ├── progress/          # Progress tracking
│   └── access_policies/   # File access policies
├── research/              # Research & Analysis
│   ├── reports/           # Research reports
│   ├── analysis/          # Data analysis
│   └── competitive_analysis/ # Competitor analysis
├── testing/               # Comprehensive Testing
│   ├── accessibility/     # WCAG 2.1 compliance
│   ├── performance/       # Performance tests
│   ├── browser/           # Cross-browser testing
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── docs/                  # Documentation
│   ├── user/              # User guides
│   ├── developer/         # Developer documentation
│   └── deployment/        # Deployment guides
└── deployment/            # Deployment files
```

## 🤖 Created with IMAP Features
- ✅ **Selective Context Management** - Agents receive only relevant information
- ✅ **Need-to-Know Principle** - Optimized information flow
- ✅ **Atomic Task Breakdown** - Modular development approach
- ✅ **Democratic Decision Making** - AI agents collaborate on decisions
- ✅ **Multi-LLM Architecture** - Best AI model for each task

## 🚀 Getting Started
1. Review requirements in `management/requirements/`
2. Check planning documents in `management/planning/`
3. Source code is organized in `src/` by file type
4. Run tests from `testing/` directory
5. Deploy using files in `deployment/`

## 📋 Development Workflow
1. **Requirements Analysis** → `management/requirements/`
2. **Atomic Planning** → `management/planning/`
3. **Democratic Decisions** → `management/decisions/`
4. **Selective Development** → `src/` with context management
5. **Comprehensive Testing** → `testing/` all aspects
6. **Documentation** → `docs/` for users and developers

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _create_default_readme(self, project_name: str, template: str) -> str:
        """Creates default README for other templates."""
        return f"""# {project_name.replace('_', ' ').title()}

Project created with IMAP Democratic Agent System using '{template}' template.

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _create_gitignore(self, template: str) -> str:
        """Creates template-specific .gitignore."""
        base_gitignore = """# Dependencies
node_modules/
venv/
.env
.env.local
.env.production

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
temp/
"""
        
        if template == "imap_website":
            return base_gitignore + """
# Build outputs
dist/
build/
public/

# CSS preprocessors
*.css.map
.sass-cache/

# JavaScript
coverage/
.nyc_output/

# Testing
screenshots/
test-results/
"""
        
        return base_gitignore
    
    def _create_imap_config_files(self, structure: Dict[str, Path]):
        """Creates IMAP-specific configuration files."""
        
        # Create initial files_access.json template
        access_template = {
            "version": "1.0",
            "description": "File access policies for IMAP agents",
            "default_policy": "deny",
            "agent_policies": {
                "Project Manager": {
                    "read": ["*"],
                    "write": ["management/*", "docs/*"],
                    "description": "Full orchestration access"
                },
                "Developer": {
                    "read": ["src/*", "management/planning/*", "management/requirements/*"],
                    "write": ["src/*"],
                    "description": "Source code development access"
                },
                "Tester": {
                    "read": ["src/*", "testing/*"],
                    "write": ["testing/*"],
                    "description": "Testing and quality assurance access"
                },
                "Researcher": {
                    "read": ["research/*", "management/requirements/*"],
                    "write": ["research/*"],
                    "description": "Research and analysis access"
                }
            }
        }
        
        access_file = structure["access_policies"] / "files_access.json"
        with open(access_file, 'w', encoding='utf-8') as f:
            json.dump(access_template, f, indent=2, ensure_ascii=False)

def get_project_name_and_template() -> tuple[str, str]:
    """
    Interactive project name and template selection.
    """
    print("🏗️ === IMAP PROJECT CREATION ===")
    print("Let's create a clean, organized project structure!")
    print()
    
    # Get project name
    while True:
        project_name = input("📝 Enter project name: ").strip()
        
        if not project_name:
            print("❌ Project name cannot be empty. Please try again.")
            continue
            
        if len(project_name) > 50:
            print("❌ Project name too long (max 50 characters). Please try again.")
            continue
        
        break
    
    # Get template
    templates = {
        "1": ("imap_website", "Website/Web App (default for IMAP)"),
        "2": ("api_project", "API/Backend Project"),
        "3": ("data_analysis", "Data Analysis Project"),
        "4": ("default", "Basic Project Structure")
    }
    
    print("\n📋 Select project template:")
    for key, (template_id, description) in templates.items():
        print(f"  {key}. {description}")
    
    while True:
        choice = input("\nSelect template (1-4, default=1): ").strip() or "1"
        
        if choice in templates:
            template_id, description = templates[choice]
            print(f"✅ Selected: {description}")
            break
        else:
            print("❌ Invalid choice. Please enter 1-4.")
    
    # Show preview
    manager = ProjectStructureManager()
    sanitized = manager.sanitize_project_name(project_name)
    
    print(f"\n📁 Project folder: PROJECTS/{sanitized}")
    print(f"📋 Template: {template_id}")
    
    # Confirm
    confirm = input("\n✅ Create project? (y/n): ").lower().strip()
    if confirm not in ['y', 'yes', '']:
        print("❌ Project creation cancelled.")
        exit()
    
    return project_name, template_id

def create_new_project() -> Dict[str, Any]:
    """
    Main function to create a new project with clean structure.
    """
    project_name, template = get_project_name_and_template()
    
    manager = ProjectStructureManager()
    structure = manager.create_project_structure(project_name, template)
    
    print(f"\n🎉 === PROJECT CREATED SUCCESSFULLY ===")
    print(f"📍 Location: {structure['project_root']}")
    print(f"📋 Template: {template}")
    print(f"📂 Ready for IMAP Democratic Agent System!")
    
    return {
        "project_name": project_name,
        "template": template,
        "structure": structure,
        "created": datetime.now().isoformat()
    }

if __name__ == '__main__':
    print("🚀 === TESTING PROJECT STRUCTURE MANAGER ===")
    result = create_new_project()
    print(f"✅ Test completed: {result['project_name']}")