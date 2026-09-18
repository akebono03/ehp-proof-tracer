# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、invariant、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

中心原則は次である。

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
```

将来 Phase の一般化を先取りせず、既存 API・既存 provenance・既存 tests を不必要に壊さない。

---

# 2. 現在のレイヤー構造

全体は概ね次の layer に分かれる。

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
structured calculation result
↓
future presentation layer
```

上位 layer は下位 layer の proof truth を変更しない。

---

# 3. 主要モジュールの責務

```text
expression.py
= 式の structural representation

proof.py
= generic ProofStep / inference mechanics

proof_repository.py
= in-memory proof entry catalog

rule_catalog.py
= inference-rule registration / search metadata

repository_inference.py
= bounded producer search
  diagnostics
  selected-path execution

homotopy_groups.py
= homotopy / Toda / EHP structural data

toda_rules.py
= Toda-specific theorem knowledge
```

Phase 90 以降の calculation / explanation layer:

```text
toda_group_query.py
= query validation / target construction

toda_group_lookup.py
= direct theorem-backed result lookup

toda_group_result.py
= normalized group result

toda_calculation_goal.py
= calculation-goal candidate / source representation

toda_calculation_goal_extraction.py
= concrete aggregate branch extraction

toda_calculation_goal_discovery.py
= repository-wide aggregate candidate discovery

toda_calculation_goal_recovery.py
= original branch ProofStep recovery

toda_calculation_goal_normalization.py
= recovered branch -> TodaGroupResult adapter

toda_calculation_result.py
= top-level calculation result representation

toda_calculation.py
= direct lookup + aggregate fallback orchestration

toda_ehp_result.py
= EHP sequence / window result representation

toda_ehp_extraction.py
= actual proof ancestry から EHP extraction

toda_ehp_group_enrichment.py
= EHP term と known group result の接続

toda_ehp_exactness_provenance.py
= exactness-use provenance

toda_proof_dependency.py
= flat dependency
  role classification
  recursive proof provenance

toda_explanation.py
= group / EHP / dependency / recursive provenance integration
```

---

# 4. Toda group semantics

`TodaGroupQuery(n, k)` は

\[
\pi_{n+k}^n
\]

を query する。

target は:

```text
TodaPrimaryGroup(
  group_dimension=n+k,
  sphere_dimension=n,
)
```

である。

`TodaPrimaryGroup(i,n)` は Toda (4.3) の \(\pi_i^n\) を表す historical class name であり、一般の all-primary ordinary \(\pi_i(S^n)\) calculator ではない。

query object の責務は:

```text
input validation
target construction
```

である。

責務ではない:

```text
proof search
group computation
presentation
```

---

# 5. Proof truth と metadata

proof truth の中心は:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

である。

`ProofRepositoryEntry` の:

```text
key
phase
theorem
```

は provenance metadata であり、数学的 truth 判定そのものには使用しない。

---

# 6. Structural equality と object identity

dataclass equality は syntax tree の一致を表す。

```text
equal
→ structurally equal
```

しかし provenance では:

```text
equal ProofStep
!=
same ProofStep identity
```

である。

そのため proof dependency / recursive provenance では `ProofStep` object identity を保持する。

equal-but-distinct `ProofStep` は、必要に応じて別 provenance として扱う。

---

# 7. Proof Repository

`ProofRepository` の責務:

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
persistent storage
presentation
automatic mutation by calculation
```

calculation / explanation layer は repository を read-only に利用する。

---

# 8. Bounded proof search

現在維持する安全 invariant:

```text
finite max_depth
finite retry
fixed-point-safe producer opt-in
concrete theorem-instance compatibility
cycle detection
shared dependency reuse
dependency-first execution
selected path = executed path
failed retry rollback
concrete producer-output validation
ProofStep provenance
repository non-mutation
```

現在の bounded search は**concrete goal が既知であること**を前提とする。

したがって target group だけから未知の RHS を推測して proof goal を生成する責務は持たない。

---

# 9. Direct theorem-backed lookup

direct lookup は repository に登録された top-level entry のうち、query target と一致する group result を返す。

対象:

```text
TodaPrimaryGroupZeroStatement
Relation(
  EQUALITY,
  lhs=target,
  rhs=FreeCyclicGroup
      | FiniteCyclicGroup
      | DirectSumGroup
)
```

複数一致は registration order を保持したまま全件返す。

silent selection はしない。

---

# 10. TodaGroupResult

`TodaGroupResult` は theorem-backed group result の normalized representation である。

fields:

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
group_structure = None
generators = ()
generator_orders = ()
```

identity invariant:

```text
proof_step is source_entry.step
```

---

# 11. Aggregate theorem fallback

direct lookup が miss した場合、現在の calculation orchestration は concrete aggregate theorem branch を探索する。

流れ:

```text
repository entries
↓
supported aggregate statement
↓
query.target と一致する concrete branch
↓
TodaCalculationGoalCandidate
```

現在は explicit supported aggregate type / branch のみ扱う。

generic dataclass recursive scan は行わない。

symbolic higher-range branch の自動 instantiation も行わない。

---

# 12. Calculation goal source

aggregate-derived candidate は:

```text
TodaCalculationGoalSource
```

を持つ。

内容:

```text
source_entry
branch_name
```

`branch_name` は nested aggregate の場合 dotted path を許す。

例:

```text
nu_squared_finite_dimensional.pi11_5_group_relation
```

これは aggregate theorem provenance を表す。

---

# 13. Original branch ProofStep recovery

aggregate branch から新しい proof を作らず、aggregate `ProofStep.premises` 内にすでに存在する original branch `ProofStep` を回収する。

回収規則:

```text
branch path を statement field として解決
↓
対応 branch statement を得る
↓
premise.conclusion == branch statement
↓
original ProofStep identity を保持
```

premise index を hard-code しない。

同一 object の重複は identity deduplication する。

equal-but-distinct steps は複数候補として保持する。

---

# 14. Recovered branch normalization

`normalize_toda_group_result()` は `ProofRepositoryEntry` を要求する。

recovered branch は top-level repository entry ではないため、normalization adapter として ephemeral `ProofRepositoryEntry` を構築する。

重要:

```text
ephemeral entry
→ repository に register しない

ephemeral_entry.step
is original recovered branch ProofStep
```

aggregate provenance は `goal_source` に別途保持する。

したがって:

```text
goal_source
→ original aggregate provenance

group_result.source_entry
→ ephemeral normalization adapter

group_result.proof_step
→ original branch proof
```

となる。

---

# 15. Top-level calculation orchestration

主要 API:

```text
build_toda_calculation_result(
  repository,
  query,
)
```

semantics:

```text
direct lookup
├─ one or more results
│  → direct results を返す
│  → aggregate fallback は起動しない
│
└─ no direct result
   ↓
   aggregate discovery
   ↓
   branch recovery
   ↓
   branch normalization
   ↓
   explanation build
   ↓
   final TodaCalculationResult
```

direct result が常に aggregate fallback より優先される。

---

# 16. TodaCalculationResult

status:

```text
NOT_FOUND
FOUND
MULTIPLE_RESULTS
```

cardinality semantics:

```text
0 candidates
→ NOT_FOUND

1 candidate
→ FOUND

2+ candidates
→ MULTIPLE_RESULTS
```

multiple candidate を勝手に ranking / selection しない。

---

# 17. TodaCalculationCandidate provenance

fields:

```text
group_result
explanation
goal_source
```

direct result:

```text
goal_source = None
```

aggregate-derived result:

```text
goal_source = original aggregate provenance
```

invariant:

```text
explanation.group_result is group_result
```

---

# 18. EHP extraction

EHP extraction の truth source は:

```text
TodaGroupResult.proof_step
↓
actually reachable ProofStep ancestry
```

である。

reachable ancestry から actual `TodaProp42ExactnessStatement` を抽出し、contiguous EHP chain を構成する。

代表:

\[
\pi_{10}^9
\xrightarrow{\Delta}
\pi_8^4
\xrightarrow{E}
\pi_9^5
\xrightarrow{H}
\pi_9^9
\xrightarrow{\Delta}
\pi_7^4.
\]

repository 全体から関係ありそうな EHP fact を集める方式ではない。

---

# 19. Exactness-use provenance

exactness provenance は:

```text
actual exactness ProofStep
actual direct consumer ProofSteps
```

を保持する。

EHP window object identity も可能な限りそのまま保持する。

---

# 20. Flat proof dependency

flat dependency representation は:

```text
TodaProofDependency
TodaProofDependencyResult
```

を用いる。

semantics:

```text
breadth-first traversal
shortest depth
premises-order stable
identity-based deduplication
cycle-safe
```

non-`ProofStep` premise は dependency node に含めない。

---

# 21. Dependency role classification

current role categories:

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

主に first-class conclusion type と `RelationType` から分類する。

theorem name や class-name substring に依存した推測は避ける。

---

# 22. Recursive proof provenance

recursive representation:

```text
TodaProofNode
TodaProofEdge
TodaRecursiveProofProvenanceResult
```

node identity:

```text
one node per ProofStep identity
```

edge:

```text
parent_step
premise_step
premise_index
```

`premise_index` は original unfiltered `ProofStep.premises` index を保持する。

shared dependency は node を複製せず、複数 incoming edge を保持する。

cycle / self-cycle は traversal を停止しつつ edge 自体は保持できる。

---

# 23. Root identity invariant

representative explanation では:

```text
group_result.proof_step
is dependency_result.root_step
is recursive_provenance.root_step
```

を維持する。

aggregate fallback 後でも root は aggregate wrapper step ではなく original branch `ProofStep` である。

---

# 24. Repository non-mutation

Phase 90–95 の query / calculation / explanation layer は repository を mutate しない。

特に:

```text
aggregate discovery
branch recovery
ephemeral normalization
EHP extraction
dependency extraction
recursive provenance extraction
```

はいずれも read-only operation である。

---

# 25. 現在の representative end-to-end coverage

actual aggregate entries だけから top-level API で regression 済み:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

これにより以下を確認している。

```text
direct sum
finite cyclic group
zero group
outer aggregate branch
nested aggregate branch
generator orders
original branch identity
aggregate provenance
EHP provenance
flat dependencies
recursive provenance
repository non-mutation
```

---

# 26. 現在の明示的境界

未実装だが、現在の Phase 95 correctness を壊す未完ではないもの:

```text
symbolic higher-range theorem instantiation
target-only unknown-RHS goal generation
target-only bounded-search fallback
detailed calculation failure taxonomy
proof ranking
best-proof selection
unbounded search
persistent proof cache
generic theorem proving
odd-primary full integration
all-primary ordinary sphere-homotopy calculator
```

これらは別 capability として deferred とする。

---

# 27. Phase 96 との境界

Phase 96 は human-readable explanation / proof report layer とする。

入力は Phase 95 までの structured result。

```text
structured proof truth
↓
presentation
```

とし、presentation layer が proof truth を変更してはならない。

Phase 96 で扱いうるもの:

```text
human-readable target summary
group structure
generator / order display
EHP sequence display
exactness-use explanation
required lemma / proposition summary
recursive proof trace presentation
literature reference presentation
Markdown / console / LaTeX report
```

Phase 95 schema を prose generation の都合で不必要に変更しない。

---

# 28. Verification policy

各 Phase completion は最低限:

```text
focused pytest
related regression
repository-wide pytest
git diff --check
```

で確認する。

Phase 95-20 時点の最新確認:

```text
focused / related:
106 passed in 4.40s

repository-wide:
7419 passed in 38.11s

git diff --check:
clean
```

wall-clock time は machine-dependent。

---

# 29. 文書運用

```text
README.md
= current project status

docs/design.md
= current architecture / semantics / invariants

docs/roadmap.md
= future-oriented plan

docs/development_log.md
= development-history index

docs/development_log/
= chronological archive

docs/proof_records.md
= proof-record index

docs/proof_records/
= mathematical / infrastructure record archive

docs/code_reference.md
= code navigation
```

`development_log` と `proof_records` の詳細 archive は原則追記型とする。

`design.md` と `roadmap.md` は current state に合わせて古い計画を削除・訂正する。
