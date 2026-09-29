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

## Phase 147 — RC1: Argument-method ownership

目的:

historical proof-purpose と current argument-method ownership の差を、target-specific special
case ではなく一般規則で解消する。

主対象:

```text
order argument と主要 exactness method の ownership
argument purpose と method introduction の対応
```

Phase 147 では RC2 以降を先取りしない。

完了条件:

```text
RC1 の concrete blocker が一般 ownership rule で解消
+
existing proof preservation
+
focused regression
```

---

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
