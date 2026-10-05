# Phase 158-R3 stale boundary repair5

## 原因

depth 3 の public proof body は depth 2 より祖先事実が1段深く表示されるため、
本文先頭が同一ではない。

depth 2:
- `まず, $\nu'$ の位数を決定するために ...`

depth 3:
- `$\pi_4^3 = \mathbb{Z}/2\{\eta_3\}$.`
- その後に `次に, $\nu'$ の位数を決定するために ...`

したがって、両 depth で同じ prose から始まることを固定した test は stale。

## 変更対象

Production code:
- 変更なし

Test file:
- `tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py`

変更 tests:
- `test_phase156_r5_repair9_depth2_public_body_starts_after_53_boundary`
- `test_phase156_r5_repair9_depth3_public_body_starts_after_53_boundary`

import 変更:
- なし

## 修正内容

exact prose start の assertion を削除し、

- proof body が空でない
- EHP sequence の `$\pi_7^3$` が proof body に含まれる

ことを確認する。

既存の boundary contract:
- `(5.3)` は Reference side
- Lemma 5.2 は public Reference に出ない
- bracket definition は Reference side にのみ存在
- proof body には漏れない

は維持する。

## 実行する pytest

depth2 / depth3 の2 test functions のみ。

その後:
- stale intro contract audit
- Phase 158-R3 112-group audit

全体 pytest は Phase 158 最後のみ。
