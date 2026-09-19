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
report orchestration != proof truth
convenience facade != proof truth
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
↓
top-level calculation-to-report result
↓
thin user-facing convenience facade
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

Phase 97:

```text
toda_calculation_report_result.py
= calculation result と candidate presentation/report の対応表現

toda_calculation_report.py
= calculation -> candidate handling -> presentation -> report orchestration
```

Phase 98:

```text
toda_calculation_facade.py
= raw n,k -> TodaGroupQuery -> existing reporting API の thin facade

TodaCalculationReportResult.report
= FOUND 専用 single report convenience

TodaCalculationReportResult.reports
= 全 report の ordered tuple convenience
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

presentation / renderer / report orchestration / convenience facade は metadata を表示・保持できるが、metadata から数学的 truth を推論してはならない。

---

# 6. Structural equality と object identity

```text
equal ProofStep
!=
same ProofStep identity
```

proof dependency / recursive provenance / presentation / report result では object identity を必要な境界で保持する。

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
automatic mutation by calculation/reporting
```

calculation / explanation / presentation / renderer / report orchestration / convenience facade layer は repository を read-only に利用する。

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

direct lookup は query target と一致する `TodaPrimaryGroupZeroStatement` または equality relation を返す。

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

explicit supported branch のみ扱い、symbolic higher-range auto-instantiation は行わない。

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

---

# 13. Original branch ProofStep recovery

aggregate wrapper から新しい proof を作らず、actual premise の original branch `ProofStep` を回収する。

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

# 15. Calculation orchestration

```text
build_toda_calculation_result(
  repository,
  query,
)
```

direct result が aggregate fallback より優先される。

---

# 16. TodaCalculationResult

```text
0 candidates  → NOT_FOUND
1 candidate   → FOUND
2+ candidates → MULTIPLE_RESULTS
```

multiple candidate を勝手に ranking / selection しない。

---

# 17. EHP extraction

truth source は `TodaGroupResult.proof_step` から actually reachable な `ProofStep` ancestry。

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

---

# 18. Exactness-use provenance

actual exactness `ProofStep`、direct consumer、window identity を保持する。

---

# 19. Flat proof dependency

breadth-first、shortest depth、premise-order stable、identity-based deduplication、cycle-safe。

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

---

# 21. Recursive proof provenance

`ProofStep` identity ごとに1 node、parent/premise edge、premise index、shared dependency を保持する。

---

# 22. Root identity invariant

```text
group_result.proof_step
is dependency_result.root_step
is recursive_provenance.root_step
```

---

# 23. Structured presentation boundary

```text
proof / calculation model
↓
presentation model
↓
renderer
```

主要 object は target / group / generator / EHP / exactness / proof source / readable proof flow / end-to-end candidate presentation。

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

---

# 25. EHP / exactness presentation

```text
exactness.sequence is ehp
```

を維持し、source identity を保持する。

---

# 26. Proof-step source presentation

mathematical role、literature source、repository metadata、calculation goal source を区別する。

---

# 27. Dependency-first readable proof flow

presentation layer で premise-before-parent order を導出し、shared dependency を保持する。

---

# 28. End-to-end presentation

1 candidate について group / EHP / exactness / dependencies / proof flow / source metadata を統合する。

---

# 29. Human-readable rendering

LaTeX / Markdown renderer は presentation model のみを読む。`\Delta` を含む map symbol を一貫して LaTeX 化する。

---

# 30. Proof-step mathematical statement renderer

actual \(\pi_9^5\) では injective \(\Delta\)、zero \(H\)、surjective \(E\)、最終 group relation を出力可能。

---

# 31. Readable proof narrative

dependency-first flow を narrative に利用し、provenance 以上の因果関係を推測しない。

---

# 32. Unified full proof report

presentation-level API:

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

---

# 33. Safe fallback policy

未対応 historical statement は explicit type-name fallback とし、guess prose を生成しない。

---

# 34. TodaCalculationReportCandidate

fields:

```text
source_candidate
presentation
report
```

invariant:

```text
presentation.source_candidate
is source_candidate
```

---

# 35. TodaCalculationReportResult

fields:

```text
calculation_result
candidates
```

`query`、`target`、`status` は `calculation_result` から委譲。

candidate alignment:

```text
report_result.candidates[i].source_candidate
is report_result.calculation_result.candidates[i]
```

Phase 98 convenience:

```text
report
reports
```

---

# 36. Top-level calculation-to-report orchestration

一般 API:

```text
build_toda_calculation_report_result(
  repository,
  query,
)
```

single-FOUND query-object convenience:

```text
build_toda_found_calculation_report_result(
  repository,
  query,
)
```

raw input facade:

```text
build_toda_report(
  repository,
  n,
  k,
)
```

`build_toda_report()` は `TodaGroupQuery(n,k)` を生成し、既存 general reporting API に委譲するだけである。

---

# 37. NOT_FOUND / FOUND / MULTIPLE_RESULTS semantics

```text
NOT_FOUND
→ candidates = ()
→ reports = ()
→ report は ValueError

FOUND
→ candidate 1件
→ report はその candidate.report
→ reports = (report,)

MULTIPLE_RESULTS
→ 全 candidate を calculation order で保持
→ reports は全 candidate.report を同じ順序で保持
→ report は ValueError
```

ranking / preferred result / silent first-candidate selection は行わない。

---

# 38. User-facing convenience boundary

Phase 98 後の最短 user-facing path:

```text
raw n,k
↓
build_toda_report()
↓
TodaCalculationReportResult
↓
report / reports
```

重要な境界:

```text
build_toda_report()
= query construction + delegation only

report
= FOUND-only convenience

reports
= lossless ordered projection of candidate.report
```

`NOT_FOUND` の固定 human-facing message は core model に持たせない。

---

# 39. Repository non-mutation

Phase 90–98 の query / calculation / explanation / presentation / renderer / report orchestration / convenience layer は repository を mutate しない。

---

# 40. Representative top-level coverage

\[
\pi_7^4,\quad
\pi_9^5,\quad
\pi_{10}^4,\quad
\pi_{11}^5,\quad
\pi_9^2,\quad
\pi_{12}^5
\]

を raw `n,k` facade から `result.report / result.reports` まで validation 済み。

---

# 41. 現在の明示的境界

```text
fixed NOT_FOUND human message in core model
CLI / Web UI
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

# 42. Phase 98 completion boundary

Phase 98 は user-facing convenience の最小追加に限定。

追加 capability:

```text
raw n,k facade
actual-use facade validation
FOUND-only result.report
ordered result.reports
representative shortest-path validation
```

追加しなかったもの:

```text
new facade class
new proof logic
new calculation logic
new provenance schema
NOT_FOUND message
candidate ranking
silent selection
```

formal status:

```text
Phase 98
→ COMPLETE
```

---

# 43. Verification policy

Phase 98-6 完了時:

```text
focused:
8 passed in 8.64s

Phase 98 related:
27 passed in 9.94s

repository-wide:
7643 passed in 123.73s

git diff --check:
clean
```

---

# 44. 文書運用

`README.md` は current status、`docs/design.md` は current architecture、`docs/roadmap.md` は future plan、`docs/development_log.md` と `docs/proof_records.md` は index として維持する。

詳細 archive は原則追記型とする。
