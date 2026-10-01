# Developer Documentation

Welcome to the Cross Renamer Tool developer documentation. This section is for TDs who want to contribute to the tool, understand its internals, or extend it for their studio's needs.

[Tutorials](tutorials/){ .md-button }
[How-to Guides](how-to-guides/){ .md-button }
[References](references/){ .md-button }
[Explanations](explanations/){ .md-button }

## Quick links
**New contributor?** Start with the [Tutorials: Set up the development](tutorials/setup_dev_environment/), then follow [Tutorials: Add feature end to end](tutorials/add_a_feature/).  
**Adding a feature?** Go straight to [Tutorials: Add feature end to end](tutorials/add_a_feature/).  
**Understanding the codebase?** Read [References: Architecture](references/architecture/) first, then [References: Design Choices](references/design_choices/).  
**Before pushing?** Check the [References: Code Style Guide](references/code_style_guide/) and run the [How-to Guides: CI/CD locally]().

## Tech stack at a glance
 
| Tool | Role |
|---|---|
| Python 3.11 | Language |
| PySide6 | UI framework |
| Maya 2024+ | Target DCC |
| Ruff | Linter + formatter |
| unittest | Test framework |
| MkDocs + Material | Documentation |
| GitHub Actions | CI/CD |
 
See [References: Technical Choices](references/technical_choices/) for the full rationale behind each choice.