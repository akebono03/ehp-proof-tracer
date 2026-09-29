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
