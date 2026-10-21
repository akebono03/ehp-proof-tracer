# Phase 166 R3-Z — 掲載順方式への使用資格判定の一本化

## 変更対象

1. `phase165_r52_r9_shared_math.py` — `search_shared_group_goal()` 全体（共通探索から旧制限 2 系統を除去）。
2. `phase165_r12_r8_typed_source_connection.py` — `audit_real_pi43_quotient_connection()` 全体（監査関数から旧制限を除去）。
3. 新規 `phase166_r3z_publication_order_unification/tests/test_phase166_r3z_publication_order_unification.py` — テスト 4 件、import 全文同梱。

既存の module-level import は変更しない。既存 `proof_use_order` 引数は API 互換性のため維持するが、使用資格を制限しない。保存済み証明に関する別系統の再帰的な経路は今回の撤去対象外。旧制限の定義モジュールも互換性のため削除しない。

`screen_shared_proof_context()` と `precedes_citing_assertion()` は変更しない。関数全体の置換後ソースは `run.ps1` 実行時に ZIP 展開ディレクトリ内の `*.installed_full.py.txt` に出力する。

## 適用

リポジトリのルートで ZIP を展開して `run.ps1` を実行。変更前に2ファイル全体をバックアップする。監査対象のソースブロックが一致しない場合、変更前に中止する。

## テスト

`python -m pytest -q phase166_r3z_publication_order_unification/tests/test_phase166_r3z_publication_order_unification.py`

GitHub の `phase165_r52_r9_shared_math.py` 等を確認したが、ローカルの R3-Y 追加変更は確認できないため、一致確認を必須とした。限定テストは旧ゲートの非適用と掲載順判定の残存の構造確認であり、π₅⁴ の実証結果を示すものではない。次の監査で実際の π₅⁴ Web 経路を検証する。

全体 pytest は Phase 166 の終了時のみ実行する。
