## Phase 154 proof-prose generation refinement

Phase 154 refined the public Narrative prose generated from existing proof provenance. It did not add new Toda theorem facts, proof edges, proof search, or a second proof engine.

The phase addressed the following presentation defects through shared rules rather than group-specific fixes:

- internal inference-rule / type-name leakage in public prose,
- English semantic statements such as `is injective` and `is exact`,
- repeated semantic reason prose,
- Reference-to-proof-body linkage,
- malformed sentence composition around reused References and semantic facts,
- Narrative transition wording,
- ASCII punctuation normalization for Japanese proof prose.

The final Narrative punctuation policy is:

```text
prose comma  = ", "
prose period = "."
```

This policy applies to prose only. TeX / mathematical punctuation and literature-title punctuation such as `Proposition 5.8.` are preserved.

The punctuation closure audit covered all standard depth-2 public Narratives

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7,
$$

for a total of 112 groups:

```text
scanned groups: 112
rendered groups: 112
exceptions: 0
japanese comma violations: 0
japanese period violations: 0
affected groups: 0
ascii comma prose lines: 484
groups with ascii comma prose: 112
ascii period prose endings: 587
groups with ascii period prose: 112
```

The Phase 154 closure audit then rechecked the full proof-prose contract:

```text
Phase 154 focused regression:
44 passed

ordering / reason regression boundary:
57 passed

112-group closure audit:
scanned groups: 112
rendered groups: 112
exceptions: 0
violations: 0
affected groups: 0

transition_repetition: 0
semantic_duplication: 0
internal_fallback_leakage: 0
english_prose: 0
reference_linkage: 0
ordering: 0
punctuation: 0
```

Reference coverage at closure was:

```text
groups with Reference section: 93
groups with body Reference markers: 89
```

Two apparent ordering findings for the dedicated $\pi_8^5$ and $\pi_{15}^8$ routes were audit false positives caused by substring matching between `## 証明` and `## 証明対象`. Exact heading-line counting and ordering confirmed that both routes have

```text
## 証明対象
→ ## 使用する結果
→ ## 証明
```

in the intended order.

Some Phase 149 / Phase 150 historical presentation tests were updated to the current Phase 154 contract:

- numbered derivation punctuation now expects `より, `,
- duplicate `FINAL_RESULT_DERIVATION` prose is expected only once in the public Narrative,
- reason-vocabulary punctuation now uses ASCII commas.

These were test-contract maintenance changes; production proof semantics were not changed.

Phase 154 documentation closure does not claim a repository-wide all-pass result. The final full regression remains the Phase-final step.
