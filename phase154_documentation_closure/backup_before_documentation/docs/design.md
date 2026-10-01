# EHP Proof Tracer 設計

この文書は EHP Proof Tracer の**現在有効なアーキテクチャ、意味論、不変条件、設計境界**を記録する。

過去の実装経緯は `docs/development_log.md`、証明記録は `docs/proof_records.md`、今後の計画は `docs/roadmap.md`、コード探索は `docs/code_reference.md` を参照する。

---

# 1. 基本設計原則

```text
実際の数学的・証明探索上の必要
↓
不足している最小表現
↓
必要な領域固有規則 / オーケストレーション
↓
既存の汎用基盤
```

次を混同しない。

```text
表現 != 型付け != 定理知識
構造的等値 != 数学的等値
探索計画 != 証明結果
表示層 != 証明事実
proof-scope 走査 != 定理探索
proof-scope relevance != executable relevance
applicability relevance != executable relevance
aggregate statement 内の別 branch occurrence != executable source relevance
既知関係の発見 != 写像評価
適用可能候補 != 証明成功
候補番号 != 数学的優先度
operation query != general evaluator
limited theorem-specific handoff != general query inference
theorem-specific membership handoff != general membership evaluator
group-generator containment != operation result
target group zero specialization != general zero-target evaluator
stable-family specialization != unrestricted symbolic substitution
concrete proof recovery != new theorem root
negative stem acceptance != negative homotopy group definition
pi_0 boundary information != ordinary group result
Web UI != 新しい数学エンジン
TeX rendering != 数学的 normalization
proof depth control != 新しい proof search
semantic renderer != 新しい数学的事実
rule-name fallback 除去 != proof semantics 変更
safe fallback != 推測した数学的説明
candidate selection != theorem ranking
Web execution != second execution engine
executable relevance filtering != theorem ranking
group-result proof replay != generator lookup
group-result proof replay != new proof search
proof narrative != new proof
Outline != proof search
Narrative deduplication != proof graph deletion
Narrative label != proof fact
human-readable label != semantic rewrite
Web presentation adapter != proof semantics
```

---

# 2. Toda group query の主要経路

```text
ProofRepository
→ TodaGroupQuery
→ foundational specialization
→ direct known-group lookup
→ concrete proof-ancestry recovery
→ stable/theorem-specific specialization
→ TodaGroupResult
→ proof / EHP provenance
→ structured presentation
→ report
```

Phase 130 以降、`TodaGroupQuery` は `k >= 0` に限定されない。

```text
n > 0
k は任意の int
```

ただし `n+k` の値に応じて意味論を分ける。

---

# 3. query domain semantics

\(m=n+k\) とする。

## \(m>0\)

通常の project group query の対象。

`k<0` かつ

$$
1\le m<n
$$

なら sphere connectivity により

$$
\pi_m(S^n)=0
$$

として扱う。

Phase 130 ではこの connectivity zero を repository-backed `TodaGroupResult` として具体化するため、Phase 131 以降の group-result proof replay 対象になる。

## \(m=0\)

$$
\pi_0(S^n)
$$

は通常の group result に正規化しない。

\(n>0\) の球面は path-connected なので、1つの path component を持つという boundary information を返す。

したがって group-result proof replay の対象外である。

## \(m<0\)

classical unstable homotopy-group domain 外として扱う。

負次数を zero group と推測しない。

---

# 4. foundational group specialization

Phase 130 で foundational specialization を group-query orchestration の先頭へ追加した。

## diagonal

$$
\pi_n^n\cong\mathbb Z\{\iota_n\}.
$$

これは `k=0` の query に対応する。

## circle higher groups

既存 Phase 56 の symbolic zero

$$
\pi_{i-1}^1=0
$$

を concrete query に specialize する。

したがって

$$
n=1,\quad k\ge1
$$

では

$$
\pi_{1+k}^1=0.
$$

新しい独立 theorem root は追加しない。

## connectivity zero

$$
1\le n+k<n
$$

では foundational sphere connectivity として zero result を返す。

この結果は `ProofRepositoryEntry` と `ProofStep` を持つ。

---

# 5. stem 1–3 specialization

Phase 130 では既存 symbolic theorem を standard query から具体化できるようにした。

## stem 1

$$
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\}.
$$

## stem 2

$$
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\}.
$$

## stem 3

$$
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\}.
$$

低次元 concrete boundary が既存 proof にある場合は concrete proof を優先する。

---

# 6. stem 4–6 specialization

## stem 4

$$
\pi_{n+4}^n=0,
\qquad n\ge6.
$$

## stem 5

低次元 concrete branch を proof ancestry から回収し、

$$
\pi_{n+5}^n=0,
\qquad n\ge7
$$

を symbolic branch から specialize する。

## stem 6

$$
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\}.
$$

既存 concrete \(n=5,6,7,8\) を維持し、symbolic specialization はその境界より上で使う。

---

# 7. stem 7 / sigma family

Toda Proposition 5.15 の既存証明には

$$
\pi_{16}^9=\mathbb Z/16\{\sigma_9\}
$$

という concrete proof が存在する。

また symbolic higher branch として

$$
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\},
\qquad n\ge9
$$

が存在する。

現行設計は次のように分ける。

```text
n = 8
→ Prop.5.15 aggregate の concrete branch

n = 9
→ existing concrete pi16_9 ProofStep を proof scope から回収

n >= 10
→ theorem-specific indexed sigma specialization
```

`n=9` を generic specialization の境界へ無理に混ぜない。

---

# 8. standard repository 非破壊

Phase 130 の specialization / recovery は standard repository root を追加しない。

期待する root:

```text
standard.toda.prop56
standard.toda.prop58
standard.toda.prop511
standard.toda.prop515
```

query 実行の前後で repository entry 集合を維持する。

---

# 9. concrete proof recovery

group query で aggregate の top-level branch に存在しない concrete result が proof ancestry に存在する場合、限定的に proof scope から回収する。

Phase 130 の代表例:

$$
\pi_{16}^9=\mathbb Z/16\{\sigma_9\}.
$$

回収条件は theorem-specific かつ target-specific に狭くする。

```text
proof-scope recovery
!= arbitrary recursive theorem mining
!= theorem ranking
!= automatic proof synthesis
```

---

# 10. operation query

operation query は lookup-first である。

```text
query string
→ minimal parser
→ direct repository / proof-scope lookup
→ direct hit はそのまま返す
→ direct miss のうち許可された exact handoff のみ具体化
→ structured presentation
→ CLI / Web
```

現在許可される exact handoff:

```text
E(nu_5)
E(sigma_11)
E(nu_5 o eta_8)
E(nu_prime)
```

対応結果:

$$
E(\nu_5)=\nu_6,
\qquad
E(\sigma_{11})=\sigma_{12},
$$

$$
E(\nu_5\eta_8)=0,
\qquad
E\nu' \in \pi_7^4.
$$

---

# 11. provenance

証明事実の中心は

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
```

である。

`ProofRepositoryEntry.key / phase / theorem` は provenance metadata。

`TodaGroupResult` はさらに

```text
source_entry
proof_step
```

を保持し、

```text
group_result.proof_step is group_result.source_entry.step
```

を不変条件とする。

```text
theorem-specific operation handoff != independent theorem root
theorem-specific membership step != general inference rule
GROUP_MEMBERSHIP match kind != membership evaluator
```

---

# 12. group-result proof replay

Phase 131 では generator ではなく群結果そのものから proof replay する経路を追加した。

```text
TodaGroupResult
→ proof_step
→ extract_toda_recursive_proof_provenance()
→ depth 制限
→ TodaGroupResultProofReplayResult
```

重要な境界:

```text
group-result replay
!= generator-first replay
!= repository re-search
!= theorem mining
!= new proof search
```

`TodaGroupResult.source_entry` と `TodaGroupResult.proof_step` の identity を維持する。

replay step は既存 recursive provenance の

```text
shortest_depth
role
ProofStep identity
```

を保持する。

これにより generator を持たない zero group でも replay できる。

例:

$$
\pi_9^2=0.
$$

また Phase 130 の foundational connectivity zero:

$$
\pi_{10}^{11}=0
$$

も repository-backed result のため replay できる。

一方、

```text
pi_0 boundary information
negative-dimensional out-of-domain information
```

は ordinary `TodaGroupResult` ではないため replay 対象外。

---

# 13. Phase 132 group proof presentation core

Phase 132 では replay 結果を Trace / Outline / Narrative へ共通接続するため、

```text
TodaGroupProofPresentation
```

を追加した。

構造:

```text
TodaGroupResultProofReplayResult
→ selected replay nodes
→ existing recursive provenance edges を selected nodes へ filter
→ TodaGroupProofPresentation
```

重要な不変条件:

```text
presentation.nodes is replay.steps
presentation.root_step is replay.root_step
presentation.source_entry is replay.source_entry
presentation.max_depth == replay.max_depth
```

presentation は新しい traversal semantics を定義しない。

```text
TodaGroupProofPresentation
!= new proof search
!= second depth semantics
!= inferred parent relation
```

proof edge は `ProofStep.premises` 由来の既存 recursive provenance を使用する。

flat replay の `depth` や表示順から parent-child relation を推測してはならない。

---

# 14. Trace / Outline / Narrative

## Trace

Phase 131 の既存 replay 表示。

```text
Depth
statement
Role
Rule
Provenance
```

監査用 ground truth とする。

## Outline

Outline は同じ presentation graph を階層的に表示する。

```text
Conclusion
→ Premise 1
→ Premise 2
→ nested premise
```

同じ親の premise は `premise_index` 順に表示する。

```text
premise_index order
!= global causal order
```

shared dependency が別 branch から参照される場合、graph 構造を保持するため Outline では必要に応じて複数箇所に現れてよい。

## Narrative

Narrative は固定テンプレートで同じ graph を文章化する。

```text
source theorem
premise fact
nested consequence
root conclusion
```

新しい数学的説明を自由生成しない。

Phase 133 以降の statement 表示優先順は次のとおり。

```text
既存 LaTeX renderer
→ 明示的 human-readable Narrative label
→ inference rule name
→ statement type name
```

明示的 Narrative label は、既存 statement type の表示名を人間向けにするだけである。

```text
human-readable Narrative label
!= theorem inference
!= statement semantic rewrite
!= new theorem fact
```

代表例:

```text
Toda56Nu4DecompositionStatement
→ Toda (5.6) の ν₄ 分解

TodaProp511FiniteDimensionalStatement
→ Toda Proposition 5.11 の有限次元結果

Toda36Lemma514SigmaDoublePrimeBridgeStatement
→ Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係
```

未対応 statement では rule name / type name fallback を維持する。

```text
Narrative
!= theorem inference
!= mathematical paraphrase guessing
!= provenance-free LLM proof
```

---

# 15. Narrative shared-dependency deduplication / wording

Phase 132-8 で Narrative 表示に `ProofStep` identity 単位の shared-dependency deduplication を追加した。

cycle guard と dedup state は別物として扱う。

```text
active_step_ids
→ 現在の再帰 stack 上の cycle guard

expanded_step_ids
→ Narrative で既に subtree を展開済みか
```

Phase 133 では表示文面を整理した。

最初の出現:

```text
subtree を通常展開
```

nested branch で既に展開済みの dependency:

```text
重複展開しない
```

root-level など、利用関係を表示すべき再参照:

```text
すでに得た ... を用いる。
```

導出の接続語:

```text
premise 1件
→ このことから

premise 2件以上
→ これらから
```

重要:

```text
Narrative subtree dedup
!= edge removal
!= node removal
!= provenance mutation
```

Trace / Outline / presentation graph は変更しない。

---

# 16. CLI proof presentation

generator-first:

```powershell
python main.py show-proof sigma_11
```

group-result-first:

```powershell
python main.py group-proof 9 7
python main.py group-proof 9 7 --depth 2
```

Phase 132 以降:

```powershell
python main.py group-proof 9 7 --mode trace
python main.py group-proof 9 7 --mode outline
python main.py group-proof 9 7 --mode narrative
python main.py group-proof 9 7 --depth 2 --mode narrative
```

`--mode` 省略時は `narrative`、`--depth` 省略時は `2`。

Trace / Outline / Narrative と depth 0 / 1 / 2 の明示指定 semantics は維持する。

```text
show-proof
→ generator から known-group identity を探す

group-proof
→ n,k query で得た group result から直接 replay / presentation
```

---

# 17. Web / CLI 共通 semantics

CLI と Web で数学エンジンを分岐させない。

Web group query は repository-backed result の場合のみ `proof_available=True` とし、result 直下に `Show proof` を表示する。

proof depth:

```text
0 / 1 / 2
```

proof view:

```text
Trace / Outline / Narrative
```

Trace は既存 structured replay view を使う。

Outline / Narrative は同じ renderer の出力を Web 用の薄い adapter に変換する。

Web adapter は数式 fragment を `data-latex` へ分離し、既存 KaTeX 表示経路を使う。

```text
Web adapter
!= proof graph builder
!= Narrative rule engine
!= second mathematical engine
```

---

# 18. Generator execution

既存 status:

```text
NONE
AMBIGUOUS
EXECUTED
```

Phase 126 以降、

```text
proof-scope relevance
applicability relevance
executable relevance
```

を区別する。

Phase 132–133 は execution semantics を変更していない。

---

# 19. parser 境界

operation query grammar の既存境界を維持する。

対応:

```text
二項 top-level composition
三項 top-level composition
E / H の generator operand
E / H の二項 composition operand
Delta の generator operand
```

未対応:

```text
四項以上
E(a o b o c)
H(a o b o c)
Delta(a o b o c)
Unicode ∘
一般再帰 parser
```

group-query CLI の `k` は Phase 130 で負値を許可したが、これは operation-query parser の一般化ではない。

---

# 20. regression / test collection

Phase 終了時の全体回帰は

```powershell
python -m pytest tests -q
```

を標準とする。

repo 内 backup directory に copied `test_*.py` を置かない。

backup は repo 外へ保存する。

最新 repository-wide regression:

```text
9980 passed in 807.31s (0:13:27)
```

---

# 21. Phase 130 完了境界

```text
low-dimensional standard query recovery
stem 1–6 stable/theorem-specific specialization
k=0 diagonal semantics
n=1 higher-group semantics
negative stem input
connectivity zero
pi_0 boundary information
negative dimension out-of-domain information
pi16_9 concrete sigma9 standard-query connection
repository non-mutation
stale negative-k CLI test correction
```

final regression:

```text
9308 passed in 577.02s (0:09:37)
```

---

# 22. Phase 131 完了境界

```text
group-result → ProofStep path audit
group-result proof replay core API
existing recursive provenance reuse
depth 0 / 1 / 2 replay
source_entry / proof_step identity preservation
zero-group replay
connectivity-zero replay
CLI group-proof
Web result → Show proof
pi_0 / negative-dimensional domain-only boundary preservation
existing show-proof semantics preservation
```

final regression:

```text
9333 passed in 583.64s (0:09:43)
```

---

# 23. Phase 132 完了境界

```text
existing proof narrative capability audit
actual ProofStep.premises edge semantics confirmation
TodaGroupProofPresentation
deterministic Outline renderer
deterministic Narrative renderer
safe statement rendering / fallback
shared dependency Narrative deduplication
CLI --mode trace|outline|narrative
Trace default compatibility
Web Trace / Outline / Narrative selector
Web KaTeX preservation
existing replay depth semantics reuse
proof graph / repository non-mutation
```

final regression:

```text
9392 passed in 587.98s (0:09:47)
```

Phase 132 は presentation layer の拡張であり、Toda の新しい数学定理、operation evaluator、proof search algorithm は追加していない。

---

# 24. Phase 133 完了境界

Phase 133 は post-Phase-132 workflow pressure 監査から、Narrative の可読性改善を実装対象として選んだ。

変更範囲:

```text
Narrative presentation only
```

実装内容:

```text
shared dependency 再参照文面の整理
単数 premise: このことから
複数 premise: これらから
代表 aggregate statement の human-readable label
低次元 / nu-family / Proposition 5.11 / Proposition 5.15 / sigma-family label
sigma 系 bridge / branch 表現の日本語化
```

不変:

```text
ProofStep
proof graph
Trace
Outline
repository roots
theorem facts
replay depth semantics
operation-query semantics
execution semantics
```

最終監査対象:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9
$$

について depth 1 / 2 を確認し、代表的な内部 rule 名と旧 Narrative 文面が残っていないことを確認した。

focused regression:

```text
43 passed
```

repository-wide final:

```text
9403 passed in 605.52s (0:10:05)
```

Phase 133 完了。

---

# 25. Phase 134–136 完了境界

Phase 134–136 は proof semantics を変更せず、Narrative と Web presentation を段階的に改善した。

Phase 134:

```text
代表 theorem-specific Narrative
fact role / block role classification
Narrative document shell
REFERENCE block assembler
display-math / boundary / conclusion presentation primitives
```

Phase 135:

```text
Web Narrative display-math adapter
Web Narrative inline-math segmentation
inline KaTeX / display KaTeX mode separation
readability-oriented Web spacing
```

Phase 136-2 の代表対象:

$$
\pi_6^3=\mathbb Z/4\{\nu'\}.
$$

最終 Narrative では、Toda Lemma 5.2 の適用順序を数学的依存関係に合わせる。

まず

$$
2\eta_3=0
$$

を確認し、その後

$$
\{\eta_3,2\iota_4,\eta_4\}_1
$$

が定義できることを述べ、この bracket のある元を \(\nu'\) と定める。

Lemma 5.2 から

$$
\nu'\in\pi_6^3,
\qquad
H(\nu')=\eta_5,
\qquad
2\nu'=\eta_3^3
$$

を得る。

Toda Proposition 2.2 の右合成公式

$$
H(\alpha\circ E\beta)=H(\alpha)\circ E\beta
$$

を明示的に用い、

$$
H(\nu'\eta_6)
=
H(\nu'\circ E\eta_5)
=
H(\nu')\circ E\eta_5
=
\eta_5^2
$$

を表示する。

位数決定では次の EHP 完全列を表示する。

$$
\pi_7^3
\xrightarrow{H}
\pi_7^5
\xrightarrow{\Delta}
\pi_5^2
\xrightarrow{E}
\pi_6^3
\xrightarrow{H}
\pi_6^5.
$$

群構造決定では

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

を明示する。

重要な境界:

```text
Narrative ordering != new proof search
Narrative prose != new theorem fact
Toda Proposition 2.2 display != new inference semantics
short exact sequence display != new group calculation engine
Web KaTeX segmentation != mathematical normalization
```

Phase 136-2 focused regression:

```text
65 passed in 15.85s
```

repository-wide regression:

```text
9517 passed in 575.31s (0:09:35)
```

---

# 26. Phase 137 Web presentation cleanup 完了境界

Phase 136-2 の Web audit で確認した presentation-only pressure:

```text
Group query description:
pi_(n+k)^n
→ static mathematical text が KaTeX 未接続

Provenance / compact summary separator:
窶・Phase
窶・repository depth
窶・showing first
→ encoding / mojibake
```

Phase 137 では数学 semantics を変更せず、`templates/index.html` の presentation のみを修正した。

Group query の project quantity は

$$
\pi_{n+k}^{n}
$$

を既存 `data-latex` → `static/web_math.js` → KaTeX の経路へ渡す。

説明文中の数式なので既存 class

```text
group-proof-rendered-inline-math
```

を再利用し、`displayMode=False` とする。

文字化け separator は、過去の正常な template と同じ em dash `—` に戻す。

```text
— Phase
— repository depth
— showing first
```

`H(nu_prime)`、`E(nu_5)`、`sigma_11` などは operation / generator の入力 syntax 例なので plain text を維持する。

```text
static mathematical display
!= query input syntax example

Web presentation cleanup
!= mathematical semantics change
!= parser change
!= proof graph change
!= provenance change
```

focused regression:

```text
Phase 137-2: 3 passed in 6.96s
Phase 137-3 Web related: 56 passed in 20.23s
```

Phase 137-4 の manual Web verification では、

```text
\pi_{n+k}^{n} → KaTeX 表示
input syntax examples → plain text 維持
provenance separator → em dash
applicability compact summary → em dash
窶・ → 画面上に残らない
```

ことを確認した。

# 27. ドキュメント数式表示境界

README / design / development log / roadmap / proof records の display math は、GitHub Markdown 上で確実に数式表示されるよう `$$ ... $$` を標準とする。

inline math は既存どおり `\(...\)` を維持する。

```text
legacy display-math delimiter → $$ ... $$
inline \(...\) → 維持

documentation delimiter normalization
!= mathematical statement change
!= proof semantics change
```

Phase 137 final の repository-wide regression は、ドキュメント更新後の Phase-final step でのみ実行する。

# Phase 143 semantic Narrative 設計

Phase 143 では Narrative の数学的表示を、内部 `rule.name` に依存した fallback から、`ProofStep.conclusion` が保持する semantic statement の構造を読む表示へ移行した。

基本経路は次のとおり。

```text
ProofStep
→ conclusion semantic statement
→ statement fields / relation / membership / group structure
→ semantic LaTeX renderer
→ Narrative block / argument renderer
→ multi-argument Narrative
```

重要な境界:

```text
semantic statement
!= 新しい theorem fact

semantic renderer
!= inference rule

semantic rendering
!= proof search

Narrative ordering
!= proof graph mutation

rule-name fallback elimination
!= provenance elimination
```

Phase 143 の完了監査では、現行の

```text
_method_evidence_data(n, k)
→ presentation / blocks / sidecar / arguments
→ render_toda_group_proof_narrative_multi_argument_markdown()
```

という実際の Narrative 入口を使用した。

監査結果:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

したがって、Phase 143 で監査した current-entrypoint Narrative については、内部 rule-name fallback を通常の数学表示として残さないことを現在の不変条件とする。

## semantic statement と dependency の役割分離

statement が nested theorem / bridge / short exact sequence 等を dependency として保持していても、親 statement の renderer が dependency の数学的内容を勝手に再構成してはならない。

```text
statement の直接 semantic fields
→ statement 自身の表示

dependency ProofStep
→ proof graph / Narrative ordering

dependency の存在
!= 親 statement の追加数学的結論
```

この原則により、保存された fields に零端点がない短完全列を renderer が推測して補う、といった表示上の theorem synthesis を避ける。

## direct premise suppression / relocation / preservation

Phase 143 終盤では、semantic statement の表示と既存の Narrative 重複抑制・relocation の境界を整理した。

特に direct premise は次の分類を混同しない。

```text
redundant direct premise
relocatable direct premise
context-hidden step
DERIVATION source block として保持すべき semantic premise
```

`context_hidden_step_ids` は引き続き最優先で非表示とする。

一方、DERIVATION source block として保持対象になった block 内の `redundant_direct_premise_step_ids` は、semantic な導出根拠そのものを失わないため表示を保持できる。

ただし `relocated_direct_premise_ids` の suppression は一律に解除しない。これにより、例えば

$$
2\nu_5=E^2\nu'
$$

は元位置と relocation 先に二重表示されず、既存の依存順序に従って一度だけ表示される。

また

$$
\pi_{15}^{8}
\cong
\mathbb Z/8\{E\sigma'\}
\oplus
\mathbb Z\{\sigma_8\}
$$

という transported decomposition は、その後の標準順序

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}
$$

とは異なる導出上の意味を持つため、両方を保持する。

```text
transported decomposition
!= final standard-order conclusion

semantic preservation
!= duplicate preservation

relocation
!= deletion of proof provenance
```

Phase 143 は presentation semantics の改善であり、Toda の新しい数学定理、group-query semantics、operation evaluator、proof search algorithm は追加していない。

---

# 28. Phase 144 generic Narrative / ownership boundary

Phase 144 は、Phase 143 で semantic statement rendering を整備した後、証明全体の
Narrative を一般構造だけで組み立てる際の ownership（所有関係）、argument boundary
（議論境界）、contribution ordering（寄与の順序）を監査した。

基本経路は次のとおり。

```text
TodaGroupResult
→ existing ProofStep provenance
→ replay / complete replay
→ TodaGroupProofPresentation
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ proof chains / contributions
→ contribution-aware generic Narrative renderer
```

この経路は新しい proof search ではない。

```text
complete replay
!= new theorem search

semantic closure
!= theorem synthesis

argument ownership
!= proof edge ownership

Narrative contribution placement
!= proof graph mutation
```

## explicit depth と complete replay

Narrative では explicit positive depth の presentation に必要な semantic dependency が
bounded replay の外側にある場合がある。このため complete replay API を用いる経路を持つ。

ただし depth 0 は root のみを要求する明示的境界であり、complete replay へ切り替えない。

```text
Narrative + explicit depth > 0
→ 必要に応じて complete replay から presentation を構築

Narrative + depth 0
→ bounded depth-0 replay を維持
```

Phase 144 final regression repair では、この depth 0 境界を `main.py` で復元した。

## R25-30-R3 ownership / argument-boundary endpoint

Phase 144-6 の技術調査は R25-30-R3 を endpoint とする。

6代表群の current inventory:

```text
pi_6^3:  selected=6   participating=6/6   detached=0/0    transport=1
pi_8^5:  selected=10  participating=7/7   detached=3/3    transport=1
pi_10^4: selected=22  participating=0/0   detached=22/0   transport=2
pi_12^5: selected=46  participating=2/2   detached=44/0   transport=4
pi_15^8: selected=54  participating=10/10 detached=44/0   transport=4
pi_16^9: selected=54  participating=10/10 detached=44/0   transport=4
```

aggregate:

```text
selected=192
participating=35
detached=157
detached_insertable=3
missing=0
```

R25-30-R3 では、対象3ケースの boundary classification と existing child Argument pair が
一致した。したがって `detached_insertable=3` を ownership leak とみなして旧
`detached_insertable=0` へ戻してはならない。

```text
historical R5 fixed-count snapshot
!= current semantic gate
```

## result-reuse pressure の分離

$\pi_{15}^{8}$、$\pi_{16}^{9}$ などで group-structure / definition の owned entry が
大きな proof subtree を再帰的に展開する現象が確認された。

これは

```text
argument-boundary leak
```

ではなく、

```text
already-established result の proof subtree を再展開する result-reuse problem
```

として分離する。

Phase 144 ではこの問題の一般解を実装しない。具体的な証明で必要になった Phase 146
以降に、その1課題だけを解く最小一般規則として扱う。

## Phase 144 regression evidence

canonical final repository-wide run:

```text
10298 collected
10273 passed
25 failed
2321.20s (0:38:41)
```

25 failures は R5-39〜R5-43 の historical completion / fixed-count snapshot に集中した。
production renderer は変更せず、固定件数を新しい固定件数へ置換することもせず、
current structural invariant に maintenance した。

focused maintenance regression:

```text
66 passed in 1308.82s (0:21:48)
```

この maintenance 後は repository-wide suite を再実行していない。そのため設計記録では
「全体 10298 passed」とは記載しない。

## Phase 145 / Phase 146+ 境界

Phase 145:

```text
default presentation → Narrative
default depth → 2
```

のみを扱う。

Phase 145 では result reuse、ownership の追加一般化、statement type の先回り実装を行わない。

Phase 146 以降:

```text
具体的に通したい証明
→ その証明で不足している1課題を特定
→ target-specific special case ではなく最小一般規則で解く
→ focused regression
→ 既存証明を壊さない
```

を1 Phaseずつ繰り返す。

# 29. Phase 145 完了境界

Phase 145 の機能変更は group-proof の default presentation だけである。

```text
default mode
→ Narrative

default depth
→ 2
```

CLI の default は概念的に次と同値である。

```powershell
python main.py group-proof n k --mode narrative --depth 2
```

Web group-proof も同じ default を使用する。

明示指定は従来どおり維持する。

```text
--mode trace
--mode outline
--mode narrative

--depth 0
--depth 1
--depth 2
```

したがって:

```text
default presentation change
!= replay semantics change
!= proof graph change
!= proof provenance change
!= theorem fact change
!= new proof search
```

Phase 145 の repository cleanup では historical Phase artifact を
`archive/phases/` 以下へ整理した。

cleanup 後の canonical test collection で、既存 test suite に

```text
tests.test_* package import
bare test_* import
```

の2形式が共存していることを確認した。

最終的な test-only compatibility boundary は:

```text
tests/__init__.py
→ tests package を明示

tests/conftest.py
→ tests directory を import path に追加
```

である。

これは既存 canonical test 本体の大量書き換えを避けるための test infrastructure であり、
production import semantics を変更しない。

Phase 145 focused regression:

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

Phase 145 完了。

Phase 146 以降は1 Phase につき1つの concrete issue を選び、その issue に必要な
最小一般規則だけを追加する。

```text
one concrete issue
→ minimum general rule
→ focused regression
→ existing proof preservation
```

Phase 145 では result-reuse、追加の ownership model、将来 proof のためだけの
semantic rule、一般 evaluator は実装していない。

---

# 30. Phase 146 historical Narrative difference audit / root-cause boundary

Phase 146 は、現在の generic Narrative が historical Phase 136-2 の
$\pi_6^3=\mathbb Z/4\{\nu'\}$ Narrative と同等の数学的説明構造を一般規則だけで
再構成できているかを監査した。

Phase 146 の基準 historical commit は

```text
908e24db89669750949fa9ad149f5e306ac05546
```

とする。

## current generic route boundary

現行 $\pi_6^3$ public Narrative は target-specific な route gate を通るが、その gate 内部では

```text
presentation
→ semantic sidecar
→ Narrative blocks
→ Narrative arguments
→ contribution-aware generic renderer
```

を使用する。

Phase 146-5 では current public $\pi_6^3$ output と current generic contribution renderer
output の exact parity を確認した。

これは

```text
current public pi_6^3
=
current generic pi_6^3
```

を意味するが、

```text
current generic pi_6^3
=
historical Phase 136-2 Narrative
```

を意味しない。

したがって route parity と historical quality parity を区別する。

## Phase 146-7 generic prose repair

Phase 146-7 では `render_toda_group_proof_narrative_argument_header_method_section()` に
generic argument-purpose prose fusion を追加した。

従来の

```text
$X$ の位数を決定する.
そのために、次の完全列を考える.
```

を、primary exactness method が argument に対応する場合に

```text
$X$ の位数を決定するために、次の完全列を考える.
```

と一文に統合する。

これは target-specific な $\pi_6^3$ 文面ではなく argument role と method component に基づく
一般表示規則である。

focused regression:

```text
11 passed
```

existing $\pi_6^3$ public-route regression:

```text
4 passed
```

Phase 146-7 では EHP naming、exactness ownership、contribution ordering、Reference prose、
equation numbering は変更していない。

## Phase 146-8 historical full structural diff

Phase 146-8 では historical Phase 136-2 と current generic Narrative を構造比較した。

raw unit inventory:

```text
historical units: 17
current units: 82
PRESERVED: 0
LOST: 17
ADDED: 47
MOVED: 0
DUPLICATED: 35
REWORDED: 0
UNMATCHED: 0

sequence-related units:
historical 4
current 44

[R#] units:
historical 8
current 1
```

ただし historical と current では unit 粒度が異なるため、

```text
PRESERVED=0
LOST=17
```

を「数学的事実が17件失われた」と解釈してはならない。

この audit の有効な結論は、historical と current の文章構造に大きな差があり、
特に exactness の過剰展開、Reference provenance の縮退、重複、配置順の差が
定量的に存在することである。

## Phase 146-9 root-cause classification

Phase 146-9 は production code を変更せず、Phase 146-8 で整理した12の visible difference
families を内部原因へ分類した。

$\pi_6^3$ current argument diagnostics:

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

したがって order argument の問題は

```text
primary exactness component が存在しない
```

ことではない。

正しくは、

```text
current argument-method ownership / selection
!= historical proof-purpose ownership / explanatory placement
```

である。

また renderer layer では

```text
base multi-argument chars: 1377
contribution-connected chars: 1579
contribution renderer changes output: True
argument builder uses direct dependency indices: True
contribution renderer performs post-render insertion: True
```

を確認した。

## six root causes

Phase 146-8 の12 visible difference families は次の6 root causes に集約する。

### RC1 — Argument-method ownership

historical proof-purpose と current argument-method ownership の差。

主対象:

```text
order argument と主要 EHP 完全列の ownership
method introduction の一部
```

### RC2 — Recursive exactness evidence exposure

primary method に吸収されない recursive exactness evidence が body / contribution として
露出する。

主対象:

```text
主要完全列の範囲選択
補助完全列の本文抑制
exactness contribution 重複の一部
```

### RC3 — Contribution ownership / insertion ordering

argument dependency narration と contribution の ownership / post-render insertion が別経路である。

主対象:

```text
contribution 重複の一部
dependency order に沿った式配置
map-property chain の配置
short exact sequence → group structure の順序
```

### RC4 — Generic provenance / reason prose

compact Reference は保持されても historical の

```text
[R#] の n=... の場合より
```

のような derived-fact reason prose を一般的に再構成できていない。

主対象:

```text
Reference section の詳細
Reference → derived fact の理由付け
definition argument の理由文章の一部
```

### RC5 — EHP semantic naming

generic transition は

```text
次の完全列を考える
```

と表示するが、stored semantics から

```text
EHP 完全列
```

という method family name をまだ一般的に表示しない。

### RC6 — Final equation numbering / prose formatting

equation numbering は selected / ordered Narrative stream の下流にある。

したがって RC1〜RC5 より先に target-specific tag rule で historical numbering を再現してはならない。

## dependency order

修正順序は

```text
RC1
→ RC2
→ RC3
→ RC4
→ RC5
→ RC6
```

とする。

RC6 は selection / ordering の下流なので最後に扱う。

## Phase 146 closure boundary

Phase 146 で実施した production change は Phase 146-7 の generic argument-purpose prose fusion
のみである。

Phase 146-8 / 146-9 は audit only であり、次は変更していない。

```text
pi_6^3 public route gate
exactness ownership
contribution selection
generic provenance rendering
EHP semantic naming
final equation numbering
```

Phase 146 完了時点では $\pi_6^3$ 専用 route gate を削除しない。

Phase 147 以降は上記 root cause を1件ずつ一般規則として扱う。

```text
one root cause
→ minimum general rule
→ focused regression
→ historical/current structural comparison
→ existing proof preservation
```

Phase 146 closure documentation 自体は production semantics を変更しない。

---

# Phase 148 設計完了記録 — Recursive exactness evidence exposure

Phase 148 / RC2 の責務は、既存 proof provenance に含まれる recursive exactness evidence
（再帰的な完全性証拠）を Narrative 本文へどこまで展開するかを一般規則として決定することである。

## exposure pipeline

```text
ProofStep / provenance
→ method evidence
→ RC1: Argument-method ownership
→ RC2: exactness exposure classification
→ Narrative body
```

Phase 148 では exactness method component を次の3分類で扱う。

```text
OWNED_PRIMARY
UNOWNED_RECURSIVE
AMBIGUOUS_RELEVANT
```

### OWNED_PRIMARY

Argument が primary method として所有する component。

```text
raw EXACTNESS_WINDOW
→ 本文では抑制

DERIVED_SHORT_EXACT_SEQUENCE / higher-level method contribution
→ ownership と contribution rule に従って保持可能

provenance
→ 保持
```

### UNOWNED_RECURSIVE

recursive provenance から到達するが、その Argument の primary method として所有されない component。

```text
body contribution
→ 自動展開しない

raw exactness
→ 自動展開しない

derived short exact sequence
→ 自動展開しない

provenance
→ 保持
```

### AMBIGUOUS_RELEVANT

複数 component が直接 relevant で一意な owner を決定できない場合。

```text
conservative fallback
→ 既存表示を維持
→ renderer が ownership を推測しない
```

## semantic closure boundary

Web Narrative は selected depth の bounded replay を入力とする。

```text
selected bounded replay
→ semantic closure
→ Narrative renderer
```

complete replay を Web Narrative の入力として常用しない。

depth 0 では semantic closure は identity とする。

positive depth では、既存 provenance のうち Narrative に必要な最小 dependency のみを補う。
Phase 148 で追加した calculation closure は、

```text
ORDER relation
→ direct EQUALITY premise
→ その equality の direct EQUALITY premises
```

という graph-level relation に限定する。

これにより $\pi_6^3$ の位数計算に必要な equality chain は補う一方、
group-structure context や Hopf chain の無関係な equality を一括で展開しない。

既存の registered definition semantic closure は維持する。

```text
semantic closure
!= new proof search
!= new theorem fact
!= proof edge creation
```

## Phase 149 との境界

Phase 148 は exposure を扱い、ordering は扱わない。

```text
RC2:
どの exactness evidence を本文に出すか

RC3:
表示対象 contribution をどの順序に置くか
```

したがって、

```text
short exact sequence
→ final group conclusion
```

のような数学書としての説明順序は Phase 149 / RC3 の責務とする。

---

<!-- PHASE149_RC3_CLOSURE -->
# Phase 149 RC3 Narrative contribution ordering

Phase 149 は Phase 146 で RC3 と分類した Narrative contribution ordering（Narrative 寄与の配置順）を扱う。

責務の分離は次のとおり。

```text
RC1:
Narrative Argument
→ primary method ownership

RC2:
primary / recursive method evidence
→ exposure classification

RC3:
visible owned evidence
→ Narrative placement
```

RC3 の一般順序は次を目標とする。

```text
method
→ evidence
→ derivation
→ conclusion
```

`OWNED_PRIMARY` exactness evidence は、RC2 の既存 contribution 抽出・filter をそのまま利用し、owner Argument の conclusion より前へ配置する。

重要なのは、global Narrative block order を proof の説明順そのものと見なさないことである。

```text
global block order
!= Argument-local explanatory order
```

Phase 149 RC3-3 では、`OWNED_PRIMARY` exactness contribution を body loop の前に収集し、元 exactness block 位置での重複表示を抑止し、owner conclusion block の直前へ挿入する。

この処理は presentation-only である。

```text
exactness placement
!= exactness exposure reclassification
!= ProofStep relocation
!= proof edge mutation
!= theorem fact creation
```

6代表群

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_10^4,\quad
\pi_12^5,\quad
\pi_15^8,\quad
\pi_16^9
$$

の RC3-4 audit では全 Argument で ordering invariant が成立した。

```text
failures=[]
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

repository-wide final regression:

```text
﻿10416 passed in 1315.93s (0:21:55)
```

なお、$\pi_6^3$ の order Argument 内で

$$
2\nu'=\eta_3^3
$$

という derived calculation の表示位置をさらに自然にできる余地はある。しかしこれは RC3 の exactness evidence placement とは異なる calculation / derivation internal ordering の問題であり、Phase 149 では変更しない。
---

<!-- PHASE150_CLOSURE -->
# 34. Phase 150 完了境界 — generic provenance / reason prose

Phase 150 は Phase 146 で RC4 と分類した `Generic provenance / reason prose`
を対象とした。

数学的 ground truth は引き続き次である。

```text
ProofStep.conclusion
ProofStep.premises
ProofStep.inference_rule
existing recursive provenance
```

Phase 150 の reason layer は、これらの既存 provenance から Narrative に必要な
「なぜこの結論を述べられるか」を型付きで表す presentation-side structure である。

```text
typed Narrative reason
!= new theorem fact
!= new proof edge
!= new proof search
!= theorem ranking
```

reason prose は typed reason から生成する。複数の異なる typed reason instance が
同一の汎用 sentence を生成する場合がある。その場合、文字列を一意化して1回だけ表示することを
正しさの条件にはしない。

正しい表示契約は sentence $s$ ごとに

$$
\#\{\text{typed reason instances rendering to }s\}
=
\#\{\text{occurrences of }s\text{ in Narrative}\}
$$

である。

6代表群の multiplicity audit では、問題となった共通 sentence について次を確認した。

```text
pi_6^3:  typed=3, rendered=3
pi_8^5:  typed=3, rendered=3
pi_10^4: typed=2, rendered=2
pi_12^5: typed=2, rendered=2
pi_15^8: typed=1, rendered=1
pi_16^9: typed=3, rendered=3
```

したがって Phase 150 final repair は production renderer を変更せず、historical test contract
を instance multiplicity に合わせた。

## renderer-route 境界

Phase 150 では段階的 generic route 移行を進めた結果、複数 renderer の共存そのものが
群間の表示差を生み、代表群ごとの修正では一般化の評価が難しいことを確認した。

したがって Phase 150 では group-by-group migration を継続しない。

```text
Phase 150
→ RC4 reason semantics / prose の確立
→ route coexistence を architectural pressure として確認
→ incremental migration をここで停止

Phase 151
→ whole-population generic baseline
```

Phase 151 では対象群を同じ generic renderer へ強制的に通して観測するが、
public renderer selection は変更しない。

```text
generic baseline audit
!= public route switch
!= dedicated renderer deletion
!= legacy fallback deletion
```

## test strategy

Phase 150 final full regression は closure baseline として全 `tests` を1回実行した。

```text
10478 passed in 2505.44s (0:41:45)
pytest exit code: 0
wall-clock elapsed: 00:41:56.919
```

この約42分の historical full suite を、今後すべての Phase 終了時に必須とはしない。

通常の開発サイクルは次とする。

```text
RC / repair
→ focused tests

Phase closure
→ focused tests
→ maintained canonical regression

major integration / release milestone
→ complete historical regression
```

test suite 自体についても、後続 Phase で現在の保証を重複して検証する historical test、
audit-only test、旧 renderer contract を整理し、canonical regression を明示する。

ただし test 数の削減そのものを目的とせず、現在の仕様・数学的 provenance・public API の
保証を維持することを優先する。

## Phase 151 境界

Phase 151 は `All-Group Generic Baseline` とする。

目的:

```text
同一 population
→ 同一 generic route
→ 同一 depth / observation conditions
→ success / failure / fallback / semantic inventory を一括取得
```

Phase 151 では generic renderer の欠陥をその場で群別修正しない。
まず全体像を取得し、欠陥分類を次 Phase の入力とする。

---

# 35. 現行 regression 方針

旧方針の「Phase 終了時に必ず repository-wide full regression」は Phase 150 closure をもって
運用上の標準から外す。

現行方針:

```text
focused regression
→ 日常の実装・repair

canonical regression
→ Phase closure の標準

complete historical regression
→ renderer 統一、public API 大変更、release 等の大きな節目
```

完全な historical suite は削除せず、必要な節目で再実行できる状態を維持する。

---

<!-- PHASE153_CLOSURE -->
# Phase 153 — Narrative Reference selection / granularity 設計

Phase 153 は Narrative の Reference（参照）を、単なる provenance の列挙ではなく、
「本文で実際に使用される外部結果の境界」として扱う一般規則を整理した。

新しい Toda theorem fact、ProofStep、proof edge、proof search は追加していない。

## Reference の基本境界

Phase 153 後の設計では、Narrative Reference は次を満たす。

```text
external Reference
!= current root theorem

displayed Reference
→ proof ancestry / proof-use に基づく

marker-bearing route
→ 本文で使用された [Rk] だけを残す

generic no-marker route
→ 実際に表示へ参加した step identity から Reference を残す
```

current `presentation.root_step` が持つ `LiteratureReference` は、renderer route に
依存せず external Reference section へ出さない。

```text
root theorem provenance
!= external supporting Reference
```

## literature-reference identity

同じ文献 locator が label 違いで複数表現される場合、locator を canonical identity として扱う。

```text
both locators exist
→ locator equality を優先

otherwise
→ full LiteratureReference equality
```

これにより、たとえば同じ `(5.2)` を異なる label で保持する step があっても、
root Reference exclusion の意味論を route 間で一致させる。

## Reference granularity

Reference は aggregate root 全体を機械的に選ぶのではなく、consumer が実際に利用する
proof boundary を優先する。

aggregate conclusion の複数 component のうち、consumer の generator / structure に対応する
component が一意に特定できる場合、その component を表示対象とする。

```text
aggregate provenance
→ consumer-relevant component
→ external Reference statement
```

これは theorem fact の分解や変更ではなく presentation granularity である。

## Reference reuse

本文中で exact step がすでに Reference statement として表示されている場合、その step は
再利用可能な proof boundary として扱う。

```text
displayed Reference step
+ premises
→ [Rk] を用いる
→ recursive derivation expansion を抑制
```

title-only Reference はこの boundary にはしない。

```text
Reference reuse
!= ProofStep deletion
!= premise deletion
!= provenance deletion
```

## used-Reference filtering

marker-bearing route では本文に現れる `[Rk]` を実使用集合とし、未使用 Reference を除外した後、
番号を連続化する。

generic route では explicit marker が無いため、表示へ参加した argument / local-body /
contribution step identity を用いて Reference 使用を帰属する。

specialized route では既存 marker mapping を壊さないことを優先し、root exclusion によって
mapping が変質する場合は specialized renderer 自身の Reference section を保持する。

## 112-group closure invariant

depth 2 の標準対象

$$
n=2,\ldots,15,
\qquad
k=0,\ldots,7
$$

について次を closure invariant とした。

```text
render errors = 0
Reference numbering is contiguous
root LiteratureReference is not external
body marker never points to a missing Reference
marker-bearing route has no unused displayed Reference
```

最終 audit:

```text
scanned groups: 112
render errors: 0
violations: 0
```

## Phase 153 の境界

```text
Reference selection / granularity
!= theorem selection
!= theorem ranking
!= proof search
!= proof graph mutation
!= proof-prose quality completion
```

接続語重複、内部 rule-name の露出、英語 statement、重複 scalar 表現、句読点などの
proof-prose generation は Phase 154 へ送る。

historical test suite の consolidation（整理）は独立 maintenance とし、Phase 154 の
proof-prose 改善を妨げる前提条件にはしない。
