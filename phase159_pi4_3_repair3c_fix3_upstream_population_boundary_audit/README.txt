Phase 159 - repair3c fix3
Upstream contribution population boundary audit

背景
----
repair3c fix2 により性能上の停止は解消方向に進んだが、
phase144_6_r5_42 の selected population が

  expected 223
  actual   3131

へ膨張した。

placement 内訳も特に

  before_dependent_contribution:
    expected 64
    actual   2784

となっている。

目的
----
repair3c により追加された selected contributions を

- legacy_downstream
- upstream_only

に分類し、upstream-only の大量増加を

- target group
- statement type
- argument role
- placement
- provider_anchor

で分解する。

また pi_4^3 を直接監査し、必要な4 statement

- TodaDeltaImageUpToSignStatement
- TodaDeltaImageFreeCyclicStatement
- TodaSuspensionKernelFreeCyclicStatement
- TodaSuspensionSurjectiveStatement

が legacy downstream か upstream-only かを確認する。

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
既存 contribution population を保ったまま pi_4^3 に必要な upstream body facts
だけを一般則で追加するための boundary を特定できること。

この監査結果を見るまで selection semantics の production 修正は行わない。
