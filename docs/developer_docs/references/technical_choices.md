# Technical Choices
This page documents the technical stack decisions - what was chosen, what was considered, and why.

## Python 3.11+
**Chosen**: Python 3.11  
**Considered**: 3.9, 3.10  
Maya 2024 ships with Python 3.10. Maya 2025 ships with Python 3.11. The tool targets Maya 2024+ ans uses Python 3.11+ syntax (`match`, improved error messages, `tomlib`).  
If you need to support Maya 2024 strictly, downgrade `requires-python` to `>=3.10` in `pyproject.toml` and avoid 3.11-only syntax.

## PySide6
**Chosen**: PySide6  
**Considered**: PySide2, maya.cmds UI  

| Option  | Pros  | Cons |
| ---- | ---- | --- |
`maya.cmds` UI | No dependency, always available | Very limited layout, ,no styling | 
PySide2 | Ships with Maya 2017-2024 | Shapes excluded |
**PySide6** | Qt6, modern API, ships with Maya 2025  | Requires install on Maya 2024 |

PySide6 was chosen for its modern API and long-term support. On Maya 2024, it requires a separate install (`pip install PySide6` in Maya's Python). On Maya 2025 it is bundled.  
!!! warning
    Do not mix PySide2 and PySide6 in the same Maya session - they conflict.  
    Cross Renamer Tool uses PySide6 exclusively.

## MayaQWidgetDockableMixin
**Chosen**: `maya.app.general.mayaMixin.MayaQWidgetDockableMixin`  
**Considered**: Plain `QDialog`, `QMainWindow`  
`MayaQWidgetDockableMixin` integrates the tool window into Maya's workspace system - the artist can dock it next to the Channel Box, float it, or save its position between sessions. A Plain `QDialog` or `QMainWindow` would always open as floating window with no docking support.

## Ruff
**Chosen**: Ruff (linter + formatter)  
**Considered**: Black + Flake8

| Tool | Role | Replaced by |
| --- | --- | --- |
| Black | Formatter | `ruff format` |
| Flake8 | Linter | `ruff check` |

Ruff replaces all two in a single tool, runs 10-100x faster, and is configured in one place (`pyproject.toml`). There is no reason to keep Black or Flake8 alongside Ruff.  
Active rule sets:
```toml
[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "F",      # pyflakes
    "I",      # isort
    "W",      # pycodestyle warnings
    "B",      # bugbear
    "BLE",    # blind exception
    "PIE",    # miscellaneous
    "RUF",    # ruff-specific 
    "UP",     # pyupgrade 
]
ignore = [
    "E501",   # line too long
    "RUF012",  # mutable class attribute
]
```

## pytest + unittest
**Chosen**: `unittest.TestCase` classes discovered by `pytest`  
**Considered**: Pure pytest, pure unittest  
`unittest` was chosen for its built-in availability (no extra dependency) and familiar structure. `pytest` is used as the test runner because it provides better output, coverage integration, and CI compatibility - but it discovers and runs `unittest.TestCase` natively without any migration needed.  
```bash
# pytest runs without unittest tests transparently
pytest tests/ -v

# Or run with unittest directly if pytest is not available
python -m unittest discover -s tests -vs
```

## MkDocs + Material theme
**Chosen**: MkDocs with `mkdocs-material`  
**Considered**: Sphinx, plain GitHub wiki  

| Option | Pros | Cons |
| --- | --- | --- |
| GitHub Wiki | Zero setup | No versioning, no custom structure |
| Sphinx | Industry standard for Python | Complex config, RST syntax | 
| **MkDocs + Material** | Markdown, beautiful theme, simple config | Less powerful than Sphinx for API docs |  

MkDocs was chosen for its simplicity - documentation is written in Markdown, the same format as the README and CHANGELOG. The Material theme provides a professional look with zero CSS work.  
`mkdocstrings` generates API reference pages directly from docstrings, removing the need to maintain a separate API documentation.

## Conventional Commits
**Chosen**: Conventional Commits specification  
**Considered**: Free-form commit messages, GitFlow tags  
Conventional Commits enforce a structured format that:
- makes the Git history readable at a glance
- allows automated changelog generation
- is enforced by the CI (Ruff auto-commit uses `♻️ Reformatting by ruff`)

See [Reference: Conventional Commits](../commit_conventions/)  for the full reference.

## JSON for presets
**Chosen**: JSON files in `src/crossrenamertool/resources/presets/`  
**Considered**: Maya `optionVar`, SQLite, INI files  
JSON was chosen because:
- it is human-readable and editable outside Maya
- it can be committed to Git and shared across a team
- Python's `json` module requires no extra dependency
- it is easy to validate and reset to default

See [References: Design Choices - JSON presets over Maya optionVar](../design_choices/#architecture-json-presets-over-maya-optionvar) for the full rationale.

## UUID for temporary names
**Chosen**: `uuid.uuid4().hex[:8]` for temporary node names during double-pass renaming  
**Considered**: timestamp, sequential counter, random string  
```python
temp = f"__tmp_{uuid.uuid4().hex[:8]}__"
# -> __tmp_a3f9c21b__
```
UUID4 is collision-resistant by design - two nodes will never get the same temporary name even in a scene with thousands of nodes. A timestamp would collide if two nodes are renamed in the same millisecond. A sequential counter required tracking state across the loop.

## GitHub Actions for CI/CD
**Chosen**: GitHub Actions  
**Considered**: GitLab CI, Jenkins, local pre-commit hooks  
GitHub Actions was chosen because the project is hosted on GitHub - no extra infrastructure is needed. The workflow runs on every push to `main` and `develop` in the following order:
```
lint (Ruff) -> Tests (unittest) -> docs (MkDocs gh-deploy)
```
Each job blocks the next - docs are never deployed if the linter or tests fail.
See the [How to Guides: CI/CD Guide for running the pipeline locally](../../how-to-guides/run_cicd_locally/).
