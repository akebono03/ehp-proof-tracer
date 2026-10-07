<!-- PHASE160_DOCUMENTATION_CLOSURE -->
# Phase 160 generic stable transport proof record

Phase 160 は stable target の theorem provenance を新しい独立 root へ置換した Phase ではない。

既存の canonical-base proof と Toda (4.5) の isomorphism provenance を、共通 transport layer で接続した。

## stable target identity

対象:

$$
\pi_{n+k}^{n}.
$$

stable condition:

$$
n\ge k+2.
$$

canonical base:

$$
\pi_{2k+2}^{k+2}.
$$

transport:

$$
E^{n-k-2}:
\pi_{2k+2}^{k+2}
\overset{\cong}{\longrightarrow}
\pi_{n+k}^{n}.
$$

この3要素は rendered prose から推測せず、structural target / scalar expression / `ProofStep` から扱う。

## finite-cyclic transport provenance

canonical-base relation

$$
\pi_{2k+2}^{k+2}
=
\mathbb Z/r\{x\}
$$

と Toda (4.5) isomorphism から、generic transport は

$$
\pi_{n+k}^{n}
=
\mathbb Z/r\{E^{n-k-2}x\}
$$

を構成する。

ここで order $r$ は保持する。

```text
generic transport
!= generator-family identity
```

したがって $E^r x=\eta_n,\nu_n,\sigma_n$ などの family identity は別 provenance step とする。

## zero-group transport provenance

canonical base が

$$
\pi_{2k+2}^{k+2}=0
$$

なら、Toda (4.5) isomorphism を介して target zero を導出する。

```text
TodaPrimaryGroupZeroStatement
→ generic zero transport
→ TodaPrimaryGroupZeroStatement
```

zero を `FiniteCyclicGroup(order=1)` へ読み替えない。

## stem 1 provenance

canonical base:

$$
\pi_4^3=\mathbb Z/2\{\eta_3\}.
$$

stable result:

$$
\pi_{n+1}^{n}
=
\mathbb Z/2\{\eta_n\}.
$$

group transport と eta-family generator identity は分離する。

## stem 2 provenance

canonical base:

$$
\pi_6^4
=
\mathbb Z/2\{\eta_4^2\}.
$$

stable result:

$$
\pi_{n+2}^{n}
=
\mathbb Z/2\{\eta_n^2\}.
$$

internal generator は consecutive eta composition として保持できる。

public notation:

$$
\eta_n\eta_{n+1}
\longmapsto
\eta_n^2.
$$

## stem 3 provenance

canonical base:

$$
\pi_8^5
=
\mathbb Z/8\{\nu_5\}.
$$

generic transport 後:

$$
\mathbb Z/8\{E^{n-5}\nu_5\}.
$$

existing nu-family bridge により:

$$
E^{n-5}\nu_5=\nu_n.
$$

したがって

$$
\pi_{n+3}^{n}
=
\mathbb Z/8\{\nu_n\}.
$$

## stem 4 provenance

canonical base:

$$
\pi_{10}^6=0.
$$

generic zero transport により

$$
\pi_{n+4}^{n}=0.
$$

## stem 5 provenance

canonical base:

$$
\pi_{12}^7=0.
$$

stem 4 と同じ generic zero transport により

$$
\pi_{n+5}^{n}=0.
$$

## stem 6 provenance

canonical base:

$$
\pi_{14}^8
=
\mathbb Z/2\{\nu_8^2\}.
$$

generic group transport:

$$
\pi_{n+6}^{n}
=
\mathbb Z/2
\{E^{n-8}\nu_8^2\}.
$$

generator normalization:

$$
E^{n-8}\nu_8^2
=
\nu_n^2.
$$

最終 result:

$$
\pi_{n+6}^{n}
=
\mathbb Z/2\{\nu_n^2\}.
$$

public group notation では

$$
\nu_n\nu_{n+3}
\longmapsto
\nu_n^2
$$

を用いるが、internal `Composition` は変更しない。

## stem 7 provenance

canonical base:

$$
\pi_{16}^9
=
\mathbb Z/16\{\sigma_9\}.
$$

generic transport:

$$
\mathbb Z/16
\{E^{n-9}\sigma_9\}.
$$

sigma-family normalization:

$$
E^{n-9}\sigma_9=\sigma_n.
$$

したがって

$$
\pi_{n+7}^{n}
=
\mathbb Z/16\{\sigma_n\}.
$$

## public Narrative provenance boundary

stable Narrative の visible Reference は、

```text
[R1] Toda (4.5) general form
[R2] canonical base literature result
```

を基本とする。

target-specific substitution は proof body に置く。

```text
general Reference
!= specialized proof line

canonical base theorem
!= newly invented stable theorem root
```

canonical base 自身では stable transport Narrative を起動しない。

## public canonicalization provenance boundary

Group query Result / Group proof Conclusion / Narrative の generator notation は整合させる。

ただし canonicalization は presentation layer だけに適用する。

```text
eta_n eta_(n+1) -> eta_n^2
nu_n nu_(n+3)   -> nu_n^2
```

これは

```text
Composition object rewrite
ProofStep rewrite
theorem fact rewrite
```

ではない。

## verification record

Phase 160 の代表 focused evidence:

```text
R7 repair:
18 passed

R8 repair2:
37 passed

R9:
19 passed

R10 repair1:
117 passed in 23.92s
```

R11 は利用者指定により pytest を実行していない。

Web manual verification:

$$
\pi_{15}^{13}
\cong
\mathbb Z/2\{\eta_{13}^{2}\},
$$

$$
\pi_{19}^{13}
\cong
\mathbb Z/2\{\nu_{13}^{2}\}.
$$

両例で Result / Conclusion / Narrative の canonical notation が一致した。

repository-wide full pytest は Phase 160 closure では実行していないため、repository-wide all-pass は claim しない。

## next proof boundary

stable range の common transport infrastructure は Phase 160 で確立した。

次 Phase は unstable range

$$
n<k+2
$$

へ戻り、existing proof provenance を低次から順に監査する。

```text
stable group
→ Phase 160 transport を再利用

unstable group
→ existing EHP / literature proof を詳細に監査
```

不足する theorem fact / proof step が実際に現れた場合のみ、最小の再利用可能規則を追加する。
