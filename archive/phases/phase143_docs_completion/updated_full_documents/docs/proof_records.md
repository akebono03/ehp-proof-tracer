# EHP Proof Tracer — 証明記録

この文書は、代表的な数学的証明および証明基盤の記録索引である。

詳細な過去記録は内容を削除せず `docs/proof_records/` 以下へ保存する。

現在の設計は `docs/design.md`、開発履歴は `docs/development_log.md`、今後の計画は `docs/roadmap.md` を参照する。

---

# 数学的証明記録

## 初期記録 / Toda 式 (5.8)

`docs/proof_records/early_records_and_toda_5_8.md`

## Toda Lemma 5.7 から Lemma 5.10

`docs/proof_records/toda_5_7_to_5_10.md`

## Toda Proposition 5.11 から Lemma 5.16

`docs/proof_records/toda_5_11_to_5_16.md`

## 安定 stem \(G_0\) から \(G_7\)

`docs/proof_records/stable_stems_g0_g7.md`

---

# 証明基盤の記録

## Phase 79–89

`docs/proof_records/proof_infrastructure_079_089.md`

証明 Repository、repository 支援推論、自動規則選択、有界 producer 探索、診断、depth パラメータ化、有限 retry、具体的定理 instance filtering の記録。

## Phase 90–101

Toda 群問い合わせ、群正規化、EHP / 証明 provenance、表示 / レポート、標準運用 repository、CLI、生成元探索の記録。

## Phase 102

`docs/proof_records/production_proof_scope_exploration_102.md`

代表結果:

$$
\nu' \in \{\eta_3,2\iota_4,\eta_4\}_1,
\qquad
H(\nu')=\eta_5.
$$

## Phase 103

`docs/proof_records/applicable_theorem_relevance_103.md`

```text
適用候補 != 証明成功
関連度カテゴリ != 定理事実
表示順 != 定理順位付け
```

## Phase 104–108 qualified execution provenance

Phase 104–108 は applicability candidate から安全な qualified execution と user-facing execute workflow までを構築した。

Phase 108 final:

```text
8850 passed in 380.25s
```

## Phase 109–113

known-group identity、indexed \(\sigma_n\)、proof replay、operation query、CLI audit、symbolic specialization reuse を整備。

```text
Phase 109: 8998 passed in 493.70s
Phase 110: 9055 passed in 455.09s
Phase 113: 9081 passed in 434.58s
```

## Phase 114 `E(nu_5)` handoff provenance

$$
E(\nu_5)=\nu_6.
$$

```text
concrete specialization
!= new theorem root
!= general E evaluator
```

## Phase 115 `E(sigma_11)` handoff provenance

$$
E(\sigma_{11})=\sigma_{12}.
$$

```text
concrete definitional specialization
!= new theorem root
!= general E evaluator
```

## Phase 116–125 Web provenance boundary

```text
Web UI != proof truth
Web proof replay != new proof search
Web execution adapter != execution semantics
candidate selection form != theorem ranking
```

## Phase 126 executable relevance provenance boundary

```text
proof-scope relevance
!= applicability relevance
!= executable relevance
```

## Phase 127 capability pressure provenance audit

operation-query 残件を監査。

## Phase 128 `E(nu_5 o eta_8)=0` handoff provenance

$$
E(\nu_5\eta_8)=0.
$$

直接 premise:

$$
\pi_{10}^6=0.
$$

```text
theorem-specific specialized query fact
!= repository mutation
!= new independent theorem root
```

## Phase 129 `E(nu_prime)` membership handoff provenance

source fact:

$$
\pi_7^4=
\mathbb Z\{\nu_4\}
\oplus
\mathbb Z/4\{E\nu'\}.
$$

採用:

$$
E\nu' \in \pi_7^4.
$$

```text
membership specialized step
→ existing pi_7^4 decomposition
→ existing Proposition 5.6 ancestry
```

final:

```text
9268 passed in 569.71s (0:09:29)
```

Phase 129 完了。

---

# Phase 130 standard-query provenance

Phase 130 は新しい数学定理を増やすのではなく、既存証明を standard query から正しく利用できるようにする provenance orchestration を整備した。

## low-dimensional recovery

既存 proof ancestry から concrete group result を回収。

代表:

$$
\pi_3^2,\quad
\pi_4^3,\quad
\pi_4^2,\quad
\pi_5^3.
$$

```text
existing ProofStep reuse
!= new theorem fact
```

## stable family specialization

$$
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\},
$$

$$
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\},
$$

$$
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\},
$$

$$
\pi_{n+4}^n=0,
$$

$$
\pi_{n+5}^n=0,
$$

$$
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\}.
$$

generic specialization は theorem の range guard を維持し、低次元 concrete branch を上書きしない。

## foundational query results

### diagonal

$$
\pi_n^n\cong\mathbb Z\{\iota_n\}.
$$

### circle

既存 Phase 56 symbolic result を再利用:

$$
\pi_{i-1}^1=0.
$$

### connectivity

$$
1\le n+k<n
\Rightarrow
\pi_{n+k}^n=0.
$$

この connectivity zero は repository-backed `TodaGroupResult` として `ProofStep` を保持する。

### \(\pi_0\) boundary

$$
n+k=0
$$

は ordinary `TodaGroupResult` とせず、path component information として分離。

### negative dimension

$$
n+k<0
$$

は classical unstable domain 外として分離。

```text
negative stem accepted
!= negative homotopy group normalized to zero
```

## \(\pi_{16}^9\) concrete sigma provenance

Toda Proposition 5.15 ancestry には既に

$$
\pi_{16}^{9}
=
\mathbb Z/16\{\sigma_9\}
$$

の concrete `ProofStep` が存在する。

Phase 130-11 はこの node を standard query に接続した。

```text
n=9,k=7
→ standard.toda.prop515 proof scope
→ exact pi16_9 concrete node
→ normalized group result
```

generic indexed sigma specialization の境界は \(n\ge10\) のまま。

```text
pi16_9 concrete recovery
!= generic sigma specialization
!= new theorem root
```

## repository boundary

Phase 130 の specialization / concrete recovery は standard repository root を変更しない。

```text
standard.toda.prop56
standard.toda.prop58
standard.toda.prop511
standard.toda.prop515
```

を維持。

## regression boundary

```text
python -m pytest tests -q
9308 passed in 577.02s (0:09:37)
```

Phase 130 完了。

---

# Phase 131 group-result proof replay provenance

Phase 131 は新しい数学的証明を追加せず、既存の group result が保持している `ProofStep` を user-facing replay に接続した。

## identity boundary

`TodaGroupResult` は

```text
source_entry
proof_step
```

を保持する。

不変条件:

```text
group_result.proof_step is group_result.source_entry.step
```

Phase 131 replay はこの identity を維持する。

```text
group-result replay
!= proof reconstruction
!= theorem lookup by generator
!= new theorem root
```

## recursive provenance reuse

既存:

```text
extract_toda_recursive_proof_provenance(group_result)
```

を再利用。

保持情報:

```text
root ProofStep
shortest depth
role
proof edges
ProofStep identity
```

Phase 131 core API はこの provenance を depth で切り出すだけであり、新しい graph traversal semantics を導入しない。

## representative result

$$
\pi_{16}^{9}
=
\mathbb Z/16\{\sigma_9\}.
$$

root provenance:

```text
Theorem: Toda Proposition 5.15
Phase: 75
Repository key: standard.toda.prop515::pi16_9
```

depth 1 では既存 premise として Toda (4.8)、Lemma 5.14、\(\sigma\)-family definition、\(\pi_{12}^{5}\) 群結果などを辿る。

depth 2 ではさらに \(\sigma''\)-bridge、\(\sigma'\) branch、\(\pi_{14}^{7}\)、Lemma 5.13 など既存 premise ancestry を辿る。

```text
displayed ancestry
!= new proof synthesis
```

## zero-group replay

$$
\pi_9^2=0
$$

は generator を持たないが、`TodaGroupResult.proof_step` を直接 root にするため replay 可能。

```text
zero group
!= no proof
```

## connectivity-zero replay

Phase 130 foundational result:

$$
\pi_{10}^{11}=0
$$

は

```text
Theorem: Sphere connectivity
Phase: 130
```

を持つ repository-backed group result なので replay 可能。

premise を持たないため、現状では depth 0 のみとなる。

## domain-only boundary

$$
\pi_0(S^n)
$$

の path-component information と、負次元 out-of-domain information は ordinary `TodaGroupResult` ではない。

したがって:

```text
domain-only information
!= group-result proof replay target
```

## CLI / Web presentation boundary

CLI:

```powershell
python main.py group-proof 9 7
python main.py group-proof 9 7 --depth 2
```

Web:

```text
Group query
→ Result
→ Proof depth 0 / 1 / 2
→ Show proof
```

CLI / Web は同じ group-result proof replay core を利用する。

```text
CLI renderer != proof truth
Web renderer != proof truth
```

## regression boundary

focused:

```text
Phase 131-3: 8 passed in 2.73s
Phase 131-4: 14 passed in 7.61s
Phase 131-5: 39 passed in 17.21s
```

repository-wide final:

```text
python -m pytest tests -q
9333 passed in 583.64s (0:09:43)
```

Phase 131 完了。

---

# Phase 132 deterministic proof presentation provenance

Phase 132 は既存 proof trace を Trace / Outline / Narrative へ表示する presentation layer を実装した。

数学的 ground truth は引き続き `ProofStep` と実際の premise ancestry である。

## common presentation core

追加:

```text
TodaGroupProofPresentation
```

source:

```text
TodaGroupResultProofReplayResult
```

nodes:

```text
replay.steps
```

edges:

```text
existing recursive provenance edges
→ replay で選択済み node のみに filter
```

重要:

```text
presentation edge
!= flat depth から推測した edge
```

`ProofStep.premises` 由来の実 edge を使用する。

## Trace provenance boundary

Trace は Phase 131 replay の監査表示であり、Phase 132 でも ground truth presentation として維持する。

```text
Trace
→ Depth / Role / Rule / statement
```

Phase 132 は Trace semantics を変更しない。

## Outline provenance boundary

Outline は presentation edge を hierarchy として表示する。

同じ parent の premise は `premise_index` 順。

```text
Outline hierarchy
→ actual premise edge

Outline hierarchy
!= shortest_depth の差分から推測
```

shared dependency は graph 上複数 parent から参照されるため、Outline に複数位置で現れても graph の重複ではない。

## Narrative provenance boundary

Narrative は固定テンプレートで presentation graph を文章化する。

```text
〜を用いる。
これらから、〜を得る。
したがって、〜を得る。
```

unsupported statement は安全な existing renderer / rule name / type name fallback を使う。

```text
Narrative
!= new proof fact
!= theorem inference
!= guessed mathematical paraphrase
!= free-form LLM proof
```

## sibling order / causal order boundary

\(\pi_{16}^{9}\) の DAG では direct premise が別 premise の ancestry にも使われる。

したがって:

```text
root premise_index order
!= Narrative global first-occurrence order
```

Narrative は dependency-first でよい。

## shared dependency dedup provenance boundary

Phase 132-8 では `ProofStep` identity で Narrative subtree の再展開を抑制。

```text
first occurrence
→ expand subtree

later occurrence
→ 既出の...を用いる。
```

ただし:

```text
Narrative dedup
!= ProofStep deletion
!= proof edge deletion
!= repository mutation
```

Trace / Outline は変更しない。

## CLI presentation boundary

```powershell
python main.py group-proof 9 7 --mode trace
python main.py group-proof 9 7 --mode outline
python main.py group-proof 9 7 --mode narrative
```

default:

```text
trace
```

Phase 131 compatibility を維持。

## Web presentation boundary

Web group proof:

```text
Proof depth: 0 / 1 / 2
Proof view: Trace / Outline / Narrative
```

Outline / Narrative は同じ renderer を再利用。

Web adapter は mathematical fragment を `data-latex` へ分離するだけで、proof semantics を再実装しない。

```text
Web adapter
!= second proof graph
!= second narrative engine
```

## regression boundary

focused / related:

```text
Phase 132-4: 10 passed / related 35 passed
Phase 132-5: 8 passed / related 43 passed
Phase 132-6: 9 passed / related 52 passed
Phase 132-7: 9 passed / related 61 passed
Phase 132-8: 8 passed / related 69 passed
Phase 132-9: 15 passed / related 84 passed
```

repository-wide final:

```text
python -m pytest tests -q
9392 passed in 587.98s (0:09:47)
```

Phase 132 完了。

---

# Phase 133 Narrative presentation provenance

Phase 133 は Phase 132 の proof graph / replay を変更せず、既存 statement を人間向けに表示する Narrative presentation のみを改善した。

数学的 ground truth は引き続き

```text
ProofStep
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

## presentation-only boundary

Phase 133 で追加した human-readable label は、statement type の**表示名**である。

```text
human-readable Narrative label
!= theorem fact
!= new inference rule
!= statement semantic rewrite
!= new proof edge
!= new theorem root
```

表示優先順:

```text
existing LaTeX renderer
→ explicit Narrative label
→ inference rule name
→ statement type name
```

明示的 label がない statement では safe fallback を維持する。

## shared dependency wording boundary

Phase 132 の shared-dependency dedup 自体は維持。

Phase 133 では表示文面のみ変更。

```text
first occurrence
→ subtree を通常展開

nested immediate reuse
→ 重複展開しない

必要な再参照
→ すでに得た ... を用いる。
```

接続語:

```text
premise 1件
→ このことから

premise 2件以上
→ これらから
```

```text
wording change
!= proof graph change
!= provenance deletion
```

## representative human-readable labels

代表的に以下を明示表示した。

```text
Toda (5.2) の η₂ 合成同型
ν′ に対する Lemma 5.2 の Toda bracket 特殊化
Toda (5.5) の ν-family 有限次元結果
Toda (5.6) の ν₄ 分解
Toda (5.6) の ν₄ 分解同型
Δ 写像が零写像であること
Hopf 写像の単射性
E²: π₆³ → π₈⁵ の単射性
π₈⁵ / E²π₆³ が位数 2 であること
Toda Proposition 5.1 の有限次元結果
Toda Proposition 5.6 の有限次元結果
Toda Proposition 5.11 の有限次元結果
π₁₂⁵ の位数 2 の Hopf 像への同型
Toda Lemma 5.13 の σ‴ に関する結果
Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係
Toda Lemma 5.14 の σ′ に関する結果
Toda Lemma 5.14 の σ₈ に関する結果
π₁₆⁹ の位数 16 と E⁴ の単射性
σ-family の定義
```

これらは既存 proof statement の表示のみを改善する。

## representative audit boundary

最終監査対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9
$$

depth 1 / 2 の10ケースを確認。

結果:

```text
Internal wording audit
→ 0件

Old / awkward Narrative wording
→ 0件
```

\(\pi_{16}^{9}\) depth 2 の代表表示:

```text
Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係
Toda Lemma 5.14 の σ′ に関する結果
Toda Lemma 5.14 の σ₈ に関する結果
σ-family の定義
```

## regression boundary

focused:

```text
43 passed in 14.16s
```

repository-wide final:

```text
python -m pytest tests -q
9403 passed in 605.52s (0:10:05)
```

Phase 133 完了。

---

# Phase 134–136 Narrative proof presentation record

Phase 134–136 では proof graph / theorem fact を変更せず、代表証明を人間が読める数学的 Narrative として表示する経路を改善した。

## \(\pi_6^3\) final Narrative structure

対象:

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

### Toda bracket の定義順序

Toda Lemma 5.2 の適用では

$$
2\alpha=0
$$

が

$$
\{\eta_3,2\iota_4,E\alpha\}_1
$$

を定義するための条件になる。

\(\alpha=\eta_3\) として、まず

$$
2\eta_3=0
$$

を確認する。

その後

$$
\{\eta_3,2\iota_4,\eta_4\}_1
$$

が定義でき、この bracket のある元を \(\nu'\) と定める。

$$
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1.
$$

Lemma 5.2 より

$$
\nu'\in\pi_6^3,
\qquad
H(\nu')=\eta_5,
\qquad
2\nu'=\eta_3^3.
$$

### Toda Proposition 2.2

右合成公式

$$
H(\alpha\circ E\beta)
=
H(\alpha)\circ E\beta
$$

を \(\alpha=\nu'\)、\(\beta=\eta_5\) に適用する。

$$
\eta_6=E\eta_5
$$

なので

$$
H(\nu'\eta_6)
=
H(\nu'\circ E\eta_5)
=
H(\nu')\circ E\eta_5
=
\eta_5\eta_6
=
\eta_5^2.
$$

### EHP exact sequence

位数決定では

$$
\pi_7^3
\xrightarrow{H}
\pi_7^5
\xrightarrow{\Delta}
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
$$

を用いる。

$$
\pi_7^5=\mathbb Z/2\{\eta_5^2\}
$$

かつ \(H(\nu'\eta_6)=\eta_5^2\) なので

$$
H:\pi_7^3\to\pi_7^5
$$

は全射。

完全性から

$$
\operatorname{Im}H
=
\ker\Delta
=
\pi_7^5
$$

となり、

$$
\Delta:\pi_7^5\to\pi_5^2
$$

は零写像。

さらに

$$
\operatorname{Im}\Delta
=
\ker E
=
0
$$

なので

$$
E:\pi_5^2\to\pi_6^3
$$

は単射。

### final short exact sequence

$$
H(\nu')=\eta_5,
\qquad
\pi_6^5=\mathbb Z/2\{\eta_5\}
$$

より

$$
H:\pi_6^3\to\pi_6^5
$$

は全射。

したがって

$$
0
\longrightarrow
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
\longrightarrow
0.
$$

$$
\pi_5^2=\mathbb Z/2\{\eta_2^3\},
\qquad
\pi_6^5=\mathbb Z/2\{\eta_5\}
$$

なので \(\pi_6^3\) の位数は 4。

一方、

$$
2\nu'=\eta_3^3
$$

かつ \(\eta_3^3\) の位数が 2 なので \(\nu'\) の位数は 4。

よって

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

## presentation / provenance boundary

```text
Narrative ordering
!= theorem fact change

explicit Toda Proposition 2.2 formula
!= new operation evaluator

connected EHP sequence display
!= new EHP semantics

short exact sequence display
!= new group engine

Web KaTeX adapter
!= proof truth
```

focused regression:

```text
65 passed in 15.85s
```

repository-wide final:

```text
9517 passed in 575.31s (0:09:35)
```

Phase 136-2 完了。

# Phase 137 Web presentation / provenance record

Phase 137 は proof fact、proof graph、theorem root、operation semantics を 変更せず、Web と文書の presentation のみを整理した。

## static Group query math

Web の Group query 説明にある project quantity

$$
\pi_{n+k}^{n}
$$

を既存 `data-latex` / KaTeX 経路へ接続した。

```text
static Web math rendering
!= new group fact
!= group-query normalization
!= proof step
```

## provenance separator cleanup

template に残っていた mojibake `窶・` は provenance data 自体ではなく、表示 separator の encoding 崩れだった。

Phase 137 では過去の正常表示と同じ em dash `—` へ戻した。

```text
separator repair
!= provenance metadata change
!= theorem / phase value change
!= repository key change
```

実画面では Generator execution の

```text
Toda Proposition 5.8 — Phase 68
```

などを確認した。

## input syntax boundary

```text
H(nu_prime)
E(nu_5)
sigma_11
```

は parser / generator input の例であり、数学表示用 TeX ではない。

したがって Phase 137 でも plain text を維持した。

## documentation display-math boundary

主要文書の display math delimiter は GitHub Markdown で確実に表示されるよう `$$ ... $$` へ統一した。

```text
documentation delimiter normalization
!= proof normalization
!= theorem statement rewrite
!= mathematical semantics change
```

focused / related regression:

```text
Phase 137-2: 3 passed in 6.96s
Phase 137-3: 56 passed in 20.23s
```

repository-wide final regression は Phase 137 final でのみ実行する。

---
# 記録原則

数学的な根拠は `ProofStep` と、その実際の premise ancestry である。

```text
証明記録 != 証明事実
表示 != proof truth
production repository の組み立て != 定理事実
探索結果 != 新しい定理事実
proof-scope 走査 != 定理探索
適用候補 != 成功した証明
候補番号 != theorem priority
known-group 証明再生 != theorem application execution
show-proof != execute
operation-query 検索 != evaluator
operation-query 結果 != 新しい独立 theorem root
query-proof replay != enclosing theorem replay
LOOKUP_MISS != evaluator required
limited operation handoff != general query inference
theorem-specific concrete specialization != general evaluator
target-zero theorem-specific specialization != general target-zero evaluator
theorem-specific membership handoff != general membership evaluator
GROUP_MEMBERSHIP != recursive containment semantics
stable group specialization != unrestricted AST substitution
concrete proof recovery != new theorem root
negative stem acceptance != negative homotopy-group theorem
pi_0 boundary information != ordinary group result
Web execution adapter != execution semantics
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement の同居 != executable source relevance
executable relevance filtering != theorem ranking
group-result replay != generator-first lookup
group-result replay != new proof search
proof narrative != new proof
Outline hierarchy != inferred hierarchy
Narrative deduplication != proof graph mutation
Narrative label != theorem fact
human-readable label != semantic rewrite
Web proof presentation != proof truth
```

既存記録は原則として削除せず、確定した意味論訂正がある場合のみ訂正する。

# Phase 143 semantic Narrative provenance record

Phase 143 は新しい数学的証明を追加した Phase ではない。

目的は、既存 `ProofStep` が保持する statement の semantic structure を Narrative で可視化し、内部 rule name を数学的説明の代用として表示する箇所を解消することだった。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing proof ancestry
```

である。

Phase 143 の renderer は `ProofStep.conclusion` の型と保存済み fields を読む。

```text
stored semantic field
→ rendering source

renderer-generated inference
→ 禁止
```

したがって、保存されていない零端点、同型、単射性、位数、完全性などを renderer が推測して追加してはならない。

## representative semantic records

Toda Lemma 5.10 の bracket modulo statement:

$$
\Delta(\iota_{13})
\in
\{\nu_6,\eta_9,2\iota_{10}\}
\pmod{2\pi_{11}^{6}}.
$$

Toda Proposition 5.9 の kernel statement:

$$
\ker\left(
\Delta:\pi_8^5\to\pi_6^2
\right)
=
\mathbb Z/2\{4\nu_5\}.
$$

Toda Lemma 5.14 / Proposition 5.15 周辺では、保存された semantic relation、membership、Hopf relation、group decomposition を個別に表示する。

## transported decomposition provenance

$\pi_{15}^{8}$ の証明では transported decomposition

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}
$$

と final standard-order conclusion

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

は同じ文字列の重複ではない。

前者は導出途中の semantic decomposition、後者は最終的な標準順序の群表示である。

したがって:

```text
transported decomposition
→ preserve as derivation evidence

final group statement
→ preserve as conclusion
```

とする。

## direct-premise relocation provenance

$\pi_8^5$ の

$$
2\nu_5=E^2\nu'
$$

は依存関係に従って結論側へ relocation される direct premise である。

Phase 143 終盤の修正では、この premise を元位置にも復活させて二重表示することを避けた。

```text
relocated premise
→ one semantic occurrence in Narrative

Narrative relocation
!= ProofStep relocation
!= proof edge mutation
```

## completion audit

現行の実利用入口:

```text
_method_evidence_data(n, k)
→ presentation / blocks / sidecar / arguments
→ render_toda_group_proof_narrative_multi_argument_markdown()
```

を使用した completion audit:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

focused regression:

```text
33 passed in 20.96s
```

repository-wide final regression:

```text
9980 passed in 807.31s (0:13:27)
```

この結果を Phase 143 の provenance / presentation 完了境界とする。

```text
semantic Narrative
!= new proof

rule-name fallback 0
!= theorem completeness

render error 0
!= all mathematical statements proved

Narrative preservation / suppression / relocation
!= proof graph mutation
```
