# Phase 159 pi3_2 active reason-function audit17

## 目的

repair16 後も definition locality が発火しない原因を、
現在ローカルで import されている
`order_toda_group_proof_narrative_injective_image_order_reason()`
の実体から確認する。

## production 変更

なし。

## tests 変更

なし。

## 監査内容

- active function の source path
- definition locality marker の存在
- `return "\n\n".join(...)` の位置
- definition locality code の位置
- active function 全文

## 判定

### definition locality marker が False

repair14 の reason-renderer 変更が現在の active source に入っていない。

### marker は True だが definition code より前に最終 return がある

definition locality が unreachable（到達不能）になっている。

### marker も配置も正常

次は実関数内の branch trace を追加して、
どの `continue` で抜けているか確認する。

## 次 substep との境界

audit17 では production code を変更しない。
