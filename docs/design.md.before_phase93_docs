# EHP Proof Tracer 設計

この文書は、EHP Proof Tracer の現在のアーキテクチャ、意味論、設計境界を記録する。

過去の実装経緯は `docs/development_log.md`、今後の Phase 順序は `docs/roadmap.md`、主要コードの探索は `docs/code_reference.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` に分離する。

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
calculation report != proof truth
presentation != mathematical data
```

既存 API と既存 proof provenance を保ち、将来 Phase の一般化を先取りしない。

---

# 2. レイヤー分離

現在の主要 layer:

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

Phase 90 以降、この上に calculation / extraction layer が加わった。

```text
TodaGroupQuery
↓
theorem-backed result lookup
↓
TodaGroupResult
↓
EHP extraction
↓
EHP term group enrichment
↓
exactness-use provenance
↓
future dependency / explanation layer
```

重要:

```text
calculation / extraction layer
```

は既存 theorem-backed proof object を束ねる責務を持つが、Toda theorem 自体を知る layer にはしない。

---

# 3. 主要モジュールの責務

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
= repository-assisted rule selection
  bounded producer search
  diagnostics
  execution

relation_rules.py
= generic relation propagation

homotopy_groups.py
= homotopy / Toda group and EHP structural data

toda_rules.py
= Toda-specific theorem knowledge

toda_group_query.py
= Toda query validation / target construction

toda_group_lookup.py
= Toda-specific known-result lookup

toda_group_result.py
= normalized theorem-backed group result

toda_ehp_result.py
= minimal EHP sequence / window result representation

toda_ehp_extraction.py
= actual theorem-backed EHP extraction from ProofStep ancestry

toda_ehp_group_enrichment.py
= EHP term -> known TodaGroupResult connection

toda_ehp_exactness_provenance.py
= exactness ProofStep / direct-consumer provenance

probes/
= representative capability demonstrations

tests/
= semantic / regression / provenance verification
```

---

# 4. structural equality と mathematical equality

Python dataclass の equality は syntax tree の一致を表す。

```text
同じ syntax
→ structural equality
```

数学的に同値だが syntax が異なる場合は、必要な concrete theorem branch に限定して explicit relation / inference rule で接続する。

global normalization や一般 CAS 化は行わない。

---

# 5. ordinary homotopy group と Toda π_i^n

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

current user-facing query target は:

```text
π_{n+k}^n
```

であり、一般の odd-primary component を統合した ordinary `π_{n+k}(S^n)` calculator ではない。

---

# 6. generic inference engine

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

provenance truth source:

```text
ProofStep.premises
ProofStep.inference_rule
```

Phase 92 の extraction でもこの provenance を利用する。

---

# 7. Proof Repository

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
presentation
```

repository metadata:

```text
key
phase
theorem
```

は mathematical truth 判定には使わない。

truth source は:

```text
entry.step.conclusion
entry.step.premises
entry.step.inference_rule
```

である。

---

# 8. bounded proof-search の安全境界

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

defaults:

```text
max_depth=2
retry_policy=None
```

formal regression:

```text
max_depth=2
max_depth=3
max_depth=4
```

Phase 89 audit 後も general backtracking / ranking / proof-cost model は deferred のままである。

---

# 9. Toda group query semantics

`TodaGroupQuery(n,k)`:

```text
n is int and not bool
n >= 1

k is int and not bool
k >= 0
```

target:

```text
TodaPrimaryGroup(
  group_dimension=n+k,
  sphere_dimension=n,
)
```

query object の責務:

```text
input validation
target construction
```

責務ではない:

```text
proof truth
proof search
group computation
presentation
```

---

# 10. known theorem-backed group lookup

`find_known_toda_group_results()` は repository 内の既存 theorem-backed group result を探す。

nonzero canonical shape:

```text
Relation(
  lhs=target,
  rhs=FreeCyclicGroup
      | FiniteCyclicGroup
      | DirectSumGroup,
  relation_type=EQUALITY,
)
```

zero canonical shape:

```text
TodaPrimaryGroupZeroStatement(group=target)
```

lookup result:

```text
0 match
→ ()

1 match
→ one entry

multiple matches
→ all entries in registration order
```

lookup miss で proof search は起動しない。

---

# 11. normalized group result

`TodaGroupResult`:

```text
target
group_structure
generators
generator_orders
source_entry
proof_step
```

order semantics:

```text
None
= infinite order

positive int
= finite order
```

zero group:

```text
group_structure=None
generators=()
generator_orders=()
```

identity preservation:

```text
result.source_entry is original ProofRepositoryEntry
result.proof_step is original ProofStep
result.group_structure is original RHS object when nonzero
```

---

# 12. EHP structural representation

既存 structural layer:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaProp42ExactnessStatement
```

`TodaEHPSequence` は sequence の項と map を保持する。

`TodaEHPExactnessWindow` は連続する3項と2 map を保持する。

`TodaProp42ExactnessStatement` はその window の exactness theorem semantics を表す。

structural window 自体と exactness theorem は区別する。

```text
TodaEHPExactnessWindow
= structure

TodaProp42ExactnessStatement
= exactness theorem conclusion
```

---

# 13. Phase 92-2 result representation

追加:

```text
TodaEHPExactnessWindowResult
TodaEHPSequenceResult
```

`TodaEHPExactnessWindowResult`:

```text
window
```

既存 `TodaEHPExactnessWindow` identity を保持する。

`TodaEHPSequenceResult`:

```text
target
sequence
windows
```

invariant:

```text
target は sequence.terms に含まれる
各 window は sequence の contiguous window
windows は sequence 全体の subset でもよい
```

Phase 92-2 は group structure / provenance を混ぜず、structural result representation に限定した。

---

# 14. Phase 92-3 actual theorem-backed EHP extraction

入口:

```text
TodaGroupResult.proof_step
```

extraction:

```text
final ProofStep
↓
reachable ProofStep.premises
↓
TodaProp42ExactnessStatement
↓
target に関係する TodaEHPExactnessWindow
↓
contiguous ordering
↓
TodaEHPSequenceResult
```

代表 actual proof:

```text
π_9^5=Z/2{ν_5η_8}
```

抽出される EHP chain:

```text
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

重要:

```text
repository に存在する EHP facts
```

を列挙するのではなく、

```text
final theorem-backed proof ancestry から到達可能な EHP exactness facts
```

を抽出する。

Phase 92-3 の traversal は EHP extraction 専用であり、generic dependency API ではない。

---

# 15. Phase 92-4 EHP term group enrichment

追加:

```text
TodaEHPGroupTermResult
TodaEHPGroupEnrichmentResult
connect_known_toda_group_results()
```

各 EHP term について既存 `TodaGroupQuery` / normalized lookup を再利用する。

```text
term
↓
TodaGroupQuery
↓
ProofRepository
↓
tuple[TodaGroupResult, ...]
```

unknown:

```text
group_results=()
```

known zero:

```text
group_results=(TodaGroupResult(group_structure=None),)
```

したがって:

```text
unknown != zero
```

を維持する。

EHP term の順序は `TodaEHPSequence.terms` と同一に保つ。

---

# 16. Phase 92-5 exactness-use provenance

追加:

```text
TodaEHPExactnessUseResult
TodaEHPExactnessUseProvenanceResult
extract_toda_ehp_exactness_use_provenance()
```

各 exactness window に対して:

```text
window_result
exactness_step
consumer_steps
```

を保持する。

`exactness_step` は:

```text
TodaProp42ExactnessStatement
```

を conclusion に持つ actual `ProofStep`。

`consumer_steps` は:

```text
consumer_step.premises
```

にその exactness step を identity で直接含む reachable `ProofStep`。

これにより:

```text
exactness window が存在する
```

ことと、

```text
その exactness が proof のどこで直接使われたか
```

を区別できる。

この layer は EHP exactness 専用であり、general dependency graph ではない。

---

# 17. Phase 92 end-to-end data flow

現在の theorem-backed flow:

```text
(n,k)
↓
TodaGroupQuery
↓
ProofRepositoryEntry
↓
TodaGroupResult
↓
ProofStep ancestry
↓
TodaEHPSequenceResult
↓
TodaEHPGroupEnrichmentResult
↓
TodaEHPExactnessUseProvenanceResult
```

代表:

```text
target:
π_9^5

EHP:
π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

group enrichment example:

```text
π_10^9 -> unresolved
π_8^4  -> known
π_9^5  -> known
π_9^9  -> unresolved
π_7^4  -> known
```

exactness provenance example:

```text
H-Δ exactness
↓
actual TodaProp42ExactnessStatement ProofStep
↓
hopf-zero derivation consumer
```

---

# 18. non-destructive extraction principle

Phase 90–92 の上位 layer は原則として既存 proof graph を copy / rebuild しない。

保持すべき identity:

```text
ProofRepositoryEntry
ProofStep
group structure object
TodaEHPExactnessWindow
TodaEHPSequenceResult input object
```

extraction / normalization / enrichment は read-only であり、repository を mutate しない。

---

# 19. unknown / zero / imported の区別

少なくとも以下を混同しない。

```text
unknown group
= repository に group result がない

known zero group
= theorem-backed zero result がある

structural EHP window
= sequence structure

exactness theorem
= TodaProp42ExactnessStatement

direct exactness use
= exactness_step が consumer premise に identity で含まれる
```

Phase 93 以降ではさらに:

```text
derived
proved
imported
assumed
```

等の dependency status を concrete need に基づいて整理する。

---

# 20. Phase 93 への境界

次は:

```text
Phase 93
proof dependency extraction / explanation layer
```

目的:

```text
final theorem-backed result
↓
actually used mathematical dependencies
↓
role-aware machine-readable explanation
```

候補 dependency:

```text
propositions
lemmas
relations
previously known groups
EHP exactness facts
map properties
generator / order facts
```

Phase 93 で先に行わないもの:

```text
recursive full proof narration
best-proof selection
proof ranking
generic theorem proving
automatic citation prose
persistent proof database
```

generic dependency extraction は actual theorem-backed need から最小に設計する。

---

# 21. verification policy

Phase completion は最低限:

```text
focused tests
related regression
repository-wide pytest
git diff --check
```

で確認する。

Phase 92-5 completion:

```text
focused:
68 passed in 8.90s

repository-wide:
7203 passed in 109.03s

git diff --check:
clean
```

wall-clock time は machine-dependent。

主要な cross-machine signal:

```text
test count
semantic coverage
provenance coverage
focused regression
repository-wide regression
```

---

# 22. 文書運用

```text
README.md
= current status / capabilities

docs/design.md
= current architecture / semantics / boundaries

docs/development_log.md
= chronological implementation history

docs/roadmap.md
= future-oriented plan

docs/code_reference.md
= code navigation

docs/proof_records.md
= representative proof / infrastructure records
```

`development_log.md` と `proof_records.md` は原則追記型。

`design.md` と `roadmap.md` は current state に合わせて古い計画を訂正・削除してよい。
