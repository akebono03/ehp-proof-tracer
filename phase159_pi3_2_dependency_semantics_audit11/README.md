# Phase 159 pi3_2 dependency semantics audit11

## 目的

repair10 が `pi_2^1=0 -> H injective` と
`pi_3^3 -> eta_2 definition` の locality を変更しなかった原因を、
presentation / semantic sidecar / reason sidecar の実データから確認する。

## production 変更

なし。

## tests 変更

なし。

## 監査内容

- public narrative 全文
- 対象 presentation nodes
- 各対象 ProofStep の direct premises
- 対象 node に接続する presentation edges
- semantic dependency records 全件
- narrative reasons 全件
- `EXACTNESS_TO_MAP_PROPERTY` reason 件数
- `DEFINITION_APPLICABILITY` reason 件数

## 完了条件

次の実データを特定できること。

1. `H injective` の direct premise 構成。
2. `eta_2 definition` の direct premise 構成。
3. `pi_3^3=Z{iota_3}` から eta_2 definition への semantic dependency の有無。
4. exactness / definition reason が reason sidecar に生成されているか。

## 次 substep との境界

audit11 では production code を変更しない。
結果を確認してから、修正対象を reason renderer、
semantic dependency、または contribution ordering のどこに置くか決める。
