# Phase 169 R10ED: Direct-Sum Narrative Generality Audit

This is a **read-only audit** of the existing R10EC direct-sum narrative projection. It changes no production source, search behavior, Proof Tree, inference rule, bibliography, or public API.

## Prerequisites

- Checked-out `develop` descending from the reviewed `main` commit `f486c3680990066e45d97ca1948654c1eb9ca539`.
- Successfully applied R10EC and R10EC-R1 (the corrected focused cyclic test).
- R10EC `projection.py` matches its reviewed SHA-256 exactly, and the common renderer contains the R10EC projection call.

## Run

From the repository root, extract the zip into `.`, then execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase169_r10ed_direct_sum_generality_audit\run.ps1
```

The runner checks the Git ancestry and source blobs and runs a focused pytest subset, followed by five real screened searches and proof-tree replay checks. The report and rendered narratives appear under this package's `output/` directory.

## Coverage

- 8-stem and 9-stem
- 2-summand and 3-summand direct sums
- 2, 4, 5, 13, and 19 consecutive suspensions
- Fail-closed behavior for missing images, malformed ordering, missing and counterfeit citations, externally used steps, and quoted intermediate steps

## Limitations

A five-case audit is not a proof that every stem or every source group is supported. R10EC intentionally requires at least two suspensions and complete, citation-backed image evidence for each direct-sum summand. The public Web entrypoint, not the projection helper, verifies the Proof Tree before projection. No full pytest suite is run in this phase step.
