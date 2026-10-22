# Phase 168 R2-8(1) Citation Mismatch Audit

This is a read-only diagnostic of nine unresolved typed literature citation boundaries.
It compares the requested group, concrete typed Relation, group-structure type,
cyclic order, generator/presentation, and registered publication/component positions.
No source code in the repository is patched, and no conclusions are added as GIVEN.

Run `powershell -ExecutionPolicy Bypass -File .\\phase168_r2_8_1_citation_mismatch_audit\\run.ps1`
from the project root. Inspect `output/citation_mismatch.json` for complete per-assertion detail.
Only limited tests run; full pytest is reserved for the end of Phase 168.
