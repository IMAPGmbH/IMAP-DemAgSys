import json
import time
from typing import Dict, List, Optional, Any, Type
from enum import Enum
from dataclasses import dataclass, asdict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import datetime

class VotingPhase(Enum):
    """Die 5 Phasen der demokratischen Entscheidungsfindung."""
    CONTEXT_LOADING = "context_loading"
    IDEA_COLLECTION = "idea_collection" 
    SYNTHESIS = "synthesis"
    RANKED_VOTING = "ranked_voting"
    COMMITMENT = "commitment"

class ConflictType(Enum):
    """Arten von Konflikten, die demokratische Entscheidungen triggern."""
    ARCHITECTURE_DECISION = "architecture_decision"
    AGENT_DISAGREEMENT = "agent_disagreement"  
    UX_UI_DIRECTION = "ux_ui_direction"
    PERFORMANCE_TRADEOFF = "performance_tradeoff"
    MANUAL_TRIGGER = "manual_trigger"

@dataclass
class AgentProposal:
    """Vorschlag eines Agents in der Ideensammlung."""
    agent_name: str
    proposal: str
    reasoning: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "proposal": self.proposal,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class VotingOption:
    """Eine synthetisierte Wahlmöglichkeit."""
    option_id: str
    title: str
    description: str
    source_proposals: List[str]  # Agent names who contributed
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class AgentVote:
    """Stimmabgabe eines Agents."""
    agent_name: str
    ranked_options: List[str]  # Option IDs in Präferenz-Reihenfolge
    reasoning_for_top_choice: str
    timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_name": self.agent_name,
            "ranked_options": self.ranked_options,
            "reasoning_for_top_choice": self.reasoning_for_top_choice,
            "timestamp": self.timestamp.isoformat()
        }

@dataclass
class DemocraticDecision:
    """Vollständige demokratische Entscheidung mit allen Phasen."""
    decision_id: str
    conflict_type: ConflictType
    trigger_reason: str
    context: str
    
    # Phase-spezifische Daten
    proposals: List[AgentProposal]
    voting_options: List[VotingOption]
    votes: List[AgentVote]
    
    # Ergebnis
    winning_option_id: str
    winning_option: Optional[VotingOption]
    final_decision: str
    
    # Metadaten
    start_time: datetime
    end_time: Optional[datetime]
    current_phase: VotingPhase
    participating_agents: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "conflict_type": self.conflict_type.value,
            "trigger_reason": self.trigger_reason,
            "context": self.context,
            "proposals": [p.to_dict() for p in self.proposals],
            "voting_options": [vo.to_dict() for vo in self.voting_options],
            "votes": [v.to_dict() for v in self.votes],
            "winning_option_id": self.winning_option_id,
            "winning_option": self.winning_option.to_dict() if self.winning_option else None,
            "final_decision": self.final_decision,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "current_phase": self.current_phase.value,
            "participating_agents": self.participating_agents
        }

class DemocraticVotingLogic:
    """Core-Logik für demokratische Entscheidungsfindung."""
    
    def __init__(self):
        self.active_decisions: Dict[str, DemocraticDecision] = {}
        self.completed_decisions: List[DemocraticDecision] = []
        
    def trigger_democratic_decision(
        self, 
        conflict_type: ConflictType,
        trigger_reason: str,
        context: str,
        participating_agents: List[str]
    ) -> str:
        """Startet eine neue demokratische Entscheidung."""
        decision_id = f"decision_{int(time.time())}_{conflict_type.value}"
        
        decision = DemocraticDecision(
            decision_id=decision_id,
            conflict_type=conflict_type,
            trigger_reason=trigger_reason,
            context=context,
            proposals=[],
            voting_options=[],
            votes=[],
            winning_option_id="",
            winning_option=None,
            final_decision="",
            start_time=datetime.now(),
            end_time=None,
            current_phase=VotingPhase.CONTEXT_LOADING,
            participating_agents=participating_agents
        )
        
        self.active_decisions[decision_id] = decision
        print(f"--- Democracy Engine: New decision triggered - {decision_id} ---")
        return decision_id
    
    def add_agent_proposal(
        self, 
        decision_id: str, 
        agent_name: str, 
        proposal: str, 
        reasoning: str
    ) -> bool:
        """Fügt einen Agent-Vorschlag zur Ideensammlung hinzu."""
        if decision_id not in self.active_decisions:
            return False
            
        decision = self.active_decisions[decision_id]
        if decision.current_phase != VotingPhase.IDEA_COLLECTION:
            return False
            
        if agent_name not in decision.participating_agents:
            return False
            
        # Prüfe, ob Agent bereits einen Vorschlag gemacht hat
        existing_proposal = next((p for p in decision.proposals if p.agent_name == agent_name), None)
        if existing_proposal:
            return False  # Nur ein Vorschlag pro Agent
            
        agent_proposal = AgentProposal(
            agent_name=agent_name,
            proposal=proposal,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
        
        decision.proposals.append(agent_proposal)
        print(f"--- Democracy Engine: Proposal added by {agent_name} for {decision_id} ---")
        return True
    
    def synthesize_options(self, decision_id: str, synthesized_options: List[Dict[str, Any]]) -> bool:
        """Synthetisiert Vorschläge zu konkreten Wahlmöglichkeiten."""
        if decision_id not in self.active_decisions:
            return False
            
        decision = self.active_decisions[decision_id]
        if decision.current_phase != VotingPhase.SYNTHESIS:
            return False
            
        decision.voting_options = []
        for i, option_data in enumerate(synthesized_options):
            option = VotingOption(
                option_id=f"option_{i+1}",
                title=option_data.get("title", f"Option {i+1}"),
                description=option_data.get("description", ""),
                source_proposals=option_data.get("source_proposals", [])
            )
            decision.voting_options.append(option)
            
        print(f"--- Democracy Engine: {len(decision.voting_options)} options synthesized for {decision_id} ---")
        return True
    
    def submit_agent_vote(
        self, 
        decision_id: str, 
        agent_name: str, 
        ranked_option_ids: List[str], 
        reasoning: str
    ) -> bool:
        """Agent gibt seine Stimme ab - COMPLETE VERSION."""
        if decision_id not in self.active_decisions:
            return False
            
        decision = self.active_decisions[decision_id]
        if decision.current_phase != VotingPhase.RANKED_VOTING:
            return False
            
        if agent_name not in decision.participating_agents:
            return False
            
        # Prüfe, ob Agent bereits abgestimmt hat
        existing_vote = next((v for v in decision.votes if v.agent_name == agent_name), None)
        if existing_vote:
            return False
            
        # Validiere, dass alle Option-IDs existieren
        valid_option_ids = [opt.option_id for opt in decision.voting_options]
        if not all(opt_id in valid_option_ids for opt_id in ranked_option_ids):
            return False
            
        vote = AgentVote(
            agent_name=agent_name,
            ranked_options=ranked_option_ids,
            reasoning_for_top_choice=reasoning,
            timestamp=datetime.now()
        )
        
        decision.votes.append(vote)
        print(f"--- Democracy Engine: Vote submitted by {agent_name} for {decision_id} ---")
        
        # Auto-calculate winner if all votes are in
        if len(decision.votes) >= len(decision.participating_agents):
            self.calculate_ranked_choice_winner(decision_id)
        
        return True
    
    def calculate_ranked_choice_winner(self, decision_id: str) -> Optional[str]:
        """Berechnet Gewinner mit Ranked Choice Voting - COMPLETE VERSION."""
        if decision_id not in self.active_decisions:
            return None
            
        decision = self.active_decisions[decision_id]
        if not decision.votes or not decision.voting_options:
            return None
            
        print(f"--- Democracy Engine: Calculating ranked choice winner for {decision_id} ---")
        
        # Ranked Choice Voting Algorithm: Borda Count Method
        option_scores = {opt.option_id: 0 for opt in decision.voting_options}
        
        for vote in decision.votes:
            if vote.ranked_options:
                # Punkte vergeben: 1. Wahl = n Punkte, 2. Wahl = n-1 Punkte, etc.
                max_points = len(decision.voting_options)
                
                for rank, option_id in enumerate(vote.ranked_options[:len(decision.voting_options)]):
                    points = max_points - rank
                    option_scores[option_id] += points
                    print(f"--- Vote: {vote.agent_name} ranked {option_id} #{rank+1} (+{points} points) ---")
        
        # Finde Option mit höchster Punktzahl
        if option_scores:
            winning_option_id = max(option_scores.items(), key=lambda x: x[1])[0]
            winning_score = option_scores[winning_option_id]
            
            decision.winning_option_id = winning_option_id
            decision.winning_option = next(opt for opt in decision.voting_options if opt.option_id == winning_option_id)
            
            # Create final decision text
            decision.final_decision = f"DEMOCRATIC DECISION COMPLETE!\n\nWinner: {decision.winning_option.title}\n\nFinal Scores:\n"
            for option_id, score in sorted(option_scores.items(), key=lambda x: x[1], reverse=True):
                option = next(opt for opt in decision.voting_options if opt.option_id == option_id)
                decision.final_decision += f"- {option.title}: {score} points\n"
            
            decision.final_decision += f"\nSelected Option Details:\n{decision.winning_option.description}"
            
            print(f"--- Democracy Engine: Winner calculated for {decision_id}: {winning_option_id} ({winning_score} points) ---")
            return winning_option_id
        
        return None
    
    def finalize_decision(self, decision_id: str, final_decision_text: str = None) -> bool:
        """Finalisiert die Entscheidung und verschiebt sie zu completed."""
        if decision_id not in self.active_decisions:
            return False
            
        decision = self.active_decisions[decision_id]
        
        if final_decision_text:
            decision.final_decision = final_decision_text
        
        decision.end_time = datetime.now()
        decision.current_phase = VotingPhase.COMMITMENT
        
        # Verschiebe zu completed decisions
        self.completed_decisions.append(decision)
        del self.active_decisions[decision_id]
        
        print(f"--- Democracy Engine: Decision {decision_id} finalized and committed ---")
        return True
    
    def get_decision_status(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """Gibt Status einer Entscheidung zurück."""
        if decision_id in self.active_decisions:
            return self.active_decisions[decision_id].to_dict()
        
        completed = next((d for d in self.completed_decisions if d.decision_id == decision_id), None)
        if completed:
            return completed.to_dict()
            
        return None
    
    def advance_phase(self, decision_id: str, new_phase: VotingPhase) -> bool:
        """Wechselt zur nächsten Phase."""
        if decision_id not in self.active_decisions:
            return False
            
        decision = self.active_decisions[decision_id]
        decision.current_phase = new_phase
        print(f"--- Democracy Engine: {decision_id} advanced to phase {new_phase.value} ---")
        return True

# Globale Instanz der Demokratie-Engine
_democracy_engine = DemocraticVotingLogic()

# === CREWAI TOOLS ===

class TriggerDemocraticDecisionInput(BaseModel):
    conflict_type: str = Field(..., description="Art des Konflikts: 'architecture_decision', 'agent_disagreement', 'ux_ui_direction', 'performance_tradeoff', 'manual_trigger'")
    trigger_reason: str = Field(..., description="Grund für die Auslösung der demokratischen Entscheidung")
    context: str = Field(..., description="Vollständiger Kontext der zu treffenden Entscheidung")
    participating_agents: List[str] = Field(..., description="Liste der Namen der teilnehmenden Agents")

class TriggerDemocraticDecisionTool(BaseTool):
    name: str = "Trigger Democratic Decision Tool"
    description: str = """
    Startet eine neue demokratische Entscheidung zwischen den Agents.
    Sollte vom Project Manager aufgerufen werden, wenn ein Konflikt erkannt wird
    oder eine wichtige Entscheidung demokratisch getroffen werden muss.
    """
    args_schema: Type[BaseModel] = TriggerDemocraticDecisionInput
    
    def _run(self, conflict_type: str, trigger_reason: str, context: str, participating_agents: List[str]) -> str:
        try:
            conflict_enum = ConflictType(conflict_type)
        except ValueError:
            return f"TOOL_ERROR: Invalid conflict_type '{conflict_type}'. Valid types: {[ct.value for ct in ConflictType]}"
        
        if not participating_agents:
            return "TOOL_ERROR: participating_agents cannot be empty"
            
        decision_id = _democracy_engine.trigger_democratic_decision(
            conflict_enum, trigger_reason, context, participating_agents
        )
        
        # Automatisch zur Ideensammlung wechseln
        _democracy_engine.advance_phase(decision_id, VotingPhase.IDEA_COLLECTION)
        
        return f"Democratic decision started with ID: {decision_id}. Phase: IDEA_COLLECTION. Participating agents: {', '.join(participating_agents)}"

class SubmitProposalInput(BaseModel):
    decision_id: str = Field(..., description="ID der laufenden demokratischen Entscheidung")
    agent_name: str = Field(..., description="Name des vorschlagenden Agents")
    proposal: str = Field(..., description="Konkreter Vorschlag für die Lösung")
    reasoning: str = Field(..., description="Begründung für den Vorschlag")

class SubmitProposalTool(BaseTool):
    name: str = "Submit Proposal Tool"
    description: str = """
    Reicht einen Vorschlag für eine laufende demokratische Entscheidung ein.
    Jeder Agent kann genau einen Vorschlag pro Entscheidung einreichen.
    """
    args_schema: Type[BaseModel] = SubmitProposalInput
    
    def _run(self, decision_id: str, agent_name: str, proposal: str, reasoning: str) -> str:
        success = _democracy_engine.add_agent_proposal(decision_id, agent_name, proposal, reasoning)
        
        if not success:
            status = _democracy_engine.get_decision_status(decision_id)
            if not status:
                return f"TOOL_ERROR: Decision {decision_id} not found"
            
            current_phase = status.get('current_phase', 'unknown')
            if current_phase != 'idea_collection':
                return f"TOOL_ERROR: Decision {decision_id} is in phase '{current_phase}', not accepting proposals"
                
            if agent_name not in status.get('participating_agents', []):
                return f"TOOL_ERROR: Agent {agent_name} is not participating in decision {decision_id}"
                
            # Prüfe, ob bereits vorgeschlagen
            existing_proposals = [p['agent_name'] for p in status.get('proposals', [])]
            if agent_name in existing_proposals:
                return f"TOOL_ERROR: Agent {agent_name} has already submitted a proposal for decision {decision_id}"
                
            return f"TOOL_ERROR: Could not submit proposal for unknown reason"
        
        return f"Proposal successfully submitted by {agent_name} for decision {decision_id}"

# NEW: Submit Vote Tool
class SubmitVoteInput(BaseModel):
    decision_id: str = Field(..., description="ID der demokratischen Entscheidung")
    agent_name: str = Field(..., description="Name des abstimmenden Agents")
    ranked_options: List[str] = Field(..., description="Liste der Option-IDs in Präferenz-Reihenfolge (1. Wahl zuerst)")
    reasoning: str = Field(..., description="Begründung für die erste Wahl")

class SubmitVoteTool(BaseTool):
    name: str = "Submit Vote Tool"
    description: str = """
    Reicht eine Ranked Choice Stimme für eine demokratische Entscheidung ein.
    Der Agent rankt alle verfügbaren Optionen in Präferenz-Reihenfolge.
    """
    args_schema: Type[BaseModel] = SubmitVoteInput
    
    def _run(self, decision_id: str, agent_name: str, ranked_options: List[str], reasoning: str) -> str:
        success = _democracy_engine.submit_agent_vote(decision_id, agent_name, ranked_options, reasoning)
        
        if not success:
            status = _democracy_engine.get_decision_status(decision_id)
            if not status:
                return f"TOOL_ERROR: Decision {decision_id} not found"
            
            current_phase = status.get('current_phase', 'unknown')
            if current_phase != 'ranked_voting':
                return f"TOOL_ERROR: Decision {decision_id} is in phase '{current_phase}', not accepting votes"
                
            if agent_name not in status.get('participating_agents', []):
                return f"TOOL_ERROR: Agent {agent_name} is not participating in decision {decision_id}"
                
            # Prüfe, ob bereits abgestimmt
            existing_votes = [v['agent_name'] for v in status.get('votes', [])]
            if agent_name in existing_votes:
                return f"TOOL_ERROR: Agent {agent_name} has already voted for decision {decision_id}"
                
            return f"TOOL_ERROR: Could not submit vote for unknown reason"
        
        return f"Ranked vote successfully submitted by {agent_name} for decision {decision_id}"

class GetDecisionStatusInput(BaseModel):
    decision_id: str = Field(..., description="ID der demokratischen Entscheidung")

class GetDecisionStatusTool(BaseTool):
    name: str = "Get Decision Status Tool"
    description: str = """
    Ruft den aktuellen Status einer demokratischen Entscheidung ab.
    Zeigt Phase, Vorschläge, Stimmen und andere relevante Informationen.
    """
    args_schema: Type[BaseModel] = GetDecisionStatusInput
    
    def _run(self, decision_id: str) -> str:
        status = _democracy_engine.get_decision_status(decision_id)
        if not status:
            return f"TOOL_ERROR: Decision {decision_id} not found"
            
        return json.dumps(status, indent=2, ensure_ascii=False)

# Export der Tools
trigger_democratic_decision_tool = TriggerDemocraticDecisionTool()
submit_proposal_tool = SubmitProposalTool() 
submit_vote_tool = SubmitVoteTool()  # NEW!
get_decision_status_tool = GetDecisionStatusTool()

if __name__ == '__main__':
    print("=== Testing COMPLETE Democratic Voting System ===")
    
    # Test complete workflow
    print("\n1. Triggering a democratic decision...")
    result = trigger_democratic_decision_tool._run(
        conflict_type="architecture_decision",
        trigger_reason="Complete workflow test",
        context="Test the complete democratic process with proposals and voting.",
        participating_agents=["Agent A", "Agent B", "Agent C"]
    )
    print(f"Result: {result}")
    
    # Extract decision ID
    decision_id = result.split("ID: ")[1].split(".")[0]
    
    # Test proposals
    print(f"\n2. Submitting proposals for {decision_id}...")
    proposals = [
        ("Agent A", "Option Alpha", "Because it's first"),
        ("Agent B", "Option Beta", "Because it's second"), 
        ("Agent C", "Option Gamma", "Because it's third")
    ]
    
    for agent, proposal, reasoning in proposals:
        result = submit_proposal_tool._run(decision_id, agent, proposal, reasoning)
        print(f"  {agent}: {result}")
    
    # Advance to synthesis (manual for test)
    _democracy_engine.advance_phase(decision_id, VotingPhase.SYNTHESIS)
    
    # Mock synthesis
    mock_options = [
        {"title": "Option Alpha Enhanced", "description": "Enhanced version of Alpha", "source_proposals": ["Agent A"]},
        {"title": "Option Beta Plus", "description": "Improved Beta", "source_proposals": ["Agent B"]},
        {"title": "Hybrid Gamma", "description": "Combined approach", "source_proposals": ["Agent C"]}
    ]
    _democracy_engine.synthesize_options(decision_id, mock_options)
    _democracy_engine.advance_phase(decision_id, VotingPhase.RANKED_VOTING)
    
    # Test voting
    print(f"\n3. Submitting ranked votes...")
    votes = [
        ("Agent A", ["option_1", "option_2", "option_3"], "Alpha is best"),
        ("Agent B", ["option_2", "option_3", "option_1"], "Beta wins"), 
        ("Agent C", ["option_3", "option_1", "option_2"], "Gamma rules")
    ]
    
    for agent, ranked_opts, reasoning in votes:
        result = submit_vote_tool._run(decision_id, agent, ranked_opts, reasoning)
        print(f"  {agent}: {result}")
    
    # Check final status
    print(f"\n4. Final decision status...")
    final_status = get_decision_status_tool._run(decision_id)
    print(final_status)
    
    print("\n=== COMPLETE Democracy Engine Testing Complete ===")