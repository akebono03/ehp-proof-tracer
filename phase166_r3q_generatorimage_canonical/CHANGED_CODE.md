# Phase 166 R3-Q：GeneratorImage 正規化

## 変更対象

1. `phase166_r3p_position_binding.py`: `place_r3p_reference_positions()` 全体を置換。`GeneratorImage` の内容と出典を照合し、既存の Hopf 主張位置100へ結び付ける。
2. `phase165_r52_r9_shared_math.py`: `build_shared_typed_bridge()` 全体を置換。対応する Relation の直接 GIVEN リンクを共通 bridge の中で除外する（主張登録 ID は維持）。`shared_expansion_provider()` 全体を置換。変換規則を逆向き探索に接続。
3. 新規 `phase166_r3q_hopf_image_relation.py`: `_compatible_element()`、`_is_image_equality()`、`hopf_image_relation_rule()`、`expand_hopf_image_relation()`。
4. 新規 `test_phase166_r3q_generatorimage_canonical.py`: 4テスト。既存6回帰テストも実行。

既存ファイルの import 節は変更しない。変更関数全文は `apply.py` で生成しバックアップ配下の `*.py.txt` に保存する。新規ファイルは import・関数全文を省略せず収録した。既存登録工場と Renderer は変更しない。

## 完了条件

新規4テストと π₃² Web回帰6テストの合計10 PASS。失敗時は2ファイルを自動復元。全体 pytest は実行しない。

## 次の境界

通常 Web に掲載順判定を接続する工程と、台帳に残る重複した Relation assertion 自体の整理は別工程。今回の対応は共通 bridge 内の GIVEN 二重性を解消し、1文献主張から型付き等式を導出することに限定する。
