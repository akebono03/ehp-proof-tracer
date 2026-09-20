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

Proof Repository、repository-assisted inference、自動 rule 選択、bounded producer search、診断、depth parameterization、有限 retry、具体的 theorem-instance filtering の記録。

## Phase 90–98

`docs/proof_records/calculation_provenance_090_095.md` ほか

Toda group query、正規化済み theorem-backed group result、EHP extraction、proof dependency / explanation、recursive proof provenance、structured presentation、full proof report、user-facing convenience facade の記録。

## Phase 99–101

repository 内の generator occurrence 探索を standard production repository と CLI に接続した。

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

actual `ProofStep.premises` ancestry を read-only に探索可能にした。

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
same ProofStep under one root
→ shortest-depth node only

same ProofStep under different roots
→ distinct root provenance
```

Phase 102 は COMPLETE。

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

proof-scope source statement と inference-rule premise pattern の compatibility から applicable theorem / lemma candidate を read-only に探索する capability を追加した。

```text
applicability candidate != proof success
relevance category != proof truth
presentation order != theorem ranking
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

Phase 103 は COMPLETE。

## Phase 104 applicability handoff / bounded execution provenance

Phase 104 は applicability candidate を explicit handoff と bounded execution に接続した。

中心経路:

```text
selected applicability candidate
↓
RepositoryGeneratorApplicabilityCandidateHandoff
↓
READY validation
↓
explicit-final-rule bounded search
↓
same BoundedProducerSearchReport object
↓
same selected producer_nodes
↓
same selected final_rule
↓
execution
↓
actual ProofStep
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

Phase 104 は COMPLETE。

```text
repository-wide after Phase 104-4P closure check:
8644 passed in 374.63s
```

## Phase 105 production-qualified applicability execution

Phase 105 は、Phase 104 の selected-candidate bounded execution を実際の standard production applicability workflow に接続した証明基盤記録である。

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

に対応する production rule family である。

### Execution seed / qualification

actual applicability candidate が保持する exact source `ProofStep` を execution seed repository に登録し、discovery rule object と同一 identity を持つ fixed-point-safe execution entry を構成した。

```text
execution entry rule
is discovery candidate rule
```

standard applicability catalog 自体は変更しない。

### Qualified ambiguity

standard `nu_prime` applicability:

```text
qualified candidates = 744

full identity groups = 744
source+rule groups = 744
source+rule-name groups = 248
scope+source groups = 248
source-step identities = 124
```

完全同一 duplicate ではなく、同一 source 上に3つの distinct rule identity が存在する。

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

各 group は original candidate 3件を保持する。

代表 candidate は discovery order 上の先頭 original candidate だが、theorem ranking ではない。

### Root/source disambiguation

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

### Explicit selection

```text
root_entry identity
+
source_step identity
```

で0件または1件の execution-family group を選択する。

全248 standard root/source pair が一意に選択できる。

### Standard execution facade

```text
standard applicability result
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

Phase 105 は COMPLETE。

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
```

この文書群は、実装済み proof object と provenance を人間が追跡しやすくするための記録であり、独立した theorem database ではない。

Phase 105 qualified execution layer が relevance category、root order、shortest depth、candidate order を暗黙の theorem ranking として使用してはならない。

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
