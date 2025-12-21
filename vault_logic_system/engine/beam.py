"""
PhilosophicalBeam - Thin abstraction for SKG traversal with shadow-aware metrics
ECM Contract v1.0 compliant - Metrics tracking with shadow adjustment
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class BeamMetrics:
    """Live metrics during traversal, subject to shadow adjustment"""
    confidence: float = 0.5
    entropy: float = 0.5
    contradiction: float = 0.0

class PhilosophicalBeam:
    """
    Thin abstraction wrapping a single SKG runner.
    Tracks trajectory and compiles final CVV for tribunal submission.
    """

    def __init__(self, skg_runner: 'SKGRunner', skg_id: str):
        self.runner = skg_runner
        self.skg_id = skg_id
        self.metrics = BeamMetrics()
        self.trajectory: List[str] = field(default_factory=list)
        self.cvv: Optional['CVV'] = None
        self.shadow_artifacts: List[Dict] = field(default_factory=list)

    def run(self, claim: Dict[str, Any]) -> 'CVV':
        """Execute SKG traversal and return Canonical Verdict Vector"""

        # Execute runner (returns CVV + shadow artifacts)
        result = self.runner.run(claim)

        self.trajectory = result.get("reasoning_path", [])
        self.cvv = result.get("cvv")
        self.shadow_artifacts = result.get("shadow_artifacts", [])

        return self.cvv

    def get_adjustment_log(self) -> List[Dict]:
        """Return log of shadow-induced metric adjustments for audit"""
        return getattr(self.runner, 'adjustment_log', [])