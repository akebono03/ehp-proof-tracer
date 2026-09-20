# EHP Proof Tracer — 証明記録

この文書は、代表的な数学的証明および証明基盤の記録索引である。

詳細な過去記録は内容を削除せず `docs/proof_records/` 以下へ分割して保存する。

現在の設計は `docs/design.md`、開発履歴は `docs/development_log.md`、今後の計画は `docs/roadmap.md` を参照する。

---

# 数学的証明記録

## 初期記録 / Toda Equation (5.8)

`docs/proof_records/early_records_and_toda_5_8.md`

記録形式、過去の代表 probe、Toda Equation (5.8)、Phase 66 完了記録を含む。

## Toda Lemma 5.7 から Lemma 5.10

`docs/proof_records/toda_5_7_to_5_10.md`

Toda Lemma 5.7、Proposition 5.8、Equation (5.10)、Proposition 5.9、Equation (5.12)、Lemma 5.10、Phase 72R / 72R-A1 の意味論訂正記録を含む。

## Toda Proposition 5.11 から Lemma 5.16

`docs/proof_records/toda_5_11_to_5_16.md`

Toda Proposition 5.11、Lemma 5.12、Proposition 5.15、Equation (5.16)、Lemma 5.16 を含む。

## Stable stems $G_0$ から $G_7$

`docs/proof_records/stable_stems_g0_g7.md`

Phase 78 の stable $G_0$ から $G_7$ までの統合記録を含む。

---

# 証明基盤の記録

## Phase 79–89

`docs/proof_records/proof_infrastructure_079_089.md`

Proof Repository、repository-assisted inference、自動 rule 選択、有界 producer search、診断、depth parameterization、有限 retry、具体的 theorem-instance filtering の記録。

## Phase 90–98

`docs/proof_records/calculation_provenance_090_095.md` ほか

Toda group query、正規化済み theorem-backed group result、EHP extraction、proof dependency / explanation、recursive proof provenance、structured presentation、full proof report、利用者向け convenience facade の記録。

## Phase 99–101

repository 内の generator occurrence 探索を標準運用リポジトリと CLI に接続した。

```text
GeneratorSymbol
→ structural occurrence
→ repository occurrence
→ semantic role
→ exploration
→ presentation
→ Markdown
→ production facade
```

新しい証明事実は生成しない。

## Phase 102

`docs/proof_records/production_proof_scope_exploration_102.md`

実際の `ProofStep.premises` ancestry を読み取り専用で探索可能にした。

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1
$$

および

$$
H(\nu')=\eta_5.
$$

重要:

```text
同じ ProofStep が同じ root 配下にある
→ 最短 depth の node のみ

同じ ProofStep が異なる root 配下にある
→ 異なる root provenance
```

Phase 102 は完了。

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

proof-scope source statement と inference-rule premise pattern の compatibility から applicable theorem / lemma candidate を読み取り専用で探索する capability を追加した。

```text
適用可能候補 != 証明成功
関連度カテゴリ != 証明事実
表示順 != 定理順位
candidate discovery = repository read-only
```

最終 catalog:

```text
catalog entries = 1188
families = 267
classified families = 158
unclassified families = 109

STRUCTURAL = 201
MAP_PROPERTY = 60
THEOREM_SPECIFIC = 424
GENERIC_RELATION = 63
BRIDGE = 140
UNCLASSIFIED = 300
```

Phase 103 は完了。

## Phase 104 applicability handoff / bounded execution provenance

Phase 104 は applicability candidate を明示的 handoff と bounded execution に接続した。

中心経路:

```text
選択済み applicability candidate
↓
RepositoryGeneratorApplicabilityCandidateHandoff
↓
READY validation
↓
最終 rule 明示の bounded search
↓
同一 BoundedProducerSearchReport object
↓
同一 selected producer_nodes
↓
同一 selected final_rule
↓
execution
↓
実際の ProofStep
```

重要な identity 不変条件:

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

```text
execution_result.report
is search_report.report
```

Phase 104 は完了。

```text
repository-wide after Phase 104-4P closure check:
8644 passed in 374.63s
```

## Phase 105 標準運用 applicability execution

Phase 105 は、Phase 104 の selected-candidate bounded execution を実際の標準運用 applicability workflow に接続した証明基盤記録である。

最初の境界:

```text
relevance category
!=
execution safety
```

対象 family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

これは Toda Equation (5.8)

$$
\Delta(\iota_9)=\pm(2\nu_4-E\nu')
$$

に対応する運用 rule family である。

### Execution seed / qualification

実際の applicability candidate が保持する exact source `ProofStep` を execution seed repository に登録し、discovery rule object と同一 identity を持つ fixed-point-safe execution entry を構成した。

```text
execution entry rule
is discovery candidate rule
```

標準 applicability catalog 自体は変更しない。

### Qualified ambiguity

標準 `nu_prime` applicability:

```text
qualified candidates = 744

full identity groups = 744
source+rule groups = 744
source+rule-name groups = 248
scope+source groups = 248
source-step identities = 124
```

完全同一 duplicate ではなく、同一 source 上に3つの異なる rule identity が存在する。

### Rule equivalence

3 catalog entry の比較:

```text
same factory = True
same rule signature = True
same entry metadata signature = True
same rule identity = False
same entry identity = False
```

そのため raw catalog を deduplicate せず、execution selection 層で family grouping する。

### Execution-family grouping

```text
744 raw qualified candidates
↓
248 execution-family groups
```

各 group は元の candidate 3件を保持する。

代表 candidate は discovery order 上の先頭 original candidate だが、theorem ranking ではない。

### Root/source の曖昧性解消

```text
root-only unique = False
source-step-only unique = False
root+source unique = True
```

root ごとの group 数:

```text
standard.toda.prop56  = 14
standard.toda.prop58  = 34
standard.toda.prop511 = 76
standard.toda.prop515 = 124
```

124個の source-step identity はすべて2 root に現れる。

global minimum depth = 1 にも6 group が残るため、`shortest_depth` を implicit ranking に使用しない。

### 明示選択

```text
root_entry identity
+
source_step identity
```

で0件または1件の execution-family group を選択する。

全248 standard root/source pair が一意に選択できる。

### 標準 execution facade

```text
標準 applicability result
→ qualified filtering
→ execution-family grouping
→ explicit root + source selection
→ representative
→ production execution orchestration
→ actual ProofStep
```

identity chain:

```text
qualified_selection.applicability_result
is original applicability_result

family_grouping.selection
is qualified_selection

family_selection.grouping
is family_grouping

execution.candidate
is family representative
```

Phase 105 では次を実装していない。

```text
automatic root selection
automatic source selection
shortest-depth ranking
theorem ranking
automatic goal discovery
new execution CLI
general qualification of every production rule family
raw applicability-catalog deduplication
```

最終検証:

```text
Phase 105-17 focused:
8 passed in 142.33s

Phase 105-7 / 10 / 14 / 16 / 17 related:
40 passed in 174.89s

repository-wide Phase 105 closure:
8709 passed in 659.02s
```

Phase 105 は完了。

## Phase 106 applicability 性能・複雑性記録

`docs/proof_records/performance_applicability_106.md`

Phase 106 は新しい証明事実を追加していない。

目的は、Phase 105 までに完成した applicability / execution 経路の意味論と provenance を保持したまま、性能圧力の所在を確認することだった。

初期監査:

```text
build_standard_production_applicability_catalog:
4.44 s / 4.37 MiB

explore_standard_repository_generator_applicability_input:
27.89 s / 274.10 MiB

select_qualified_repository_generator_applicability_candidates:
1.11 s / 25.00 MiB

group_qualified_repository_generator_execution_families:
0.025 s / 0.28 MiB

execute_standard_repository_generator_applicability_result_by_root_and_source:
1.09 s / 25.00 MiB
```

applicability discovery が支配的だった。

詳細監査:

```text
proof-scope nodes = 3889
generator occurrences = 626
pattern references = 2549

compatible references = 797573
match attempts = 797573
successful matches = 797573

full-scope candidates = 797573
generator-relevant candidates = 176616
retained ratio = 22.1442%
```

問題は失敗 match ではなく、generator に関係しない scope node についても candidate object を大量に materialize していたことだった。

同一 proof graph 上の監査で、relevant-scope prefilter が現在の結果と完全一致することを確認した。

```text
candidate_signature_sequence_equal = True
candidate_signature_multiset_equal = True
scope_identity_sequence_equal = True
root_identity_sequence_equal = True
source_identity_sequence_equal = True
catalog_entry_identity_sequence_equal = True
rule_identity_sequence_equal = True
```

実装後:

```text
applicability exploration:
8.16 s / 62.42 MiB

raw candidates = 176616
qualified candidates = 744
family groups = 248
unique source-step identities = 124
selected family size = 3
execution = True
```

重要:

```text
性能改善
!=
証明事実の変更

relevant-scope prefilter
!=
candidate ranking

materialization の削減
!=
raw catalog deduplication
```

Phase 106 は完了。

```text
repository-wide:
8712 passed in 337.86s
```

---

# 記録原則

数学的な根拠は `ProofStep` と、その実際の premise ancestry である。

```text
proof record != proof truth
presentation != proof truth
rendered prose != proof truth
report orchestration != proof truth
production repository assembly != theorem truth
exploration result != new theorem truth
proof-scope traversal != theorem search
known relation discovery != map evaluation
Toda membership discovery != bracket solving
applicability candidate != successful proof
relevance category != theorem truth
candidate ordering != theorem ranking
candidate selection != proof success
handoff validation != theorem truth
bounded search report != executed proof
qualified candidate != unique execution target
execution-family representative != theorem ranking
performance optimization != theorem truth
```

この文書群は、実装済み proof object と provenance を人間が追跡しやすくするための記録であり、独立した theorem database ではない。

実行資格付き execution layer が relevance category、root order、shortest depth、candidate order を暗黙の theorem ranking として使用してはならない。

Phase 106 の性能最適化も、candidate の意味論、順序、identity、provenance を変更してはならない。

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
