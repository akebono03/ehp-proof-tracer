# EHP Proof Tracer 開発記録

この文書は開発履歴の索引である。

現在の仕様・設計は `README.md` と `docs/design.md` を優先する。
今後の計画は `docs/roadmap.md`、代表的な数学的証明・証明基盤の記録は `docs/proof_records.md` を参照する。

過去の詳細な開発記録は、内容を削除せず `docs/development_log/` 以下へ分割して保存する。

---

# 開発履歴アーカイブ

## Phase 1–48

`docs/development_log/phases_001_048.md`

可換群計算、汎用推論、EHP、Toda の基礎表現から Proposition 4.4 周辺まで。

## Phase 49–64

`docs/development_log/phases_049_064.md`

$\pi_3^2$、$\pi_4^3$、Toda Proposition 5.1、Lemma 5.2、$\nu'$、$\nu_4$、$\nu$-family、性能安定化まで。

## Phase 65–78

`docs/development_log/phases_065_078.md`

Toda Proposition 5.6 から Lemma 5.16、stable $G_0$ から $G_7$ までの主要な数学的証明経路。

## Phase 79–89

`docs/development_log/phases_079_089.md`

Proof Repository、repository-assisted inference、自動 rule 選択、有界 producer search、診断、depth parameterization、有限 retry、具体的 theorem-instance compatibility まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda group query、正規化済み group result、EHP provenance、flat / recursive proof provenance、計算オーケストレーションの記録。Phase 95 完了記録を含む。

## Phase 96

`docs/development_log/phases_096.md`

構造化 presentation、EHP / exactness presentation、proof source presentation、依存関係順の proof flow、Markdown / LaTeX renderer、読みやすい narrative、統合 full proof report、最終監査の記録。

Phase 96 は完了。

```text
repository-wide:
7609 passed in 121.63s
```

## Phase 97

`docs/development_log/phases_097.md`

calculation-to-report オーケストレーション境界監査、最小 top-level report result 表現、`NOT_FOUND / FOUND / MULTIPLE_RESULTS` 処理、代表6 target の top-level validation、最終監査の記録。

Phase 97 は完了。

```text
repository-wide:
7609 passed in 121.63s
```

## Phase 98

`docs/development_log/phases_098.md`

利用者向け convenience の必要性監査、raw `n,k` の薄い facade、単一 `FOUND` report access、順序保持した report collection access、代表経路の validation、最終監査の記録。

Phase 98 は完了。

```text
repository-wide:
7643 passed in 123.73s
```

## Phase 99

Phase 99 は element-centered repository exploration を段階的に追加した。

```text
GeneratorSymbol の構造的包含
→ 構造的 occurrence path
→ repository 全体の occurrence lookup
→ semantic role 分類
→ element-centered exploration
→ grouped presentation
→ Markdown rendering
→ one-shot exploration facade
```

Phase 99 は完了。

```text
repository-wide:
7824 passed in 136.59s
```

## Phase 100

Phase 100 では既存 theorem-backed bootstrap を標準運用リポジトリへ統合し、repository-free facade と最小 CLI へ接続した。

```text
raw n,k
→ build_standard_toda_report(n,k)
  または python main.py n k
→ 標準運用リポジトリ
→ build_toda_report(repository,n,k)
→ TodaCalculationReportResult
→ 人間向け proof report
```

Phase 100-12 は完了。

```text
repository-wide:
8010 passed in 179.65s
```

## Phase 101

`docs/development_log/phases_101.md`

Phase 101 は Phase 99 の generator-centered exploration を運用利用者向け経路へ接続した。

```text
generator 文字列
→ canonical GeneratorSymbol
→ 標準運用リポジトリ
→ structural occurrence exploration
→ grouped Markdown
→ main.py explore
```

Phase 101 は完了。

```text
repository-wide:
8058 passed in 133.01s
```

## Phase 102

`docs/development_log/phases_102.md`

Phase 102 は top-level registered conclusion exploration を実際の運用 proof ancestry へ拡張し、Toda membership と既知 map relation を読み取り専用で探索する capability を追加した。

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1
$$

および

$$
H(\nu')=\eta_5
$$

Phase 102 は完了。

```text
repository-wide after Phase 102-7:
8142 passed in 129.93s
```

## Phase 103

`docs/development_log/phases_103.md`

Phase 103 は proof-scope exploration を applicable theorem / lemma candidate discovery へ接続した。

```text
generator
→ proof-scope source statements
→ premise-pattern compatibility
→ applicability candidates
→ rule groups
→ rule families
→ relevance categories
→ compact / detailed presentation
→ main.py explore-applicable
```

Phase 103-6 では relevance metadata を導入した。

```text
THEOREM_SPECIFIC
MAP_PROPERTY
STRUCTURAL
BRIDGE
GENERIC_RELATION
UNCLASSIFIED
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

```text
Phase 103 regression:
54 test files
409 passed in 186.07s
```

## Phase 104

Phase 104 は relevance-classified applicability candidate を、theorem ranking や automatic unbounded execution に拡張せず、既存の有界 proof-search infrastructure へ安全に接続した。

中心経路:

```text
適用可能候補
↓
候補の絞り込み / source 範囲での選択
↓
明示的 handoff
↓
execution-catalog 検証
↓
READY
↓
検証済み最終 rule の明示
↓
有界 producer search
↓
事前構築済み search report
↓
選択 producer path
↓
実行
↓
ProofStep provenance
```

主要不変条件:

```text
候補の絞り込み != theorem ranking
候補選択 != proof success
candidate handoff != automatic proof execution
```

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

## Phase 105

Phase 105 は、Phase 104 で完成した selected applicability candidate の bounded execution capability を、**実際の標準運用 applicability workflow に接続できるか**を監査し、最初の qualified production rule family について端から端までの統合を完成させた。

基本方針:

```text
relevance classification
!=
execution safety qualification
```

主要段階:

```text
Phase 105-1 / 105-2
運用 workflow pressure と safe-catalog 境界監査

Phase 105-3 / 105-4
Toda Equation (5.8) rule の execution safety と source provenance 監査

Phase 105-5
exact source ProofStep を使う execution-seed repository adapter

Phase 105-6
最初の qualified production execution entry / catalog adapter

Phase 105-7
candidate → seed → execution catalog → handoff → search → execution

Phase 105-8
selection boundary 監査

Phase 105-9
qualified candidate filtering と NONE / UNIQUE / AMBIGUOUS 表現

Phase 105-10
UNIQUE qualified candidate → orchestration handoff

Phase 105-11
standard applicability → qualified selection → handoff 境界監査

Phase 105-12
source-identity deduplication / disambiguation 境界監査

Phase 105-13
qualified rule-equivalence / repeated catalog-entry provenance 監査

Phase 105-14
qualified execution-family grouping / representative selection 実装

Phase 105-15
root/source scoped disambiguation 監査

Phase 105-16
explicit root + source scoped family selection 実装

Phase 105-17
standard applicability → qualified grouping → explicit selection → execution facade integration

Phase 105-18
最終文書更新 / 完了
```

Phase 105-12 の監査:

```text
qualified candidates = 744
source+rule-name groups = 248
scope+source groups = 248
unique source-step identities = 124
```

Phase 105-13:

```text
same factory
same rule signature
same entry metadata signature
different entry identity
different rule identity
```

そのため raw applicability catalog は保持し、execution selection 層で family grouping した。

```text
744 raw qualified candidates
↓
248 execution-family groups
```

Phase 105-15:

```text
root-only unique = False
source-step-only unique = False
root+source unique = True
```

global minimum depth にも6 group が残るため、`shortest_depth` を暗黙の選択規則にしない。

Phase 105-16 では

```text
explicit root_entry identity
+
explicit source_step identity
```

で execution-family group を0件または1件へ絞る API を実装した。

Phase 105-17 では

```text
標準 applicability result
→ qualified filtering
→ execution-family grouping
→ explicit root + source selection
→ representative candidate
→ production execution orchestration
→ actual ProofStep
```

までを1本の facade に接続した。

Phase 105 で実装しなかったもの:

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

最終確認:

```text
Phase 105-17 focused:
8 passed in 142.33s

Phase 105-7 / 10 / 14 / 16 / 17 related:
40 passed in 174.89s

repository-wide Phase 105 closure:
8709 passed in 659.02s
```

Phase 105 は完了。

## Phase 106

`docs/development_log/phases_106.md`

Phase 106 は Phase 105 後の機能拡張を始める前に、性能と複雑性の健全性を監査した。

基準監査:

```text
catalog build:
4.44 s / 4.37 MiB

nu_prime applicability exploration:
27.89 s / 274.10 MiB

qualified filtering:
1.11 s / 25.00 MiB

family grouping:
0.025 s / 0.28 MiB

標準実行 facade:
1.09 s / 25.00 MiB
```

主要ボトルネックは execution ではなく applicability discovery だった。

詳細監査:

```text
proof-scope nodes = 3889
generator occurrences = 626
full-scope candidates = 797573
generator-relevant candidates = 176616
retained = 22.1442%
```

同一 proof graph 上で relevant-scope prefilter を監査し、候補列と provenance identity が完全一致することを確認した。

```text
candidate_signature_sequence_equal = True
candidate_signature_multiset_equal = True
scope_identity_sequence_equal = True
root_identity_sequence_equal = True
source_identity_sequence_equal = True
catalog_entry_identity_sequence_equal = True
rule_identity_sequence_equal = True
```

Phase 106-4 で `_build_generator_applicability_result()` に最小変更を行い、generator-relevant scope のみを既存 finder へ渡すようにした。

focused regression:

```text
22 passed in 57.94s
```

実装後の基準:

```text
nu_prime applicability exploration:
8.16 s / 62.42 MiB

raw candidates = 176616
qualified candidates = 744
family groups = 248
unique source-step identities = 124
selected family size = 3
executed = True
```

repository-wide:

```text
8712 passed in 337.86s
```

監査内の warmed run:

```text
8712 passed in 220.35s
```

正式な closure 値には独立実行の `337.86s` を採用する。

Phase 106 は完了。

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は、該当する archive file に追記するか、Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

現在の capability を確認する目的では、この開発履歴よりも次を優先する。

```text
README.md
docs/design.md
docs/roadmap.md
docs/code_reference.md
docs/proof_records.md
```

次の開始点は `Phase 107-1` の qualified-execution expansion pressure audit である。
