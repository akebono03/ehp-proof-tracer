Phase156-R5 — 112-group cross-group Reference minimal-display audit

変更対象
========
Production changes:
- なし

新規 audit package:
- phase156_r5_cross_group_reference_minimal_display_audit/
  - audit_phase156_r5.py
  - test_phase156_r5_audit_classifier.py
  - run_phase156_r5_cross_group_reference_minimal_display_audit.ps1
  - README.txt

目的
====
Phase156-R1〜R4 の結果を112群全体で横断監査し、
Reference minimal display が route ごとに崩れていないことを確認する。

監査軸
======
1. Reference header の連番性
2. body marker `[R#]` に対応する header が存在すること
3. public Reference header が本文で実際に使われていること
4. Phase156-R3 の minimal statement selection 規則
   - boundary-used statements を優先
   - boundary が無ければ entry-external used statements を優先
   - same-entry internal usage だけでは複数選択しない
5. Phase156-R4 の exact body restatement suppression
   - public Reference に実際に表示された canonical statement だけを比較
   - derivation / calculation context のある本文は許可

特殊 route
==========
hand-written Reference section の `\[`、`\]`、説明文などは
canonical Reference statement とみなさない。

そのため R4 初版のような display scaffolding の誤検出を避ける。

出力
====
phase156_r5_audit_output/
- phase156_r5_summary.txt
- phase156_r5_result.json
- phase156_r5_group_summary.csv
- phase156_r5_violations.csv
- phase156_r5_violation_summary.csv
- phase156_r5_exceptions.csv

完了条件
========
- groups = 112
- exceptions = 0
- non_contiguous_reference_headers = 0
- body_marker_without_header = 0
- public_header_without_body_use = 0
- boundary_selection_mismatch = 0
- entry_external_selection_mismatch = 0
- same_entry_internal_public_expansion = 0
- suppressible_exact_body_restatement = 0
- total violations = 0

R5 で変更しないもの
===================
- Reference theorem / lemma selection
- Reference statement selector
- Reference rendering
- proof-body suppression
- proof graph / proof data
- stable range
- existing tests
- documents

テスト
======
1. focused audit-classifier tests
2. Phase153 public Reference audit-only regression
3. Phase155 audit-boundary contract
4. 112-group R5 audit

repository-wide pytest は R5 では実行しない。

次 Phase との境界
=================
violations = 0 の場合:
Phase156-R6 — focused/sharded regression へ進む。

violations > 0 の場合:
R6 へ進まず、R5 repair substep として具体的な category だけを修正する。


Fixed1
======
R5 初版では `## 使用する結果` と `## 証明` の間だけを
Reference section とみなしていた。

しかし generic contribution renderer は
`reference_section + "\n\n" + rendered`
という構造を持ち、Reference entry header (`**[R#] ...**`) が
`## 使用する結果` heading の内側にない route がある。

repair1 diagnostic で次の4群がこれに該当した。
- pi_6^3
- pi_10^4
- pi_12^5
- pi_16^9

4群とも missing とされた `[R#]` は実際には
`**[R#] ...**` という Reference entry header 自身として存在した。
したがって production rendering defect ではなく、
R5 audit contract mismatch と分類する。

Fixed1 の監査規則:
1. Reference entry header は文書全体から `**[R#] ...**` で認識する。
2. body usage marker は Reference entry header 行自身を除外して数える。
3. `## 使用する結果` heading を必須としない。
4. canonical statement の display 判定は各 Reference entry block 内で行う。
5. production code は変更しない。
