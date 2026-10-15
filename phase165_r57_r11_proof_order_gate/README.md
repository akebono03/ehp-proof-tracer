# Phase 165 R57-R11: Proof-use ordering gate

Install from the project root, then run `phase165_r57_r11_proof_order_gate/run.ps1`.

This patch does not establish global ordinal metadata. It blocks a previously
accepted shortcut: proving the requested group's structure directly from an
unordered symbolic group-structure reference. Earlier non-root dependencies,
including the existing pi3_2 derivation, remain eligible. It adds no fixed
answer, no new GIVEN, no legacy replay, and no renderer-specific narrative.

Only focused tests are run. The full suite is reserved for Phase closure.
