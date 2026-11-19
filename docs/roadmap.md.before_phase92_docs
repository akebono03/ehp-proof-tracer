# EHP Proof Tracer ロードマップ

この文書は今後の capability dependency と Phase 順序を記録する。

過去の詳細な実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明・infrastructure trace は `docs/proof_records.md` を参照する。

---

# 1. 現在地

数学面:

```text
Toda Lemma 5.16 までの concrete proof spine
stable G_0 through G_7
0-stem から 7-stem までの主要な 2-primary / Toda π_i^n 計算材料
```

proof infrastructure:

```text
Proof Repository
→ automatic final-rule selection
→ missing-premise producer analysis
→ multiple producer generation
→ bounded dependency DAG selection
→ max_depth parameterization
→ search / execution diagnostics
→ finite explicit producer retry
→ concrete theorem-instance compatibility filtering
→ selected concrete requested-premise provenance
→ concrete execution-output validation
→ goal ProofStep
```

formal bounded-depth regression:

```text
max_depth = 2
max_depth = 3
max_depth = 4
```

defaults:

```text
max_depth = 2
retry_policy = None
```

Phase 91 までの latest confirmed repository-wide regression:

```text
7154 passed in 100.44s
```

---

# 2. Phase 86 完了境界

Phase 86 で bounded producer search の explicit depth parameterization を完成した。

```text
max_depth=2
max_depth=3
max_depth=4
```

維持:

```text
finite explicit depth bound
cycle-safe search
shared dependency identity reuse
dependency-first execution
diagnostic context
ProofStep provenance
repository non-mutation
default max_depth=2 compatibility
```

---

# 3. Phase 87 完了境界

Phase 87 で producer ambiguity に対する finite retry を追加した。

```text
FiniteProducerRetryPolicy(max_attempts=N)
```

default:

```text
retry_policy=None
→ multiple safe producers
→ AMBIGUOUS_PRODUCER
```

explicit retry:

```text
candidate failure
→ temporary selection rollback
→ next candidate
```

budget exhaustion:

```text
PRODUCER_RETRY_EXHAUSTED
```

Phase 87 は general backtracking を導入しない。

---

# 4. Phase 88 完了境界

Phase 88 の目的は、same conclusion type collision を concrete theorem-instance ambiguity と区別することだった。

代表 collision:

```text
TodaDeltaImageUpToSignStatement

Δ(ι₅)
Δ(ι₉)
Δ(ι₁₇)
```

完成 flow:

```text
known sibling premises
→ bindings
→ concrete requested_statement
→ producer conclusion type
→ goal_compatibility
→ concrete-compatible producer candidates
→ bounded search
→ selected node preserves requested_statement
→ execution validates exact concrete output
```

結果:

```text
false ambiguity
→ Phase 88 filtering で除去

same concrete target に複数 producer
→ true ambiguity
→ Phase 87 finite retry の対象
```

safe lookup と unsafe diagnostic は同じ concrete compatibility semantics を使う。

Phase 88 end-to-end regression:

```text
real Δι5 / Δι9 / Δι17 collision
→ concrete Δι17 request
→ Δι17 only
→ unique selection
→ report SUCCESS
→ execution SUCCESS
→ correct ProofStep provenance
→ repository non-mutation
```

Phase 88 は COMPLETE。

---

# 5. Phase 89 完了境界

Phase 89-1 では post-Phase88 proof-search pressure / true-ambiguity necessity audit を行った。

監査結果:

```text
actual theorem-backed search で
same concrete requested statement に
複数 viable producer が残る実例
→ 現時点では確認されない

Phase 87 finite retry
→ synthetic ambiguity / deeper dependency failure では有効

general backtracking
→ actual theorem-backed need は確認されない

producer ranking / proof cost
→ concrete need は確認されない

registration order が actual proof を変える例
→ 現時点では確認されない

max_depth > 4 が必要な actual theorem-backed path
→ 現時点では確認されない
```

したがって Phase 89 では新しい search algorithm を実装しない。

```text
general backtracking deferred
producer ranking deferred
proof-cost model deferred
depth > 4 generalization deferred
```

Phase 89 は COMPLETE。

---

# 6. 次の中期目標

次の中期目標は、既存の数学表現・定理・proof-search を束ねて、

```text
input:
n, k

target:
π_{n+k}^n
```

から、計算結果だけでなく計算に使った数学的情報全体を取得できるようにすることである。

目標出力:

```text
target
group structure
generators
generator orders
relevant EHP exact sequence
exactness points used
required propositions
required lemmas
required relations
previously known groups actually used
proof trace
proofs of required lemmas / relations when available
distinction between derived / proved / imported / assumed facts
```

重要:

```text
π_{n+k}(S^n)
```

全体を現在の target としない。

現時点では奇素数 primary component を一般的に統合していないため、Toda の記法

```text
π_{n+k}^n
```

を正式な query target とする。

---

# 7. Phase 90：π_{n+k}^n query / calculation architecture

Phase 90 は COMPLETE。

完成した最小 flow:

```text
(n,k)
↓
TodaGroupQuery
↓
TodaPrimaryGroup(n+k,n)
↓
ProofRepository
↓
existing theorem-backed group result lookup
↓
actual ProofStep
```

## Phase 90-1：current calculation representation / orchestration audit

現行 representation を監査し、既存で次が利用可能と確認した。

```text
TodaPrimaryGroup
TodaEHPSequence
TodaEHPExactnessWindow
FreeCyclicGroup
FiniteCyclicGroup
DirectSumGroup
TodaPrimaryGroupZeroStatement
Relation
ProofStep
ProofRepositoryEntry
ProofRepository
```

nonzero group result:

```text
Relation(
  lhs=target,
  rhs=FreeCyclicGroup
      | FiniteCyclicGroup
      | DirectSumGroup,
  relation_type=EQUALITY,
)
```

zero group result:

```text
TodaPrimaryGroupZeroStatement(group=target)
```

generator / order と EHP exactness provenance は既存 proof graph に保持されている一方、query / normalization / recursive provenance / report が不足していることを確認した。

Phase 90-1:

```text
COMPLETE
```

## Phase 90-2：minimal query representation

追加:

```text
toda_group_query.py
TodaGroupQuery(n,k)
```

validation:

```text
n>=1
k>=0
int only
bool rejected
```

target:

```text
TodaGroupQuery(n,k).target
=
TodaPrimaryGroup(n+k,n)
```

責務:

```text
input validation
target construction
```

Phase 90-2 repository-wide regression:

```text
7109 passed in 118.26s
```

Phase 90-2:

```text
COMPLETE
```

## Phase 90-3：known-result lookup

追加:

```text
toda_group_lookup.py
is_toda_group_result_for_target()
find_known_toda_group_results()
```

lookup:

```text
query
→ target
→ repository.entries()
→ entry.step.conclusion
→ Toda group-result shape filter
→ matching entries
```

semantics:

```text
GIVEN / INFERENCE を両方対象
0件 → ()
複数件 → 全件
registration order 保持
winner selection なし
proof search on miss なし
repository mutation なし
```

actual theorem-backed integration:

```text
TodaGroupQuery(4,3)
→ π_7^4=Z{ν₄}⊕Z/4{Eν′}

TodaGroupQuery(4,6)
→ π_10^4=Z/8{ν₄²}

TodaGroupQuery(2,7)
→ π_9^2=0
```

verified:

```text
actual ProofStep identity preserved
actual premises preserved
cross-match absent
repository unchanged
```

Phase 90-3 completion repository-wide regression:

```text
7135 passed in 101.39s
```

`git diff --check`:

```text
clean
```

Phase 90-3:

```text
COMPLETE
```

Phase 90 全体でまだ行わない:

```text
normalized group-result object
generator / order extraction
EHP / exactness extraction
dependency extraction
recursive proof traversal
fact classification
proof search on lookup miss
top-level calculation orchestration
human-readable report
```

---

---

# 8. Phase 91：group structure / generator result

Phase 91 は COMPLETE。

Phase 90 の theorem-backed lookup result を machine-readable に正規化した。

追加:

```text
toda_group_result.py

TodaGroupStructure
TodaGroupResult
```

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

normalization:

```text
normalize_toda_group_result()
```

query integration:

```text
find_normalized_toda_group_results()
```

flow:

```text
TodaGroupQuery
↓
known theorem-backed entry
↓
actual ProofStep
↓
TodaGroupResult
↓
group structure
generators
generator orders
```

actual theorem-backed verification:

```text
π_7^4
=
Z{ν₄}⊕Z/4{Eν′}

→
generators=(ν₄,Eν′)
generator_orders=(None,4)
```

```text
π_10^4
=
Z/8{ν₄²}

→
generators=(ν₄²,)
generator_orders=(8,)
```

```text
π_9^2=0

→
group_structure=None
generators=()
generator_orders=()
```

preserved:

```text
source_entry identity
ProofStep identity
premise provenance
DirectSumGroup summand ordering
repository non-mutation
```

Phase 91-2:

```text
10 passed in 0.90s
repository-wide:
7145 passed in 107.78s
```

Phase 91-3:

```text
9 passed in 6.39s
Phase 90-91 regression:
58 passed in 7.82s
repository-wide:
7154 passed in 100.44s
git diff --check clean
```

Phase 91 ではまだ行わない:

```text
EHP / exactness extraction
dependency extraction
recursive proof traversal
fact classification
proof search on lookup miss
top-level calculation orchestration
presentation
```


# 9. Phase 92：EHP sequence / exactness extraction

既存の:

```text
TodaEHPSequence
TodaEHPExactnessWindow
```

を計算結果と接続する。

## Phase 92-1：relevant EHP window

target の計算で実際に利用した EHP sequence / exactness window を取得する。

## Phase 92-2：group structures in EHP display

EHP sequence の各項に、利用可能な既知群構造を対応付ける。

概念:

```text
A ─P→ B ─E→ π_{n+k}^n ─H→ C ─P→ D
     ↓          ↓            ↓
   known      target        known
```

## Phase 92-3：exactness-use provenance

単に「EHP を使った」と表示せず、

```text
exactness at B:
im(P) = ker(E)

exactness at π_{n+k}^n:
im(E) = ker(H)
```

のように、どの項で完全性を使用したかを proof provenance と接続する。

---

# 10. Phase 93：mathematical dependency extraction

final group result の `ProofStep` から、実際に使用した mathematical dependency を抽出する。

対象:

```text
propositions
lemmas
relations
previously known groups
EHP exactness facts
map properties
generator / order facts
```

重要:

```text
potentially relevant facts
```

ではなく、

```text
actually used facts
```

を出力する。

dependency role も保持する。

例:

```text
Lemma A
→ Relation B を導出するために使用

Relation B
→ generator order を決定するために使用

previous group C
→ EHP exactness の source term として使用
```

---

# 11. Phase 94：recursive proof provenance

補題・命題・関係式が単なる dependency label ではなく、証明が repository に存在する場合はその proof まで再帰的に辿れるようにする。

概念:

```text
final result
├─ dependency A
│  ├─ premise A1
│  ├─ premise A2
│  └─ proof of A
├─ dependency B
│  └─ proof of B
└─ dependency C
   └─ imported / assumed
```

dependency provenance status は少なくとも次を区別する。

```text
derived
proved
imported
assumed
```

意味:

```text
derived
= 今回の calculation run で導出された

proved
= repository 内に derivation / ProofStep provenance がある

imported
= 文献由来 theorem / explicit fact として登録され、内部証明は未符号化

assumed
= この calculation の前提として与えられた
```

同じ statement が複数 role を持つ場合の扱いは Phase 94 の concrete need に基づいて決定する。

---

# 12. Phase 95：calculation orchestration

ここで初めて上位 API を束ねる。

概念:

```text
(n,k)
↓
target π_{n+k}^n
↓
known-result lookup
or
goal-directed bounded proof search
↓
group structure
↓
generator information
↓
EHP information
↓
dependency extraction
↓
recursive provenance
↓
calculation result
```

重要:

```text
calculation orchestration
!= new theorem truth
```

数学固有の theorem knowledge は既存 / 新規の Toda rule に置き、orchestrator に埋め込まない。

---

# 13. Phase 96：human-readable hierarchical report

structured calculation result から人間向け report を生成する。

表示モード候補:

```text
summary
proof
full
```

## summary

```text
target
group structure
generators
```

## proof

```text
summary
+ EHP sequence
+ exactness
+ required lemmas / propositions / relations
+ main proof trace
```

## full

```text
proof
+ recursive dependency proofs
+ previous-group derivations when available
+ provenance status
```

presentation layer は数学的 truth source にしない。

---

# 14. Phase 97：0-stem through 7-stem end-to-end validation

最初の大きな完成点。

0-stem から 7-stem までの既実装数学を代表ケースとして、

```text
(n,k)
→ π_{n+k}^n
→ group structure
→ generators
→ EHP sequence
→ exactness
→ lemmas / propositions / relations
→ recursive proof provenance
```

が一貫して取得できることを確認する。

Phase 97 completion 後に初めて、

```text
7-stem までの既実装範囲について、
n,k を入力し、
π_{n+k}^n の計算結果と証明依存を再構成できる
```

ことを代表 capability とする。

全組合せを一度に一般化するのではなく、実装済み theorem coverage に沿った representative matrix から始める。

---

# 15. Phase 97 後の開発方向

主方向:

```text
8-stem 以降の Toda / EHP 数学を追加
```

従方向:

```text
新しい数学を query orchestration で実行
↓
具体的な不足 capability を発見
↓
必要最小限の representation / inference / search を追加
```

原則:

```text
新しい generic capability を先に作らない
actual theorem-backed pressure から必要性を決める
```

---

# 16. 当面の scope boundary

現時点で対象:

```text
Toda π_i^n
free part where Toda π_i^n definition includes it
2-primary calculations already represented in the project
EHP exactness
Toda propositions / lemmas / relations already encoded
bounded proof search
```

現時点では対象外:

```text
odd-primary components の一般統合
π_{n+k}(S^n) 全体の自動計算
general theorem prover
unbounded recursive search
general backtracking
producer ranking
proof-cost optimization
best-proof selection
generic CAS normalization
generic symbolic dimension solver
generic map typing solver
```

奇素数成分を将来追加する場合も、現在の `π_i^n` query semantics を壊さず別 Phase で拡張する。

---

# 17. presentation / storage の境界

Phase 90-97 で必要になる presentation:

```text
EHP sequence rendering
dependency rendering
hierarchical proof rendering
```

ただし次は先取りしない:

```text
persistent Proof Repository
proof graph serialization
schema migration
persistent search cache
interactive GUI
web visualization
```

最初は in-memory structured result と deterministic text report を優先する。

---

# 18. 性能方針

wall-clock time は複数 PC 間で直接比較しない。

主要 signal:

```text
test count
semantic coverage
provenance coverage
focused regression
repository-wide regression
```

重い deterministic fixture builder が同一 object graph を繰り返し利用する場合:

```python
@lru_cache(maxsize=1)
```

を優先する。

最適化は:

```text
pytest --durations
→ profiler
→ concrete bottleneck
→ minimum change
→ same-machine comparison
→ full regression
```

の順で行う。

---

# 19. 次に着手する Phase

```text
Phase 92-1
current EHP sequence / exactness representation audit
```

最初に現行 GitHub code と actual EHP-related tests を確認する。

中心対象:

```text
TodaEHPSequence
TodaEHPExactnessWindow
TodaSuspensionMap
TodaHopfInvariantMap
TodaDeltaMap
ProofStep
actual EHP-related theorem consequences
```

確認する中心:

```text
existing EHP sequence object から terms / maps を lossless に取得できるか

target π_i^n が sequence / exactness window のどこに位置するかを
既存表現から判定できるか

実際に group proof で使用した EHP exactness window を
ProofStep provenance から特定できるか

structural EHP window と
derived exactness statement をどう区別するか

E / H / Δ map object identity を保持すべきか

normalized TodaGroupResult と
EHP term の known group structure をどう接続するか
```

Phase 92-1 では class を先取りせず、current representation と actual theorem-backed provenance の監査を優先する。

Phase 93 の dependency classification、Phase 94 の recursive proof provenance、Phase 95 の top-level calculation orchestration、Phase 96 の presentation はまだ実装しない。
