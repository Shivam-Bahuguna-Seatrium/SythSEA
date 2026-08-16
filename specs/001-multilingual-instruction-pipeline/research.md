# Research Decisions: Multilingual Synthetic Instruction Research Pipeline

## Decision 1: Python 3.11+ with a typed package and CLI

**Decision**: Use Python 3.11+ with `pyproject.toml`, Pydantic models, Typer CLI
commands, Ruff, mypy, and pytest.

**Rationale**: Python matches the NLP ecosystem required by the project,
supports local and remote model adapters, and is practical for research
notebooks and publication analysis. Pydantic and typed interfaces make the
metadata and stage contracts executable rather than prose-only.

**Alternatives considered**: A notebook-only project was rejected because it
would make resumability, testing, and provenance difficult. A web application
was deferred because the first release is an experiment workflow, not an
end-user product.

## Decision 2: Explicit stage interfaces instead of a mandatory orchestration framework

**Decision**: Implement a small stage protocol with versioned inputs and outputs.
The runner executes a declared graph of roles: profile, resource discovery,
topic/context, generation, language specialist, code-switch validation,
cultural validation, semantic verification, diversity/difficulty, critic,
judge, refinement, quality gate, and deduplication.

**Rationale**: The project must test whether the multi-agent design contributes;
stage-level enable/disable controls make ablations possible and preserve audit
trails. A lightweight graph avoids coupling the research to a fast-changing
agent framework.

**Alternatives considered**: A single multi-agent framework was rejected for the
first release because it can obscure state transitions and make provider access
part of the scientific claim. A single generation prompt is retained as the
Tier B baseline, not as the production architecture.

## Decision 3: Parquet artifacts with a DuckDB experiment catalog

**Decision**: Store datasets, reviews, metrics, errors, and reports as versioned
Parquet or JSON artifacts. Store searchable metadata, run state, provenance
links, checksums, and aggregate analysis in DuckDB.

**Rationale**: This is portable, queryable, efficient for columnar experiment
tables, and usable offline. It supports public and restricted roots without
requiring a hosted database.

**Alternatives considered**: A hosted relational database was rejected for the
pilot because it adds deployment and access dependencies. JSON-only files were
rejected because large experiment tables and language-slice queries become
awkward.

## Decision 4: Adapter-based local and remote model access

**Decision**: Define a common generation adapter interface. Support local
Transformers inference and optional vLLM for open models; support remote teacher
APIs only through adapters that record provider, model, request settings, prompt
version, response metadata, and cost.

**Rationale**: Open-source models improve replication, while teacher-family
comparisons may require remote providers. The adapter boundary prevents a
provider from becoming an undocumented requirement.

**Alternatives considered**: A single commercial teacher was rejected because
access, pricing, and model version changes would threaten reproducibility.

## Decision 5: Validation before expensive evaluation

**Decision**: Apply schema, provenance, language-profile, safety, semantic,
cultural, quality, duplicate, and leakage checks before downstream tuning or
expensive evaluation. Cache every deterministic and model-backed decision with
its checker version.

**Rationale**: This reduces cost and prevents invalid records from contaminating
comparisons. It also makes failure reasons and rejected records auditable.

**Alternatives considered**: Evaluating every raw generated record was rejected
because it wastes compute and makes low-quality volume look like evidence.

## Decision 6: Evaluation protocol

**Decision**: Compare Tier A human seed data, Tier B single-agent synthetic data,
optional Tier D English-to-target translation data, and Tier C full SynthSEA data.
Run language-specific slices first, then code-switching conditions, then
downstream data-efficiency conditions at 1K, 5K, 10K, 25K, and 50K.

Use automated metrics as evidence rather than a single truth source: task
success or exact-match metrics where applicable, language-appropriate
reference-based metrics, semantic similarity, diversity, duplication rate,
safety/quality pass rates, and structured human ratings. Use bootstrap or
permutation intervals and pre-declared comparisons; use multiplicity correction
when many language/condition comparisons are reported.

**Rationale**: The protocol tests generation quality, downstream utility, and
data efficiency separately and prevents aggregate scores from hiding language
differences.

**Alternatives considered**: A single aggregate metric was rejected because it
would violate multilingual and evaluation-rigor principles. LLM-as-judge alone
was rejected; it can be an auxiliary signal with calibration and human checks.

## Decision 7: Human review and adjudication

**Decision**: Language or cultural experts validate the four profiles. Independent
reviewers rate sampled outputs using a versioned rubric. Disagreements,
abstentions, reviewer roles, and adjudication decisions remain separate records.

**Rationale**: Expert profile validation and general quality rating are different
activities. Preserving disagreement avoids false certainty and supports
agreement analysis.

**Alternatives considered**: Automated judgment without human review was
rejected by the constitution and the specification.

## Decision 8: Public and restricted release controls

**Decision**: Every source, record, and artifact receives an access class and
retention rule. Public export traverses only approved public records and emits a
manifest of exclusions; restricted material remains under a separate root.

**Rationale**: The accepted clarification permits useful restricted research
inputs while preventing accidental public disclosure or license violations.

**Alternatives considered**: Public-only data would simplify release but could
exclude important local resources. Unrestricted mixed exports are unacceptable.

## Decision 9: Cost and reliability controls

**Decision**: Add batching, async bounded concurrency, cache keys, retry/backoff,
rate limits, model routing, token/cost accounting, checkpointing, resumable run
state, and a dry-run mode. Deduplicate before expensive downstream evaluation.

**Rationale**: These controls support a feasible RegiCON timeline and prevent
partial failures from becoming silent data loss.

**Alternatives considered**: Unbounded generation was rejected because raw
volume is not the research objective and would make cost unpredictable.

## Decision 10: Downstream adaptation is a separate evaluation track

**Decision**: Treat downstream instruction adaptation as a first-class experiment
stage under `src/synthsea/training/`. It consumes versioned Tier A/B/C/D datasets,
records the adaptation configuration and model checkpoint, and emits separate
language-specific utility results.

**Rationale**: Synthetic-data quality and downstream model utility are different
claims. Recording them separately satisfies evaluation rigor and prevents a
strong generation score from being mistaken for downstream improvement.

**Alternatives considered**: Reporting only generation-quality metrics was
rejected because it cannot test the central data-utility claim.

## Decision 11: Explicit access-class semantics

**Decision**: Use three access classes: `public` for externally releasable
artifacts, `restricted` for approved project research material excluded from
public exports, and `private` for researcher-only material. Public manifests
MUST list excluded restricted and private artifact identifiers.

**Rationale**: Separating restricted and private material makes retention,
sharing, and release review decisions auditable.

**Alternatives considered**: Treating private and restricted as synonyms was
rejected because their permissions may differ.

## Decision 12: Split Apple Silicon training from local chat inference

**Decision**: Use MLX-LM as the Apple Silicon fine-tuning engine and retain the
local Ollama `/api/generate` adapter for interactive chat and small generation
pilots. MLX jobs must record the base model or adapter, MLX-LM version, command,
dataset and split versions, seed, training configuration, macOS version,
available unified memory, logs, checkpoints, and output checksums. The initial
local chat profile remains `qwen2.5:3b`; a fine-tuning model is chosen only from
an MLX-compatible model with documented license and memory requirements.

**Rationale**: MLX is designed for Apple Silicon's unified memory and MLX-LM
supports low-rank and full fine-tuning, including quantized models. Ollama is a
good local inference runtime but not the research training engine. Separating
them keeps chat responsive while giving fine-tuning an explicit, reproducible
job contract.

**Alternatives considered**: Requiring CUDA or a hosted teacher would prevent
local replication. Using Ollama as the fine-tuning engine was rejected because
the needed training configuration, checkpoints, and reproducibility controls are
better represented by MLX-LM. Treating a MacBook pilot as production-scale was
rejected because memory, throughput, and model limits must be reported.