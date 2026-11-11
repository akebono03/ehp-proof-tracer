# EHP Proof Tracer — Phase 174 R64: Sentence Coverage Frontier

This read-only audit inventories all rendered proof paragraphs in the two previously certified sample groups and separates the five R63 witness-checked lines from paragraphs not yet individually reviewed for source relevance.

It does **not** change production code, ProofSteps, proof rules, registered assertions, databases, or citation rendering. The absence of a citation marker is not treated as an error. Source ownership and sentence-level relevance remain distinct concepts. The output is a local JSON report under `LOCALAPPDATA/EHPProofTracerAudit`.

Run `run.ps1 -DryRun` and then `run.ps1`. The installer has no modifications to apply; the script uses repository-relative imports. Focused pytest disables the cache provider. Full-suite tests are reserved for phase closeout.
