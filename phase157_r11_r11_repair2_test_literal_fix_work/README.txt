Phase157 R11-R11 repair2 — test literal fix

失敗原因:
R11-R11 で既存 test を更新した際、
`"\n## 証明\n"` が壊れた multiline string になった。

repair2:
- `tests/test_phase157_r5_r9_fixed_definition_body_suppression.py`
  の対象 test function 全体だけを修復。
- production code は変更しない。
- py_compile 後、R11-R11 focused pytest を再実行する。
- full repository pytest は Phase157 closure まで実行しない。
