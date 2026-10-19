# Phase 166 R2: Typed (5.3) Witness Audit

This package constructs a typed, read-only candidate for the Toda (5.3) double relation using the existing `expression.py` and `proof.py` model classes. It verifies the ambient source and target dimensions but does **not** verify the mathematical equality, certify an original source, or create `ProofStep` objects.

## Run

Extract to the project root and execute `powershell -ExecutionPolicy Bypass -File .\phase166_r2_typed53\run.ps1` from PowerShell.

The script expects the repository's `sphere_relation2.csv` or the copy in the previous R1 source audit directory. It writes `results/audit_result.json` and `results/typed53_candidates.csv`. The script runs three targeted pytest tests and never invokes the full suite.

No production files are modified. The formula representation is a carefully selected witness, not a general TeX parser or a proof of truth.
