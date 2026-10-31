# Phase 171 R20R10 読み取り専用失敗箇所監査

## 監査対象と変更対象

- 監査対象：通常の `search_group_from_registered_goal(n=3, k=3)` による `π_6^3` の型付き群構造証明。
- **本番変更ファイル・クラス・関数・メソッド：なし。**
- 追加ファイル：本パッケージの `audit.py`、`run.ps1`、`tests/test_audit.py`、`README.md`、`AUDIT_PLAN_JA.md`、`__init__.py`。
- 既存の `reconstruct_registered_goal` は呼出し中だけ監査用ラッパーから呼び出し、`finally` で元に戻す。元のアルゴリズム、候補順序、証拠の取得・照合規則を変更しない。

## 現時点で判明した事実

GitHub `develop` の R20R9R4 `audit.json` を確認した。`typed_double_inference_matching_proposals=1`、`typed_double_inference_certified_proposals=1` に対して、`public_status=partial`、`public_complete=false`。公開探索の未解決目標は9種類で、位数4、EHP短完全列、Eの単射性、Hの全射性、巡回構造と最終群関係が含まれる。

ログに記録される9目標はすべて探索時の未解決イベントであり、最深部の一箇所のエラーを断定するものではない。探索が `partial` と判定されるのは、何らかの `ProofStep` が受理されながら最終結論が完成しなかったためである。

## 観測方法

1. ローカルの `develop` と Git HEAD を読み取る。変更の可能性があるため、既存の未コミット変更は保持する。
2. GitHub `develop` で確認した本番9ファイルの Git blob SHA を、改行の違いだけを許容して実バイトから再計算する。内容に差があれば停止。
3. `phase165_r52_r2_search_adapter.reconstruct_registered_goal` の呼出しだけを監査ラッパーで観測。`expansion_provider` の返値と `progress_observer` の呼出しを記録し、オリジナル関数へ同じ引数を渡す。
4. `search_group_from_registered_goal(n=3,k=3)` を通常の `build_shared_typed_bridge()` から実行する。
5. 解決不能となった目標を `NO_BACKWARD_PROPOSAL` または `PREMISE_OR_INFERENCE_NOT_COMPLETED` 等に分類。各候補の型付き Subgoal と、実際に受理された結論を記録する。
6. 最後に独立した R4–R8 参照証明木を構築し、そこで得た型付き結論と、実際の公開探索で候補・完成が観測されたかを照合する。**参照証明木を公開探索に渡さない。**
7. 対象 HEAD と追跡済みファイルの Git status が監査前後で不変であることを検査する。監査 JSON はリポジトリ外に書き出す。

## 限定テスト

`python -B -m pytest -p no:cacheprovider -q phase171_r20r10_read_only_frontier_audit/tests/test_audit.py`

## 完了条件と次工程の境界

R20R10 の完了条件は、実際の公開探索における最深部の未解決目標、その候補数、失敗した前提と R4–R8 参照証明の型・推論規則の対応を監査ログで確認すること。これは診断の完了であり、数学的証明の完成ではない。

今工程では `public_status=complete` に変更しない。原因を確定した後、別工程で最小限の本番修正を検討する。`complete` が出た後にだけ Web 証明表示を検証する。Phase 171 終了時以外は全体 pytest を実行しない。
