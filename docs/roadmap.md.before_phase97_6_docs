# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面では、Toda の finite-dimensional calculation spine と stable \(G_0\) through \(G_7\) の主要 2-primary data を実装済み。

proof infrastructure:

```text
Proof Repository
→ automatic rule selection
→ concrete producer compatibility
→ bounded dependency search
→ max_depth parameterization
→ finite retry
→ diagnostics
→ selected-path execution
→ ProofStep provenance
```

calculation / explanation:

```text
TodaGroupQuery
→ direct theorem-backed lookup
→ aggregate concrete-branch fallback
→ branch ProofStep recovery
→ TodaGroupResult normalization
→ EHP / exactness provenance
→ flat dependencies
→ recursive proof provenance
→ TodaCalculationResult
```

presentation / report:

```text
structured presentation
→ EHP / exactness presentation
→ proof source presentation
→ dependency-first proof flow
→ LaTeX / Markdown rendering
→ mathematical statement rendering
→ readable proof narrative
→ unified full proof report
```

代表 target:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

最新 regression:

```text
7577 passed in 43.70s
```

---

# 2. 完了済み capability

Phase 90–96:

```text
query target construction
theorem-backed known-result lookup
normalized group structure / generators / orders
actual EHP extraction
exactness-use provenance
flat proof dependencies
dependency role classification
recursive proof provenance
aggregate theorem branch discovery
original branch ProofStep recovery
aggregate provenance
direct-result precedence
multiple-result preservation
top-level calculation orchestration
structured presentation
group / generator / order presentation
EHP / exactness presentation
proof source presentation
dependency-first proof flow
shared-dependency presentation
LaTeX / Markdown rendering
mathematical statement rendering
readable narrative
unified full proof report
final representative report audit
```

Phase 96 は正式 COMPLETE。

---

# 3. 次 Phase：Phase 97

主題:

```text
user-facing proof-report query / calculation-to-report API
```

現状:

```text
TodaGroupQuery
→ TodaCalculationResult
→ candidate
→ end-to-end presentation
→ full proof report Markdown
```

Phase 97 ではこれを user-facing top-level API にまとめる。

目標:

```text
(n, k)
↓
query
↓
calculation
↓
candidate handling
↓
presentation
↓
human-readable proof report
```

---

# 4. Phase 97-1 推奨監査

```text
current calculation-to-report orchestration boundary audit
```

監査対象:

```text
TodaGroupQuery
build_toda_calculation_result()
TodaCalculationResult
TodaCalculationStatus
TodaCalculationCandidate
build_toda_end_to_end_candidate_presentation()
render_toda_full_proof_report_markdown()
```

確認点:

```text
1. user-facing API の最小 input
2. repository の受け渡し
3. single FOUND convenience
4. MULTIPLE_RESULTS の保持
5. NOT_FOUND の扱い
6. string-only か structured result object か
7. direct / aggregate source preservation
8. proof truth / presentation boundary
```

---

# 5. Phase 97 で守る境界

再実装しない:

```text
group lookup semantics
aggregate branch discovery
proof recovery
group normalization
EHP extraction
dependency extraction
presentation model
mathematical renderer
narrative renderer
```

既存 API を compose する。

multiple candidate に対する ranking / best selection は行わない。

---

# 6. Deferred：symbolic higher-range instantiation

例えば:

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\]

\[
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
\]

\[
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
\]

の concrete specialization は別 capability とする。

---

# 7. Deferred：target-only proof-search fallback

query は target group だけを持ち、unknown RHS theorem goal は生成しない。

target-to-goal generation の actual need が生じたときに別 Phase で扱う。

---

# 8. Deferred：calculation failure diagnostics

現在:

```text
NOT_FOUND
FOUND
MULTIPLE_RESULTS
```

のみ。

`NOT_FOUND` の細分類は Phase 97 で actual need が確認された場合にのみ検討する。

---

# 9. Deferred：renderer coverage expansion

historical aggregate statement の一部は explicit type-name fallback。

```text
unknown statement
→ safe fallback
```

を維持し、readability pressure が確認された型から最小追加する。

---

# 10. Deferred：proof optimization

現時点で不要:

```text
general backtracking
producer ranking
proof-cost optimization
best-proof selection
persistent proof cache
global proof optimization
```

---

# 11. Deferred：mathematical scope expansion

将来候補:

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
symbolic stable-range specialization
ordinary all-primary π_{n+k}(S^n)
```

---

# 12. 文書体系

```text
README.md
→ concise current status

docs/design.md
→ current architecture

docs/roadmap.md
→ future plan

docs/development_log.md
→ history index

docs/development_log/
→ chronological archives

docs/proof_records.md
→ proof-record index

docs/proof_records/
→ mathematical / infrastructure archives
```

---

# 13. Completion policy

各 Phase:

```text
focused pytest
related regression
repository-wide pytest
git diff --check
```

実装前:

```text
current GitHub code
related tests
actual theorem-backed need
```

を確認する。

---

# 14. 直近の次作業

Phase 96 は正式 COMPLETE。

次:

```text
Phase 97-1
current calculation-to-report orchestration boundary audit
```
