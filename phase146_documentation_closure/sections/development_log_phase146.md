# Phase 146 — historical Narrative difference audit / root-cause classification

Phase 146 は、$\pi_6^3$ の current generic Narrative と historical Phase 136-2 Narrative の
差を監査し、今後の一般化課題を concrete root cause 単位へ分解する Phase とした。

## Phase 146-1〜146-5: current generic route audit

current public $\pi_6^3$ route を追跡し、public route 内部が semantic sidecar、blocks、
arguments、generic contribution renderer を使用していることを確認した。

Phase 146-5 では current public output と current generic contribution renderer output が
exact parity であることを確認した。

この結果から、問題を「current public vs current generic」ではなく
「current generic vs historical Phase 136-2 quality」として再定義した。

## Phase 146-6: historical baseline

historical comparison baseline:

```text
Phase 136-2
commit 908e24db89669750949fa9ad149f5e306ac05546
```

historical proof が持っていた主要 semantic contract を比較し、core mathematics は current
にも存在する一方、

```text
$\nu'$ の位数を決定するために, 次の EHP 完全列を考える.
```

という proof-strategy prose が current では失われていることを確認した。

## Phase 146-7: generic argument-purpose prose fusion

変更対象:

```text
toda_group_proof_narrative_argument_renderer.py
render_toda_group_proof_narrative_argument_header_method_section()
```

target-specific 文面を追加せず、argument purpose と primary exactness transition を
一般規則で一文に融合した。

focused:

```text
11 passed
```

existing pi_6^3 public-route regression:

```text
4 passed
```

全体 suite はこの時点では実行していない。

## Phase 146-8: Historical Narrative Full Structural Diff Audit

production changes:

```text
none
```

historical/current structural inventory:

```text
historical units: 17
current units: 82
PRESERVED: 0
LOST: 17
ADDED: 47
DUPLICATED: 35

sequence-related:
historical 4
current 44

[R#]:
historical 8
current 1
```

unit granularity が異なるため raw PRESERVED / LOST 件数を semantic loss 件数とは解釈しない。

一方、次の pressure は実在することを確認した。

```text
Reference richness / reason prose
definition reasoning
order-method ownership
EHP naming
exact-sequence window selection
auxiliary exactness leakage
contribution duplication
dependency ordering
map-property chain placement
short exact sequence placement
equation numbering / formatting
```

## Phase 146-9: Historical Difference Root-Cause Classification

production changes:

```text
none
```

audit harness の初版〜R2 では current production API signature 追従不足があり、
R3 で current `develop` の実呼び出し経路に合わせた。

R3 successful diagnostics:

```text
arg 0 establish_group_structure:
method_evidence=3 components=1 primary=True primary_windows=3 contributions=2

arg 1 establish_order:
method_evidence=2 components=1 primary=True primary_windows=2 contributions=2

arg 2 establish_definition:
method_evidence=0 components=0 primary=False primary_windows=0 contributions=0
```

ここで、order argument に primary component が存在することを確認した。
したがって Phase 146-7 後の不足を「order primary が無い」と説明するのは誤りである。

12 visible difference families を6 root causes に集約した。

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

Phase 146-9 report は UTF-8 strict decode PASS。

## Phase 146 完了境界

Phase 146 の production change は Phase 146-7 の generic prose fusion のみ。

Phase 146-8 / 146-9 は audit only。

未変更:

```text
pi_6^3 public route gate
exactness ownership
contribution selection
provenance rendering
EHP naming
equation numbering
proof graph
theorem facts
proof search
```

Phase 146 では route gate を削除しない。

Phase 147 以降は6 root causes を依存順に1件ずつ扱う。
