# Phase 171 Closeout R2 — 5文書の全文生成・更新

## GitHub 監査基準

- `develop` HEAD: `e814ec939652807d464fd76051d34a9da40328f8`
- 事前監査：Closeout R1 の remote/local 一致・追跡済み変更なし
- 回帰修正：R1R1 の Phase 169 R3Z テスト変更のみ許可（追加安全検査5 PASS、限定 pytest 88 PASS）
- 全体 pytest はこの R2 で実行しない。

## 変更ファイル

1. `README.md` — Phase 171 の現況を英語で先頭へ追加。既存の Phase 170 記録は保持。
2. `docs/design.md` — Proof Tree・Narrative Model・Renderer の責務を追記。
3. `docs/development_log.md` — 監査と R1/R1R1 の履歴を追記。
4. `docs/roadmap.md` — Phase 171 終了 Gate と Phase 172 候補を追記。
5. `docs/proof_records.md` — $\pi_6^3$ 完成証明の検証記録を追記。

コード本体・数学的推論・関連の API は変更しない。新規監査コードは
`phase171_closeout_r2_documentation_full_output/update_docs.py`、
`run.ps1`、`tests/test_document_writer.py`。

## 実行条件・出力

対象5文書のコミット上の Git blob ID を照合する。既存の文書は全文を保持し、
README は一意の差込位置で更新、他4文書は末尾へ追記。原文の BOM・改行形式を維持。
結果の全文5ファイルと ZIP を `%LOCALAPPDATA%/EHPProofTracerRecovery/phase171_closeout_r2_*/FULL_DOCUMENTS/` と
`PHASE171_R2_FIVE_FULL_DOCUMENTS.zip` に出力する。

通常実行で関連文書契約・R3Z・R20R13R2 の限定 pytest を行う。いずれか失敗したら
5文書を元に戻す。`git add`・commit・reset・pull・push は行わない。

## 完了条件と Phase 172 境界

R2 成功条件は5全文ファイル生成、限定 pytest PASS、差分対象が5文書と R1R1 の
テスト1ファイルだけであること。**この段階では Phase 171 を正式終了しない。**
次の Phase 171 最終 Gate でアクティブ `tests/` 全体 pytest を一度だけ実行し、
成功数・終了コード・追跡済み差分を確定する。
Phase 172 では表示重複の削除などを監査候補とし、Closeout で先取りしない。
