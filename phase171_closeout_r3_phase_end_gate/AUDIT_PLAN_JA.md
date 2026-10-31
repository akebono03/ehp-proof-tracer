# Phase 171 Closeout R3 — 最終 Gate 監査仕様

## 監査前に確認した現行コードとテスト

- GitHub `akebono03/ehp-proof-tracer` `develop`：`3e74849bf90bc115c16503ddd46d49996baa0856`。
- 現行アクティブ全体テストの先例：`phase170_r3_r11_active_suite_closeout/closeout.py`、`run.ps1`。実行対象は `tests/` のみで、歴史的な全テストを再収集しない。
- 既存の証明と表示の回帰：`phase171_r20r13_eta_sentence_layout/tests/test_projection.py`、`phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py`、`phase171_r20r2_first_successful_search/tests/test_first_successful_search.py`、R1R1 の `phase169_r3z_reference_only_generic_eta/tests/test_r3z_reference_only_generic_eta.py`。
- R2R4 の Windows 実行は限定 pytest 11、24、56 PASS。更新差分は文書5ファイル、合計100行追加、`git diff --check` 出力なし。
- R2R3 による歴史文書の CRCRLF/CRLF 混在を維持し、本文を正規化して保存しない。

## 変更対象

- **新規** `phase171_closeout_r3_phase_end_gate/closeout.py`：審査済み内容の検査、Phase 末尾の全体 pytest、終了レポートと文書全文の保存。
- **新規** `phase171_closeout_r3_phase_end_gate/run.ps1`：Windows 起動。
- **新規** `phase171_closeout_r3_phase_end_gate/tests/test_closeout.py`：独立した短時間の Guard テスト。
- **正常な本番実行で更新** `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の5ファイル。元の本文バイト列を維持し、終了節だけを挿入・追記する。README は英語、それ以外は日本語。
- 本番数学コード、既存の関数、クラス、import、テストは変更しない。

## Gate の順序

1. `-DryRun`：`develop` と reviewed HEAD の祖先関係、`origin/develop`、未ステージング変更の許可範囲、審査済みコード5件の Git blob、R2 文書5件の本文を検査する。全体 pytest は実行しない。
2. 通常実行：同一の preflight 成功後に `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を**1回だけ**実行する。
3. 終了コード0と pytest PASS 件数を確認し、HEAD、追跡差分、文書の SHA-256 が変化していないことを確認する。失敗した場合は正式終了を書かない。
4. 実際の PASS 件数と実行結果を使って正式終了節を生成し、5文書全文を出力する。数学的コードは変更しない。文書の更新処理に失敗すれば全文復元する。
5. `PHASE171_CLOSEOUT_R3_RESULT=PHASE171_CLOSED_FULL_SUITE_PASS` と `PHASE171_CLOSEOUT_R3_FINAL=PHASE171_CLOSED_FULL_SUITE_PASS` を確認する。レポート・全5文書 ZIP は `%LOCALAPPDATA%\EHPProofTracerRecovery` に保存する。

## 完了条件

- $\pi_6^3=\mathbb Z/4\{\nu'\}$ の完成証明・未解決目標ゼロ・Reference 8件・Web `generic-complete-proof` は既存の証明検証と対応する不変条件として維持される。
- 全体 pytest の終了コード0、PASS 件数を保存。`tests/` 以外の歴史的な退役テストを「全体」に含めたと主張しない。
- Git の追跡済み差分は最終的に文書5件のみ。未追跡の監査パッケージを追跡済み変更として誤判定しない。
- 最終終了の記録をすべての文書へ書き、全文を ZIP に保存。
- Phase 172 の表示品質改善・新しい数学的命題は本 Gate に含めない。

## 失敗時と再開

- 全体 pytest が FAIL：文書5件を変更せず `REFUSED_OR_FAILED` を保存。原因を調査する。
- 全体 pytest は PASS したが文書更新が FAIL：文書を復元し、同一 HEAD と5文書の SHA-256 が一致するときだけ `-ResumeReport` を指定して **pytest を再実行せず** 再開可能。
- 既に最終マーカーを持つ文書を再更新しない。`git pull`・`git reset`・自動 commit は行わない。
