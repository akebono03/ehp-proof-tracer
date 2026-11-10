# Phase 174 R3-R7-R55 監査計画

## GitHub 基準と監査済みコード

2026-11-10 GitHub `develop` HEAD：`40db3a00ca8be58e589e0949e6a70dcedd3b9cf5`。変更対象 Renderer：`phase168_r3_5_model_renderer.py` Git blob `64e0570e8462ee0361ed07afab836c66ce8e7895`。R54 の Flask `POST /`、R53 の検索接続、共通 Model を監査済み。

## 原因

`render_model_backed_narrative_markdown()` は `project_exactness_chains()` が返す複数の完全列を表示する際、各完全列に「群構造を決定するために」という同一導入文を付す。R54 は `group` と `group_proof` の各 HTTP で導入文2件を確認した。これは証明の重複でもソース重複でもない。

## 対象

本番は `phase168_r3_5_model_renderer.py` 内 `render_model_backed_narrative_markdown()` だけ。import 変更なし。`for chain in chains` を `for chain_index, chain in enumerate(chains)` とし、`chain_index == 0` の導入文のみ従来どおり、後続は「さらに, 」にする。Proposition の番号、完全列、証明木、文献、数学規則は変更しない。

## 検査

`Source Guard`、構文、パッチ契約、実 Flask POST 2経路、結論 `\pi_{12}^{7}=0`、`generic-complete-proof`、28 ProofSteps、未解決 Goal 0、文献番号・結論 □、導入文各1件、後続接続の文言、R54/R53/R52 の限定回帰テスト。全体 pytest は Phase の最後だけ。

## 次工程

R55 PASS 後、Phase 174 完了前の残り表示回帰の調査、文書整備、最終全体 pytest を別工程で実施する。ブラウザ KaTeX 表示と実配備サーバは R55 の合格条件ではない。
