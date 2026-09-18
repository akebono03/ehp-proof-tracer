# 42. Infrastructure Record — Phase 90 Toda group query / known-result lookup

## 42.1 記録種別

Phase 90 は calculation-query infrastructure record。

新しい数学 theorem を証明しない。

既に証明・登録された theorem-backed group result を `(n,k)` query から取得する最初の縦断経路を構築する。

数学的 formal proof record 数は13のまま。

## 42.2 TodaGroupQuery

追加:

```text
toda_group_query.py
TodaGroupQuery(n,k)
```

target:

```text
TodaPrimaryGroup(
  group_dimension=n+k,
  sphere_dimension=n,
)
```

validation:

```text
n >= 1
k >= 0
int only
bool rejected
```

query object は proof truth を持たず:

```text
input validation
target construction
```

のみを責務とする。

## 42.3 canonical known group-result shape

nonzero:

```text
Relation(
  lhs=target,
  rhs=FreeCyclicGroup
      | FiniteCyclicGroup
      | DirectSumGroup,
  relation_type=EQUALITY,
)
```

zero:

```text
TodaPrimaryGroupZeroStatement(
  group=target,
)
```

zero を fake cyclic group へ変換しない。

## 42.4 known-result lookup

追加:

```text
toda_group_lookup.py

is_toda_group_result_for_target()
find_known_toda_group_results()
```

flow:

```text
TodaGroupQuery
↓
query.target
↓
ProofRepository.entries()
↓
entry.step.conclusion
↓
group-result predicate
↓
tuple[ProofRepositoryEntry, ...]
```

generic `ProofRepository` は Toda-specific knowledge を持たないまま維持する。

## 42.5 lookup semantics

```text
GIVEN
INFERENCE
```

の両方を lookup 対象とする。

```text
0 match
→ ()

1 match
→ one entry

multiple matches
→ all entries in registration order
```

Phase 90 では:

```text
ranking
winner selection
conflict resolution
canonical proof selection
```

を行わない。

## 42.6 miss semantics

```text
lookup miss
!=
proof failure
```

Phase 90:

```text
miss → ()
```

のみ。

automatic producer search / inference は起動しない。

## 42.7 actual theorem-backed integration

### π_7^4

```text
TodaGroupQuery(4,3)
↓
Phase 65 actual ProofStep
↓
π_7^4
=
Z{ν₄}⊕Z/4{Eν′}
```

### π_10^4

```text
TodaGroupQuery(4,6)
↓
Phase 73 actual ProofStep
↓
π_10^4
=
Z/8{ν₄²}
```

### π_9^2

```text
TodaGroupQuery(2,7)
↓
Phase 75 actual ProofStep
↓
π_9^2
=
0
```

## 42.8 identity / provenance

verified:

```text
returned ProofRepositoryEntry is expected actual entry
returned entry.step is exact original ProofStep object
actual premises preserved
actual INFERENCE rule preserved
cross-target match absent
repository unchanged
```

query layer は proof graph を再構築しない。

## 42.9 regression

Phase 90-2:

```text
13 passed in 1.04s
repository-wide:
7109 passed in 118.26s
```

Phase 90-3-2 related:

```text
50 passed in 5.89s
repository-wide:
7125 passed in 97.71s
```

Phase 90-3-3 related:

```text
108 passed in 8.67s
repository-wide:
7135 passed in 101.39s
```

```text
git diff --check
clean
```

## 42.10 completion boundary

完成:

```text
(n,k)
→ Toda target
→ existing theorem-backed group result
→ actual ProofStep
```

未実装:

```text
normalized calculation result
generator / order extraction
EHP exactness extraction
dependency extraction
recursive proof traversal
fact classification
proof search on lookup miss
top-level calculation orchestration
automatic human-readable report
```

## 42.11 記録状態

```text
Phase 90
COMPLETE
```

---

---

# 44. Phase 91 infrastructure record：normalized theorem-backed group result

Phase 91 は新しい数学 theorem を証明する Phase ではない。

Phase 90 で取得可能になった actual theorem-backed group result を:

```text
group structure
generator
generator order
proof provenance
```

を失わず machine-readable に正規化する infrastructure Phase である。

## 44.1 normalized result

追加:

```text
TodaGroupResult
```

fields:

```text
target
group_structure
generators
generator_orders
source_entry
proof_step
```

truth source は引き続き:

```text
source_entry.step.conclusion
```

であり、normalized object が theorem truth を新規に作るわけではない。

## 44.2 generator-order semantics

```text
FiniteCyclicGroup
→ positive integer order

FreeCyclicGroup
→ None
```

`None` は:

```text
infinite order
```

を表す。

zero group:

```text
group_structure=None
generators=()
generator_orders=()
```

## 44.3 DirectSumGroup ordering

`DirectSumGroup.summands` の tuple 順序を保持して:

```text
summand[0]
→ generators[0]
→ generator_orders[0]

summand[1]
→ generators[1]
→ generator_orders[1]
```

の対応を維持する。

normalization 時の sorting や canonical direct-sum rearrangement は行わない。

## 44.4 actual theorem-backed π_7^4

Phase 65 actual ProofStep:

```text
π_7^4
=
Z{ν₄}
⊕
Z/4{Eν′}
```

Phase 91 normalized result:

```text
target
=
π_7^4

group_structure
=
DirectSumGroup(
  FreeCyclicGroup(ν₄),
  FiniteCyclicGroup(4,Eν′),
)

generators
=
(ν₄,Eν′)

generator_orders
=
(None,4)
```

verified:

```text
normalized group_structure
is
actual conclusion.rhs
```

## 44.5 actual theorem-backed π_10^4

Phase 73 actual ProofStep:

```text
π_10^4
=
Z/8{ν₄²}
```

normalized:

```text
group_structure
=
FiniteCyclicGroup(
  order=8,
  generator=ν₄²,
)

generators
=
(ν₄²,)

generator_orders
=
(8,)
```

## 44.6 actual theorem-backed π_9^2

Phase 75 actual ProofStep:

```text
π_9^2=0
```

normalized:

```text
group_structure=None
generators=()
generator_orders=()
```

zero result を synthetic `ZeroGroup` class に変換せず、Phase 91 の最小表現では `None` を使用する。

## 44.7 proof identity / provenance

Phase 91 の重要 invariant:

```text
result.source_entry
is
actual repository entry
```

かつ:

```text
result.proof_step
is
actual ProofStep
```

さらに:

```text
result.proof_step
is
result.source_entry.step
```

を `TodaGroupResult` 自体の invariant として要求する。

これにより:

```text
TodaGroupResult
↓
ProofRepositoryEntry
↓
actual ProofStep
↓
premises
↓
upstream theorem-backed proof graph
```

へ戻れる。

normalized result は proof graph を複製しない。

## 44.8 lookup integration

Phase 90:

```text
find_known_toda_group_results()
```

はそのまま残す。

Phase 91 追加:

```text
normalize_toda_group_result()
find_normalized_toda_group_results()
```

flow:

```text
query
↓
known-result lookup
↓
actual entries
↓
normalization
↓
TodaGroupResult tuple
```

lookup miss:

```text
()
```

の semantics は Phase 90 から変更しない。

automatic proof search はまだ起動しない。

## 44.9 repository non-mutation

Phase 91 normalization 前後で:

```text
repository.entries()
```

が structural equality だけでなく object identity の並びも維持されることを確認した。

したがって:

```text
query
lookup
normalization
```

はいずれも repository read-only layer である。

## 44.10 regression

Phase 91-2:

```text
minimal normalized result:
10 passed in 0.90s

Phase 90-91 regression:
49 passed in 6.00s

repository-wide:
7145 passed in 107.78s
```

Phase 91-3:

```text
actual theorem-backed normalization:
9 passed in 6.39s

Phase 90-91 regression:
58 passed in 7.82s

repository-wide:
7154 passed in 100.44s

git diff --check:
clean
```

## 44.11 completion boundary

完成:

```text
(n,k)
→ Toda target
→ theorem-backed entry
→ actual ProofStep
→ normalized group structure
→ generators
→ generator orders
```

未実装:

```text
EHP sequence extraction
exactness-use extraction
dependency extraction
recursive proof traversal
fact classification
proof search on lookup miss
top-level calculation orchestration
automatic human-readable report
```

## 44.12 記録状態

```text
Phase 91
COMPLETE
```

---

# 45. 現在の proof-record 状態 after Phase 91

数学的 formal proof records:

```text
13
```

infrastructure records through:

```text
Phase 79  minimal in-memory Proof Repository
Phase 80  repository-assisted inference
Phase 81  automatic rule selection
Phase 82  one-level producer search
Phase 83  multiple one-level producers
Phase 84  bounded depth=2 search
Phase 85  diagnostics / integrated execution
Phase 86  max_depth parameterization
Phase 87  finite retry
Phase 88  concrete theorem-instance filtering
Phase 89  proof-search pressure audit
Phase 90  query / known-result lookup
Phase 91  normalized group structure / generator result
```

最新 mathematical frontier:

```text
stable G_0 through G_7
```

最新 calculation-result capability:

```text
(n,k)
→ TodaPrimaryGroup(n+k,n)
→ existing theorem-backed group result
→ actual ProofStep
→ TodaGroupResult
→ group structure / generators / generator orders
```

次:

```text
Phase 92-1
current EHP sequence / exactness representation audit
```

---

# Phase 92 proof record：actual theorem-backed EHP extraction

## 対象

actual theorem-backed group result:

```text
π_9^5 = Z/2{ν_5η_8}
```

入口:

```text
TodaGroupResult.proof_step
```

## 抽出された EHP chain

```text
π_10^9
  --Δ-->
π_8^4
  --E-->
π_9^5
  --H-->
π_9^9
  --Δ-->
π_7^4
```

対応する exactness windows:

```text
Δ-E:
π_10^9 --Δ--> π_8^4 --E--> π_9^5

E-H:
π_8^4 --E--> π_9^5 --H--> π_9^9

H-Δ:
π_9^5 --H--> π_9^9 --Δ--> π_7^4
```

## provenance

各 structural window は existing `TodaEHPExactnessWindow` identity を保持する。

exactness theorem:

```text
TodaProp42ExactnessStatement(window=...)
```

は actual `ProofStep` として保持される。

Phase 92-5 ではさらに:

```text
window_result
↓
exactness_step
↓
direct consumer_steps
```

を記録する。

代表:

```text
H-Δ exactness
↓
actual TodaProp42ExactnessStatement ProofStep
↓
hopf_zero_step
```

## group enrichment

同じ EHP chain 上で repository に known theorem-backed group result がある項だけを接続する。

代表 fixture:

```text
π_10^9 -> unknown
π_8^4  -> known
π_9^5  -> known
π_9^9  -> unknown
π_7^4  -> known
```

意味:

```text
unknown
→ group_results=()

known zero
→ TodaGroupResult(group_structure=None)
```

よって unknown と zero は区別される。

## non-destructive identity

保持:

```text
TodaGroupResult.proof_step
ProofRepositoryEntry
TodaEHPExactnessWindow
exactness ProofStep
consumer ProofStep
```

抽出 / enrichment / provenance connection は repository を mutate しない。

## regression record

Phase 92-2:

```text
15 passed in 2.78s
repository-wide:
7169 passed in 104.18s
```

Phase 92-3 correction completion:

```text
44 passed in 7.25s
repository-wide:
7179 passed in 97.33s
```

Phase 92-4:

```text
75 passed in 8.34s
repository-wide:
7191 passed in 92.43s
```

Phase 92-5:

```text
68 passed in 8.90s
repository-wide:
7203 passed in 109.03s
git diff --check clean
```

## Phase 92 boundary

Phase 92 は EHP-specific extraction / enrichment / exactness-use provenance まで。

deferred:

```text
generic dependency extraction
dependency role classification
recursive proof explanation
automatic proof narrative generation
```

次:

```text
Phase 93
proof dependency extraction / explanation layer
```

---

# 17. Phase 93 proof dependency / representative explanation infrastructure

## 17.1 記録の位置づけ

Phase 93 は新しい Toda theorem を証明した Phase ではない。

既に theorem-backed に導出済みの結果から:

```text
何を使ってその結論を得たか
```

を machine-readable に抽出する infrastructure を追加した。

代表 target:

```text
π_9^5=Z/2{ν₅η₈}
```

Phase 68 で既に導出済みのこの theorem-backed result を使い、proof dependency / role / EHP provenance を統合した。

したがってこの記録は:

```text
mathematical theorem record
```

ではなく:

```text
proof explanation infrastructure record
```

である。

---

## 17.2 Representative result

代表 result:

```text
π_9^5=Z/2{ν₅η₈}
```

既存 `TodaGroupResult`:

```text
target
group_structure
generators
generator_orders
source_entry
proof_step
```

を変更せず再利用する。

---

## 17.3 EHP context

Phase 92 extraction で actual final proof ancestry から得られる EHP chain:

```text
π_10^9
  --Δ-->
π_8^4
  --E-->
π_9^5
  --H-->
π_9^9
  --Δ-->
π_7^4
```

3 exactness windows:

```text
Δ-E
E-H
H-Δ
```

は actual `TodaProp42ExactnessStatement` `ProofStep` と結びついている。

---

## 17.4 Dependency extraction

Phase 93-3:

```text
extract_toda_proof_dependencies()
```

は final:

```text
group_result.proof_step
```

を root として breadth-first に premise graph を辿る。

dependency record:

```text
TodaProofDependency(
  proof_step,
  depth,
  role,
)
```

depth semantics:

```text
1
= direct premise

2+
= transitive premise
```

shared dependency が複数経路に存在する場合:

```text
shortest depth
```

を採用する。

identity:

```text
id(ProofStep)
```

で deduplicate する。

---

## 17.5 Representative dependency roles

actual `π_9^5` proof graph では代表的に:

```text
delta_e_exactness_step
e_h_exactness_step
h_delta_exactness_step
→ EHP_EXACTNESS
```

```text
delta_e_window_step
e_h_window_step
h_delta_window_step
→ EHP_WINDOW
```

```text
π_8^4 group result
→ GROUP_STRUCTURE
```

```text
Δ injectivity
Hopf zero
E surjectivity
→ MAP_PROPERTY
```

```text
Δ(η₉)=Eν′η₇
generator bridge
→ RELATION
```

```text
ν₅ definition
→ DEFINITION
```

として分類される。

---

## 17.6 Role classification boundary

current roles:

```text
EHP_EXACTNESS
EHP_WINDOW
GROUP_STRUCTURE
RELATION
ORDER
MAP_PROPERTY
DEFINITION
LITERATURE
OTHER
```

classification truth:

```text
ProofStep.conclusion type
RelationType
```

を中心に判定する。

使用しないもの:

```text
repository phase string
repository theorem string
class-name substring guessing
```

未知の Toda-specific statement は:

```text
OTHER
```

へ残す。

これは incomplete classification ではなく、誤分類を避けるための explicit boundary。

---

## 17.7 Representative explanation integration

Phase 93-5 で:

```text
TodaRepresentativeExplanationResult
```

を追加。

保持:

```text
group_result
ehp_result
exactness_provenance
dependency_result
```

概念図:

```text
π_9^5 theorem-backed result
│
├─ group result
│  └─ Z/2{ν₅η₈}
│
├─ EHP result
│  └─ π_10^9 --Δ--> π_8^4 --E--> π_9^5 --H--> π_9^9 --Δ--> π_7^4
│
├─ exactness provenance
│  ├─ Δ-E exactness ProofStep
│  ├─ E-H exactness ProofStep
│  └─ H-Δ exactness ProofStep
│
└─ dependency result
   ├─ group facts
   ├─ map properties
   ├─ relations
   ├─ definitions
   └─ other reachable proof facts
```

---

## 17.8 Identity / provenance invariants

Phase 93 では既存 proof object を再構築しない。

確認:

```text
explanation.group_result
is original TodaGroupResult

dependency_result.root_step
is group_result.proof_step

group_result.proof_step
is source_entry.step

dependency.proof_step
is actual reachable ProofStep
```

shared dependency は copy しない。

repository も mutate しない。

---

## 17.9 GIVEN / INFERENCE boundary

Phase 93 は existing proof graph を read-only に観察する。

したがって Phase 93 自身は:

```text
GIVEN → INFERENCE
```

の theorem-spine を新たに作る Phase ではない。

各 dependency の `ProofStep.rule` は upstream Phase で確立済みの値をそのまま保持する。

例:

```text
structural EHP window
→ GIVEN

actual exactness theorem step
→ INFERENCE

π_8^4 result
→ INFERENCE

Hopf-zero
→ INFERENCE
```

Phase 93 はこれらを書き換えない。

---

## 17.10 Flat dependency view の限界

Phase 93 result は:

```text
dependency
depth
role
```

を提供する。

ただし:

```text
dependency A
├─ premise A1
└─ premise A2
```

という edge relation 自体を first-class result object としてまだ保持しない。

元の `ProofStep.premises` には情報が存在するが、Phase 93 explanation result は flat dependency view。

この境界を超えるのが Phase 94。

---

## 17.11 Phase 94 boundary

次:

```text
Phase 94
recursive proof provenance
```

目標:

```text
final
├─ A
│  ├─ A1
│  └─ shared
└─ B
   └─ shared
```

を shared-node-preserving DAG として machine-readable に保持すること。

Phase 94 でも automatic narrative generation はまだ別 layer とする。

---

## 17.12 Regression status

Phase 93-2 completion:

```text
16 passed in 2.43s
repository-wide:
7219 passed in 104.72s
```

Phase 93-3 completion:

```text
32 passed in 8.50s
repository-wide:
7235 passed in 99.34s
```

Phase 93-4 completion:

```text
49 passed in 7.29s
repository-wide:
7252 passed in 91.30s
```

Phase 93-5 completion:

```text
66 passed in 7.61s

Phase 92 -> 93:
88 passed in 5.05s

repository-wide:
7269 passed in 102.15s

git diff --check:
clean
```

### 状態

COMPLETE

---

# Phase 94 infrastructure record：recursive proof provenance

## 18.1 記録の位置づけ

Phase 94 は新しい Toda theorem を証明した Phase ではない。

Phase 93 で machine-readable になった:

```text
何を使ったか
```

という flat dependency view を、

```text
各 dependency がどの premise から導かれたか
```

まで保持する recursive proof graph へ拡張した infrastructure record である。

代表 target:

```text
π_9^5=Z/2{ν₅η₈}
```

root は Phase 68 actual theorem-backed:

```text
final_step
```

をそのまま使用する。

---

## 18.2 node representation

追加:

```text
TodaProofNode
```

fields:

```text
proof_step
shortest_depth
role
```

identity rule:

```text
same node
iff
same ProofStep object identity
```

したがって:

```text
equal-but-distinct ProofStep
```

は別 node。

shared dependency は copy せず一つの node として保持する。

---

## 18.3 edge representation

追加:

```text
TodaProofEdge
```

fields:

```text
parent_step
premise_step
premise_index
```

edge truth:

```text
parent_step.premises[premise_index]
is
premise_step
```

`premise_index` は元の unfiltered premise tuple の index。

例:

```text
parent.premises = (
  "non-ProofStep premise",
  child_step,
)
```

なら:

```text
edge.premise_index = 1
```

となる。

---

## 18.4 recursive result

追加:

```text
TodaRecursiveProofProvenanceResult
```

fields:

```text
root_step
nodes
edges
```

主要 invariant:

```text
root appears exactly once in nodes
root shortest_depth = 0
node ProofStep identities are unique
edge endpoints appear in nodes
duplicate proof edges are rejected
```

---

## 18.5 actual theorem-backed extraction

追加:

```text
extract_toda_recursive_proof_provenance()
```

入口:

```text
TodaGroupResult.proof_step
```

代表 `π_9^5`:

```text
group_result.proof_step
is
Phase 68 final_step
```

traversal は breadth-first。

node identity は `id(ProofStep)` で deduplicate する。

edge は parent を処理するときに original premise order で追加する。

---

## 18.6 Phase 93 flat view との整合

Phase 93:

```text
TodaProofDependencyResult
```

Phase 94:

```text
TodaRecursiveProofProvenanceResult
```

について:

```text
recursive nodes
=
root
+
flat dependencies
```

を identity set として確認。

また各 flat dependency について:

```text
dependency.depth
=
corresponding node.shortest_depth
```

が成立する。

shortest depth は graph structure そのものではなく summary metadata。

recursive truth は edges に保持される。

---

## 18.7 representative actual edges

actual `π_9^5` proof graph では代表的に:

```text
hopf_zero_step
├─ delta_injective_step
└─ h_delta_exactness_step
```

を edge として取得する。

さらに:

```text
delta_e_exactness_step
→ delta_e_window_step
```

のように actual exactness theorem step から structural EHP window step への dependency edge も保持する。

これらは repository theorem-name metadata から再構築した edge ではない。

truth source は:

```text
ProofStep.premises
```

そのもの。

---

## 18.8 shared-node semantics

synthetic DAG:

```text
root
├─ A
│  └─ shared
└─ B
   └─ shared
```

result:

```text
nodes:
root
A
B
shared
```

`shared` node は1回だけ。

edges:

```text
root -> A
root -> B
A -> shared
B -> shared
```

はすべて保持する。

したがって DAG を tree copy へ展開しない。

---

## 18.9 stable order

node order:

```text
breadth-first
+
premise tuple order
```

edge order:

```text
parent traversal order
+
premise_index order
```

を regression で固定。

同一 proof graph に対して deterministic な representation を得る。

---

## 18.10 cycle semantics

synthetic regression で:

```text
A -> B -> A
```

および:

```text
A -> A
```

を確認。

`seen_step_ids` により traversal は終了する。

ただし edge は:

```text
B -> A
A -> A
```

も失わない。

重要:

```text
cycle regression exists
!=
actual Toda proof graph is cyclic
```

である。

cycle fixture は traversal safety semantics を固定するためだけに用いる。

---

## 18.11 representative explanation integration

Phase 94-5 で:

```text
TodaRepresentativeExplanationResult
```

へ:

```text
recursive_provenance
```

を追加。

現在の fields:

```text
group_result
ehp_result
exactness_provenance
dependency_result
recursive_provenance
```

identity invariant:

```text
dependency_result.root_step
is recursive_provenance.root_step
is group_result.proof_step
```

したがって flat view と recursive view は同じ theorem-backed proof root を参照する。

---

## 18.12 non-destructive provenance

Phase 94 は existing proof graph を変更しない。

保持:

```text
group_result.proof_step identity
source_entry.step identity
dependency ProofStep identity
recursive node ProofStep identity
recursive edge endpoint ProofStep identity
premise ordering
premise index
```

repository も mutate しない。

---

## 18.13 regression record

Phase 94-2:

```text
related:
45 passed in 1.84s

repository-wide:
7282 passed in 36.82s
```

Phase 94-3:

```text
related:
68 passed in 3.06s

repository-wide:
7295 passed in 36.52s
```

Phase 94-4:

```text
related:
50 passed in 2.77s

repository-wide:
7303 passed in 36.63s
```

Phase 94-5:

```text
related:
48 passed in 2.98s

repository-wide:
7313 passed in 36.98s

git diff --check:
clean
```

---

## 18.14 Phase 94 completion boundary

Phase 94 で完成:

```text
flat dependency provenance
+
first-class proof nodes
+
first-class proof edges
+
shared-node-preserving DAG representation
+
cycle-safe traversal
+
stable ordering
+
actual π_9^5 recursive extraction
+
representative explanation integration
```

Phase 94 で行わない:

```text
automatic natural-language proof narration
top-level calculation orchestration
proof ranking
best-proof selection
persistent graph database
generic theorem proving
```

次:

```text
Phase 95-1
current calculation entry points / orchestration boundary audit
```

### 状態

COMPLETE
