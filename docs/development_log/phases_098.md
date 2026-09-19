# Phase 98 開発記録

この文書は Phase 98 の chronological development record である。

Phase 98 の主題:

```text
user-facing input / report-access convenience
```

Phase 97 までの structured calculation-to-report API を壊さず、actual usage pressure がある convenience のみを薄く追加することを目的とした。

---

# Phase 98-1

## current user-facing convenience pressure audit

確認した主対象:

```text
TodaGroupQuery
build_toda_calculation_report_result()
build_toda_found_calculation_report_result()
TodaCalculationReportResult
TodaCalculationReportCandidate
NOT_FOUND / FOUND / MULTIPLE_RESULTS
```

監査結論:

```text
raw n,k convenience
→ 実需要あり

single FOUND report access
→ 実需要あり

MULTIPLE_RESULTS report collection
→ 実需要あり

NOT_FOUND fixed human-readable message
→ core model では不要

new facade class
→ 不要

candidate ranking / best selection
→ 不要
```

境界:

```text
core proof/calculation
↓
TodaCalculationReportResult
↓
thin convenience
↓
future CLI / Web UI
```

---

# Phase 98-2

## minimal facade representation / API

追加:

```text
toda_calculation_facade.py

build_toda_report(
  repository,
  n,
  k,
)
```

実装は:

```text
raw n,k
↓
TodaGroupQuery
↓
build_toda_calculation_report_result()
```

のみ。

`TodaGroupQuery` validation を再実装しない。

確認:

```text
focused:
7 passed in 8.74s

Phase 97 + Phase 98-2 related:
18 passed in 5.85s

repository-wide:
7616 passed in 123.28s

git diff --check:
clean
```

---

# Phase 98-3

## actual-use facade validation / convenience boundary audit

production code 追加なし。

代表6 target:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

確認:

```text
raw n,k facade から全6 target FOUND
query / target construction
candidate identity
group semantics
goal-source provenance
pi9_5 EHP / exactness / proof-root identity
nested branch
sigma''' branch
repository non-mutation
```

結果:

```text
focused:
9 passed in 7.39s

related:
24 passed in 5.30s

repository-wide:
7625 passed in 119.20s

git diff --check:
clean
```

---

# Phase 98-4

## single FOUND report access convenience audit / minimal property

追加:

```text
TodaCalculationReportResult.report
```

semantics:

```text
FOUND
→ candidates[0].report を返す

NOT_FOUND
→ ValueError

MULTIPLE_RESULTS
→ ValueError
```

MULTIPLE_RESULTS で first candidate を silent selection しない。

確認:

```text
focused:
5 passed in 11.16s

Phase 97/98 related:
45 passed in 9.15s

repository-wide:
7630 passed in 110.32s

git diff --check:
clean
```

---

# Phase 98-5

## NOT_FOUND / MULTIPLE_RESULTS human-facing access audit

監査結論:

```text
NOT_FOUND fixed message
→ core model では不要

MULTIPLE_RESULTS report collection
→ convenience pressure あり
```

追加:

```text
TodaCalculationReportResult.reports
```

semantics:

```text
NOT_FOUND
→ ()

FOUND
→ (report,)

MULTIPLE_RESULTS
→ 全 candidate.report を candidate order で tuple 化
```

確認:

```text
focused:
5 passed in 10.30s

Phase 97/98 related:
28 passed in 8.92s

repository-wide:
7635 passed in 112.51s

git diff --check:
clean
```

---

# Phase 98-6

## representative actual-use convenience validation

production code 追加なし。

最短 user-facing path:

```text
raw n,k
→ build_toda_report()
→ TodaCalculationReportResult
→ result.report
→ result.reports
```

代表6 target で確認:

```text
all FOUND
single report access
ordered reports access
full human-readable report
candidate identity
goal-source provenance
pi9_5 EHP / exactness / proof-root identity
repository non-mutation
```

結果:

```text
focused:
8 passed in 8.64s

Phase 98 related:
27 passed in 9.94s

repository-wide:
7643 passed in 123.73s

git diff --check:
clean
```

---

# Phase 98-7

## final audit / documentation

最終監査:

```text
proof truth unchanged
calculation semantics unchanged
presentation / renderer semantics unchanged
candidate identity/order preserved
direct / aggregate provenance preserved
NOT_FOUND / FOUND / MULTIPLE_RESULTS preserved
no silent multiple-result selection
repository non-mutation preserved
representative six-target shortest-path validation complete
```

Phase 98 で追加した convenience:

```text
build_toda_report(repository, n, k)
TodaCalculationReportResult.report
TodaCalculationReportResult.reports
```

Phase 98 で追加しなかったもの:

```text
new facade class
NOT_FOUND fixed human-readable message
candidate ranking
preferred result
new proof logic
new calculation logic
new provenance schema
```

---

# Phase 98 最終状態

```text
raw n,k
→ build_toda_report()
→ TodaGroupQuery
→ calculation
→ TodaCalculationResult
→ ordered candidate handling
→ end-to-end presentation
→ unified full proof report
→ TodaCalculationReportResult
→ report / reports
```

formal status:

```text
Phase 98
→ COMPLETE
```

次の推奨:

```text
Phase 99-1
→ current exploration / query capability pressure audit
```

候補:

```text
element-centered search
Toda bracket containment
map-image lookup
applicable lemma discovery
coset / indeterminacy representation
derived-result enumeration
```
