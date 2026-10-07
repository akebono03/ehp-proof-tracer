Phase 159 R1-7c R3 repair4 repair1
====================================

原因:
- repair4 production / focused tests は PASS。
- 失敗した Phase157 test は古い `**[R1] (5.3).**` を固定していた。
- 現行 public Reference では `(5.3)` は `Equation 5.3` と表示される。
- Reference number `[Rk]` は必要参照の集合と順序で変わるため固定しない。

変更:
- production code changes: none
- test_phase157_r5_r6_53_bracket_definition_reference.py の1関数だけ変更
- `import re` を追加
- `Equation 5.3` を任意の `[Rk]` で確認
- bracket definition formula の存在確認は維持

repository-wide pytest は実行しない。
