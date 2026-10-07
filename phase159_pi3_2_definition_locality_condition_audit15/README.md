# Phase 159 pi3_2 definition locality condition audit15

## 目的

repair14 で exactness locality は解決したが、
`pi_3^3 = Z{iota_3}` が eta_2 definition の直前へ移動しなかった。

definition locality の各判定条件を直接表示し、
どの条件で発火しないか特定する。

## production 変更

なし。

## tests 変更

なし。

## 監査項目

- definition ProofStep の検出数
- generic definition prose
- generic definition の math spans
- isomorphism premise 数
- public definition paragraph の match
- 各 direct premise の normalized key
- 各 direct premise の public paragraph match
- 関連 public paragraphs の index

## 完了条件

次のどれが失敗しているか特定する。

1. definition step detection
2. math-span definition match
3. isomorphism premise detection
4. H isomorphism premise paragraph match
5. pi_3^3 premise paragraph match

## 次 substep との境界

audit15 では production code を変更しない。
原因確定後、definition locality のみを修正する。
