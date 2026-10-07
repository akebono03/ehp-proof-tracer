<!-- PHASE160_DOCUMENTATION_CLOSURE -->
# Phase 160 Generic stable transport 実装記録

日付: 2026-10-08

Phase 160 は、Phase 159 で確定した stable / unstable boundary を production architecture へ実装した。

対象は、stable range

$$
n\ge k+2
$$

にある

$$
\pi_{n+k}^{n}
$$

を、canonical stable base

$$
\pi_{2k+2}^{k+2}
$$

から Toda (4.5) の suspension isomorphism で移送する共通経路である。

## R1 — current stable implementation audit

現行の stable family 実装を確認し、stem ごとに theorem-specific transport が混在していることを棚卸しした。

設計原則:

```text
group-structure transport
→ generic

generator naming / normalization
→ family-specific
```

を Phase 160 の境界として採用した。

## R2 — generic stable target semantics

`stable_rules.py` に stable target の共通意味論を追加した。

主要 helper:

```text
toda_primary_group_stem
is_in_toda_stable_range
canonical_toda_stable_base
toda_stable_transport_exponent
```

対象 $\pi_{n+k}^n$ について

$$
n_0=k+2,
\qquad
E^{n-k-2}
$$

を一意に決める。

focused verification:

```text
38 passed
```

## R3 — canonical Toda (4.5) specialization

canonical base から concrete target への suspension map と Toda (4.5) isomorphism step を構成する helper を追加した。

```text
build_canonical_toda_stable_transport_map
build_canonical_toda_45_isomorphism_step
```

Toda (4.5) の structural scalar expression を保持し、Reference の一般形と target-specific specialization を分離した。

focused verification:

```text
55 passed
```

## R4 — generic finite-cyclic group transport

`FiniteCyclicGroup` 用の generic stable transport rule を追加した。

出力は

```text
same order
+
IteratedSuspension(source_generator, exponent)
```

であり、family-specific generator name へは正規化しない。

focused verification:

```text
72 passed
```

## R5 — 1-stem production connection

$k=1$ の production path を generic finite-cyclic transport へ接続した。

既存 eta-family normalization は downstream の別 layer として維持した。

focused verification:

```text
54 passed
```

## R6 — 7-stem sigma transport / normalization separation

$\sigma$ family の stable path を

```text
generic finite-cyclic transport
→ E^(n-9) sigma_9
→ sigma-family normalization
→ sigma_n
```

へ分離した。

専用の transport + normalization 一体 rule は production path から外し、互換用コードとして残した。

focused verification:

```text
31 passed
```

## R7 — public stable Narrative

generic stable finite-cyclic transport を public Narrative へ接続した。

初期 repair で renderer alias の NameError を修正し、stem 1 と stem 7 の common stable Narrative を確認した。

focused verification:

```text
18 passed
```

## R8 — 2-stem production connection

canonical base

$$
\pi_6^4=\mathbb Z/2\{\eta_4^2\}
$$

からの 2-stem production transport を generic finite-cyclic rule へ接続した。

fixture repair では $\eta_{n+1}$ の symbolic construction を current production semantics に合わせた。

focused verification:

```text
37 passed
```

## R9 — 2-stem public Narrative

2-stem の public Narrative を stable common wrapper へ接続した。

public notation は expanded composition

$$
\eta_n\eta_{n+1}
$$

ではなく

$$
\eta_n^2
$$

を使用する。

focused verification:

```text
19 passed
```

## R10 — remaining stable stems integration

残る 3–6 stem を一括接続した。

### 3-stem

$$
\pi_8^5=\mathbb Z/8\{\nu_5\}
$$

から generic finite-cyclic transport を使用し、既存 $\nu$-family bridge で $\nu_n$ へ正規化した。

### 4-stem

$$
\pi_{10}^6=0
$$

から generic zero-group transport を使用した。

### 5-stem

$$
\pi_{12}^7=0
$$

から 4-stem と同じ generic zero-group transport を使用した。

### 6-stem

$$
\pi_{14}^8=\mathbb Z/2\{\nu_8^2\}
$$

について

```text
generic finite-cyclic transport
→ E^(n-8)(nu_8^2)
→ nu-squared normalization
→ nu_n^2
```

へ分離した。

最初の R10 apply は `toda_prop511_zero_bootstrap.py` の import anchor が2件一致したため安全に停止した。

repair1 では unique top-level import block を anchor にし、6-stem aggregate が利用する `run_inference_until_stable_with_history` import も補った。

最終 focused verification:

```text
117 passed in 23.92s
```

repository-wide full pytest は実行していない。

## R11 — Group query / Conclusion generator canonicalization

Web 目視確認で、Narrative は canonical notation を使っている一方、Group query Result と Group proof Conclusion が expanded composition を表示している差を発見した。

修正対象:

```text
eta_n eta_(n+1)
→ eta_n^2

nu_n nu_(n+3)
→ nu_n^2
```

raw expression renderer は変更せず、public group generator renderer を追加して Result / Conclusion に共通利用した。

内部 semantics は `Composition` のまま保持する。

R11 は利用者指示によりテストを実行していない。

Web 目視確認では

$$
\pi_{15}^{13}\cong\mathbb Z/2\{\eta_{13}^2\}
$$

と

$$
\pi_{19}^{13}\cong\mathbb Z/2\{\nu_{13}^2\}
$$

について Result / Conclusion / Narrative の表記一致を確認した。

## Phase 160 completion boundary

Phase 160 で stable stem 1–7 は

```text
canonical stable base
→ Toda (4.5)
→ generic group transport
→ family normalization（必要な場合）
→ public canonical notation
```

という共通構造へ整理された。

canonical bases:

```text
stem 1: pi_4^3
stem 2: pi_6^4
stem 3: pi_8^5
stem 4: pi_10^6
stem 5: pi_12^7
stem 6: pi_14^8
stem 7: pi_16^9
```

Phase 160 では direct-sum stable transport、free-cyclic stable transport、任意 family normalization は追加していない。

利用者指定により Phase 160 closure で repository-wide full pytest は実行しない。

したがって completion evidence は、

```text
R1–R10 の focused audit / verification
R10 repair1: 117 passed
R11 Web manual verification
```

であり、repository-wide all-pass は claim しない。

Phase 160 完了。
