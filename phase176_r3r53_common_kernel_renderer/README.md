# Phase 176 R3R53 — Common kernel statement renderer

This rendering-only change delegates the `KernelMultipleStatement` branch of `typed_sentence` to the existing repository conclusion renderer. It does not assert a subgroup is free cyclic or determine an order from a rendering fixture. Explicitly proved `SuspensionKernelFreeCyclicStatement` and other statement types are left unchanged.

Run `run.ps1 -DryRun` from the repository, then `run.ps1`. The installer requires the reviewed baseline or its exact successor, and preserves line endings and unrelated bytes. The complete replacement function is in `typed_sentence_FULL.py.txt`; the installer checks it against the actual edited function. No top-level imports change. The shared renderer already exists and is not modified.

The five focused suites are run in separate processes. The real Web audit checks the 62-step root ancestry, 51 inferences and 11 GIVENs, ten citations, the contextual lift replay and both complete and partial-prefix kernel displays. The partial-prefix comparison is display-only, not a separate proof search. Reports are written under `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r3r53_common_kernel_renderer`. The historical R3R52 baseline audit is intentionally not rerun: it expects the old defect. Its independent helper tests remain in the focused suite.

No mathematical rules, GIVEN registrations, proof search behavior, citation text or duplicate-suppression logic are changed. The full test suite is reserved for Phase 176 closeout.
