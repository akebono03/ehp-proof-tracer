# Phase 98 — User-Facing Convenience 記録

この文書は Phase 98 で追加した user-facing convenience capability と proof-truth boundary を記録する。

---

# 1. 目的

Phase 97 までで:

```text
ProofRepository
TodaGroupQuery(n,k)
→ calculation
→ presentation
→ full proof report
→ TodaCalculationReportResult
```

が存在した。

Phase 98 の目的:

```text
actual usage pressure がある入力・report access convenience のみ追加
```

境界:

```text
convenience facade != proof truth
```

---

# 2. Raw n,k facade

追加:

```text
build_toda_report(
  repository,
  n,
  k,
)
```

flow:

```text
raw n,k
↓
TodaGroupQuery(n,k)
↓
build_toda_calculation_report_result()
↓
TodaCalculationReportResult
```

query validation は `TodaGroupQuery` に委譲する。

---

# 3. Single FOUND report access

追加:

```text
TodaCalculationReportResult.report
```

semantics:

```text
FOUND
→ exactly one candidate.report

NOT_FOUND
→ ValueError

MULTIPLE_RESULTS
→ ValueError
```

`MULTIPLE_RESULTS` から first candidate を自動選択しない。

---

# 4. Ordered report collection access

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
→ tuple(candidate.report for candidate in candidates)
```

candidate order をそのまま保持する。

---

# 5. Candidate alignment invariant

Phase 97 から引き続き:

```text
report_result.candidates[i].source_candidate
is report_result.calculation_result.candidates[i]
```

Phase 98 convenience は candidate を再構築・並べ替えしない。

---

# 6. Provenance preservation

raw n,k facade、`report`、`reports` のいずれも:

```text
direct result provenance
aggregate goal-source provenance
branch path
proof-step identity
EHP / exactness provenance
recursive provenance
```

を変更しない。

---

# 7. Repository non-mutation

convenience layer は repository を mutate しない。

---

# 8. Representative shortest-path validation

対象:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

最短 user-facing path:

```text
raw n,k
→ build_toda_report()
→ result.report
→ result.reports
```

全6 target が `FOUND`。

---

# 9. Group semantics preservation

代表 target で:

```text
direct sum
finite cyclic
zero group
generator order
nested aggregate branch
sigma''' branch
```

を保持。

---

# 10. EHP / exactness preservation

actual \(\pi_9^5\) では EHP / exactness presentation と proof-root identity を convenience layer 後も保持。

---

# 11. NOT_FOUND boundary

Phase 98 では core model に fixed human-readable message を追加しない。

理由:

```text
status + candidates + reports
で structured semantics は十分

message wording は
CLI / Web UI / presentation surface の責務
```

---

# 12. MULTIPLE_RESULTS boundary

Phase 98 は:

```text
all reports preserved
ordered access available
```

まで。

次は行わない:

```text
ranking
best selection
preferred candidate
silent first-candidate selection
```

---

# 13. Final regression

```text
Phase 98-6 focused:
8 passed in 8.64s

Phase 98 related:
27 passed in 9.94s

repository-wide:
7643 passed in 123.73s

git diff --check:
clean
```

---

# 14. Completion

```text
raw n,k
→ thin facade
→ structured report result
→ safe single-report access
→ lossless ordered multi-report access
```

formal status:

```text
Phase 98
→ COMPLETE
```

次:

```text
Phase 99-1
→ current exploration / query capability pressure audit
```
