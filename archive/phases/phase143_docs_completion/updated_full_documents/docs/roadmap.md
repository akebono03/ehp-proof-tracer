# EHP Proof Tracer ロードマップ

この文書は**今後の機能依存関係と Phase 順序**を記録する。

過去の実装履歴は `docs/development_log.md`、現在の設計は `docs/design.md`、代表的な証明記録は `docs/proof_records.md` を参照する。

---

# 1. 現在地

標準 group query:

```text
n,k
→ query-domain classification
→ foundational specialization
→ standard production repository
→ TodaGroupQuery
→ direct known-group lookup
→ concrete proof recovery
→ 必要なら theorem-specific stable specialization
→ TodaGroupResult
→ structured presentation
→ report
```

group-result proof:

```text
TodaGroupResult
→ existing proof_step / source_entry
→ recursive provenance
→ depth-limited replay
→ TodaGroupProofPresentation
→ Trace / Outline / Narrative
→ human-readable Narrative labels
→ theorem-specific natural Narrative blocks
→ shared presentation primitives
→ CLI / Web
```

operation query:

```text
query
→ direct lookup
→ direct miss
→ exact theorem-specific handoff
→ presentation
→ query-proof
```

基本境界:

```text
direct lookup first
limited theorem-specific handoff != general query inference
query != general evaluator
GROUP_MEMBERSHIP != general membership evaluator
group containment != operation result
LOOKUP_MISS != evaluator required
stable specialization != general AST substitution
concrete proof recovery != arbitrary theorem mining
negative stem input != negative homotopy group definition
pi_0 information != ordinary group result
Web UI != new mathematical engine
depth control != new proof search
candidate selection != theorem ranking
group-result replay != generator lookup
group-result replay != theorem search
proof narrative != new proof
Narrative deduplication != proof graph deletion
Narrative label != theorem fact
Narrative semantic role != theorem fact
presentation primitive != proof semantics
theorem-specific Narrative != generic theorem synthesis
```

---

# 2. 完了済み機能

## Phase 90–111

```text
Toda group query / normalization
EHP / proof provenance
reporting
generator exploration
recursive proof scope
applicability discovery
qualified execution
known-group identity
indexed sigma specialization
show-proof
operation query / query-proof
3-term top-level composition query
replay --depth
```

## Phase 112–115

```text
real workflow pressure audit
symbolic sigma_n → TodaGroupQuery integration
E(nu_5)=nu_6 handoff
E(sigma_11)=sigma_12 handoff
```

## Phase 116–125

```text
Flask / KaTeX Web UI
group query
operation query / query-proof
generator show-proof
generator explore
generator explore-proof
generator explore-applicable
generator execute
workflow navigation
```

## Phase 126–129

```text
proof-scope / applicability / executable relevance separation
operation-query capability pressure audit
E(nu_5 o eta_8)=0 handoff
E(nu_prime) membership semantics
E nu' in pi_7^4 handoff
GROUP_MEMBERSHIP result classification
```

Phase 129 final:

```text
9268 passed in 569.71s (0:09:29)
```

## Phase 130

```text
low-dimensional query recovery
stem 1 eta specialization
stem 2 eta^2 specialization
stem 3 nu specialization
stem 4 Prop.5.8 zero specialization
stem 5 Prop.5.9 concrete + zero specialization
stem 6 Prop.5.11 nu^2 specialization
k=0 diagonal Z{iota_n}
n=1 higher groups zero
negative stem acceptance
positive below-diagonal connectivity zero
pi_0 boundary information
negative dimension out-of-domain information
pi16_9 = Z/16{sigma_9} concrete standard-query connection
stale CLI negative-k test correction
```

final:

```text
9308 passed in 577.02s (0:09:37)
```

Phase 130 完了。

## Phase 131

```text
group-result → ProofStep path audit
TodaGroupResultProofReplayStep
TodaGroupResultProofReplayResult
build_toda_group_result_proof_replay()
existing recursive provenance reuse
depth 0 / 1 / 2
ProofStep identity preservation
source_entry identity preservation
zero-group replay
connectivity-zero replay
CLI group-proof n k
CLI group-proof n k --depth N
Web group result → Show proof
Web proof depth 0 / 1 / 2
pi_0 / negative-dimensional domain-only result exclusion
existing generator show-proof semantics preservation
```

final:

```text
9333 passed in 583.64s (0:09:43)
```

Phase 131 完了。

## Phase 132

Phase 132 は group-result proof replay の presentation layer を拡張した。

完了内容:

```text
proof narrative capability audit
ProofStep.premises edge semantics confirmation
TodaGroupProofPresentation
deterministic Outline
deterministic Narrative
safe statement / rule / type fallback
shared dependency Narrative deduplication
CLI group-proof --mode trace|outline|narrative
Trace default preservation
shared --depth semantics
Web Trace / Outline / Narrative selector
Web KaTeX preservation
proof graph non-mutation
repository non-mutation
```

final:

```text
9392 passed in 587.98s (0:09:47)
```

Phase 132 完了。

## Phase 133

Phase 133 は post-Phase-132 workflow pressure から Narrative readability を選択した。

完了内容:

```text
representative Narrative readability audit
shared dependency 再参照文面の整理
premise 1件 → このことから
premise 2件以上 → これらから
代表 aggregate statement の human-readable label
低次元 / nu-family / Proposition 5.11 / Proposition 5.15 / sigma-family label
sigma 系 bridge / branch 表現の最終日本語化
representative five-group depth 1 / 2 final audit
```

代表監査:

$$
\pi_6^3,\quad
\pi_8^5,\quad
\pi_{10}^4,\quad
\pi_{12}^5,\quad
\pi_{16}^9
$$

```text
Internal wording audit
→ 0件

Old / awkward Narrative wording
→ 0件
```

final:

```text
9403 passed in 605.52s (0:10:05)
```

Phase 133 完了。

## Phase 134

Phase 134 は Narrative を代表的な数学的証明として自然に読める形へ改善し、その後 presentation-only 共通化を行った。

代表3例:

$$
\pi_6^3=\mathbb Z/4\{\nu'\},
$$

$$
\pi_8^5=\mathbb Z/8\{\nu_5\},
$$

$$
\pi_{15}^{8}
=
\mathbb Z\{\sigma_8\}
\oplus
\mathbb Z/8\{E\sigma'\}.
$$

完了内容:

```text
pi_6^3: order / membership / group-structure Narrative
pi_8^5: nu_5 order / boundary / quotient Narrative
pi_15^8: Proposition 4.4 transport Narrative
TARGET / REFERENCE / DEFINITION / BOUNDARY / DERIVED fact roles
ORDER / MEMBERSHIP / GROUP_STRUCTURE / OTHER block roles
Narrative document shell commonization
REFERENCE block assembler
display-math presentation primitive
completed-boundary presentation primitive
final-conclusion presentation primitive
three-example cross audit
Phase-specific helper / hardcode re-audit
completion audit
```

維持した境界:

```text
presentation commonization only
!= theorem logic generalization
!= generic multi-generator proof synthesis
!= generic direct-sum theorem synthesis
!= new proof search
```

final focused regression:

```text
40 passed in 5.78s
```

final repository-wide regression:

```text
9495 passed in 282.46s (0:04:42)
```

Phase 134 完了。

---

# 3. standard-query coverage through stem 7

```text
k < 0
→ target dimension に応じて connectivity zero / pi_0 info / out-of-domain

k = 0
→ Z{iota_n}

k = 1
→ eta family

k = 2
→ eta^2 family

k = 3
→ nu family

k = 4
→ Prop.5.8 family / zero branch

k = 5
→ Prop.5.9 family / zero branch

k = 6
→ nu^2 family

k = 7
→ sigma family
```

具体的定理 branch がある場合は generic specialization より既存 concrete proof を優先する。

---

# 4. 現在の proof access

generator 起点:

```text
generator
→ known-group identity
→ show-proof
```

group query 起点:

```text
n,k
→ TodaGroupResult
→ replay
→ Trace / Outline / Narrative
→ CLI / Web
```

operation fact 起点:

```text
query
→ selected operation fact
→ query-proof
```

これらは同じ `ProofStep` / provenance infrastructure を利用する。

---

# 5. Phase 135–137 presentation cleanup

Phase 135 は Web Narrative の display / inline math presentation を監査し、既存 KaTeX 経路を Narrative に適合させた。

Phase 136-2 は

$$
\pi_6^3=\mathbb Z/4\{\nu'\}
$$

の Narrative を数学的依存関係に合わせて再構成した。

Phase 137 は Phase 136-2 closure audit で確認した Web presentation-only pressure を修正した。

完了内容:

```text
Group query の \pi_{n+k}^{n} を static KaTeX へ接続
窶・ separator 6か所を em dash へ復元
operation / generator input syntax examples は plain text 維持
Phase 137-2 focused: 3 passed
Phase 137-3 related Web regression: 56 passed
Phase 137-4 manual Web verification
Phase 137-5 documentation update
main docs display math → GitHub-friendly $$ blocks
```

境界:

```text
static math display → KaTeX
query / generator input syntax examples → plain text
Web presentation cleanup != mathematical semantics change
Web presentation cleanup != parser change
documentation delimiter cleanup != mathematical content change
```

Phase 137 final の repository-wide regression は Phase-final step で実行する。

Phase 137 完了後の次段階は Phase 138 capability audit とする。

候補:

```text
未対応群への theorem-specific Narrative 拡張
Web workflow の次の実利用 pressure
operation query の残存 concrete pressure
stem 8 以降の coverage
```

事前に優先順位を固定せず、現行 workflow の監査結果から選ぶ。

---

# 6. 残存数学 pressure

```text
H(nu_5)
→ DEFER
→ element-level H proof support の再監査が必要

Delta(nu_prime)
→ DEFER
→ element-level Delta proof support の再監査が必要

H(sigma_11)
→ DEFER
→ sigma_11 Hopf transport / proof support の再監査が必要

Delta(sigma_11)
→ DEFER
→ concrete Delta proof / EHP window support の再監査が必要
```

---

# 7. proof presentation の今後の候補

Phase 132–134 で以下は実装済み。

```text
Trace
Outline
Narrative
shared-dependency Narrative dedup
shared-dependency natural reuse wording
human-readable aggregate statement labels
natural theorem-specific Narrative blocks
fact-role / block-role classification
Narrative document shell
REFERENCE block assembler
display-math / boundary / conclusion presentation primitives
CLI mode selection
Web mode selection
KaTeX rendering
```

今後の改善候補:

```text
未対応 theorem-specific Narrative の追加
より広い representative group の Narrative audit
Phase 番号付き generic helper の rename-only cleanup
rich graph visualization
```

ただし実利用 pressure が確認されるまで実装しない。

---

# 8. 先取りしないもの

```text
general E evaluator
general H evaluator
general Delta evaluator
general membership evaluator
arbitrary recursive containment → operation result
general target-zero evaluator
general operation-query grammar
general symbolic AST substitution
arbitrary theorem mining from proof scope
new theorem ranking
automatic best-target selection
general premise-component dependency engine
unbounded proof search
free-form provenance-free proof generation
generic multi-generator theorem synthesis
generic direct-sum theorem synthesis
```

---

# 9. test / backup 運用

Phase 完了時:

```powershell
python -m pytest tests -q
```

backup は repository 外へ保存する。

repo 内 backup に copied `test_*.py` を置かない。

最新 full regression:

```text
9517 passed in 575.31s (0:09:35)
```

---

# 10. 長期保留

```text
semantic theorem ranking
semantic executable-target ranking
automatic best-target selection
general premise-component dependency engine
general operation-query grammar
general E/H/Delta evaluator
general membership evaluator
general target-zero evaluator
general Toda bracket solver
coset / indeterminacy computation
proof-cost optimization
producer ranking
unbounded backtracking
persistent cache / parallelization
repository snapshot / versioning
rich graph proof visualization
odd-primary integration
all-primary ordinary sphere-homotopy calculation
authentication
database persistence
deployment automation
rich SPA architecture
```

---

# 11. 完了判断原則

```text
既存数学を先に再利用する
direct fact を上書きしない
新しい theorem root を不要に作らない
provenance を失わない
一般 evaluator を必要性なしに作らない
parser を需要なしに一般化しない
generic specialization より concrete proof を優先する
focused regression で境界を固定する
CLI / Web manual integration で表示境界を確認する
repository-wide regression で Phase を閉じる
```

# Phase 143 完了後のロードマップ

## 現在地

Phase 143 完了。

確定した基盤:

```text
group result
→ existing ProofStep provenance
→ presentation graph
→ argument / block structure
→ semantic statement rendering
→ Narrative
```

Phase 143 completion audit:

```text
scanned groups: 128
scanned presentation nodes: 1663
rule-name fallback occurrences: 0
distinct fallback rule names: 0
render errors: 0
```

final regression:

```text
9980 passed in 807.31s (0:13:27)
```

## Phase 144

次 Phase は、Phase 143 で semantic rendering を整備した Narrative を**証明全体として読む監査**から開始する。

優先事項:

1. $\pi_6^3$ で得た自然な証明文と、一般 semantic rules から生成される他群の Narrative を比較する。
2. statement 単体が数式化されていても、証明全体の順序・接続語・依存関係が数学書として不自然でないか確認する。
3. 専用 prose を増やす前に、block role、argument transition、direct premise、dependency reuse など既存の一般構造で改善できるか確認する。
4. Phase 143 で達成した rule-name fallback 0 を維持する。
5. 新しい数学的 theorem fact や proof-search capability が本当に必要になるまでは追加しない。

Phase 144 の開始時点では、実装を先取りしない。まず代表群を横断監査し、共通の presentation pressure が確認できた場合だけ最小変更を行う。

## その後の候補

Phase 144 以降、実際の利用圧が確認できたものから順に検討する。

```text
Narrative の theorem / lemma 参照から既存証明への navigation
Web 上の参照クリックによる proof replay
より広い群での自然な Narrative 品質監査
7-stem 全体の proof-backed coverage 監査
必要に応じた proof presentation graph の可視化
```

これらは Phase 143 の完了条件には含めない。

特に theorem / lemma reference の clickable navigation は有用な将来候補だが、

```text
reference navigation
!= proof inference
!= theorem ranking
!= new proof search
```

として presentation / navigation 層に限定して設計する。

## 維持する境界

```text
free part + 2-primary focus
odd-primary full integration は deferred
general E/H/Delta evaluator は未実装
general Toda bracket solver は未実装
unbounded proof search は未実装
theorem ranking は未実装
free-form LLM proof generation は採用しない
```
