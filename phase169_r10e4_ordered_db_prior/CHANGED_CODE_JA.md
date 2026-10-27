# R10E4 — 変更単位

変更対象の本番ファイル、関数は以下の3つだけ。

1. `phase165_r3_recursive_search.py` の `reconstruct_registered_goal()`：他の出典がない場合、対象 $(k,n)$ より小さい DB の型付き Goal を候補に追加。既存の `SourceBoundGoal` はそのまま。
2. `phase168_r3_41p13_trust_boundary/verification.py` の `verify_proof_tree_for_narrative()`：DB 前提を元 DB から独立に再確認し、その他の `GIVEN` の文献審査と既存 API を維持。
3. `phase169_r10e1_general_group_transport/transport.py` の `expand_prior_general_group_transport()`：共通輸送の source に、文献根拠を欠く場合は実在 DB の先行基点を検討。有限巡回群・零群・直和の既存型と制約を変更しない。

新規モジュール `phase169_r10e4_ordered_db_prior/db_prior.py`：`precedes_db_goal()`, `group_coordinates()`, `_has_explicit_row()`, `exact_prior_database_result()`, `_optional_registered_locator()`, `admitted_db_step()`, `verified_db_step()` を順に定義。新規クラスはない。

新規テスト `tests/test_r10e4_ordered_db_prior.py`：先行関係、厳密な DB 行、零群、相違する群構造、偽装 `GIVEN`、二重パッチ拒否を検査。

既存の import 宣言は変更しない。追加の import は変更した関数内部に全て記載する。実行時に変更関数の全文を `output/*_FULL.py`、変更後ファイルの全文を `output/*.FULL` として作成する。コードの省略はない。

実行後に見る表示：`R10E4_LIMITED_TESTS_AND_AUDIT=PASS`、`R10E4_INTEGRITY_RESULT=PASS`、個別の `BASE_DB`・`PRIOR_ADMITTED`・`STATUS`。どの DB 行からでも無条件に完成証明が作れる、という意味ではない。Reference の DB 表示が追加された場合も文献引用と混同しない。

次の Phase では新しい群構造命題・生成元像の出典不足を切り分ける。今回の変更が未登録命題を自動的に文献命題へ昇格させることはない。
