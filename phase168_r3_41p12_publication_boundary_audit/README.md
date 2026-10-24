# R3-41P12 Publication Boundary Audit

This audit inspects the publication precedence of registered GIVEN steps along the actual public Web route. It does not modify application code, existing tests, or reference registries. The result of a source screening or a citation match is never treated as automatic proof of publication precedence.

Extract this package at the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase168_r3_41p12_publication_boundary_audit\run.ps1`.

The script runs focused tests only and creates a dated `output/review_bundle_*.zip`. Each group is compared byte-for-byte with the frozen narrative obtained in R3-41P11. The `publication_certified` result is true only if a positioned citing assertion is resolved and **every** used GIVEN precedes it according to the existing publication-order rule. If a citing assertion cannot be resolved, the audit reports `UNVERIFIABLE_TARGET`; it does not certify the proof. This audit does not certify mathematical truth or the validity of GIVEN source texts.
