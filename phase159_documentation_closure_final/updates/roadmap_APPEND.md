

<!-- PHASE159_DOCUMENTATION_CLOSURE -->
# Phase 159 完了後の roadmap

Phase 159 は $k=1$ の低次 public proof、特に $\pi_3^2$ と $\pi_4^3$ の監査を完了し、stable / unstable routing の設計境界を確定した。

次 Phase の主対象は generic stable transport（一般安定移送）である。

## 次 Phase の開始条件

まず GitHub 現行コードと関連テストを再確認し、現在の $k=1$ stable implementation を inventory する。Phase 159 で確定した設計を基準に、次の責務を既存コードのどこから抽出できるかを確認する。

```text
is_in_toda_stable_range(target)
canonical_stable_base(target)
build_toda_45_stable_transport_step(base, target)
resolve_stable_generator_transport(base_generator, target)
```

## 実装順序

最初に stable range

$$
n\ge k+2
$$

と canonical base

$$
\pi_{2k+2}^{k+2}
$$

を semantic rule として扱う。次に Toda (4.5) の general-form Reference と target specialization を分離したまま、群構造の transport を generic 化する。

generator normalization は同じ generic rule に押し込まず、family-specific layer として接続する。

## 継続する境界

unstable range

$$
n<k+2
$$

では、引き続き既存 literature fact、EHP sequence、proof provenance を使った詳細 proof を優先する。stable transport の導入を理由に unstable proof を省略しない。

次 Phase でも、対象 Phase に必要な最小変更だけを行い、未監査の stem や generator family を一度に先取り実装しない。
