# Phase 159 documentation closure

## Phase 159 完了

Phase 159 は、public Narrative の統一後に、低次群から数学的 proof coverage を実際に確認し、不足する一般規則だけを補う Phase として完了する。

主要な到達点は次の通り。

- $\pi_3^2=\mathbb Z\{\eta_2\}$ の public proof を完成した。
- $\pi_4^3=\mathbb Z/2\{\eta_3\}$ の public proof を完成した。
- Reference は特殊化済みの文言ではなく、可能な限り literature statement の一般形を表示し、本文で target へ specialization（特殊化）する境界を確認した。
- equation numbering（式番号）と proof-item numbering（証明項目番号）を区別し、後続で実際に参照される式だけに番号を付ける Phase 158 の契約を維持した。
- public Narrative の順序は文字列比較ではなく semantic identity / proof dependency（意味的同一性・証明依存関係）に基づいて扱う方針を維持した。
- $k=1$ の stable case では Freudenthal suspension による transport を利用できることを確認し、現在の専用処理を generic stable transport の prototype と位置付けた。

## Phase 159 と次 Phase の境界

Phase 159 では全 stem の stable transport を実装しない。

次 Phase では、target $\pi_{n+k}^{n}$ に対し

$$
n\ge k+2
$$

を stable-range condition（安定範囲条件）とし、canonical stable base（標準安定基点）

$$
\pi_{2k+2}^{k+2}
$$

から

$$
E^{n-k-2}:\pi_{2k+2}^{k+2}\overset{\cong}{\longrightarrow}\pi_{n+k}^{n}
$$

で群構造を移送する generic design を扱う。

設計上は次の4責務に分離する。

1. `is_in_toda_stable_range(target)` — $n\ge k+2$ の意味的判定。
2. `canonical_stable_base(target)` — $(n_0,k)=(k+2,k)$ の選択。
3. `build_toda_45_stable_transport_step(base, target)` — Toda (4.5) による同型移送。
4. `resolve_stable_generator_transport(base_generator, target)` — $\eta,\nu,\sigma,\ldots$ の family-specific generator normalization。

群構造の stable transport は generic とし、generator の標準名への正規化だけを family-specific とする。

したがって以後の proof audit は原則として

$$
n<k+2
\quad\Longrightarrow\quad
\text{unstable proof を詳細監査},
$$

$$
n\ge k+2
\quad\Longrightarrow\quad
\text{generic stable transport を利用}
$$

という境界で整理する。
