# Phase 106 — 性能・複雑性健全性監査と applicability prefilter

Phase 106 は、Phase 105 で最初の標準運用 qualified execution 経路が完成した直後に、機能拡張を急がず、現在の性能と複雑性を測定するために実施した。

この Phase の目的は新機能追加ではなく、

```text
どこが実際に重いかを測る
↓
必要な場合だけ最小最適化する
↓
意味論と provenance を維持する
```

ことである。

---

# Phase 106-1：性能・複雑性基準監査

標準 `nu_prime` 経路を段階別に計測した。

```text
build_standard_production_applicability_catalog:
4.439548 s
4.37 MiB peak

explore_standard_repository_generator_applicability_input:
27.893780 s
274.10 MiB peak

select_qualified_repository_generator_applicability_candidates:
1.109798 s
25.00 MiB peak

group_qualified_repository_generator_execution_families:
0.025466 s
0.28 MiB peak

execute_standard_repository_generator_applicability_result_by_root_and_source:
1.093390 s
25.00 MiB peak
```

件数:

```text
catalog entries = 1188
scope nodes = 3889
generator occurrences = 626
raw candidates = 176616
qualified candidates = 744
family groups = 248
unique source-step identities = 124
unique root identities = 4
```

結論:

```text
主要性能圧力
=
bounded execution ではなく applicability discovery
```

---

# Phase 106-2：applicability 規模・重複圧力監査

applicability discovery の内部を分解した。

```text
catalog build:
5.640820 s

proof-scope exploration:
2.655764 s

premise-pattern index build:
0.029932 s

candidate materialization over full scope:
23.830016 s
273.30 MiB peak

generator-filtered applicability facade:
28.085111 s
274.07 MiB peak
```

規模:

```text
proof-scope nodes = 3889
occurrences = 626
pattern references = 2549

compatible references = 797573
mean per scope node = 205.08
p90 = 686
p99 = 686
max = 686
```

pattern matching:

```text
match attempts = 797573
successful matches = 797573
success ratio = 1.0
```

candidate population:

```text
candidate count = 797573
unique source-step identities = 1975
unique scope-node identities = 3888
mean candidates per source identity = 403.83
sources under multiple roots = 1913
```

generator filter:

```text
797573
→
176616

retained = 22.1442%
discarded = 77.8558%
```

結論:

失敗する pattern match が大量に存在することが問題ではなかった。

互換と判定された797,573件はすべて実際に match していた。

問題は、generator に無関係な scope node に対しても candidate object を構築し、後段で約77.9%を捨てていたことだった。

---

# Phase 106-3：relevant-scope prefilter 初回意味論監査

最初の監査では、

```text
current_generator_applicability_facade
```

と

```text
audit_only_relevant_scope_prefilter_materialization
```

を比較した。

性能:

```text
current:
32.636174 s
274.08 MiB peak

prefilter:
4.919675 s
61.61 MiB peak
```

しかし identity 比較が `False` になった。

原因は prefilter の意味論ではなく、比較対象が別々に再構築された標準 repository / proof graph だったことである。

異なる object graph 間で `scope_node identity` を比較していたため、この監査だけでは意味論同値性を判定できなかった。

このため Phase 106-3 はその時点では未完了とし、実装へ進まなかった。

---

# Phase 106-3A：同一 proof graph 上の意味論監査

同じ

```text
catalog
proof_scope_exploration
```

を共有し、

```text
現行:
full scope materialization
→ occurrence-node identity filter

候補:
occurrence-node identity set
→ relevant scope nodes only
→ candidate materialization
```

を比較した。

結果:

```text
current full candidate count = 797573
current filtered candidate count = 176616
proposed candidate count = 176616
```

意味論・identity:

```text
candidate_signature_sequence_equal = True
candidate_signature_multiset_equal = True
scope_identity_sequence_equal = True
root_identity_sequence_equal = True
source_identity_sequence_equal = True
catalog_entry_identity_sequence_equal = True
rule_identity_sequence_equal = True
all_current_scope_nodes_relevant = True
all_proposed_scope_nodes_relevant = True
```

性能:

```text
current:
23.763063 s
273.30 MiB peak

prefilter:
4.656941 s
61.61 MiB peak
```

削減:

```text
time reduction = 80.40%
peak-memory reduction = 77.46%
scope-node reduction = 86.06%
candidate materialization reduction = 77.86%
```

この監査により、relevant-scope prefilter は現在の candidate sequence と provenance identity を保持できることが確定した。

---

# Phase 106-4：relevant-scope applicability prefilter 実装

変更対象:

```text
repository_generator_applicability_facade.py
tests/test_phase106_4_relevant_scope_prefilter_optimization.py
```

production code の変更対象は

```text
_build_generator_applicability_result()
```

のみ。

現行の

```text
full proof scope
→ 全 candidate materialize
→ occurrence_node_ids で filter
```

を、

```text
occurrence_node_ids
→ relevant RepositoryProofScopeResult
→ 既存 applicability finder
```

へ変更した。

変更しなかったもの:

```text
repository_proof_scope_applicability.py
rule matching
catalog semantics
Phase 104 handoff
Phase 105 qualification
Phase 105 grouping
Phase 105 execution
```

focused regression:

```text
22 passed in 57.94s
```

---

# Phase 106-5：実装後 closure 監査

実装後の基準:

```text
build_standard_production_applicability_catalog:
6.414673 s
4.37 MiB peak

explore_standard_repository_generator_applicability_input:
8.160966 s
62.42 MiB peak

select_qualified_repository_generator_applicability_candidates:
1.214806 s
25.00 MiB peak

group_qualified_repository_generator_execution_families:
0.025120 s
0.28 MiB peak

execute_standard_repository_generator_applicability_result_by_root_and_source:
1.072918 s
25.00 MiB peak
```

意味論件数:

```text
raw candidates = 176616
qualified candidates = 744
family groups = 248
representatives = 248
unique source-step identities = 124
unique root identities = 4
selected family size = 3
executed = True
```

repository-wide 独立実行:

```text
8712 passed in 337.86s
```

監査内の再実行:

```text
8712 passed in 220.35s
```

後者は filesystem / OS cache 等の温まった状態の影響を受ける可能性があるため、Phase 106 の正式な closure 値には独立実行の

```text
8712 passed in 337.86s
```

を採用する。

---

# Phase 106 の確定事項

```text
主要ボトルネック
=
applicability discovery の full-scope candidate materialization
```

```text
解決方法
=
generator-relevant scope prefilter
```

```text
維持したもの
=
candidate sequence
candidate semantics
scope identity
root identity
source identity
catalog-entry identity
rule identity
bindings
Phase 105 execution behavior
```

Phase 106 は完了。

---

# 次 Phase との境界

Phase 107-1 は

```text
post-Phase106 qualified-execution expansion pressure audit
```

とする。

Phase 106 で行わなかったもの:

```text
複数 production rule family の qualification
automatic root selection
automatic source selection
automatic goal discovery
execution CLI
result presentation integration
persistent cache
parallelization
catalog redesign
raw catalog deduplication
```

次は性能最適化を続けるのではなく、qualified execution のどの拡張が実際に必要かを監査する。
