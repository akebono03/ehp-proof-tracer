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

Proof Repository、repository-assisted inference、自動 rule 選択、bounded producer search、診断、depth parameterization、有限 retry、具体的 theorem-instance compatibility まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda group query、正規化済み group result、EHP provenance、flat / recursive proof provenance、計算オーケストレーションの記録。Phase 95 完了記録を含む。

## Phase 96

`docs/development_log/phases_096.md`

構造化 presentation、EHP / exactness presentation、proof source presentation、依存関係順の proof flow、Markdown / LaTeX renderer、読みやすい narrative、統合 full proof report、最終監査の記録。

Phase 96 は COMPLETE。

## Phase 97

`docs/development_log/phases_097.md`

calculation-to-report オーケストレーション境界監査、最小 top-level report result 表現、`NOT_FOUND / FOUND / MULTIPLE_RESULTS` 処理、代表6 target の top-level validation、最終監査の記録。

Phase 97 は COMPLETE。

```text
repository-wide:
7609 passed in 121.63s
```

## Phase 98

`docs/development_log/phases_098.md`

user-facing convenience の必要性監査、raw `n,k` thin facade、single `FOUND` report access、順序保持した report collection access、代表経路の validation、最終監査の記録。

Phase 98 は COMPLETE。

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

Phase 99 は COMPLETE。

```text
repository-wide:
7824 passed in 136.59s
```

## Phase 100

Phase 100 では既存 theorem-backed bootstrap を standard production repository へ統合し、repository-free facade と minimal CLI へ接続した。

```text
raw n,k
→ build_standard_toda_report(n,k)
  または python main.py n k
→ standard production repository
→ existing build_toda_report(repository,n,k)
→ TodaCalculationReportResult
→ 人間向け proof report
```

Phase 100-12 は COMPLETE。

```text
repository-wide:
8010 passed in 179.65s
```

## Phase 101

`docs/development_log/phases_101.md`

Phase 101 は Phase 99 の generator-centered exploration を production user-facing path へ接続した。

```text
generator string
→ canonical GeneratorSymbol
→ standard production repository
→ structural occurrence exploration
→ grouped Markdown
→ main.py explore
```

Phase 101 は COMPLETE。

```text
repository-wide:
8058 passed in 133.01s
```

## Phase 102

`docs/development_log/phases_102.md`

Phase 102 は top-level registered conclusion exploration を actual production proof ancestry へ拡張し、Toda membership と既知 map relation を read-only に探索する capability を追加した。

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1
$$

および

$$
H(\nu')=\eta_5
$$

Phase 102 は COMPLETE。

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

Phase 103 は COMPLETE。

```text
Phase 103 regression:
54 test files
409 passed in 186.07s
```

## Phase 104

Phase 104 は relevance-classified applicability candidate を、theorem ranking や automatic unbounded execution に拡張せず、既存 bounded proof-search infrastructure へ安全に接続した。

中心経路:

```text
applicability candidate
↓
candidate filtering / source-scoped selection
↓
explicit handoff
↓
execution-catalog validation
↓
READY
↓
explicit validated final rule
↓
bounded producer search
↓
prebuilt search report
↓
selected producer path
↓
actual execution
↓
ProofStep provenance
```

主要不変条件:

```text
candidate filtering != theorem ranking
candidate selection != proof success
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

Phase 104 は COMPLETE。

```text
repository-wide after Phase 104-4P closure check:
8644 passed in 374.63s
```

## Phase 105

Phase 105 は、Phase 104 で完成した selected applicability candidate の bounded execution capability を、**実際の standard production applicability workflow に接続できるか**を監査し、最初の qualified production rule family について end-to-end integration を完成させた。

基本方針:

```text
relevance classification
!=
execution safety qualification
```

主要段階:

```text
Phase 105-1 / 105-2
production workflow pressure と safe-catalog 境界監査

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
final documentation / closure
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
standard applicability result
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

Phase 105 は COMPLETE。

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は、該当する archive file に追記するか、将来の Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

現在の capability を確認する目的では、この開発履歴よりも次を優先する。

```text
README.md
docs/design.md
docs/roadmap.md
docs/code_reference.md
docs/proof_records.md
```
