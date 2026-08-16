# Research Decisions: Springer Conference Paper Generation and Reproducible Research Package

## Decision 1: Venue profile before manuscript rendering

**Decision**: Require an official CFP, author guide, or template reference before
marking a package submission-ready. Store the source, access date, selected
format family, page limit, author mode, required sections, and reference style.

**Rationale**: Springer LNCS, Springer Nature, and conference-specific formats
are not interchangeable. The feature must expose uncertainty rather than guess.

**Alternatives considered**: Defaulting to LNCS was rejected because the venue
may use another Springer or non-Springer format.

## Decision 2: Manifest-first evidence ingestion

**Decision**: Accept only verified experiment manifests with checksums, access
classes, language slices, conditions, metrics, provenance, limitations, and
artifact versions.

**Rationale**: A manuscript must be reproducible from immutable evidence rather
than from conversational context or unstated local files.

**Alternatives considered**: Reading arbitrary result files was rejected because
it makes stale or unreviewed values indistinguishable from primary results.

## Decision 3: Explicit claim status and traceability

**Decision**: Represent each claim as verified, missing, unsupported, restricted,
excluded, or blocked, with references to artifacts or bibliography entries.

**Rationale**: Plausible prose and unverified numbers must never become reported
results. A visible status supports author review and audit.

**Alternatives considered**: Allowing free-form generated prose was rejected by
the constitution's scientific-validity and transparent-reporting principles.

## Decision 4: Template-driven manuscript sections

**Decision**: Generate a fixed section model covering the required conference
sections, with venue-specific additions and explicit missing-evidence markers.

**Rationale**: Deterministic section assembly makes paper structure testable and
supports consistent regeneration when evidence changes.

**Alternatives considered**: One-shot full-paper generation was rejected because
it obscures evidence boundaries and makes partial review difficult.

## Decision 5: Evidence-derived tables and figures

**Decision**: Tables and figures are derived only from verified result artifacts;
each output records source artifact IDs, transformation/query, language slices,
condition IDs, and version.

**Rationale**: Visual artifacts often become detached from the result version
that produced them. Provenance must travel with every visual.

**Alternatives considered**: Manually pasted tables and figures were rejected
because they are difficult to audit and regenerate safely.

## Decision 6: Bibliography validation with human approval

**Decision**: Track bibliography metadata, identifiers, provenance, in-text use,
duplicates, missing fields, and validation status. Human approval remains
required for publication-critical references.

**Rationale**: Citation tools can normalize formatting but cannot guarantee that
a source supports a claim or that generated references are real.

**Alternatives considered**: Treating generated citations as authoritative was
rejected.

## Decision 7: Read-only source boundary

**Decision**: The paper package generator reads source datasets, experiment
outputs, and manifests but writes only under a new package directory. It records
source checksums before and after generation.

**Rationale**: Publication work must not mutate evidence or invalidate previous
runs.

**Alternatives considered**: Updating source reports in place was rejected for
reproducibility and release-safety reasons.

## Decision 8: Reproducibility appendix as a first-class artifact

**Decision**: Generate a structured appendix containing prompts, model versions,
seeds, configurations, dataset versions, evaluation commands, environment data,
artifact checksums, and known limitations.

**Rationale**: Reproducibility details are too important to leave as informal
notes and must be checked independently from manuscript prose.

**Alternatives considered**: A short narrative reproducibility paragraph alone
was rejected because it cannot carry complete run metadata.

## Decision 9: Optional PDF build with truthful status

**Decision**: Provide a builder adapter that detects required document tools and
reports `available`, `failed`, or `unavailable`; source artifacts remain valid
when PDF generation is unavailable.

**Rationale**: A source package can be reviewed in restricted environments, while
false PDF success would mislead authors about submission readiness.

**Alternatives considered**: Making LaTeX or a publisher tool a hard dependency
was rejected because it harms portability.

## Decision 10: Public, restricted, and private package views

**Decision**: Generate an access-aware manifest. Public packages contain only
public-approved artifacts; restricted and private inputs are excluded and listed
by identifier without exposing their contents.

**Rationale**: Aggregate evidence may be releasable even when raw sources are
not, but the access decision must remain auditable.

**Alternatives considered**: A single mixed package was rejected because it risks
license and privacy violations.
