"""
Flask web interface (removed)

This module used to provide a simple Flask-based UI for ad-hoc access
to the UCM Core ECM. The Flask layer has been intentionally reverted to
avoid introducing a special-case web server into the repository.

Design decision:
- Keep the canonical interface programmatic (the Python API and FastAPI
  endpoints where available).
- Build any human-facing UI as a separate React/Vite frontend that
  consumes FastAPI endpoints from the ECM backend.

If you see this file in the tree it means the experimental Flask UI was
kept as a placeholder; import or running it will exit immediately.
"""

import sys

sys.exit("Flask web interface removed; use FastAPI + React/Vite frontend instead.")