

<!-- PHASE159_DOCUMENTATION_CLOSURE -->
# Phase 159 stem-1 proof record

Phase 159 の数学的 proof coverage は $k=1$ から開始した。

## $\pi_3^2$

対象は

$$
\pi_3^2=\mathbb Z\{\eta_2\}.
$$

public proof の監査では、既存 proof provenance に従った依存順序、definition premise の配置、map-property の提示、Reference の一般形、式番号と proof-item 番号の区別を確認した。

Reference の literature statement は general form のまま保持し、$\pi_3^2$ 固有の代入・特殊化は proof body に置く。

## $\pi_4^3$

対象は

$$
\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

この群は $k=1$ に対して stable range の入口

$$
n=k+2=3
$$

に位置する。Phase 159 では $k=1$ の stable suspension proof を監査し、Toda (4.5) の一般形を Reference として用い、proof body で target へ特殊化する境界を確認した。

## generic stable transport への記録

一般の target

$$
\pi_{n+k}^{n}
$$

について stable range を

$$
n\ge k+2
$$

とする。canonical stable base は

$$
\pi_{2k+2}^{k+2}
$$

であり、stable target への群構造の移送は

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}
$$

で表す。

この記録は次 Phase の設計入力であり、Phase 159 において全 stem の transport proof が production 実装済みであることを意味しない。

## provenance boundary

```text
general literature Reference
!= target-specific specialization

semantic identity
!= rendered prose equality

generic group transport
!= family-specific generator normalization

Phase 159 design closure
!= all-stem stable implementation
```

Phase 159 documentation closure では repository-wide full pytest を実行していないため、新しい全体回帰 PASS は記録しない。
