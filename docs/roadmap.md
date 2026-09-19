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
→ readable proof narrative
→ unified full proof report
```

top-level reporting / convenience:

```text
raw n,k
→ build_toda_report()
→ TodaGroupQuery
→ calculation
→ candidate handling
→ presentation
→ report
→ TodaCalculationReportResult
→ report / reports access
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
7643 passed in 123.73s
```

---

# 2. 完了済み capability

Phase 90–98:

```text
query target construction
theorem-backed known-result lookup
normalized group structure / generators / orders
actual EHP extraction
exactness-use provenance
flat / recursive proof provenance
aggregate theorem branch discovery
original branch ProofStep recovery
direct-result precedence
multiple-result preservation
calculation orchestration
structured presentation
proof source presentation
dependency-first proof flow
LaTeX / Markdown rendering
readable narrative
unified full proof report
calculation-report representation
single FOUND calculation-to-report API
NOT_FOUND / FOUND / MULTIPLE_RESULTS top-level handling
representative six-target top-level validation
raw n,k user-facing facade
FOUND-only result.report
ordered result.reports
representative shortest-path validation
```

Phase 98 は正式 COMPLETE。

---

# 3. 現在の user-facing API

最短経路:

```text
build_toda_report(
  repository,
  n,
  k,
)
```

output:

```text
TodaCalculationReportResult
```

single `FOUND`:

```text
result.report
```

全 candidate report:

```text
result.reports
```

status semantics:

```text
NOT_FOUND
→ reports == ()
→ report は ValueError

FOUND
→ report 使用可能
→ reports == (report,)

MULTIPLE_RESULTS
→ reports は全 candidate report
→ report は ValueError
```

multiple candidate の ranking / best selection はしない。

---

# 4. Phase 98 で守った境界

再実装しなかったもの:

```text
query validation
group lookup semantics
aggregate branch discovery
proof recovery
group normalization
EHP extraction
dependency extraction
presentation model
mathematical renderer
narrative renderer
candidate ranking
```

追加しなかったもの:

```text
new facade class
NOT_FOUND fixed message
silent first-candidate selection
new proof or calculation logic
```

direct / aggregate provenance、candidate identity/order、repository non-mutation を保持。

---

# 5. 次 Phase の選定方針

Phase 98 で convenience pressure は一度解消した。

次は speculative convenience を増やさず、actual usage pressure から主題を選ぶ。

有力候補:

```text
A. CLI / Web UI boundary audit
B. symbolic exploration / query capability audit
C. element-centered search audit
D. mathematical scope expansion audit
```

特に user-facing exploration の候補:

```text
指定した元を含む Toda bracket の検索
nu' in {a,b,c} 型 containment query
coset / indeterminacy の表示・計算
写像による元の行き先検索
補題・命題を適用できる元の検索
本に明示されていない導出済み結果の列挙
```

次 Phase はこれらを一度に実装せず、最初に current representation / actual need audit を行う。

---

# 6. Deferred：symbolic higher-range instantiation

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\qquad
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
\qquad
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
\]

の concrete specialization は別 capability とする。

---

# 7. Deferred：target-only proof-search fallback

query は target group だけを持ち、unknown RHS theorem goal は生成しない。

---

# 8. Deferred：calculation failure diagnostics

現在:

```text
NOT_FOUND
FOUND
MULTIPLE_RESULTS
```

のみ。細分類は actual need が確認された場合に検討する。

core model の fixed human-readable `NOT_FOUND` message も deferred。

---

# 9. Deferred：renderer coverage expansion

historical aggregate statement の一部は explicit type-name fallback。

readability pressure が確認された型から最小追加する。

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

# 11. Deferred：user interfaces

将来候補:

```text
CLI
Web UI
structured export
interactive proof graph
```

UI の都合で proof truth / provenance schema を変更しない。

---

# 12. Deferred：mathematical scope expansion

将来候補:

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
symbolic stable-range specialization
ordinary all-primary π_{n+k}(S^n)
```

---

# 13. 文書体系

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

# 14. Completion policy

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

# 15. 直近の次作業

Phase 98 は正式 COMPLETE。

次の Phase は user-facing convenience の追加ではなく、actual usage pressure を監査して選定する。

有力な最初の監査候補:

```text
Phase 99-1
current exploration / query capability pressure audit
```

確認候補:

```text
element-centered search
Toda bracket containment
map-image lookup
applicable lemma discovery
coset / indeterminacy representation
derived-result enumeration
```

CLI / Web UI を先に進める場合も、まず boundary audit から開始する。
