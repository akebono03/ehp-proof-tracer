Phase157-R5-R2 — Literature boundary inventory

目的:
- Phase157-R5-R1 の selected-step CSV を再利用し、
  UNTRACKED 128件と FIXED_STATEMENT_WITHOUT_COMPONENT 24件を
  locator / rule / statement type / affected groups 単位に集約する。
- R5-R3 の boundary catalog 拡張単位を確定しやすくする。

production code:
- 変更なし

existing tests:
- 変更なし

実行しないもの:
- 112-group proof replay の再実行
- full Narrative rendering
- pytest

入力:
phase157_r5_r1_audit_output/
  phase157_r5_r1_selected_steps.csv

出力:
phase157_r5_r2_inventory_output/
  phase157_r5_r2_summary.txt
  phase157_r5_r2_result.json
  phase157_r5_r2_locator_inventory.csv
  phase157_r5_r2_rule_inventory.csv
  phase157_r5_r2_statement_type_inventory.csv
  phase157_r5_r2_catalog_candidates.csv
  phase157_r5_r2_untracked_rows.csv
  phase157_r5_r2_fixed_without_component_rows.csv

重要:
- UNTRACKED はこの段階では FIXED_STATEMENT / PROOF_INTERNAL を決め打ちしない。
- literature/source record を確認してから R5-R3 で分類する。
- FIXED_STATEMENT_WITHOUT_COMPONENT は分類自体は fixed なので、
  R5-R3 では component granularity の追加が主作業となる。
