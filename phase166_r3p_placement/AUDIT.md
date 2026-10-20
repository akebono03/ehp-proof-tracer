# Phase 166 R3-P 実装境界

変更対象：

- `phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` 全体（関数末尾の接続のみ変更）
- `phase166_r3c_publication_order.py` の `precedes_citing_assertion()` 全体（同じ文献順序位置にある異なる登録 ID の内部順序比較を許容）
- 新規 `phase166_r3p_position_binding.py` の `place_r3p_reference_positions()`（統合後の指定位置で追加）
- 新規 `tests/test_phase166_r3p_positions.py` のテスト3件

`publication_position` は引き続き保持する。既存 manifest の番号は変更しない。既存出典 ID・数学的主張・ProofStepLink・Renderer・推論規則に変更を加えない。

出典の区分と証明使用順序は別に扱い、η-family 定義を Proposition 5.1 の文献本文に存在したと断定しない。全体 pytest は実行しない。
