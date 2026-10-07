Phase 159 - pi_4^3 repair3b
Provider-anchor ancestry audit

目的
----
repair3a で確認された

  local body には必要な事実が存在する
  current chain_ids にはそれらが入らない
  ordered contributions = 0

という状態について、現在の supporting-block provider を起点に
presentation graph を upstream（前提方向）へたどり、

  Delta(iota_5)=+-2 eta_2
  -> Im Delta = Z{2 eta_2}
  -> ker E = Z{2 eta_2}

および

  pi_4^5 = 0
  + exactness
  -> E surjective

が provider-anchor ancestry に含まれるかを確認する。

監査対象
--------
- argument 0 conclusion
- supporting-block providers
- current _anchored_chain_step_ids() result
- provider anchors から upstream へたどった ancestry
- target facts の current_chain / upstream membership
- target facts から provider anchor までの shortest path
- target 周辺の presentation edges

変更対象
--------
なし。

Production code changes: NONE
Existing test changes: NONE
Document changes: NONE

pytest
------
実行しない。
repository-wide pytest は Phase の最後にのみ実行する。

完了条件
--------
次のいずれかまで分類する。

1. PROVIDER_ANCESTRY_CONTAINS_REQUIRED_BODY
   必要な本文事実は provider anchor の upstream prerequisite として存在する。
   current anchored-chain construction の向きが欠落原因。

2. QUOTIENT_ANCESTRY_CONFIRMED_ONLY
   Delta -> Im Delta -> ker E は upstream にあるが、
   surjectivity 側は同じ ancestry だけでは説明できない。

3. PROVIDER_ANCESTRY_INCOMPLETE
   必要な quotient chain 自体が current providers の upstream に揃わない。
   argument/provider ownership をさらに監査する必要がある。

Phase 境界
----------
repair3b は audit-only。
production code 修正は診断結果を確認してから次 repair で行う。
