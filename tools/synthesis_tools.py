import json
from typing import Dict, Optional, List, Type, Any
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from dataclasses import dataclass
from collections import defaultdict
import re

# Import the democracy engine from team_voting_tool
try:
    from tools.team_voting_tool import _democracy_engine, VotingPhase, VotingOption
except ImportError:
    print("Warning: Could not import democracy engine. Synthesis tools will not work properly.")
    _democracy_engine = None
    VotingPhase = None
    VotingOption = None

@dataclass
class ProposalCluster:
    """Cluster ähnlicher Vorschläge."""
    theme: str
    description: str
    contributing_agents: List[str]
    merged_reasoning: str
    representative_proposal: str

class ProposalSynthesisLogic:
    """Logik für die Synthese von Agent-Vorschlägen zu Wahloptionen."""
    
    def analyze_proposals(self, proposals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analysiert alle Vorschläge und identifiziert Themen und Überschneidungen."""
        if not proposals:
            return {"error": "No proposals to analyze"}
        
        analysis = {
            "total_proposals": len(proposals),
            "agents": [p["agent_name"] for p in proposals],
            "themes": [],
            "overlaps": [],
            "unique_aspects": []
        }
        
        # Einfache Keyword-basierte Themen-Erkennung
        technology_keywords = {
            "meta_documentation": ["meta", "documentation", "process", "creation", "showcase"],
            "collaboration": ["collaboration", "team", "collaborative", "democratic"],
            "technical": ["technical", "architecture", "code", "development", "stack"],
            "overview": ["overview", "about", "general", "mission", "capabilities"],
            "contact": ["contact", "reach", "communication"]
        }
        
        proposal_themes = defaultdict(list)
        
        for proposal in proposals:
            text = (proposal["proposal"] + " " + proposal["reasoning"]).lower()
            
            for theme, keywords in technology_keywords.items():
                if any(keyword in text for keyword in keywords):
                    proposal_themes[theme].append(proposal["agent_name"])
        
        analysis["themes"] = [
            {"theme": theme, "agents": agents} 
            for theme, agents in proposal_themes.items() 
            if agents
        ]
        
        return analysis
    
    def cluster_similar_proposals(self, proposals: List[Dict[str, Any]]) -> List[ProposalCluster]:
        """Clustert ähnliche Vorschläge basierend auf Inhalt und Ansatz."""
        if not proposals:
            return []
        
        print(f"📊 Clustering {len(proposals)} proposals...")
        
        clusters = {}
        
        for proposal in proposals:
            text = (proposal["proposal"] + " " + proposal["reasoning"]).lower()
            agent = proposal["agent_name"]
            
            # Bestimme primäres Thema basierend auf Inhalt
            primary_theme = "general"
            
            if any(word in text for word in ["meta", "documentation", "process", "showcase", "creation"]):
                primary_theme = "meta_documentation"
            elif any(word in text for word in ["about", "overview", "general", "mission", "contact"]):
                primary_theme = "overview_approach"
            elif any(word in text for word in ["technical", "architecture", "code", "development"]):
                primary_theme = "technical_focus"
            
            if primary_theme not in clusters:
                clusters[primary_theme] = ProposalCluster(
                    theme=primary_theme,
                    description="",
                    contributing_agents=[],
                    merged_reasoning="",
                    representative_proposal=""
                )
            
            cluster = clusters[primary_theme]
            cluster.contributing_agents.append(agent)
            
            # Verwende den ersten Vorschlag als repräsentativen
            if not cluster.representative_proposal:
                cluster.representative_proposal = proposal["proposal"]
                cluster.merged_reasoning = proposal["reasoning"]
            else:
                # Merge reasoning
                cluster.merged_reasoning += f" | {agent}: {proposal['reasoning']}"
        
        print(f"✅ Created {len(clusters)} clusters: {list(clusters.keys())}")
        return list(clusters.values())
    
    def generate_voting_options(self, clusters: List[ProposalCluster], max_options: int = 4) -> List[Dict[str, Any]]:
        """Generiert klare Wahloptionen aus den Proposal-Clustern."""
        voting_options = []
        
        # Sortiere Cluster nach Anzahl der unterstützenden Agents
        sorted_clusters = sorted(clusters, key=lambda c: len(c.contributing_agents), reverse=True)
        
        for i, cluster in enumerate(sorted_clusters[:max_options]):
            option = {
                "title": self._generate_option_title(cluster),
                "description": self._generate_option_description(cluster),
                "source_proposals": cluster.contributing_agents,
                "rationale": cluster.merged_reasoning
            }
            voting_options.append(option)
            print(f"📋 Option {i+1}: {option['title']} (from {', '.join(cluster.contributing_agents)})")
        
        return voting_options
    
    def _generate_option_title(self, cluster: ProposalCluster) -> str:
        """Generiert einen prägnanten Titel für eine Wahloption."""
        theme_titles = {
            "meta_documentation": "Meta-Documentation Approach",
            "overview_approach": "General Overview Approach", 
            "technical_focus": "Technical-Focused Approach",
            "collaboration": "Collaboration-Centered Approach",
            "general": "Hybrid Approach"
        }
        
        base_title = theme_titles.get(cluster.theme, f"{cluster.theme.title()} Approach")
        
        if len(cluster.contributing_agents) > 1:
            return f"{base_title} (Team Consensus)"
        else:
            return f"{base_title} ({cluster.contributing_agents[0]} Proposal)"
    
    def _generate_option_description(self, cluster: ProposalCluster) -> str:
        """Generiert eine ausführliche Beschreibung für eine Wahloption."""
        description = cluster.representative_proposal
        
        if len(cluster.contributing_agents) > 1:
            description += f"\n\nSupported by: {', '.join(cluster.contributing_agents)}"
            description += f"\nCombined reasoning: {cluster.merged_reasoning}"
        else:
            description += f"\n\nProposed by: {cluster.contributing_agents[0]}"
            description += f"\nReasoning: {cluster.merged_reasoning}"
        
        return description

# Globale Instanz der Synthesis-Logik
_synthesis_logic = ProposalSynthesisLogic()

# === CREWAI TOOLS ===

class AnalyzeProposalsInput(BaseModel):
    decision_id: str = Field(..., description="ID der demokratischen Entscheidung")

class AnalyzeProposalsTool(BaseTool):
    name: str = "Analyze Proposals Tool"
    description: str = """
    Analysiert alle eingereichten Vorschläge für eine demokratische Entscheidung.
    Identifiziert Themen, Überschneidungen und einzigartige Aspekte.
    Wird vom Reflector verwendet, um die Proposal-Landschaft zu verstehen.
    """
    args_schema: Type[BaseModel] = AnalyzeProposalsInput
    
    def _run(self, decision_id: str) -> str:
        if not _democracy_engine:
            return "TOOL_ERROR: Democracy engine not available"
        
        status = _democracy_engine.get_decision_status(decision_id)
        if not status:
            return f"TOOL_ERROR: Decision {decision_id} not found"
        
        proposals = status.get("proposals", [])
        if not proposals:
            return f"TOOL_INFO: No proposals yet for decision {decision_id}"
        
        analysis = _synthesis_logic.analyze_proposals(proposals)
        
        return json.dumps({
            "decision_id": decision_id,
            "analysis": analysis,
            "summary": f"Analyzed {analysis['total_proposals']} proposals from {len(analysis['agents'])} agents. "
                      f"Identified {len(analysis['themes'])} main themes."
        }, indent=2, ensure_ascii=False)

class SynthesizeOptionsInput(BaseModel):
    decision_id: str = Field(..., description="ID der demokratischen Entscheidung")
    max_options: int = Field(4, description="Maximale Anzahl von Wahloptionen (Standard: 4)")

class SynthesizeOptionsTool(BaseTool):
    name: str = "Synthesize Voting Options Tool"
    description: str = """
    Synthetisiert Agent-Vorschläge zu klaren, abstimmbaren Optionen.
    Clustert ähnliche Vorschläge und erstellt 3-4 distinkte Wahlmöglichkeiten.
    Wird vom Reflector verwendet, um von der Ideensammlung zum Voting überzugehen.
    """
    args_schema: Type[BaseModel] = SynthesizeOptionsInput
    
    def _run(self, decision_id: str, max_options: int = 4) -> str:
        if not _democracy_engine:
            return "TOOL_ERROR: Democracy engine not available"
        
        print(f"🔄 Synthesizing options for decision {decision_id}...")
        
        status = _democracy_engine.get_decision_status(decision_id)
        if not status:
            return f"TOOL_ERROR: Decision {decision_id} not found"
        
        # FIXED: Don't require specific phase, just check if proposals exist
        proposals = status.get("proposals", [])
        if not proposals:
            return f"TOOL_ERROR: No proposals to synthesize for decision {decision_id}"
        
        print(f"📋 Found {len(proposals)} proposals to synthesize")
        
        # Cluster proposals
        clusters = _synthesis_logic.cluster_similar_proposals(proposals)
        
        if not clusters:
            return f"TOOL_ERROR: Could not create clusters from proposals"
        
        # Generate voting options
        voting_options = _synthesis_logic.generate_voting_options(clusters, max_options)
        
        if not voting_options:
            return f"TOOL_ERROR: Could not generate voting options from clusters"
        
        print(f"🗳️ Generated {len(voting_options)} voting options")
        
        # FIXED: Manually advance to synthesis phase first
        _democracy_engine.advance_phase(decision_id, VotingPhase.SYNTHESIS)
        
        # Update the decision with synthesized options
        success = _democracy_engine.synthesize_options(decision_id, voting_options)
        
        if not success:
            return f"TOOL_ERROR: Could not update decision {decision_id} with synthesized options"
        
        # FIXED: Advance to voting phase
        _democracy_engine.advance_phase(decision_id, VotingPhase.RANKED_VOTING)
        
        print(f"✅ Decision {decision_id} advanced to RANKED_VOTING phase")
        
        result = {
            "decision_id": decision_id,
            "synthesized_options": voting_options,
            "clusters_found": len(clusters),
            "options_created": len(voting_options),
            "phase": "ranked_voting",
            "message": f"Successfully synthesized {len(proposals)} proposals into {len(voting_options)} voting options",
            "status": "success"
        }
        
        return json.dumps(result, indent=2, ensure_ascii=False)

class FacilitateReflectionInput(BaseModel):
    decision_id: str = Field(..., description="ID der demokratischen Entscheidung")
    reflection_prompt: str = Field(..., description="Spezifischer Reflection-Prompt oder Meta-Frage")

class FacilitateReflectionTool(BaseTool):
    name: str = "Facilitate Reflection Tool"
    description: str = """
    Stellt Meta-Fragen und erleichtert die Reflexion über den Entscheidungsprozess.
    Hilft dem Team dabei, blinde Flecken zu identifizieren und tiefere Einsichten zu gewinnen.
    Wird vom Reflector verwendet, um die Qualität der demokratischen Entscheidung zu verbessern.
    """
    args_schema: Type[BaseModel] = FacilitateReflectionInput
    
    def _run(self, decision_id: str, reflection_prompt: str) -> str:
        if not _democracy_engine:
            return "TOOL_ERROR: Democracy engine not available"
        
        status = _democracy_engine.get_decision_status(decision_id)
        if not status:
            return f"TOOL_ERROR: Decision {decision_id} not found"
        
        # Generiere kontextuelle Reflexionsfragen
        context = status.get("context", "")
        proposals = status.get("proposals", [])
        current_phase = status.get("current_phase", "")
        
        reflection_analysis = {
            "decision_id": decision_id,
            "current_phase": current_phase,
            "reflection_prompt": reflection_prompt,
            "meta_questions": self._generate_meta_questions(context, proposals),
            "process_observations": self._analyze_process(proposals, current_phase),
            "recommendations": self._generate_recommendations(proposals, current_phase)
        }
        
        return json.dumps(reflection_analysis, indent=2, ensure_ascii=False)
    
    def _generate_meta_questions(self, context: str, proposals: List[Dict]) -> List[str]:
        """Generiert relevante Meta-Fragen für die Reflexion."""
        questions = [
            "Was übersehen wir in unserer aktuellen Diskussion?",
            "Welche langfristigen Konsequenzen berücksichtigen wir noch nicht?",
            "Wie können die verschiedenen Perspektiven sich gegenseitig stärken?"
        ]
        
        if "performance" in context.lower():
            questions.append("Balancieren wir Performance und Wartbarkeit angemessen?")
        
        if "framework" in context.lower():
            questions.append("Berücksichtigen wir die Lernkurve des Teams ausreichend?")
        
        if len(proposals) > 3:
            questions.append("Gibt es gemeinsame Grundannahmen, die alle Vorschläge teilen?")
        
        return questions
    
    def _analyze_process(self, proposals: List[Dict], current_phase: str) -> Dict[str, Any]:
        """Analysiert die Qualität des bisherigen Prozesses."""
        return {
            "participation_balance": self._assess_participation(proposals),
            "reasoning_depth": self._assess_reasoning_quality(proposals),
            "diversity_of_approaches": self._assess_diversity(proposals),
            "phase_readiness": f"Process is in {current_phase} phase"
        }
    
    def _assess_participation(self, proposals: List[Dict]) -> str:
        """Bewertet die Ausgewogenheit der Teilnahme."""
        if not proposals:
            return "No participation yet"
        
        agents = [p["agent_name"] for p in proposals]
        unique_agents = set(agents)
        
        if len(unique_agents) >= 3:
            return "Good participation balance"
        elif len(unique_agents) == 2:
            return "Moderate participation - could benefit from more voices"
        else:
            return "Limited participation - encourage more agents to contribute"
    
    def _assess_reasoning_quality(self, proposals: List[Dict]) -> str:
        """Bewertet die Qualität der Begründungen."""
        if not proposals:
            return "No reasoning to assess yet"
        
        avg_reasoning_length = sum(len(p.get("reasoning", "")) for p in proposals) / len(proposals)
        
        if avg_reasoning_length > 100:
            return "Rich, detailed reasoning provided"
        elif avg_reasoning_length > 50:
            return "Adequate reasoning depth"
        else:
            return "Could benefit from more detailed reasoning"
    
    def _assess_diversity(self, proposals: List[Dict]) -> str:
        """Bewertet die Vielfalt der Ansätze."""
        if len(proposals) < 2:
            return "Need more proposals to assess diversity"
        
        # Einfache Bewertung basierend auf unterschiedlichen Schlüsselwörtern
        all_text = " ".join([p["proposal"] + " " + p.get("reasoning", "") for p in proposals]).lower()
        
        diversity_indicators = ["alternative", "different", "another approach", "however", "instead"]
        diversity_score = sum(1 for indicator in diversity_indicators if indicator in all_text)
        
        if diversity_score >= 3:
            return "High diversity of approaches"
        elif diversity_score >= 1:
            return "Moderate diversity - good range of options"
        else:
            return "Similar approaches - could benefit from more diverse thinking"
    
    def _generate_recommendations(self, proposals: List[Dict], current_phase: str) -> List[str]:
        """Generiert Empfehlungen für den weiteren Prozess."""
        recommendations = []
        
        if current_phase == "idea_collection" and len(proposals) < 3:
            recommendations.append("Consider encouraging more agents to contribute proposals")
        
        if current_phase == "idea_collection":
            recommendations.append("Ensure all proposals address the core decision criteria")
            recommendations.append("Look for opportunities to combine complementary approaches")
        
        if proposals:
            reasoning_lengths = [len(p.get("reasoning", "")) for p in proposals]
            if min(reasoning_lengths) < 30:
                recommendations.append("Encourage more detailed reasoning for all proposals")
        
        return recommendations

# Export der Tools
analyze_proposals_tool = AnalyzeProposalsTool()
synthesize_voting_options_tool = SynthesizeOptionsTool()
facilitate_reflection_tool = FacilitateReflectionTool()

# TEST FUNCTION
def test_synthesis_fix():
    """Test the fixed synthesis with the existing decision."""
    print("🧪 === TESTING FIXED SYNTHESIS ===")
    
    # Use the existing decision from the logs
    decision_id = "decision_1748122344_architecture_decision"
    
    try:
        # Test synthesis directly
        result = synthesize_voting_options_tool._run(decision_id, max_options=3)
        print(f"📊 Synthesis Result:\n{result}")
        
        # Check updated status
        status = _democracy_engine.get_decision_status(decision_id)
        if status:
            print(f"\n📋 Updated Status:")
            print(f"Phase: {status.get('current_phase', 'unknown')}")
            print(f"Voting Options: {len(status.get('voting_options', []))}")
            print(f"Proposals: {len(status.get('proposals', []))}")
        
        return result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "failed", "error": str(e)}

if __name__ == '__main__':
    test_synthesis_fix()