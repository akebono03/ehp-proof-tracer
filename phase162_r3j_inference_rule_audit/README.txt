Phase 162 R3-J — InferenceRule metadata and exact replay audit

目的: R3-IでSidecar未対応の45推論を、既存InferenceRuleの直接前提・結論再適用・適用条件に照らして分類する。
現行推論規則・Reason Builder・公開Rendererは変更しない。追加理由文は0件。

変更ファイル（すべて新規、リポジトリ直下／tests配下へ配置）:
- phase162_r3j_inference_rule_audit.py: R3JRuleEntry, classify_r3j_inference_rule(), build_phase162_r3j_inference_rule_audit()
- audit_phase162_r3j.py: main()
- tests/test_phase162_r3j_inference_rule_audit.py: focused pytest 7件

利用方法（PowerShell、R3-I適用済み）:
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase162_r3j_inference_rule_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File ".\phase162_r3j_inference_rule_audit\run_phase162_r3j.ps1"

出力:
phase162_r3j_output/inference_rule_entries.json
phase162_r3j_output/inference_rule_groups.json
phase162_r3j_output/inference_rule_audit.json

注意:
RULE_REPLAY_VERIFIED_PROSE_UNAUDITED は推論規則の再適用成功であり、数学的理由文が生成できたことを意味しない。
R3-Iの結論ラベルのみ9件は今回の45件の対象外。GIVENの外部的真偽は検証しない。
全体pytestはPhase 162終了時のみ行う。
