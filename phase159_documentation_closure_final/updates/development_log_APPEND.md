

<!-- PHASE159_DOCUMENTATION_CLOSURE -->
# Phase 159 Mathematical proof coverage / stem-1 closure

日付: 2026-10-07

Phase 159 は Phase 158 で統一した public Narrative route を前提として、低次群を $n$ の小さい側から実際に読み、proof provenance と public proof の不足を修正する Phase とした。

開始対象は $k=1$ の $\pi_3^2$ であり、その後 $\pi_4^3$ を監査した。

## 完了した主要事項

$\pi_3^2$ では、定義 premise の locality、依存順序、map property、式番号、Reference の一般形表示を整理した。Reference は target 固有の特殊化を埋め込まず、literature statement の一般形を表示し、proof body 側で必要な特殊化を行う境界を確認した。

$\pi_4^3$ では、stable suspension による証明の public Narrative を監査し、既存の $k=1$ stable route が今後の generic stable transport の prototype として利用できることを確認した。

Phase 159 中の修正では、文章そのものを数学的同一性として比較する設計へ戻さず、semantic identity と proof provenance に基づく比較を維持した。式番号は後続で実際に参照される visible equation にのみ付与する Phase 158 contract を維持した。

## stable transport 設計

対象 $\pi_{n+k}^n$ に対し stable range を

$$
n\ge k+2
$$

とし、各 stem の canonical stable base を

$$
\pi_{2k+2}^{k+2}
$$

とする設計を確定した。stable target は

$$
E^{n-k-2}:\pi_{2k+2}^{k+2}\overset{\cong}{\longrightarrow}\pi_{n+k}^{n}
$$

で移送する。

群構造の transport は generic とし、generator naming / normalization は $\eta$、$\nu$、$\sigma$ など family-specific とする。

## closure boundary

Phase 159 では全 stem への generic stable transport 実装は行わない。$k=1$ を prototype として設計を確定したところで終了する。

ユーザー指定により、この documentation closure では repository-wide full pytest は実行しない。したがって Phase 159 closure は新たな repository-wide all-pass を claim しない。
