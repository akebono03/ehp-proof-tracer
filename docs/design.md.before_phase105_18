# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、invariant、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・proof-search 上の必要
↓
不足している最小表現
↓
必要な domain rule / orchestration
↓
既存 generic infrastructure
```

次を混同しない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
catalog metadata != proof truth
search plan != proof result
calculation result != proof truth
presentation != proof truth
rendered prose != proof truth
production repository assembly != theorem truth
CLI != proof truth
exploration result != new theorem truth
generator input resolution != mathematical equality
proof-scope traversal != theorem search
known relation discovery != map evaluation
Toda membership discovery != bracket solving
applicability candidate != successful proof
relevance category != theorem ranking
candidate selection != proof success
handoff validation != theorem truth
bounded search result != executed proof
```

---

# 2. 現在のレイヤー構造

計算経路:

```text
expression / statement representation
↓
generic proof / inference mechanics
↓
Toda-specific theorem knowledge
↓
Proof Repository / rule catalog
↓
bounded proof search
↓
Toda group query / lookup
↓
calculation-goal discovery / recovery / normalization
↓
group result
↓
EHP / exactness provenance
↓
flat / recursive proof provenance
↓
structured presentation
↓
human-readable proof report
↓
repository-explicit facade
↓
standard production repository
↓
minimal calculation CLI
```

generator exploration / applicability 経路:

```text
generator string
↓
resolve_generator_input()
↓
GeneratorSymbol
↓
standard production repository
↓
registered conclusion / recursive ProofStep ancestry
↓
structural occurrences
↓
Toda memberships / known map relations
↓
premise-pattern compatibility
↓
applicability candidates
↓
rule groups / rule families
↓
relevance-classified presentation
```

Phase 104 bounded handoff / execution 経路:

```text
selected applicability candidate
↓
RepositoryGeneratorApplicabilityCandidateHandoff
↓
RepositoryGeneratorApplicabilityHandoffValidation
↓
READY + execution_entry
↓
explicit-final-rule bounded search
↓
RepositoryGeneratorApplicabilityHandoffSearchReport
↓
prebuilt BoundedProducerSearchReport
↓
selected producer_nodes / final_rule
↓
RepositoryGeneratorApplicabilityHandoffExecutionResult
↓
BoundedProducerExecutionResult
↓
RepositoryInferenceResult
↓
actual ProofStep provenance
```

---

# 3. 主要モジュール

基礎:

```text
expression.py
proof.py
proof_repository.py
rule_catalog.py
repository_inference.py
homotopy_groups.py
toda_rules.py
```

計算 / provenance:

```text
toda_group_query.py
toda_group_lookup.py
toda_group_result.py
toda_calculation_goal*.py
toda_calculation.py
toda_calculation_result.py
toda_ehp_*.py
toda_proof_dependency.py
toda_explanation.py
```

presentation / report:

```text
toda_presentation.py
toda_ehp_presentation.py
toda_proof_presentation.py
toda_proof_flow_presentation.py
toda_end_to_end_presentation.py
toda_human_readable_renderer.py
toda_proof_narrative_renderer.py
toda_full_proof_report_renderer.py
toda_calculation_report*.py
```

production calculation:

```text
standard_production_repository.py
toda_calculation_facade.py
main.py
```

top-level generator exploration:

```text
generator_input.py
structural_containment.py
repository_element_lookup.py
generator_occurrence_roles.py
repository_element_exploration.py
repository_element_presentation.py
repository_element_renderer.py
repository_element_facade.py
```

recursive proof-scope / applicability:

```text
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_renderer.py
repository_proof_scope_applicability.py
```

Phase 104 handoff / bounded execution:

```text
repository_generator_applicability_handoff.py
repository_inference.py
```

---

# 4. Toda group query

`TodaGroupQuery(n, k)` は

$$
\pi_{n+k}^n
$$

を query する。

valid domain:

```text
n > 0
k >= 0
```

---

# 5. Proof truth と metadata

proof truth の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata。

presentation、renderer、facade、production repository、CLI、exploration、resolver、proof-scope traversal、applicability classification は proof truth を追加してはならない。

---

# 6. Repository read-only invariant

query / calculation / reporting / exploration / applicability discovery / bounded execution planning は repository を read-only に扱う。

execution は inference result を構成するが、元の `ProofRepository` 自体を mutate しない。

```text
repository entries before == repository entries after
```

必要な箇所では `ProofStep` identity も保持する。

---

# 7. Calculation result semantics

```text
0 candidates  → NOT_FOUND
1 candidate   → FOUND
2+ candidates → MULTIPLE_RESULTS
```

multiple candidate を自動 ranking / selection しない。

---

# 8. EHP / exactness provenance

truth source は final theorem-backed `ProofStep` から reachable な ancestry。

代表:

$$
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
$$

---

# 9. Production calculation facade

repository-explicit:

```text
build_toda_report(repository, n, k)
```

production:

```text
build_standard_toda_report(n, k)
```

production path は既存 repository-explicit path を compose し、計算 logic を複製しない。

---

# 10. Generator input semantics

`resolve_generator_input()` は explicit user input を exact `GeneratorSymbol` へ変換する。

代表 alias:

```text
η / eta
ν / nu
σ / sigma
ι / iota

ν′ / ν' / nu' / nu_prime
σ' / sigma_prime
σ'' / sigma_double_prime
σ''' / sigma_triple_prime
```

indexed:

```text
eta_2
nu_5
sigma_8
iota_4
```

重要:

```text
unindexed generator != wildcard
```

free-form typo correctionや数学的同値判定は行わない。

---

# 11. Top-level generator occurrence semantics

1 occurrence:

```text
entry
path
matched_generator
roles
```

重要 invariant:

```text
same entry + different structural path
= different occurrence
```

entry-level deduplication はしない。

順序:

```text
repository registration order
→ structural path order
```

---

# 12. Semantic roles

```text
RELATION_LHS
RELATION_RHS
GROUP_GENERATOR
COMPOSITION_LEFT
COMPOSITION_RIGHT
MAP_INPUT
TODA_BRACKET_FIRST
TODA_BRACKET_SECOND
TODA_BRACKET_THIRD
```

1 occurrence は複数 role を持ち得る。

grouped view は master occurrence order を保持する。

---

# 13. Proof-scope traversal semantics

`RepositoryProofScopeNode` は:

```text
root_entry
proof_step
shortest_depth
```

を持つ。

entry ごとに breadth-first traversal を行う。

invariant:

```text
depth 0
= root_entry.step

same ProofStep identity under one root
= one node at shortest depth

same ProofStep identity under different roots
= distinct provenance nodes

cycle
= safe termination

repository
= not mutated
```

synthetic `ProofRepositoryEntry` は作らない。

未登録 premise は未登録 premise のまま actual `ProofStep` identity を保持する。

---

# 14. Proof-scope generator occurrence semantics

proof-scope generator occurrence は top-level occurrence と異なり、登録 entry の conclusion ではなく ancestry node の

```text
scope_node.proof_step.conclusion
```

を検索する。

保持する情報:

```text
scope_node
path
matched_generator
roles
```

`scope_node.root_entry` により production root provenance を失わない。

---

# 15. Toda membership exploration

対象:

```text
TodaBracketMembershipStatement
TodaBracketMembershipTheoremStatement
```

次を区別する。

```text
generator appears as membership element
generator appears in bracket first
generator appears in bracket second
generator appears in bracket third
```

代表 production ancestry:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1.
$$

Toda membership discovery は bracket value の計算ではない。

---

# 16. Known map-relation exploration

対象は already represented な equality relation

```text
Relation(
  lhs=MapApplication(...),
  rhs=...,
  relation_type=EQUALITY,
)
```

かつ generator occurrence が

```text
RELATION_LHS
MAP_INPUT
```

を持つ場合。

代表:

$$
H(\nu')=\eta_5.
$$

これは既知 relation の discovery であり、一般 $E/H/\Delta$ evaluator ではない。

---

# 17. Proof-scope production facade

repository-explicit:

```text
explore_repository_generator_proof_scope(
  repository,
  generator,
)
```

production:

```text
explore_standard_repository_generator_proof_scope_input(
  generator_input,
)
```

structured result:

```text
generator
scope
occurrences
toda_memberships
map_relations
```

Toda membership / map relation の `source_occurrence` は master `occurrences` 内の occurrence identity を再利用する。

---

# 18. Applicability discovery semantics

Phase 103 の applicability candidate は概念的に:

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

を保持する。

重要な境界:

```text
premise compatibility != all premises satisfied
applicability candidate != rule execution
applicability candidate != proof success
applicability candidate != theorem truth
```

`RuleRelevanceCategory`:

```text
THEOREM_SPECIFIC
MAP_PROPERTY
STRUCTURAL
GENERIC_RELATION
BRIDGE
UNCLASSIFIED
```

category 順序は theorem ranking、proof strength、proof success probability ではない。

Phase 103 closure baseline:

```text
catalog entries = 1188
families = 267
classified families = 158
unclassified families = 109

STRUCTURAL = 201
MAP_PROPERTY = 60
THEOREM_SPECIFIC = 424
GENERIC_RELATION = 63
BRIDGE = 140
UNCLASSIFIED = 300
```

---

# 19. Phase 104 candidate selection boundary

Phase 104 は applicability presentation から直接 automatic execution を行わない。

candidate-set reduction / source-scoped selection は:

```text
candidate filtering
candidate-set reduction
source-scoped selection
rule-family selection
```

までを担う。

重要:

```text
candidate filtering != theorem ranking
candidate selection != proof success
selection order != proof quality
```

選択された candidate object の identity を後続 handoff に保持する。

---

# 20. Phase 104 handoff representation

`RepositoryGeneratorApplicabilityCandidateHandoff` は最小に:

```text
candidate
goal
```

を保持する。

handoff は candidate の copy や rule の再構成を行わない。

```text
handoff.candidate is selected candidate
```

が provenance の起点になる。

---

# 21. READY validation semantics

`RepositoryGeneratorApplicabilityHandoffValidation` は execution catalog に対して selected rule を確認する。

status:

```text
READY
RULE_NOT_IN_EXECUTION_CATALOG
RULE_NOT_FIXED_POINT_SAFE
GOAL_INCOMPATIBLE
```

`READY` のみ `execution_entry` を持つ。

validation は identity ベースで selected rule と execution entry を接続する。

```text
handoff.candidate.candidate.inference_rule
is validation.execution_entry.rule
```

意味:

```text
candidate discovery
!=
execution safety validation
```

execution catalog は theorem truth を生成しない。

---

# 22. Explicit-final-rule bounded search

Phase 104 の bounded search は READY validation で確定した final rule を再選択しない。

概念的な入口:

```text
_build_bounded_producer_search_report_for_final_rule(
  repository,
  rule_catalog,
  goal,
  final_rule,
  ...
)
```

ここでは final rule は authoritative input。

producer search、`max_depth`、retry policy は search-time concern である。

search report が `SUCCESS` なら:

```text
search_result.final_rule
is validation.execution_entry.rule
```

を handoff wrapper が保証する。

---

# 23. Prebuilt-search-report execution

Phase 104-4M では bounded execution loop を prebuilt report 入力で共有可能にした。

internal execution core:

```text
repository
+
BoundedProducerSearchReport
↓
execution
```

execution core は次を受け取らない。

```text
rule_catalog
execution_catalog
max_depth
retry_policy
goal-selection policy
```

これらは search 時点までで消費済みである。

legacy `execute_depth_two_producer_search()` は従来 signature を維持し、

```text
build report
↓
shared report execution core
```

へ委譲する。

Phase 104 handoff path は 4K で作成した report を直接 shared core に渡す。

---

# 24. Search-report identity invariant

Phase 104 execution wrapper の最重要 invariant:

```text
execution_result.report
is search_report.report
```

`==` ではなく `is` を要求する。

これは「同じ内容の report」ではなく、

```text
4K で作ったその report object を
再探索せず execution が消費した
```

ことを表す。

`SUCCESS` の場合、同じ `BoundedProducerSearchResult` 内の:

```text
producer_nodes
final_rule
```

が authoritative execution plan になる。

---

# 25. Actual ProofStep provenance

`apply_inference_match()` は実行した `InferenceRule` object をそのまま:

```text
ProofStep.inference_rule
```

へ格納する。

したがって Phase 104-4O で固定した final-rule identity chain は:

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

である。

selected producer についても:

```text
producer_node.producer_rule
is executed_producer_step.inference_rule
```

が成立する。

代表 premise chain:

```text
source_step
→ producer_step
→ goal_step
```

も actual `ProofStep.premises` で保持される。

---

# 26. GOAL_ALREADY_AVAILABLE semantics

READY validation 後、search 時点で goal が repository に既に存在する場合:

```text
status = GOAL_ALREADY_AVAILABLE
search_result = None
```

execution は producer rule / final rule を実行しない。

ただし wrapper は:

```text
candidate
handoff
validation
search report
```

の provenance を保持する。

意味は:

```text
selected candidate は READY まで validation された
しかし goal は既存だったため rule execution は不要だった
```

である。

---

# 27. Failure report semantics

search report が:

```text
NO_PRODUCER
UNSAFE_PRODUCER
AMBIGUOUS_PRODUCER
PRODUCER_RETRY_EXHAUSTED
CYCLE_DETECTED
DEPTH_LIMIT
PRODUCER_NOT_APPLICABLE
PRODUCER_OUTPUT_NOT_USABLE
FINAL_RULE_NOT_APPLICABLE
GOAL_NOT_DERIVED
```

等なら、execution adapter は再探索しない。

```text
search failure
→ same failure report preserved
→ no execution result proof
```

execution diagnostic も search report 成功判定後に再実行しない。

---

# 28. Repository drift boundary

Phase 104 は repository snapshot/versioning を導入しない。

未実装:

```text
STALE_SEARCH_REPORT
REPOSITORY_CHANGED
repository version token
snapshot hash
```

Phase 104 の責務は:

```text
同じ repository workflow 内で
確定済み report をそのまま execution する
```

ことまで。

repository drift 検知は actual pressure が出た場合の将来 capability とする。

---

# 29. CLI boundary

calculation:

```text
python main.py 5 7
```

top-level exploration:

```text
python main.py explore "nu'"
```

recursive proof-scope exploration:

```text
python main.py explore-proof nu_prime
```

applicability exploration:

```text
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

Phase 104 は新しい CLI を追加しない。

---

# 30. 現在の未実装境界

```text
free-form natural-language search
wildcard family search
general composition evaluation
general Toda-bracket solving
bracket-value computation
general coset / indeterminacy computation
general E / H / Δ evaluation
recursive theorem solving beyond represented ancestry
automatic enumeration of unstated consequences
symbolic higher-range auto-instantiation
general theorem ranking
producer ranking
proof-cost optimization
best-proof selection
general unbounded backtracking
persistent proof cache
repository snapshot/versioning
stale-search-report detection
Web UI
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
```

---

# 31. 文書 TeX 方針

GitHub Markdown では数式に:

```text
inline:  $...$
display: $$...$$
```

を使用する。

`\(...\)` / `\[...\]` を標準表示方法として前提にしない。

コードや CLI は backtick / code block、数式は数式 delimiter を使う。

---

# 32. Completion baseline

Phase 103:

```text
PHASE103_7_CLOSURE_AUDIT = PASS

Phase 103 regression:
54 test files
409 passed in 186.07s
```

Phase 104:

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
