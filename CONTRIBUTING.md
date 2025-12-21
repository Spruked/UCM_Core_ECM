# Contributing to UCM Core ECM

Thank you for your interest in contributing to UCM Core ECM! This document provides guidelines and information for contributors.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation
```bash
git clone <repository-url>
cd UCM_Core_ECM
pip install -r requirements.txt  # if requirements.txt exists
```

### Running Tests
```bash
python vault_logic_system/tests/run_tests.py
```

All tests must pass before submitting a pull request.

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep line length under 88 characters (Black default)

## ECM Contract Compliance

All changes must maintain ECM contract compliance. The ECM runtime enforces:

- Confidence values must be between 0.0 and 1.0
- CVV triplets must sum to valid ranges
- Invariants must be preserved across operations
- Shadow propagation must not contaminate logic

### Testing Requirements

- Add unit tests for new functionality
- Ensure all existing tests pass
- Test edge cases and error conditions
- Validate ECM contract compliance

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the full test suite
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include test results in the PR description
- Ensure CI/CD checks pass

## Philosophical SKG Guidelines

When modifying or adding philosophical knowledge graphs:

- Maintain philosophical accuracy
- Preserve the unique characteristics of each thinker
- Ensure cross-SKG compatibility
- Document reasoning patterns clearly

## Architecture Principles

- **Confidence Capping**: Prevent pathological accumulation
- **Shadow Propagation**: Metrics-only cross-influence
- **ECM Contract**: Runtime enforcement of epistemic integrity
- **Multi-Beam Orchestration**: Sequential execution with global coherence

## Reporting Issues

When reporting bugs or requesting features:

- Use the issue templates
- Provide detailed reproduction steps
- Include system information
- Attach relevant logs or test output

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a positive community
- Follow the golden rule

## License

By contributing to this project, you agree that your contributions will be licensed under the same MIT License that covers the project.