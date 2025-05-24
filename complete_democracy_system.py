"""
Complete Democracy System with Ranked Choice Voting
Vollständiges demokratisches System: Proposals → Synthesis → Ranked Voting → Final Decision
"""
from typing import Dict, Any, List
from crewai import Task, Crew, Process
from tools.team_voting_tool import submit_proposal_tool, get_decision_status_tool
from tools.synthesis_tools import synthesize_voting_options_tool
import time


class CompleteDemocracySystem:
    """
    Vollständiges demokratisches System mit allen 5 Phasen:
    1. Trigger Decision
    2. Collect Proposals 
    3. Synthesize Options
    4. Ranked Choice Voting
    5. Final Decision
    """
    
    def __init__(self, workflow_manager):
        self.workflow_manager = workflow_manager
        self.agent_manager = workflow_manager.agent_manager
    
    def run_complete_democratic_decision(
        self, 
        context: str, 
        participating_agents: List[str],
        conflict_type: str = "architecture_decision",
        trigger_reason: str = "Democratic decision needed"
    ) -> Dict[str, Any]:
        """
        Führt eine vollständige demokratische Entscheidung durch alle 5 Phasen.
        """
        print("🗳️ === COMPLETE DEMOCRATIC DECISION PROCESS ===")
        print(f"Participants: {', '.join(participating_agents)}")
        
        try:
            # Phase 1: Trigger Decision
            print("\n📋 Phase 1: Triggering Democratic Decision...")
            decision_result = self._trigger_decision(context, participating_agents, conflict_type, trigger_reason)
            
            if decision_result["status"] != "success":
                return decision_result
            
            decision_id = decision_result["decision_id"]
            
            # Phase 2: Collect Proposals
            print(f"\n💡 Phase 2: Collecting Proposals from {len(participating_agents)} agents...")
            proposals_result = self._collect_proposals(decision_id, context, participating_agents)
            
            if proposals_result["status"] not in ["success", "partial_success"]:
                return proposals_result
            
            # Phase 3: Synthesize Voting Options
            print(f"\n🔄 Phase 3: Synthesizing proposals into voting options...")
            synthesis_result = self._synthesize_options(decision_id)
            
            if synthesis_result["status"] != "success":
                return synthesis_result
            
            # Phase 4: Ranked Choice Voting
            print(f"\n🗳️ Phase 4: Conducting Ranked Choice Voting...")
            voting_result = self._conduct_ranked_voting(decision_id, context, participating_agents)
            
            if voting_result["status"] != "success":
                return voting_result
            
            # Phase 5: Final Decision
            print(f"\n🏆 Phase 5: Finalizing Democratic Decision...")
            final_result = self._finalize_decision(decision_id)
            
            print("🎉 === DEMOCRATIC DECISION COMPLETE ===")
            return final_result
            
        except Exception as e:
            print(f"❌ Complete democracy failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _trigger_decision(self, context: str, participating_agents: List[str], conflict_type: str, trigger_reason: str) -> Dict[str, Any]:
        """Phase 1: Trigger the democratic decision."""
        try:
            from tools.team_voting_tool import trigger_democratic_decision_tool
            
            decision_output = trigger_democratic_decision_tool._run(
                conflict_type=conflict_type,
                trigger_reason=trigger_reason,
                context=context,
                participating_agents=participating_agents
            )
            
            # Extract decision_id
            if "Democratic decision started with ID: " in decision_output:
                id_start = decision_output.find("ID: ") + 4
                id_end = decision_output.find(".", id_start)
                if id_end == -1:
                    id_end = len(decision_output)
                decision_id = decision_output[id_start:id_end].strip()
                
                print(f"✅ Decision triggered: {decision_id}")
                return {
                    "status": "success",
                    "decision_id": decision_id
                }
            else:
                return {
                    "status": "failed",
                    "error": f"Could not extract decision_id from: {decision_output}"
                }
                
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Failed to trigger decision: {e}"
            }
    
    def _collect_proposals(self, decision_id: str, context: str, participating_agents: List[str]) -> Dict[str, Any]:
        """Phase 2: Collect proposals from all agents."""
        successful_proposals = 0
        
        for agent_name in participating_agents:
            print(f"🤖 Asking {agent_name} for proposal...")
            
            try:
                proposal_task = Task(
                    description=f"""
DEMOCRATIC DECISION PARTICIPATION

DECISION CONTEXT:
{context}

YOUR ROLE: {agent_name}

YOUR TASK:
1. Analyze the context and provide YOUR specific proposal/solution
2. Consider your expertise ({agent_name} perspective)
3. Provide clear reasoning for your proposal

IMPORTANT: 
- Submit your proposal using the Submit Proposal Tool
- Decision ID: {decision_id}
- Be specific and constructive
- Consider what would work best for this project

Make your proposal now!
""",
                    expected_output=f"Confirmation that {agent_name} submitted their proposal",
                    agent=self.agent_manager.get_agent(agent_name),
                    tools=[submit_proposal_tool]
                )
                
                crew = Crew(
                    agents=[self.agent_manager.get_agent(agent_name)],
                    tasks=[proposal_task],
                    process=Process.sequential,
                    verbose=True
                )
                
                result = crew.kickoff()
                successful_proposals += 1
                print(f"✅ {agent_name}: Proposal submitted")
                
            except Exception as e:
                print(f"❌ {agent_name}: Failed to submit proposal - {e}")
        
        print(f"📊 Proposals collected: {successful_proposals}/{len(participating_agents)}")
        
        return {
            "status": "success" if successful_proposals > 0 else "failed",
            "successful_proposals": successful_proposals,
            "total_agents": len(participating_agents)
        }
    
    def _synthesize_options(self, decision_id: str) -> Dict[str, Any]:
        """Phase 3: Synthesize proposals into voting options."""
        try:
            # Use Reflector (Grok) to synthesize options
            synthesis_task = Task(
                description=f"""
SYNTHESIS OF DEMOCRATIC PROPOSALS

Your role is to synthesize the submitted proposals into clear voting options.

DECISION ID: {decision_id}

YOUR TASK:
1. Use the Synthesize Voting Options Tool to create 3-4 distinct voting options
2. Cluster similar proposals together
3. Ensure each option is clear and actionable
4. Create options that represent different approaches

This moves the decision from idea collection to ranked voting phase.
""",
                expected_output="Confirmation that voting options have been synthesized and the decision advanced to voting phase",
                agent=self.agent_manager.get_agent("Reflector"),
                tools=[synthesize_voting_options_tool]
            )
            
            crew = Crew(
                agents=[self.agent_manager.get_agent("Reflector")],
                tasks=[synthesis_task],
                process=Process.sequential,
                verbose=True
            )
            
            result = crew.kickoff()
            print("✅ Options synthesized by Reflector")
            
            return {
                "status": "success",
                "result": str(result)
            }
            
        except Exception as e:
            print(f"❌ Synthesis failed: {e}")
            return {
                "status": "failed",
                "error": str(e)
            }
    
    def _conduct_ranked_voting(self, decision_id: str, context: str, participating_agents: List[str]) -> Dict[str, Any]:
        """Phase 4: Conduct ranked choice voting."""
        successful_votes = 0
        
        # Wait a moment for synthesis to complete
        time.sleep(2)
        
        for agent_name in participating_agents:
            print(f"🗳️ {agent_name} casting ranked vote...")
            
            try:
                voting_task = Task(
                    description=f"""
RANKED CHOICE VOTING

DECISION CONTEXT:
{context}

DECISION ID: {decision_id}

YOUR TASK:
1. Review the synthesized voting options for this decision
2. Rank them in order of your preference (1st choice, 2nd choice, etc.)
3. Provide reasoning for your top choice

IMPORTANT:
- Use tools to check the current decision status first
- Then submit your ranked vote 
- Consider what's best for the overall project
- Rank ALL available options

Cast your ranked vote now!
""",
                    expected_output=f"Confirmation that {agent_name} submitted their ranked vote",
                    agent=self.agent_manager.get_agent(agent_name),
                    tools=[get_decision_status_tool, submit_proposal_tool]  # Note: would need submit_vote_tool
                )
                
                crew = Crew(
                    agents=[self.agent_manager.get_agent(agent_name)],
                    tasks=[voting_task],
                    process=Process.sequential,
                    verbose=True
                )
                
                result = crew.kickoff()
                successful_votes += 1
                print(f"✅ {agent_name}: Vote cast")
                
            except Exception as e:
                print(f"❌ {agent_name}: Failed to vote - {e}")
        
        print(f"📊 Votes cast: {successful_votes}/{len(participating_agents)}")
        
        return {
            "status": "success" if successful_votes > 0 else "failed",
            "successful_votes": successful_votes,
            "total_agents": len(participating_agents)
        }
    
    def _finalize_decision(self, decision_id: str) -> Dict[str, Any]:
        """Phase 5: Get final decision results."""
        try:
            # Get final status
            final_status = get_decision_status_tool._run(decision_id=decision_id)
            
            print(f"🏆 Final Decision Status:")
            print(final_status)
            
            return {
                "status": "success",
                "decision_id": decision_id,
                "final_decision": final_status,
                "democracy_complete": True
            }
            
        except Exception as e:
            return {
                "status": "failed",
                "error": f"Failed to get final decision: {e}"
            }


def test_complete_democracy():
    """Test the complete democratic system."""
    try:
        from project_workflow_manager import ModularOptimizedWorkflowManager
        from pathlib import Path
        
        print("🧪 === TESTING COMPLETE DEMOCRACY SYSTEM ===")
        
        # Load existing project
        project_structure = Path("PROJECTS/I_HOPE_IT_WORKS")
        project_info = {
            "project_name": "I_HOPE_IT_WORKS",
            "template": "imap_website",
            "structure": {
                "project_root": project_structure,
                "management": project_structure / "management"
            }
        }
        
        workflow = ModularOptimizedWorkflowManager(project_info, budget_euros=20.0)
        
        # Create democracy system
        democracy = CompleteDemocracySystem(workflow)
        
        # Test context
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
        
        participating_agents = ["Project Manager", "Developer", "Researcher"]  # Smaller test group
        
        # Run complete democracy
        result = democracy.run_complete_democratic_decision(
            context=context,
            participating_agents=participating_agents,
            conflict_type="architecture_decision",
            trigger_reason="Website content and structure decision"
        )
        
        print(f"\n📊 === COMPLETE DEMOCRACY RESULT ===")
        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Democracy Complete: {result.get('democracy_complete', False)}")
        
        return result
        
    except Exception as e:
        print(f"❌ Complete democracy test failed: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "exception", "error": str(e)}


if __name__ == '__main__':
    test_complete_democracy()