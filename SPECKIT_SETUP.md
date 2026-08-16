# Spec Kit Setup for SynthSEA

This guide installs and uses GitHub Spec Kit with GitHub Copilot in VS Code for the SynthSEA project.

## Prerequisites

- VS Code with GitHub Copilot and Copilot Chat enabled
- Python 3.11 or newer
- Git
- `uv`

Check the prerequisites:

```bash
python3 --version
git --version
uv --version
```

## Install the Specify CLI

Run this from any terminal:

```bash
uv tool install specify-cli
```

Verify the installation:

```bash
specify --version
specify check
```

To update the CLI later:

```bash
specify self check
specify self upgrade
```

## Configure This Project

Open the project folder in VS Code, then run:

```bash
cd /home/azureuser/shivam-dev/SynthSEA
specify init --here --force --integration copilot --script py
```

Verify the Copilot integration:

```bash
specify integration list
```

The project should contain:

- `.specify/` for Spec Kit configuration, templates, scripts, and memory
- `.github/skills/speckit-*` for Copilot Spec Kit skills

## Recommended SynthSEA Workflow

Use GitHub Copilot Chat in this project and run the following skills in order.

### 1. Establish research and engineering principles

```text
/speckit-constitution
```

Use principles covering scientific validity, reproducibility, data governance, culturally sensitive multilingual NLP, statistical evaluation, testing, and transparent reporting.

### 2. Create the baseline specification

```text
/speckit-specify
```

Use the existing project brief as the source:

```text
Use SynthSEA_Master_Research_Implementation_Prompt.md as the source context. Define the research system and reproducible experimental workflow for synthetic instruction generation across Singapore English/Singlish, Malay, Tamil, and Singapore-context Mandarin. Focus on research goals, users, expected outputs, evaluation requirements, risks, and acceptance criteria. Do not choose implementation technologies yet.
```

### 3. Resolve ambiguity before planning

```text
/speckit-clarify
```

Pay particular attention to dataset permissions, language and variety definitions, code-switching scope, model access, annotation protocol, contamination controls, baselines, human evaluation, and statistical significance.

### 4. Create the technical plan

```text
/speckit-plan
```

Include the selected models, data formats, experiment tracking, reproducibility strategy, evaluation harness, storage layout, compute requirements, and test strategy.

### 5. Generate a requirements checklist

```text
/speckit-checklist
```

Review the checklist manually. A checked item means the requirement is sufficiently clear and reviewable; it does not mean the implementation is complete.

### 6. Generate implementation tasks

```text
/speckit-tasks
```

Tasks should be small, dependency-ordered, testable, and mapped to requirements. Include data validation, experiment reproducibility, evaluation, documentation, and safeguards as first-class tasks.

### 7. Analyze the artifacts before implementation

```text
/speckit-analyze
```

Resolve conflicts or missing coverage in the specification, plan, and task list before coding.

### 8. Implement the tasks

```text
/speckit-implement
```

For a large research system, implement one phase at a time and validate each phase before continuing.

### 9. Check for unfinished work

```text
/speckit-converge
```

If it adds tasks, run `/speckit-implement` again and repeat until the project converges.

## Best Practices

These practices are based on the official Spec Kit Quick Start and Reference documentation.

1. Specify the problem and expected outcomes before selecting the technology stack.
2. Keep the constitution stable and treat it as the governing standard for later artifacts.
3. Use clarification before planning whenever requirements, datasets, evaluation, or constraints are ambiguous.
4. Treat the specification, plan, and tasks as connected artifacts. Run analysis before implementation.
5. Keep requirements and evaluation criteria measurable. For SynthSEA, define language coverage, data splits, baselines, metrics, human-review criteria, and reproducibility checks explicitly.
6. Keep generated project artifacts under version control, except for local secrets, credentials, caches, and machine-specific files.
7. Use `specify self check` regularly and upgrade deliberately. Review generated changes after a Spec Kit upgrade.
8. Use `/speckit-converge` after implementation to find gaps between the research specification and the codebase.
9. Keep feature work separate from Spec Kit tooling updates. Update research artifacts only when the intended behavior or methodology changes.
10. Review all generated code and research claims. Spec Kit structures the workflow; it does not replace scientific, security, licensing, or ethics review.

## Useful Commands

```bash
# Check the installed CLI and available tools
specify check

# List installed integrations
specify integration list

# Show CLI help
specify --help
specify init --help

# Upgrade Spec Kit
specify self upgrade
```

## Official Web Sources

- [Spec Kit repository and README](https://github.com/github/spec-kit/blob/main/README.md)
- [Spec Kit Quick Start](https://github.github.io/spec-kit/quickstart.html)
- [Spec Kit Reference](https://github.github.io/spec-kit/reference/overview.html)
- [Agentic SDD reference](https://github.github.io/spec-kit/reference/agentic-sdd.html)
