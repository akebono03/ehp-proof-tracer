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
production repository assembly != theorem truth
CLI != proof truth
exploration result != new theorem truth
```

将来 Phase の一般化を先取りせず、既存 API・既存 provenance・既存 tests を不必要に壊さない。

---

# 2. 現在のレイヤー構造

計算・証明経路:

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
repository-explicit convenience facade
↓
standard production repository facade
↓
minimal CLI
```

Phase 99 の探索経路:

```text
repository theorem conclusions
↓
structural generator containment
↓
generator occurrence path extraction
↓
repository-level occurrence lookup
↓
semantic role classification
↓
element-centered exploration
↓
grouped presentation
↓
Markdown renderer
↓
one-shot exploration facade
```

上位 layer は下位 layer の proof truth を変更しない。

---

# 3. 主要モジュールの責務

基礎:

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

計算・provenance:

```text
toda_group_query.py
toda_group_lookup.py
toda_group_result.py
toda_calculation_goal.py
toda_calculation_goal_extraction.py
toda_calculation_goal_discovery.py
toda_calculation_goal_recovery.py
toda_calculation_goal_normalization.py
toda_calculation_result.py
toda_calculation.py
toda_ehp_result.py
toda_ehp_extraction.py
toda_ehp_group_enrichment.py
toda_ehp_exactness_provenance.py
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
toda_calculation_report_result.py
toda_calculation_report.py
```

user-facing calculation:

```text
toda_calculation_facade.py
= repository-explicit raw n,k facade
  + production repository-free one-shot facade

standard_production_repository.py
= standard theorem-backed ProofRepository assembly

main.py
= minimal CLI boundary
```

Phase 99 exploration:

```text
structural_containment.py
repository_element_lookup.py
generator_occurrence_roles.py
repository_element_exploration.py
repository_element_presentation.py
repository_element_renderer.py
repository_element_facade.py
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

valid domain:

```text
n > 0
k >= 0
```

`TodaPrimaryGroup(i,n)` は historical class name であり、all-primary ordinary \(\pi_i(S^n)\) calculator を意味しない。

---

# 5. Proof truth と metadata

proof truth の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata であり、数学的 truth 判定そのものには使用しない。

presentation、renderer、report orchestration、convenience facade、production repository assembly、CLI、exploration facade は proof truth を追加してはならない。

---

# 6. Structural equality と object identity

```text
equal ProofStep
!=
same ProofStep identity
```

proof dependency / recursive provenance / presentation / report result では object identity を必要な境界で保持する。

generator exploration では generator equality により containment を判定する一方、repository entry と actual `ProofStep` provenance を保持する。

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
theorem truth generation
persistent storage
presentation
rendering
CLI messaging
automatic mutation by calculation/reporting/exploration
```

query / calculation / presentation / reporting / exploration は repository を read-only に利用する。

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

direct lookup は query target と一致する theorem-backed group result を返す。

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

# 12. Calculation goal provenance

aggregate-derived candidate は source entry と branch path を保持する。

branch normalization のための ephemeral adapter は repository へ register しない。

---

# 13. Calculation orchestration

```text
build_toda_calculation_result(
  repository,
  query,
)
```

direct result が aggregate fallback より優先される。

status:

```text
0 candidates  → NOT_FOUND
1 candidate   → FOUND
2+ candidates → MULTIPLE_RESULTS
```

multiple candidate を勝手に ranking / selection しない。

---

# 14. EHP / exactness provenance

truth source は final theorem-backed `ProofStep` から actually reachable な ancestry である。

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

actual exactness step、consumer、window identity を保持する。

---

# 15. Flat / recursive proof provenance

flat dependency は breadth-first、shortest depth、premise-order stable、identity-based deduplication、cycle-safe。

recursive provenance は `ProofStep` identity ごとに1 node とし、premise edge、premise index、shared dependency を保持する。

root invariant:

```text
group_result.proof_step
is dependency_result.root_step
is recursive_provenance.root_step
```

---

# 16. Presentation boundary

```text
proof / calculation model
↓
presentation model
↓
renderer
```

presentation は proof truth を変更しない。

未対応 historical statement は explicit type-name fallback とし、推測で mathematical prose を生成しない。

---

# 17. Reporting result semantics

`TodaCalculationReportResult` は calculation candidate と report candidate の identity/order alignment を保持する。

```text
NOT_FOUND
→ candidates = ()
→ reports = ()
→ report は ValueError

FOUND
→ candidate 1件
→ report はその candidate.report

MULTIPLE_RESULTS
→ 全 candidate を calculation order で保持
→ reports は同順序
→ report は ValueError
```

---

# 18. Repository-explicit user-facing facade

```text
build_toda_report(
  repository,
  n,
  k,
)
```

は `TodaGroupQuery` と既存 reporting API を compose する thin facade である。

proof logic、normalization、presentation、rendering を再実装しない。

---

# 19. Standard production repository

Phase 100 の production path は、

```text
build_standard_production_proof_repository()
```

で標準 theorem-backed repository を構築する。

目的:

```text
caller-specific manual bootstrap
↓
standard production assembly
```

この builder は既存 theorem-backed construction を compose する orchestration layer であり、新しい theorem truth を作らない。

production repository は通常の `ProofRepository` と同じ lookup / provenance semantics を持つ。

---

# 20. Production repository-free facade

```text
build_standard_toda_report(
  n,
  k,
)
```

は、

```text
standard production repository
↓
build_toda_report(repository, n, k)
↓
TodaCalculationReportResult
```

を compose する。

重要な互換性:

```text
build_toda_report(repository, n, k)
```

は既存 API として残す。

production facade のために既存 API の意味論を変更しない。

---

# 21. CLI boundary

`main.py` は minimal CLI entry point である。

```text
python main.py n k
```

責務:

```text
argument parsing
CLI semantic validation
production facade invocation
report output
NOT_FOUND message
exit code
```

責務ではない:

```text
theorem proof
repository bootstrap detail
group normalization
EHP extraction
presentation construction
proof ranking
generator string resolution
subcommand framework
```

---

# 22. CLI input validation

CLI は repository 構築前に

\[
n>0,\qquad k\ge0
\]

を検証する。

invalid input:

```text
syntax/type invalid
or
n <= 0
or
k < 0
↓
argparse error
↓
exit 2
↓
production facade is not called
```

通常の入力ミスで traceback を出さない。

core `TodaGroupQuery` validation は引き続き独立して保持する。CLI validation は core validation の代替ではなく user-facing boundary guard である。

---

# 23. CLI result and exit semantics

```text
FOUND
→ report(s) を stdout
→ exit 0

MULTIPLE_RESULTS
→ candidate order で全 reports を stdout
→ exit 0

NOT_FOUND
→ explicit not-found message
→ exit 1

invalid input
→ argparse error
→ exit 2
```

`MULTIPLE_RESULTS` で silent first-candidate selection はしない。

`if __name__ == "__main__"` boundary により `import main` は CLI を実行しない。

---

# 24. Generator exploration

Phase 99 exploration は `GeneratorSymbol` を既知入力として受け取る。

same entry 内でも different structural path は別 occurrence とする。

repository order、presentation order、Markdown order を保持し、repository を mutate しない。

この探索は theorem truth を追加しない。

---

# 25. Production path invariants

Phase 100-12 closure 後の重要 invariant:

```text
CLI
→ production facade
→ standard production repository
→ repository-explicit report facade
→ existing calculation/report stack
```

各層は下位 logic を複製しない。

```text
CLI != calculation engine
production facade != theorem engine
production repository assembly != theorem truth
report renderer != proof truth
```

---

# 26. Repository non-mutation

query / calculation / explanation / presentation / renderer / report orchestration / convenience / exploration layer は repository を mutate しない。

standard production repository builder は新しい repository を構築するが、calculation/report invocation が既存 repository を mutate することを意味しない。

---

# 27. 現在の明示的境界

```text
string -> GeneratorSymbol parser / resolver
free-form element query
element-exploration CLI subcommands
Web UI
general composition evaluation
general Toda bracket solver
coset / indeterminacy calculator
automatic applicable-lemma discovery
derived-result enumeration beyond current repository lookup semantics
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

# 28. Phase 100-12 production closure

Phase 100-12B:

```text
standard production repository integration
```

Phase 100-12C-1:

```text
minimal production one-shot facade integration
```

Phase 100-12C-2:

```text
minimal CLI integration
```

Phase 100-12C-3:

```text
CLI boundary / error-path / direct invocation audit
```

Phase 100-12C-4:

```text
minimal CLI semantic-validation hardening
```

Phase 100-12D:

```text
production user-facing path final closure audit
documentation integration
```

closure path:

```text
raw n,k
↓
CLI or direct Python API
↓
semantic validation
↓
standard production repository
↓
build_toda_report()
↓
calculation / provenance / presentation
↓
human-readable proof report
```

---

# 29. Verification policy

Phase 100-12 closure verification:

```text
Phase 100-12C-1 related:
38 passed in 9.07s

Phase 100-12C-4 related:
21 passed in 9.74s

repository-wide:
8010 passed in 179.65s

git diff --check:
clean
```

direct CLI probes:

```text
python main.py 5 7
python main.py 20 20
python main.py 0 7
python main.py -1 7
python main.py 5 -1
python main.py 1 0
python main.py --help
```

---

# 30. 文書運用

`README.md` は current status、`docs/design.md` は current architecture、`docs/roadmap.md` は future plan、`docs/development_log.md` と `docs/proof_records.md` は履歴・記録 index として維持する。

`development_log.md` と `proof_records.md` は原則追記型とする。

詳細 archive は必要になった Phase 範囲で追加する。
