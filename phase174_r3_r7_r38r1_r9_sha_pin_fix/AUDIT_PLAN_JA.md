# R38R1：Source Guard の最小修正

## 調査の結論

R38 の既存 `PINNED` で R9 `rule.py` の Git blob SHA が **39桁**になっていた。GitHub 現行 `develop` の同ファイルは `2c44c68be90cb761d7bdd35e29f23977b5f93a2e`（40桁）。R38 側の記載から末尾 `e` が欠落していた。Windows の CRLF 問題とは断定しない。

## 変更ファイル・位置

- 変更: `phase174_r3_r7_r38_source_bound_zero_image_public_wiring/install.py` のトップレベル `PINNED` 定数の1文字のみ。
- 新規: `phase174_r3_r7_r38r1_r9_sha_pin_fix/install.py`（保護付き・冪等インストーラー）
- 新規: `phase174_r3_r7_r38r1_r9_sha_pin_fix/tests/test_patch.py`（関連限定pytest）
- 変更した関数・クラス・import: なし。既存 `verify_checkout()` と `matches_blob()` は一切変更しない。
- 主要5ドキュメントと本番コード、Narrative Renderer: 変更なし。

## ガード

GitHub R37 を取り込んだ `develop` HEAD とブランチを確認。既存 R38 `install.py` がレビュー済みの原版または修正版の SHA256 に一致するときだけ、原版から1文字を変更する。DryRun は置換後の Source Guard をメモリ上で動かし、ファイルを書き換えない。通常実行の修正後は R38 の元の `run.ps1` へ委譲して限定 pytest を行う。既存ファイルの予期しない変更を認めない。

## 完了条件と次段階

- R38R1 DryRun と本実行で Source Guard が PASS。
- R38 既存の監査・限定 pytest が PASS。
- R9 数学コードや R38 Provider を変更しない。
- 全体 pytest は Phase の最後まで未実施。

修正は R38 の実行障害に限定し、零像や最終群の証明完成を主張しない。
