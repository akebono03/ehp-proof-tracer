# Phase 158-R3 stale boundary helper repair4

## 原因

repair3 の `_body()` は

`rendered.find("## 証明")`

を使用していた。

public Narrative には先に

`## 証明対象`

が存在するため、`## 証明` が部分一致し、proof body の開始位置を誤認した。

その結果、Reference section にある (5.3) の bracket definition まで
`body` に含まれていた。

## 変更対象

Production code:
- 変更なし

Test file:
- `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`

Helper:
- `_body()`

import 変更:
- なし

## 修正

旧:
`marker = "## 証明"`

新:
`marker = "\n## 証明\n"`

section heading を完全な行境界で一致させる。

## 実行する pytest

- depth2 boundary test
- depth3 boundary test

その後:
- stale intro contract audit
- Phase 158-R3 112-group audit

全体 pytest は Phase 158 の最後のみ。
