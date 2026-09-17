# EHP Proof Tracer 設計

この文書は現在のアーキテクチャ、意味論、設計境界、および次の calculation orchestration layer の設計目標を記録する。

過去の実装経緯は `docs/development_log.md`、将来の Phase 順序は `docs/roadmap.md`、主要コードの探索は `docs/code_reference.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` に分離する。

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

Phase 90 以降はこの上に次を追加する。

```text
π_{n+k}^n query
↓
calculation orchestration
↓
structured calculation result
↓
dependency / recursive provenance extraction
↓
human-readable presentation
```

重要:

```text
calculation orchestration
```

は既存 layer を束ねる責務を持つが、Toda theorem 自体を知る layer にはしない。

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
= homotopy / Toda group and map data

toda_rules.py
= Toda-specific theorem knowledge

probes/
= representative capability demonstrations

tests/
= semantic / regression / provenance verification
```

Phase 90 以降の orchestration module の配置は Phase 90-1 audit 後に決める。

audit 前に新規 module 名を固定しない。

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

Phase 90 以降の user-facing query target は、現時点では ordinary

```text
π_{n+k}(S^n)
```

ではなく、

```text
π_{n+k}^n
```

とする。

理由:

```text
odd-primary components を一般的に統合していない
現在の Toda / EHP proof spine が Toda π_i^n を中心に構築されている
既存 TodaPrimaryGroup と直接接続できる
```

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

provenance は:

```text
ProofStep.premises
ProofStep.inference_rule
```

に保持する。

Phase 90 以降の dependency extraction はこの provenance を truth source とする。

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

repository metadata は inference applicability を変更しない。

同一 `ProofStep` alias は repository-to-available-steps bridge で identity deduplicate する一方、同じ conclusion を持つ別 `ProofStep` は別 proof として保持する。

---

# 8. InferenceRuleCatalog

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

`goal_compatibility` は concrete theorem-instance compatibility hook である。

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

# 9. proof-search progression

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

Phase 85
search / execution diagnostics

Phase 86
explicit max_depth parameterization

Phase 87
finite explicit producer retry

Phase 88
concrete theorem-instance compatibility filtering

Phase 89
post-Phase88 necessity audit
→ no concrete need for new general search algorithm
```

---

# 10. bounded search safety invariants

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

default:

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

---

# 11. Phase 87 finite producer retry

表現:

```text
FiniteProducerRetryPolicy(max_attempts=N)
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

# 12. Phase 88 concrete requested_statement semantics

same conclusion type collision は concrete theorem ambiguity と同一ではない。

代表:

```text
TodaDeltaImageUpToSignStatement

Δ(ι₅)
Δ(ι₉)
Δ(ι₁₇)
```

設計原則:

```text
same conclusion type
!=
same concrete theorem target
```

known sibling premises の bindings から safely concrete 化できる場合:

```text
PremisePattern
+
VariableBinding
↓
requested_statement
```

を構成する。

unbound variable が残る場合:

```text
requested_statement=None
```

として legacy type-only semantics に戻る。

---

# 13. producer-side concrete compatibility

producer lookup は optional:

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

selected path では:

```text
BoundedProducerSearchNode.requested_statement
```

に concrete request を保持する。

execution 後:

```text
requested_statement is not None
→ step.conclusion == requested_statement
```

を検証する。

wrong concrete instance は:

```text
PRODUCER_OUTPUT_NOT_USABLE
```

として分類する。

---

# 14. Phase 89 audit boundary

Phase 89-1 audit では次を確認した。

```text
actual theorem-backed true ambiguity
→ 現時点では未確認

general backtracking の concrete need
→ 未確認

producer ranking / proof-cost model の concrete need
→ 未確認

actual theorem-backed max_depth > 4 need
→ 未確認
```

したがって今後は search engine の抽象的一般化を先に進めない。

次の圧力源は:

```text
π_{n+k}^n calculation orchestration
```

とする。

---

# 15. calculation query の基本意味論

Phase 90 以降の基本 query:

```text
input:
n, k
```

target:

```text
TodaPrimaryGroup(
  group_dimension=n+k,
  sphere_dimension=n,
)
```

user-facing notation:

```text
π_{n+k}^n
```

query object は target construction のみを責務とし、proof truth を持たない。

概念:

```text
TodaGroupQuery
```

実際の class 名・module placement は Phase 90-1 audit 後に決定する。

---

# 16. calculation result の基本契約

最終的な structured result は少なくとも次の情報を保持できることを目標とする。

```text
target
group_structure
generators
generator_orders
relations
EHP data
exactness uses
dependencies
proof provenance
```

必要に応じて status / diagnostic も保持する。

重要:

```text
文字列 report
```

を mathematical truth source にしない。

必ず:

```text
structured facts
↓
structured calculation result
↓
presentation
```

とする。

---

# 17. group structure と generator 情報

計算結果では単なる抽象群だけでなく、可能な範囲で named generator を保持する。

例:

```text
π_8^5 = Z/8{ν_5}
```

から:

```text
group structure:
Z/8

generator:
ν_5

order:
8
```

を structured data として取り出せることを目標とする。

Direct sum の場合:

```text
summand
generator
order / free
```

の対応を失わない。

既存:

```text
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
```

を優先して再利用し、不必要に並行 group model を作らない。

---

# 18. EHP sequence の設計目標

既存:

```text
TodaEHPSequence
TodaEHPExactnessWindow
```

を calculation result と接続する。

出力対象は単なる sequence label ではない。

最低限:

```text
terms
maps
target position
known group structures
exactness points actually used
```

を扱う。

概念表示:

```text
A ─P→ B ─E→ π_{n+k}^n ─H→ C ─P→ D
```

可能なら各項の下に:

```text
known group structure
unknown
target result
```

を対応付ける。

---

# 19. exactness-use provenance

「EHP 完全列を使った」という一行だけでは proof trace として不十分。

実際に使用した完全性を:

```text
at B:
im(P) = ker(E)

at π_{n+k}^n:
im(E) = ker(H)
```

のように exactness point 単位で追跡する。

可能であれば、この fact を導いた / 使用した `ProofStep` と接続する。

presentation はその structured provenance から生成する。

---

# 20. mathematical dependency の分類

final group result から実際に使用した dependency を抽出する。

分類候補:

```text
proposition
lemma
relation
previous group
EHP exactness
map property
generator fact
order fact
typing / membership fact
```

Phase 93 では分類を必要最小限から開始し、generic ontology を先取りしない。

---

# 21. dependency は actual-use から抽出する

report 用の補題一覧を手書き metadata として別管理しない。

原則:

```text
final ProofStep
↓
premises
↓
premise ProofSteps
↓
inference_rule
↓
recursive dependency graph
```

から actual dependency を抽出する。

これにより:

```text
使った theorem
```

と

```text
近くに存在するが使っていない theorem
```

を区別する。

theorem source name が現在 rule metadata だけでは十分でない場合、Phase 93 の concrete need に沿って最小 metadata を追加する。

---

# 22. 補題・関係式の証明も provenance の一部とする

補題・命題・関係式を単なる label として表示するだけで終わらせない。

その statement に repository 内 proof provenance が存在する場合:

```text
dependency statement
↓
ProofStep
↓
premises
↓
dependency proof
```

を再帰的に辿れることを正式な目標とする。

概念:

```text
final result
├─ lemma A
│  ├─ premise A1
│  ├─ premise A2
│  └─ derivation
├─ relation B
│  └─ derivation
└─ theorem C
   └─ imported fact
```

---

# 23. dependency provenance status

少なくとも次の意味を区別する。

```text
derived
proved
imported
assumed
```

## derived

今回の calculation run の proof search / execution で導出された。

## proved

calculation の開始時点ですでに利用可能だが、repository 内にその statement を支える derivation / ProofStep provenance が存在する。

## imported

文献由来 theorem / explicit fact として登録されているが、内部でその theorem 自体の proof は符号化されていない。

## assumed

今回の calculation の前提として与えられ、内部 derivation を要求しない。

実装時には既存 `ProofRule` / metadata でどこまで判定可能かを Phase 94 で監査してから追加表現を決める。

---

# 24. previous groups の扱い

ユーザー要求:

```text
それ以前の群構造を仮定して
π_{n+k}^n を計算する
```

を、無条件の「全 lower stem assumption」として実装しない。

実際には:

```text
target
↓
proof dependency
↓
actually required previous groups
```

を抽出する。

初期 repository には lower-stem known facts を供給してよいが、report には実際に使用した群だけを出す。

---

# 25. calculation orchestration

Phase 95 の上位 flow:

```text
query
↓
target construction
↓
goal/result lookup
↓
必要なら bounded proof search
↓
group structure result
↓
generator / relation extraction
↓
EHP extraction
↓
dependency extraction
↓
recursive proof provenance
↓
structured calculation result
```

orchestrator が theorem-specific branch を直接 if/else で持つことを避ける。

悪い例:

```text
if n == 5 and k == 3:
  return Prop.5.6
```

目標:

```text
target
→ repository / catalog / theorem rules
→ proof
```

から結果を得る。

---

# 26. presentation layer

structured result から deterministic human-readable report を生成する。

候補 mode:

```text
summary
proof
full
```

summary:

```text
target
group structure
generators
```

proof:

```text
summary
EHP sequence
exactness used
required lemmas / propositions / relations
main proof trace
```

full:

```text
proof
recursive proof of dependencies when available
provenance status
previous-group derivations when available
```

presentation layer は mathematical statements を生成し直さない。

---

# 27. report の代表構造

概念:

```text
Target
  π_{n+k}^n

Result
  group structure

Generators
  names
  orders

Relevant EHP sequence
  terms and maps

Exactness used
  im = ker at concrete terms

Required previous groups
  actual dependencies only

Required propositions / lemmas
  actual dependencies only

Required relations
  actual dependencies only

Proof
  ordered / hierarchical trace

Dependency proofs
  recursively expanded when available

Provenance
  derived / proved / imported / assumed
```

これは output contract の方向性であり、Phase 90-1 前に class hierarchy を固定するものではない。

---

# 28. proof tree と proof DAG

実際の provenance は shared dependency を持つため tree ではなく DAG になりうる。

内部表現では:

```text
shared ProofStep identity
```

を失わない。

presentation では必要に応じて tree-like に展開してもよいが、同一 proof の重複を truth 上の別証明として扱わない。

既存 bounded search の shared dependency reuse semantics と整合させる。

---

# 29. cycle と recursive presentation

proof-search cycle detection と presentation recursion は別問題。

既存 search の cycle-safe semantics を利用する。

dependency report の再帰展開でも:

```text
visited ProofStep identity
```

等により presentation-side infinite recursion を避ける必要がある。

具体的方式は Phase 94/96 の actual graph で決める。

---

# 30. theorem source と proof availability

最終 report では可能な範囲で:

```text
Toda Proposition 5.6
Toda Lemma 5.7
Toda (5.9)
```

等の source identity を表示したい。

ただし source label を inference semantics に混ぜない。

```text
theorem source metadata
!=
theorem truth
```

proof availability も:

```text
source exists
```

と

```text
internal proof exists
```

を区別する。

---

# 31. 0-stem through 7-stem validation

Phase 97 では、既に実装した 0-stem から 7-stem の代表ケースを calculation API の regression とする。

確認:

```text
correct target
correct group structure
correct generator information
correct EHP sequence when used
correct exactness points
correct dependency list
correct recursive proof provenance
correct provenance status
repository non-mutation where applicable
deterministic output
```

「7-stem 全組合せの数学を新規に再証明する Phase」ではなく、既存 proof spine を新しい orchestration layer から再利用できることを確認する Phase とする。

---

# 32. Phase 97 後の数学開発

基本サイクル:

```text
新しい Toda / EHP theorem を実装
↓
新しい π_i^n calculation を追加
↓
calculation orchestrator から実行
↓
不足 representation / inference capability を具体的に発見
↓
必要最小限だけ generic layer を拡張
```

proof-search algorithm を抽象的興味だけで拡張しない。

---

# 33. odd-primary boundary

現時点では odd-primary component を一般的に統合しない。

そのため:

```text
π_{n+k}(S^n)
```

を「完全な群」として report しない。

Toda notation:

```text
π_{n+k}^n
```

を維持する。

将来 odd-primary calculation を追加する場合:

```text
Toda π_i^n query semantics
```

を壊さず、component integration を別 layer / Phase として設計する。

---

# 34. 意図的に未実装の一般化

現時点で追加しない:

```text
unbounded recursive proof search
general backtracking
producer ranking
proof-cost model
best-proof selection
DFS/BFS/A* policy
formal max_depth > 4 coverage
persistent search cache
persistent Proof Repository
generic theorem prover
generic mathematical-equivalence normalization
generic sign algebra
generic Toda-bracket coset algebra
generic symbolic dimension solver
generic map typing solver
generic stable theorem engine
stable ring machinery
```

これらは calculation orchestration または新しい actual theorem から concrete need が生じた場合だけ検討する。

---

# 35. storage boundary

現在の `ProofRepository` は in-memory。

Phase 90-97 で必要なのは:

```text
query
calculation
dependency extraction
presentation
```

であり、persistent storage は必須ではない。

先取りしない:

```text
proof graph serialization
schema migration
persistent search cache
proof replay persistence
database-backed proof repository
```

---

# 36. testing policy

Phase 90 以降も minimum-change principle を維持する。

各 capability で確認する:

```text
representation
input validation
backward compatibility
positive case
negative case
wrong target
provenance
dependency identity
deterministic ordering
repository non-mutation
focused regression
repository-wide regression
git diff --check
```

EHP extraction では追加で:

```text
correct terms
correct maps
correct target position
correct exactness point
```

recursive proof extraction では追加で:

```text
proof available
proof unavailable
imported / assumed distinction
shared dependency reuse
cycle-safe traversal
```

を確認する。

---

# 37. fixture / performance policy

重い deterministic fixture builder が同一 object graph を繰り返し利用する場合:

```python
@lru_cache(maxsize=1)
```

を最初から優先する。

性能確認:

```text
pytest --durations
→ profiler
→ concrete bottleneck
→ minimum change
→ same-machine comparison
→ full regression
```

複数 PC 間で wall-clock time を直接比較しない。

---

# 38. Phase 90-1 audit boundary

次に行う:

```text
Phase 90-1
current π_{n+k}^n calculation representation / orchestration audit
```

実装前に必ず現行 GitHub のコードと関連テストを確認する。

中心確認対象:

```text
TodaPrimaryGroup
TodaEHPSequence
TodaEHPExactnessWindow
group-structure statements
generator / order statements
existing EHP rules
Toda proposition / lemma integration rules
ProofStep provenance
ProofRepository
InferenceRuleCatalog
repository_inference
0-stem through 7-stem representative probes/tests
```

監査結果から:

```text
既存型で足りる部分
不足 representation
不足 provenance
不足 orchestration
```

を分離する。

Phase 90-1 では将来 Phase の class hierarchy や presentation API を先取り実装しない。
