# Phase 159 pi3_2 locality re-apply audit13

## 目的

repair12 の locality 規則が public output に反映されない原因を、
production code を変更せず切り分ける。

## production 変更

なし。

## tests 変更

なし。

## 監査内容

1. 現在の public proof body を paragraph index 付きで表示。
2. reason sidecar の reason sentence / conclusion / premises を表示。
3. 現在の public proof body に
   `order_toda_group_proof_narrative_injective_image_order_reason()`
   を単独で再適用。
4. 再適用前後の位置を比較。
5. eta2 definition ProofStep の direct premises が
   public body に対応しているか確認。

## 判定

- `changed=True` かつ再適用後に期待順序になる:
  pipeline 後段で locality が崩されている。
- `changed=False`:
  function 内の paragraph match / definition detection が発火していない。
- 一部だけ動く:
  exactness locality と definition locality を個別に切り分ける。

## 次 substep との境界

audit13 では production code を変更しない。
結果確認後にだけ修正を行う。
