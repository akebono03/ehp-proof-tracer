Phase 156-R5 repair11 Proposition 5.1 path diagnostic

Production changes: none.

目的
====
repair11 で Proposition 5.1 が public Reference から prune されなかった理由を、
proof graph の実際の path から確定する。

出力
====
depth 2 / 3 ごとに:
- Proposition 5.1 Reference entry の各 ProofStep
- rendered statement
- internal / owned 判定
- direct consumer
- internal step を除外した状態で root へ到達する shortest path
- path 上の Reference / rule / rendered statement
- public Reference headers

判定したいこと
==============
1. Proposition 5.1 が本当に parent proof から直接利用されているか。
2. aggregate / semantic closure / bridge により偽の外部 path が生じているか。
3. entry 単位ではなく statement/component 単位の pruning が必要か。

この診断結果が出るまでは Proposition 5.1 の特別除外は行わない。
