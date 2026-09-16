# EHP Proof Tracer コードリファレンス

この文書は EHP Proof Tracer の主要 module と、その責務・主要 class / function・探索方法をまとめる。

対象は **Phase 88 completion 時点**。

全 API の機械的列挙ではなく、次の探索を速くするための索引である。

```text
新しい Phase の必要数学 / proof-search need
↓
どの module を確認すべきか
↓
既存 class / function / rule の再利用候補
↓
最小変更
```

実装・監査前には必ず現在のコードと関連 test を確認する。

---

# 1. module 境界

```text
expression.py
  数学式の structural representation

proof.py
  generic proof / inference mechanics

proof_repository.py
  in-memory ProofStep catalog

rule_catalog.py
  rule registration / search metadata

repository_inference.py
  repository-assisted inference
  missing-premise analysis
  bounded producer search
  diagnostics / report
  retry
  selected-path execution

relation_rules.py
  generic relation propagation

scalar_rules.py
  scalar parity / congruence / inequalities

homotopy_groups.py
  ordinary / Toda group and map structures

low_dimensional_facts.py
  foundational concrete facts

toda_rules.py
  Toda-specific theorem statements / inference rules

probes/
  representative capability demonstrations

tests/
  generic and Phase-specific regression
```

---

# 2. proof.py

主要 structure:

```text
ProofRule
ProofStep
PremisePattern
PatternVariable
VariableBinding
InferenceRule
InferenceMatch
InferenceRunResult
```

`ProofStep`:

```text
conclusion
premises
rule
note
inference_rule
```

provenance の authoritative object。

主要 matching / execution:

```text
match_statement_pattern()
match_premise_pattern()
merge_variable_bindings()
substitute_statement_pattern()
find_inference_match()
find_inference_matches()
apply_inference_match()
derive_inference_round_result()
run_inference_until_stable_with_history()
find_goal_step()
```

重要 boundary:

```text
match_guard
```

は premise bindings に依存し得るため、Phase 88 の early goal compatibility hook と同一視しない。

---

# 3. proof_repository.py

主要 class:

```text
ProofRepositoryEntry
ProofRepository
```

API:

```text
register()
get()
entries()
find_by_conclusion()
find_by_statement_type()
find_by_phase()
find_by_theorem()
dependencies()
```

責務:

```text
existing ProofStep catalog / lookup
```

非責務:

```text
proof construction
inference
persistent storage
```

---

# 4. rule_catalog.py

主要 class:

```text
InferenceRuleCatalogEntry
InferenceRuleCatalog
```

Phase 88 completion 時点の entry metadata:

```text
key
rule
conclusion_type
fixed_point_safe
goal_compatibility
```

`goal_compatibility`:

```text
None
or
callable(goal) -> bool
```

主要 final-goal lookup:

```text
find_goal_compatible_rule_entries()
find_goal_compatible_rules()
```

producer lookup:

```text
find_premise_producer_candidate_entries(
  catalog,
  premise_pattern,
  requested_statement=None,
)

find_premise_producer_rule_entries(
  catalog,
  premise_pattern,
  requested_statement=None,
)

find_premise_producer_rules(
  catalog,
  premise_pattern,
  requested_statement=None,
)
```

Phase 88 semantics:

```text
requested_statement is None
→ legacy type-only lookup

requested_statement is concrete
→ conclusion type
  + goal_compatibility(requested_statement)
```

safe rule lookup はさらに `fixed_point_safe=True` を要求する。

registration order と rule identity dedup は維持する。

---

# 5. repository_inference.py — repository bridge

主要 basic API:

```text
RepositoryInferenceResult
repository_available_steps()
derive_goal_from_repository()
derive_goal_from_repository_with_catalog()
```

`repository_available_steps()`:

```text
same ProofStep aliases
→ identity deduplicate

different ProofStep objects with equal conclusion
→ preserve
```

repository は mutation しない。

---

# 6. repository_inference.py — premise analysis

主要 class:

```text
PremiseAvailability
MissingPremiseProducerLookup
```

Phase 88 completion fields:

```text
PremiseAvailability
  inference_rule
  matched_steps
  missing_indices
  bindings

MissingPremiseProducerLookup
  inference_rule
  premise_index
  premise_pattern
  producer_rules
  requested_statement
```

主要 function:

```text
detect_missing_premises()
find_missing_premise_producer_lookups()
analyze_producer_premise_availabilities()
all_missing_premises_uniquely_producible()
```

Phase 88 helper responsibility:

```text
all PatternVariable bound?
→ yes: concrete requested_statement
→ no: requested_statement=None
```

unbound variable を `None` へ誤置換しない。

---

# 7. repository_inference.py — bounded search representation

主要 class:

```text
BoundedProducerSearchNode
BoundedProducerSearchResult
FiniteProducerRetryPolicy
```

`BoundedProducerSearchNode` は現在:

```text
requesting_rule
premise_index
premise_pattern
producer_rule
producer_availability
depths
requested_statement
dependencies
```

を保持する。

`requested_statement=None` が backward-compatible default。

shared producer は複数 depth を:

```text
depths=(...)
```

で保持する。

---

# 8. repository_inference.py — diagnostics / report

主要 enum / class:

```text
BoundedProducerSearchStatus
BoundedProducerSearchDiagnostic
BoundedProducerSearchReport
BoundedProducerExecutionResult
```

search diagnostic:

```text
diagnose_direct_producer_failure()
diagnose_depth_two_producer_search_failure()
```

execution diagnostic:

```text
diagnose_depth_two_producer_execution_failure()
```

report:

```text
build_depth_two_producer_search_report()
```

Phase 88-13 以降、unsafe candidate lookup も:

```text
lookup.requested_statement
```

を使用する。

Phase 88-15 以降、execution output は concrete request がある場合:

```text
step.conclusion == node.requested_statement
```

を要求する。

---

# 9. repository_inference.py — selection / execution

selection:

```text
select_unique_depth_two_producer_chain()
```

existing API name は historical compatibility のため維持。

現在は:

```text
max_depth >= 2
```

の bounded selection を扱い、正式 regression は2/3/4。

retry:

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

execution:

```text
execute_depth_two_producer_search()
```

重要 invariant:

```text
report.search_result
=
actually executed search_result
```

選択後に別 search をやり直さない。

---

# 10. Phase 88 concrete-goal path

探索するときの主要 call chain:

```text
detect_missing_premises()
↓
PremiseAvailability.bindings
↓
find_missing_premise_producer_lookups()
↓
MissingPremiseProducerLookup.requested_statement
↓
find_premise_producer_rules(..., requested_statement=...)
↓
select_unique_depth_two_producer_chain()
↓
BoundedProducerSearchNode.requested_statement
↓
build_depth_two_producer_search_report()
↓
diagnose_depth_two_producer_execution_failure()
↓
execute_depth_two_producer_search()
```

false ambiguity の調査ではこの順に見る。

---

# 11. Phase 88 realistic collision rules

same conclusion type の代表:

```text
TodaDeltaImageUpToSignStatement
```

実在 rule:

```text
Phase 52
toda_delta_iota5_two_eta2_up_to_sign_inference_rule()

Phase 66
toda_58_delta_iota9_nu4_nu_prime_inference_rule()

Phase 76
toda_516_delta_iota17_generator_inference_rule()
```

Phase 88 end-to-end regression はこの collision を使用する。

---

# 12. Phase 88 tests

主要 test:

```text
tests/test_phase88_realistic_catalog_collision_observability.py
tests/test_phase88_goal_side_compatibility.py
tests/test_phase88_concrete_missing_premise_representation.py
tests/test_phase88_producer_goal_compatibility_filtering.py
tests/test_phase88_unsafe_producer_diagnostic_compatibility.py
tests/test_phase88_selected_node_concrete_execution_validation.py
tests/test_phase88_concrete_goal_end_to_end.py
```

役割:

```text
collision observability
goal-side compatibility
binding preservation
concrete producer filtering
unsafe diagnostic consistency
selected-node concrete provenance
execution concrete validation
end-to-end success
```

---

# 13. Phase 87 tests / retry boundary

代表:

```text
tests/test_phase87_selection_side_finite_retry.py
tests/test_phase87_retry_diagnostics_report.py
tests/test_phase87_selected_path_execution_retry_provenance.py
```

Phase 88 filtering 後も同一 concrete target に複数 producer が残る場合のみ Phase 87 retry semantics が relevant。

---

# 14. Phase 86 tests / bounded-depth boundary

正式 regression:

```text
max_depth=2
max_depth=3
max_depth=4
```

代表:

```text
tests/test_phase86_explicit_max_depth_parameterization.py
tests/test_phase86_depth_three_bounded_search.py
tests/test_phase86_depth_four_bounded_search.py
```

---

# 15. toda_rules.py

Toda theorem-specific semantics を保持する。

ここへ置くもの:

```text
Toda source statement の専用 consequence
concrete group / map / bracket relation
narrow theorem-specific transport
```

ここへ置かないもの:

```text
generic proof search policy
repository lookup
catalog ranking
generic equality mechanics
```

Phase 88 では Toda rule 本体を変更せず、既存 real rules の catalog metadata / search semantics を改善した。

---

# 16. expression.py / homotopy_groups.py

`expression.py`:

```text
HomotopyElement
GeneratorSymbol
Multiple
Sum
Composition
Suspension
IteratedSuspension
TodaBracket
WhiteheadProduct
...
```

`homotopy_groups.py`:

```text
HomotopyGroup
TodaPrimaryGroup
StableHomotopyGroup
StablePrimaryComponent
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
...
```

structural object を global normalization で数学同値化しない。

---

# 17. probes/

代表:

```text
probe_phase78_capabilities
  stable G_0...G_7

probe_phase79_capabilities
  Proof Repository

probe_phase80_capabilities
  repository-assisted inference

probe_phase81_capabilities
  automatic rule selection

probe_phase82_capabilities
  one-level search

probe_phase83_capabilities
  multiple missing premises

probe_phase84_capabilities
  bounded depth=2

probe_phase85_capabilities
  diagnostics / integrated execution

probe_phase86_capabilities
  bounded depth parameterization

probe_phase87_capabilities
  finite retry
```

Phase 88 は dedicated production probe を追加せず、focused + end-to-end regression で固定している。

---

# 18. 現在の regression baseline

Phase 88-17 完了確認:

```text
end-to-end:
8 passed in 2.06s

Phase 88 related:
47 passed in 2.96s

search/retry/execution:
34 passed in 2.41s

repository-wide:
7096 passed in 35.90s

git diff --check:
clean
```

---

# 19. 新しい proof-search Phase の確認順

実装前:

```text
1. actual failure / need
2. current catalog candidates
3. missing premise binding state
4. concrete requested_statement の有無
5. safe / unsafe filtering
6. remaining true ambiguity
7. selected dependency DAG
8. execution provenance
9. existing tests
10. minimum change
```

general backtracking / ranking / cost / DFS / BFS / A* は concrete need が確認されるまで追加しない。
