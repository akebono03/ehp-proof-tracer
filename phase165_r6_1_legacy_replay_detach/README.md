# Phase 165 R6-1: historical replay detachment

Scope: replace the complete root-level `phase165_r14_r40_replay.py` and `phase165_r14_r41_proof_transfer.py`. Their old reconstructed-π₃² logic is deleted; callable compatibility entrypoints remain because historical tests import them. All proof generation delegates to `build_registered_common_replay`. No literature facts or inference rules change. The package subdirectory copies are installer artifacts and are not updated here.

The runner backs up files and runs three focused tests. These tests validate routing and absence of direct R38 dependencies, **not** an end-to-end mathematical proof. Full pytest is deferred until the Phase ends. Removing compatibility APIs and historical tests is outside this batch.
