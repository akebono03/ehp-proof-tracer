# EHP Proof Tracer — Phase 174 R63

This audit verifies specific sentence-level source attributions against actual
verified ProofStep ancestry in two completed group queries. It does not modify
production modules, proof rules, literature registrations, or rendering.

The target cases are the cited EHP exactness chain in each query, Toda (5.10),
Proposition 2.7, and one-premise Delta surjectivity from the previously admitted
database group presentation. Assertions must be visible as source-labelled proof
sentences and have source-owning GIVEN ancestors. The exactness chain additionally
requires an actual proof consumer of the typed general source.

This is **not** a proof that every sentence's reference is perfectly relevant.
No "cite all ancestors" policy or automatic centralized rendering is added.

Run `run.ps1 -DryRun`, then `run.ps1` from a checkout into which this archive
was extracted. The script performs only focused tests and disables the pytest
cache provider. Report artifacts are written outside the repository to
`%LOCALAPPDATA%/EHPProofTracerAudit/`.
