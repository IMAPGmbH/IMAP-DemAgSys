"""
IMAP Democratic Agent System - Modular Phases
Each phase is a separate module for better maintainability and tweaking.
"""

from .phase_1_setup import Phase1Setup
from .phase_2_democracy import Phase2Democracy  
from .phase_3_design import Phase3Design
from .phase_4_development import Phase4Development
from .phase_5_content import Phase5Content
from .phase_6_polish import Phase6Polish

# Phase registry for dynamic loading
PHASES = {
    1: Phase1Setup,
    2: Phase2Democracy,
    3: Phase3Design, 
    4: Phase4Development,
    5: Phase5Content,
    6: Phase6Polish
}

def get_phase(phase_number: int):
    """Get a phase class by number."""
    if phase_number not in PHASES:
        raise ValueError(f"Phase {phase_number} not found. Available: {list(PHASES.keys())}")
    return PHASES[phase_number]

def get_all_phases():
    """Get all available phases."""
    return PHASES

__all__ = [
    'Phase1Setup', 'Phase2Democracy', 'Phase3Design', 
    'Phase4Development', 'Phase5Content', 'Phase6Polish',
    'get_phase', 'get_all_phases', 'PHASES'
]