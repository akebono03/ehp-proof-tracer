# Phase157 R11-R11 repair6

## Production

### toda_group_proof_narrative_contribution_renderer.py

変更関数全体:
- `order_toda_group_proof_narrative_surjectivity_support()`

変更:
- visible paragraph の比較時だけ `[R#]より, ` prefix を除く。
- `\tag{N}` は既存 match-key で比較時のみ除く。
- support step 3件すべてが visible な場合のみ contiguous block を移動。
- display text 自体は変更しない。

## Test

### tests/test_phase157_r5_r9_fixed_definition_body_suppression.py

- Reference membership の期待終止を `,` から `.` に更新。

## 完了条件

- `[R2]より, H(nu')=E^2 eta_3 tag(4)` が tag(6) より前。
- tag(4), tag(5), tag(6) が H-surjectivity より前。
- pi_6^5 group も H-surjectivity より前。
- focused pytest pass。
- full pytest はまだ実行しない。
