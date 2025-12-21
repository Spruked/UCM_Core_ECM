import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

import pytest
from ecm_runtime import CVV, ECMRuntime, softmax, enforce_invariants


# -----------------------------
# Helpers
# -----------------------------

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


# -----------------------------
# CVV Validation Tests
# -----------------------------

def test_cvv_validation_passes_within_range():
    make_cvv("a", 0.0, 0.0, 0.0, 0.0).validate()
    make_cvv("b", 1.0, 1.0, 1.0, 1.0).validate()
    make_cvv("c", 0.5, 0.3, 0.7, 0.9).validate()


def test_cvv_validation_fails_out_of_range_confidence_high():
    with pytest.raises(ValueError):
        make_cvv("bad", 1.1, 0.5, 0.5, 0.5).validate()


def test_cvv_validation_fails_out_of_range_confidence_low():
    with pytest.raises(ValueError):
        make_cvv("bad", -0.1, 0.5, 0.5, 0.5).validate()


def test_cvv_validation_fails_out_of_range_contradiction_high():
    with pytest.raises(ValueError):
        make_cvv("bad", 0.5, 1.1, 0.5, 0.5).validate()


def test_cvv_validation_fails_out_of_range_entropy_low():
    with pytest.raises(ValueError):
        make_cvv("bad", 0.5, 0.5, -0.01, 0.5).validate()


def test_cvv_validation_fails_out_of_range_coverage_high():
    with pytest.raises(ValueError):
        make_cvv("bad", 0.5, 0.5, 0.5, 1.1).validate()


def test_cvv_signature_is_deterministic_and_content_based():
    cvv1 = make_cvv("id", 0.42, 0.1, 0.3, 0.8, falsified=True)
    cvv2 = make_cvv("id", 0.42, 0.1, 0.3, 0.8, falsified=True)
    cvv_diff = make_cvv("id", 0.43, 0.1, 0.3, 0.8)
    assert cvv1.signature() == cvv2.signature()
    assert cvv1.signature() != cvv_diff.signature()


# -----------------------------
# Invariant Enforcement Tests
# -----------------------------

def test_enforce_invariants_accepts_near_perfect_sum():
    probs = softmax([0.0, 1.0, 2.0])
    enforce_invariants([make_cvv("a", 0.7, 0.1, 0.3, 0.8)], probs)  # should pass


def test_enforce_invariants_rejects_bad_sum():
    with pytest.raises(RuntimeError):
        enforce_invariants(
            [make_cvv("a", 0.7, 0.1, 0.3, 0.8)],
            [0.3, 0.3, 0.3],  # sum = 0.9
        )


# -----------------------------
# ECM Decision Path Tests (strictly isolated)
# -----------------------------

def test_hard_reject_any_falsified():
    cvvs = [
        make_cvv("a", 0.99, 0.0, 0.0, 1.0, falsified=True),
        make_cvv("b", 0.99, 0.0, 0.0, 1.0),
    ]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] == "REJECT"


def test_suspend_requires_both_low_reliability_and_high_entropy():
    cvvs = [
        make_cvv("a", 0.7, 0.1, 0.85, 0.7),
        make_cvv("b", 0.7, 0.1, 0.85, 0.7),
    ]
    ecm = ECMRuntime(cvvs, advisory(reliability="D"))
    assert ecm.decide()["status"] == "SUSPEND"


def test_low_reliability_but_low_entropy_does_not_suspend():
    cvvs = [
        make_cvv("a", 0.85, 0.1, 0.3, 0.8),
        make_cvv("b", 0.85, 0.1, 0.3, 0.8),
    ]
    ecm = ECMRuntime(cvvs, advisory(reliability="D"))
    assert ecm.decide()["status"] != "SUSPEND"  # falls to other paths (likely ACCEPT or default)


def test_reinterpreted_requires_high_inevitability_and_multiple_aligned_views():
    cvvs = [
        make_cvv("a", 0.75, 0.15, 0.4, 0.8),
        make_cvv("b", 0.74, 0.14, 0.4, 0.8),
        make_cvv("c", 0.76, 0.13, 0.4, 0.8),
        make_cvv("d", 0.73, 0.16, 0.4, 0.8),
    ]
    ecm = ECMRuntime(cvvs, advisory(inevitability=0.85))
    assert ecm.decide()["status"] == "REINTERPRETED"

    # Counter: drop inevitability
    ecm_low = ECMRuntime(cvvs, advisory(inevitability=0.7))
    assert ecm_low.decide()["status"] != "REINTERPRETED"


def test_conditional_accept_one_dominant_strong_view():
    cvvs = [
        make_cvv("strong", 0.88, 0.1, 0.4, 0.8),
        make_cvv("weak1", 0.52, 0.3, 0.6, 0.6),
        make_cvv("weak2", 0.48, 0.3, 0.6, 0.6),
    ]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] == "CONDITIONAL"


def test_accept_consensus_high_confidence_low_variance():
    cvvs = [
        make_cvv("a", 0.78, 0.08, 0.25, 0.85),
        make_cvv("b", 0.76, 0.09, 0.26, 0.85),
        make_cvv("c", 0.77, 0.07, 0.24, 0.85),
    ]
    ecm = ECMRuntime(cvvs, advisory(inevitability=0.7))  # low inevitability to avoid REINTERPRETED
    assert ecm.decide()["status"] == "ACCEPT"


def test_reject_on_collectively_low_confidence():
    cvvs = [
        make_cvv("a", 0.45, 0.2, 0.6, 0.5),
        make_cvv("b", 0.44, 0.25, 0.65, 0.5),
    ]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] == "REJECT"


def test_default_suspend_fallback():
    cvvs = [
        make_cvv("a", 0.65, 0.2, 0.5, 0.6),
        make_cvv("b", 0.64, 0.22, 0.52, 0.6),
    ]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] == "SUSPEND"


# -----------------------------
# High Contradiction Dedicated Tests
# -----------------------------

def test_high_contradiction_triggers_suspend_even_with_high_confidence():
    """High contradiction overrides confidence → forces SUSPEND"""
    cvvs = [
        make_cvv("a", 0.85, 0.65, 0.4, 0.8),   # high confidence, very high contradiction
        make_cvv("b", 0.82, 0.70, 0.45, 0.8),
        make_cvv("c", 0.80, 0.68, 0.42, 0.8),
    ]
    ecm = ECMRuntime(cvvs, advisory(reliability="A"))  # strong advisory
    verdict = ecm.decide()
    assert verdict["status"] == "SUSPEND"
    assert "contradiction" in verdict.get("rationale", "").lower()  # optional: check rationale if exposed


def test_extreme_contradiction_dominates_over_everything():
    """Near-max contradiction → SUSPEND regardless of other signals"""
    cvvs = [
        make_cvv("a", 0.95, 0.95, 0.1, 0.9),   # almost certain but almost fully contradictory
        make_cvv("b", 0.94, 0.96, 0.1, 0.9),
    ]
    ecm = ECMRuntime(cvvs, advisory(inevitability=0.9, reliability="A"))
    assert ecm.decide()["status"] == "SUSPEND"


def test_contradiction_threshold_boundary():
    """Test just below vs just above expected contradiction trigger threshold"""
    # Assuming internal threshold around ~0.6 for strong suspend push (adjust if spec differs)
    cvvs_low = [
        make_cvv("a", 0.80, 0.59, 0.3, 0.8),
        make_cvv("b", 0.81, 0.58, 0.3, 0.8),
    ]
    ecm_low = ECMRuntime(cvvs_low, advisory())
    # May go to ACCEPT or CONDITIONAL depending on other rules
    assert ecm_low.decide()["status"] != "SUSPEND"

    cvvs_high = [
        make_cvv("a", 0.80, 0.61, 0.3, 0.8),
        make_cvv("b", 0.81, 0.62, 0.3, 0.8),
    ]
    ecm_high = ECMRuntime(cvvs_high, advisory())
    assert ecm_high.decide()["status"] == "SUSPEND"


def test_contradiction_competes_with_falsification():
    """Falsification is absolute — must override even extreme contradiction"""
    cvvs = [
        make_cvv("a", 0.90, 0.99, 0.8, 0.7, falsified=True),  # falsified + max contradiction
        make_cvv("b", 0.50, 0.99, 0.9, 0.5),
    ]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] == "REJECT"  # falsification wins


def test_contradiction_vs_reinterpreted():
    """High contradiction blocks REINTERPRETED path"""
    cvvs = [
        make_cvv("a", 0.76, 0.65, 0.4, 0.8),
        make_cvv("b", 0.75, 0.67, 0.4, 0.8),
        make_cvv("c", 0.77, 0.64, 0.4, 0.8),
        make_cvv("d", 0.74, 0.66, 0.4, 0.8),
    ]
    ecm = ECMRuntime(cvvs, advisory(inevitability=0.9))  # would normally REINTERPRETED
    assert ecm.decide()["status"] == "SUSPEND"
    assert ecm.decide()["status"] != "REINTERPRETED"


def test_single_high_contradiction_view():
    """Even one highly contradictory view can poison the pool"""
    cvvs = [
        make_cvv("strong", 0.90, 0.10, 0.2, 0.9),     # clean strong view
        make_cvv("poison", 0.85, 0.80, 0.7, 0.7),     # highly contradictory
    ]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] == "SUSPEND"


# -----------------------------
# Edge Cases
# -----------------------------

def test_empty_cvvs_must_suspend():
    ecm = ECMRuntime([], advisory())
    assert ecm.decide()["status"] == "SUSPEND"


def test_single_cvv_high_confidence_goes_conditional_or_accept():
    cvvs = [make_cvv("solo", 0.90, 0.05, 0.2, 0.9)]
    ecm = ECMRuntime(cvvs, advisory())
    assert ecm.decide()["status"] in {"CONDITIONAL", "ACCEPT"}


def test_invariants_are_enforced():
    cvvs = [make_cvv("a", 0.7, 0.1, 0.3, 0.8)]
    ecm = ECMRuntime(cvvs, advisory())
    verdict = ecm.decide()
    assert "invariants_checked" in verdict["audit"]