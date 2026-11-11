# R70 限定テストの記録

- Python 構文検査と ZIP 整合性：PASS。
- 分離環境：新規 pytest の実リポジトリ Source Guard 依存の1件を除いた7件 PASS。
- 擬似 ProofStep：合成像、Δ 全射性、E=0 と H 単射性の3種類の出力を確認。
- Windows 実リポジトリ：未実施。`run.ps1` で限定 pytest と公開 Group query を確認する。
- 全体 pytest：Phase 174 の完了時にのみ実施する。
