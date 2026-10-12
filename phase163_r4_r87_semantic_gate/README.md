# Phase 163 R4-R87 — Semantic Registration Gate

This package reads the R86 claim review catalog, validates nine source-grounded claims, and produces a Japanese report of scope requirements and blockers. It does not certify mathematical correctness, modify production source modules, allocate permanent IDs, or connect to proof search.

Run `run.ps1` from the repository root after extracting this ZIP there. The runner uses `phase163_r4_r86_output/claim_review_catalog.json` as the authoritative input and requires a byte-for-byte match with the bundled R86 snapshot to avoid silently switching inputs. It runs only focused pytest.
