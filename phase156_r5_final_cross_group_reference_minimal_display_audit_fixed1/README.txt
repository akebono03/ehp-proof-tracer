Phase156-R5 — final 112-group cross-group Reference minimal-display audit

変更対象
========
Production changes:
- なし

新規 audit package:
- phase156_r5_final_cross_group_reference_minimal_display_audit/
  - audit_phase156_r5_final.py
  - test_phase156_r5_final_audit.py
  - run_phase156_r5_final_cross_group_reference_minimal_display_audit.ps1
  - README.txt

R5 repair5 の結論
=================
最終 public Reference に残る statement を4群で graph entry に逆対応した。

対象:
- pi_6^3
- pi_10^4
- pi_12^5
- pi_16^9

結果:
- unmatched public headers = 0
- exceptions = 0
- final public statement の proof-body occurrences = 0
- final public statement は graph 上で entry-external consumer を持つ

したがってこれらは Reference-owned と分類する。

最終 contract
=============
必須:
1. Reference header は連番
2. body `[R#]` marker には対応する Reference header がある
3. Phase156-R3 minimal statement selection
   - boundary-used candidate 優先
   - entry-external used candidate 優先
   - same-entry internal usage のみでは複数 public statement にしない
4. final public canonical Reference statement と proof body の exact duplicate = 0

informational:
- Reference header が explicit body `[R#]` marker を持たないケース

理由:
generic renderer は proof-graph usage によって Reference entry を保持する正式経路を持つ。
従って header -> explicit marker は必須 contract ではない。

変更しないもの
==============
- production code
- Phase156-R3 selector
- Phase156-R4 suppression
- proof graph / proof data
- stable range
- existing tests
- documents

完了条件
========
- groups = 112
- exceptions = 0
- non_contiguous_reference_headers = 0
- body_marker_without_header = 0
- boundary_selection_mismatch = 0
- entry_external_selection_mismatch = 0
- same_entry_internal_public_expansion = 0
- exact_reference_body_restatement = 0
- total required violations = 0

header-without-marker は件数だけ記録する。

テスト
======
1. focused final-audit contract tests
2. Phase153 public Reference audit-only regression
3. Phase155 audit-boundary contract
4. 112-group final R5 audit

repository-wide pytest は R5 では実行しない。

次 Phase
========
PASS 後:
Phase156-R6 — focused/sharded regression


Fixed1
======
初版 final audit は `defaultdict` を使用していたが、
`collections` から import していなかったため、
112-group audit 開始時に NameError で停止した。

変更:
- audit_phase156_r5_final.py
  - `from collections import Counter, defaultdict`
- test_phase156_r5_final_audit.py
  - audit module import regression を追加

Production changes:
- なし

監査 contract:
- 変更なし
