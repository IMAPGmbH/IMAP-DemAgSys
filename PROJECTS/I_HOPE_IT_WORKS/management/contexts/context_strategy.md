# Context Strategy

## 1. Guiding Principles

This project employs a strict 'Need-to-Know' principle for information dissemination to AI agents. The Project Manager (Gemini 2.5 Pro) is responsible for constructing and providing minimal, semantically rich contexts to each agent for their assigned tasks. This strategy aims to:

-   **Maximize Efficiency:** Prevent information overload and allow agents to focus on their specific responsibilities.
-   **Minimize Redundancy:** Avoid agents processing or re-analyzing information already handled by others or irrelevant to their task.
-   **Enhance Focus:** Provide targeted information to improve the quality and speed of task completion.
-   **Maintain Clarity:** Ensure that the context provided is directly applicable and easily understandable.

## 2. Context Construction Techniques

The Project Manager will utilize the following techniques to prepare context for agents:

1.  **Retrieval Augmented Generation (RAG):**
    *   Key documents (e.g., `requirements_analysis.md`, `atomic_task_breakdown.md`, `style_guide.md`, outputs of democratic decisions) will serve as the primary knowledge base.
    *   For a given task, relevant sections or specific data points will be retrieved from these documents.

2.  **Intelligent Summarization:**
    *   The `Text Summarization Tool` will be used to condense larger documents or lengthy discussion outcomes (e.g., from democratic decisions) into concise summaries tailored to the agent's needs.
    *   Summaries will focus on actionable items, key decisions, specifications, or constraints relevant to the upcoming task.

3.  **Selective Information Filtering:**
    *   Based on the `atomic_task_breakdown.md` and `files_access.json`, information will be filtered to ensure an agent only receives data pertinent to their current scope of work.
    *   Dependencies will be explicitly highlighted (e.g., "Your task depends on the output of Task X, which is Y").

4.  **Direct Referencing to Clean Structure:**
    *   Context provision will heavily rely on pointing agents to specific files within the established clean project structure (e.g., "Refer to `docs/style_guide.md` for color palette and typography rules.").
    *   Agents are expected to be able to read these specified files.

5.  **Structured Prompts:**
    *   The Project Manager will craft prompts for agents that clearly define:
        *   The task objective.
        *   The specific deliverables.
        *   The required input files/information (with paths).
        *   The expected output format and location.
        *   Any constraints or specific instructions.

## 3. Context Sources

The primary sources for context generation will be:

-   `management/requirements/user_requirements.md`
-   `management/requirements/requirements_analysis.md`
-   `management/planning/atomic_task_breakdown.md`
-   `management/planning/research_questions.md` (and their answers as they become available in `research/`)
-   `management/planning/website_concept_and_pages.md` (and other outputs of democratic decisions stored in `management/decisions/`)
-   `management/content/*` (outlines, final content)
-   `docs/style_guide.md`
-   `research/design/*` (moodboards, concepts, wireframes, mockups)
-   Outputs from previous tasks as defined in the `atomic_task_breakdown.md`.

## 4. Democratic Decision Context

-   The `Trigger Democratic Decision Tool` requires comprehensive context for the decision to be made. The Project Manager will synthesize this from relevant project artifacts.
-   The outcome of democratic decisions (obtained via `Get Decision Status Tool`) will be formally documented (e.g., in `management/decisions/`) and will become a critical piece of context for subsequent tasks.

## 5. Role of Agents in Context Management

-   While the Project Manager orchestrates context, agents are expected to:
    *   Clearly state if the provided context is insufficient or ambiguous.
    *   Utilize the provided file paths to access necessary information directly.
    *   Focus their processing on the context given for their specific task.

## 6. Iteration and Refinement

This context strategy may be refined as the project progresses and the team gains more experience with inter-agent collaboration and information flow. Feedback from agents on the quality and utility of context provided will be encouraged.