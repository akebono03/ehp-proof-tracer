Phase157-R5-R1 — 112-group Literature Statement Boundary cross-audit

目的:
- n=2..15, k=0..7 の112群を横断して、
  current selected Reference steps を Literature Statement Boundary で分類する。
- production code は変更しない。
- existing tests は変更しない。
- pytest は実行しない。
- full Narrative は生成しない。

監査分類:
- FIXED_STATEMENT
- PROOF_INTERNAL
- UNTRACKED
- FIXED_STATEMENT_INELIGIBLE
- FIXED_STATEMENT_WITHOUT_COMPONENT
- FIXED_STATEMENT_MISSING_COMPONENT

確認する欠陥:
- PROOF_INTERNAL が Reference として選ばれている。
- 同一 Proposition 内で target 自身または後続 fixed group result が選ばれている。
- fixed statement と分類されたのに component metadata が不完全。

UNTRACKED:
- 直ちに defect とは数えない。
- R5-R2 で fixed statement catalog を追加すべき literature locator / rule の候補。

軽量化:
- 各群 depth=2 の proof replay + semantic closure のみ。
- public Narrative render は行わない。
- 恒常 pytest は追加しない。

出力:
phase157_r5_r1_audit_output/
  phase157_r5_r1_summary.txt
  phase157_r5_r1_result.json
  phase157_r5_r1_selected_steps.csv
  phase157_r5_r1_confirmed_defects.csv
  phase157_r5_r1_group_inventory.csv
  phase157_r5_r1_locator_summary.csv
  phase157_r5_r1_exceptions.csv

次:
- R5-R1 の population を確認後、
  R5-R2 で未登録 literature boundary を必要な範囲だけ追加する。
