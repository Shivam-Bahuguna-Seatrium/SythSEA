<!--
Sync Impact Report
- Version change: scaffold -> 1.0.0
- Modified principles: replaced five generic scaffold principles with seven
	SynthSEA research and engineering principles
- Added sections: Research Constraints; Development Workflow
- Removed sections: none; generic scaffold guidance was replaced
- Follow-up TODOs: none
-->

# SynthSEA Constitution

## Core Principles

### I. Scientific Validity
Every research claim MUST be supported by measurable evidence from a defined
experiment, evaluation, or documented analysis. Claims MUST identify their
scope, assumptions, comparison point, and limitations. The specification,
implementation, and paper-facing results MUST distinguish observed results
from hypotheses and interpretation. This prevents plausible-sounding system
behavior from being presented as scientific evidence.

### II. Reproducibility
Datasets, dataset versions, data splits, configurations, random seeds, prompts,
model versions, dependency versions, environment details, and evaluation
scripts MUST be tracked for every reported experiment. A documented command or
workflow MUST reproduce each primary result from versioned inputs. Any result
that cannot be reproduced MUST be labeled accordingly and excluded from claims
of fully reproducible performance.

### III. Responsible Data Stewardship
The project MUST respect dataset licenses, privacy requirements, consent
conditions, cultural context, and the representation of relevant language
communities. Data provenance, collection or acquisition method, permitted use,
filtering, personal-data handling, and known representation gaps MUST be
documented. The project MUST NOT infer that a language variety is low-resource
without evidence supporting that characterization.

### IV. Multilingual and Cultural Quality
Singapore English and Singlish, Malay, Tamil, and Singapore-context Mandarin
MUST be evaluated separately before aggregate results are reported. Experiments
MUST document language variety, script, code-switching behavior, cultural
context, and resource availability for each evaluation slice. Aggregate scores
MUST NOT conceal meaningful differences between languages or varieties.

### V. Evaluation Rigor
Research evaluations MUST include relevant baselines and MUST define the data
split, metrics, sample sizes, and acceptance criteria in advance. Where the
research question requires it, evaluations MUST include ablations, automated
metrics, human evaluation, error analysis, and statistical significance or
uncertainty analysis. Synthetic data quality MUST be evaluated independently
from downstream model performance so that improvements are not attributed to
the wrong mechanism.

### VI. Engineering Quality
Implementation MUST use modular components with clear interfaces, automated
tests for critical behavior, type checking where supported, and documentation
for setup and operation. Data and experiment pipelines MUST be deterministic
where practical, or MUST record all sources of nondeterminism. Changes MUST
preserve a runnable path for validation and MUST include focused checks for
new or modified behavior.

### VII. Transparent Reporting
Reports MUST disclose limitations, failure cases, contamination and leakage
risks, compute requirements, model access constraints, licensing constraints,
and ethical risks. Results MUST include enough methodological detail for a
reviewer to assess validity without relying on undocumented agent behavior or
private local state. Negative, null, and materially inconsistent results MUST
be retained in research records and considered in conclusions.

## Research Constraints

SynthSEA MUST maintain explicit records for language and variety definitions,
data provenance, consent and licensing status, annotation or human-review
protocols, model and prompt configuration, experiment identifiers, and
evaluation outputs. The project MUST define separate reporting slices for the
four target language settings and MUST document why any additional slice,
metric, or exclusion is included. Security, privacy, and ethical review MUST
precede the use of sensitive or community-derived data in generation or
evaluation workflows.

## Development Workflow

Work MUST proceed from a reviewed specification to clarification, technical
planning, task generation, consistency analysis, implementation, and
convergence review. Every implementation task MUST map to a requirement or
quality constraint and MUST have an observable completion check. Before a
primary result is accepted, the project MUST run the relevant tests, validate
data and configuration provenance, execute the evaluation workflow, and record
the resulting artifacts. Code review and research review MUST verify
constitution compliance before publication-facing claims are finalized.

## Governance

This constitution is the governing standard for SynthSEA specifications,
implementation decisions, experiments, evaluations, and research reporting.
When another project document conflicts with it, the conflict MUST be resolved
by amending the constitution or explicitly documenting an approved exception.

Amendments MUST describe the motivation, affected principles, compatibility
impact, and required follow-up work. Versioning follows semantic versioning:
MAJOR for incompatible governance changes or principle removal, MINOR for new
principles or materially expanded requirements, and PATCH for clarifications
that do not change obligations. Each amendment MUST update the sync impact
report and last-amended date. Compliance MUST be reviewed during specification,
planning, implementation review, and before publication or release of primary
results.

**Version**: 1.0.0 | **Ratified**: 2026-08-13 | **Last Amended**: 2026-08-13
