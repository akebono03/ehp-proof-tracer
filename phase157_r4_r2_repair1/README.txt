Phase157-R4-R2 repair1

原因:
- Phase157-R2 では Proposition 5.15 が未登録だったため、
  unknown rule + Proposition 5.15 => None を期待していた。
- Phase157-R4-R2 で Proposition 5.15 が tracked reference になったため、
  unknown rule は PROOF_INTERNAL と分類されるのが現在の正しい契約。

変更:
- tests/test_phase157_r2_literature_statement_boundary.py
  の該当テスト1件のみ更新。

Production code changes:
- none

全体 pytest は Phase157 closure まで実行しない。
