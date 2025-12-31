# main.py - Integration orchestrator

# main.py - Integration orchestrator

import json
import os
import math
import random
import time
from typing import Dict, List, Any

def softmax(scores):
    exp_scores = [math.exp(s) for s in scores]
    total = sum(exp_scores)
    return [e / total for e in exp_scores]

def load_skg(path):
    """Stub: Load SKG from JSON file"""
    with open(path, 'r') as f:
        return json.load(f)

def load_test_seed_vault(path):
    """Stub: Load test seed vault"""
    return {
        "claim_id": "test_claim_001",
        "claim_type": "moral_reasoning"
    }  # Stub

class SpaceFieldNS:
    def __init__(self):
        self.geometry = None
    
    def load_geometry(self, path):
        with open(path, 'r') as f:
            self.geometry = json.load(f)
    
    def get_entry_node(self, claim_type):
        return "SPACE_247"  # Stub
    
    def get_shadows_at(self, node):
        return []  # Stub
    
    def get_adjacent(self, node):
        # Stub: return adjacent nodes based on geometry
        return ["SPACE_248", "SPACE_249", "SPACE_250"]  # Example adjacent nodes

class SeedInvocationLayer:
    def __init__(self, logic_seed_dir, reference_seed_dir):
        self.logic_seed_dir = logic_seed_dir
        self.reference_seed_dir = reference_seed_dir
        
        # Initialize shadow propagator
        from vault_logic_system.engine.shadow_propagator import ShadowPropagator
        self.shadow_propagator = ShadowPropagator()
        
        # Shadow trigger conditions
        self.shadow_triggers = {
            'contradiction_threshold': 1,  # High contradiction if > 1 contradiction flags
            'confidence_delta_threshold': 0.15,  # Emit if confidence >= 0.15
            'entropy_spike_threshold': 0.7  # Emit if entropy marker >= 0.7
        }

    def invoke_logic_seed(self, seed_name, params, calling_skg):
        """Execute logic seed using MiniSKGExecutor with confidence capping"""
        try:
            # Load seed from master vault
            seed_path = os.path.join(self.logic_seed_dir, f"{seed_name}.json")
            with open(seed_path, 'r') as f:
                seed_json = json.load(f)

            # Execute with MiniSKGExecutor
            from vault_logic_system.engine.mini_skg_executor import MiniSKGExecutor
            executor = MiniSKGExecutor(seed_json)
            result = executor.traverse(params, calling_skg)

            # Enforce invariants
            from ecm_runtime import enforce_seed_invariants
            enforce_seed_invariants(result)

            # Emit shadow if trigger conditions met
            evaluation_target = params.get('claim_id', 'unknown_claim')
            node_location = params.get('node_id', 'unknown_node')
            
            shadow = self.shadow_propagator.emit_shadow(
                skg_origin=calling_skg,
                node_location=node_location,
                evaluation_target=evaluation_target,
                mini_skg_result=result,
                trigger_conditions=self.shadow_triggers
            )

            return {
                "fragment": result.rule_results,
                "confidence": result.confidence_score,
                "contradictions": result.contradiction_flags,
                "shadow_emitted": shadow is not None,
                "shadow_id": shadow.shadow_id if shadow else None
            }
        except FileNotFoundError:
            # Fallback to stub if seed not found
            return {"fragment": "logic_result", "confidence": 0.8}
        except Exception as e:
            # Error handling - return low confidence
            return {"fragment": f"error: {str(e)}", "confidence": 0.1}
    
    def apply_shadow_adjustments(self, target_skg: str, node_location: str, base_metrics: Dict[str, float]) -> Dict[str, float]:
        """Apply shadow adjustments to target SKG metrics"""
        return self.shadow_propagator.apply_shadows_to_metrics(target_skg, node_location, base_metrics)
    
    def get_shadow_stats(self) -> Dict[str, Any]:
        """Get shadow propagation statistics"""
        return self.shadow_propagator.get_shadow_stats()
    
    def query_reference_seed(self, seed_name, query_params):
        return {"constraints": [], "confidence": 0.9}  # Stub

class ContextShadowManager:
    def add_shadow(self, node, shadow):
        pass  # Stub

class FalsificationEvent:
    def __init__(self, type, delta):
        self.type = type
        self.delta = delta

class Beam:
    def __init__(self, skg, current_node, seed_vault, invocation_layer, space_field):
        self.skg = skg
        self.current_node = current_node
        self.seed_vault = seed_vault
        self.invocation_layer = invocation_layer
        self.space_field = space_field
        self.entropy = 0.5  # Stub
        self.trajectory = []  # Stub
        self.path = []  # Stub
        self.consistency = type('obj', (object,), {'decay_rate': 0.1})()  # Stub
        self.falsification_engine = FalsificationEngine(self)  # Add this
        
        # Shadow-affected metrics
        self.metrics = {
            'confidence': 0.5,
            'entropy': 0.5,
            'contradiction': 0.0
        }
    
    def get_context(self):
        return {"context": "data"}  # Stub
    
    def get_query_params(self):
        return {"query": "params"}  # Stub
    
    def integrate_seed_fragment(self, fragment):
        pass  # Stub
    
    def adjust_confidence(self, delta):
        pass  # Stub
    
    def process_cross_path_events(self, shadows):
        pass  # Stub
    
    def process_cross_path(self, shadows):
        pass  # Stub
    
    def adjust_from_seed_fragment(self, fragment):
        pass  # Stub
    
    def apply_constraints(self, constraints):
        pass  # Stub
    
    def evaluate_rules(self, concept_domain):
        # Stub: evaluate how well SKG rules apply to this concept domain
        return 0.8  # Placeholder confidence
    
    def calculate_semantic_distance(self, node):
        # Stub: calculate semantic fit between current path and node
        return 0.7  # Placeholder
    
    def check_shadow_resonance(self, node):
        # Stub: check for resonance with cross-path shadows
        return 1.0  # No bonus
    
    def select_next_node(self):
        # Evaluate each adjacent node against SKG rules
        candidates = self.space_field.get_adjacent(self.current_node)
        if not candidates:
            return None  # No adjacent nodes
        
        scores = []
        for node in candidates:
            rule_compliance = self.evaluate_rules(node)  # Assuming node has concept_domain
            semantic_fit = self.calculate_semantic_distance(node)
            shadow_bonus = self.check_shadow_resonance(node)
            scores.append(rule_compliance * semantic_fit * shadow_bonus)
        
        # Softmax over scores
        probabilities = softmax(scores)
        selected_index = random.choices(range(len(candidates)), weights=probabilities)[0]
        return candidates[selected_index]
    
    def traverse_to(self, next_node):
        self.current_node = next_node
        self.trajectory.append(next_node)
    
    def generate_shadow(self):
        return {"shadow": "data"}  # Stub
    
    def compile_verdict(self, trajectory=None):
        return {
            "verdict_status": "ACCEPTED",
            "confidence": 0.8,
            "internal_consistency": 0.85,
            "reasoning_path": ["SPACE_247", "SPACE_248"],
            "seed_vault_coverage": 0.75
        }  # Stub

def structural_convergence(seed_vault_data, activated_skgs):
    """
    Orchestrates parallel traversal of SKGs through shared space field
    """
    # 1. Initialize space field geometry
    space_field = SpaceFieldNS()
    space_field.load_geometry(seed_vault_data['claim_domain'])
    
    # 2. Deploy SKG beams in parallel
    active_beams = []
    for skg in activated_skgs:
        beam = Beam(
            skg=skg,
            entry_node=space_field.get_entry_node(seed_vault_data['claim_type']),
            seed_vault=seed_vault_data
        )
        active_beams.append(beam)
        space_field.register_beam(beam)
    
    # 3. Traverse until termination conditions
    while not space_field.all_beams_terminated():
        for beam in active_beams:
            # Execute one traversal step
            current_node = beam.current_node
            
            # Check for cross-path events
            shadows = space_field.get_context_shadows(current_node)
            if shadows:
                beam.process_cross_path(shadows)
            
            # Invoke logic seeds if node requires
            if current_node.requires_seed_invocation:
                fragment = invocation_layer.invoke_logic_seed(
                    seed_name=current_node.seed_name,
                    params=current_node.seed_params,
                    calling_skg=beam.skg.name
                )
                beam.adjust_from_seed_fragment(fragment)
            
            # Query reference seeds for constraints
            if current_node.requires_reference_query:
                constraints = invocation_layer.query_reference_seed(
                    seed_name=current_node.reference_name,
                    query_params=current_node.query_params
                )
                beam.apply_constraints(constraints)
            
            # Assess falsification
            falsification = beam.check_falsification()
            beam.confidence.adjust(falsification.delta)
            
            # Move to next node
            next_node = beam.select_next_node()
            beam.traverse_to(next_node)
            
            # Leave context shadow
            space_field.add_context_shadow(
                node=current_node,
                shadow=beam.generate_shadow()
            )
    
    # 4. Collect final verdicts
    verdicts = {}
    for beam in active_beams:
        verdicts[beam.skg.name] = beam.compile_verdict()
    
    return verdicts

class Beam:
    def check_falsification(self):
        """Evaluate if current trajectory is being falsified"""
        # Check against reference seed constraints
        constraints = self.current_node.get_active_constraints()
        for constraint in constraints:
            if self.trajectory.violates(constraint):
                return FalsificationEvent(type="CONSTRAINT_VIOLATION", delta=-0.20)
        
        # Check internal consistency decay
        if self.consistency.decay_rate > 0.15:
            return FalsificationEvent(type="CONSISTENCY_DECAY", delta=-0.10)
        
        return FalsificationEvent(type="NONE", delta=0.0)

class FalsificationEngine:
    def __init__(self, beam):
        self.beam = beam
        self.violation_history = []
    
    def evaluate(self, node):
        """Returns falsification score and confidence adjustment"""
        score = 0.0
        deltas = []
        
        # Type 1: Reference Constraint Violation
        violations = self._check_constraints(node)
        if violations:
            score += 0.40
            deltas.append(-0.15 * len(violations))
        
        # Type 2: Internal Contradiction Detection
        contradictions = self._check_contradictions(node)
        if contradictions:
            score += 0.30
            deltas.append(-0.10 * contradictions)
        
        # Type 3: Path Irreversibility
        if self._is_path_irreversible(node):
            score += 0.20
            deltas.append(-0.05)
        
        # Type 4: Entropy Cap Breach
        if self.beam.entropy > 0.85:
            score += 0.10
            deltas.append(-0.08)
        
        return {
            "falsification_score": min(score, 1.0),
            "confidence_delta": sum(deltas),
            "violation_types": self._classify_violations()
        }
    
    def _check_constraints(self, node):
        active_constraints = node.get_constraints()
        violations = []
        for constraint in active_constraints:
            if not self.beam.trajectory.satisfies(constraint):
                violations.append({
                    "constraint_id": constraint.id,
                    "violation_type": constraint.type,
                    "severity": constraint.severity
                })
        return violations
    
    def _check_contradictions(self, node):
        """Detect logical contradictions in reasoning path"""
        path_rules = [n.applied_rules for n in self.beam.path]
        contradictions = 0
        
        for i, rule_set in enumerate(path_rules):
            for j, later_rule_set in enumerate(path_rules[i+1:]):
                if self._rules_contradict(rule_set, later_rule_set):
                    contradictions += 1
        
        return contradictions
    
    def _rules_contradict(self, rule_set1, rule_set2):
        return False  # Stub
    
    def _is_path_irreversible(self, node):
        return False  # Stub
    
    def _classify_violations(self):
        return ["constraint_violation"]  # Stub

class SKGRunner:
    def __init__(self, skg, space_field, invocation_layer, shadow_propagator=None):
        self.skg = skg
        self.skg_id = skg.get('skg_metadata', {}).get('space_field_id', skg.get('name', 'unknown'))
        self.space_field = space_field
        self.invocation_layer = invocation_layer
        self.shadow_propagator = shadow_propagator
        self.shadow_manager = ContextShadowManager()
        self.adjustment_log = []
    
    def run(self, claim: Dict[str, Any], max_iterations=100):
        """Execute SKG traversal through space field"""

        # Extract seed vault data from claim
        seed_vault_data = claim.get('seed_vault_data', claim)

        # Initialize traversal state
        iteration = 0
        trajectory = []
        current_node_id = self.space_field.get_entry_node(claim.get('claim_type', 'default'))

        # Track metrics for CVV generation
        metrics = type('Metrics', (), {
            'confidence': 0.5,
            'entropy': 0.5,
            'contradiction': 0.0
        })()

        while iteration < max_iterations:
            trajectory.append(current_node_id)

            # Check termination conditions
            if iteration > 10:  # Stub: terminate after 10 iterations
                break

            # Process node: seeds, constraints, falsification (stub implementation)
            # In real implementation, this would invoke seeds and apply shadow adjustments

            # Simulate some processing that might trigger shadows
            if iteration == 2:  # Simulate seed invocation on third node
                try:
                    result = self.invocation_layer.invoke_logic_seed(
                        seed_name='seed_deductive_reasoner',
                        params={'claim_id': claim.get('proposition', ''), 'node_id': current_node_id},
                        calling_skg=self.skg_id
                    )
                    # Update metrics from seed result
                    if 'confidence' in result:
                        metrics.confidence = result['confidence']
                except:
                    pass  # Seed not found, continue

            iteration += 1
            current_node_id = f"node_{iteration}"  # Stub: simple node progression

        # Create CVV from final metrics
        from ecm_runtime import CVV
        cvv = CVV(
            confidence=metrics.confidence,
            contradiction=metrics.contradiction,
            entropy=metrics.entropy,
            coverage=0.8,  # Stub: coverage metric
            falsified=False,  # Stub: falsification status
            skg_id=self.skg_id
        )

        # Collect shadow artifacts emitted during traversal
        shadow_artifacts = getattr(self, 'emitted_shadows', [])

        return {
            "cvv": cvv,
            "reasoning_path": trajectory,
            "shadow_artifacts": shadow_artifacts,
            "verdict": {"status": "processed"}  # Stub verdict
        }
        
        # Check cross-path events
        shadows = self.space_field.get_shadows_at(node)
        if shadows:
            beam.process_cross_path_events(shadows)
        
        return beam

class CoreTribunal:
    def __init__(self, softmax_skg):
        self.softmax_skg = softmax_skg
        self.axis_weights = {"ontological": 0.35, "practical": 0.40, "epistemic": 0.25}
    
    def synthesize(self, philosopher_verdicts, seed_vault_data):
        # Step 1: Generate advisory report from Soft Max SKG
        softmax_advisory = self.softmax_skg.get('traverse_result', {
            "probabilities": {"locke": 0.25, "hume": 0.25, "kant": 0.25, "spinoza": 0.25},
            "epistemic_inevitability": 0.8,
            "reliability_tier": "A",
            "byzantine_warnings": {"flagged_philosophers": []}
        })  # Stub
        
        # Step 2: Soft Max output is ADVISORY ONLY
        # Core can:
        #   - Accept softmax probabilities as tribunal weights
        #   - Reject and use axis-based jurisdiction
        #   - Partially incorporate (e.g., only use Byzantine flags)
        
        if softmax_advisory["reliability_tier"] == "D":
            # One philosopher is faulty - investigate manually
            flagged = softmax_advisory["byzantine_warnings"]["flagged_philosophers"]
            self._handle_byzantine_fault(flagged, philosopher_verdicts)
        
        # Step 3: Core makes final decision
        # (May incorporate softmax probabilities but not required to)
        final_verdict = self._apply_jurisdiction_weights(
            philosopher_verdicts,
            softmax_weights=softmax_advisory["verdict_probabilities"]  # OPTIONAL
        )
        
        # Step 4: Append softmax advisory to audit trail
        final_verdict["meta_analysis"] = {
            "softmax_advisory": softmax_advisory,
            "core_accepted_softmax": True,  # or False
            "rationale": "Softmax confirmed axis dominance pattern"
        }
        
        return final_verdict
    
    def _handle_byzantine_fault(self, flagged, verdicts):
        pass  # Stub
    
    def _apply_jurisdiction_weights(self, verdicts, softmax_weights=None):
        # Stub implementation
        return {
            "claim_id": "test_claim_001",
            "final_verdict": {
                "status": "ACCEPTED",
                "primary_axis_judgments": {
                    "ontological": {"summary": "Ontological summary", "dominant_philosophers": ["locke"], "confidence": 0.8},
                    "practical": {"summary": "Practical summary", "dominant_philosophers": ["kant"], "confidence": 0.8},
                    "epistemic": {"summary": "Epistemic summary", "dominant_philosophers": ["spinoza"], "confidence": 0.8}
                },
                "reinterpretations": [],
                "philosopher_weights": softmax_weights or {"locke": 0.25, "hume": 0.25, "kant": 0.25, "spinoza": 0.25},
                "cross_tensions_resolved": ["Tension resolved"],
                "prescriptive_guidance": {"guidance": "Proceed with caution"}
            },
            "all_philosopher_verdicts": verdicts,
            "meta_analysis": {}
        }

class TribunalSynthesizer:
    def __init__(self, softmax_skg):
        self.softmax_skg = softmax_skg
        self.axis_weights = {"ontological": 0.35, "practical": 0.40, "epistemic": 0.25}
    
    def synthesize(self, philosopher_verdicts, seed_vault_data):
        """
        Produces final verdict + reinterpretations from four philosopher outputs
        
        Input: {
          "locke": {verdict_object},
          "hume": {verdict_object},
          "kant": {verdict_object},
          "spinoza": {verdict_object}
        }
        
        Output: Tribunal Verdict v1.1 format
        """
        
        # 1. Generate Soft Max advisory
        softmax_advisory = self.softmax_skg.get('traverse_result', {
            "probabilities": {"locke": 0.25, "hume": 0.25, "kant": 0.25, "spinoza": 0.25},
            "epistemic_inevitability": 0.8,
            "reliability_tier": "A",
            "byzantine_warnings": {"flagged_philosophers": []}
        })  # Stub
        
        # 2. Calculate axis-specific judgments
        axis_judgments = self._calculate_axis_judgments(philosopher_verdicts, softmax_advisory)
        
        # 3. Identify dominant philosophers per axis
        axis_dominance = self._identify_axis_dominance(axis_judgments)
        
        # 4. Generate reinterpretations
        reinterpretations = self._generate_reinterpretations(
            philosopher_verdicts, 
            axis_dominance,
            softmax_advisory['epistemic_inevitability']
        )
        
        # 5. Resolve cross-tensions
        tensions_resolved = self._resolve_tensions(philosopher_verdicts)
        
        # 6. Determine final status
        final_status = self._determine_status(axis_judgments, reinterpretations)
        
        # 7. Assemble prescriptive guidance
        guidance = self._generate_guidance(axis_judgments, reinterpretations)
        
        # 8. Compile final verdict
        claim_id = seed_vault_data.get('claim_id', f"claim_{int(time.time() * 1000)}")

        return {
            "claim_id": claim_id,
            "final_verdict": {
                "status": final_status,
                "primary_axis_judgments": axis_judgments,
                "reinterpretations": reinterpretations,
                "philosopher_weights": softmax_advisory['probabilities'],
                "cross_tensions_resolved": tensions_resolved,
                "prescriptive_guidance": guidance
            },
            "all_philosopher_verdicts": philosopher_verdicts,
            "meta_analysis": {
                "softmax_advisory": softmax_advisory,
                "core_accepted_softmax": True
            }
        }
    
    def _calculate_axis_judgments(self, verdicts, softmax):
        """Calculate confidence per philosophical axis"""
        return {
            "ontological": {
                "summary": self._summarize_ontological(verdicts),
                "dominant_philosophers": self._dominant_on_axis(verdicts, "ontological"),
                "confidence": self._axis_confidence(verdicts, softmax, "ontological")
            },
            "practical": {
                "summary": "Practical summary",
                "dominant_philosophers": ["kant"],
                "confidence": 0.8
            },
            "epistemic": {
                "summary": "Epistemic summary",
                "dominant_philosophers": ["spinoza"],
                "confidence": 0.75
            }
        }
    
    def _summarize_ontological(self, verdicts):
        return "Ontological summary"  # Stub
    
    def _dominant_on_axis(self, verdicts, axis):
        return ["locke", "hume"]  # Stub
    
    def _axis_confidence(self, verdicts, softmax, axis):
        return 0.8  # Stub
    
    def _generate_reinterpretations(self, verdicts, dominance, inevitability):
        """Create rephrased propositions with philosophical support"""
        reinterpretations = []
        
        # High inevitability → strong reinterpretation
        if inevitability > 0.80:
            # Find proposition that 3+ philosophers can support
            consensus_prop = self._find_consensus_proposition(verdicts)
            reinterpretations.append({
                "rephrased_proposition": consensus_prop,
                "supporting_philosophers": dominance['practical'],
                "tribunal_weight": inevitability
            })
        
        return reinterpretations
    
    def _find_consensus_proposition(self, verdicts):
        return "Consensus proposition"  # Stub
    
    def _resolve_tensions(self, verdicts):
        """Enumerate how philosophical conflicts were resolved"""
        return [
            "Tension resolved"
        ]  # Stub
    
    def _identify_axis_dominance(self, axis_judgments):
        return {"practical": ["kant"], "epistemic": ["spinoza"]}  # Stub
    
    def _determine_status(self, axis_judgments, reinterpretations):
        return "ACCEPTED"  # Stub
    
    def _generate_guidance(self, axis_judgments, reinterpretations):
        return {"guidance": "Proceed with caution"}  # Stub

class UCMReasoningCore:
    def __init__(self):
        # 1. Load space field geometry
        self.space_field = SpaceFieldNS()
        self.space_field.load_geometry("space_field/geometry/hlsf_base_geometry.json")
        
        # 2. Load philosophical SKGs
        self.skgs = {
            "locke": load_skg("skgs/philosophical/locke_empiricism_skg.json"),
            "hume": load_skg("skgs/philosophical/hume_skepticism_skg.json"),
            "kant": load_skg("skgs/philosophical/kant_critical_skg.json"),
            "spinoza": load_skg("skgs/philosophical/spinoza_monism_skg.json")
        }
        
        # 3. Load meta-reasoning SKG
        self.softmax_skg = load_skg("skgs/meta/softmax_consensus_skg.json")
        
        # 4. Initialize invocation layer
        self.invocation_layer = SeedInvocationLayer(
            logic_seed_dir="vault_logic_system/vaults/master_seed_vault/",
            reference_seed_dir="vault_logic_system/vaults/master_seed_vault/"
        )
        
        # 5. Initialize shadow propagator (singleton across all beams)
        from vault_logic_system.engine.shadow_propagator import ShadowPropagator
        self.shadow_propagator = ShadowPropagator()

        # 6. Initialize tribunal
        self.tribunal = TribunalSynthesizer(softmax_skg=self.softmax_skg)

        # 7. Initialize SKG runners with shadow propagator
        self.skg_runners = [
            SKGRunner(self.skgs["hume"], self.space_field, self.invocation_layer, self.shadow_propagator),
            SKGRunner(self.skgs["kant"], self.space_field, self.invocation_layer, self.shadow_propagator),
            SKGRunner(self.skgs["locke"], self.space_field, self.invocation_layer, self.shadow_propagator),
            SKGRunner(self.skgs["spinoza"], self.space_field, self.invocation_layer, self.shadow_propagator),
        ]

        # 8. Initialize multi-beam orchestrator
        from vault_logic_system.engine.multi_beam_runner import MultiBeamRunner
        self.multi_beam = MultiBeamRunner(self.skg_runners, self.shadow_propagator)

        print("✅ UCM Reasoning Core initialized with 4-beam deliberation")
    
    def reason(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute full deliberation: 4 beams → shadows → ECM → verdict
        """
        print(f"\n🔍 Deliberating claim: {claim.get('proposition', 'Unknown')}")

        # Step 1: Multi-beam traversal (parallel epistemics)
        beam_result = self.multi_beam.run(claim)

        # Step 2: ECM synthesis with shadow-aware CVVs
        from ecm_runtime import ECMRuntime
        ecm_runtime = ECMRuntime(
            cvvs=beam_result.cvvs,
            softmax_advisory={}  # Optional: can add meta-analysis later
        )

        verdict = ecm_runtime.decide()

        # Step 3: Build philosopher verdict stubs from CVVs (tribunal expects verdict objects)
        philosopher_verdicts = {}
        for i, cvv in enumerate(beam_result.cvvs):
            skg_id = getattr(cvv, 'skg_id', getattr(cvv, 'skg', f'skg_{i}'))
            philosopher_verdicts[skg_id] = {
                "status": getattr(cvv, 'status', 'PROVISIONAL'),
                "confidence": getattr(cvv, 'confidence', 0.0),
                "cvv": cvv
            }

        # Use tribunal synthesizer to produce canonical final_verdict structure
        tribunal_output = self.tribunal.synthesize(philosopher_verdicts, claim.get('seed_vault_data', {}))

        # Step 4: Compile full result with audit trail and backward-compatible keys
        final_result = {
            # Backward-compatible top-level keys expected by integration tests
            "final_verdict": tribunal_output.get('final_verdict', {}),
            "all_philosopher_verdicts": tribunal_output.get('all_philosopher_verdicts', philosopher_verdicts),
            "meta_analysis": tribunal_output.get('meta_analysis', {}),

            # Additional diagnostics and signatures
            "ecm_runtime_verdict": verdict,
            "beam_metadata": beam_result.beam_metadata,
            "resonance_markers": beam_result.resonance_markers,
            "cvv_signatures": [getattr(cvv, 'signature', lambda: None)() for cvv in beam_result.cvvs],
            "timestamp_ms": int(time.time() * 1000),
            "deliberation_complete": True
        }

        # Log a concise tribunal verdict summary when possible
        try:
            status = final_result['final_verdict'].get('status', 'UNKNOWN')
            confidence = final_result['meta_analysis'].get('softmax_advisory', {}).get('epistemic_inevitability', 0.0)
            print(f"🏛️  Tribunal verdict: {status} (softmax inevitability: {confidence:.3f})")
        except Exception:
            pass

        return final_result

    def adjudicate_claim(self, claim_text, seed_vault_data):
        """Legacy method - redirects to new reason method"""
        claim = {
            "proposition": claim_text,
            "seed_vault_data": seed_vault_data
        }
        return self.reason(claim)
    
    def _log_audit_trail(self, verdict):
        print(f"Audit: Verdict {verdict['claim_id']} processed")  # Stub
    
    def get_shadow_stats(self) -> Dict[str, Any]:
        """Get shadow propagation statistics across all SKGs"""
        return self.invocation_layer.get_shadow_stats()


# --- FastAPI endpoints (created when FastAPI is available) ---
try:
    from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Header
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    from typing import Optional, List
    from pathlib import Path
    import aiofiles
    import os
    import re
    import uuid
    import subprocess
    import logging
except Exception as _e:
    # FastAPI not installed in this environment — API endpoints will be
    # unavailable. This keeps the repository importable for tests that do
    # not require the HTTP API.
    app = None
    print("FastAPI not available; HTTP API endpoints disabled.", _e)
else:
    app = FastAPI(title="UCM Core ECM API", version="1.0.0")

    # Allow common local dev origins (Vite/CRA default ports) — adjust as needed.
    origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    UPLOAD_DIR = Path(__file__).parent / "uploads"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ALLOWED_EXT = {".txt", ".json", ".md", ".pdf", ".doc", ".docx"}

    # Initialize a single core instance for HTTP handling
    core = UCMReasoningCore()

    # Utilities: secure filename, optional virus scan, and auth dependency
    FNAME_SAFE_RE = re.compile(r"[^A-Za-z0-9._-]")

    def secure_filename(filename: str) -> str:
        """Sanitize uploaded filename and prefix with a short uuid to avoid collisions."""
        name = Path(filename).name
        name = name.strip().replace(" ", "_")
        name = FNAME_SAFE_RE.sub("", name)
        # collapse multiple dots
        name = re.sub(r"\.+", ".", name)
        if name.startswith("."):
            name = "file" + name
        # limit length
        if len(name) > 120:
            base, ext = os.path.splitext(name)
            name = base[:120 - len(ext)] + ext
        prefix = uuid.uuid4().hex[:8]
        return f"{prefix}_{name}"

    def scan_file(path: Path) -> bool:
        """Attempt to scan file for malware. Controlled by ECM_UPLOAD_SCAN env var.

        The function will attempt to use `pyclamd` if available, otherwise
        it will fall back to a `clamscan` subprocess call if present on PATH.
        If scanning is enabled but no scanner is available, an error is raised.
        """
        scan_enabled = os.getenv("ECM_UPLOAD_SCAN", "false").lower() == "true"
        if not scan_enabled:
            return True

        # Try pyclamd first
        try:
            import pyclamd

            try:
                cd = pyclamd.ClamdUnixSocket()
            except Exception:
                cd = pyclamd.ClamdNetworkSocket()
            res = cd.scan_file(str(path))
            # pyclamd returns None for clean files
            return res is None
        except Exception:
            # Fallback to clamscan binary
            try:
                proc = subprocess.run(["clamscan", "--no-summary", str(path)], capture_output=True)
                return proc.returncode == 0
            except FileNotFoundError:
                raise HTTPException(status_code=500, detail="Upload scanning enabled but no scanner available (install pyclamd or clamscan)")

    def require_api_key(x_api_key: Optional[str] = Header(None), authorization: Optional[str] = Header(None)):
        """Simple API key check. Enable by setting ECM_REQUIRE_AUTH=true and ECM_API_KEY env var."""
        req = os.getenv("ECM_REQUIRE_AUTH", "false").lower() == "true"
        if not req:
            return True
        api_key = os.getenv("ECM_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="ECM_REQUIRE_AUTH=true but ECM_API_KEY not configured")
        provided = x_api_key
        if not provided and authorization and authorization.startswith("Bearer "):
            provided = authorization.split(" ", 1)[1]
        if provided != api_key:
            raise HTTPException(status_code=401, detail="Unauthorized")
        return True

    class AdjudicateRequest(BaseModel):
        query: str
        seed_vault: Optional[dict] = None

    @app.post("/api/adjudicate")
    async def api_adjudicate(payload: AdjudicateRequest, _auth: bool = Depends(require_api_key)):
        query = (payload.query or "").strip()
        if not query:
            raise HTTPException(status_code=400, detail="Empty query")
        try:
            result = core.adjudicate_claim(query, payload.seed_vault or {})
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/upload")
    async def api_upload(files: List[UploadFile] = File(...), _auth: bool = Depends(require_api_key)):
        uploaded = []
        for upload in files:
            raw_name = Path(upload.filename).name
            ext = Path(raw_name).suffix.lower()
            if ext not in ALLOWED_EXT:
                # skip unsupported file types
                continue
            filename = secure_filename(raw_name)
            dest = UPLOAD_DIR / filename
            async with aiofiles.open(dest, "wb") as out_f:
                content = await upload.read()
                await out_f.write(content)

            # Virus scan if enabled; will raise HTTPException on failure
            try:
                clean = scan_file(dest)
            except HTTPException:
                # remove file if scanning failed due to missing scanner
                try:
                    dest.unlink(missing_ok=True)
                except Exception:
                    pass
                raise

            if not clean:
                # infected — remove and fail
                try:
                    dest.unlink(missing_ok=True)
                except Exception:
                    pass
                raise HTTPException(status_code=400, detail=f"Malicious content detected in {raw_name}")

            uploaded.append({
                "filename": filename,
                "size": dest.stat().st_size,
                "content_type": upload.content_type,
            })

        return {"message": f"Successfully uploaded {len(uploaded)} files", "files": uploaded}

    @app.get("/api/health")
    async def api_health():
        return {"status": "healthy", "service": "UCM Core ECM FastAPI"}

    # Serve uploaded files for convenience (local/dev only)
    app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")