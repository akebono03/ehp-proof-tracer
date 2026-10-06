Phase 159 R1-7c R3 repair4 repair3
====================================

診断結果
--------
repair4 repair2 audit により次を確認した。

- current pi_6^3 public Reference:
  [R2] (5.3).
- bracket definition も Reference 内に存在する。
- repair4 pruner direct call:
  entries_equal=True
  lines_equal=True

したがって repair4 production regression ではない。

前回 repair1 で `(5.3)` を `Equation 5.3` に変更した test expectation は誤り。
正しい current contract は:

- locator title は `(5.3)` のまま
- Reference number は `[R1]` に固定しない
- 任意の `[Rk]` として `(5.3)` が存在すればよい
- bracket definition formula の存在確認を維持する

変更
----
Production code changes: none

変更ファイル:
tests/test_phase157_r5_r6_53_bracket_definition_reference.py

変更 test:
test_phase157_r5_r6_pi6_reference_53_displays_bracket_definition()

repository-wide pytest は実行しない。
