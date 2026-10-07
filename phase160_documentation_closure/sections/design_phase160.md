<!-- PHASE160_DOCUMENTATION_CLOSURE -->
# Phase 160 — generic stable transport の現行設計

Phase 159 で設計した stable transport（安定移送）を Phase 160 で production path へ実装した。ここから先は本節を stable transport の現行設計とする。

## stable target semantics

対象を

$$
\pi_{n+k}^{n}
$$

とする。

stable range（安定域）は

$$
n\ge k+2
$$

であり、canonical stable base（標準安定基点）は

$$
n_0=k+2,
\qquad
\pi_{2k+2}^{k+2}
$$

である。

target への transport exponent（移送回数）は

$$
n-n_0=n-k-2
$$

である。

したがって canonical transport は

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}
$$

となる。

この意味論は `stable_rules.py` の target / stem / canonical-base helper と、Toda (4.5) の concrete specialization builder で共有する。

## Toda (4.5) specialization

literature Reference は Toda (4.5) の general form（一般形）を保持する。

```text
Reference
→ n >= k + 2 の一般形

proof body
→ canonical base と concrete target への代入
```

target 固有の式を Reference statement 自体へ書き戻さない。

`build_canonical_toda_stable_transport_map()` と `build_canonical_toda_45_isomorphism_step()` は、canonical base から target への structural suspension map と Toda (4.5) isomorphism step を構成する。

## generic finite-cyclic transport

`FiniteCyclicGroup` の stable transport は family 名に依存しない。

入力:

```text
canonical-base group relation
Toda (4.5) isomorphism
```

出力:

```text
same cyclic order
+
IteratedSuspension(source_generator, exponent)
```

したがって例えば

$$
\pi_8^5=\mathbb Z/8\{\nu_5\}
$$

を transport した直後の generator は、概念的には

$$
E^{n-5}\nu_5
$$

であり、この generic layer 自体はそれを $\nu_n$ と同一視しない。

重要な境界:

```text
cyclic order transport
→ generic

named family generator
→ family-specific normalization
```

## generic zero-group transport

4-stem と 5-stem は `FiniteCyclicGroup(order=1)` として表現しない。

Toda (4.5) isomorphism

$$
E^r:G\overset{\cong}{\longrightarrow}H
$$

と

$$
G=0
$$

から

$$
H=0
$$

を得る generic zero-group transport を用いる。

この規則は `TodaPrimaryGroupZeroStatement` をそのまま扱う。

## family-specific normalization

Phase 160 では group transport と generator naming を分離した。

### eta family

1-stem:

$$
E^{n-3}\eta_3=\eta_n.
$$

2-stem:

$$
E^{n-4}\eta_4^2=\eta_n^2.
$$

内部では $\eta_n^2$ が `Composition` として保持される場合があるが、public group notation は power notation（冪記法）へ canonicalize する。

### nu family

3-stem:

$$
E^{n-5}\nu_5=\nu_n.
$$

6-stem:

$$
E^{n-8}\nu_8^2=\nu_n^2.
$$

6-stem は特に

```text
generic finite-cyclic transport
→ transported generator E^(n-8)(nu_8^2)
→ nu-squared normalization
```

の2段階を明示的に分ける。

### sigma family

7-stem:

$$
E^{n-9}\sigma_9=\sigma_n.
$$

Phase 160-R6 で generic finite-cyclic transport と sigma-family normalization を分離した。

## stem 1–7 の production stable architecture

stable target の canonical base は次のとおり。

| stem | canonical stable base | stable family |
| --- | --- | --- |
| 1 | $\pi_4^3=\mathbb Z/2\{\eta_3\}$ | $\mathbb Z/2\{\eta_n\}$ |
| 2 | $\pi_6^4=\mathbb Z/2\{\eta_4^2\}$ | $\mathbb Z/2\{\eta_n^2\}$ |
| 3 | $\pi_8^5=\mathbb Z/8\{\nu_5\}$ | $\mathbb Z/8\{\nu_n\}$ |
| 4 | $\pi_{10}^6=0$ | $0$ |
| 5 | $\pi_{12}^7=0$ | $0$ |
| 6 | $\pi_{14}^8=\mathbb Z/2\{\nu_8^2\}$ | $\mathbb Z/2\{\nu_n^2\}$ |
| 7 | $\pi_{16}^9=\mathbb Z/16\{\sigma_9\}$ | $\mathbb Z/16\{\sigma_n\}$ |

production path は、既存 theorem-specific transport rule を削除して互換性を壊すのではなく、current production builder が generic rule を使うように接続する。旧専用 rule は compatibility（互換性）のため残してよい。

## public Narrative

stable public Narrative は stem ごとの専用証明本文を作らず、共通 shape を用いる。

```text
## 証明対象

## 使用する結果
[R1] Toda (4.5) general form
[R2] canonical base result

---

## 証明
canonical base
concrete Toda (4.5) specialization
generator transport / normalization（必要な場合）
target group result

□
```

4-stem と 5-stem は generator equation を持たず、zero group の同型移送だけを表示する。

canonical base 自身では stable transport wrapper を起動しない。

## public generator canonicalization

internal expression（内部式）と public notation（公開表記）を区別する。

内部では例えば

$$
\eta_n\eta_{n+1},
\qquad
\nu_n\nu_{n+3}
$$

を `Composition` として保持できる。

public group display では

$$
\eta_n^2,
\qquad
\nu_n^2
$$

を使用する。

この canonicalization は、

```text
Group query Result
Group proof Conclusion
Narrative target / conclusion
```

で整合させる。

一方 `render_toda_expression_latex()` の raw expression rendering は変更しない。証明途中で expanded composition（展開形）が数学的に必要なら、その表現を保持する。

```text
public group canonicalization
!= semantic expression rewrite
!= proof fact mutation
```

## Phase 160 の非目標

Phase 160 では以下を実装しない。

```text
unrestricted stable theorem database
generic DirectSumGroup stable transport
generic FreeCyclicGroup stable transport
arbitrary generator-family normalization
unstable proof の stable transport による置換
new theorem roots
second proof engine
```

このプログラムの主対象は unstable homotopy groups（非安定ホモトピー群）であり、stable range は詳細な非安定計算を無限に繰り返さないための共通移送として扱う。

## 次 Phase との境界

Phase 160 で stem 1–7 の stable transport infrastructure は共通化できた。

次 Phase では stable layer をさらに一般化するのではなく、unstable range

$$
n<k+2
$$

の proof audit に戻る。

Phase 159 で stem 1 の低次境界を確認済みなので、残る低次 unstable target を $(k,n)$ の小さい順に監査し、実際に不足する数学規則だけを追加する。

repository-wide full pytest は Phase 160 closure では実行しない。
