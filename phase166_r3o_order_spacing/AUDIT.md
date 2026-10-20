# Phase 166 R3-O 実装・監査

変更対象：`phase163_r4_r94_output/manifest.json`（117レコード、うち108文献）、`phase166_r3b_publication_order_binding/phase166_r3b_publication_order_binding.py::_load_manifest_reference_order`、`phase165_r52_r9_shared_math.py::build_shared_typed_bridge`。

出典 ID、数式、ProofStep、一般規則、Renderer は変更しない。既存の順序値を100倍し、変換済み値を再度100倍しないよう確認する。

既存 manifest は移行時にバックアップする。実行時には変更関数全文を表示する。検証は限定 pytest とし、全体 pytest は Phase 終了時に行う。

**次段階との境界：** Suspension identity の7701への追加、eta-family 定義の帰属先と証明使用順序の整理、Web 探索の切り替えは今回行わない。
