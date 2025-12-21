"""
MiniSKGExecutor - Surgical confidence-capped seed execution
ECM Contract v1.0 compliant - No learning, no memory, just bounds enforcement
"""

from typing import Dict, List, Any, Tuple
from dataclasses import dataclass
import json


@dataclass
class MiniSKGResult:
    """Result from mini-SKG execution with confidence capping"""
    confidence_score: float
    rule_results: Dict[str, Any]
    contradiction_flags: List[str]


class MiniSKGExecutor:
    """Surgical mini-SKG executor with confidence accumulation capping"""

    def __init__(self, seed_json: Dict):
        self.seed = seed_json
        self.traversal_depth = 0
        self.rule_results = {}
        self.contradiction_flags = []
        self.confidence_accumulator = 0.0  # Track accumulated deltas
        self.base_confidence = seed_json.get("initial_confidence", 0.5)  # Seed baseline

    def traverse(self, params: Dict, context: str) -> MiniSKGResult:
        """Execute 3-5 node mini-SKG with confidence capping"""

        # Reset per traversal (no memory)
        self.confidence_accumulator = 0.0
        self.rule_results = {}
        self.contradiction_flags = []
        self.traversal_depth = 0

        # Execute each node in sequence
        concept_nodes = self.seed.get("entries", [])
        for node in concept_nodes[:5]:  # Cap at 5 nodes max
            if self.traversal_depth >= 5:
                break

            result = self._execute_node(node, params, context)
            self.rule_results[node["id"]] = result

            # Accumulate confidence deltas (surgical, no memory)
            if "confidence_delta" in result:
                self.confidence_accumulator += result["confidence_delta"]

            if result.get("contradiction_detected", False):
                self.contradiction_flags.append(node["id"])

            self.traversal_depth += 1

        # Cap accumulated confidence (matches ECM gradient semantics)
        raw_confidence = self.base_confidence + self.confidence_accumulator
        capped_confidence = max(0.0, min(1.0, raw_confidence))

        return MiniSKGResult(
            confidence_score=capped_confidence,
            rule_results=self.rule_results,
            contradiction_flags=self.contradiction_flags
        )

    def _execute_node(self, node: Dict, params: Dict, context: str) -> Dict[str, Any]:
        """Execute single node logic with intelligent evaluation"""
        node_id = node.get("id", "")
        term = node.get("term", "")
        node_type = node.get("type", "")
        definition = node.get("definition", "")
        value = node.get("value", {})

        # Initialize execution result
        confidence_delta = 0.0
        contradiction_detected = False
        evaluation_notes = []

        # Evaluate based on node type and content
        if node_type == "inference_rule":
            confidence_delta, contradiction_detected, notes = self._evaluate_inference_rule(
                node, params, context
            )
            evaluation_notes.extend(notes)

        elif node_type == "method":
            confidence_delta, contradiction_detected, notes = self._evaluate_method(
                node, params, context
            )
            evaluation_notes.extend(notes)

        elif node_type == "concept":
            confidence_delta, contradiction_detected, notes = self._evaluate_concept(
                node, params, context
            )
            evaluation_notes.extend(notes)

        else:
            # Default evaluation for unknown types
            confidence_delta = 0.05  # Small boost for recognized structure
            evaluation_notes.append(f"Unknown node type '{node_type}' - minimal confidence boost")

        # Check for contradictions in content
        if self._detect_contradiction(term, definition, context):
            contradiction_detected = True
            confidence_delta = max(confidence_delta - 0.3, -0.5)  # Significant penalty
            evaluation_notes.append("Contradiction detected in node content")

        return {
            "node_id": node_id,
            "term": term,
            "type": node_type,
            "confidence_delta": confidence_delta,
            "contradiction_detected": contradiction_detected,
            "evaluation_context": context,
            "params_used": list(params.keys()),
            "evaluation_notes": evaluation_notes
        }

    def _evaluate_inference_rule(self, node: Dict, params: Dict, context: str) -> Tuple[float, bool, List[str]]:
        """Evaluate an inference rule node"""
        term = node.get("term", "").lower()
        value = node.get("value", {})
        certainty = value.get("certainty", 0.8)  # Default certainty for inference rules

        confidence_delta = 0.0
        contradiction_detected = False
        notes = []

        # Evaluate specific inference rules
        if "modus_ponens" in term:
            confidence_delta = certainty * 0.15  # Strong boost for modus ponens
            notes.append("Applied modus ponens inference rule")
        elif "modus_tollens" in term:
            confidence_delta = certainty * 0.12  # Good boost for modus tollens
            notes.append("Applied modus tollens inference rule")
        elif "syllogism" in term:
            confidence_delta = certainty * 0.10  # Moderate boost for syllogism
            notes.append("Applied syllogistic reasoning")
        else:
            confidence_delta = certainty * 0.08  # Default boost for other inference rules
            notes.append(f"Applied general inference rule: {node.get('term', 'unknown')}")

        return confidence_delta, contradiction_detected, notes

    def _evaluate_method(self, node: Dict, params: Dict, context: str) -> Tuple[float, bool, List[str]]:
        """Evaluate a method node"""
        term = node.get("term", "").lower()
        definition = node.get("definition", "")

        confidence_delta = 0.0
        contradiction_detected = False
        notes = []

        # Evaluate reasoning methods
        if "deductive" in term:
            confidence_delta = 0.12  # Boost for deductive methods
            notes.append("Deductive reasoning method recognized")
        elif "inductive" in term:
            confidence_delta = 0.08  # Moderate boost for inductive methods
            notes.append("Inductive reasoning method recognized")
        elif "logical" in definition.lower():
            confidence_delta = 0.10  # Boost for logical methods
            notes.append("Logical method framework applied")
        else:
            confidence_delta = 0.06  # Default boost for methods
            notes.append(f"General reasoning method: {node.get('term', 'unknown')}")

        return confidence_delta, contradiction_detected, notes

    def _evaluate_concept(self, node: Dict, params: Dict, context: str) -> Tuple[float, bool, List[str]]:
        """Evaluate a concept node"""
        confidence_delta = 0.05  # Base boost for concepts
        contradiction_detected = False
        notes = []

        # Check if concept is relevant to context
        term = node.get("term", "").lower()
        context_lower = context.lower()

        if term in context_lower:
            confidence_delta += 0.05  # Additional boost for contextual relevance
            notes.append(f"Concept '{node.get('term', '')}' is contextually relevant")
        else:
            notes.append(f"Concept '{node.get('term', '')}' evaluated but not directly relevant")

        return confidence_delta, contradiction_detected, notes

    def _detect_contradiction(self, term: str, definition: str, context: str) -> bool:
        """Detect contradictions in node content"""
        content = f"{term} {definition} {context}".lower()

        contradiction_indicators = [
            "contradiction", "paradox", "inconsistent", "mutually exclusive",
            "cannot be both", "impossible", "false premise", "invalid conclusion"
        ]

        for indicator in contradiction_indicators:
            if indicator in content:
                return True

        return False