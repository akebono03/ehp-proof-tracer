# Phase 159-R1-4

変更対象:
- toda_group_proof_narrative_renderer.py
  - `_phase159_project_generic_semantics_to_public_proof()`
- tests/test_phase159_r1_2_pi3_2_narrative_repair.py
  - exactness contract test
  - map-property contract test
  - punctuation contract test

import 変更:
- なし

完了条件:
- proof body の `\\xrightarrow` 行が1本だけ
- その1本が canonical long exact sequence + `は完全である.`
- `(1), (2) より, H... は同型.`
- standalone math sentences に period
- unique-preimage prose 維持
- focused/regression tests + git diff --check PASS

次 Phase との境界:
- Reference attribution は未変更
- stable range / Freudenthal は未変更
