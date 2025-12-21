#!/usr/bin/env python3
"""
Debug script for ECM decision logic
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from ecm_runtime import CVV, ECMRuntime

def make_cvv(
    skg_id: str,
    confidence: float,
    contradiction: float,
    entropy: float,
    coverage: float,
    falsified: bool = False,
):
    return CVV(
        skg_id=skg_id,
        confidence=confidence,
        contradiction=contradiction,
        entropy=entropy,
        coverage=coverage,
        falsified=falsified,
    )

def advisory(reliability: str = "A", inevitability: float = 0.8):
    return {
        "reliability_tier": reliability,
        "epistemic_inevitability": inevitability,
    }

# Test the failing cases
print("=== Debugging failing tests ===")

# Test 1: high contradiction should trigger suspend
print("\n1. High contradiction test:")
cvvs = [
    make_cvv("a", 0.85, 0.65, 0.4, 0.8),
    make_cvv("b", 0.82, 0.70, 0.45, 0.8),
    make_cvv("c", 0.80, 0.68, 0.42, 0.8),
]
avg_contradiction = sum(c.contradiction for c in cvvs) / len(cvvs)
print(f"Average contradiction: {avg_contradiction}")
ecm = ECMRuntime(cvvs, advisory(reliability="A"))
result = ecm.decide()
print(f"Result: {result}")

# Test 2: single high contradiction view
print("\n2. Single high contradiction view:")
cvvs = [
    make_cvv("strong", 0.90, 0.10, 0.2, 0.9),
    make_cvv("poison", 0.85, 0.80, 0.7, 0.7),
]
avg_contradiction = sum(c.contradiction for c in cvvs) / len(cvvs)
print(f"Average contradiction: {avg_contradiction}")
ecm = ECMRuntime(cvvs, advisory())
result = ecm.decide()
print(f"Result: {result}")

# Test 3: single CVV high confidence
print("\n3. Single CVV high confidence:")
cvvs = [make_cvv("solo", 0.90, 0.05, 0.2, 0.9)]
ecm = ECMRuntime(cvvs, advisory())
result = ecm.decide()
print(f"Result: {result}")