# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、不変条件、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・証明探索上の必要
↓
不足している最小表現
↓
必要な領域固有規則 / オーケストレーション
↓
既存の汎用基盤
```

次を混同しない。

```text
表現 != 型付け != 定理知識
構造的等値 != 数学的等値
catalog metadata != 証明事実
search plan != 証明結果
calculation result != 証明事実
presentation != 証明事実
production repository assembly != 定理事実
exploration result != 新しい定理事実
proof-scope traversal != 定理探索
known relation discovery != 写像評価
Toda membership discovery != bracket solving
applicability candidate != 証明成功
relevance category != 定理順位
candidate selection != 証明成功
handoff validation != 定理事実
bounded search result != 実行済み証明
qualified candidate != 一意な実行対象
execution-family grouping != raw catalog deduplication
representative selection != 定理順位付け
```

---

# 2. 現在の主要経路

計算経路:

```text
式 / statement 表現
↓
汎用 proof / inference 機構
↓
Toda 固有の定理知識
↓
Proof Repository / rule catalog
↓
bounded proof search
↓
Toda group query / lookup
↓
計算 goal の発見 / 復元 / 正規化
↓
group result
↓
EHP / exactness provenance
↓
proof provenance
↓
構造化 presentation
↓
人間向け proof report
```

generator 探索 / applicability 経路:

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
構造的 occurrence
↓
Toda membership / 既知 map relation
↓
premise-pattern compatibility
↓
applicability candidate
↓
rule group / rule family
↓
relevance 分類済み presentation
```

Phase 104 handoff / execution:

```text
selected applicability candidate
↓
RepositoryGeneratorApplicabilityCandidateHandoff
↓
READY validation
↓
explicit-final-rule bounded search
↓
prebuilt BoundedProducerSearchReport
↓
selected-path execution
↓
actual ProofStep provenance
```

Phase 105 standard production-qualified execution:

```text
RepositoryGeneratorApplicabilityExplorationResult
↓
qualified candidate filtering
↓
execution-family grouping
↓
explicit root_entry + source_step selection
↓
representative candidate
↓
production execution orchestration
↓
actual ProofStep
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

探索 / applicability:

```text
generator_input.py
repository_element_*.py
repository_proof_scope.py
repository_proof_scope_exploration.py
repository_proof_scope_facade.py
repository_proof_scope_applicability.py
repository_generator_applicability_facade.py
repository_generator_applicability_selection.py
```

Phase 105:

```text
repository_generator_applicability_execution_seed.py
repository_generator_applicability_execution_entry.py
repository_generator_applicability_execution_orchestration.py
repository_generator_qualified_execution_selection.py
repository_generator_qualified_execution_handoff.py
repository_generator_qualified_execution_family.py
repository_generator_qualified_execution_family_selection.py
repository_generator_standard_qualified_execution_facade.py
```

---

# 4. Proof truth と metadata

証明事実の中心:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata である。

presentation、renderer、facade、production repository、CLI、exploration、resolver、proof-scope traversal、applicability classification は証明事実を追加してはならない。

---

# 5. Repository read-only 不変条件

query / calculation / reporting / exploration / applicability discovery / bounded execution planning は repository を read-only に扱う。

execution は inference result を構成するが、元の `ProofRepository` 自体を変更しない。

```text
repository entries before == repository entries after
```

必要な箇所では `ProofStep` identity も保持する。

---

# 6. Calculation result の意味論

```text
0 candidates  → NOT_FOUND
1 candidate   → FOUND
2+ candidates → MULTIPLE_RESULTS
```

複数 candidate を自動で順位付け・選択しない。

---

# 7. EHP / exactness provenance

根拠は final theorem-backed `ProofStep` から到達可能な ancestry である。

代表例:

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

# 8. Generator input の意味論

`resolve_generator_input()` は明示的なユーザー入力を exact `GeneratorSymbol` へ変換する。

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

重要:

```text
unindexed generator != wildcard
```

自由形式の typo correction や数学的同値判定は行わない。

---

# 9. Proof-scope traversal の意味論

`RepositoryProofScopeNode`:

```text
root_entry
proof_step
shortest_depth
```

不変条件:

```text
depth 0 = root_entry.step

same ProofStep identity under one root
= one node at shortest depth

same ProofStep identity under different roots
= distinct provenance nodes

cycle
= safe termination
```

---

# 10. Applicability discovery の意味論

candidate は概念的に次を保持する。

```text
catalog_entry
premise_index
premise_pattern
source_step
bindings
```

重要:

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

category 順序は theorem ranking ではない。

---

# 11. Phase 104 handoff 不変条件

`READY` validation 後の final rule は再選択しない。

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

prebuilt report は再生成しない。

```text
execution_result.report
is search_report.report
```

selected producer も identity を保持する。

```text
producer_node.producer_rule
is executed_producer_step.inference_rule
```

---

# 12. Phase 105 execution qualification

Phase 105 は relevance 分類を execution safety とみなさない。

最初に production-qualified とした family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

standard applicability catalog では、この factory に由来する構造的に同値な3つの clone entry が存在する。

監査結果:

```text
qualified raw candidates = 744
source+rule-name groups = 248
unique source-step identities = 124
```

3 clone は

```text
same factory
same rule signature
same entry metadata signature
different catalog-entry identity
different rule identity
```

である。

raw catalog から重複除去せず、execution selection 層で family grouping を行う。

---

# 13. Execution-family grouping

同一 source 上の structurally equivalent qualified clone candidates を1 family group にまとめる。

概念的 grouping key:

```text
scope_node identity
source_step identity
qualified family name
premise_index
bindings
```

group は original candidate を全件保持する。

代表 candidate:

```text
group.representative is group.candidates[0]
```

これは theorem ranking ではなく、同一 clone family 内の execution identity を選ぶ規約である。

---

# 14. Root/source disambiguation

standard `nu_prime` では 248 execution-family groups がある。

```text
standard.toda.prop56  = 14
standard.toda.prop58  = 34
standard.toda.prop511 = 76
standard.toda.prop515 = 124
```

124個の source-step identity はすべて2 root に現れる。

```text
source-step identity alone
!= unique execution provenance
```

root だけでも複数 group が残る。

global minimum `shortest_depth = 1` にも6 group が残るため、

```text
shortest_depth
!= implicit selection policy
```

とする。

一方、

```text
root_entry identity
+
source_step identity
```

は全248 group で一意である。

---

# 15. Explicit family selection

`RepositoryGeneratorQualifiedExecutionFamilySelection` は explicit `root_entry` と `source_step` identity を入力として0件または1件の group を返す。

foreign identity は拒否する。

root の自動優先、depth ranking、group-order ranking は行わない。

---

# 16. Standard execution facade

```text
execute_standard_repository_generator_applicability_result_by_root_and_source(
  applicability_result,
  root_entry,
  source_step,
  goal,
  max_depth=2,
  retry_policy=None,
)
```

この facade は generator string から proof graph を作り直さない。

```text
root_entry / source_step identity
must belong to the same applicability_result graph
```

を守るためである。

identity chain:

```text
original applicability_result
→ qualified_selection.applicability_result
→ family_grouping.selection
→ family_selection.grouping
→ representative
→ execution.candidate
```

---

# 17. Phase 105 で実装しないもの

```text
automatic root selection
automatic source selection
shortest-depth ranking
theorem ranking
proof ranking
automatic goal discovery
new execution CLI
general qualification of every production rule family
raw applicability-catalog deduplication
repository snapshot/versioning
```

---

# 18. CLI 境界

```text
python main.py 5 7
python main.py explore "nu'"
python main.py explore-proof nu_prime
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

Phase 105 は execution CLI を追加しない。

---

# 19. 現在の未実装境界

```text
自由形式自然言語検索
wildcard family search
一般 composition evaluation
一般 Toda-bracket solving
bracket-value computation
一般 coset / indeterminacy computation
一般 E / H / Δ evaluation
represented ancestry を超える recursive theorem solving
未記載数学的帰結の自動列挙
symbolic higher-range auto-instantiation
general theorem ranking
producer ranking
proof-cost optimization
best-proof selection
general unbounded backtracking
persistent proof cache
repository snapshot/versioning
stale-search-report detection
automatic production root/source selection
general production-rule execution qualification
user-facing execution CLI
Web UI
odd-primary full integration
all-primary ordinary sphere-homotopy calculation
```

---

# 20. 文書 TeX 方針

GitHub Markdown では数式に

```text
inline:  $...$
display: $$...$$
```

を使用する。

コードや CLI は backtick / code block、数式は数式 delimiter を使う。

---

# 21. 完了基準

Phase 103:

```text
PHASE103_7_CLOSURE_AUDIT = PASS
409 passed in 186.07s
```

Phase 104:

```text
repository-wide after Phase 104-4P closure check:
8644 passed in 374.63s

PASS — no residual production implementation required
```

Phase 105:

```text
Phase 105-17 focused:
8 passed in 142.33s

Phase 105-7 / 10 / 14 / 16 / 17 related:
40 passed in 174.89s

repository-wide Phase 105 closure:
8709 passed in 659.02s
```

Phase 105 は COMPLETE。
