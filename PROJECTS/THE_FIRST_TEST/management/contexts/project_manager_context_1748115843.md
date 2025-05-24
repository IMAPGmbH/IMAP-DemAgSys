=== CURRENT TASK ===

As the Project Manager, analyze requirements and create atomic task breakdown using the clean project structure.

USER REQUIREMENTS:
Hey Team, baut eine einfache Testwebsite mit Navigation, ein paar Unterseiten. Das ganze soll euer Können demonstrieren, aber nicht zu sehr ausufern! Es soll ein cooles dunkles Design sein, mit dunklen fast schwarzen grautönen , schriftarten: poppins regular für copy, semibold für überschriften! baut kleine elegante farbige akzente in einem knalligen lila/magenta ein. Den Inhalt dürft ihr euch demokratisch völlig frei ausdenken! Dokumentiert gerne euren Gedankenprozess auf der Seite, die ihr erstellt, also im Endprodukt! Dann wird es richtig Meta. Viel Spaß!

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


=== PROJECT STRUCTURE ===
📁 Management: PROJECTS\THE_FIRST_TEST\management
📁 Source: PROJECTS\THE_FIRST_TEST\src
📁 Documentation: PROJECTS\THE_FIRST_TEST\docs

=== RELEVANT INFORMATION ===
📄 PROJECTS\THE_FIRST_TEST\management\requirements\user_requirements.md (summarized):
The project requires building a simple test website with navigation and several subpages, showcasing team skills without excessive complexity.  The design should be dark, using dark gray tones, with Poppins Regular font for body text and Semibold for headings.  Vibrant purple/magenta accents are required.  Content is freely chosen by the team.  The development process should be documented on the website itself.

**Atomic Task Breakdown (Clean Project Structure):**

1. **Project Setup:** Create a new project directory, initialize Git repository, and select a suitable framework (e.g., React, Vue, or similar).
2. **Design System:** Define color palette (dark grays, vibrant purple/magenta), typography (Poppins Regular/Semibold), and overall styling.  Create reusable CSS components.
3. **Navigation Structure:** Plan and implement website navigation (main menu, subpages).
4. **Content Creation:** Brainstorm and collaboratively decide on website content for each subpage.
5. **Subpage Development:** Develop individual subpages, integrating content and styling.
6. **Development Documentation:**  Implement a section within the website to document the team's design and development process.  This documentation will be incorporated directly into the final product.  Consider using Markdown for clear formatting.
7. **Testing & Quality Assurance:** Conduct thorough testing across different browsers and devices.
8. **Deployment:** Deploy the website to a hosting platform.

**Selective Context Planning:** Focus initial development on core functionality (navigation, basic subpage structure) before adding styling and detailed content. Prioritize creating reusable components to minimize repetitive work.  Regular team communication and version control are essential.

=== GUIDANCE FOR PROJECT MANAGER ===
🎯 You are the central orchestrator with clean project structure.
- Use management/ directory for all planning artifacts
- Save contexts in management/contexts/ for other agents
- Store decisions in management/decisions/
- Coordinate file access via access policies
- Follow Buddhist Middle Way: thorough but efficient
