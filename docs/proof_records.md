# EHP Proof Tracer — 証明記録

この文書は、代表的な数学的証明および証明基盤の記録索引である。

詳細な過去記録は内容を削除せず `docs/proof_records/` 以下へ保存する。

現在の設計は `docs/design.md`、開発履歴は `docs/development_log.md`、今後の計画は `docs/roadmap.md` を参照する。

---

# 数学的証明記録

## 初期記録 / Toda Equation (5.8)

`docs/proof_records/early_records_and_toda_5_8.md`

## Toda Lemma 5.7 から Lemma 5.10

`docs/proof_records/toda_5_7_to_5_10.md`

## Toda Proposition 5.11 から Lemma 5.16

`docs/proof_records/toda_5_11_to_5_16.md`

## Stable stems \(G_0\) から \(G_7\)

`docs/proof_records/stable_stems_g0_g7.md`

---

# 証明基盤の記録

## Phase 79–89

`docs/proof_records/proof_infrastructure_079_089.md`

Proof Repository、repository-assisted inference、自動 rule 選択、有界 producer search、診断、depth parameterization、有限 retry、具体的 theorem-instance filtering の記録。

## Phase 90–101

Toda group query、group normalization、EHP / proof provenance、presentation / report、standard production repository、CLI、generator exploration の記録。

## Phase 102

`docs/proof_records/production_proof_scope_exploration_102.md`

代表結果:

\[
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
\]

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

```text
applicability candidate != proof success
relevance category != theorem truth
presentation order != theorem ranking
```

## Phase 104

selected candidate を READY validation、explicit-final-rule bounded search、prebuilt report execution へ接続。

```text
candidate rule
is validation.execution_entry.rule
is search_result.final_rule
is goal_step.inference_rule
```

```text
8644 passed in 374.63s
```

## Phase 105

最初の standard qualified family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
```

```text
8709 passed in 659.02s
```

## Phase 106

`docs/proof_records/performance_applicability_106.md`

```text
797573 full-scope candidates
→ 176616 generator-relevant candidates
```

```text
8.16 s / 62.42 MiB
8712 passed in 337.86s
```

## Phase 107 multi-family qualified execution provenance

Phase 107 は新しい数学的 theorem truth を追加していない。

admission 済み family:

```text
toda_58_delta_iota9_nu4_nu_prime_inference_rule
toda_lemma57_pi6_2_eta2_nu_prime_inference_rule
```

second family は既存の

\[
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\}
\]

を導く2-premise production rule である。

multi-premise candidate から companion premise を任意探索せず、同じ root / rule / goal / source identity を満たす既存 production application を一意に recovery する。

repository-wide:

```text
8783 passed in 290.63s
```

Phase 107 は完了。

## Phase 108 user-facing execution provenance

Phase 108 は新しい数学的 theorem truth を追加していない。

generator input から qualified execution と actual `ProofStep` provenance を利用できる user-facing path を追加した。

```text
generator input
→ executable target resolution
→ ambiguity-safe candidate selection
→ qualified execution
→ executed goal_step
→ Result + Proof
```

candidate number は 1-based addressing であり theorem ranking ではない。

```text
candidate number != theorem ranking
```

Windows CP932 boundary を実 subprocess smoke で検出し、script entry point の stdout / stderr を UTF-8 に統一した。

repository-wide:

```text
8850 passed in 380.25s
```

Phase 108 は完了。

## Phase 109 known-group identity / proof replay provenance

Phase 109 は新しい独立した数学的 theorem root を追加していない。

既存の Toda Proposition 5.15 symbolic proof、既存 repository proof scope、既存 qualified execution semantics を保持したまま、known-group identity と proof replay の user-facing path を追加した。

### Proof-derived ambient-group fallback

explicit ambient-group fact がない generator でも、既存 proof scope の group relation が generator を direct generator として持ち、target group が一意なら known-group identity に利用できる。

代表例:

```text
nu_5
sigma'''
sigma''
sigma'
sigma_8
sigma_9
```

### Indexed sigma specialization

Toda Proposition 5.15:

\[
\pi_{n+7}^{n}=\mathbb Z/16\{\sigma_n\},
\qquad n\ge 9.
\]

concrete integer index \(n\ge 10\) に対して theorem-specific specialization を導入した。

例:

\[
\pi_{18}^{11}=\mathbb Z/16\{\sigma_{11}\},
\]

\[
\pi_{19}^{12}=\mathbb Z/16\{\sigma_{12}\}.
\]

concrete specialization step は symbolic higher step を direct premise とする。

```text
concrete specialization
→ symbolic Proposition 5.15 higher step
```

arbitrary symbolic AST rewrite は行わない。

### Known-group proof replay

```text
generator
→ unique known-group identity node
→ existing ProofStep
→ direct ancestry
→ presentation
```

qualified execution wrapper を流用しない。

```text
show-proof != execute
```

repository-wide:

```text
8998 passed in 493.70s (0:08:13)
```

Phase 109 は完了。

## Phase 110 operation query / proof replay provenance

Phase 110 は新しい数学的 theorem truth を追加していない。

既存 repository / proof-scope にすでに存在する relation・map statement・composition-containing statement を user-facing query から検索し、その既存 `ProofStep` provenance を保持したまま表示・replay する経路を追加した。

### Operation query parser

最小 grammar:

```text
H(<operand>)
E(<operand>)
Delta(<operand>)
<generator> o <generator>
```

代表:

```text
H(nu_prime)
Delta(iota_9)
E(eta_2 o nu_prime)
eta_2 o nu_prime
```

parser は evaluator input を作らない。

```text
query specification
!= mathematical evaluation request
```

### Existing fact lookup

`H` は既存 map-relation exploration を再利用する。

`E` は既存 repository 表現の `MapApplication(E, ...)` と `Suspension(...)` を lookup semantics で認識する。

\(\Delta\) は既存 `TodaDeltaImageUpToSignStatement` を保持する。

composition query は exact `Composition` containment を探索する。

代表結果:

\[
H(\nu')=\eta_5,
\]

\[
H(\nu')=E^2\eta_3,
\]

\[
\Delta(\iota_9)
=
\pm(2\nu_4-E\nu'),
\]

\[
\Delta(\iota_9)
=
\pm[\iota_4,\iota_4],
\]

\[
E\eta_2\nu'=0.
\]

重要:

```text
lookup != inference != evaluator
```

### Raw provenance preservation

同じ `ProofStep` が複数 repository root の ancestry に現れることは provenance 上正当である。

したがって raw lookup occurrence は削除しない。

presentation layer のみ equal statement を group 化する。

```text
raw matches
→ equal mathematical statement grouping
→ presentation item
```

各 presentation item は元の全 match を保持する。

```text
deduplicated presentation
!= raw provenance deletion
```

### Presentation priority

primary display order は shallowest proof-scope depth と stable source order に基づく。

これは theorem ranking ではない。

### Operation-query proof replay

`query-proof` は selected fact の primary match を使う。

replay root:

```text
selected presentation item
→ primary_match
→ scope_node.proof_step
```

enclosing repository theorem root ではない。

例えば

\[
H(\nu')=\eta_5
\]

を replay すると depth 0 はこの relation 自身であり、direct premises として

\[
H(\nu')=E^2\eta_3,
\qquad
E^2\eta_3=\eta_5
\]

を保持する。

```text
operation-query proof replay
!= repository theorem replay
```

### Multiple fact safety

multiple facts では silent auto-selection をしない。

```text
1 fact
→ --fact 省略可

multiple facts
→ --fact N が必要
```

`--fact` は 1-based addressing であり theorem ranking ではない。

### Statement presentation

既存 generic renderer で数学表示できる statement はそのまま利用する。

Phase 110 で追加した narrow presentation:

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

未知 aggregate は意味を推測せず safe type-name fallback とする。

```text
`TodaProp56FiniteDimensionalStatement`
```

raw dataclass repr を user-facing replay に漏らさない。

### CLI

```text
python main.py query "H(nu_prime)"
python main.py query "Delta(iota_9)"
python main.py query "E(eta_2 o nu_prime)"
python main.py query "eta_2 o nu_prime"

python main.py query-proof "H(nu_prime)" --fact 1
python main.py query-proof "H(nu_prime)" --fact 2
python main.py query-proof "E(eta_2 o nu_prime)"
python main.py query-proof "eta_2 o nu_prime" --fact 4
```

### Closure

最終 repository-wide regression:

```text
9055 passed in 455.09s (0:07:35)
```

whitespace check:

```text
git diff --check
clean
```

representative smoke では `query`、`query-proof`、`execute`、`show-proof`、`python main.py 5 3` が正常に動作した。

Phase 110 は完了。

---

# 記録原則

数学的な根拠は `ProofStep` と、その実際の premise ancestry である。

```text
proof record != proof truth
presentation != proof truth
production repository assembly != theorem truth
exploration result != new theorem truth
proof-scope traversal != theorem search
applicability candidate != successful proof
relevance category != theorem truth
candidate ordering != theorem ranking
handoff validation != theorem truth
bounded search report != executed proof
qualified candidate != unique execution target
execution-family representative != theorem ranking
generic qualification != concrete execution success
production-application recovery != new theorem truth
family dispatch != theorem ranking
performance optimization != theorem truth
user-facing resolver != theorem ranking
candidate number != theorem priority
candidate-list presentation != proof truth
executed conclusion equality != repository target object identity
CLI rendering != new theorem truth
known-group identity lookup != qualified execution
proof-derived ambient fallback != new theorem truth
symbolic specialization != arbitrary AST rewriting
proof-scope specialization != theorem execution
known-group proof replay != theorem application execution
show-proof != execute
operation query lookup != evaluator
operation query result != new theorem truth
deduplicated presentation != provenance deletion
presentation order != theorem ranking
query-proof fact number != theorem priority
query-proof replay != enclosing theorem replay
safe type fallback != invented theorem branch
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。
