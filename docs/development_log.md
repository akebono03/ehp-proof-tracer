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

初回 focused test は `nu_prime` の Toda-bracket group が必ず非空という誤ったテスト前提により1件失敗した。

```text
1 failed, 12 passed
```

production code を再監査し、group は空でもよいことを確認。テストを「既存 presentation と Web view の grouping が一致する」不変条件へ修正した。

修正後:

```text
Phase 121 focused:
13 passed in 7.05s

existing Web compatibility:
40 passed in 10.14s
```

### Phase 121-5: browser/manual integration check

`nu_prime`:

```text
Occurrences: 6
Group generators
Composition left
Composition right
Roles
Phase
Theorem
KaTeX
```

`sigma_11`:

```text
Occurrences: 0
```

これは Web adapter の不具合ではない。

```text
explore sigma_11
→ standard production repository の direct occurrence は 0

explore-proof sigma_11
→ specialized recursive proof-scope occurrence を得られる
```

したがって、

```text
explore != explore-proof
direct occurrence != specialized proof-scope occurrence
```

という既存境界を維持した。

`eta_999`:

```text
Occurrences: 0
```

unknown indexed generator は正常な zero-occurrence result として表示した。

既存 Web capability も確認:

```text
group query n=11, k=7
operation query / query-proof E(sigma_11)
generator proof
KaTeX
```

### Phase 121-final: documentation / completion

更新対象:

```text
README.md
docs/design.md
docs/roadmap.md
docs/development_log.md
```

Phase 121 は新しい数学的 proof / theorem root / ProofStep provenance を追加していないため、`docs/proof_records.md` は変更しない。

repository-wide regression:

```text
python -m pytest -q
9197 passed in 455.68s (0:07:35)
```

Phase 121 は完了。

### Phase 121 後の境界

remaining read-only Web capability:

```text
explore-proof
explore-applicable
```

`execute` は引き続き read-only capability より後段とする。

次 Phase は remaining read-only capability を再監査し、structured presentation boundary と browser 表示量を比較してから、必要なら1 capability だけを選ぶ。
