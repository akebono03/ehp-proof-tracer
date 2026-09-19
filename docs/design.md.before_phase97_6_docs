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
rendered prose != proof truth
```

将来 Phase の一般化を先取りせず、既存 API・既存 provenance・既存 tests を不必要に壊さない。

---

# 2. 現在のレイヤー構造

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
structured presentation
↓
human-readable renderer
↓
unified proof report
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
= bounded producer search / diagnostics / selected-path execution

homotopy_groups.py
= homotopy / Toda / EHP structural data

toda_rules.py
= Toda-specific theorem knowledge
```

Phase 90 以降:

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
= flat dependency / role classification / recursive provenance

toda_explanation.py
= group / EHP / dependency / recursive provenance integration
```

Phase 96:

```text
toda_presentation.py
= target / group / generator / order presentation

toda_ehp_presentation.py
= EHP / exactness presentation

toda_proof_presentation.py
= proof-step role / literature / repository / goal-source presentation

toda_proof_flow_presentation.py
= dependency-first readable proof flow

toda_end_to_end_presentation.py
= calculation candidate から end-to-end presentation への統合

toda_human_readable_renderer.py
= target / group / EHP の LaTeX と base Markdown report

toda_proof_narrative_renderer.py
= proof-step mathematical statement と readable narrative

toda_full_proof_report_renderer.py
= base report と narrative の unified report
```

---

# 4. Toda group semantics

`TodaGroupQuery(n, k)` は

\[
\pi_{n+k}^n
\]

を query する。

target:

```text
TodaPrimaryGroup(
  group_dimension=n+k,
  sphere_dimension=n,
)
```

`TodaPrimaryGroup(i,n)` は Toda (4.3) の \(\pi_i^n\) を表す historical class name であり、all-primary ordinary \(\pi_i(S^n)\) calculator ではない。

---

# 5. Proof truth と metadata

proof truth の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata であり、数学的 truth 判定そのものには使用しない。

presentation / renderer は metadata を表示できるが、metadata から数学的 truth を推論してはならない。

---

# 6. Structural equality と object identity

```text
equal ProofStep
!=
same ProofStep identity
```

proof dependency / recursive provenance / presentation では `ProofStep` object identity を保持する。

equal-but-distinct `ProofStep` は必要に応じて別 provenance として扱う。

---

# 7. Proof Repository

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
persistent storage
presentation
rendering
automatic mutation by calculation
```

calculation / explanation / presentation / renderer layer は repository を read-only に利用する。

---

# 8. Bounded proof search

安全 invariant:

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

現在の bounded search は concrete goal が既知であることを前提とする。

---

# 9. Direct theorem-backed lookup

direct lookup は query target と一致する:

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

を返す。

複数一致は registration order を保持し、silent selection はしない。

---

# 10. TodaGroupResult

fields:

```text
target
group_structure
generators
generator_orders
source_entry
proof_step
```

order:

```text
None = infinite
positive int = finite
```

zero group:

```text
group_structure = None
generators = ()
generator_orders = ()
```

invariant:

```text
proof_step is source_entry.step
```

---

# 11. Aggregate theorem fallback

direct lookup miss 時:

```text
repository entries
↓
supported aggregate statement
↓
query.target と一致する concrete branch
↓
TodaCalculationGoalCandidate
```

explicit supported branch のみ扱い、generic dataclass recursive scan や symbolic higher-range auto-instantiation は行わない。

---

# 12. Calculation goal source

aggregate-derived candidate:

```text
TodaCalculationGoalSource(
  source_entry,
  branch_name,
)
```

nested branch は dotted path を許す。

例:

```text
nu_squared_finite_dimensional.pi11_5_group_relation
```

---

# 13. Original branch ProofStep recovery

aggregate wrapper から新しい proof を作らず、actual premise の original branch `ProofStep` を回収する。

```text
branch path
→ branch statement
→ premise.conclusion == branch statement
→ original ProofStep identity
```

premise index を hard-code しない。

---

# 14. Recovered branch normalization

recovered branch 用に ephemeral `ProofRepositoryEntry` を作るが repository へ register しない。

```text
goal_source
→ original aggregate provenance

group_result.source_entry
→ ephemeral normalization adapter

group_result.proof_step
→ original branch proof
```

---

# 15. Top-level calculation orchestration

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
│  → direct results
│
└─ none
   ↓
   aggregate discovery
   ↓
   branch recovery
   ↓
   branch normalization
   ↓
   explanation build
   ↓
   TodaCalculationResult
```

direct result が aggregate fallback より優先される。

---

# 16. TodaCalculationResult

```text
0 candidates → NOT_FOUND
1 candidate  → FOUND
2+ candidates → MULTIPLE_RESULTS
```

multiple candidate を勝手に ranking / selection しない。

---

# 17. EHP extraction

truth source:

```text
TodaGroupResult.proof_step
↓
actually reachable ProofStep ancestry
```

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

repository 全体から関連しそうな fact を集める方式ではない。

---

# 18. Exactness-use provenance

保持するもの:

```text
actual exactness ProofStep
actual direct consumer ProofSteps
window identity
```

presentation でも source identity を保持する。

---

# 19. Flat proof dependency

```text
breadth-first traversal
shortest depth
premises-order stable
identity-based deduplication
cycle-safe
```

non-`ProofStep` premise は dependency node に含めない。

---

# 20. Dependency role classification

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

first-class conclusion type と `RelationType` を中心に分類し、class-name substring 推測を避ける。

---

# 21. Recursive proof provenance

```text
TodaProofNode
TodaProofEdge
TodaRecursiveProofProvenanceResult
```

node は `ProofStep` identity ごとに1つ。

edge は:

```text
parent_step
premise_step
premise_index
```

shared dependency は node を複製せず、複数 incoming edge を保持する。

---

# 22. Root identity invariant

```text
group_result.proof_step
is dependency_result.root_step
is recursive_provenance.root_step
```

aggregate fallback 後も root は original branch `ProofStep`。

---

# 23. Structured presentation boundary

```text
proof / calculation model
↓
presentation model
↓
renderer
```

主要 object:

```text
TodaCalculationPresentationCandidate
TodaTargetPresentation
TodaGeneratorPresentation
TodaGroupStructurePresentation
TodaGroupResultPresentation
TodaEHPSequencePresentation
TodaEHPExactnessPresentation
TodaProofStepPresentation
TodaReadableProofFlowPresentation
TodaEndToEndCandidatePresentation
```

---

# 24. Mathematical atomic presentation

group structure:

```text
ZERO
FREE_CYCLIC
FINITE_CYCLIC
DIRECT_SUM
```

generator order:

```text
INFINITE
FINITE
```

Phase 91 の raw `None` order は semantic `INFINITE` に変換する。

---

# 25. EHP / exactness presentation

end-to-end presentation 内では:

```text
exactness.sequence is ehp
```

を維持。

source EHP result / exactness provenance identity を保持する。

---

# 26. Proof-step source presentation

区別するもの:

```text
mathematical role
literature source
repository metadata
calculation goal source
```

aggregate goal-source metadata を internal dependency へ伝播させない。

---

# 27. Dependency-first readable proof flow

Phase 94 recursive provenance の BFS order は変更しない。

presentation layer で cycle-safe DFS/postorder により:

```text
premise before parent
```

を導出。

shared dependency:

```text
incoming_use_count
is_shared_dependency
```

を保持する。

---

# 28. End-to-end presentation

1 candidate について:

```text
calculation candidate
group
EHP
exactness
dependencies
proof flow
source metadata
```

を統合。

代表 target:

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5.
\]

---

# 29. Human-readable rendering

主要 API:

```text
render_toda_expression_latex()
render_toda_target_latex()
render_toda_group_structure_latex()
render_toda_group_result_latex()
render_toda_ehp_sequence_latex()
render_toda_end_to_end_markdown()
```

\(\Delta\) は `\Delta` として LaTeX 正規化する。

---

# 30. Proof-step mathematical statement renderer

actual \(\pi_9^5\) で:

\[
\Delta:\pi_9^9\to\pi_7^4
\]

が injective、

\[
H:\pi_9^5\to\pi_9^9
\]

が zero map、

\[
E:\pi_8^4\to\pi_9^5
\]

が surjective、

\[
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}
\]

を出力可能。

未対応 statement type は type-name fallback とする。

---

# 31. Readable proof narrative

dependency-first flow の順序を narrative に使用する。

renderer は provenance 以上の因果関係を推測しない。

generic `MAP_PROPERTY` lead は:

```text
From the preceding statements
```

と中立化している。

---

# 32. Unified full proof report

main API:

```text
render_toda_full_proof_report_markdown(
  presentation,
)
```

sections:

```text
Result
Source
EHP sequence
Exactness
Proof flow
Readable proof narrative
```

`Proof flow` は provenance-oriented、`Readable proof narrative` は human-facing であり責務が異なる。

---

# 33. Safe fallback policy

未対応 historical aggregate statement は:

```text
`TodaProp56FiniteDimensionalStatement`
```

のように explicit fallback。

guess prose は生成しない。

user-facing report に Python object repr を漏らさない。

---

# 34. Repository non-mutation

Phase 90–96 の query / calculation / explanation / presentation / renderer layer は repository を mutate しない。

---

# 35. Representative coverage

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5
\]

について:

```text
direct sum / finite cyclic / zero
outer / nested aggregate branch
generator orders
EHP provenance
flat / recursive provenance
dependency-first flow
LaTeX rendering
mathematical statement rendering
readable narrative
unified report
deterministic rendering
repository non-mutation
```

を regression 済み。

---

# 36. 現在の明示的境界

```text
symbolic higher-range theorem instantiation
target-only unknown-RHS goal generation
target-only bounded-search fallback
detailed calculation failure taxonomy
proof ranking / best-proof selection
unbounded search
persistent proof cache
full prose rendering for every historical statement type
generic theorem proving
odd-primary full integration
all-primary ordinary sphere-homotopy calculator
```

---

# 37. Phase 97 との境界

Phase 96 までで:

```text
TodaGroupQuery
→ TodaCalculationResult
→ candidate
→ presentation
→ full proof report
```

が揃った。

Phase 97 は user-facing orchestration のみを扱う。

```text
(n, k)
→ calculation
→ candidate handling
→ presentation
→ report
```

presentation semantics や proof truth を再実装しない。

---

# 38. Verification policy

Phase 96-12 完了時:

```text
focused / related:
75 passed in 6.50s

repository-wide:
7577 passed in 43.70s

git diff --check:
clean
```

---

# 39. 文書運用

```text
README.md
= current project status

docs/design.md
= current architecture / semantics / invariants

docs/roadmap.md
= future-oriented plan

docs/development_log.md
= history index

docs/development_log/
= chronological archive

docs/proof_records.md
= proof-record index

docs/proof_records/
= mathematical / infrastructure archive

docs/code_reference.md
= code navigation
```

`development_log` と `proof_records` の詳細 archive は原則追記型とする。
