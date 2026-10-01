## Phase 154 — Proof prose generation refinement

Phase 154 の implementation / closure audit は完了し、documentation closure まで到達した。

対象:

```text
internal fallback leakage
English statement prose
transition repetition
semantic duplication
Reference-to-proof-body linkage
sentence composition
punctuation normalization
```

一般規則による改善結果:

```text
Phase 154 focused regression:
44 passed

ordering / reason regression boundary:
57 passed

112-group public Narrative closure:
scanned groups: 112
rendered groups: 112
exceptions: 0
violations: 0
```

category 別:

```text
transition_repetition: 0
semantic_duplication: 0
internal_fallback_leakage: 0
english_prose: 0
reference_linkage: 0
ordering: 0
punctuation: 0
```

punctuation policy:

```text
prose comma  = ", "
prose period = "."
```

112群すべてで ASCII comma prose / ASCII period prose を確認した。

Phase 154 は $\pi_6^3$ 専用 prose hardcoding ではなく shared source / graph-backed rule を優先した。

documentation closure 時点では repository-wide final full regression はまだ実行していない。

```text
Phase 154 implementation closure
→ documentation closure
→ final full regression
→ Phase 154 formal completion
```

### Phase 155 — Reference statement relevance / minimal display

Phase 155 では Reference selection 自体を作り直さず、Reference section に表示する
statement の必要性と粒度を監査する。

主な問い:

```text
Reference title は必要
↓
statement lines は proof body が実際に必要とするものだけか

group-result statement は本当に本文の論証で使われているか
aggregate statement の余分な component が表示されていないか
同じ Reference 内で statement を過剰表示していないか
```

方針:

```text
Proof graph / consumer usage
→ necessary Reference statement set
→ minimal display
```

群別 special case や theorem fact の削除ではなく、presentation relevance（表示上の必要性）の
一般規則として扱う。

先取りしないもの:

```text
Reference selection の全面再設計
new theorem facts
proof search
theorem ranking
automatic best proof selection
dedicated renderer retirement
```

Phase 155 の正式な implementation scope は開始時の all-group audit で確定する。
