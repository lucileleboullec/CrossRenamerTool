# Run CICD locally

Use this guide to reproduce the CI pipeline on your machine before pushing - this avoids failed runs on GitHub Actions.

## The CI pipeline order
```
1. Lint (Ruff) → 2. Tests (unittest) → 3. Docs(MKDocs)
```
Each step must pass before the next runs. Reproduce them in the same order locally.

## Step 1 - Lint

```bash
# Check for errors
ruff check .

# Auto-fix what can be fixed
ruff check --fix .

# Format
ruff format .

# Verify the format is clean
ruff format --check .
```
The CI failed if `ruff check .` or `ruff format --check .` exists with a non-zero code.

## Step 2 - Tests
```bash
# Set up the environment
$env:PYTHONPATH = "src" 

python -m unittest discover -s tests -v
```
All tests must pass. If a test fails locally it will fail in the CI.

## Step 3 - Docs
```bash
# Install docs dependencies if not already installed
pip install -e ".[docs]"

# Build in strict mode - same as the CI
mkdocs build --strict

# Preview locally
mkdocs serve
```
`--strict` treats warnings as errors - exactly like the CI. If it passes locally with `--strict`, it will pass in the CI.

## Run everything in one command
```powershell
# Windows Powershell
ruff check .; ruff format --check .; python -m unittest discover -s tests -v; mkdocs build --strict
```

```bash
# macOS / Linux
ruff check . && ruff format --check . && python -m unittest discover -s tests -v && mkdocs build --strict
```
If all four commands exit with code 0, your push will pas the CI.

## Checking what the CI sees
The CI runs on Ubuntu - if you are on Windows and test passes locally but fails in the CI, the most common cause is a path separator (`\` vs `/`). Always use `pathlib.Path` instead of string concatenation for file paths:
```python
# ❌ Windows-only
path = "resources\\presets\\prefixes.json

# ✅ cross-platform
from pathlib import Path
path = Path("resources") / "presets" / "prefixes.json"
```
