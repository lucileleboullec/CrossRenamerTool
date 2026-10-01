# Set up the development environment

This tutorial walks you through setting up a local development environment for Cross Renamer Tool from scratch. By the end, you will be able to run the tests, lint the code and preview the documentation locally.

**Prerequisites**: Git, Python 3.11+, Maya 2024+ (optional for UI testing)

## 1. Clone the repository
```bash
git clone https://github.com/lucileleboullec/CrossRenamerTool.git
cd CrossRenamerTool
```

## 2. Create a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

## 3. Install the dev dependencies

```bash
pip install -e ".[dev]"
```

This installs the package in editable mode (`-e`) so changes to the source are reflected immediately, plus the dev dependencies (`ruff`, `pytest`, `pytest-cov`).

## 4. Install the doc dependencies (optional)

```bash
pip install -e ".[docs]"
```

Only needed if you plan to work on the documentation

## 5. Verify the setup

```powershell
# Ruff the linter - should pass with no errors
ruff check .

# Run the tests
$env:PYTHONPATH = "src"  
python -m unittest discover -s tests -v

# Preview the docs (if installed)
mkdocs serve
```

If all three commands pass, your environment is ready.

## Next steps
Now that your environment is set up, follow the [Tutorials: Add a feature end to end](../add_a_feature/) to make your first contribution.