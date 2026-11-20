# Phase 176 R3R31R1 — テスト修正

## 原因

旧テストの `incorrect` は、関数外に8スペース字下げした文を置いており、`ast.parse()` が `IndentationError` で停止していた。テストしたかったのは「構文が有効だが、アンカーが `shared_expansion_provider()` の外側にある」場合である。

## 変更対象

- `phase176_r3r31_generic_hopf_public_connection/tests/test_installer.py` の `test_patch_rejects_outside_function()` 全文だけを置換。import は変更しない。
- 新規 `phase176_r3r31r1_outside_function_test_fix/installer.py`、`run.ps1`、新規テスト、文書。
- 既存の `installer.py`、共有探索、数学規則、GIVEN は変更しない。

## 完了条件

新しいテスト入力は構文的に有効で、`ANCHOR_OUTSIDE_SHARED_PROVIDER` により拒否される。限定 pytest のみ実施し、全体 pytest は Phase 終了時まで実施しない。

## 次 Phase の境界

R3R32 では、R3R31 監査で `equality symmetry` しか候補がなかった中間 Hopf 値を扱う。根の群構造を先取りしない。
