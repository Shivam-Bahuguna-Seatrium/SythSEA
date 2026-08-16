# Paper Package Plan Validation Quickstart

This guide validates the paper-generation design using fixture evidence. It
must not modify the existing SynthSEA datasets, experiment results, or original
manifests.

## Prerequisites

- Python 3.11 or newer
- The completed SynthSEA pipeline from `specs/001-multilingual-instruction-pipeline/`
- An official conference CFP or author guide
- A candidate Springer or venue-specific template reference
- A small verified fixture evidence manifest
- Optional LaTeX/BibTeX tools for PDF compilation

## Validation sequence

1. Create a venue profile from the official CFP and record the access date,
   template family, page limit, author mode, required sections, and reference
   style.
2. Validate the venue profile against
   [venue-profile.schema.json](contracts/venue-profile.schema.json).
3. Ingest a verified evidence manifest containing Tier A/B/C/D conditions,
   four language slices, metrics, limitations, access classes, and checksums.
4. Reject a fixture manifest with a missing checksum, inconsistent experiment
   ID, or unverified artifact.
5. Create verified, missing, unsupported, restricted, and excluded claim
   fixtures; verify only verified claims can become asserted results.
6. Generate manuscript sections, tables, figures, bibliography, and the
   reproducibility appendix from the verified fixture.
7. Validate the paper package against
   [paper-package.schema.json](contracts/paper-package.schema.json).
8. Confirm that every number, table, and figure resolves to evidence or a
   source citation and that all four language slices precede aggregate results.
9. Build a public package and verify restricted/private artifact identifiers are
   excluded from content but retained in the exclusion manifest.
10. Run the optional PDF builder. If tools are absent, verify the package reports
    `unavailable` and retains source files and compliance results.
11. Snapshot source checksums before and after generation and verify they are
    identical.

## Expected checks

```bash
pytest tests/paper
ruff check src/synthsea/paper tests/paper
mypy src/synthsea/paper
```

The final readiness report MUST distinguish blocking issues, warnings, missing
results, unsupported claims, citation issues, reproducibility status, ethics
status, and release status.
