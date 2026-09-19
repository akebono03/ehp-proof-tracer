# Phase 97 — Calculation-to-Report Orchestration 記録

この文書は Phase 97 で追加した top-level reporting capability と proof-truth boundary を記録する。

---

# 1. 目的

Phase 96 までで:

```text
TodaGroupQuery
→ TodaCalculationResult
→ candidate
→ structured presentation
→ unified full proof report
```

が個別 API として存在した。

Phase 97 の目的:

```text
calculation-to-report orchestration
```

境界:

```text
report orchestration != proof truth
```

---

# 2. Result representation

candidate-level:

```text
TodaCalculationReportCandidate
```

fields:

```text
source_candidate
presentation
report
```

result-level:

```text
TodaCalculationReportResult
```

fields:

```text
calculation_result
candidates
```

---

# 3. Candidate alignment invariant

各 index で:

```text
report_result.candidates[i].source_candidate
is report_result.calculation_result.candidates[i]
```

report layer で candidate を再構築・並べ替えしない。

---

# 4. Single FOUND API

```text
build_toda_found_calculation_report_result(
  repository,
  query,
)
```

`FOUND` の exactly one candidate に限定。

---

# 5. General top-level API

```text
build_toda_calculation_report_result(
  repository,
  query,
)
```

flow:

```text
TodaGroupQuery
↓
build_toda_calculation_result()
↓
TodaCalculationResult
↓
candidate iteration
↓
build_toda_end_to_end_candidate_presentation()
↓
render_toda_full_proof_report_markdown()
↓
TodaCalculationReportCandidate
↓
TodaCalculationReportResult
```

---

# 6. Status semantics

```text
NOT_FOUND
→ report candidates = ()

FOUND
→ report candidate 1件

MULTIPLE_RESULTS
→ 全 report candidate を calculation order で保持
```

---

# 7. No silent selection

Phase 97 は ranking / best result / preferred candidate / silent first-candidate selection を一般 API に導入しない。

---

# 8. Direct result provenance

direct theorem-backed result では:

```text
goal_source = None
```

を report orchestration 後も維持。

---

# 9. Aggregate-derived provenance

aggregate-derived result は source entry、phase、theorem、branch path を保持。

nested branch も dotted path のまま保持する。

---

# 10. Representative top-level validation

対象:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

全6 target が一般 top-level API から `FOUND`。

---

# 11. Group semantics preservation

direct sum、finite cyclic、zero group、generator order、nested branch を presentation/report layer まで保持。

---

# 12. EHP / exactness preservation

actual \(\pi_9^5\) では EHP / exactness presentation と proof-root identity を top-level orchestration 後も保持。

---

# 13. Repository non-mutation

report orchestration は repository を read-only metadata source として利用する。

---

# 14. User-facing input boundary

現在の user-facing input:

```text
ProofRepository
TodaGroupQuery(n, k)
```

すなわち:

```text
(n, k)
→ TodaGroupQuery
→ top-level calculation-to-report API
```

raw `n, k` overload は convenience のため deferred。

---

# 15. Final regression

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

# 16. Completion

```text
query
→ calculation
→ candidate handling
→ structured presentation
→ unified full proof report
→ structured report result
```

formal status:

```text
Phase 97
→ COMPLETE
```

次:

```text
Phase 98-1
→ current user-facing convenience pressure audit
```
