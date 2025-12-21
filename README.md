# UCM Core ECM - Universal Cognitive Mediation with Epistemic Contract Management

*A philosophical reasoning engine that orchestrates four foundational thinkers (Hume, Kant, Locke, Spinoza) through multi-beam deliberation with confidence capping, shadow propagation, and ECM contract enforcement.*

## Overview

UCM Core ECM implements a sophisticated epistemic reasoning system that combines philosophical knowledge graphs with modern software engineering principles. The system enables true multi-paradigm deliberation through:

- **Four Philosophical Beams**: Hume (empiricism), Kant (categorical imperative), Locke (social contract), Spinoza (rational monism)
- **Confidence Capping**: Prevents pathological seed behavior through intelligent node evaluation
- **Shadow Propagation**: Cross-SKG metric influence without logic contamination
- **ECM Runtime**: Contract-faithful decision enforcement with CVV (Confidence-Validity-Verification) validation
- **Multi-Beam Orchestration**: Parallel philosophical reasoning with global coherence

## Architecture

```
UCMReasoningCore
├── Philosophical SKGs (JSON-based knowledge graphs)
│   ├── hume_skg.json     - Empirical reasoning patterns
│   ├── kant_skg.json     - Deontological ethics
│   ├── locke_skg.json    - Social contract theory
│   └── spinoza_skg.json  - Rational metaphysics
├── Engine Components
│   ├── MiniSKGExecutor   - Surgical confidence capping
│   ├── ShadowPropagator  - Cross-paradigm influence
│   ├── MultiBeamRunner   - Orchestration layer
│   └── ECM Runtime       - Contract enforcement
└── Space Field Geometry  - Traversal environment
```

## Key Features

### 🔒 Confidence Capping
- Prevents infinite confidence accumulation
- Intelligent node evaluation with invariant enforcement
- Surgical intervention in pathological seed behavior

### 🌑 Shadow Propagation
- Metrics-only influence between SKGs
- TTL-based propagation with adjustment limits
- Resonance markers for epistemic coherence

### ⚡ Multi-Beam Orchestration
- Sequential execution with global shadow state
- Four-beam philosophical deliberation
- Tribunal synthesis for final verdicts

### 📋 ECM Contract Compliance
- 26 comprehensive runtime tests
- CVV validation framework
- Contract fidelity verification

## Quick Start

### Prerequisites
- Python 3.8+
- dataclasses, typing (standard library)

### Installation
```bash
git clone <repository-url>
cd UCM_Core_ECM
pip install -r requirements.txt  # If dependencies exist
```

### Basic Usage
```python
from main import UCMReasoningCore

# Initialize the reasoning engine
core = UCMReasoningCore()

# Run multi-beam deliberation
result = core.reason("ethical_dilemma_query")
print(f"Verdict: {result[
verdict]}")
print(f"Confidence: {result[confidence]}")
print(f"Shadows Applied: {result[shadow_count]}")
```

### Running Tests
```bash
python vault_logic_system/tests/run_tests.py
```

**Test Results (Latest Run):**
```
Running 26 tests...
✅ All 26 ECM runtime tests passed!
✅ ECM_CONTRACT.json contract fidelity verified
✅ ECM runtime enforcement working correctly
```

## Philosophical SKGs

### Hume (Empiricism)
- Focus: Experience-based reasoning
- Strengths: Evidence validation, inductive patterns
- Application: Scientific methodology, causal inference

### Kant (Deontology)
- Focus: Categorical imperatives
- Strengths: Universal moral laws, duty ethics
- Application: Rights-based decisions, rule consistency

### Locke (Social Contract)
- Focus: Individual rights and consent
- Strengths: Liberty preservation, property rights
- Application: Democratic governance, civil liberties

### Spinoza (Rational Monism)
- Focus: Rational metaphysics
- Strengths: Logical necessity, substance monism
- Application: Systemic coherence, metaphysical foundations

## Technical Components

### MiniSKGExecutor
```python
# Core traversal with confidence capping
executor = MiniSKGExecutor(skg_data, confidence_cap=0.95)
result = executor.traverse(seed_input, space_field)
```

### ShadowPropagator
```python
# Cross-SKG influence management
propagator = ShadowPropagator(ttl=5, adjustment_limit=0.1)
propagator.emit_shadow(source_skg="hume", target_skg="kant", metric_delta=0.05)
```

### MultiBeamRunner
```python
# Orchestration of four philosophical beams
runner = MultiBeamRunner(beams=[hume_beam, kant_beam, locke_beam, spinoza_beam])
verdict = runner.run(query, global_shadows=True)
```

### ECM Runtime
- **Contract Validation**: Ensures epistemic integrity
- **CVV Framework**: Confidence-Validity-Verification triplets
- **Runtime Enforcement**: Automatic invariant checking

## Development Status

### ✅ Completed
- MiniSKGExecutor with confidence capping
- ShadowPropagator with TTL and limits
- MultiBeamRunner orchestration
- ECM contract compliance (26/26 tests)
- Four philosophical SKGs implemented
- Space field geometry integration

### 🔄 In Progress
- Docker containerization
- GitHub repository setup
- Performance optimization

### 📋 Roadmap
- [ ] Web API interface
- [ ] Configuration management
- [ ] Advanced telemetry
- [ ] Benchmarking suite

## Testing

The system includes comprehensive ECM runtime tests covering:

- Confidence validation (range checking, capping)
- Contradiction handling (thresholds, resolution)
- CVV signature verification (deterministic, content-based)
- Invariant enforcement (sum validation, boundary conditions)
- Multi-beam coherence (shadow propagation, tribunal synthesis)

**All 26 tests currently pass with 100% ECM contract fidelity.**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure ECM contract compliance
5. Submit a pull request

## License

[License information to be added]

## Acknowledgments

- Inspired by philosophical epistemology and cognitive architectures
- Built with modern Python engineering practices
- Designed for epistemic contract management in AI systems

---

*This system represents a novel approach to philosophical reasoning in computational systems, enabling coherent multi-paradigm deliberation through carefully constrained cross-influence mechanisms.*
