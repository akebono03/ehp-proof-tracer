Phase 151-2 — All-Group Generic Baseline Measurement
=======================================================

112群を Narrative / depth 2 の同一 generic route で測定する監査専用package。
production code変更なし。existing tests変更なし。文章品質の修正なし。

出力:
- audit_output/all_group_baseline.csv
- audit_output/fallback_inventory.csv
- audit_output/typed_reason_inventory.csv
- audit_output/exception_inventory.csv
- audit_output/baseline_summary.txt

測定:
success/failure, presentation nodes, blocks, arguments, typed reasons,
OTHER blocks, raw/rule-name/type fallback, markdown chars, exceptions。

typed reasonは現行TodaGroupProofNarrativeReasonKindをそのまま集計する。
fallbackはgeneric step rendererの実出力から分類する。
rule_name: inference_rule.nameそのもの
type_name: backtick付きstatement class名
raw_repr/raw_str: statementのrepr/strそのもの

Phase 151-2では欠陥を修正しない。
次のPhase 151-3で112群を横断して共通パターンを監査する。
full historical regressionは実行しない。
