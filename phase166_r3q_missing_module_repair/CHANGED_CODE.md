# Phase 166 R3-Q：モジュール配置修復

変更対象：プロジェクト直下へ新規配置する `phase166_r3q_hopf_image_relation.py`。クラス変更なし。既存関数変更なし。新規ファイル内の import・関数全文は同梱ファイルで確認できる。前回 ZIP のソースと同じバイト列を使用し、挙動変更なし。

pytest：`phase166_r3q_generatorimage_canonical/test_phase166_r3q_generatorimage_canonical.py`（4件）、`phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py`（6件）。完了条件：トップレベル import 成功、10件 PASS、Web POST の再確認。次工程の台帳重複整理・掲載順接続は行わない。全体 pytest は Phase 166 終了時のみ実行。
