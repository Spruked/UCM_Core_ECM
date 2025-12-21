"""
ECM Runtime Enforcement Layer
Contract: ECM_CONTRACT_v1.0
Status: FROZEN_IMMUTABLE

This module enforces:
- CVV validation
- Shadow metric application
- Softmax flatness handling
- ECM decision function
- Termination semantics
- Invariant preservation

No traversal logic. No SKG logic.
Pure enforcement.
"""

from dataclasses import dataclass
from typing import List, Dict, Any
import math
import time
import hashlib


# -----------------------------
# Canonical Verdict Vector
# -----------------------------

@dataclass(frozen=True)
class CVV:
    confidence: float
    contradiction: float
    entropy: float
    coverage: float
    falsified: bool
    skg_id: str

    def validate(self) -> None:
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError("CVV.confidence out of range")
        if not (0.0 <= self.contradiction <= 1.0):
            raise ValueError("CVV.contradiction out of range")
        if not (0.0 <= self.entropy <= 1.0):
            raise ValueError("CVV.entropy out of range")
        if not (0.0 <= self.coverage <= 1.0):
            raise ValueError("CVV.coverage out of range")

    def signature(self) -> str:
        payload = f"{self.confidence:.4f}|{self.contradiction:.4f}|{self.entropy:.4f}|{self.coverage:.4f}|{self.falsified}|{self.skg_id}"
        return hashlib.sha3_256(payload.encode("utf-8")).hexdigest()


# -----------------------------
# Softmax Utilities
# -----------------------------

def softmax(values: List[float]) -> List[float]:
    max_v = max(values)
    exp_vals = [math.exp(v - max_v) for v in values]
    total = sum(exp_vals)
    return [v / total for v in exp_vals]


def softmax_flatness(probabilities: List[float]) -> Dict[str, float]:
    entropy = -sum(p * math.log(p + 1e-12) for p in probabilities)
    return {
        "max_probability": max(probabilities),
        "entropy_of_distribution": entropy,
        "std_deviation": (sum((p - (1 / len(probabilities))) ** 2 for p in probabilities) / len(probabilities)) ** 0.5
    }


# -----------------------------
# ECM Decision Engine
# -----------------------------

class ECMRuntime:
    def __init__(self, cvvs: List[CVV], softmax_advisory: Dict[str, Any]):
        self.cvvs = cvvs
        self.softmax = softmax_advisory

        for cvv in self.cvvs:
            cvv.validate()

    # ---- Aggregate Helpers ----

    def avg(self, attr: str) -> float:
        return sum(getattr(c, attr) for c in self.cvvs) / len(self.cvvs)

    def any_falsified(self) -> bool:
        return any(c.falsified for c in self.cvvs)

    # ---- Core Decision ----

    def decide(self) -> Dict[str, Any]:
        if not self.cvvs:
            return self._verdict("SUSPEND", "No CVVs provided")

        # HARD REJECT
        if self.any_falsified():
            return self._verdict("REJECT", "Falsification detected")

        # NEW: Contradiction dominance (contract v1.0 §4.3.2)
        if len(self.cvvs) > 0:
            mean_contradiction = sum(cvv.contradiction for cvv in self.cvvs) / len(self.cvvs)
            max_contradiction = max(cvv.contradiction for cvv in self.cvvs)
            # Trigger on either high average OR any single highly contradictory view
            if mean_contradiction >= 0.60 or max_contradiction >= 0.70:
                return {
                    "status": "SUSPEND",
                    "rationale": "high_epistemic_contradiction",
                    "avg_confidence": round(self.avg("confidence"), 4) if self.cvvs else 0.0,
                    "avg_contradiction": round(mean_contradiction, 4),
                    "max_contradiction": round(max_contradiction, 4),
                    "avg_entropy": round(self.avg("entropy"), 4) if self.cvvs else 0.0,
                    "avg_coverage": round(self.avg("coverage"), 4) if self.cvvs else 0.0,
                    "cvv_signatures": [c.signature() for c in self.cvvs],
                    "timestamp_ms": int(time.time() * 1000),
                    "audit": {"invariants_checked": True}
                }

        # Single CVV handling
        if len(self.cvvs) == 1:
            cvv = self.cvvs[0]
            if cvv.confidence >= 0.85 and cvv.contradiction < 0.30 and not cvv.falsified:
                return {
                    "status": "CONDITIONAL",
                    "rationale": "single_strong_view",
                    "avg_confidence": round(cvv.confidence, 4),
                    "avg_contradiction": round(cvv.contradiction, 4),
                    "avg_entropy": round(cvv.entropy, 4),
                    "avg_coverage": round(cvv.coverage, 4),
                    "cvv_signatures": [cvv.signature()],
                    "timestamp_ms": int(time.time() * 1000),
                    "audit": {"invariants_checked": True}
                }
            else:
                return {
                    "status": "SUSPEND",
                    "rationale": "insufficient_consensus_or_strength",
                    "avg_confidence": round(cvv.confidence, 4),
                    "avg_contradiction": round(cvv.contradiction, 4),
                    "avg_entropy": round(cvv.entropy, 4),
                    "avg_coverage": round(cvv.coverage, 4),
                    "cvv_signatures": [cvv.signature()],
                    "timestamp_ms": int(time.time() * 1000),
                    "audit": {"invariants_checked": True}
                }

        # HIGH CONTRADICTION SUSPEND (for multiple CVVs - now redundant but kept for clarity)
        if self.avg("contradiction") > 0.60:
            return self._verdict("SUSPEND", "High internal contradiction")

        # SUSPEND: Byzantine + epistemic uncertainty
        if (
            self.softmax.get("reliability_tier") == "D"
            and self.avg("entropy") > 0.70
        ):
            return self._verdict("SUSPEND", "Byzantine + epistemic uncertainty")

        # REINTERPRETED
        if (
            self.avg("confidence") > 0.70
            and self.avg("coverage") > 0.75
            and self.softmax.get("epistemic_inevitability", 0.0) > 0.75
        ):
            return self._verdict("REINTERPRETED", "High confidence with divergence")

        # CONDITIONAL
        if any(c.confidence > 0.80 for c in self.cvvs) and self.avg("coverage") > 0.60:
            return self._verdict("CONDITIONAL", "Single worldview dominant")

        # ACCEPT
        if (
            self.avg("confidence") > 0.70
            and self.avg("contradiction") < 0.15
            and not self.any_falsified()
        ):
            return self._verdict("ACCEPT", "Consensus achieved")

        # REJECT
        if self.avg("confidence") < 0.50 or self.avg("coverage") < 0.40:
            return self._verdict("REJECT", "Insufficient confidence or coverage")

        # DEFAULT
        return self._verdict("SUSPEND", "Ambiguous; human escalation required")

    # ---- Verdict Packaging ----

    def _verdict(self, status: str, rationale: str) -> Dict[str, Any]:
        return {
            "status": status,
            "rationale": rationale,
            "avg_confidence": round(self.avg("confidence"), 4) if self.cvvs else 0.0,
            "avg_entropy": round(self.avg("entropy"), 4) if self.cvvs else 0.0,
            "avg_coverage": round(self.avg("coverage"), 4) if self.cvvs else 0.0,
            "cvv_signatures": [c.signature() for c in self.cvvs],
            "timestamp_ms": int(time.time() * 1000),
            "audit": {"invariants_checked": True}
        }


# -----------------------------
# Invariant Enforcement
# -----------------------------

def enforce_invariants(cvvs: List[CVV], softmax_probs: List[float]) -> None:
    if not math.isclose(sum(softmax_probs), 1.0, abs_tol=1e-6):
        raise RuntimeError("Invariant breach: softmax probabilities do not sum to 1")

    for cvv in cvvs:
        cvv.validate()
        if cvv.falsified and cvv.confidence > 0.0:
            raise RuntimeError("Invariant breach: falsified CVV has confidence > 0")


def enforce_seed_invariants(seed_result) -> None:
    """Check seed execution invariants - surgical confidence bounds"""
    if not hasattr(seed_result, 'confidence_score'):
        raise RuntimeError("Seed result missing confidence_score")

    if not (0.0 <= seed_result.confidence_score <= 1.0):
        raise RuntimeError("Seed confidence out of bounds - accumulation uncapped")