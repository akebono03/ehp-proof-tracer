# Phase 165 R56-R1: Shared GeneratorSuspension Rendering Repair

This targeted patch repairs the shared Toda narrative renderer's missing typed `GeneratorSuspension` presentation. It formats the identity `E(iota_n) = iota_(n+1)` through the existing generic map and expression rendering helpers. It does not modify proof search, inference rules, registered facts, or the R55 `n,k` interface.

From the repository root, expand the ZIP and execute `phase165_r56_r1_generator_suspension_fix/run.ps1`. The installer checks the function anchor, saves an original backup, updates the entire target function in place, and outputs its full source in `CHANGED_CODE.md`. Import declarations are unchanged. It is safe to rerun after a successful installation. Focused pytest only; no full suite until phase closure.

Completion requires the preexisting failing R56 test and the new focused tests to pass. This is only a prose-formatting correction. It does not certify reference provenance, eliminate all duplicate exact sequences, or complete general partial-proof presentation. Those remain separate work within Phase 165.
