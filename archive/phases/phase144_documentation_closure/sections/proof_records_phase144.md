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
