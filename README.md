# UCM Core ECM - Universal Cognitive Mediation with Epistemic Contract Management

*A philosophical reasoning engine that orchestrates four foundational thinkers (Hume, Kant, Locke, Spinoza) through multi-beam deliberation with confidence capping, shadow propagation, and ECM contract enforcement.*

## Overview

UCM Core ECM implements a sophisticated epistemic reasoning system that combines philosophical knowledge graphs with modern software engineering principles. The system enables true multi-paradigm deliberation through:

- **Four Philosophical Beams**: Hume (empiricism), Kant (categorical imperative), Locke (social contract), Spinoza (rational monism)
- **Confidence Capping**: Prevents pathological seed behavior through intelligent node evaluation
- **Shadow Propagation**: Cross-SKG metric influence without logic contamination
- **ECM Runtime**: Contract-faithful decision enforcement with CVV (Confidence-Validity-Verification) validation
- **Multi-Beam Orchestration**: Parallel philosophical reasoning with global coherence
- **FastAPI Backend**: RESTful API with authentication and upload hardening
- **React/Vite Frontend**: Modern TypeScript UI for human-facing interaction
- **CI/CD Pipeline**: Automated testing and frontend builds via GitHub Actions

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
│   ├── ECM Runtime       - Contract enforcement
│   └── TribunalSynthesizer - Verdict synthesis
├── FastAPI Backend
│   ├── /api/adjudicate   - Multi-beam deliberation
│   ├── /api/upload       - File upload with hardening
│   └── /api/health       - Health check
├── React/Vite Frontend
│   ├── QueryForm         - Text/file input for queries
│   ├── ResultCard        - Structured verdict display
│   └── Authentication    - API key handling
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
- 30 comprehensive runtime tests
- CVV validation framework
- Contract fidelity verification

### 🚀 FastAPI Backend
- RESTful endpoints for adjudication and uploads
- Optional authentication via API keys
- Upload hardening with filename sanitization and virus scanning
- CORS-enabled for frontend integration

### ⚛️ React/Vite Frontend
- TypeScript-based modern UI
- File upload support for philosophical texts
- Structured result rendering with verdict details
- Authentication wired via environment variables

### 🔄 CI/CD Pipeline
- Automated testing on pushes/PRs
- Frontend build verification
- Pytest integration with 30/30 tests passing

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+ (for frontend)
- dataclasses, typing (standard library)

### Installation

```bash
git clone <repository-url>
cd UCM_Core_ECM
pip install -r requirements.txt
cd frontend && npm install
```

### Running the Backend

```bash
# Development (no auth)
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Production (with auth and scanning)
export ECM_REQUIRE_AUTH=true
export ECM_API_KEY=your-secure-api-key
export ECM_UPLOAD_SCAN=true  # Requires clamscan or pyclamd
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Running the Frontend

```bash
cd frontend
npm run dev  # Starts on http://localhost:5173
```

### Basic Usage (Programmatic)

```python
from main import UCMReasoningCore

# Initialize the reasoning engine
core = UCMReasoningCore()

# Run multi-beam deliberation
result = core.reason({
    "proposition": "Is free will compatible with determinism?",
    "seed_vault_data": {}
})

print(f"Verdict: {result['final_verdict']['status']}")
print(f"Confidence: {result['meta_analysis']['softmax_advisory']['epistemic_inevitability']}")
```

### API Usage

```python
import requests

# Health check
r = requests.get('http://127.0.0.1:8000/api/health')
print(r.json())  # {"status": "healthy", "service": "UCM Core ECM FastAPI"}

# Adjudication
r = requests.post('http://127.0.0.1:8000/api/adjudicate',
                  json={'query': 'Is AI consciousness murder?'},
                  headers={'Authorization': 'Bearer your-api-key'})
print(r.json())
```

### Running Tests

```bash
# All tests (30/30 passing)
python -m pytest

# Integration tests only
python -m pytest vault_logic_system/tests/test_api_integration.py

# In isolated environment (recommended)
python -m venv .venv
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python -m pytest -q
```

**Test Results (Latest Run):**
```
Running 30 tests...
✅ All 30 ECM runtime tests passed!
✅ ECM_CONTRACT.json contract fidelity verified
✅ ECM runtime enforcement working correctly
✅ Integration tests: 3/3 passed
```

## Environment Variables

### Backend
- `ECM_REQUIRE_AUTH`: Enable API key authentication (default: false)
- `ECM_API_KEY`: API key for authentication (required if auth enabled)
- `ECM_UPLOAD_SCAN`: Enable virus scanning for uploads (default: false, requires clamscan/pyclamd)

### Frontend
- `VITE_API_BASE`: Backend API URL (default: http://localhost:8000)
- `VITE_API_KEY`: API key for requests (matches backend ECM_API_KEY)

## Security & Upload Hardening

The FastAPI backend includes optional hardening for uploads and authentication:

- **Authentication**: API key enforcement via `ECM_REQUIRE_AUTH` and `ECM_API_KEY`. Send via `Authorization: Bearer <KEY>` or `x-api-key` header.
- **Upload Scanning**: Malware detection via `pyclamd` or `clamscan` when `ECM_UPLOAD_SCAN=true`.
- **Filename Sanitization**: Unsafe characters removed, UUID prefix added to prevent collisions and traversal attacks.

For production, always enable authentication and scanning, run behind HTTPS, and use proper secrets management.

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

### TribunalSynthesizer
```python
# Verdict synthesis from philosopher verdicts
tribunal = TribunalSynthesizer()
final_verdict = tribunal.synthesize(philosopher_verdicts, seed_data)
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
- TribunalSynthesizer for verdict synthesis
- ECM contract compliance (30/30 tests)
- Four philosophical SKGs implemented
- Space field geometry integration
- FastAPI backend with auth and upload hardening
- React/Vite TypeScript frontend with file upload and result rendering
- CI/CD pipeline with automated testing and builds
- Integration tests for API endpoints

### 🔄 In Progress
- Docker containerization
- Performance optimization
- Advanced telemetry

### 📋 Roadmap
- [ ] Benchmarking suite
- [ ] Configuration management
- [ ] End-to-end CI with scanning
- [ ] Production deployment guides

## Testing

The system includes comprehensive ECM runtime tests covering:

- Confidence validation (range checking, capping)
- Contradiction handling (thresholds, resolution)
- CVV signature verification (deterministic, content-based)
- Invariant enforcement (sum validation, boundary conditions)
- Multi-beam coherence (shadow propagation, tribunal synthesis)
- API integration (health, adjudicate, upload endpoints)

**All 30 tests currently pass with 100% ECM contract fidelity.**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure ECM contract compliance
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by philosophical epistemology and cognitive architectures
- Built with modern Python engineering practices
- Designed for epistemic contract management in AI systems

---

*This system represents a novel approach to philosophical reasoning in computational systems, enabling coherent multi-paradigm deliberation through carefully constrained cross-influence mechanisms.*

**Test Results (Latest Run):**
```
Running 30 tests...
✅ All 30 ECM runtime tests passed!
✅ ECM_CONTRACT.json contract fidelity verified
✅ ECM runtime enforcement working correctly
✅ Integration tests: 3/3 passed
```

## Web Interface

The system includes a complete FastAPI backend and React/Vite frontend for end-to-end functionality:

- **Backend**: RESTful API with `/api/adjudicate`, `/api/upload`, and `/api/health` endpoints
- **Frontend**: TypeScript UI with file upload, query input, and structured result display
- **Authentication**: API key handling via environment variables
- **CORS**: Configured for local development

To run both:

```bash
# Terminal 1: Backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Frontend
cd frontend && npm run dev
```

Open `http://localhost:5173` to use the interface.

## Security & Upload Hardening

The FastAPI backend includes optional hardening for uploads and authentication. These are environment-controlled so development remains convenient while production can enforce stricter controls.

- `ECM_REQUIRE_AUTH=true` — When enabled, requests must include an API key. Set `ECM_API_KEY` to a strong secret and send it via the `x-api-key` header or `Authorization: Bearer <KEY>`.
- `ECM_UPLOAD_SCAN=true` — When enabled, uploads are scanned for malware. The code will attempt to use `pyclamd` (recommended) or fall back to the `clamscan` binary if available. If scanning is enabled but no scanner is present, uploads will be rejected.

Filename sanitization is applied to uploads (unsafe characters removed, prefixed with a short UUID) to avoid directory traversal and collisions.

For production, always enable `ECM_REQUIRE_AUTH` and `ECM_UPLOAD_SCAN`, and run the application behind HTTPS with proper authentication and secrets management.

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
- TribunalSynthesizer for verdict synthesis
- ECM contract compliance (30/30 tests)
- Four philosophical SKGs implemented
- Space field geometry integration
- FastAPI backend with auth and upload hardening
- React/Vite TypeScript frontend with file upload and result rendering
- CI/CD pipeline with automated testing and builds
- Integration tests for API endpoints

### 🔄 In Progress
- Docker containerization
- Performance optimization
- Advanced telemetry

### 📋 Roadmap
- [ ] Benchmarking suite
- [ ] Configuration management
- [ ] End-to-end CI with scanning
- [ ] Production deployment guides

## Testing

The system includes comprehensive ECM runtime tests covering:

- Confidence validation (range checking, capping)
- Contradiction handling (thresholds, resolution)
- CVV signature verification (deterministic, content-based)
- Invariant enforcement (sum validation, boundary conditions)
- Multi-beam coherence (shadow propagation, tribunal synthesis)
- API integration (health, adjudicate, upload endpoints)

**All 30 tests currently pass with 100% ECM contract fidelity.**

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure ECM contract compliance
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Inspired by philosophical epistemology and cognitive architectures
- Built with modern Python engineering practices
- Designed for epistemic contract management in AI systems

---

*This system represents a novel approach to philosophical reasoning in computational systems, enabling coherent multi-paradigm deliberation through carefully constrained cross-influence mechanisms.*
