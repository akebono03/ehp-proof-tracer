# Phase 97 開発記録

この文書は Phase 97 の chronological development record である。

Phase 97 の主題:

```text
user-facing proof-report query / calculation-to-report API
```

Phase 96 までの calculation / presentation / renderer API を、proof truth を変更せず top-level reporting API として compose することを目的とした。

---

# Phase 97-1

## current calculation-to-report orchestration boundary audit

結論:

```text
repository は caller-owned
FOUND は exactly one candidate
MULTIPLE_RESULTS は silent selection しない
NOT_FOUND は fake report を作らない
structured result を primary API とする
direct / aggregate provenance は既存 candidate identity で保持
```

---

# Phase 97-2

## minimal top-level result representation

追加:

```text
TodaCalculationReportCandidate
TodaCalculationReportResult
```

主要 invariant:

```text
presentation.source_candidate
is source_candidate
```

および:

```text
report_result.candidates[i].source_candidate
is report_result.calculation_result.candidates[i]
```

確認:

```text
focused:
13 passed in 14.89s

related:
77 passed in 16.51s

repository-wide:
7590 passed in 136.07s
```

---

# Phase 97-3

## single FOUND calculation-to-report API

追加:

```text
build_toda_found_calculation_report_result()
```

production code は既存 API の compose のみ。

初回テストでは LaTeX literal の過剰 escape を修正。

修正後:

```text
focused:
19 passed in 9.70s

related:
70 passed in 10.89s

repository-wide:
7596 passed in 127.48s
```

---

# Phase 97-4

## NOT_FOUND / MULTIPLE_RESULTS top-level handling

一般 API:

```text
build_toda_calculation_report_result()
```

semantics:

```text
NOT_FOUND
→ report candidates = ()

FOUND
→ report candidate 1件

MULTIPLE_RESULTS
→ 全 candidate を順序保持して report 化
```

初回 validation では失敗時 pytest repr が巨大 provenance object を展開して重くなったため、Phase 97-4 の本質ではない renderer detail assertion を軽量化。

修正後:

```text
focused:
5 passed in 8.40s

Phase 97 related:
24 passed in 6.63s

repository-wide:
7601 passed in 125.78s
```

---

# Phase 97-5

## actual representative targets end-to-end top-level API validation

production code 追加なし。

対象:

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
all six FOUND
candidate identity preservation
direct sum / finite cyclic / zero semantics
generator orders
nested branch provenance
goal-source phase/theorem/branch
pi9_5 EHP / exactness
proof-root identity
full Markdown report
repository non-mutation
```

最終確認:

```text
focused:
8 passed in 9.99s

Phase 97 related:
32 passed in 9.44s

repository-wide:
7609 passed in 121.63s

git diff --check:
clean
```

---

# Phase 97-6

## final audit / documentation

最終監査:

```text
proof truth unchanged
calculation semantics unchanged
presentation / renderer semantics unchanged
candidate identity/order preserved
NOT_FOUND / FOUND / MULTIPLE_RESULTS preserved
no silent multiple-result selection
direct / aggregate provenance preserved
repository non-mutation preserved
representative six-target top-level validation complete
```

user-facing input boundary:

```text
(n, k)
→ TodaGroupQuery(n, k)
→ build_toda_calculation_report_result()
```

raw `n, k` overload は convenience として deferred。

---

# Phase 97 最終状態

```text
TodaGroupQuery
→ calculation
→ TodaCalculationResult
→ ordered candidate handling
→ end-to-end presentation
→ unified full proof report
→ TodaCalculationReportResult
```

formal status:

```text
Phase 97
→ COMPLETE
```

次の推奨:

```text
Phase 98-1
→ current user-facing convenience pressure audit
```
