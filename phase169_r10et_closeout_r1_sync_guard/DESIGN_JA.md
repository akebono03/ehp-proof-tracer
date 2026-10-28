# Phase 169 R10ET Closeout R1 — Git 同期境界の読み取り監査

## 変更対象

- 新規 `phase169_r10et_closeout_r1_sync_guard/audit.py`：`git()`、`remote_sha()`、`git_blob_map()`、`outside_repo_dir()`、`decision()`、`execute()`、`main()`。
- 新規 `run.ps1`：読み取り監査の起動。
- 新規 `tests/test_audit.py`：判定・Git blob・リモート解析の限定試験。
- 既存の本体・テスト・文書・Git index・refs は**変更しない**。

## 経緯

2026-10-28 17:46 の R6D は 19/19 監査 PASS、限定 pytest 24 PASS、`R10ET_R6D_COMPLETE=PASS` を報告した。旧ローカル HEAD は `232a92883b0cb009762b437cbb3cc550f00ab6bd`。

GitHub の `develop` はその後 `fc07630e8c2ca04b16f0e3eb08a06ea4f12e9b79` になり、R5D・R6C の7つの実装・既存テスト変更を含むコミットが存在することを確認した。R6D 監査ファイルや監査出力も同コミットに含まれる。5つの主要文書は依然 Phase 168 完了時点が最終記録である。

## 監査の境界

- `git ls-remote origin refs/heads/develop` によりリモートを読む。ローカル refs を更新しない。
- コード8ファイルと文書5ファイルを、GitHub の検証済み Git blob 識別子と比較する。
- 未コミット変更がある場合は自動統合せず、文書更新を保留する。
- 監査結果は `%LOCALAPPDATA%` の下に書く。Dropbox 内の長い生成パス問題を再発させない。
- R5D と R6C の既存変更、R6D の修正を失う `reset`、`clean`、`checkout` 等を決して実行しない。
- 新たな数学的推論、Definition、証明経路、Renderer は先取りしない。

## 完了条件・次段階

この R1 は同期状態を測る監査である。`R10ET_CLOSEOUT_R1_EXIT=0` は監査成功であり、Phase 169 終了や文書更新完了を意味しない。結果が `READY_FOR_DOCUMENT_CLOSEOUT` なら、次の R2 で README.md 等5文書を全文出力し、現状を反映する。ローカル HEAD や変更が一致しなければ、先に差分を保護して同期方針を決める。

全体 pytest は Phase 169 の最終段階にのみ実行する。
