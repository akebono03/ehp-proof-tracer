# EHP Proof Tracer 設計

この文書は現在のアーキテクチャ、意味論、設計境界を記録する。

過去の実装経緯は `docs/development_log.md`、将来構想は `docs/roadmap.md`、主要コードの探索は `docs/code_reference.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` に分離する。

---

# 1. 基本設計原則

```text
実際の数学的・proof-search 上の必要
↓
不足している最小表現
↓
必要な explicit fact / domain rule / orchestration
↓
既存 generic inference engine
```

数学固有の theorem knowledge を generic inference engine に埋め込まない。

```text
representation != typing != theorem knowledge
structural equality != mathematical equality
catalog metadata != proof truth
search plan != proof result
```

既存 API と既存 proof provenance を保ち、将来 Phase の一般化を先取りしない。

---

# 2. レイヤー分離

```text
文献由来 theorem / explicit facts
↓
domain-specific inference rules
↓
InferenceRuleCatalog
↓
repository-assisted bounded proof search
↓
ProofStep / InferenceRule
↓
expression / statement structures
↓
homotopy / EHP data
↓
abelian-group algebra
```

主要責務:

```text
expression.py
= 式の structural representation

proof.py
= generic proof / inference mechanics

proof_repository.py
= in-memory ProofStep catalog

rule_catalog.py
= rule registration and search metadata

repository_inference.py
= repository-assisted rule selection / bounded producer search / diagnostics / execution

relation_rules.py
= generic relation propagation

homotopy_groups.py
= homotopy / Toda group and map data

toda_rules.py
= Toda-specific theorem knowledge

probes/
= representative capability demonstrations

tests/
= semantic / regression / provenance verification
```

---

# 3. structural equality と mathematical equality

Python dataclass の equality は syntax tree の一致を表す。

```text
同じ syntax
→ structural equality
```

数学的に同値だが syntax が異なる場合は、必要な concrete theorem branch に限定して explicit relation / inference rule で接続する。

global normalization や一般 CAS 化は行わない。

---

# 4. ordinary homotopy group と Toda π_i^n

`HomotopyGroup(i,n)` は ordinary `π_i(S^n)` を表す。

`TodaPrimaryGroup(i,n)` は historical class name であり、Toda (4.3) の `π_i^n` を表す。

```text
i=n
  π_n^n = π_n(S^n)

i=2n-1
  π_(2n-1)^n = E^(-1)(π_(2n)(S^(n+1);2))

otherwise
  π_i^n = π_i(S^n;2)
```

したがって:

```text
HomotopyGroup
!= structurally
TodaPrimaryGroup
```

である。

---

# 5. generic inference engine

中心 object:

```text
Relation
ProofStep
PremisePattern
PatternVariable
VariableBinding
InferenceRule
InferenceMatch
InferenceRunResult
```

基本実行:

```text
available ProofStep
↓
premise matching
↓
variable bindings
↓
match_guard
↓
conclusion_builder / conclusion_pattern
↓
ProofRule.INFERENCE
↓
fixed-point or staged execution
```

provenance は:

```text
ProofStep.premises
ProofStep.inference_rule
```

に保持する。

---

# 6. Proof Repository

`ProofRepository` は既存 `ProofStep` の in-memory catalog である。

責務:

```text
registration
metadata
lookup
direct dependency access
```

責務ではない:

```text
proof construction
theorem truth
inference
graph rewriting
persistent storage
```

repository metadata は inference applicability を変更しない。

同一 `ProofStep` alias は repository-to-available-steps bridge で identity deduplicate する一方、同じ conclusion を持つ別 `ProofStep` は別 proof として保持する。

---

# 7. InferenceRuleCatalog

`InferenceRuleCatalogEntry` は rule search 用 metadata を保持する。

現在の主要 field:

```text
key
rule
conclusion_type
fixed_point_safe
goal_compatibility
```

`fixed_point_safe` は automatic search / execution への opt-in 境界。

`goal_compatibility` は Phase 88 で追加した concrete theorem-instance compatibility hook である。

contract:

```text
goal_compatibility is None
or
callable(goal) -> bool
```

`None` は従来の type-only behavior を保持する。

final-goal lookup:

```text
catalog entries
↓
fixed_point_safe
↓
exact conclusion_type
↓
goal_compatibility(goal), if present
↓
goal-compatible rule entries
```

`match_guard` は一般に premise bindings に依存するため、missing premise を生成する前の goal-side filter として代用しない。

---

# 8. Phase 80–84 proof-search progression

```text
Phase 80
repository + explicit rules
→ forward inference

Phase 81
goal
→ automatic final-rule selection

Phase 82
one missing premise
→ one-level producer generation

Phase 83
multiple missing premises
→ multiple one-level producers

Phase 84
bounded depth=2 producer dependency DAG
→ dependency-first execution
```

shared producer は logical rule identity で再利用し、複数 path depth を保持する。

---

# 9. Phase 85 diagnostics / report / execution

status family:

```text
SUCCESS
GOAL_ALREADY_AVAILABLE

NO_FINAL_RULE
AMBIGUOUS_FINAL_RULE
NO_PRODUCER
UNSAFE_PRODUCER
AMBIGUOUS_PRODUCER
CYCLE_DETECTED
DEPTH_LIMIT

PRODUCER_NOT_APPLICABLE
PRODUCER_OUTPUT_NOT_USABLE
FINAL_RULE_NOT_APPLICABLE
GOAL_NOT_DERIVED

PRODUCER_RETRY_EXHAUSTED
```

`BoundedProducerSearchReport` は search failure と execution failure を同じ API で表し、execution failure では selected `search_result` を残す。

最重要 invariant:

```text
diagnosed selected path
=
executed path
```

---

# 10. Phase 86 bounded depth parameterization

既存 API 名は compatibility のため `depth_two` を含むが、実際の selection / diagnostics / report / execution は explicit `max_depth` を受け取る。

正式 regression:

```text
max_depth=2
max_depth=3
max_depth=4
```

default:

```text
max_depth=2
```

depth は producer edge 数で数える。

cycle classification は depth boundary と独立に保持する。

---

# 11. Phase 87 finite producer retry

表現:

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

default:

```text
retry_policy=None
```

複数 safe producer が残る場合:

```text
retry_policy=None
→ AMBIGUOUS_PRODUCER
```

明示 policy がある場合だけ registration order で有限個試行する。

candidate selection failure 時は temporary selection state を rollback し、次 candidate を試せる。

budget exhausted:

```text
PRODUCER_RETRY_EXHAUSTED
```

これは general backtracking ではない。

---

# 12. Phase 88 の中心問題：type collision と theorem-instance ambiguity の分離

同じ `conclusion_type` を持つ producer rule が複数あっても、それだけでは実際の theorem ambiguity ではない。

代表例:

```text
TodaDeltaImageUpToSignStatement

Δ(ι₅)
Δ(ι₉)
Δ(ι₁₇)
```

type-only lookup:

```text
3 candidates
```

concrete request:

```text
Δ(ι₁₇)
```

なら、goal-side compatibility によって unrelated instance を除外できる。

設計原則:

```text
same conclusion type
!=
same concrete theorem target
```

---

# 13. PremiseAvailability.bindings

Phase 88 では `detect_missing_premises()` が selected premise matching の bindings を捨てない。

`PremiseAvailability`:

```text
inference_rule
matched_steps
missing_indices
bindings
```

bindings は missing premise を concrete 化するための context である。

best-match selection の既存 tie behavior は維持する。

```text
strictly greater match count のときだけ best を更新
→ 同数 tie では最初の assignment を保持
```

---

# 14. concrete requested_statement

`MissingPremiseProducerLookup` は:

```text
inference_rule
premise_index
premise_pattern
producer_rules
requested_statement
```

を保持する。

concrete 化:

```text
known sibling premises
↓
VariableBinding
↓
missing PremisePattern.statement_pattern
↓
all PatternVariable が bound されているか確認
↓
substitute
↓
requested_statement
```

重要 safety boundary:

```text
unbound PatternVariable
→ requested_statement=None
```

とし、`PatternVariable` を `None` へ誤置換した concrete statement を作らない。

type-only pattern や完全に binding できない pattern では legacy lookup へ戻る。

---

# 15. producer-side concrete compatibility

producer lookup API は optional:

```text
requested_statement=None
```

を受け取る。

flow:

```text
premise statement_type
↓
candidate conclusion_type
↓
requested_statement がある場合:
  goal_compatibility(requested_statement)
↓
fixed_point_safe filtering
↓
producer rules
```

`requested_statement=None` では Phase 82–87 の type-only behavior を維持する。

維持 invariant:

```text
catalog registration order
InferenceRule identity deduplication
fixed_point_safe semantics
```

---

# 16. false ambiguity と true ambiguity

Phase 88 後の責務分離:

```text
same-type but different theorem instances
→ concrete compatibility filtering
→ false ambiguity を除去

same concrete requested statement に複数 producer が残る
→ true ambiguity
→ Phase 87 finite retry の対象
```

retry は false ambiguity の補修機構として使わない。

---

# 17. unsafe producer diagnostic consistency

safe producer lookup と unsafe diagnostic lookup は同じ concrete `requested_statement` を利用する。

したがって:

```text
requested = Δ(ι₁₇)

unsafe same-type entries:
  Δ(ι₅)
  Δ(ι₉)
  Δ(ι₁₇)

diagnostic:
  concrete-compatible Δ(ι₁₇) entry only
```

となる。

safe selection と diagnostic で theorem-instance semantics を分岐させない。

---

# 18. BoundedProducerSearchNode.requested_statement

selected path でも concrete request を失わないため:

```text
BoundedProducerSearchNode.requested_statement
```

を保持する。

propagation:

```text
MissingPremiseProducerLookup.requested_statement
↓
selection node spec
↓
BoundedProducerSearchNode.requested_statement
↓
BoundedProducerSearchResult
↓
BoundedProducerSearchReport
↓
execution diagnostic
```

default:

```text
requested_statement=None
```

で Phase 84–87 の direct node construction と互換性を維持する。

---

# 19. concrete execution validation

producer 実行後の output validation:

```text
requested_statement is not None
→ step.conclusion == requested_statement

requested_statement is None
→ legacy match_premise_pattern(node.premise_pattern, step)
```

これにより:

```text
requested B(ι₁₇)
actual B(ι₉)
```

のような wrong concrete instance は producer node で:

```text
PRODUCER_OUTPUT_NOT_USABLE
```

として分類する。

後段の final-rule failure まで誤りを持ち越さない。

---

# 20. Phase 88 end-to-end representative regression

real producer rules:

```text
Phase 52  Δ(ι₅)
Phase 66  Δ(ι₉)
Phase 76  Δ(ι₁₇)
```

same conclusion type:

```text
TodaDeltaImageUpToSignStatement
```

fixture:

```text
real Phase 76 prerequisites in repository
+
real Δ producer collision catalog
+
minimal synthetic final rule requesting concrete Δ(ι₁₇)
```

verified:

```text
type-only lookup = 3 producers
concrete requested_statement = Δ(ι₁₇)
filtered lookup = Δ(ι₁₇) producer only
selection succeeds without retry
selected node preserves requested_statement
report = SUCCESS
execution = SUCCESS
producer ProofStep uses selected real Δ(ι₁₇) rule
final ProofStep uses synthetic final rule
Δ(ι₅) / Δ(ι₉) are not selected
repository unchanged
```

---

# 21. proof-search safety invariants

現在維持する invariant:

```text
finite depth bound
finite retry bound
fixed-point-safe opt-in
concrete compatibility when safely available
legacy type-only fallback
cycle detection
shared dependency reuse
dependency-first order
selection rollback for failed retry candidates
selected path = executed path
concrete producer output validation
ProofStep provenance
repository non-mutation
```

---

# 22. 意図的に未実装の一般化

```text
unbounded recursive proof search
general backtracking
producer ranking
proof-cost model
best-proof selection
DFS
BFS
A*
formal max_depth > 4 coverage
persistent search cache
persistent Proof Repository
automatic proof narrative generation
generic theorem prover
generic mathematical-equivalence goal normalization
```

これらは concrete need が確認されるまで追加しない。

---

# 23. テスト / regression 方針

各 proof-search extension で確認する:

```text
representation
backward compatibility
positive selection
negative selection
ambiguity
wrong instance
diagnostics
execution
provenance
repository non-mutation
full regression
```

Phase 88 completion:

```text
end-to-end regression: 8 passed in 2.06s
Phase 88 related:      47 passed in 2.96s
search/retry/execution:34 passed in 2.41s
repository-wide:      7096 passed in 35.90s
git diff --check:     clean
```

wall-clock time は machine-dependent とし、test count と semantic coverage を主要 signal とする。

---

# 24. 現在の completion boundary

数学:

```text
Toda Lemma 5.16 までの concrete proof spine
stable G_0 through G_7
```

proof infrastructure:

```text
in-memory Proof Repository
automatic final-rule selection
one-level and multiple-missing producer generation
bounded dependency DAG search
max_depth 2 / 3 / 4 regression
search / execution diagnostics
integrated selected-path execution
finite explicit retry
concrete theorem-instance producer filtering
concrete requested-premise provenance
concrete execution-output validation
```

Phase 88 は COMPLETE。

次 Phase は新しい mechanism を即実装せず、実際の remaining ambiguity / search pressure を監査してから決定する。
