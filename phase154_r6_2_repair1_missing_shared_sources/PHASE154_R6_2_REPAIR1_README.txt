Phase 154-R6-2 Repair1 — Missing shared sources

初回 R6-2
---------
81 focused tests 中:
- 70 passed
- 11 failed

主因
----
R6-2 初回で production 対象を6ファイルに絞りすぎた。

不足していた shared source:
1. toda_group_proof_narrative_exactness_method_renderer.py
2. toda_group_proof_narrative_transition_renderer.py
3. toda_group_proof_narrative_argument_single_renderer.py

これにより:
- `そのために、`
- `以上より、`
- `.そのために、`
が残った。

また R2/R8/Phase143 の一部 test が旧 `、。` contract を
まだ期待していた。

変更対象 production
-------------------
1. toda_group_proof_narrative_exactness_method_renderer.py
   - `render_toda_group_proof_narrative_exactness_method_transition`

2. toda_group_proof_narrative_transition_renderer.py
   - `render_toda_group_proof_narrative_transition_connector`

3. toda_group_proof_narrative_argument_single_renderer.py
   - `_normalize_toda_group_proof_narrative_argument_header_spacing`

import 変更
-----------
なし。

test 修正
---------
句読点 contract のみ:
- `、` -> `, `
- `。` -> `.`

対象:
- Phase 154 R2/R5/R6
- Phase 153 R8
- Phase 143 exactness / argument-header tests

新規 test
---------
tests/test_phase154_r6_2_repair1_missing_shared_sources.py

完了条件
--------
- focused tests PASS
- 5代表群:
  - Japanese comma = 0
  - Japanese period = 0
  - ASCII comma が存在
  - ASCII period が存在
- pi6_3 argument header が
  `...決定するために, 次の完全列を考える.`
  と再結合される
- pi11_4 R5 linkage 維持

全体テスト
----------
実行しない。
Phase 154 最後にのみ実行する。

次
----
R6-2 完了後:
- punctuation closure audit
- Phase 154 closure
- phase-end full regression
