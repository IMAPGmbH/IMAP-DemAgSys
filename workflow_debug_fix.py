# Quick fix für run_complete_workflow in project_workflow_manager.py
from typing import Dict, Any

def run_complete_workflow(self, user_requirements: str = None) -> Dict[str, Any]:
    """Run the complete modular workflow through all 6 phases."""
    print("🚀 === MODULAR IMAP WORKFLOW (ALL 6 PHASES) ===")
    print(f"Project: {self.project_name}")
    print(f"Total Phases: {len(PHASES)}")
    
    try:
        if user_requirements is None:
            user_requirements = self._get_user_requirements_interactive()
        
        # Execute all phases sequentially with better error handling
        for phase_number in range(1, len(PHASES) + 1):
            print(f"\n🔄 === STARTING PHASE {phase_number} ===")
            
            try:
                phase_result = self._execute_phase(phase_number, user_requirements)
                
                # Store phase result
                self.project_metadata["phase_results"][f"phase_{phase_number}"] = phase_result
                self.project_metadata["current_phase"] = phase_number
                
                # DEBUG: Print detailed phase result
                print(f"📊 Phase {phase_number} Result: {phase_result}")
                
                # Improved status checking
                status = phase_result.get("status", "unknown")
                
                if status == "success":
                    print(f"✅ Phase {phase_number} completed successfully")
                    # Continue to next phase
                elif status in ["complete", "phase_1_complete_manual_recovery"]:
                    print(f"✅ Phase {phase_number} completed (status: {status})")
                    # Continue to next phase  
                elif status == "democratic_reflection_triggered":
                    print(f"🗳️ Phase {phase_number} triggered democratic reflection")
                    self.project_metadata["democratic_decisions"].append({
                        "phase": phase_number,
                        "decision_id": phase_result.get("reflection_decision_id"),
                        "reason": phase_result.get("failed_task")
                    })
                    # Continue to next phase (don't stop for democratic decisions)
                elif status == "failed":
                    print(f"❌ Phase {phase_number} failed - checking if we should stop")
                    print(f"Error details: {phase_result.get('error', 'No error details')}")
                    
                    # Ask user if they want to continue despite failure
                    continue_choice = input(f"Phase {phase_number} failed. Continue anyway? (y/n): ").lower().strip()
                    if continue_choice not in ['y', 'yes']:
                        print(f"❌ Stopping workflow at Phase {phase_number}")
                        break
                    else:
                        print(f"🚀 Continuing despite Phase {phase_number} failure")
                else:
                    print(f"⚠️ Phase {phase_number} returned unexpected status: {status}")
                    print(f"Result: {phase_result}")
                    
                    # Ask user how to proceed
                    continue_choice = input(f"Unexpected status. Continue to next phase? (y/n): ").lower().strip()
                    if continue_choice not in ['y', 'yes']:
                        print(f"❌ Stopping workflow at Phase {phase_number}")
                        break
                
                self._save_project_metadata()
                
            except Exception as phase_error:
                print(f"💥 EXCEPTION in Phase {phase_number}: {phase_error}")
                import traceback
                traceback.print_exc()
                
                # Store error in metadata
                self.project_metadata["phase_results"][f"phase_{phase_number}"] = {
                    "status": "exception",
                    "error": str(phase_error)
                }
                
                # Ask if user wants to continue
                continue_choice = input(f"Phase {phase_number} threw exception. Continue? (y/n): ").lower().strip()
                if continue_choice not in ['y', 'yes']:
                    print(f"❌ Stopping workflow due to Phase {phase_number} exception")
                    break
                else:
                    print(f"🚀 Continuing despite Phase {phase_number} exception")
        
        # Create final project summary
        final_result = self._create_final_project_summary()
        
        print("\n🎉 === MODULAR WORKFLOW COMPLETE ===")
        print(f"✅ Workflow finished!")
        print(f"📁 Project location: {self.project_structure['project_root']}")
        print(f"💰 Budget used: {self.used_budget}€ von {self.budget_euros}€")
        print(f"🌐 Website ready: {final_result.get('website_ready', False)}")
        
        return final_result
        
    except Exception as e:
        print(f"❌ FATAL ERROR in workflow: {e}")
        import traceback
        traceback.print_exc()
        
        self.project_metadata["status"] = "failed"
        self.project_metadata["error"] = str(e)
        self._save_project_metadata()
        return {"status": "failed", "error": str(e)}

# TEST: Laufende Phase 2 direkt
def test_phase_2():
    """Testet Phase 2 direkt"""
    try:
        from project_workflow_manager import ModularOptimizedWorkflowManager
        from pathlib import Path
        
        # Load existing project
        project_structure = Path("PROJECTS/I_HOPE_IT_WORKS")
        project_info = {
            "project_name": "I_HOPE_IT_WORKS",
            "template": "imap_website",
            "structure": {
                "project_root": project_structure,
                "management": project_structure / "management",
                "planning": project_structure / "management" / "planning"
            }
        }
        
        workflow = ModularOptimizedWorkflowManager(project_info, budget_euros=10.0)
        
        print("🧪 Testing Phase 2 directly...")
        phase_2_result = workflow._execute_phase(2)
        
        print(f"\n📊 Phase 2 Direct Test Result:")
        print(f"Status: {phase_2_result.get('status', 'unknown')}")
        print(f"Details: {phase_2_result}")
        
        return phase_2_result
        
    except Exception as e:
        print(f"❌ Phase 2 direct test failed: {e}")
        import traceback
        traceback.print_exc()
        return {"status": "exception", "error": str(e)}

if __name__ == '__main__':
    print("🔧 === TESTING PHASE 2 DIRECTLY ===")
    test_phase_2()