# Phase 166 R3-AU-12 監査内容

対象は新規 `audit.py` の `source_checks()`、`inspect_view()`、`main()`、新規 `test_r3au12.py` の3テスト関数、`run.ps1`、README.md、AUDIT.md。既存ファイル・APIの変更なし。

実際の Web view の `conclusion_latex`、`key`、`partial_result`、`rendered_lines`、`steps` を採取する。`generic-complete-proof` は探索ステータスであり、TeX 表示成功から推測しない。画面のブラウザー描画の目視確認ではない。

次の Phase では入力変更時の分岐と実 Web 画面での整合性を確認する。全体 pytest は Phase 166 末尾のみ。
