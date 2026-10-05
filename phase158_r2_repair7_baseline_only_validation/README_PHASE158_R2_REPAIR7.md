# Phase 158-R2 repair7

## 目的

Phase 158-R2 の public shell normalization が、
R2 直前 baseline の Reference / Proof 内容を壊していないことだけを検証する。

## Production code

変更なし。

## Existing repository tests

変更なし。

次の Phase 154 tests は、GitHub 現行でも旧 Reference 番号を固定しており、
local pre-R2 baseline（Phase 157 後）と一致しないため、今回の focused set から除外する。

- `tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py`
- `tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py`

これらは R2 成否とは別に stale test repair として扱う。

## 実行

1. no-pyc syntax check
2. Phase 158 baseline-preservation focused tests
3. 112-group baseline-preservation audit
4. summary

## R2 completion candidate

- public contract valid: 112
- Reference payload preserved: 112
- Proof payload preserved: 112
- fully valid: 112
- exceptions: 0

全体 pytest は Phase 158 最後のみ。
