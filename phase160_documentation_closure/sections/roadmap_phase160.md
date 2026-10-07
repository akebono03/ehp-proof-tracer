<!-- PHASE160_DOCUMENTATION_CLOSURE -->
# Phase 160 完了後の roadmap

Phase 160 で Phase 159 の stable-transport design を production path へ実装した。

stable range

$$
n\ge k+2
$$

では、stem 1–7 について canonical stable base

$$
\pi_{2k+2}^{k+2}
$$

から Toda (4.5)

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}
$$

を使う共通経路が利用できる。

## 完了した stable infrastructure

```text
stable target / stem semantics
canonical stable base selection
canonical Toda (4.5) specialization
generic finite-cyclic transport
generic zero-group transport
eta-family normalization connection
nu-family normalization connection
nu-squared normalization
sigma-family normalization
stem 1–7 public stable Narrative
Group query Result / Conclusion canonical generator notation
```

stable stems:

```text
1: Z/2{eta_n}
2: Z/2{eta_n^2}
3: Z/8{nu_n}
4: 0
5: 0
6: Z/2{nu_n^2}
7: Z/16{sigma_n}
```

## Phase 161 — unstable proof audit の再開

次 Phase は stable layer の追加一般化を目的としない。

このプログラムの主対象である unstable homotopy groups（非安定ホモトピー群）へ戻る。

Phase 159 では stem 1 の低次境界

$$
\pi_3^2,
\qquad
\pi_4^3
$$

を確認した。

Phase 161 では残る unstable target

$$
n<k+2
$$

を低い $(k,n)$ から順に実際の public proof で監査する。

自然な開始候補は stem 2 の unstable range:

$$
\pi_4^2,
\qquad
\pi_5^3
$$

である。

進行原則:

```text
existing proof を生成
→ public Narrative を数学的に読む
→ missing proof step を特定
→ 必要最小限の一般規則を追加
→ focused verification
→ 次の unstable target
```

stable target は Phase 160 の common transport を再利用し、同じ stable 証明を stem ごとに再実装しない。

## Phase 161 で先取りしないもの

```text
generic DirectSumGroup stable transport
generic FreeCyclicGroup stable transport
new stable theorem database
arbitrary generator normalization
unbounded theorem search
proof provenance と無関係な文章による補完
未遭遇の unstable defect の先回り修正
```

## test boundary

利用者方針により、Phase 160 documentation closure では full pytest を実行しない。

Phase 161 も各 repair では focused verification を基本とし、全体テストは Phase の最後に利用者が実行を選択した場合のみ行う。

## 最新の直近順序

```text
Phase 160 documentation closure
→ Phase 161: unstable proof audit を再開
→ stem 2 の低次 unstable target から確認
→ 実際に不足する一般規則だけを追加
→ stable range に入ったら Phase 160 transport を再利用
```
