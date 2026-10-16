# Phase 165 R6-1 R2：同名モジュール修正

現行 GitHub の package 側ファイルは、共通探索接続前の古い版でした。前回の修正パッチは誤って共通探索呼び出しの存在を要求していました。今回はこの不正な条件を除き、旧 Provider クラス・関数と旧引数の存在を確認してから、既に撤去済みのルート版に同期します。

変更対象：`phase165_r52_r7_registered_common_proof/phase165_r52_r7_registered_common_proof.py`（ファイル全体）。ルート側を変更しません。元ファイルのバックアップを作成します。

対象テスト：`test_shadow_fix.py` と `phase165_r52_r7_registered_common_proof/test_phase165_r52_r7_registered_common_proof.py`。全体 pytest は実施しません。R6-2 の汎用逆向き規則実装は対象外です。
