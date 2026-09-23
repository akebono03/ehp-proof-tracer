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
safe fallback != 推測した数学的説明
candidate selection != theorem ranking
Web execution != second execution engine
executable relevance filtering != theorem ranking
group-result proof replay != generator lookup
group-result proof replay != new proof search
proof narrative != new proof
Outline != proof search
Narrative deduplication != proof graph deletion
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

\[
1\le m<n
\]

なら sphere connectivity により

\[
\pi_m(S^n)=0
\]

として扱う。

Phase 130 ではこの connectivity zero を repository-backed `TodaGroupResult` として具体化するため、Phase 131 以降の group-result proof replay 対象になる。

## \(m=0\)

\[
\pi_0(S^n)
\]

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

\[
\pi_n^n\cong\mathbb Z\{\iota_n\}.
\]

これは `k=0` の query に対応する。

## circle higher groups

既存 Phase 56 の symbolic zero

\[
\pi_{i-1}^1=0
\]

を concrete query に specialize する。

したがって

\[
n=1,\quad k\ge1
\]

では

\[
\pi_{1+k}^1=0.
\]

新しい独立 theorem root は追加しない。

## connectivity zero

\[
1\le n+k<n
\]

では foundational sphere connectivity として zero result を返す。

この結果は `ProofRepositoryEntry` と `ProofStep` を持つ。

---

# 5. stem 1–3 specialization

Phase 130 では既存 symbolic theorem を standard query から具体化できるようにした。

## stem 1

\[
\pi_{n+1}^n=\mathbb Z/2\{\eta_n\}.
\]

## stem 2

\[
\pi_{n+2}^n=\mathbb Z/2\{\eta_n\eta_{n+1}\}.
\]

## stem 3

\[
\pi_{n+3}^n=\mathbb Z/8\{\nu_n\}.
\]

低次元 concrete boundary が既存 proof にある場合は concrete proof を優先する。

---

# 6. stem 4–6 specialization

## stem 4

\[
\pi_{n+4}^n=0,
\qquad n\ge6.
\]

## stem 5

低次元 concrete branch を proof ancestry から回収し、

\[
\pi_{n+5}^n=0,
\qquad n\ge7
\]

を symbolic branch から specialize する。

## stem 6

\[
\pi_{n+6}^n=\mathbb Z/2\{\nu_n^2\}.
\]

既存 concrete \(n=5,6,7,8\) を維持し、symbolic specialization はその境界より上で使う。

---

# 7. stem 7 / sigma family

Toda Proposition 5.15 の既存証明には

\[
\pi_{16}^9=\mathbb Z/16\{\sigma_9\}
\]

という concrete proof が存在する。

また symbolic higher branch として

\[
\pi_{n+7}^n=\mathbb Z/16\{\sigma_n\},
\qquad n\ge9
\]

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

\[
\pi_{16}^9=\mathbb Z/16\{\sigma_9\}.
\]

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

\[
E(\nu_5)=\nu_6,
\qquad
E(\sigma_{11})=\sigma_{12},
\]

\[
E(\nu_5\eta_8)=0,
\qquad
E\nu' \in \pi_7^4.
\]

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

\[
\pi_9^2=0.
\]

また Phase 130 の foundational connectivity zero:

\[
\pi_{10}^{11}=0
\]

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

statement 表示の優先順は、安全に既存 renderer を利用し、未対応 statement では rule name / type name fallback を使う。

```text
Narrative
!= theorem inference
!= mathematical paraphrase guessing
!= provenance-free LLM proof
```

---

# 15. Narrative shared-dependency deduplication

Phase 132-8 で Narrative 表示に `ProofStep` identity 単位の shared-dependency deduplication を追加した。

cycle guard と dedup state は別物として扱う。

```text
active_step_ids
→ 現在の再帰 stack 上の cycle guard

expanded_step_ids
→ Narrative で既に subtree を展開済みか
```

最初の出現:

```text
subtree を通常展開
```

後続出現:

```text
既出の ... を用いる。
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

`--mode` 省略時は `trace`。

既存 Phase 131 semantics を維持する。

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

Outline / Narrative は Phase 132 renderer の出力を Web 用の薄い adapter に変換する。

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

Phase 132 は execution semantics を変更していない。

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

# 24. 次 Phase との境界

Phase 133 は post-Phase-132 capability / workflow pressure audit とする。

最初に確認する:

```text
現在の group query
Trace / Outline / Narrative の実利用
operation query の残件
standard query の次の不足
Web workflow の実利用上の不足
```

実装対象を先に決め打ちしない。

先取りしないもの:

```text
general E evaluator
general H evaluator
general Delta evaluator
general membership evaluator
higher stem の無条件追加
general symbolic AST substitution
arbitrary proof-scope theorem mining
theorem ranking
automatic best-target selection
unbounded proof search
free-form provenance-free proof generation
```
