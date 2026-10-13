# Phase 165 R45 — ProofStep 推論規則の照合

変更対象の production モジュールはありません。新規ファイルは `audit.py`、`test_audit.py`、`run.ps1` です。`audit_proofstep_rules()` は現在の R41 Replay の全祖先を走査し、結論の型、前提、`inference_rule.name`、出典、既存の generic renderer による表示を記録します。`main()` は `phase165_r14_r45_output/report.json` を出力します。

今回は、既存コードに原因があるか確認するための読み取り専用監査です。`H` の単射・全射、`Δ=0` の推論に exactness が前提として含まれるか、既存 Renderer がどう解釈しているかを示します。

対象 pytest は3件です。全体 pytest は行いません。実行結果を確認するまで Renderer、ProofStep、Registry のどれを直すべきか断定しません。
