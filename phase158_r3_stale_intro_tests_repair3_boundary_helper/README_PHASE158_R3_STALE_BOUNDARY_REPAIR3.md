# Phase 158-R3 stale boundary helper repair3

## 原因

`tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`
の `_body()` helper が、証明本文の開始位置を prose 文字列

`次に, $\nu'$ の位数を決定するために`

で探していた。

現在の public Narrative では証明本文は `## 証明` section で明示され、
pi6_3 の本文も `まず, ...` から始まる。

そのため helper の prose 固定は stale。

## 変更対象

Production code:
- 変更なし

Test file:
- `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`

変更 helper:
- `_body()`

変更 tests:
- `test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary`
- `test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary`

import 変更:
- なし

## 修正内容

`_body()` は `## 証明` を public boundary として使用する。

本文開始 expectation は現行 baseline の

`まず, $\nu'$ の位数を決定するために`

へ合わせる。

数学内容・Reference attribution・production renderer は変更しない。

## 実行する pytest

depth2 / depth3 の2 test functions のみ。

その後:
- stale intro contract audit
- Phase 158-R3 112-group audit

全体 pytest は Phase 158 最後のみ。
