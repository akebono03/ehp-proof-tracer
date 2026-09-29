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

## Phase 145 — default presentation change only

Phase 145 の目的は1つだけ。

```text
group-proof default mode
trace → narrative

group-proof default depth
現行 default → 2
```

CLI / Web の実際の default 経路を監査し、必要最小限の変更で Narrative + depth 2 を
default にする。

Phase 145 では次を行わない。

```text
result-reuse の一般化
ownership model の追加変更
新しい semantic statement type の先回り実装
全 rule-name / statement type の網羅的再監査
新しい theorem fact
新しい proof search
```

完了条件:

```text
default group-proof presentation が Narrative
default depth が 2
explicit user selection は既存 semantics を維持
既存 API / proof provenance を壊さない
focused regression が通る
Phase-final repository-wide regression を実行
```

## Phase 146 以降 — 1 Phase = 1 concrete issue

Phase 146 以降は「一般化を先に完成させる」方式を採用しない。

基本手順:

```text
1. 次に通したい具体的な証明を1つ選ぶ
2. generic Narrative で不足している具体的課題を1つ特定する
3. その課題だけを解く最小一般規則を設計する
4. target-specific special case を作らず実装する
5. focused regression で既存証明を守る
6. その Phase を閉じる
```

各 Phase の完了条件:

> 対象となる1課題を target-specific special handling ではなく一般規則で解決し、
> 既存の証明を壊さない。

例:

```text
ある具体的 proof で Reference reuse だけが不足
→ その Phase は Reference reuse だけ

次の proof で composition expression が不足
→ 次 Phase は composition expression だけ

result-reuse が初めて具体的 blocker になる
→ その Phase で result-reuse の最小一般規則だけ
```

したがって、巨大な「すべての一般規則を完成させる Phase」は作らない。

## 先取りしないもの

```text
全 statement type の事前 renderer 化
全 rule-name fallback の需要なし一括除去
将来 proof のためだけの result-reuse framework
general E evaluator
general H evaluator
general Delta evaluator
general membership evaluator
general Toda bracket solver
unbounded proof search
theorem ranking
automatic best-target selection
free-form provenance-free LLM proof generation
```

## 将来候補

具体的利用圧が出た時点で個別 Phase として検討する。

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
