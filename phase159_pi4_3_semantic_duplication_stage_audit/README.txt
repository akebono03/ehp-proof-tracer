Phase 159 pi4_3 semantic duplication stage audit

この監査は production code を変更しません。

目的:
- pi4_3 root conclusion が public Narrative pipeline のどの段階で
  1回から2回に増えるかを特定する。
- 文字列ベースの推測修正を避ける。

記録する段階:
- base multi-argument renderer
- contribution insertion
- reason prose
- reference filtering / linking
- connector normalization
- exactness / map-property insertion
- unique-step suppression
- final ordering

出力では root conclusion の出現回数が変化した段階に
`CHANGED FROM ...` を表示する。

注意:
前回の新規テストにあった
`rendered.split("## 証明", 1)`
は `## 証明対象` を誤って拾うため、今回の監査では使用しない。

この監査では pytest と全体テストを実行しない。
