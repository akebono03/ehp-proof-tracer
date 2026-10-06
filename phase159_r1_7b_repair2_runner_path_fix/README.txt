Phase 159-R1-7b — Exact-sequence display/order repair

Production change:
- toda_group_proof_narrative_renderer.py

Tests:
- update test_phase157_r20_repair37_short_exact_after_map_support.py
- add test_phase159_r1_7b_exact_sequence_display_order.py

Scope:
- center exact sequences with display math
- center short exact sequences
- place matching typed exactness before a `完全性より,` map-property derivation

Out of scope:
- pi_6^3 calculation-chain consolidation
- equation numbering redesign
- Reference aggregate suppression
- map-property wording cleanup
- full pytest

Run from repository root:
powershell -ExecutionPolicy Bypass -File ".\phase159_r1_7b_exact_sequence_display_order_repair\run_phase159_r1_7b.ps1"


Repair1
-------
The first package used an overly strict multi-line replacement anchor around
`_phase158_normalize_public_equation_numbers(...)`.

Repair1 locates the existing proof-body normalization call itself and inserts
the R1-7b normalizer immediately after it. Production behavior is otherwise
unchanged.


Repair2
-------
Repair1 の `run_phase159_r1_7b.ps1` が旧 package directory
`phase159_r1_7b_exact_sequence_display_order_repair`
を参照していたため、repair1 の apply script が実行されていませんでした。

Repair2 では runner の `$PhaseDir` と verification output directory を
`phase159_r1_7b_repair2_runner_path_fix` に修正しました。

Production code の変更内容は repair1 と同じです。
