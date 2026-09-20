# EHP Proof Tracer ロードマップ

この文書は**今後の capability dependency と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

運用計算経路:

```text
raw n,k
→ python main.py n k
  または build_standard_toda_report()
→ 標準運用リポジトリ
→ 証明レポート
```

generator 探索:

```text
generator 文字列
→ top-level / recursive proof-scope exploration
→ Toda membership / 既知 map relation
→ applicable theorem / lemma candidates
→ 関連度分類済み表示
```

標準運用・実行資格付き経路:

```text
標準 applicability result
↓
実行資格を満たす候補の抽出
↓
実行ファミリーのグループ化
↓
root_entry + source_step の明示選択
↓
family representative
↓
運用実行オーケストレーション
↓
実際の ProofStep
```

applicability 性能経路:

```text
generator occurrence
↓
generator に関係する scope_node のみを事前選別
↓
既存 applicability finder
↓
既存と同じ候補列・provenance identity
```

最新確認:

```text
Phase 106-4 focused:
22 passed in 57.94s

repository-wide Phase 106 closure:
8712 passed in 337.86s

nu_prime applicability exploration:
8.16 s / 62.42 MiB
```

Phase 106 は完了。

---

# 2. 完了済み capability

Phase 90–98:

```text
query
group normalization
EHP / exactness provenance
flat / recursive proof provenance
calculation orchestration
structured presentation
readable full proof report
raw n,k facade
```

Phase 99–104:

```text
structural generator containment
repository occurrence lookup
semantic roles
generator exploration
standard production repository
calculation CLI
production generator-input handling
recursive proof-scope exploration
Toda membership / known map relation discovery
applicability discovery
relevance classification
candidate handoff
READY validation
explicit-final-rule bounded search
prebuilt-report execution
actual ProofStep provenance
```

Phase 105:

```text
運用 execution-safety pressure audit
exact source-step execution seed
最初の qualified production execution entry
candidate execution orchestration
qualified NONE / UNIQUE / AMBIGUOUS 表現
execution-family clone audit
execution-family grouping
root/source disambiguation audit
explicit root + source family selection
standard applicability-to-execution facade
repository-wide closure regression
```

Phase 106:

```text
性能・複雑性基準監査
applicability discovery の規模監査
candidate 重複圧力監査
同一 proof graph 上の relevant-scope prefilter 意味論監査
generator-relevant scope prefilter 実装
focused regression
repository-wide regression
性能 closure
```

---

# 3. 現在の利用者向け API

計算:

```text
build_toda_report(repository, n, k)
build_standard_toda_report(n, k)
python main.py n k
```

generator 探索:

```text
explore_repository_generator(repository, generator)
explore_standard_repository_generator_input(generator_input)
python main.py explore "nu'"
```

再帰的 proof-scope exploration:

```text
explore_repository_generator_proof_scope(repository, generator)
explore_standard_repository_generator_proof_scope_input(generator_input)
python main.py explore-proof nu_prime
```

applicability exploration:

```text
explore_standard_repository_generator_applicability_input(generator_input)
python main.py explore-applicable nu_prime
python main.py explore-applicable nu_prime --detailed
```

実行資格付き facade:

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

実行資格付き execution は現在 Python infrastructure capability であり、新しい CLI はない。

---

# 4. Phase 105 で確定した境界

```text
relevance
!=
execution qualification
```

標準 `nu_prime` applicability:

```text
qualified raw candidates = 744
execution-family groups = 248
unique source-step identities = 124
```

同一 source 上の3つの qualified candidate は、factory / rule signature / entry metadata が同じだが、rule identity / catalog-entry identity が異なる。

したがって:

```text
raw applicability catalog
→ 保持

execution selection layer
→ family grouping
```

とする。

さらに:

```text
root のみ
→ 一意ではない

source_step のみ
→ 一意ではない

shortest_depth
→ selection policy にしない

root_entry identity + source_step identity
→ 248 group すべてで一意
```

Phase 105 はこの explicit selection を運用 facade に接続した。

---

# 5. Phase 106 で確定した性能境界

Phase 106 開始時の標準 `nu_prime` applicability exploration:

```text
27.89 s
274.10 MiB peak
176616 最終 candidates
```

内訳監査では、全証明範囲に対して

```text
797573 full-scope candidates
```

を構築した後、

```text
176616 generator-relevant candidates
```

だけを残していた。

77.86% の candidate materialization が後段で不要になっていた。

同一 proof graph 上の relevant-scope prefilter 監査では、次がすべて保持された。

```text
candidate sequence
candidate multiset
scope_node identity
root_entry identity
source_step identity
catalog_entry identity
rule identity
premise_index
premise_pattern
bindings
```

実装後:

```text
8.16 s
62.42 MiB peak
176616 raw candidates
744 qualified candidates
248 execution-family groups
124 unique source-step identities
```

したがって Phase 106 では、性能改善のために applicability semantics や execution semantics を変更していない。

---

# 6. 次 Phase の開始境界

次は

```text
Phase 107-1
post-Phase106 qualified-execution expansion pressure audit
```

とする。

目的は、Phase 105 の first-family integration を機械的に一般化することではない。

監査候補:

```text
1. qualified production rule family を
   1 family から複数 family へ広げる実需要があるか

2. explicit root/source selection を
   user-facing workflow からどう指定するか

3. goal を呼び出し側が与える現在の境界を
   維持すべきか、goal discovery が必要か

4. execution CLI が本当に必要か

5. execution result を calculation / exploration presentation に
   接続する実需要があるか
```

Phase 107-1 では実装を先取りせず、実際の圧力を確認してから最小境界を決める。

---

# 7. 保留：複数 production rule family の qualification

現在、標準運用で execution qualification されている family は

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

のみである。

今後 family を増やす場合は、各 family ごとに

```text
actual production source
execution safety
goal compatibility
required seed context
rule identity preservation
producer-search behavior
```

を確認する。

relevance category を qualification の根拠にしない。

---

# 8. 保留：goal discovery

現在の運用 execution facade は `goal` を明示入力とする。

未実装:

```text
source candidate から goal を自動推定
unknown RHS を含む target search
複数 goal 候補の ranking
```

---

# 9. 保留：数学的 evaluator

未実装:

```text
一般 Toda-bracket solver
bracket value computation
indeterminacy / coset normalization
一般 composition evaluation
一般 E(x) / H(x) / Δ(x) evaluation
```

既知 relation / membership の探索とは分離する。

---

# 10. 保留：proof optimization

```text
一般 backtracking
theorem ranking
producer ranking
proof-cost optimization
best-proof selection
persistent proof cache
```

実際の圧力が出るまで保留する。

Phase 106 の relevant-scope prefilter はこの「proof optimization」とは別であり、候補意味論を変えない局所的な materialization 削減である。

---

# 11. 保留：repository versioning

未実装:

```text
repository version token
repository snapshot
STALE_SEARCH_REPORT
REPOSITORY_CHANGED
cross-session execution-plan persistence
```

---

# 12. 保留：利用者向け画面

将来候補:

```text
qualified execution workflow の user-facing orchestration
execution CLI
Web UI
structured export
interactive proof graph
filterable exploration UI
```

---

# 13. 保留：数学的対象範囲

```text
odd-primary integration
broader unstable stems
additional Toda propositions / lemmas
all-primary ordinary sphere-homotopy calculation
```

---

# 14. 直近の次作業

```text
Phase 107-1
post-Phase106 qualified-execution expansion pressure audit
```

最初に確認するのは「何を追加できるか」ではなく、「何を追加する必要があるか」である。

Phase 106 で性能上の主要圧力を閉じたため、Phase 107 では

```text
複数 family qualification
user-facing root/source selection
goal discovery
execution CLI
result presentation integration
```

のどれが次の実需要なのかを監査する。
