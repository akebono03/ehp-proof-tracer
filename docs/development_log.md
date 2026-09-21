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

\(\pi_3^2\)、\(\pi_4^3\)、Toda Proposition 5.1、Lemma 5.2、\(\nu'\)、\(\nu_4\)、\(\nu\)-family、性能安定化まで。

## Phase 65–78

`docs/development_log/phases_065_078.md`

Toda Proposition 5.6 から Lemma 5.16、stable \(G_0\) から \(G_7\) までの主要な数学的証明経路。

## Phase 79–89

`docs/development_log/phases_079_089.md`

Proof Repository、repository-assisted inference、自動 rule 選択、有界 producer search、診断、depth parameterization、有限 retry、具体的 theorem-instance compatibility まで。

## Phase 90–95

`docs/development_log/phases_090_095.md`

Toda group query、正規化済み group result、EHP provenance、flat / recursive proof provenance、計算オーケストレーションの記録。

## Phase 96–98

```text
Phase 96:
structured presentation / readable full proof report
7609 passed in 121.63s

Phase 97:
calculation-to-report orchestration
7609 passed in 121.63s

Phase 98:
raw n,k convenience facade
7643 passed in 123.73s
```

詳細:

```text
docs/development_log/phases_096.md
docs/development_log/phases_097.md
docs/development_log/phases_098.md
```

## Phase 99

element-centered repository exploration を追加。

```text
GeneratorSymbol
→ occurrence
→ semantic role
→ grouped presentation
→ Markdown
→ one-shot exploration facade
```

```text
7824 passed in 136.59s
```

## Phase 100

standard production repository、`build_standard_toda_report(n,k)`、`python main.py n k` を統合。

```text
8010 passed in 179.65s
```

## Phase 101

`docs/development_log/phases_101.md`

generator-centered exploration を標準 repository と `main.py explore` へ接続。

```text
8058 passed in 133.01s
```

## Phase 102

`docs/development_log/phases_102.md`

recursive proof-scope exploration、Toda membership、known map relation discovery を追加。

代表結果:

\[
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
\]

```text
8142 passed in 129.93s
```

## Phase 103

`docs/development_log/phases_103.md`

applicable theorem / lemma discovery と relevance classification を追加。

```text
409 passed in 186.07s
```

## Phase 104

selected applicability candidate を READY validation、explicit-final-rule bounded search、prebuilt-report execution へ接続。

```text
8644 passed in 374.63s
```

## Phase 105

first qualified production family を standard applicability workflow へ接続。

対象:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/development_log/phases_106.md`

applicability performance / complexity audit。

```text
797573 full-scope candidates
→ 176616 generator-relevant candidates
```

generator-relevant scope prefilter を実装。

```text
8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107

`docs/development_log/phases_107.md`

first-family-only execution を multi-family execution へ拡張。

second qualified family:

```text
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

主要 capability:

```text
exact production-application recovery
NONE / UNIQUE / AMBIGUOUS recovery status
exact multi-premise seed
two-premise bounded execution integration
explicit root + source + family selection
generic qualified-family admission
family-name dispatch
multi-family standard facade
```

repository-wide:

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108

Phase 107 の internal qualified execution を user-facing workflow と CLI へ接続。

主要 capability:

```text
generator input
→ executable target resolution
→ ambiguity handling
→ candidate list
→ candidate selection
→ qualified execution
→ final executed ProofStep
→ Result + Proof presentation
→ CLI
```

CLI:

```text
python main.py execute nu_prime
python main.py execute nu_prime --candidate 1
```

Windows CP932 boundary を実 subprocess smoke で検出し、script entry point の stdout / stderr を UTF-8 化した。

repository-wide:

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109

Phase 108 後の operational audit から開始し、generator query の user-facing semantics と known-group proof replay を閉じた。

主要な流れ:

```text
known-group identity
→ proof-derived ambient fallback
→ indexed sigma specialization
→ proof-scope integration
→ qualified-execution boundary audit
→ known-group proof replay
→ show-proof
→ statement rendering coverage
→ user-facing ordering closure
```

Toda Proposition 5.15:

\[
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

concrete indexed specialization は \(n\ge 10\) に限定し、symbolic higher step を direct premise として保持する。

known-group proof replay:

```text
generator
→ unique known-group identity node
→ existing ProofStep
→ direct provenance
→ show-proof
```

qualified theorem execution:

```text
generator
→ executable-target resolver
→ qualified theorem application
→ bounded execution
→ execute
```

確定した境界:

```text
show-proof != execute
candidate number != theorem ranking
concrete sigma_n specialization != third qualified execution family
```

最終 repository-wide regression:

```text
8998 passed in 493.70s (0:08:13)
```

Phase 109 は完了。

## Phase 110

Phase 110 は user-facing mathematical operation query の実需要監査から開始し、既存 repository / proof-scope にすでに表現されている数学的 operation fact を直接検索・表示・proof replay できる経路を追加した。

主要サブフェーズ:

```text
110-1:
user-facing mathematical operation query capability audit

110-2:
query input / syntax boundary audit

110-3:
existing-relation lookup design

110-4:
minimal operation query implementation boundary audit

110-5:
minimal operation query core implementation

110-6:
operation query CLI integration

110-7:
operation query result deduplication / prioritization audit

110-8:
deduplicated presentation implementation

110-9:
operation query proof replay / provenance detail audit

110-10:
operation query proof replay implementation

110-11:
proof replay statement presentation audit

110-12:
proof replay statement presentation implementation

110-13:
feature completion / regression audit
```

最小 query grammar:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

代表 CLI:

```text
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"
```

代表結果:

\[
H(\nu')=\eta_5,
\qquad
H(\nu')=E^2\eta_3,
\]

\[
\Delta(\iota_9)
=
\pm(2\nu_4-E\nu'),
\]

\[
E\eta_2\nu'=0.
\]

operation query は evaluator ではない。

```text
lookup != inference != evaluation
```

raw proof-scope occurrences は保持し、presentation layer だけで equal mathematical statement を group 化する。

```text
deduplicated display
!= provenance deletion
```

`query-proof` を追加。

```text
python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 2
python main.py query-proof "E(eta_2 o nu_prime)"
python main.py query-proof "eta_2 o nu_prime" --fact 4
```

proof replay root は enclosing theorem aggregate ではなく、選択された fact 自身の `ProofStep`。

\[
H(\nu')=\eta_5
\]

の direct replay は

\[
H(\nu')=E^2\eta_3,
\qquad
E^2\eta_3=\eta_5
\]

を表示する。

multiple facts のときは silent auto-selection を行わず `--fact N` を要求する。

proof replay statement presentation では既知 semantics を数学表示し、未知 aggregate は raw Python repr ではなく safe type-name fallback にする。

代表:

\[
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
\]

\[
E^2\nu'\in2\iota_5\circ\pi_8^5,
\]

\[
\Delta:\pi_8^5\to\pi_6^2
\quad\text{is surjective}.
\]

Phase 110 最終確認:

```text
python -m pytest -q
9055 passed in 455.09s (0:07:35)

git diff --check
clean
```

representative smoke:

```text
query
query-proof
execute
show-proof
python main.py 5 3
```

すべて正常。

Phase 110 は完了。

---

# 現在の運用方針

`development_log.md` は索引として維持する。

詳細な新規開発記録は archive file に追記するか、Phase 範囲に応じて新しい archive file を追加する。

既存履歴は原則として削除せず、誤りが確定した場合のみ必要な訂正を行う。

現在 capability の確認では次を優先する。

```text
README.md
docs/design.md
docs/roadmap.md
docs/code_reference.md
docs/proof_records.md
```

次 Phase は Phase 110 の operation query / proof replay を前提に、CLI 全体の利用者視点の残課題と、次に実需要のある最小 capability を監査して開始する。
