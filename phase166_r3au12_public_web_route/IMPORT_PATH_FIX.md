# Phase 166 R3-AU-12 import 修正

変更対象：`run.ps1` のみ。`$Root` を `PYTHONPATH` の先頭に追加し、`python .\phase166_r3au12_public_web_route\audit.py` からリポジトリ直下の `web_group_proof` を import できるようにする。監査コード、テスト、既存 API、本番コードの変更なし。

実行後：監査結果と限定 pytest 3件を確認。全体 pytest は実行しない。
