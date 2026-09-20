# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

production calculation:

```text
raw n,k
→ python main.py n k
  or build_standard_toda_report()
→ standard production repository
→ proof report
```

generator exploration:

```text
generator string
→ top-level / recursive proof-scope exploration
→ Toda memberships / known map relations
→ applicable theorem / lemma candidates
→ relevance-classified presentation
```

safe candidate consumption:

```text
selected applicability candidate
↓
explicit handoff
↓
execution-catalog validation
↓
READY
↓
explicit-final-rule bounded search
↓
prebuilt search report
↓
selected-path execution
↓
actual ProofStep provenance
```

最新確認:

```text
Phase 104-4M focused:
32 passed in 8.26s

repository-wide after Phase 104-4M:
8641 passed in 381.78s

Phase 104-4O focused:
9 passed in 1.63s

repository-wide after Phase 104-4P closure check:
8644 passed in 374.63s

Phase 104-4P:
PASS — no residual production implementation required
```

Phase 104 は COMPLETE。

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

Phase 99:

```text
structural generator containment
repository occurrence lookup
semantic roles
element exploration
grouped Markdown
repository-explicit one-shot facade
```

Phase 100:

```text
standard production repository
repository-free calculation facade
minimal calculation CLI
production calculation closure
```

Phase 101:

```text
production generator-input audit
production top-level exploration facade
aggregate occurrence presentation bridge
main.py explore dispatch
alias / indexed / zero / invalid validation
deterministic structural occurrence semantics
repository non-mutation
CLI boundary regression
legacy n,k compatibility
```

Phase 102:

```text
theorem-pattern exploration
Toda membership filtering
known map-relation exploration
recursive proof-scope traversal
ancestry semantic exploration
production proof-scope facade
main.py explore-proof
end-to-end validation
```

Phase 103:

```text
applicability candidate representation
indexed premise-pattern compatibility search
proof-scope applicability integration
production applicability facade
rule-group / rule-family presentation
compact / detailed renderer
main.py explore-applicable
RuleRelevanceCategory metadata
production relevance classification
final closure audit
```

Phase 104:

```text
candidate filtering / reduction
source-scoped candidate selection
rule-family selection
candidate handoff representation
execution-catalog validation
READY boundary
explicit-final-rule bounded search
READY search-report adapter
prebuilt-search-report shared execution core
READY execution adapter
report identity preservation
selected producer-path preservation
final-rule identity preservation
actual ProofStep provenance
end-to-end provenance regression
closure audit
```

---

# 3. 現在の user-facing APIs

calculation:

```text
build_toda_report(repository, n, k)
build_standard_toda_report(n, k)
python main.py n k
```

top-level generator exploration:

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

Phase 104 の handoff / execution path は現在 Python infrastructure capability であり、新しい CLI は追加していない。

---

# 4. Phase 104 で確定した境界

次を分離する。

```text
applicability candidate != proof success
relevance category != theorem ranking
candidate filtering != theorem ranking
candidate selection != proof success
candidate handoff != automatic proof execution
```

READY validation は:

```text
selected rule identity
execution catalog membership
fixed-point-safe metadata
goal compatibility
```

のみを確認する。

bounded search が確定した後、execution は:

```text
same report
same producer_nodes
same final_rule
```

を消費し、search を再実行しない。

最重要 identity:

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

および:

```text
execution_result.report
is search_report.report
```

---

# 5. 次の自然な候補

Phase 104 で applicability candidate の安全な bounded execution まで closure した。

次は、この capability をさらに広げる前に**実際の production workflow で次に不足しているものを監査する**。

自然な開始点:

```text
Phase 105-1
post-handoff production workflow / next-capability pressure audit
```

監査候補:

```text
Phase 104 handoff/execution capability を
どの production workflow から実際に利用するか

derived-but-not-explicit result discovery への圧力があるか

user-facing orchestration が本当に必要か

execution result を既存 calculation / exploration result と
どこまで統合すべきか
```

Phase 105-1 では先に実装せず、actual pressure を確認する。

---

# 6. Deferred：derived-but-not-explicit result discovery

Phase 102 は actual proof ancestry に既に存在する `ProofStep` discovery。

Phase 103 はそこから applicable candidate discovery。

Phase 104 は明示的に選択された candidate の bounded execution。

今後は必要性が確認された場合のみ:

```text
already represented but not root-visible
```

と

```text
not yet derived but derivable through validated bounded execution
```

を明確に分離した production workflow を検討する。

---

# 7. Deferred：Toda bracket evaluation

Phase 102 で membership discovery は実装済み。

未実装:

```text
bracket value computation
general bracket solver
indeterminacy computation
coset normalization
```

existing theorem-specific bracket statements を general solver とみなさない。

---

# 8. Deferred：map evaluation

Phase 102 で known relation discovery は実装済み。

未実装:

```text
E(x) の一般評価
H(x) の一般評価
Δ(x) の一般評価
unknown map-image inference
```

既知 `Relation(MapApplication(...), ...)` の検索とは分離する。

---

# 9. Deferred：coset / indeterminacy

```text
subgroup representation
coset representative
modulo relation
indeterminacy subgroup
normalization
```

は actual mathematical pressure が出てから設計する。

---

# 10. Deferred：composition evaluation

known composition relation lookup から開始し、general composition calculator を先取りしない。

---

# 11. Deferred：symbolic higher-range instantiation

$$
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
\qquad
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\},
\qquad
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\}
$$

の concrete specialization は別 capability。

---

# 12. Deferred：proof optimization

```text
general backtracking
theorem ranking
producer ranking
proof-cost optimization
best-proof selection
persistent proof cache
```

actual pressure が出るまで deferred。

---

# 13. Deferred：repository versioning

Phase 104 の prebuilt search-report execution は、同じ workflow 内で report をそのまま消費するところまで。

未実装:

```text
repository version token
repository snapshot
STALE_SEARCH_REPORT
REPOSITORY_CHANGED
cross-session execution-plan persistence
```

これらは actual concurrency / persistence pressure が出てから扱う。

---

# 14. Deferred：user interfaces

実装済み:

```text
minimal calculation CLI
minimal top-level generator-exploration CLI
minimal recursive proof-scope CLI
applicability exploration CLI
```

将来候補:

```text
Phase 104 execution workflow の user-facing orchestration
Web UI
structured export
interactive proof graph
filterable exploration UI
```

user-facing execution は Phase 105-1 監査で必要性を確認するまで実装しない。

---

# 15. Deferred：mathematical scope

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
all-primary ordinary sphere-homotopy calculation
```

---

# 16. 直近の次作業

Phase 104 は COMPLETE。

次候補:

```text
Phase 105-1
post-handoff production workflow / next-capability pressure audit
```

目的は、Phase 104 で完成した

```text
selected candidate
→ READY
→ bounded search
→ actual execution
```

を無条件に user-facing 化することではなく、次に本当に必要な production capability を監査して最小境界を決めることである。
