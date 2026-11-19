# Phase 176 R1 — k=5 登録全群 Source-first 監査

## 監査対象

`data/sphere.csv` の k=5、n≥2 の重複排除した全登録ペア。登録行が複数存在しても群は一度ずつ実探索する。

## 変更対象

新規ディレクトリ `phase176_r1_k5_source_first_audit/` の `audit.py`、`run.ps1`、`__init__.py`、`tests/test_audit.py`、この監査計画のみ。既存の証明コード・テスト・5文書は変更しない。

## 手順

1. `develop`、Phase 175 最終 HEAD の祖先関係、5文書の正式終了マーカー、Final Closeout の存在、Git 差分を検証する。
2. `sphere.csv` からすべての k=5 の n を列挙する。
3. 各群について独立 worker で `search_group_from_registered_goal` を実行し、状態・Open Goals・Reference・ProofStep・結論を記録する。
4. 共通 Web `build_standard_web_group_proof_view` の narrative 出力を試み、失敗は結果と区別して報告する。
5. レポートはリポジトリ外の `%LOCALAPPDATA%/EHPProofTracerAudit/phase176_r1_k5_source_first_audit/report.json` へ出力する。失敗も保存する。

## 完了条件

登録ペアを全件列挙し、worker が各ペアの実測結果を返す。未完成証明を失敗扱いにしないが、worker 例外は Gate FAIL とする。Web の失敗は `PASS_R1_AUDIT_WITH_WEB_GAPS` で明示する。全体 pytest は実行しない。

## 次 Phase との境界

出典補強、一般規則の実装、Provider 接続、文書改訂、全体 pytest、旧 Source Guard 4件の修正を先取りしない。
