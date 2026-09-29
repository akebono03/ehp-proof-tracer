---

# 28. Phase 144 generic Narrative / ownership boundary

Phase 144 は、Phase 143 で semantic statement rendering を整備した後、証明全体の
Narrative を一般構造だけで組み立てる際の ownership（所有関係）、argument boundary
（議論境界）、contribution ordering（寄与の順序）を監査した。

基本経路は次のとおり。

```text
TodaGroupResult
→ existing ProofStep provenance
→ replay / complete replay
→ TodaGroupProofPresentation
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ proof chains / contributions
→ contribution-aware generic Narrative renderer
```

この経路は新しい proof search ではない。

```text
complete replay
!= new theorem search

semantic closure
!= theorem synthesis

argument ownership
!= proof edge ownership

Narrative contribution placement
!= proof graph mutation
```

## explicit depth と complete replay

Narrative では explicit positive depth の presentation に必要な semantic dependency が
bounded replay の外側にある場合がある。このため complete replay API を用いる経路を持つ。

ただし depth 0 は root のみを要求する明示的境界であり、complete replay へ切り替えない。

```text
Narrative + explicit depth > 0
→ 必要に応じて complete replay から presentation を構築

Narrative + depth 0
→ bounded depth-0 replay を維持
```

Phase 144 final regression repair では、この depth 0 境界を `main.py` で復元した。

## R25-30-R3 ownership / argument-boundary endpoint

Phase 144-6 の技術調査は R25-30-R3 を endpoint とする。

6代表群の current inventory:

```text
pi_6^3:  selected=6   participating=6/6   detached=0/0    transport=1
pi_8^5:  selected=10  participating=7/7   detached=3/3    transport=1
pi_10^4: selected=22  participating=0/0   detached=22/0   transport=2
pi_12^5: selected=46  participating=2/2   detached=44/0   transport=4
pi_15^8: selected=54  participating=10/10 detached=44/0   transport=4
pi_16^9: selected=54  participating=10/10 detached=44/0   transport=4
```

aggregate:

```text
selected=192
participating=35
detached=157
detached_insertable=3
missing=0
```

R25-30-R3 では、対象3ケースの boundary classification と existing child Argument pair が
一致した。したがって `detached_insertable=3` を ownership leak とみなして旧
`detached_insertable=0` へ戻してはならない。

```text
historical R5 fixed-count snapshot
!= current semantic gate
```

## result-reuse pressure の分離

$\pi_{15}^{8}$、$\pi_{16}^{9}$ などで group-structure / definition の owned entry が
大きな proof subtree を再帰的に展開する現象が確認された。

これは

```text
argument-boundary leak
```

ではなく、

```text
already-established result の proof subtree を再展開する result-reuse problem
```

として分離する。

Phase 144 ではこの問題の一般解を実装しない。具体的な証明で必要になった Phase 146
以降に、その1課題だけを解く最小一般規則として扱う。

## Phase 144 regression evidence

canonical final repository-wide run:

```text
10298 collected
10273 passed
25 failed
2321.20s (0:38:41)
```

25 failures は R5-39〜R5-43 の historical completion / fixed-count snapshot に集中した。
production renderer は変更せず、固定件数を新しい固定件数へ置換することもせず、
current structural invariant に maintenance した。

focused maintenance regression:

```text
66 passed in 1308.82s (0:21:48)
```

この maintenance 後は repository-wide suite を再実行していない。そのため設計記録では
「全体 10298 passed」とは記載しない。

## Phase 145 / Phase 146+ 境界

Phase 145:

```text
default presentation → Narrative
default depth → 2
```

のみを扱う。

Phase 145 では result reuse、ownership の追加一般化、statement type の先回り実装を行わない。

Phase 146 以降:

```text
具体的に通したい証明
→ その証明で不足している1課題を特定
→ target-specific special case ではなく最小一般規則で解く
→ focused regression
→ 既存証明を壊さない
```

を1 Phaseずつ繰り返す。
