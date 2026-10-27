# Phase 169 R6 — π₈⁶ 監査パッケージ

## 対象

GitHub `akebono03/ehp-proof-tracer` の `develop` ブランチを事前に確認した。

この Phase では本番ファイル・既存クラス・既存関数・既存テストの変更は行わない。

新規ファイルは `audit.py`、`run.ps1`、`tests/test_r6_pi86_boundary.py`、`__init__.py`、この文書および英語の `README.md` のみ。

`audit.py` の新規関数は `git`、`citation_screened_claims`、`prior_summary`、`inspect`、`summary_markdown`、`main` である。`tests/test_r6_pi86_boundary.py` には fixture 1件、テスト4件を新規追加する。

## 監査の目的

1. $\pi_8^6$ を complete と誤認せず、現時点の partial を記録する。
2. $\pi_6^4$ と $\pi_7^5$ の文献順の利用可否を個別に照合する。
3. 既存の1回懸垂複合輸送、R5B root 専用接続、一般の反復懸垂輸送の候補数を比較する。
4. Toda (4.5) の2回懸垂が型付き具体化できるか、DB の生成元が現在の `IteratedSuspension` 表現と一致するかを確かめる。
5. 群構造 DB 行を GIVEN に格上げしない。

## 実行テスト

`tests/test_r6_pi86_boundary.py`、R5B の既存テスト、R3O の既存テストのみ。全体 pytest は Phase 169 終了まで実施しない。

## 完了条件と次工程

監査 JSON に候補生成器の各件数、文献順、生成元型、公開 Web 状態と未解決 Goal 数が記録され、実行前後で追跡対象の Git 状態が変化しないこと。

次 Phase では、この情報を使って必要な最小限の候補生成接続を検討する。数学的規則を先取りして追加しない。
