# Phase 166 R3-O パッチ修正

変更対象：`phase163_r4_r94_output/manifest.json`、`phase166_r3b_publication_order_binding/phase166_r3b_publication_order_binding.py` の `_load_manifest_reference_order()`、`phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()`。

R3-L/R3-N による追加コードを保持して、命題コピーの引数だけ変更します。事前検証に失敗した場合は書き込みません。既存ファイルのバックアップを作成し、変更後の関数全文を表示します。全体 pytest は実施しません。
