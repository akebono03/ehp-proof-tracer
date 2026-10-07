

<!-- PHASE159_STABLE_TRANSPORT_DESIGN -->
# Phase 159 完了時の stable / unstable 設計境界

Phase 159 では $k=1$ の低次群を用いて public proof の構造を監査し、stable transport（安定移送）を全 stem に一般化するための設計境界を確定した。全 stem への実装拡張は Phase 159 では行わない。

## stable range の判定

対象を

$$
\pi_{n+k}^{n}
$$

とする。Toda (4.5) / Freudenthal suspension theorem による安定移送を使用する境界は

$$
n\ge k+2
$$

とする。したがって routing（経路選択）の設計は

```text
n < k + 2
→ unstable proof を既存 proof provenance から詳細に構成する

n >= k + 2
→ generic stable transport を使用する
```

である。

## canonical stable base

各 stem $k$ について stable range の入口を

$$
n_0=k+2
$$

とし、canonical stable base（標準安定基点）を

$$
\pi_{2k+2}^{k+2}
$$

とする。target $\pi_{n+k}^{n}$ が stable range にあるとき、

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}
$$

によって群構造を移送する。

## generic layer と family-specific layer

将来の generic stable transport は次の責務へ分離する。

```text
is_in_toda_stable_range(target)
canonical_stable_base(target)
build_toda_45_stable_transport_step(base, target)
resolve_stable_generator_transport(base_generator, target)
```

前3項の stable-range 判定、canonical base 選択、群構造の suspension transport は stem に依存しない generic rule とする。最後の generator transport / normalization は family-specific rule とする。

例えば $k=1$ では

$$
E^{n-3}\eta_3=\eta_n
$$

という $\eta$-family の正規化を行う。$\nu$-family、$\sigma$-family などは、それぞれ既存 literature fact と generator convention に基づく別の normalization を持ち得る。

したがって

```text
group-structure stable transport
→ generic

generator naming / normalization
→ family-specific
```

を設計原則とする。

## Reference と specialization の境界

Toda (4.5) の Reference は general form（一般形）のまま表示する。target 固有の変数代入は proof body で行う。

```text
Reference
→ literature statement の general form

proof body
→ target への specialization
```

Reference を target 固有の文へ書き換えて literature statement 自体を変形したように見せてはならない。

## semantic identity

proof fact の同一性・依存関係・重複抑制は rendered prose の文字列一致で決めない。既存 statement identity、semantic key、ProofStep provenance など意味構造に基づいて扱う。文章の normalization は presentation layer に限定する。

## Phase 159 と次 Phase の境界

Phase 159 では $k=1$ の実装を prototype として監査し、$\pi_3^2$ と $\pi_4^3$ の public proof を完成点とする。

次 Phase では、まず現行 $k=1$ 実装のうち generic layer に持ち上げられる部分を inventory し、その後に最小限の generic stable transport を実装する。Phase 159 の段階では他 stem の production route を先取りして変更しない。
