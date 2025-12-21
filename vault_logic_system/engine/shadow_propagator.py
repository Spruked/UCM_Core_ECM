"""
ShadowPropagator - Cross-SKG metric influence without logic contamination
ECM Contract v1.0 compliant - Metrics only, no reasoning transfer
"""

import time
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ShadowTrigger(Enum):
    HIGH_CONTRADICTION = "high_contradiction"
    CONFIDENCE_DELTA = "confidence_delta"
    ENTROPY_SPIKE = "entropy_spike"

@dataclass
class ShadowArtifact:
    """Lightweight metadata for cross-SKG awareness"""
    shadow_id: str
    skg_origin: str
    timestamp_ms: int
    node_location: str
    evaluation_target: str
    trigger_type: ShadowTrigger

    # Non-binding metadata (metrics only)
    confidence_delta: float
    contradiction_flag: bool
    entropy_marker: float

    # Integrity seals
    skg_hash: str
    invocation_count: int
    ttl_ms: int = 5000

    def is_expired(self, current_time: int) -> bool:
        """Check if shadow has exceeded TTL"""
        return (current_time - self.timestamp_ms) > self.ttl_ms

    def get_adjustment_delta(self) -> float:
        """Calculate metric adjustment delta (capped)"""
        base_delta = 0.0

        if self.trigger_type == ShadowTrigger.HIGH_CONTRADICTION:
            base_delta = -0.15 if self.contradiction_flag else 0.0
        elif self.trigger_type == ShadowTrigger.CONFIDENCE_DELTA:
            base_delta = min(self.confidence_delta * 0.3, 0.10)  # Dampened influence
        elif self.trigger_type == ShadowTrigger.ENTROPY_SPIKE:
            base_delta = -min(self.entropy_marker * 0.2, 0.08)  # Entropy reduction

        # Apply cumulative cap
        return max(-0.25, min(0.25, base_delta))

class ShadowPropagator:
    """
    Manages shadow propagation between SKGs with strict constraints:
    - TTL = 5000ms
    - Max 3 adjustments per node
    - Cumulative delta cap = 0.25
    - No logic contamination
    """

    def __init__(self):
        self.active_skg: Optional[str] = None
        self.active_shadows: Dict[str, List[ShadowArtifact]] = {}
        self.node_adjustment_counts: Dict[str, int] = {}
        self.node_cumulative_deltas: Dict[str, float] = {}

    def emit_shadow(self, skg_origin: str, node_location: str, evaluation_target: str,
                   mini_skg_result: Any, trigger_conditions: Dict[str, Any]) -> Optional[ShadowArtifact]:
        """
        Emit shadow artifact if trigger conditions met
        Returns shadow if emitted, None otherwise
        """

        # Check trigger conditions
        trigger_type = self._evaluate_triggers(mini_skg_result, trigger_conditions)
        if not trigger_type:
            return None

        # Generate shadow ID
        timestamp = int(time.time() * 1000)
        shadow_content = f"{skg_origin}{node_location}{timestamp}"
        shadow_id = hashlib.sha3_256(shadow_content.encode()).hexdigest()[:16]

        # Create shadow artifact
        shadow = ShadowArtifact(
            shadow_id=shadow_id,
            skg_origin=skg_origin,
            timestamp_ms=timestamp,
            node_location=node_location,
            evaluation_target=evaluation_target,
            trigger_type=trigger_type,
            confidence_delta=mini_skg_result.confidence_score,
            contradiction_flag=len(mini_skg_result.contradiction_flags) > 0,
            entropy_marker=self._calculate_entropy_marker(mini_skg_result),
            skg_hash=self._generate_skg_hash(skg_origin),
            invocation_count=len(mini_skg_result.rule_results)
        )

        # Store shadow for propagation
        target_key = f"{evaluation_target}_{node_location}"
        if target_key not in self.active_shadows:
            self.active_shadows[target_key] = []
        self.active_shadows[target_key].append(shadow)

        return shadow

    def apply_shadows_to_metrics(self, target_skg: str, node_location: str,
                               base_metrics: Dict[str, float]) -> Dict[str, float]:
        """
        Apply shadow adjustments to target SKG metrics
        Returns adjusted metrics dict
        """

        target_key = f"{target_skg}_{node_location}"
        if target_key not in self.active_shadows:
            return base_metrics

        # Clean expired shadows
        current_time = int(time.time() * 1000)
        active_shadows = [s for s in self.active_shadows[target_key] if not s.is_expired(current_time)]

        # Update active shadows
        self.active_shadows[target_key] = active_shadows

        if not active_shadows:
            return base_metrics

        # Check adjustment limits
        adjustment_key = f"{target_skg}_{node_location}"
        current_count = self.node_adjustment_counts.get(adjustment_key, 0)
        current_cumulative = self.node_cumulative_deltas.get(adjustment_key, 0.0)

        if current_count >= 3:  # Max 3 adjustments per node
            return base_metrics

        # Calculate total adjustment
        total_adjustment = 0.0
        applied_shadows = []

        for shadow in active_shadows:
            if shadow.skg_origin != target_skg:  # Don't apply self-shadows
                delta = shadow.get_adjustment_delta()
                total_adjustment += delta
                applied_shadows.append(shadow)

        # Apply cumulative cap
        total_adjustment = max(-0.25, min(0.25, total_adjustment))

        # Update tracking
        self.node_adjustment_counts[adjustment_key] = current_count + len(applied_shadows)
        self.node_cumulative_deltas[adjustment_key] = current_cumulative + total_adjustment

        # Apply adjustments to metrics
        adjusted_metrics = base_metrics.copy()

        # Adjust confidence (primary target)
        if 'confidence' in adjusted_metrics:
            adjusted_metrics['confidence'] = max(0.0, min(1.0,
                adjusted_metrics['confidence'] + total_adjustment))

        # Adjust entropy (secondary target)
        if 'entropy' in adjusted_metrics:
            # Entropy moves opposite to confidence adjustments
            entropy_adjustment = -total_adjustment * 0.5
            adjusted_metrics['entropy'] = max(0.0, min(1.0,
                adjusted_metrics['entropy'] + entropy_adjustment))

        # Adjust contradiction score (tertiary target)
        if 'contradiction' in adjusted_metrics:
            contradiction_adjustment = total_adjustment * 0.3
            adjusted_metrics['contradiction'] = max(0.0, min(1.0,
                adjusted_metrics['contradiction'] + contradiction_adjustment))

        return adjusted_metrics

    def _evaluate_triggers(self, mini_skg_result: Any, trigger_conditions: Dict[str, Any]) -> Optional[ShadowTrigger]:
        """Evaluate if shadow emission conditions are met"""

        # High contradiction trigger
        if len(mini_skg_result.contradiction_flags) > trigger_conditions.get('contradiction_threshold', 0):
            return ShadowTrigger.HIGH_CONTRADICTION

        # Confidence delta trigger
        confidence_delta_threshold = trigger_conditions.get('confidence_delta_threshold', 0.2)
        if mini_skg_result.confidence_score >= confidence_delta_threshold:
            return ShadowTrigger.CONFIDENCE_DELTA

        # Entropy spike trigger
        entropy_threshold = trigger_conditions.get('entropy_spike_threshold', 0.8)
        entropy_marker = self._calculate_entropy_marker(mini_skg_result)
        if entropy_marker >= entropy_threshold:
            return ShadowTrigger.ENTROPY_SPIKE

        return None

    def _calculate_entropy_marker(self, mini_skg_result: Any) -> float:
        """Calculate entropy marker from MiniSKG result"""
        # Simple entropy calculation based on result variance
        if not mini_skg_result.rule_results:
            return 0.0

        deltas = [result.get('confidence_delta', 0.0)
                 for result in mini_skg_result.rule_results.values()]
        if not deltas:
            return 0.0

        mean_delta = sum(deltas) / len(deltas)
        variance = sum((d - mean_delta) ** 2 for d in deltas) / len(deltas)
        return min(1.0, variance * 10)  # Scale and cap

    def _generate_skg_hash(self, skg_origin: str) -> str:
        """Generate integrity hash for SKG origin"""
        return hashlib.sha3_256(skg_origin.encode()).hexdigest()[:16]

    def get_shadow_stats(self) -> Dict[str, Any]:
        """Get statistics about active shadows"""
        total_shadows = sum(len(shadows) for shadows in self.active_shadows.values())
        expired_count = 0
        current_time = int(time.time() * 1000)

        for shadows in self.active_shadows.values():
            expired_count += sum(1 for s in shadows if s.is_expired(current_time))

        return {
            'total_active_shadows': total_shadows,
            'expired_shadows': expired_count,
            'active_nodes': len(self.active_shadows),
            'adjustment_counts': dict(self.node_adjustment_counts),
            'cumulative_deltas': dict(self.node_cumulative_deltas)
        }

    def set_active_skg(self, skg_id: str) -> None:
        """Set the currently active SKG for shadow emission filtering"""
        self.active_skg = skg_id

    def get_resonance_markers(self) -> Dict[str, Any]:
        """Get resonance markers from shadow interactions"""
        current_time = int(time.time() * 1000)

        # Count shadows per node within TTL
        node_shadow_counts = {}
        active_shadow_count = 0

        for node_key, shadows in self.active_shadows.items():
            active_shadows = [s for s in shadows if not s.is_expired(current_time)]
            if active_shadows:
                node_shadow_counts[node_key] = len(active_shadows)
                active_shadow_count += len(active_shadows)

        # Generate resonance markers (simplified)
        resonance_events = []
        for node_key, count in node_shadow_counts.items():
            if count >= 2:  # Trigger condition: ≥2 shadows in same node
                skgs_involved = list(set(s.skg_origin for s in self.active_shadows[node_key]
                                       if not s.is_expired(current_time)))
                confidence_shifts = [s.confidence_delta for s in self.active_shadows[node_key]
                                   if not s.is_expired(current_time)][:2]  # Last 2

                resonance_events.append({
                    "node": node_key,
                    "skgs_involved": skgs_involved,
                    "confidence_shifts": confidence_shifts,
                    "timestamp": current_time
                })

        return {
            "total_resonance_events": len(resonance_events),
            "active_shadows": active_shadow_count,
            "node_shadow_distribution": node_shadow_counts,
            "resonance_events": resonance_events
        }