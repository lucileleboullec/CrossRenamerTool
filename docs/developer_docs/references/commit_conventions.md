# Commit Conventions
Cross Renamer Tool uses [Gitmoji](https://gitmoji.dev) for commit messages. Every commit starts with an emoji that indicates the type of change.
```
<type emoji>(<scope>) <description>

[optional body]

[optional footer]
```

## Gitmoji reference

| Emoji | Code | When to use |
|---|---|---|
| ✨ | `:sparkles:` | New feature |
| 🐛 | `:bug:` | Bug fix |
| 🔥 | `:fire:` | Remove code or files |
| 📝 | `:memo:` | Documentation |
| 💄 | `:lipstick:` | UI / style changes |
| ♻️ | `:recycle:` | Refactoring |
| 🧪 | `:test_tube:` | Add or update tests |
| 🔧 | `:wrench:` | Configuration files (pyproject.toml, mkdocs.yml...) |
| 👷 | `:construction_worker:` | CI/CD |
| 🚀 | `:rocket:` | Performance improvement |
| 💥 | `:boom:` | Breaking change |
| 🎨 | `:art:` | Code formatting (Ruff) |
| 🚑️ | `:ambulance:` | Critical hotfix |
| 📦️ | `:package:` | Dependencies |
| 🏗️ | `:building_construction:` | Architecture changes |
| 💬 | `:speech_balloon:` | Strings, tooltips, labels |
| 🗑️ | `:wastebasket:` | Deprecation |
| 🩹 | `:adhesive_bandage:` | Minor non-critical fix |

Full reference: [gitmoji.dev](https://gitmoji.dev)

## Examples for this project
 
```bash
✨ Add swap L/R feature with regex pattern
🐛 Fix name conflict in double-pass renaming
📝 Add commit conventions to developer docs
♻️ Extract _process_nodes helper in maya_api
🧪 Add edge cases for search_replace tests
🔧 Configure ruff rules in pyproject.toml
👷 Add tests job to CI/CD pipeline
💄 Update QSS stylesheet for spinbox arrows
🎨 Ruff format
💥 Migrate to unified add_preset / remove_preset API
📦️ Add mkdocs-material to docs dependencies
🏗️ Migrate architecture from maya_api to model layer
💬 Update tooltips with HTML formatting
🔥 Remove unused black configuration
```

## Scopes
The scope is optional by recommended. Use the module or feature name:

| Scope | Covers |
| --- | --- |
| `renamer` | `core/renamer.py` | 
| `maya_api` | `model/maya_api.py` |
| `presets` | `core/presets.py` |
| `ui` | Any widget or main window |
| `rename` | Rename feature |
| `prefix` | Prefix/Suffix feature |
| `search` | Search & Replace feature |
| `utils` | Utils page features |
| `cicd` | GitHub Actions workflows |
| `docs` | Documentation files |

## Rules
### Description
- Use the **imperative mood** - "add feature" not "added feature"
- Start with a **Uppercase** letter
- No period at the end
- Keep it under **72 characters**

```bash
# ✅ correct
✨ Add step parameter to rename_nodes
🐛 Avoid name conflict with double-pass renaming
 
# ❌ incorrect
✨ added step parameter        ← past tense
✨ add step parameter.         ← trailing period
✨ add the step parameter to the rename_nodes function in maya_api.py  ← too long
```

## Body (optional)
Use the body to explain *why*, not *what* - the diff already shows what changed:

```
♻️ Extract _process_nodes helper in maya_api

All node-level operations shared the same loop - retrieve nodes, check existence, apply renamer, log result.
Centralizing this in _process_nodes remove duplication and makes each operation a one-liner.
```

## Breaking changes
Add `BREAKING CHANGES:` in the footer:

```
💥 Migrate to unified add_preset / remove_preset API

BREAKING CHANGE: add_prefix() and remove_prefix() are removed.
Use add_preset("prefixes", value) and remove_preset("prefixes", value) instead.
```

## Branch naming

| Branch type | Pattern | Example |
| --- | --- | --- |
| Feature | `feature/<description>` | `feature/swap-side`|
| Buf fix | `fix/<description>` | `fix/name-conflit-step`|
| Documentation | `docs/<description>` | `docs/api-reference`|
| CI/CD | `ci/<description>` | `ci/add-tests-job`|

## Pull Request naming
PR titles follow the same Gitmoji format as commit messages:
```
✨ Add fix shape names feature
🐛 Handle empty selection in hierarchy mode
📝 Add developer documentation structure
```

The PR description must include:
- What was changed and why
- How to test it
- Screenshots for UI changes
- Known limitations or follow-up work

## Note on the auto-commit from Ruff
The CI auto-commit action uses `♻️ Reformatting by ruff` — this is already valid Gitmoji. Never amend or rebase it out of the history.
