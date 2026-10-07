Phase 159 - repair3c fix4
Legacy selection delta audit

目的
----
repair3c 前の contribution selection を、現行の同じ presentation / arguments /
proof_chains 上で再現し、repair3c 後との差分を step identity で直接比較する。

fix3 では current selected row が legacy downstream chain に属するかだけを見たため、
legacy selected population そのものとの厳密比較ではなかった。

fix4 では以下を再現する。

- legacy downstream-only _anchored_chain_step_ids
- legacy necessity
- legacy provider-key membership
- legacy visibility occurrence
- legacy owner selection

これを current production selection と同一 context 上で比較する。

確認項目
--------
各 TARGET:
- legacy selected count
- current selected count
- added count
- removed count
- added/removed statement type
- added role / placement / provider_anchor

pi_4^3:
4つの必要 fact を個別に確認する。

- TodaDeltaImageUpToSignStatement
- TodaDeltaImageFreeCyclicStatement
- TodaSuspensionKernelFreeCyclicStatement
- TodaSuspensionSurjectiveStatement

各 fact について:
- legacy selected か
- current selected か
- base public markdown にすでに存在するか
- rendered prose

変更
----
Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
実行しない。
repository-wide pytest も実行しない。

完了条件
--------
repair3c が本当に追加した selected contribution の集合を厳密に特定し、
pi_4^3 に必要な fact と大量増加分を分離する一般的 boundary を設計できること。

この結果を見るまで production selection の追加修正は行わない。
