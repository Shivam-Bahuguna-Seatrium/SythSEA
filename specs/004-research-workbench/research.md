# Feature 004 Research Decisions

## Decision: Use React with Vite for the research workspace

**Rationale**: The application needs dense, responsive screens for tables,
job status, provenance, and chat. A React client can keep workspace state local
to each view while a FastAPI backend remains authoritative for governance and
research artifacts. The UI will use a restrained laboratory-workbench visual
language: an off-white canvas, charcoal text, moss green for verified states,
amber for pending work, and vermilion for blockers. Lucide icons are used for
tool actions, and all workflow pages are direct operational views rather than a
marketing landing page.

**Alternatives considered**: A server-rendered HTML interface was rejected
because chat streaming, long-running job monitoring, and dense client-side
comparison interactions would become harder to maintain. A dashboard-only
design was rejected because ingestion and provenance require detail workflows.

## Decision: Use FastAPI as a local governance boundary

**Rationale**: Existing SynthSEA is a typed Python pipeline. FastAPI can expose
the existing Pydantic validation and write only through a small service layer,
keeping access-class checks and provenance rules off the browser. The API will
be local-first and will not expose the DuckDB database directly.

**Alternatives considered**: Letting the React app read files or query DuckDB
directly was rejected because it would bypass access restrictions and make run
state inconsistent.

## Decision: Model fine-tuning as a persistent job, not a request-bound task

**Rationale**: Training duration is variable and a workstation can lack memory
or an eligible model. The UI needs acknowledgement quickly while job execution,
logs, artifacts, cancellation, and failures persist independently. A completed
job remains an execution record, not research evidence until downstream
evaluation is registered.

**Alternatives considered**: Running fine-tuning inside a synchronous HTTP
request was rejected because browser timeouts obscure progress and failures.

## Decision: Use MLX-LM for Apple Silicon fine-tuning through FastAPI

**Rationale**: MLX is built for Apple Silicon's unified-memory architecture and
MLX-LM supports low-rank and full fine-tuning of compatible, including
quantized, models. FastAPI owns job submission, command construction, logs,
cancellation, checkpoint registration, and reproducibility metadata; React only
requests and observes job state. The system records model license, MLX-LM
version, command, base model, adapter configuration, dataset/split versions,
seed, macOS version, and unified-memory limits.

**Alternatives considered**: Ollama was rejected as the fine-tuning engine. It
remains the local chat runtime. Client-side MLX calls were rejected because they
would make job state, artifacts, and access controls non-auditable.

## Decision: Use the existing local Ollama adapter for chat

**Rationale**: Feature 001 already has a local Ollama adapter with model tag,
seed, temperature, timeout, and token metadata. The chat service reuses that
adapter and records each interaction as exploratory. It must not silently use a
remote model or substitute a different local model.

**Alternatives considered**: Client-side calls to Ollama were rejected because
they would bypass centralized access classification, logs, and reproducibility
metadata.

## Decision: Keep local chat separate from experiment execution

**Rationale**: Chat supports prompt discovery and model inspection. An explicit
promotion action with provenance and access review is required before a chat
turn can become a prompt template, candidate dataset record, or experiment
input. This protects the scientific distinction between exploration and
measured evidence.

**Alternatives considered**: Automatically saving chat text as dataset content
was rejected because it would create unreviewed, potentially restricted data.

## Decision: Show research states directly in every view

**Rationale**: The workspace needs clear visible status for verified, pending,
restricted, fixture, stale, failed, and blocked artifacts. Every aggregate view
must disclose missing language slices, and readiness cannot show a green state
when venue, citations, ethics, or evidence are incomplete.

**Alternatives considered**: Hiding unavailable data and presenting only
successful runs was rejected because it would violate transparent reporting.

## Practical Local Pilot

1. Run the FastAPI service locally against the current `experiments/`,
   `research/`, and `reports/` roots.
2. Start the React development server.
3. Use the dataset intake page with a CPU-safe fixture first.
4. Select the local Ollama `qwen2.5:3b` profile and send a labeled exploratory
   chat message.
5. Create a fixture fine-tuning job, inspect its job record, then run the
   existing downstream evaluation workflow before considering any research claim.