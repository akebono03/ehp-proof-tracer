# Phase 174 R3-R7-R39 — Source-bound Generator-Zero Proof Frontier

This is a read-only, source-guarded audit. It uses actual registered Toda (5.9) literature leaves and the existing generic typed ProofStep inference engine. It does not introduce a group-specific narrative, proof rule, GIVEN, or production source change.

The audit reconstructs the actual typed inference for `E(nu_5 eta_8^2)=0` using existing stable suspension, composition, associativity, and zero-left-factor rules. It separately checks the admitted earlier DB prior for the cyclic group presentation. The R6 zero-image rule requires an **INFERENCE** presentation: an adopted DB prior **GIVEN** cannot be relabeled as such. No zero-image or root completion is claimed.

Unpack the ZIP into the repository root and run `run.ps1 -DryRun`, then `run.ps1` in PowerShell. The script runs focused pytest groups, never the full suite. Reports are written under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r39`.

All code changes are limited to this new audit package. Existing APIs, search order, citations, and presentation behavior are preserved.
