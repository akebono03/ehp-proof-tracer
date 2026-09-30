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

# Phase 144 完了後のロードマップ

## 現在地

Phase 144 完了。

確定した基盤:

```text
group result
→ existing ProofStep provenance
→ replay / complete replay
→ presentation graph
→ semantic sidecar
→ argument / block structure
→ proof chains / contributions
→ contribution-aware generic Narrative
```

Phase 144-6 R25-30-R3 で ownership / argument-boundary classification を current gate として
確定した。

current six-group boundary:

```text
selected=192
participating=35
detached=157
detached_insertable=3
missing=0
```

`detached_insertable=3` は boundary leak として修正対象にしない。

また、$\pi_{15}^8$ / $\pi_{16}^9$ などで確認した巨大な proof-subtree 再展開は
result-reuse problem として分離済みであり、Phase 144 の未完了事項とはしない。

Phase 144 closure evidence:

```text
canonical repository-wide:
10298 collected
10273 passed
25 failed
2321.20s (0:38:41)

historical R5-39..43 snapshot maintenance:
66 passed in 1308.82s (0:21:48)
```

25 failures は historical fixed-count / completion snapshots に限定され、production renderer
を変更せず structural invariant へ maintenance した。maintenance 後の whole suite は
再実行していないため、未観測の全PASS件数は記録しない。

## Phase 145 — 完了

Phase 145 の目的は次の default presentation change に限定した。

```text
group-proof default mode
trace → narrative

group-proof default depth
→ 2
```

CLI / Web の default を Narrative + depth 2 に変更し、explicit user selection の
Trace / Outline / Narrative および depth 0 / 1 / 2 は維持した。

Phase 145 では次を実装していない。

```text
result-reuse の一般化
ownership model の追加変更
新しい semantic statement type の先回り実装
新しい theorem fact
新しい proof search
general E/H/Delta evaluator
```

repository cleanup 後に canonical test import dependency を修復し、mixed import style
に対する test-only compatibility layer を追加した。

最終 repository-wide regression:

```text
10303 passed in 2375.31s (0:39:35)
```

Phase 145 完了。

## Phase 146 — 完了: historical Narrative difference audit

Phase 146 は $\pi_6^3$ の current generic Narrative と historical Phase 136-2 Narrative を
比較し、一般化不足を root cause 単位に分類した。

Phase 146-7 では generic argument-purpose prose fusion を実装した。

Phase 146-8 / 146-9 は audit only。

Phase 146-9 の最終分類:

```text
12 visible difference families
→ 6 root causes
```

```text
RC1 Argument-method ownership
RC2 Recursive exactness evidence exposure
RC3 Contribution ownership / insertion ordering
RC4 Generic provenance / reason prose
RC5 EHP semantic naming
RC6 Final equation numbering / prose formatting
```

dependency order:

```text
RC1 → RC2 → RC3 → RC4 → RC5 → RC6
```

Phase 146 完了時点では $\pi_6^3$ public route gate を削除しない。

---

## Phase 147 — 完了: RC1 Argument-method ownership

Phase 147 は historical proof-purpose と current argument-method ownership の差を、
target-specific special case ではなく一般 ownership API で整理した。

完了内容:

```text
RC1-1 ownership boundary audit
RC1-2 minimal ownership API design
RC1-3 minimal ownership API implementation
RC1-4 ownership integration audit
RC1-5 final regression
```

確定した経路:

```text
Narrative Argument
→ existing method evidence
→ exactness method components
→ argument-owned primary exactness method
→ renderer
```

multi renderer は primary-method selection に ownership API を使用する。

旧 inline primary selector は multi renderer から除去した。

body / evidence handling 用の method evidence extraction は維持し、RC2 を先取りしていない。

$\pi_6^3$ では、

```text
establish_order
→ primary exactness method

establish_group_structure
→ a different primary exactness method
```

を確認した。

final regression:

```text
10314 passed in 2942.66s (0:49:02)
```

Phase 147 完了。

---

## 現在地: Phase 148 — RC2 Recursive exactness evidence exposure

## Phase 148 — RC2: Recursive exactness evidence exposure

目的:

primary method に吸収されない recursive exactness evidence のうち、main Narrative に
必要なものと補助 provenance を一般規則で区別する。

主対象:

```text
主要 exact-sequence window selection
auxiliary exactness suppression
exactness contribution duplication の RC2 部分
```

RC3 の contribution insertion ordering は扱わない。

---

## Phase 149 — RC3: Contribution ownership / insertion ordering

目的:

argument dependency narration と post-render contribution placement のずれを一般規則で解消する。

主対象:

```text
contribution duplication の RC3 部分
dependency order に沿った式配置
map-property chain placement
short exact sequence → group structure ordering
```

---

## Phase 150 — RC4: Generic provenance / reason prose

目的:

stored provenance から Reference と derived fact の関係を一般的に文章化する。

主対象:

```text
Reference section detail
[R#] → derived fact reason prose
definition reasoning prose
```

historical $\pi_6^3$ 専用の `[R#]` 文面は埋め込まない。

---

## Phase 151 — RC5: EHP semantic naming

目的:

exactness method の stored semantics から、適切な場合に

```text
EHP 完全列
```

という method family name を一般的に表示する。

単なる文字列置換ではなく semantic classification に基づく。

---

## Phase 152 — RC6: Final equation numbering / prose formatting

目的:

RC1〜RC5 後の final selected / ordered Narrative stream に基づき、equation numbering と
prose formatting を確定する。

RC6 を最後にする理由:

```text
equation numbering
→ selection / ordering の下流
```

したがって RC1〜RC5 より先に historical tag を固定しない。

---

## Phase 147〜152 共通原則

```text
1 Phase = 1 root cause
minimum general rule
target-specific special handling を作らない
future Phase の機能を先取りしない
focused regression で既存 proof を守る
whole suite は各 Phase の最後だけ
```

各 Phase の完了条件:

> 対象 root cause を concrete proof pressure に基づく最小一般規則で解決し、
> 既存 proof semantics と provenance を壊さない。

---

## 将来候補

RC1〜RC6 と独立した具体的利用圧が出た時点で個別 Phase として検討する。

```text
Narrative reference から既存証明への navigation
Web reference click → proof replay
7-stem 全体の proof-backed Narrative audit
result-reuse / already-established-result reuse
rich proof graph visualization
stem 8 以降の coverage
```

候補の並びは実装順を固定しない。

## 維持する数学的境界

```text
free part + 2-primary focus
odd-primary full integration は deferred
general E/H/Delta evaluator は未実装
general Toda bracket solver は未実装
unbounded proof search は未実装
theorem ranking は未実装
```

---

# Phase 148 完了後ロードマップ

## Phase 148 — 完了

RC2 `Recursive exactness evidence exposure` を完了した。

```text
RC1 Argument-method ownership
→ Phase 147 完了

RC2 Recursive exactness evidence exposure
→ Phase 148 完了
```

Phase 148 では proof provenance を削除せず、Narrative 本文への exactness evidence の
表示範囲だけを一般規則で制御した。

## Phase 149 — RC3 Narrative ordering

次 Phase は contribution ownership / insertion ordering
（寄与の所有と挿入順序）を扱う。

主要 pressure は、数学的説明の順序として

```text
method / short exact sequence
→ derivation
→ final group conclusion
```

と読むべき箇所で、final conclusion が method contribution より先に現れる場合があること。

Phase 149 では次を守る。

```text
RC2 exposure classification
→ 変更しない

proof graph
→ 変更しない

theorem facts
→ 追加しない

depth semantics
→ 変更しない

ordering / placement
→ 必要最小限の一般規則だけを追加
```

$\pi_6^3$ の historical prose を直接 special case として復元するのではなく、
Argument、transition、contribution ownership から導ける ordering rule を監査する。

## その後

Phase 146 の root-cause 順序を維持する。

```text
RC3 → RC4 → RC5 → RC6
```

- RC3: Contribution ownership / insertion ordering
- RC4: Generic provenance / reason prose
- RC5: EHP semantic naming
- RC6: Final equation numbering / prose formatting

下流の formatting を先に固定せず、selection / ownership / ordering の意味構造を先に確定する。

---

<!-- PHASE149_RC3_CLOSURE -->
# Phase 149 完了 — RC3 Narrative contribution ordering

Phase 149 / RC3 は完了。

目的:

```text
RC2 で表示対象になった evidence を
owner Argument の論証順に配置する
```

達成した一般規則:

```text
method
→ evidence
→ derivation
→ conclusion
```

代表6群の cross-group audit:

```text
pi_6^3:  ordering_ok=True
pi_8^5:  ordering_ok=True
pi_10^4: ordering_ok=True
pi_12^5: ordering_ok=True
pi_15^8: ordering_ok=True
pi_16^9: ordering_ok=True
AUDIT_RESULT=PASS
```

focused regression:

```text
57 passed in 10.85s
```

repository-wide final:

```text
﻿10416 passed in 1315.93s (0:21:55)
```

## 次の順序

Phase 146 で整理した残課題は引き続き次の依存順で扱う。

```text
Phase 150 / RC4
Generic provenance / reason prose

Phase 151 / RC5
EHP semantic naming

Phase 152 / RC6
Final equation numbering / prose formatting
```

Phase 150 では RC3 の ordering を再設計しない。表示された fact に対して、一般的な provenance / reason prose をどのように付与するかを対象とする。

$\pi_6^3$ の order Argument 内にある derived calculation

$$
2\nu'=\eta_3^3
$$

の局所的な表示順改善候補は記録するが、Phase 150 の RC4 を先取りして Phase 149 に追加実装しない。
