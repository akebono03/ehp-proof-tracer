# Phase 173 正式終了文書の設計

対象は `README.md` と `docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の**5ファイル全文**のみ。既存 Python の Proof Search、Proof Tree、Narrative Renderer、Web の実装・テストは変更しない。

検証の入口は、Phase 173 訂正 Gate R2 の実在する JSON と標準出力ログである。Phase 173、`phase_end_corrective_r2`、HEAD `25b1ee1f7c848356604061991db06265cfccb296`、`3546 passed in 80.58s (0:01:20)`、終了コード0、原本 `UNAVAILABLE_ORIGINAL_FILES`、画面確認4群を照合する。初回失敗の機械生成原本4ファイルは存在確認できていないため、「保存済み」と称さない。

GitHub 現行コードの5文書 Blob を事前監査した。R2 実行 HEAD および GitHub のアーカイブ追加のみの後続 HEAD `9003ada8d9d723fbcbec67db55f4d4382ad45ea2` だけを現状のローカル HEAD として許容する。`origin/develop` とローカルの両方で5文書が固定 Blob と一致し、ローカル HEAD が遠隔 HEAD の祖先であることを確認する。未審査のコミット、追跡済み改変、Stage 変更は拒否する。

DryRun と通常実行のいずれも5文書の**変更後の全文**を `full_documents/` にファイル出力する。通常実行は元の全文を `original_backups/` に保存してから、5文書を一括生成しアトミックに書き換える。書き換え途中のエラーでは対象の既存内容を復元する。Git index を変更せず、全体 pytest を再実行しない。文書出力は現行の改行形式を保持し、`development_log` と `proof_records` の履歴は追記を原則とする。

数学的な境界：$\pi_{12}^{4}\cong\mathbb Z/2$、$\pi_{13}^{4}\cong(\mathbb Z/2)^3$ の抽象群証明と、未完成の記名生成元 Goal を区別する。$\pi_8^5$ は未完成、$\pi_8^4$ は完成。本文で一般的な未証明の群を完成へ昇格させない。数式には `$...$` と `$$...$$` を使用する。
