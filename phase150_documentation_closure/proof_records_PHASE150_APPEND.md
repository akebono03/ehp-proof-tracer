---

<!-- PHASE150_CLOSURE -->
# Phase 150 RC4 Generic provenance / reason prose provenance record

Phase 150 は新しい Toda theorem fact を追加していない。

対象は Phase 146 の RC4:

```text
Generic provenance / reason prose
```

である。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 150 の typed reason は、既存 proof provenance と semantic sidecar から導出される
Narrative presentation 上の理由情報である。

```text
typed reason
!= theorem fact

reason sentence
!= proof edge

reason sidecar
!= proof search

visible reason
!= provenance mutation
```

## visible reason multiplicity

6代表群:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9
$$

について typed reason と rendered sentence の多重度を監査した。

共通 generic reason sentence について:

```text
pi_6^3:  typed=3, rendered=3
pi_8^5:  typed=3, rendered=3
pi_10^4: typed=2, rendered=2
pi_12^5: typed=2, rendered=2
pi_15^8: typed=1, rendered=1
pi_16^9: typed=3, rendered=3
```

したがって、複数回出現した共通 sentence は単一 reason の renderer duplication ではない。
異なる typed reason instance が同一 generic prose へ写された結果である。

final contract:

$$
\#\{\text{typed reasons rendering to }s\}
=
\#\{\text{rendered occurrences of }s\}.
$$

Repair R2 は production renderer を変更せず、この instance-level contract を test した。

focused:

```text
RC4-5:
9 passed in 5.65s

nine-failure repair set:
17 passed in 9.03s
```

## Phase 148 exactness compatibility

Phase 150 final regression で検出された Phase 148 関連 historical failures は、
semantic exactness evidence の消失ではなかった。

proof provenance 上の typed exactness statement は維持されている一方、現行 generic Narrative は
旧 literal exactness phrase を必須としない。

したがって historical display expectation を現行 presentation contract に合わせた。
production proof provenance は変更していない。

## renderer-route provenance boundary

Phase 150 では一部代表群の generic route 移行が進んだが、全群が同一 route になったわけではない。

この coexistence 自体が群間の Narrative 差を作るため、以後は group-by-group migration を
継続しない。

Phase 151 では public route を変更せず、対象 population 全体を同一 generic route へ通して
baseline を取得する。

```text
forced generic audit
!= public route change

generic comparison
!= proof provenance change

route unification planning
!= dedicated renderer deletion
```

## final verification record

Phase 150 final full regression:

```text
Python 3.10.3
pytest 9.1.1
branch: develop

10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

したがって Phase 150 closure 時点で canonical repository test population は全PASSである。

## next-phase provenance boundary

Phase 151 は `All-Group Generic Baseline`。

新しい theorem fact、proof edge、proof search、public route switch を追加せず、同一 generic
presentation route による whole-population observation を行う。

Phase 152 でその結果を defect category に分類し、Phase 153 以降で1カテゴリずつ最小一般規則を
実装する。
