# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

production calculation:

```text
raw n,k
→ python main.py n k
  または build_standard_toda_report()
→ standard production repository
→ proof report
```

generator exploration:

```text
generator string
→ top-level / recursive proof-scope exploration
→ Toda membership / 既知 map relation
→ applicable theorem / lemma candidates
→ relevance 分類済み presentation
```

standard production-qualified execution:

```text
standard applicability result
↓
qualified candidate filtering
↓
execution-family grouping
↓
explicit root_entry + source_step selection
↓
family representative
↓
production execution orchestration
↓
actual ProofStep
```

最新確認:

```text
Phase 105-17 focused:
8 passed in 142.33s

Phase 105-7 / 10 / 14 / 16 / 17 related:
40 passed in 174.89s

repository-wide Phase 105 closure:
8709 passed in 659.02s
```

Phase 105 は COMPLETE。

---

# 2. 完了済み capability

Phase 90–98:

```text
query
group normalization
EHP / exactness provenance
flat / recursive proof provenance
calculation orchestration
structured presentation
readable full proof report
raw n,k facade
```

Phase 99–104:

```text
structural generator containment
repository occurrence lookup
semantic roles
generator exploration
standard production repository
calculation CLI
production generator-input handling
recursive proof-scope exploration
Toda membership / known map relation discovery
applicability discovery
relevance classification
candidate handoff
READY validation
explicit-final-rule bounded search
prebuilt-report execution
actual ProofStep provenance
```

Phase 105:

```text
production execution-safety pressure audit
exact source-step execution seed
first qualified production execution entry
candidate execution orchestration
qualified NONE / UNIQUE / AMBIGUOUS representation
execution-family clone audit
execution-family grouping
root/source disambiguation audit
explicit root + source family selection
standard applicability-to-execution facade
repository-wide closure regression
```

---

# 3. 現在の user-facing API

calculation:

```text
build_toda_report(repository, n, k)
build_standard_toda_report(n, k)
python main.py n k
```

generator exploration:

```text
explore_repository_generator(repository, generator)
explore_standard_repository_generator_input(generator_input)
python main.py explore "nu'"
```

recursive proof-scope exploration:

```text
explore_repository_generator_proof_scope(repository, generator)
explore_standard_repository_generator_proof_scope_input(generator_input)
python main.py explore-proof nu_prime
```

applicability exploration:

```text
explore_standard_repository_generator_applicability_input(generator_input)
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

qualified execution facade:

```text
execute_standard_repository_generator_applicability_result_by_root_and_source(
  applicability_result,
  root_entry,
  source_step,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

qualified execution は現在 Python infrastructure capability であり、新しい CLI はない。

---

# 4. Phase 105 で確定した境界

```text
relevance
!=
execution qualification
```

standard `nu_prime` applicability:

```text
qualified raw candidates = 744
execution-family groups = 248
unique source-step identities = 124
```

同一 source 上の3つの qualified candidate は、factory / rule signature / entry metadata が同じだが、rule identity / catalog-entry identity が異なる。

したがって:

```text
raw applicability catalog
→ 保持

execution selection layer
→ family grouping
```

とする。

さらに:

```text
root only
→ 一意ではない

source_step only
→ 一意ではない

shortest_depth
→ selection policy にしない

root_entry identity + source_step identity
→ 248 group すべてで一意
```

Phase 105 はこの explicit selection を production facade に接続した。

---

# 5. 次 Phase の開始境界

Phase 105 は first qualified production rule family の end-to-end integration まで完了した。

次 Phase では、機能を無条件に一般化せず、まず **どの拡張圧力が実際に必要か** を監査する。

自然な開始点:

```text
Phase 106-1
post-Phase105 qualified-execution expansion pressure audit
```

監査候補:

```text
1. qualified production rule family を
   1 family から複数 family へ広げる必要があるか

2. explicit root/source selection を
   user-facing workflow からどう指定するか

3. goal を呼び出し側が与える現在の境界を
   維持すべきか、goal discovery が必要か

4. execution CLI が本当に必要か

5. execution result を calculation / exploration presentation に
   接続する実需要があるか
```

Phase 106-1 では実装を先取りせず、actual pressure を確認してから最小境界を決める。

---

# 6. Deferred：複数 production rule family の qualification

現在 production-qualified な family は

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

のみである。

今後 family を増やす場合は、各 family ごとに

```text
actual production source
execution safety
goal compatibility
required seed context
rule identity preservation
producer-search behavior
```

を確認する。

relevance category を qualification の根拠にしない。

---

# 7. Deferred：goal discovery

現在の production execution facade は `goal` を明示入力とする。

未実装:

```text
source candidate から goal を自動推定
unknown RHS を含む target search
複数 goal 候補の ranking
```

---

# 8. Deferred：数学的 evaluator

未実装:

```text
general Toda-bracket solver
bracket value computation
indeterminacy / coset normalization
general composition evaluation
general E(x) / H(x) / Δ(x) evaluation
```

既知 relation / membership の探索とは分離する。

---

# 9. Deferred：proof optimization

```text
general backtracking
theorem ranking
producer ranking
proof-cost optimization
best-proof selection
persistent proof cache
```

actual pressure が出るまで deferred とする。

---

# 10. Deferred：repository versioning

未実装:

```text
repository version token
repository snapshot
STALE_SEARCH_REPORT
REPOSITORY_CHANGED
cross-session execution-plan persistence
```

---

# 11. Deferred：user interface

将来候補:

```text
qualified execution workflow の user-facing orchestration
execution CLI
Web UI
structured export
interactive proof graph
filterable exploration UI
```

---

# 12. Deferred：mathematical scope

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
all-primary ordinary sphere-homotopy calculation
```

---

# 13. 直近の次作業

```text
Phase 106-1
post-Phase105 qualified-execution expansion pressure audit
```

目的は Phase 105 の first-family integration をそのまま一般化することではなく、

```text
複数 family qualification
user-facing root/source selection
goal discovery
execution CLI
result presentation integration
```

のどれが次に本当に必要かを監査し、最小の Phase 106 境界を決めることである。
