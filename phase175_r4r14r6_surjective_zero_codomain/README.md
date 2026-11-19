# Phase 175 R4R14R6 — Generic Zero Codomain Root

This package adds one general, mathematically valid backward proof rule: a surjective homomorphism with zero image has a zero codomain. The candidate is constructed using a type-checked suspension map into an arbitrary eligible zero-group target. It is not restricted to the requested dimension or stem.

The existing Toda (5.9) source and the R4R14R5 generator-zero transport remain unchanged. No group conclusion or source fact is admitted as a new GIVEN. The previous Delta-surjectivity EHP root route remains available.

`installer.py` permits only the reviewed R4R14R5 shared source blob, including a local uncommitted R5 change, and inserts exactly one provider call. It does not stage or commit changes. It writes the full updated shared function to `SHARED_FUNCTION_FULL_JA.md` when executed.

Run `run.ps1 -DryRun`, then `run.ps1` from the package directory. The full test suite is deliberately not run. Actual proof-search status and open goals are saved to a JSON report in the operating system temporary directory. A successful integration gate does **not** claim that the target proof is complete.
