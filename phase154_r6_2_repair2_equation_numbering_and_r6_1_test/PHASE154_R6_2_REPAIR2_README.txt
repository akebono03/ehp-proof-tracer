Phase 154-R6-2 Repair2

Repair1 result
--------------
- 82 passed
- 2 failed

残存 production defect
----------------------
`(1) と (2) より、`

生成経路:
1. `toda_group_proof_narrative_argument_body_renderer.py`
   が `これらより、` を生成
2. `toda_group_proof_narrative_equation_numbering.py`
   が番号参照へ変換し
   `(1) と (2) より、`
   を生成

Repair2 では両方を ASCII comma + space に変更する。

変更対象 production
-------------------
1. toda_group_proof_narrative_argument_body_renderer.py
   - step derivation connector を `これらより, ` に変更

2. toda_group_proof_narrative_equation_numbering.py
   - connector lookup を `これらより, ` に変更
   - numbered connector を `より, ` に変更

import 変更
-----------
なし。

test repair
-----------
Repair1 の test punctuation 一括置換により、
R6-1 audit test の判定条件
`prose.endswith("。")`
まで誤って `prose.endswith(".")` に変わった。

`tests/test_phase154_r6_1_repair3_ascii_period_policy.py`
を正しい current contract で全文置換する。

新規 test
---------
tests/test_phase154_r6_2_repair2_equation_numbering.py

関連 test
---------
tests/test_phase143_57c_step_derivation_connector.py
の punctuation expectation を current `, .` contract に更新する。

完了条件
--------
- focused tests PASS
- 5代表群で Japanese comma = 0
- 5代表群で Japanese period = 0
- ASCII comma が存在
- ASCII period が存在
- pi6_3 の numbered derivation が
  `(1) と (2) より, `
  となる

全体テスト
----------
実行しない。Phase 154 最後にのみ実行する。

次
----
R6-2 完了後:
1. punctuation closure audit
2. Phase 154 closure
3. phase-end full regression
