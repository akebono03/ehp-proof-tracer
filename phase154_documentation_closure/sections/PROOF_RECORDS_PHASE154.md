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
