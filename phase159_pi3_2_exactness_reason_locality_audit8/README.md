# Phase 159 pi3_2 exactness reason locality audit8

## 目的

repair7 後も

`[R1]より, pi_2^1=0.`

と

`完全性より, H は単射.`

の間に1段落残る原因を特定する。

## production 変更

なし。

## tests 変更

なし。

## 監査内容

1. public proof body の全 paragraph を index 付きで出力。
2. `EXACTNESS_TO_MAP_PROPERTY` reason を列挙。
3. 各 reason の `conclusion_step` と `premise_steps` を
   generic renderer で表示。
4. 次の statement の public paragraph index を表示。
   - pi_2^1=0
   - pi_3^3=Z{iota_3}
   - H injective
   - E isomorphism
   - E injective
   - Delta zero
   - H surjective
   - H isomorphism

## 完了条件

index 9 の paragraph と、
H injective reason の premise 構成を特定できること。

## 次 substep との境界

audit8 では production code を変更しない。
原因確認後にのみ locality rule の修正箇所を決める。
