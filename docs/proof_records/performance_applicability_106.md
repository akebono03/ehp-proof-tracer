# Phase 106 — Applicability 性能・provenance 保持記録

この記録は Phase 106 の性能監査と最小最適化について、証明基盤上の意味論不変条件をまとめる。

Phase 106 は新しい数学的定理や証明事実を追加しない。

---

# 1. 監査対象

対象は標準 `nu_prime` applicability 経路。

```text
explore_standard_repository_generator_applicability_input("nu_prime")
```

および、その結果を使用する Phase 105 qualified execution 経路。

---

# 2. 初期状態

```text
scope nodes = 3889
generator occurrences = 626
raw generator-relevant candidates = 176616
qualified candidates = 744
execution-family groups = 248
unique source-step identities = 124
```

applicability exploration:

```text
27.89 s
274.10 MiB peak
```

---

# 3. ボトルネック

full proof scope に対する candidate materialization:

```text
797573 candidates
```

その後、generator occurrence を含む node だけを残すと:

```text
176616 candidates
```

保持率:

```text
22.1442%
```

約77.9%は generator-specific facade で最終的に捨てられていた。

---

# 4. pattern matching の意味

```text
compatible references = 797573
match attempts = 797573
successful matches = 797573
```

したがって、性能圧力は「失敗する match の多さ」ではない。

既存 index が compatible と判定した reference はすべて実際に match している。

主因は candidate object の大量 materialization である。

---

# 5. prefilter の意味論監査

同一 proof graph 上で比較した。

現行:

```text
full scope
→ candidate materialization
→ occurrence scope_node identity filter
```

候補:

```text
occurrence scope_node identity set
→ relevant scope only
→ candidate materialization
```

確認項目:

```text
candidate_signature_sequence_equal = True
candidate_signature_multiset_equal = True
scope_identity_sequence_equal = True
root_identity_sequence_equal = True
source_identity_sequence_equal = True
catalog_entry_identity_sequence_equal = True
rule_identity_sequence_equal = True
```

したがって prefilter は candidate の順序・意味論・provenance identity を変更しない。

---

# 6. 実装境界

変更:

```text
repository_generator_applicability_facade.py
_build_generator_applicability_result()
```

新規回帰テスト:

```text
tests/test_phase106_4_relevant_scope_prefilter_optimization.py
```

変更なし:

```text
repository_proof_scope_applicability.py
InferenceRulePremisePatternIndex
match_premise_pattern()
standard production applicability catalog
Phase 104 handoff
Phase 105 qualified selection
Phase 105 family grouping
Phase 105 root/source selection
Phase 105 execution orchestration
```

---

# 7. 実装後

```text
applicability exploration:
8.16 s
62.42 MiB peak
```

件数:

```text
raw candidates = 176616
qualified candidates = 744
family groups = 248
representatives = 248
unique source-step identities = 124
unique root identities = 4
selected family size = 3
execution = True
```

---

# 8. repository-wide 回帰

独立実行:

```text
8712 passed in 337.86s
```

監査内の再実行:

```text
8712 passed in 220.35s
```

正式記録には独立実行を採用する。

---

# 9. 証明基盤上の結論

```text
性能改善
!=
証明事実の追加

scope prefilter
!=
candidate ranking

scope prefilter
!=
catalog deduplication

materialization 削減
!=
execution-family selection の変更
```

Phase 106 の変更は、既存の applicability semantics と proof provenance を保持した局所的な性能改善である。
