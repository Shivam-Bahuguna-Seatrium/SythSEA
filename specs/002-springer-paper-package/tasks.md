---

description: "Task list for the Springer conference paper generation and reproducible research package"
---

# Tasks: Springer Conference Paper Generation and Reproducible Research Package

**Input**: Design documents from `specs/002-springer-paper-package/`

**Tests**: Contract, unit, integration, golden-output, immutability, and smoke tests are included.

## Phase 1: Setup

- [X] T001 Add the paper-package dependency/configuration section to `pyproject.toml`; verify the existing SynthSEA suite remains installable.
- [X] T002 [P] Create `src/synthsea/paper/`, `tests/paper/`, and `reports/paper-packages/` package directories with `__init__.py` files; verify imports resolve.
- [X] T003 [P] Add venue, paper, and fixture configuration files under `configs/paper/`; verify YAML parses with no secrets.
- [X] T004 [P] Add fixture CFP, template metadata, evidence manifest, golden sections, build marker, and bibliography under `tests/paper/fixtures/`; verify fixtures are self-contained.
- [X] T005 [P] Configure paper test discovery and quality settings in `pyproject.toml`; verify `pytest tests/paper` discovers tests.

## Phase 2: Foundational

- [X] T006 [P] Define paper enums, IDs, timestamps, access classes, statuses, and reason codes in `src/synthsea/paper/models.py`; verify invalid statuses are rejected.
- [X] T007 [P] Implement JSON Schema loading and validation for paper contracts in `src/synthsea/paper/contracts.py`; verify valid and invalid fixtures.
- [X] T008 [P] Implement immutable source snapshots and checksums in `src/synthsea/paper/evidence.py`; verify source files remain unchanged.
- [X] T009 [P] Implement public/restricted/private artifact selection in `src/synthsea/paper/package.py`; verify restricted/private content never enters public output.
- [X] T010 [P] Add paper run event metadata in `src/synthsea/paper/events.py`; verify package ID, manifest, venue, stage, and timestamp are recorded.
- [X] T011 Add foundational tests in `tests/paper/unit/test_foundation.py`; verify models, contracts, checksums, access, and output isolation.

## Phase 3: User Story 1 - Establish Venue and Format Requirements (P1 MVP)

- [X] T012 [P] [US1] [FR-001] Test venue profile requirements in `tests/paper/contract/test_venue_profile.py`.
- [X] T013 [P] [US1] [FR-002] Test LNCS, Springer Nature, venue-specific, and non-Springer resolution in `tests/paper/unit/test_template_resolution.py`.
- [X] T014 [P] [US1] [FR-014] Test venue compliance blockers in `tests/paper/integration/test_venue_compliance.py`.
- [X] T015 [P] [US1] [FR-001] Implement `VenueProfile` loading in `src/synthsea/paper/venue.py`.
- [X] T016 [US1] [FR-002] Implement explicit template conflict handling in `src/synthsea/paper/venue.py`.
- [X] T017 [US1] [FR-014] Implement venue compliance checks in `src/synthsea/paper/compliance.py`.
- [X] T018 [US1] [FR-001] Add `synthsea paper venue-profile` in `src/synthsea/cli.py`.

## Phase 4: User Story 2 - Assemble Verified Research Evidence (P1)

- [X] T019 [P] [US2] [FR-003] Add evidence fixtures in `tests/paper/fixtures/evidence/manifest.json`.
- [X] T020 [P] [US2] [FR-003] Test evidence manifest contracts in `tests/paper/contract/test_evidence_manifest.py`.
- [X] T021 [P] [US2] [FR-004] Test claim-to-evidence references in `tests/paper/unit/test_claims.py`.
- [X] T022 [P] [US2] [FR-006] Test source immutability in `tests/paper/integration/test_source_immutability.py`.
- [X] T023 [P] [US2] [FR-003] Implement evidence verification in `src/synthsea/paper/evidence.py`.
- [X] T024 [P] [US2] [FR-004] Implement `PaperClaim` validation in `src/synthsea/paper/claims.py`.
- [X] T025 [US2] [FR-020] Implement access-aware evidence views in `src/synthsea/paper/package.py`.
- [X] T026 [US2] [FR-003] Add `synthsea paper evidence-check` in `src/synthsea/cli.py`.

## Phase 5: User Story 3 - Generate the Manuscript Package (P1)

- [X] T027 [P] [US3] [FR-007] Add required-section fixtures in `tests/paper/fixtures/golden/expected_sections.json`.
- [X] T028 [P] [US3] [FR-008] [FR-009] Test four-language result ordering in `tests/paper/unit/test_language_result_sections.py`.
- [X] T029 [P] [US3] [FR-010] Test visual provenance in `tests/paper/unit/test_visual_artifacts.py`.
- [X] T030 [P] [US3] [FR-011] Test appendix completeness in `tests/paper/unit/test_reproducibility_appendix.py`.
- [X] T031 [P] [US3] [FR-005] [FR-017] Test anti-fabrication behavior in `tests/paper/integration/test_no_fabrication.py`.
- [X] T032 [P] [US3] [FR-007] Implement section assembly in `src/synthsea/paper/sections.py`.
- [X] T033 [P] [US3] [FR-010] Implement table and figure metadata in `src/synthsea/paper/tables.py` and `src/synthsea/paper/figures.py`.
- [X] T034 [P] [US3] [FR-011] Implement reproducibility appendix assembly in `src/synthsea/paper/reproducibility.py`.
- [X] T035 [P] [US3] [FR-012] Implement bibliography handling in `src/synthsea/paper/citations.py`.
- [X] T036 [US3] [FR-007] Implement deterministic manuscript rendering in `src/synthsea/paper/renderer.py`.
- [X] T037 [US3] [FR-015] [FR-019] Implement package assembly and manifests in `src/synthsea/paper/package.py`.
- [X] T038 [US3] [FR-015] Add `synthsea paper generate` in `src/synthsea/cli.py`.

## Phase 6: User Story 4 - Validate Claims, Citations, and Reproducibility (P1)

- [X] T039 [P] [US4] [FR-004] Test claim traceability in `tests/paper/contract/test_claim_traceability.py`.
- [X] T040 [P] [US4] [FR-012] Test bibliography validation in `tests/paper/unit/test_citations.py`.
- [X] T041 [P] [US4] [FR-013] Test ethics and limitations in `tests/paper/unit/test_ethics_validation.py`.
- [X] T042 [P] [US4] [FR-011] Test reproducibility validation in `tests/paper/unit/test_reproducibility_validation.py`.
- [X] T043 [P] [US4] [FR-018] Test readiness reporting in `tests/paper/integration/test_readiness_report.py`.
- [X] T044 [P] [US4] [FR-004] Implement claim/evidence graph validation in `src/synthsea/paper/claims.py`.
- [X] T045 [P] [US4] [FR-012] Implement bibliography validation in `src/synthsea/paper/citations.py`.
- [X] T046 [P] [US4] [FR-013] Implement ethics and threat-to-validity checks in `src/synthsea/paper/compliance.py`.
- [X] T047 [P] [US4] [FR-011] Implement reproducibility validation in `src/synthsea/paper/reproducibility.py`.
- [X] T048 [US4] [FR-018] Implement readiness report generation in `src/synthsea/paper/compliance.py`.
- [X] T049 [US4] [FR-018] Add `synthsea paper validate` in `src/synthsea/cli.py`.

## Phase 7: User Story 5 - Build and Review Submission Outputs (P2)

- [X] T050 [P] [US5] [FR-016] Add document-tool fixtures in `tests/paper/fixtures/build/`.
- [X] T051 [P] [US5] [FR-014] Test page, asset, figure, and bibliography compliance in `tests/paper/unit/test_builder_compliance.py`.
- [X] T052 [P] [US5] [FR-015] Test final package contract in `tests/paper/contract/test_paper_package.py`.
- [X] T053 [P] [US5] [FR-016] Test unavailable PDF behavior in `tests/paper/integration/test_optional_pdf_build.py`.
- [X] T054 [P] [US5] [FR-016] Implement optional document-tool detection in `src/synthsea/paper/builder.py`.
- [X] T055 [P] [US5] [FR-014] Implement compliance checks in `src/synthsea/paper/compliance.py`.
- [X] T056 [US5] [FR-015] Implement package build metadata in `src/synthsea/paper/package.py`.
- [X] T057 [US5] [FR-016] Add `synthsea paper build` in `src/synthsea/cli.py`.

## Phase 8: Polish

- [X] T058 [P] [FR-006] Add source immutability smoke checks in `tests/paper/smoke/test_source_immutability.py`.
- [X] T059 [P] [FR-018] Add the 10,000-item validation benchmark in `tests/paper/smoke/test_paper_performance.py`.
- [X] T060 [P] [FR-015] Add paper-package documentation in `docs/paper-package.md`.
- [X] T061 [P] [FR-018] Run the full paper suite, Ruff, and mypy from `quickstart.md`.

## Dependencies and Execution Order

- Setup T001-T005 precedes foundation T006-T011.
- US1 T012-T018 establishes the approved venue profile MVP.
- US2 T019-T026 establishes immutable evidence and claim validation.
- US3 T027-T038 generates the manuscript package.
- US4 T039-T049 validates claims, citations, ethics, and reproducibility.
- US5 T050-T057 handles optional builds and final compliance.
- Polish T058-T061 runs after all desired stories.

## Parallel Opportunities

- T002-T005, T006-T011, T012-T014, T019-T022, T027-T031, T039-T043, T050-T053, and T058-T060 are parallel groups.

## MVP and Completion

The MVP is US1 plus US2: an approved venue profile and verified, immutable evidence package. All 61 tasks are complete and validated by the paper test suite, Ruff, mypy, and CLI smoke commands.
