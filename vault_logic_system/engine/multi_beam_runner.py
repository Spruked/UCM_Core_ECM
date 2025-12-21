"""
MultiBeamRunner - Orchestrates parallel philosophical reasoning with shadow propagation
ECM Contract v1.0 compliant - Deterministic execution with global shadow state
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from vault_logic_system.engine.beam import PhilosophicalBeam

@dataclass
class MultiBeamResult:
    """Container for tribunal-ready output"""
    cvvs: List['CVV']
    shadow_registry: 'ShadowPropagator'
    resonance_markers: Dict[str, Any]
    beam_metadata: Dict[str, Any]

class MultiBeamRunner:
    """
    Orchestrates parallel philosophical reasoning:
    - Executes beams sequentially (deterministic)
    - Maintains global shadow state across executions
    - Returns plurality of CVVs for ECM synthesis
    """

    def __init__(self, skg_runners: List['SKGRunner'], shadow_propagator: 'ShadowPropagator'):
        self.shadow_propagator = shadow_propagator

        # Initialize beams with runners
        self.beams = [
            PhilosophicalBeam(runner, getattr(runner, 'skg_id', f'skg_{i}'))
            for i, runner in enumerate(skg_runners)
        ]

        # Verify beam count matches contract (4 philosophers)
        if len(self.beams) != 4:
            raise ValueError(f"MultiBeamRunner requires exactly 4 SKG beams, got {len(self.beams)}")

    def run(self, claim: Dict[str, Any]) -> MultiBeamResult:
        """
        Execute all beams, collect CVVs, maintain shadow state.
        Sequential execution is epistemically parallel because shadows persist globally.
        """

        cvvs = []
        beam_metadata = {}

        # Execute beams sequentially (shadows accumulate across executions)
        for i, beam in enumerate(self.beams, 1):
            # Set active SKG for shadow emission filtering
            self.shadow_propagator.set_active_skg(beam.skg_id)

            # Run beam through space field
            cvv = beam.run(claim)
            if cvv:
                cvvs.append(cvv)

            # Collect metadata for audit
            beam_metadata[beam.skg_id] = {
                "trajectory_length": len(beam.trajectory),
                "shadows_emitted": len(beam.shadow_artifacts),
                "adjustments_applied": len(beam.get_adjustment_log()),
                "final_confidence": cvv.confidence if cvv else 0.0,
                "final_entropy": cvv.entropy if cvv else 0.0
            }

            # Log beam completion for debug
            confidence = cvv.confidence if cvv else 0.0
            entropy = cvv.entropy if cvv else 0.0
            print(f"  [Beam {i}/4] {beam.skg_id}: confidence={confidence:.3f}, entropy={entropy:.3f}")

        # Compile resonance markers from shadow registry
        resonance_markers = self.shadow_propagator.get_resonance_markers()

        return MultiBeamResult(
            cvvs=cvvs,
            shadow_registry=self.shadow_propagator,
            resonance_markers=resonance_markers,
            beam_metadata=beam_metadata
        )