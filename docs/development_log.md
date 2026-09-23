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

Toda Proposition 5.6 から Lemma 5.16、安定 $G_0$ から $G_7$ までの主要な数学的証明経路。

## Phase 79–89

`docs/development_log/phases_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的定理 instance 適合性まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda 群問い合わせ、正規化済み群結果、EHP provenance、flat / recursive 証明 provenance、計算オーケストレーションの記録。

## Phase 96–98

```text
Phase 96:
構造化表示 / 読みやすい完全証明レポート
7609 passed in 121.63s

Phase 97:
計算からレポートまでのオーケストレーション
7609 passed in 121.63s

Phase 98:
生の n,k 入力用簡易 facade
7643 passed in 123.73s
```

詳細:

```text
docs/development_log/phases_096.md
docs/development_log/phases_097.md
docs/development_log/phases_098.md
```

## Phase 99

生成元中心の repository 探索を追加。

```text
GeneratorSymbol
→ 出現
→ 意味論的役割
→ グループ化表示
→ Markdown
→ 一括探索 facade
```

```text
7824 passed in 136.59s
```

## Phase 100

標準運用 repository、`build_standard_toda_report(n,k)`、`python main.py n k` を統合。

```text
8010 passed in 179.65s
```

## Phase 101

`docs/development_log/phases_101.md`

生成元中心の探索を標準 repository と `main.py explore` へ接続。

```text
8058 passed in 133.01s
```

## Phase 102

`docs/development_log/phases_102.md`

再帰的 proof-scope 探索、Toda membership、既知の写像関係探索を追加。

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
$$

```text
8142 passed in 129.93s
```

## Phase 103

`docs/development_log/phases_103.md`

適用可能な定理 / 補題の探索と関連度分類を追加。

```text
409 passed in 186.07s
```

## Phase 104

選択された適用候補を READY 検証、明示的 final rule による有界探索、事前構築済み report の実行へ接続。

```text
8644 passed in 374.63s
```

## Phase 105

第1 qualified production family を標準 applicability workflow へ接続。

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/development_log/phases_106.md`

適用可能性の性能 / 複雑性監査。

```text
797573 全 scope 候補
→ 176616 生成元関連候補
8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107

`docs/development_log/phases_107.md`

multi-family qualified execution へ拡張。

```text
8783 passed in 290.63s
```

## Phase 108

qualified execution を利用者向け workflow と CLI へ接続。

```text
生成元入力
→ 実行可能対象の解決
→ 曖昧性処理
→ 候補一覧
→ 候補選択
→ qualified execution
→ 結果 + 証明表示
```

```text
8850 passed in 380.25s
```

## Phase 109

既知群同一性、indexed sigma 具体化、known-group proof replay、`show-proof` を統合。

$$
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
$$

```text
8998 passed in 493.70s (0:08:13)
```

## Phase 110

既存 repository / proof-scope の operation fact を query / query-proof から利用可能にした。

```text
lookup != inference != evaluation
deduplicated presentation != provenance deletion
query-proof root = selected fact's own ProofStep
```

```text
9055 passed in 455.09s (0:07:35)
```

## Phase 111

CLI capability audit、global help、symbolic dimension 表示、3-term top-level composition query、replay `--depth`、safe fallback を追加。

```text
9074 passed in 446.27s (0:07:26)
```

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は archive file に追記するか、Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

## Phase 112

実際の数学的 workflow で capability pressure を監査。

```text
LOOKUP_MISS != evaluator required
```

を重要境界として確認し、`sigma_11` group-query orchestration gap を Phase 113 の対象に選定。

## Phase 113

既存 indexed $\sigma_n$ specialization を `TodaGroupQuery` 経路へ最小接続。

```text
query.k == 7
query.n >= 10
```

で既存 proof scope specialization を再利用。

```text
9081 passed in 434.58s (0:07:14)
```

## Phase 114

既存 Toda Proposition 5.6 の

$$
E^{n-5}\nu_5=\nu_n
$$

を再利用し、

$$
E(\nu_5)=\nu_6
$$

を exact handoff として operation query へ接続。

```text
9097 passed in 449.47s (0:07:29)
```

## Phase 115

既存 Toda Lemma 5.14 の $\sigma$-family definition を再利用し、

$$
E(\sigma_{11})=\sigma_{12}
$$

を exact handoff として接続。

```text
9111 passed in 432.54s (0:07:12)
```

## Phase 116

TeX-capable Web UI の readiness audit。

```text
Flask
KaTeX
thin Web adapter
structured presentation reuse
CLI output / Markdown は再解析しない
```

## Phase 117

最小 group-query Web UI を実装し、KaTeX 表示を確認。

## Phase 118

operation query / query-proof を Web UI へ接続。

```text
9169 passed in 465.97s (0:07:45)
```

## Phase 119

次の Web capability を監査し、`show-proof` を選定。

## Phase 120

known-group `show-proof` を Web UI へ接続。

```text
web_generator_proof.py
depth 0 / 1 / 2
safe fallback
```

```text
9184 passed in 453.04s (0:07:33)
```

## Phase 121

Phase 121 は Phase 120 後に残った read-only Web capability を再監査し、`explore` を最小の次対象として Web UI へ接続した。

新しい数学的 theorem、proof-search rule、qualified execution family、operation-query grammar は追加していない。

### Phase 121-1: remaining read-only Web capability audit

対象:

```text
explore
explore-proof
explore-applicable
```

監査結果:

```text
explore
→ existing facade
→ structured RepositoryGeneratorExplorationPresentation
→ conclusion_latex
→ grouped occurrence views
→ Web 化の境界が最も小さい

explore-proof
→ read-only
→ structured result はある
→ dedicated Web presentation boundary は explore より弱い

explore-applicable
→ rich structured presentation はある
→ source / rule family / candidate 階層と表示量が大きい
→ execute workflow に近い
```

`execute` は candidate selection・ambiguity・execution semantics を伴うため対象外とした。

### Phase 121-2: `explore` Web integration selection

```text
scope:
read-only direct generator exploration only

not included:
explore-proof
explore-applicable
execute
candidate selection
qualified execution
```

### Phase 121-3: Web adapter boundary design

```text
browser
→ Flask route
→ web_generator_exploration.py
→ explore_standard_repository_generator_input(...)
→ RepositoryGeneratorExplorationReport
→ RepositoryGeneratorExplorationPresentation
→ Web-specific immutable view
→ Jinja
→ KaTeX
```

CLI Markdown は解析しない。

### Phase 121-4: minimal implementation + focused tests

追加:

```text
web_generator_exploration.py
tests/test_phase121_4_web_generator_exploration.py
tests/test_phase121_4_web_app_generator_exploration.py
```

変更:

```text
web_app.py
templates/index.html
```

Web occurrence view:

```text
conclusion_latex
role_labels
phase
theorem
```

修正後:

```text
Phase 121 focused:
13 passed in 7.05s

existing Web compatibility:
40 passed in 10.14s
```

### Phase 121-5: browser/manual integration check

```text
nu_prime
→ Occurrences: 6

sigma_11
→ Occurrences: 0

eta_999
→ Occurrences: 0
```

```text
explore != explore-proof
direct occurrence != specialized proof-scope occurrence
```

### Phase 121-final: documentation / completion

```text
9197 passed in 455.68s (0:07:35)
```

Phase 121 は完了。

## Phase 122

Phase 122 は remaining read-only Web capability のうち `explore-proof` と `explore-applicable` を再監査し、`explore-proof` を最小の次対象として Web UI へ接続した。

新しい数学的 theorem、proof-search rule、qualified execution family、operation-query grammar、proof-scope semantics は追加していない。

### Phase 122-1: `explore-proof` / `explore-applicable` audit

```text
explore-proof
→ read-only
→ RepositoryProofScopeExplorationResult が既にある

explore-applicable
→ read-only
→ rich RepositoryGeneratorApplicabilityPresentation が既にある
→ source / rule family / candidate の階層が大きい
→ result volume が大きい
```

### Phase 122-2 / 122-3

`explore-proof` のみに限定し、既存 recursive proof-scope result を thin Web adapter から公開する設計を固定。

### Phase 122-4

追加:

```text
web_generator_proof_scope.py
tests/test_phase122_4_web_generator_proof_scope.py
tests/test_phase122_4_web_app_generator_proof_scope.py
```

focused tests:

```text
15 passed
```

### Phase 122-5

ブラウザで `nu_prime`、`sigma_11`、`eta_999` と既存 Web capability を確認。

```text
67 passed in 21.93s
```

### Phase 122-final

repository-wide regression:

```text
9212 passed in 455.16s (0:07:35)
```

Phase 122 は完了。

## Phase 123

Phase 123 は残っていた read-only Web capability `explore-applicable` を監査し、既存 applicability semantics を変えずに compact Web surface として接続した。

新しい数学的 theorem、proof-search rule、qualified execution family、query grammar、candidate-selection semantics は追加していない。

### Phase 123-1: current applicability audit

確認対象:

```text
RepositoryGeneratorApplicabilityExplorationResult
RepositoryGeneratorApplicabilityPresentation
ApplicabilitySourceGroupPresentation
ApplicabilityRuleFamilyPresentation
compact renderer
detailed renderer
CLI default compact behavior
```

既存 presentation が次をすでに保持することを確認した。

```text
source grouping
rule group
rule family
candidate identity
raw candidate count
relevance ordering
```

### Phase 123-2: Web exposure decision

Web は read-only compact 表示のみに限定。

公開:

```text
generator
proof-scope occurrence count
applicability candidate count
source count
rule-group count
rule-family count
source category
source statement
root
depth
source type
raw candidate count
rule family name
catalog-entry count
rule-family raw candidate count
```

非公開:

```text
candidate identity
candidate selection
fixed_point_safe
premise indexes
bindings
detailed toggle
qualified execution
execute action
```

### Phase 123-3: Web adapter boundary

```text
generator input
→ existing standard applicability facade
→ existing applicability presentation
→ thin Web immutable view
→ Jinja
→ KaTeX
```

source classification と relevance ordering は既存 presentation を再利用し、Web で再実装しない。

### Phase 123-4: minimal implementation + focused tests

追加:

```text
web_generator_applicability.py
tests/test_phase123_4_web_generator_applicability.py
tests/test_phase123_4_web_app_generator_applicability.py
```

変更:

```text
web_app.py
templates/index.html
```

focused tests:

```text
13 passed in 61.24s
```

### Phase 123-5: browser/manual integration audit

`nu_prime`:

```text
Proof-scope occurrences: 626
Applicability candidates: 176616
Source statements with candidates: 542
Rule groups: 123300
Rule families: 29308
```

source categories:

```text
Toda memberships: 46
Map relations: 44
Other statements: 452
```

機能・数学データ・KaTeX・zero-result semantics は正常だったが、全 source / rule family を HTML に展開すると browser output が大きすぎることを確認した。

`sigma_11`:

```text
1 occurrence
686 candidates
1 source
472 rule groups
112 rule families
```

`eta_999`:

```text
0 / 0 / 0 / 0 / 0
```

### Phase 123-5A: compact Web display volume fix

underlying applicability result を変更せず、Jinja の描画量だけを制限した。

```text
source:
各 category 先頭 5 件

rule family:
各 displayed source 先頭 10 件

details:
初期折りたたみ

summary:
全件数を維持

omitted:
省略件数を明示
```

focused regression:

```text
17 passed in 69.57s
```

### Phase 123-5B: browser/manual re-audit

`nu_prime`:

```text
full summary counts preserved
46 Toda memberships → first 5 rendered
44 map relations → first 5 rendered
452 other statements → first 5 rendered
large rule-family groups → first 10 rendered
omitted counts shown
```

`sigma_11`:

```text
compact display verified
rule-family details collapsed
```

`eta_999`:

```text
zero result preserved
no truncation message
```

Phase 123-5B は PASS。

### Phase 123-final: documentation / completion

更新対象:

```text
README.md
docs/design.md
docs/roadmap.md
docs/development_log.md
docs/proof_records.md
```

Phase 123 は新しい数学的 proof / theorem root を追加していない。`proof_records.md` には Web applicability presentation が proof truth ではないという境界のみ追記する。

repository-wide regression:

```text
python -m pytest -q
9229 passed in 509.16s (0:08:29)
```

Phase 123 は完了。

### Phase 123 後の境界

read-only Web capability の優先接続は一通り完了した。

次 Phase 124 は実装前監査とし、

```text
execute Web integration readiness
vs
current single-page Web UI organization / usability cleanup
```

の優先度を判断する。

`execute` は candidate selection・ambiguity・execution semantics を伴うため、read-only capability の延長として自動的に接続しない。
