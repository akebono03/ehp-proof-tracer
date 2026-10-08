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

---

# Phase 144 generic Narrative / ownership provenance record

Phase 144 は新しい Toda の数学的証明を追加した Phase ではない。

目的は、Phase 143 までに semantic rendering 可能になった既存 `ProofStep` provenance を、
専用 renderer に依存せず証明全体の Narrative として組み立てる際の ownership、
argument boundary、contribution ordering を監査することだった。

## provenance source

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 144 の generic Narrative はこれらを

```text
presentation
semantic sidecar
Narrative blocks
Narrative arguments
proof chains
ordered contributions
```

へ写して表示する。

```text
Narrative ownership
!= theorem ownership

contribution placement
!= proof edge creation

semantic closure
!= new proof inference
```

## complete replay provenance boundary

explicit positive depth の Narrative で semantic dependency closure を得るため complete replay
API を利用できる。

ただし complete replay は既存 proof ancestry をより完全に収集するだけで、新しい theorem
fact を生成しない。

depth 0 は明示的 bounded replay として維持する。

```text
depth 0
→ root boundary

complete replay
→ existing ancestry only
```

## R25-30-R3 boundary record

6代表群:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

current boundary inventory:

```text
pi_6^3:  selected=6 participating=6/6 detached=0/0 transport=1 missing=0
pi_8^5:  selected=10 participating=7/7 detached=3/3 transport=1 missing=0
pi_10^4: selected=22 participating=0/0 detached=22/0 transport=2 missing=0
pi_12^5: selected=46 participating=2/2 detached=44/0 transport=4 missing=0
pi_15^8: selected=54 participating=10/10 detached=44/0 transport=4 missing=0
pi_16^9: selected=54 participating=10/10 detached=44/0 transport=4 missing=0
```

aggregate:

```text
selected=192
participating=35
detached=157
detached_insertable=3
missing=0
```

R25-30-R3 では boundary classification と existing child Argument pair が対象ケースで一致した。

したがって:

```text
detached_insertable=3
!= proof provenance leak
!= ownership-boundary failure
```

と記録する。

## result-reuse provenance boundary

$\pi_{15}^8$ / $\pi_{16}^9$ の group-structure / definition entry では、owned entry 自身の
proof subtree が大きく再展開される場合がある。

これは provenance が誤って別 argument へ漏れたことを意味しない。

```text
large recursive expansion
→ result-reuse / already-established-result reuse pressure

large recursive expansion
!= argument-boundary leak
```

この問題は Phase 144 では proof graph を変更せず、将来 concrete blocker になった時点で
最小一般規則として扱う。

## final verification record

canonical repository-wide:

```text
10298 collected
10273 passed
25 failed
2321.20s (0:38:41)
```

25 failures は historical R5-39〜R5-43 completion / fixed-count snapshots に限定された。

maintenance policy:

```text
production renderer を旧 snapshot に戻さない
190 を 192 へ単純置換して新 snapshot にしない
33 を 35 へ単純置換して新 snapshot にしない
structural invariant を current test boundary とする
```

focused maintenance:

```text
66 passed in 1308.82s (0:21:48)
```

この後 repository-wide suite は再実行していない。

したがって Phase 144 の provenance record は、

```text
canonical whole-suite evidence
+
historical-snapshot focused maintenance evidence
```

の組として保持する。

## next-phase provenance boundary

Phase 145 は default display を Narrative + depth 2 に変更するだけであり、proof provenance
そのものを変更しない。

Phase 146 以降は concrete proof pressure を1件ずつ扱い、その不足だけを general rule
として実装する。

---

# Phase 145 default presentation / regression provenance record

Phase 145 は数学的 proof provenance を変更した Phase ではない。

目的は、Phase 144 までに構築した group-result Narrative を通常利用時の default
presentation とすることだった。

## default presentation boundary

default:

```text
mode = Narrative
depth = 2
```

explicit selection:

```text
Trace / Outline / Narrative
depth 0 / 1 / 2
```

は維持する。

```text
default mode change
!= ProofStep change

default depth change
!= proof ancestry change

Narrative default
!= Narrative theorem inference
```

Phase 145 の default depth 2 は user-facing initial selection であり、
既存 complete replay / bounded replay semantics を別物へ変更するものではない。

## repository cleanup provenance boundary

historical Phase artifact は `archive/phases/` 以下へ整理した。

canonical tests が必要とする test helper / audit helper は archive-only artifact と
同一視せず、canonical dependency として利用可能な状態を維持する。

cleanup 後の import regression は数学的 provenance の failure ではなく test collection
infrastructure の compatibility problem だった。

確認した mixed import inventory:

```text
tests.test_* package imports: 43
bare test_* imports: 547
unique bare test_* modules: 184
bare modules without canonical target: 0
```

最終 test-only compatibility:

```text
tests/__init__.py
tests/conftest.py
```

production proof repository、`ProofStep`、Narrative renderer の数学的 semantics は変更していない。

## final verification record

focused:

```text
46 passed in 15.62s
```

canonical collection:

```text
10303 tests collected
```

repository-wide final:

```text
10303 passed in 2375.31s (0:39:35)
```

したがって Phase 145 の provenance boundary は:

```text
Narrative + depth 2 default
+
repository/test infrastructure closure
```

であり、

```text
new theorem fact
new proof edge
new proof search
new Narrative generalization rule
result-reuse framework
```

は含まない。

Phase 146 以降は concrete proof pressure を1件ずつ選び、その不足に必要な最小一般規則だけを
追加する。

---

# Phase 146 historical Narrative comparison / provenance record

Phase 146 は $\pi_6^3$ の数学的 theorem fact を変更する Phase ではない。

比較対象:

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

historical baseline:

```text
Phase 136-2
commit 908e24db89669750949fa9ad149f5e306ac05546
```

## preserved mathematical core

historical/current 比較では、少なくとも次の数学的 core が current proof provenance に
保持されていることを確認した。

$$
2\eta_3=0,
$$

$$
\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1,
$$

$$
\nu'\in\pi_6^3,
\qquad
H(\nu')=\eta_5,
$$

$$
2\nu'=\eta_3^3,
$$

および EHP exactness と final group relation。

したがって Phase 146 の問題は theorem fact の消失そのものではなく、stored proof facts を
Narrative として選択・所有・配置・説明する presentation structure の差である。

## historical/current structural pressure

Phase 146-8 raw inventory:

```text
historical units: 17
current units: 82
ADDED: 47
DUPLICATED: 35

sequence-related:
historical 4
current 44

[R#]:
historical 8
current 1
```

raw matcher の `PRESERVED=0 / LOST=17` は unit 粒度差の影響を受けるため、数学的 fact loss
の件数として使用しない。

## current argument provenance diagnostics

Phase 146-9 R3:

```text
establish_group_structure:
method_evidence=3
components=1
primary=True
primary_windows=3
contributions=2

establish_order:
method_evidence=2
components=1
primary=True
primary_windows=2
contributions=2

establish_definition:
method_evidence=0
components=0
primary=False
primary_windows=0
contributions=0
```

この記録から、

```text
order argument has no primary exactness component
```

という説明は採用しない。

問題は historical proof-purpose と current method ownership / explanatory placement の差である。

## renderer-layer provenance boundary

Phase 146-9 では

```text
base multi-argument chars: 1377
contribution-connected chars: 1579
contribution renderer changes output: True
argument builder uses direct dependency indices: True
contribution renderer performs post-render insertion: True
```

を確認した。

したがって proof fact が graph 上に存在することと、その fact が historical と同じ説明位置に
現れることを同一視しない。

```text
proof provenance presence
!= Narrative explanatory placement

argument dependency
!= post-render contribution placement
```

## root-cause provenance classification

12 visible difference families を次へ集約した。

```text
RC1 Argument-method ownership
RC2 Recursive exactness evidence exposure
RC3 Contribution ownership / insertion ordering
RC4 Generic provenance / reason prose
RC5 EHP semantic naming
RC6 Final equation numbering / prose formatting
```

修正依存順:

```text
RC1 → RC2 → RC3 → RC4 → RC5 → RC6
```

RC6 は selection / ordering の下流であるため、historical tag を target-specific に
先に再現しない。

## Phase 146-7 production provenance

Phase 146-7 の generic prose fusion は presentation-only rule である。

```text
argument purpose
+
primary exactness transition
→ fused purpose/method sentence
```

これは

```text
new theorem fact
new proof edge
new exactness fact
new EHP evaluator
```

ではない。

## closure boundary

Phase 146 完了時点で次を維持する。

```text
existing ProofStep provenance
existing theorem facts
existing proof graph
existing proof search
pi_6^3 public route gate
```

Phase 147 以降で root cause を修正する場合も、stored provenance から一般的に導ける
presentation rule だけを追加し、historical $\pi_6^3$ の文字列を直接 special case として
埋め込まない。

## final verification record

Test Performance Repair 1〜9 後の repository-wide final:

```text
10306 passed in 1304.31s (0:21:44)
```

この結果を Phase 146 の final regression boundary とする。

---

# Phase 147 Argument-method ownership provenance record

Phase 147 は新しい Toda の数学的 theorem fact を追加した Phase ではない。

対象は Phase 146 で RC1 と分類した Narrative presentation 上の
`Argument-method ownership` である。

## ownership provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 147 で追加した ownership API は、既存 proof provenance から取得できる

```text
argument relevant groups
method evidence
exactness method components
```

を組み合わせ、

```text
Narrative Argument
→ primary exactness method component | None
```

という presentation 上の関係を導出する。

したがって:

```text
Argument-method ownership
!= theorem ownership

primary exactness ownership
!= new exactness fact

ownership selection
!= new proof search

ownership selection
!= proof edge creation

ownership API
!= EHP evaluator
```

## supporting blocks と method ownership の分離

Phase 147 の audit では、

```text
Argument.supporting_blocks
```

と

```text
Argument method ownership
```

を同一視しないことを確認した。

`supporting_blocks` に exactness block が直接含まれなくても、既存 recursive provenance から
method evidence が得られる場合がある。

したがって ownership は `NarrativeArgument` の stored field として追加せず、
既存 semantic structure から導出する API とした。

## pi_6^3 ownership record

対象:

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

Phase 147 RC1-4 では `establish_order` と `establish_group_structure` が、それぞれ異なる
primary exactness method を所有することを確認した。

```text
establish_order
→ $\nu'$ の位数決定の primary exactness method

establish_group_structure
→ $\pi_6^3$ の群構造決定の primary exactness method
```

これにより generic Narrative は proof purpose と method introduction を

```text
$\nu'$ の位数を決定するために、次の完全列を考える.
```

のように結び付けられる。

これは historical $\pi_6^3$ 専用文字列を埋め込んだものではない。

## RC1 / RC2 boundary

multi-argument renderer では primary-method selection を ownership API へ移した。

一方、body / evidence handling に必要な

```text
extract_toda_group_proof_narrative_argument_method_evidence()
```

は維持した。

したがって Phase 147 は、

```text
どの argument がどの primary method を所有するか
```

を扱うが、

```text
recursive exactness evidence を本文にどこまで表示するか
```

は変更しない。

後者は Phase 148 / RC2 の責務である。

同様に、

```text
short exact sequence
→ final group conclusion
```

などの contribution placement / ordering は Phase 149 / RC3 の責務として残す。

## final verification record

focused:

```text
RC1 ownership:
54 passed in 17.54s

Generic Narrative:
24 passed in 6.66s

Web group-proof Narrative:
20 passed in 10.72s
```

repository-wide final:

```text
10314 passed in 2942.66s (0:49:02)
```

この結果を Phase 147 / RC1 の final regression boundary とする。

```text
RC1 complete
!= historical pi_6^3 Narrative fully restored

RC1 complete
!= auxiliary exactness exposure solved

RC1 complete
!= contribution ordering solved
```

次の provenance / presentation pressure は Phase 148 / RC2
`Recursive exactness evidence exposure` とする。

---

# Phase 148 recursive exactness exposure / provenance record

Phase 148 は新しい Toda の数学的 theorem fact を追加した Phase ではない。

対象は Phase 146 で RC2 と分類した

```text
Recursive exactness evidence exposure
```

である。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 148 の exposure classification は、既存 provenance を Narrative 本文へ表示するかを
決める presentation rule である。

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

したがって:

```text
Narrative suppression
!= ProofStep deletion

body contribution suppression
!= provenance deletion

exactness exposure class
!= theorem classification

semantic closure
!= new theorem inference
```

## OWNED_PRIMARY provenance

Argument が primary method として所有する exactness component では、
raw exactness window の反復表示を抑制しつつ、所有された method の説明に必要な
higher-level contribution を利用できる。

```text
raw window suppression
!= exactness fact deletion
```

## UNOWNED_RECURSIVE provenance

recursive dependency として存在するだけの exactness evidence は、
Narrative body へ自動展開しない。

この規則は raw exactness window だけでなく、その component から生成される
derived short exact sequence contribution にも適用する。

```text
UNOWNED_RECURSIVE
→ body contributions = ()

provenance
→ preserved
```

## Web bounded replay provenance

Phase 148 の監査で、Web Narrative が selected depth より complete replay を利用し、
深い recursive exactness evidence を本文へ持ち込んでいたことを確認した。

修正後:

```text
selected bounded replay
→ semantic closure
→ Narrative
```

とする。

semantic closure は既存 proof ancestry から表示に必要な dependency を補うだけである。

depth 0:

```text
closure = identity
```

positive depth の order calculation:

```text
ORDER relation
→ direct EQUALITY premise
→ direct EQUALITY premises of that equality
```

既存 registered definition closure は維持する。

## six-group audit record

対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

最終 RC2-4 audit:

```text
all bounded below complete = True
all closure-added exactness = 0
all visible raw exactness = 0
all ambiguous exposure = 0
```

これは raw exactness が proof graph から消えたことを意味しない。
Narrative body への exposure が抑制されたことを意味する。

## final regression record

focused:

```text
92 passed in 36.15s
```

canonical repository regression:

```text
pytest -q tests

10398 passed
3 failed
1316.54s (0:21:56)
```

3 failures は Phase 148 repair 中に誤変更された
`tests/test_phase144_6_pi6_generic_production_route.py`
の historical generic-route contract に限定された。

GitHub `develop` の現行 contract へ復元後:

```text
4 passed in 1.71s
```

repository-wide suite は再実行していない。

したがって final provenance record は、

```text
whole-suite measured evidence
+
focused stale-contract restoration evidence
```

として保持する。

## next-phase boundary

Phase 149 / RC3 は Narrative ordering を扱う。

```text
RC2:
what exactness evidence is exposed

RC3:
where exposed contributions are placed
```

Phase 148 では ordering rule を先取りしない。

---

<!-- PHASE149_RC3_CLOSURE -->
# Phase 149 RC3 Narrative ordering / provenance record

Phase 149 は新しい Toda theorem fact を追加していない。

対象は Phase 146 の RC3:

```text
Contribution ownership / insertion ordering
```

である。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 149 の placement rule は RC2 で表示可能と判定された existing contribution の Narrative 上の位置だけを変更する。

```text
Narrative placement
!= ProofStep placement

Narrative placement
!= proof edge creation

Narrative placement
!= theorem inference

Narrative placement
!= exactness exposure classification
```

## pi_6^3 record

対象:

$$
\pi_6^3=\mathbb{Z}/4\{\nu'\}.
$$

Phase 149 RC3-1 では final group conclusion より後に derived short exact sequence が表示されていた。

RC3-3 Repair R1 後は、

$$
0
\longrightarrow
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5
\longrightarrow
0
$$

が owner `establish_group_structure` Argument の final conclusion より前に表示される。

この配置は $\pi_6^3$ 専用条件ではなく `OWNED_PRIMARY` exposure と owner conclusion の関係から決まる。

## six-group ordering record

対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9.
$$

RC3-4:

```text
pi_6^3: owned_primary_visible=1, ordering_ok=True
pi_8^5: owned_primary_visible=1, ordering_ok=True
pi_10^4: owned_primary_visible=0, ordering_ok=True
pi_12^5: owned_primary_visible=0, ordering_ok=True
pi_15^8: owned_primary_visible=0, ordering_ok=True
pi_16^9: owned_primary_visible=0, ordering_ok=True

failures=[]
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

## remaining boundary

$\pi_6^3$ の order Argument では、式 (1), (2) から得る

$$
2\nu'=\eta_3^3
$$

をさらに早い位置へ置く方が文章上自然である可能性がある。

ただしこれは exactness contribution placement ではなく calculation / derivation internal ordering である。

したがって:

```text
observed prose-order improvement
!= RC3 failure
```

として Phase 149 では production change を追加しない。

## final verification record

repository-wide final regression:

```text
﻿10416 passed in 1315.93s (0:21:55)
```

Phase 149 / RC3 完了。

次の provenance pressure は Phase 150 / RC4 `Generic provenance / reason prose` とする。
---

<!-- PHASE150_CLOSURE -->
# Phase 150 RC4 Generic provenance / reason prose provenance record

Phase 150 は新しい Toda theorem fact を追加していない。

対象は Phase 146 の RC4:

```text
Generic provenance / reason prose
```

である。

## provenance boundary

数学的 ground truth は引き続き

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

である。

Phase 150 の typed reason は、既存 proof provenance と semantic sidecar から導出される
Narrative presentation 上の理由情報である。

```text
typed reason
!= theorem fact

reason sentence
!= proof edge

reason sidecar
!= proof search

visible reason
!= provenance mutation
```

## visible reason multiplicity

6代表群:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{15}^8,\quad
\pi_{16}^9
$$

について typed reason と rendered sentence の多重度を監査した。

共通 generic reason sentence について:

```text
pi_6^3:  typed=3, rendered=3
pi_8^5:  typed=3, rendered=3
pi_10^4: typed=2, rendered=2
pi_12^5: typed=2, rendered=2
pi_15^8: typed=1, rendered=1
pi_16^9: typed=3, rendered=3
```

したがって、複数回出現した共通 sentence は単一 reason の renderer duplication ではない。
異なる typed reason instance が同一 generic prose へ写された結果である。

final contract:

$$
\#\{\text{typed reasons rendering to }s\}
=
\#\{\text{rendered occurrences of }s\}.
$$

Repair R2 は production renderer を変更せず、この instance-level contract を test した。

focused:

```text
RC4-5:
9 passed in 5.65s

nine-failure repair set:
17 passed in 9.03s
```

## Phase 148 exactness compatibility

Phase 150 final regression で検出された Phase 148 関連 historical failures は、
semantic exactness evidence の消失ではなかった。

proof provenance 上の typed exactness statement は維持されている一方、現行 generic Narrative は
旧 literal exactness phrase を必須としない。

したがって historical display expectation を現行 presentation contract に合わせた。
production proof provenance は変更していない。

## renderer-route provenance boundary

Phase 150 では一部代表群の generic route 移行が進んだが、全群が同一 route になったわけではない。

この coexistence 自体が群間の Narrative 差を作るため、以後は group-by-group migration を
継続しない。

Phase 151 では public route を変更せず、対象 population 全体を同一 generic route へ通して
baseline を取得する。

```text
forced generic audit
!= public route change

generic comparison
!= proof provenance change

route unification planning
!= dedicated renderer deletion
```

## final verification record

Phase 150 final full regression:

```text
Python 3.10.3
pytest 9.1.1
branch: develop

10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

したがって Phase 150 closure 時点で canonical repository test population は全PASSである。

## next-phase provenance boundary

Phase 151 は `All-Group Generic Baseline`。

新しい theorem fact、proof edge、proof search、public route switch を追加せず、同一 generic
presentation route による whole-population observation を行う。

Phase 152 でその結果を defect category に分類し、Phase 153 以降で1カテゴリずつ最小一般規則を
実装する。

---

<!-- PHASE153_CLOSURE -->
# Phase 153 Reference selection / granularity provenance record

Phase 153 は数学的 theorem fact を追加した Phase ではない。

対象は既存 `ProofStep` provenance から Narrative に提示する external Reference の選択、
粒度、再利用、表示境界である。

## provenance ground truth

引き続き ground truth は

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
LiteratureReference
```

である。

Phase 153 の Reference layer は、これらから表示に必要な外部結果を選ぶ presentation rule である。

```text
Reference selection
!= theorem selection

Reference granularity
!= theorem decomposition

Reference reuse
!= premise deletion

Reference filtering
!= provenance deletion
```

## root Reference boundary

current `presentation.root_step` の literature citation は、その証明自身の provenance であり、
external supporting Reference ではない。

したがって:

```text
root LiteratureReference
→ provenance として保持
→ external Reference section から除外
```

この boundary は legacy / generic / specialized route に共通である。

## locator identity

同じ文献箇所が label 違いで保持される場合の identity は次とする。

```text
both references have locator
→ compare locator

otherwise
→ compare full LiteratureReference
```

この rule により `(5.2)` など同じ locator の root citation が label 差によって
external Reference に漏れることを防ぐ。

## used Reference provenance

marker-bearing route:

```text
rendered body [Rk]
→ used Reference set
→ filter
→ contiguous renumbering
```

generic no-marker route:

```text
displayed argument/local-body/contribution steps
→ used step ids
→ structural Reference attribution
```

したがって explicit marker の有無は provenance の有無を意味しない。

## Reference reuse provenance

Reference statement として exact step が表示済みなら、その step の既存 premises を本文で
再展開しなくても、`[Rk]` 利用として proof boundary を示せる。

```text
Reference boundary reuse
→ display compression

existing ProofStep ancestry
→ preserved
```

## aggregate granularity record

aggregate statement に複数の group relation / generator component が含まれる場合、
consumer と構造的に対応する一意 component を Reference statement として選択できる。

これは aggregate theorem の数学的意味を変更するものではない。

```text
aggregate theorem provenance
→ preserved

Narrative Reference statement
→ consumer-relevant component
```

## n=2 six-group ancestry record

監査対象:

$$
\pi_4^2,\quad
\pi_5^2,\quad
\pi_6^2,\quad
\pi_7^2,\quad
\pi_8^2,\quad
\pi_9^2.
$$

root 自身ではなく、実際に利用する premise / ancestry から external Reference を選ぶ
一般 rule を確認した。

## final 112-group provenance audit

対象:

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7.
$$

結果:

```text
scanned groups: 112
render errors: 0
groups with Reference section: 93
marker-bearing groups: 90
generic/reference-only groups: 3
Reference headers: 147
body Reference markers: 146
maximum References in one group: 6
groups at maximum: pi_6^3
violations: 0
```

Reference invariant:

```text
Reference numbers contiguous
root citation not external
body marker points to an existing Reference
marker-bearing body has no unused displayed Reference
```

すべて PASS。

## regression evidence boundary

Phase 153 closure verification:

```text
30 passed in 7.97s
```

full canonical historical suite は 10,554 tests を収集したが、古い presentation expectation が
複数残っていることを確認し、今回は全完走を completion evidence にしなかった。

確認済みの stale Phase 132 Narrative expectation については test-only repair を行い、

```text
22 passed in 6.28s
```

を確認した。

repository-wide all-pass は観測していないため記録しない。

## next provenance boundary

Phase 154 は Reference selection ではなく proof-prose generation を扱う。

```text
stored proof provenance
→ unchanged

Reference selection / granularity
→ Phase 153 で確定

prose realization / connection
→ Phase 154
```

Test Suite Consolidation は別 maintenance backlog とする。

<!-- PHASE154_DOCUMENTATION_CLOSURE -->
# Phase 154 Proof prose generation provenance record

Phase 154 は新しい Toda theorem fact や proof edge を追加する Phase ではない。

対象は stored proof provenance から public Narrative prose を生成する presentation layer である。

## provenance ground truth

引き続き ground truth は:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
LiteratureReference
```

である。

Phase 154 で変更したのは、

```text
semantic prose realization
transition composition
reason sentence visibility
Reference-to-consumer connection
punctuation
```

であり、

```text
proof graph
theorem facts
proof-search semantics
Reference selection provenance
```

は保持した。

## internal-fallback provenance boundary

semantic fact が proof graph 上に存在していても、public prose が inference-rule name や
statement type-name を露出する必要はない。

```text
stored ProofStep
→ semantic renderer
→ human-readable public fact
```

内部 fallback の非表示は provenance deletion ではない。

## final-reason deduplication provenance

複数の typed reason instance が同一 `FINAL_RESULT_DERIVATION` sentence を生成する場合:

```text
typed reason instances
→ preserved

public duplicate final sentence
→ one visible occurrence
```

したがって Phase 150 時点の

```text
typed reason multiplicity
= visible sentence multiplicity
```

は Phase 154-R4 で public presentation contract として更新された。

## Reference linkage provenance

Reference-to-body linkage は Reference source step と consumer step の既存 Proof graph relation を
利用する。

```text
Reference source
→ existing graph ancestry
→ unique visible non-root consumer
→ [Rk]より, consumer fact.
```

一意 consumer が安全に決められない場合:

```text
[Rk]を用いる.
```

を維持する。

これは Phase 153 の Reference selection / granularity を変更しない。

## punctuation provenance boundary

Narrative prose punctuation:

```text
comma  = ", "
period = "."
```

数学的 TeX、literature title、group-expression 内部 punctuation は対象外である。

5代表群修正後、112-group depth-2 public Narrative closure audit で:

```text
japanese comma violations: 0
japanese period violations: 0
groups with ascii comma prose: 112
groups with ascii period prose: 112
```

を確認した。

## closure audit record

Phase 154 focused regression:

```text
44 passed
```

ordering / reason boundary:

```text
57 passed
```

112-group final closure:

```text
scanned groups: 112
rendered groups: 112
exceptions: 0
violations: 0

transition_repetition: 0
semantic_duplication: 0
internal_fallback_leakage: 0
english_prose: 0
reference_linkage: 0
ordering: 0
punctuation: 0
```

Reference coverage:

```text
groups with Reference section: 93
groups with body Reference markers: 89
```

## dedicated renderer audit provenance

$\pi_8^5$ と $\pi_{15}^8$ の ordering violation は production fact ではなく audit false positive
だった。

substring:

```text
## 証明
```

が

```text
## 証明対象
```

へ一致したことが原因である。

exact heading-line audit により:

```text
## 証明対象
<
## 使用する結果
<
## 証明
```

を両群で確認した。

production renderer は変更していない。

## regression evidence boundary

documentation closure 時点では repository-wide full regression を実行していない。

したがって completion evidence は:

```text
Phase 154 focused regression PASS
Phase 149 / 150 boundary regression PASS
112-group closure invariant PASS
punctuation closure invariant PASS
```

であり、

```text
repository-wide all-pass
```

はまだ claim しない。

Phase 154 final full regression を次の Phase-final step とする。

<!-- PHASE155_TEST_PROVENANCE_START -->
# Phase 155 test-suite provenance record

Phase155 は数学的 proof provenance を変更していない。

最終 collection:

```text
10384 total
10382 routine
2 audit-only
```

completion evidence:

```text
routine sharded regression PASS
+
explicit closure audit 2/2 PASS
```

Phase144 completion/source-shape audit は historical implementation shape を current failure と誤認するため closure boundary から削除した。

Phase153 exact selected-statement/body duplicate audit は 117件を観測した。

```text
117 observations
→ Phase156 audit input
!= Phase155 production defect
```

Phase97 closure audit は `goal_source` を常に要求しない。

```text
direct result
→ goal_source=None を許容

aggregate result
→ goal_source identity / repository metadata を保持
```

次の provenance boundary:

```text
Phase153: Reference selection / granularity
Phase154: proof prose generation
Phase155: test verification boundary
Phase156: Reference statement necessity / minimal display
```
<!-- PHASE155_TEST_PROVENANCE_END -->

<!-- PHASE158_DOCUMENTATION_CLOSURE -->
# Phase 158 public Narrative contract provenance record

Phase 158 は新しい Toda theorem fact を追加することを主目的とした Phase ではない。

対象は existing proof provenance を public Narrative として表示する際の route、shell、equation linkage、derivation ordering の統一である。

## provenance ground truth

Phase 158 後も数学的 ground truth は引き続き:

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
LiteratureReference
```

である。

Phase 158 の public contract はこれらを表示する presentation policy であり、

```text
public route unification
!= theorem unification

shell normalization
!= proof rewrite

equation numbering
!= mathematical inference

Narrative ordering
!= premise-edge mutation
```

である。

## public shell provenance boundary

depth 2 以上では route に依存せず:

```text
# Group proof narrative
## 証明対象
## 使用する結果
---
## 証明
□
```

を public shell とする。

`## 使用する結果` の導入文を削除しても `LiteratureReference`、Reference entry、statement、番号、consumer relation は保持される。

## single generic route provenance

`max_depth >= 2` の public Narrative は generic multi-argument / contribution route を利用する。

```text
presentation
→ semantic closure
→ semantic sidecar
→ blocks
→ arguments
→ contributions
→ public Narrative
```

これは existing proof graph を別の graph に置換するものではない。

旧 dedicated helper がコード上に残っていても、full public depth-2 route の数学的根拠は同じ stored provenance から取得する。

## equation linkage provenance

equation number は visible proof fact の identity ではなく、現在の Narrative 内で後続 derivation が参照するための local display label である。

したがって:

```text
visible source + later reference
→ \tag{N}

transition target であるだけ
→ tag 不要

terminal conclusion
→ later reference がなければ tag 不要
```

proof-item numbering は別 presentation structure であり、equation tag identity と混同しない。

## ordering provenance

$\pi_7^4$ と $\pi_{15}^8$ の診断では、

```text
proof graph ordering
semantic block ordering
Narrative Argument ordering
```

は成立していた。

public output だけが root conclusion を早く表示する route を通っていたため、structured root Argument の存在を generic ordering route の条件とした。

したがって ordering repair は、

```text
existing dependency order
→ public output へ忠実に反映
```

したもので、新しい dependency を追加していない。

## R5-6 closure record

initial focused closure:

```text
34 passed
11 failed
```

failure classification:

```text
stale Phase 157 QED expectation
production equation-numbering defect
stale Phase 150 prose / dedicated-route expectations
```

production repair は equation-numbering function のみに限定した。

terminal / unreferenced transition target を numbering set へ追加しないことで、

```text
generated equation tags
=
equations actually referenced later
```

という current contract を回復した。

最終 verification:

```text
direct repaired-contract:
32 passed in 16.16s

R5 focused closure:
45 passed in 20.24s

git diff --check:
PASS
```

repository-wide pytest は実行していないため、Phase 158 について repository-wide all-pass は provenance record として claim しない。

## next provenance pressure

Phase 159 は presentation route ではなく mathematical proof coverage を扱う。

開始点:

$$
\pi_3^2
$$

すなわち

$$
k=1,\quad n=2.
$$

以後 $n$ を増やしながら existing proof provenance の不足を調べる。

不足する規則が見つかった場合のみ、群固有の special case ではなく、既存文献事実と proof structure に基づく再利用可能な一般規則を追加する。

stable range では Freudenthal suspension theorem による同型移送を利用できる境界を必要に応じて導入する。


<!-- PHASE159_DOCUMENTATION_CLOSURE -->
# Phase 159 stem-1 proof record

Phase 159 の数学的 proof coverage は $k=1$ から開始した。

## $\pi_3^2$

対象は

$$
\pi_3^2=\mathbb Z\{\eta_2\}.
$$

public proof の監査では、既存 proof provenance に従った依存順序、definition premise の配置、map-property の提示、Reference の一般形、式番号と proof-item 番号の区別を確認した。

Reference の literature statement は general form のまま保持し、$\pi_3^2$ 固有の代入・特殊化は proof body に置く。

## $\pi_4^3$

対象は

$$
\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

この群は $k=1$ に対して stable range の入口

$$
n=k+2=3
$$

に位置する。Phase 159 では $k=1$ の stable suspension proof を監査し、Toda (4.5) の一般形を Reference として用い、proof body で target へ特殊化する境界を確認した。

## generic stable transport への記録

一般の target

$$
\pi_{n+k}^{n}
$$

について stable range を

$$
n\ge k+2
$$

とする。canonical stable base は

$$
\pi_{2k+2}^{k+2}
$$

であり、stable target への群構造の移送は

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}
$$

で表す。

この記録は次 Phase の設計入力であり、Phase 159 において全 stem の transport proof が production 実装済みであることを意味しない。

## provenance boundary

```text
general literature Reference
!= target-specific specialization

semantic identity
!= rendered prose equality

generic group transport
!= family-specific generator normalization

Phase 159 design closure
!= all-stem stable implementation
```

Phase 159 documentation closure では repository-wide full pytest を実行していないため、新しい全体回帰 PASS は記録しない。


<!-- PHASE160_DOCUMENTATION_CLOSURE -->
# Phase 160 generic stable transport proof record

Phase 160 は stable target の theorem provenance を新しい独立 root へ置換した Phase ではない。

既存の canonical-base proof と Toda (4.5) の isomorphism provenance を、共通 transport layer で接続した。

## stable target identity

対象:

$$
\pi_{n+k}^{n}.
$$

stable condition:

$$
n\ge k+2.
$$

canonical base:

$$
\pi_{2k+2}^{k+2}.
$$

transport:

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}.
$$

この3要素は rendered prose から推測せず、structural target / scalar expression / `ProofStep` から扱う。

## finite-cyclic transport provenance

canonical-base relation

$$
\pi_{2k+2}^{k+2}
=
\mathbb Z/r\{x\}
$$

と Toda (4.5) isomorphism から、generic transport は

$$
\pi_{n+k}^{n}
=
\mathbb Z/r\{E^{n-k-2}x\}
$$

を構成する。

ここで order $r$ は保持する。

```text
generic transport
!= generator-family identity
```

したがって $E^r x=\eta_n,\nu_n,\sigma_n$ などの family identity は別 provenance step とする。

## zero-group transport provenance

canonical base が

$$
\pi_{2k+2}^{k+2}=0
$$

なら、Toda (4.5) isomorphism を介して target zero を導出する。

```text
TodaPrimaryGroupZeroStatement
→ generic zero transport
→ TodaPrimaryGroupZeroStatement
```

zero を `FiniteCyclicGroup(order=1)` へ読み替えない。

## stem 1 provenance

canonical base:

$$
\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

stable result:

$$
\pi_{n+1}^{n}
=
\mathbb Z/2\{\eta_n\}.
$$

group transport と eta-family generator identity は分離する。

## stem 2 provenance

canonical base:

$$
\pi_6^4
=
\mathbb Z/2\{\eta_4^2\}.
$$

stable result:

$$
\pi_{n+2}^{n}
=
\mathbb Z/2\{\eta_n^2\}.
$$

internal generator は consecutive eta composition として保持できる。

public notation:

$$
\eta_n\eta_{n+1}
\longmapsto
\eta_n^2.
$$

## stem 3 provenance

canonical base:

$$
\pi_8^5
=
\mathbb Z/8\{\nu_5\}.
$$

generic transport 後:

$$
\mathbb Z/8\{E^{n-5}\nu_5\}.
$$

existing nu-family bridge により:

$$
E^{n-5}\nu_5=\nu_n.
$$

したがって

$$
\pi_{n+3}^{n}
=
\mathbb Z/8\{\nu_n\}.
$$

## stem 4 provenance

canonical base:

$$
\pi_{10}^6=0.
$$

generic zero transport により

$$
\pi_{n+4}^{n}=0.
$$

## stem 5 provenance

canonical base:

$$
\pi_{12}^7=0.
$$

stem 4 と同じ generic zero transport により

$$
\pi_{n+5}^{n}=0.
$$

## stem 6 provenance

canonical base:

$$
\pi_{14}^8
=
\mathbb Z/2\{\nu_8^2\}.
$$

generic group transport:

$$
\pi_{n+6}^{n}
=
\mathbb Z/2
\{E^{n-8}\nu_8^2\}.
$$

generator normalization:

$$
E^{n-8}\nu_8^2
=
\nu_n^2.
$$

最終 result:

$$
\pi_{n+6}^{n}
=
\mathbb Z/2\{\nu_n^2\}.
$$

public group notation では

$$
\nu_n\nu_{n+3}
\longmapsto
\nu_n^2
$$

を用いるが、internal `Composition` は変更しない。

## stem 7 provenance

canonical base:

$$
\pi_{16}^9
=
\mathbb Z/16\{\sigma_9\}.
$$

generic transport:

$$
\mathbb Z/16
\{E^{n-9}\sigma_9\}.
$$

sigma-family normalization:

$$
E^{n-9}\sigma_9=\sigma_n.
$$

したがって

$$
\pi_{n+7}^{n}
=
\mathbb Z/16\{\sigma_n\}.
$$

## public Narrative provenance boundary

stable Narrative の visible Reference は、

```text
[R1] Toda (4.5) general form
[R2] canonical base literature result
```

を基本とする。

target-specific substitution は proof body に置く。

```text
general Reference
!= specialized proof line

canonical base theorem
!= newly invented stable theorem root
```

canonical base 自身では stable transport Narrative を起動しない。

## public canonicalization provenance boundary

Group query Result / Group proof Conclusion / Narrative の generator notation は整合させる。

ただし canonicalization は presentation layer だけに適用する。

```text
eta_n eta_(n+1) -> eta_n^2
nu_n nu_(n+3)   -> nu_n^2
```

これは

```text
Composition object rewrite
ProofStep rewrite
theorem fact rewrite
```

ではない。

## verification record

Phase 160 の代表 focused evidence:

```text
R7 repair:
18 passed

R8 repair2:
37 passed

R9:
19 passed

R10 repair1:
117 passed in 23.92s
```

R11 は利用者指定により pytest を実行していない。

Web manual verification:

$$
\pi_{15}^{13}
\cong
\mathbb Z/2\{\eta_{13}^{2}\},
$$

$$
\pi_{19}^{13}
\cong
\mathbb Z/2\{\nu_{13}^{2}\}.
$$

両例で Result / Conclusion / Narrative の canonical notation が一致した。

repository-wide full pytest は Phase 160 closure では実行していないため、repository-wide all-pass は claim しない。

## next proof boundary

stable range の common transport infrastructure は Phase 160 で確立した。

次 Phase は unstable range

$$
n<k+2
$$

へ戻り、existing proof provenance を低次から順に監査する。

```text
stable group
→ Phase 160 transport を再利用

unstable group
→ existing EHP / literature proof を詳細に監査
```

不足する theorem fact / proof step が実際に現れた場合のみ、最小の再利用可能規則を追加する。
