# Feature Specification: Deep Research and Final Reproducible Report

**Feature Branch**: `003-deep-research-final-report`

**Created**: 2026-08-13

**Status**: Draft

**Input**: User description: "Create a complete research-to-publication workflow for SynthSEA that performs evidence-grounded novelty and literature research, verifies RegiCON 2026 requirements, identifies missing experiments and artifacts, and generates a final reproducible report without fabricating results."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build an Evidence-Grounded Research Dossier (Priority: P1)

As a principal researcher, I want a documented literature, novelty, venue, and scientific-requirements dossier so that I can determine whether SynthSEA is defensible and suitable for the target venue before claiming results.

**Why this priority**: A final report is not trustworthy unless its novelty, scope, related work, and venue requirements are verified first.

**Independent Test**: Run the dossier workflow against the project prompt and available sources, then inspect a versioned research dossier containing source records, retrieval dates, novelty comparisons, unresolved questions, and venue requirements.

**Acceptance Scenarios**:

1. **Given** the SynthSEA project description and target venue, **When** research is performed, **Then** the dossier records verifiable sources, URLs or identifiers, retrieval dates, findings, and limitations.
2. **Given** a related-work source, **When** it is added to the literature matrix, **Then** the record contains title, authors, year, venue, DOI or URL, contribution, limitation, and relevance without invented fields.
3. **Given** unavailable or conflicting official venue information, **When** the dossier is validated, **Then** the requirement is marked unresolved and cannot be treated as an approved formatting rule.
4. **Given** competing claims of novelty, **When** the novelty analysis is generated, **Then** it distinguishes prior art, SynthSEA differences, evidence gaps, and hypotheses requiring experiments.

### User Story 2 - Define the Research and Experiment Readiness Plan (Priority: P1)

As an experimental ML researcher, I want research questions, hypotheses, datasets, baselines, ablations, metrics, statistics, human review, and ethics requirements recorded as an executable matrix so that missing evidence is explicit.

**Why this priority**: The project cannot produce a genuine final report until every claim has a defined test and every test has defined evidence requirements.

**Independent Test**: Generate the requirements matrix from the dossier and inspect whether each research question maps to hypotheses, conditions, data splits, metrics, sample sizes, artifacts, and acceptance rules for the four target language settings.

**Acceptance Scenarios**:

1. **Given** the four target language settings, **When** the experiment matrix is generated, **Then** Singapore English/Singlish, Malay, Tamil, and Singapore-context Mandarin have separate data, quality, and evaluation requirements before aggregation.
2. **Given** a proposed claim, **When** it is added to the evidence matrix, **Then** the matrix requires an experiment identifier, artifact path, metric definition, comparison, uncertainty information, and limitation.
3. **Given** missing data, reviewers, compute, models, or licenses, **When** readiness is checked, **Then** the gap is classified as blocking, warning, or out of scope with an actionable resolution.
4. **Given** a human-evaluation requirement, **When** the protocol is recorded, **Then** it specifies sampling, rubric, reviewer qualifications, privacy handling, agreement analysis, and adjudication rules.

### User Story 3 - Run and Register Reproducible Research Evidence (Priority: P1)

As a research engineer, I want exact experiment commands and immutable evidence manifests so that primary results can be reproduced and traced to versioned inputs, configurations, models, prompts, seeds, and environments.

**Why this priority**: A report must be based on executed, verifiable evidence rather than planned or simulated output.

**Independent Test**: Execute a bounded CPU-safe fixture run and register its outputs, then verify that the manifest contains checksums, configuration, environment, command, status, language slice, access class, and provenance while source inputs remain unchanged.

**Acceptance Scenarios**:

1. **Given** a declared experiment condition, **When** the run starts, **Then** it records the command, inputs, dataset versions, model versions, prompts, decoding settings, seeds, environment, and status before accepting results.
2. **Given** a failed, partial, restricted, or stale artifact, **When** evidence registration runs, **Then** it preserves the failure or restriction and excludes it from verified primary-result claims.
3. **Given** a registered result, **When** its checksum and provenance are revalidated, **Then** the system detects changes and blocks stale evidence from final reporting.
4. **Given** CPU fixtures and real research runs, **When** readiness is reported, **Then** fixture evidence is visibly distinguished from publication evidence.

### User Story 4 - Generate and Validate the Final Research Report (Priority: P1)

As a research author, I want a complete report and reproducible package generated only from verified evidence so that every result, table, figure, citation, and conclusion is auditable before submission.

**Why this priority**: This is the publication-facing outcome of SynthSEA and must fail closed when evidence or venue requirements are incomplete.

**Independent Test**: Supply an approved venue profile and verified fixture evidence, generate the report package, then validate section completeness, claim coverage, citations, language slices, reproducibility metadata, ethics, restrictions, and release status.

**Acceptance Scenarios**:

1. **Given** verified evidence and an approved venue profile, **When** final report generation runs, **Then** it creates all required report sections, references, tables, figures, appendices, provenance records, and validation outputs.
2. **Given** a numerical claim without verified evidence, **When** generation runs, **Then** it omits or marks the claim as `[MISSING EVIDENCE]` and never invents a value.
3. **Given** results for the four target language settings, **When** results are rendered, **Then** each setting is reported separately before any aggregate result.
4. **Given** missing official venue information, required evidence, citations, or document tools, **When** final validation runs, **Then** release status is blocked with actionable issues and preserved source artifacts.
5. **Given** a complete package, **When** report validation runs, **Then** every claim, table, figure, and bibliography entry resolves to a verified artifact or an approved source record.

### Edge Cases

- RegiCON 2026 requirements may be unavailable, changed, or inconsistent across official sources; the workflow must preserve source versions and mark unresolved rules.
- The target venue may not use a Springer format; the workflow must report the actual venue format instead of forcing a generic template.
- Literature sources may be inaccessible, duplicated, retracted, or missing identifiers; they must be flagged rather than completed by guesswork.
- The four language settings may have unequal data, reviewer, or metric coverage; the report must disclose the imbalance and avoid misleading aggregates.
- A claim may be plausible but unsupported, contradicted by results, or based on restricted evidence; it must remain blocked or qualified.
- A result artifact may change after registration; checksum or manifest mismatch must invalidate dependent claims.
- A human evaluation may contain disagreement, abstention, small samples, privacy constraints, or unqualified reviewers; the limitation must remain visible.
- An experiment may fail because of model access, rate limits, missing dependencies, compute limits, or licensing restrictions; partial outputs must not count as completed evidence.
- A generated table or figure may be stale, transformed incorrectly, or inconsistent with the selected manifest; validation must reject or quarantine it.
- LaTeX, bibliography tools, fonts, or venue templates may be unavailable; source and validation artifacts must still be produced with an unavailable-build status.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST create a versioned research dossier containing novelty analysis, literature records, venue requirements, scientific requirements, unresolved questions, source URLs or identifiers, and retrieval dates.
- **FR-002**: The system MUST record only verifiable academic and official venue sources and MUST preserve source provenance, access status, and limitations.
- **FR-003**: The system MUST record literature title, authors, year, venue, DOI or URL, contribution, limitation, relevance, and verification status without fabricating missing citation data.
- **FR-004**: The system MUST compare SynthSEA against prior multilingual, synthetic-data, multi-agent, code-switching, culturally grounded, and Southeast Asian NLP methods and distinguish evidence-backed novelty from hypotheses.
- **FR-005**: The system MUST verify the official RegiCON 2026 CFP, author guide, template, page limits, formatting, required sections, submission dates, anonymization, and citation rules when official sources are available.
- **FR-006**: The system MUST mark unavailable, conflicting, or unverified venue requirements as unresolved and MUST block approval based on unresolved requirements.
- **FR-007**: The system MUST define research questions, hypotheses, datasets, licenses, language terminology, baselines, ablations, controls, metrics, sample sizes, seeds, uncertainty, significance tests, and acceptance criteria.
- **FR-008**: The system MUST represent Singapore English/Singlish, Malay, Tamil, and Singapore-context Mandarin as separate research and reporting slices before aggregation.
- **FR-009**: The system MUST define automatic quality, downstream, human, statistical, safety, cultural, and error-analysis evidence requirements where relevant to each claim.
- **FR-010**: The system MUST maintain a claim-to-evidence matrix mapping each claim, number, table, figure, and conclusion to an experiment identifier, verified artifact, transformation, source citation, and limitation.
- **FR-011**: The system MUST classify evidence as verified, provisional, missing, unsupported, restricted, excluded, stale, failed, or fixture and MUST prevent non-verified evidence from supporting primary-result claims.
- **FR-012**: The system MUST define exact reproducible commands and expected artifacts for each required experiment and MUST record inputs, outputs, configuration, prompts, model versions, decoding settings, seeds, software environment, and checksums.
- **FR-013**: The system MUST keep report generation read-only with respect to source datasets, experiment outputs, and original manifests.
- **FR-014**: The system MUST generate the complete final report structure: title, abstract, keywords, introduction, research questions, related work, research gap, methodology, architecture, dataset design, experimental protocol, baselines, ablations, results, statistical analysis, human evaluation, error analysis, cultural and ethical considerations, limitations, discussion, conclusion, reproducibility, data and code availability, acknowledgements, references, and appendices.
- **FR-015**: The system MUST generate tables and figures only from verified artifacts and MUST record source artifact, transformation, language slice, version, and caption metadata.
- **FR-016**: The system MUST include only verified citations in final claims and MUST validate bibliography fields, identifiers, duplicates, provenance, and in-text usage.
- **FR-017**: The system MUST preserve `[MISSING EVIDENCE]` markers or equivalent explicit statuses for unresolved sections and MUST never invent results, participants, citations, reviewer outcomes, or quantitative values.
- **FR-018**: The system MUST validate dataset licensing, privacy, consent, cultural context, representation gaps, ethics review, model access, copyright, contamination, leakage, and threats to validity.
- **FR-019**: The system MUST generate research dossier, literature matrix, novelty analysis, venue record, experimental requirements matrix, evidence matrix, reproducibility checklist, risk register, report schema, and updated quickstart documentation.
- **FR-020**: The system MUST generate manuscript source, bibliography, figures, tables, appendices, evidence manifests, validation reports, build instructions, and release metadata as separate versioned artifacts.
- **FR-021**: The system MUST provide CLI workflows to research, register evidence, generate, validate, and optionally build the final report package.
- **FR-022**: The system MUST report an unavailable PDF-build status when required document tools are missing and MUST never report a false successful build.
- **FR-023**: The system MUST block final release when required venue approval, evidence coverage, citation validation, reproducibility metadata, ethics checks, or required sections are incomplete.
- **FR-024**: The system MUST preserve negative, null, failed, and materially inconsistent results in research records and reflect them in limitations or conclusions where relevant.

### Key Entities

- **ResearchDossier**: Versioned research record containing sources, findings, novelty analysis, venue requirements, unresolved questions, and research scope.
- **SourceRecord**: Academic, official, dataset, or technical source with identifier, provenance, retrieval date, verification status, and permitted use.
- **ResearchQuestion**: Question with hypotheses, scope, language slices, variables, evidence requirements, and acceptance criteria.
- **ExperimentRequirement**: Planned experiment condition with data, baseline, ablation, metrics, sample size, statistical method, command, and expected artifacts.
- **EvidenceRecord**: Immutable experiment or evaluation artifact with checksum, access class, provenance, status, language slice, and manifest reference.
- **ClaimEvidenceLink**: Mapping between a report claim and its supporting evidence, citation, transformation, and limitation.
- **ReportPackage**: Versioned final report source, references, tables, figures, appendix, validation results, build output, and release manifest.
- **ReadinessReport**: Blocking issues, warnings, evidence coverage, citation status, reproducibility status, ethics status, and release decision.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: The research dossier records 100% of included sources with provenance, retrieval date, verification status, and a DOI, URL, or explicit unavailable identifier.
- **SC-002**: Every research question and publication claim maps to a defined experiment or documented analysis, required artifact, metric, comparison, and limitation.
- **SC-003**: The readiness workflow identifies 100% of deliberately missing venue rules, unsupported claims, missing evidence, stale artifacts, absent citations, and incomplete reproducibility fields in fixture validation.
- **SC-004**: The final report reports all four target language settings separately before any aggregate result and flags missing slices explicitly.
- **SC-005**: Every verified primary result has a reproducible command, versioned inputs, configuration, model and prompt metadata, seed, environment record, checksum, and evaluation output.
- **SC-006**: A generated package contains the research dossier, literature matrix, novelty analysis, venue record, requirements matrix, evidence matrix, report source, references, tables, figures, reproducibility appendix, validation report, and release manifest.
- **SC-007**: 100% of numerical claims, tables, and figures in a release-ready package resolve to verified evidence or an approved cited source.
- **SC-008**: Public packages contain zero restricted or private source artifacts and document all excluded artifacts and permitted aggregate evidence.
- **SC-009**: Report generation leaves source datasets, experiment outputs, and original manifests byte-for-byte unchanged.
- **SC-010**: Missing PDF tooling results in an explicit unavailable status and never a false successful build.
- **SC-011**: A researcher can identify every blocking issue and the next resolution action from the readiness report without private agent-session state.

## Assumptions

- The official RegiCON 2026 CFP and author guidance are authoritative; a generic Springer template is not accepted without venue evidence.
- Feature 003 consumes and validates Feature 001 experiment artifacts and Feature 002 paper-package capabilities; it does not fabricate or silently replace missing experiments.
- Real primary results require researcher-approved datasets, models, licenses, human-review procedures, compute access, and experiment execution outside CPU fixtures when necessary.
- Citation discovery may require human approval, while the workflow records verification and prevents unverified sources from supporting final claims.
- Final author names, affiliations, acknowledgements, funding, and legal declarations are supplied by the research team.
- The first release targets one approved venue at a time and supports local deterministic fixtures for testing.

## Out of Scope

- Inventing or estimating missing research results, citations, participants, or venue rules.
- Guaranteeing novelty, acceptance, or publisher compliance without expert review and official source evidence.
- Replacing qualified linguistic review, community consultation, ethics review, peer review, or author approval.
- Modifying source datasets, experiment outputs, or original evidence manifests during report generation.
- Automatic access to paywalled or private sources without authorized credentials.
- Publisher submission APIs, camera-ready upload automation, or multi-venue formatting beyond the approved first venue.