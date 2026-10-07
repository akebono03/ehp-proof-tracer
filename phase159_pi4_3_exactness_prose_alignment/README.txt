Phase 159 - pi_4^3 exactness prose alignment

目的
====
pi_6^3 では exactness reason が証明本文の主文として表示される一方、
pi_4^3 では次の未統一が残っていた。

1. 「これより, 完全性より,」という connector の二重化
2. exactness reason の後に
   Im Δ = ...
   ker E = ...
   が再掲される semantic duplication
3. EXACTNESS_TO_KERNEL だけ「である.」が残り、
   現行 exactness prose の式末規則と一致しない

今回の変更
==========
typed reason EXACTNESS_TO_KERNEL に対する一般規則として、

- reason sentence を「完全性より, ... .」に統一
- reason の直前の standalone「これより,」を抑制
- reason が包含する image statement / kernel statement の
  後続再掲を抑制

を行う。

pi_4^3、eta_2、特定の Proposition 名による hard-code は追加しない。

変更対象
========
toda_group_proof_narrative_reason_renderer.py

追加:
_normalize_exactness_to_kernel_reason_prose()

変更:
render_toda_group_proof_narrative_reason_sentence()
insert_toda_group_proof_narrative_reason_prose()

tests/test_phase159_pi4_3_exactness_reason_unification.py

追加:
test_phase159_pi4_3_exactness_reason_matches_existing_exactness_prose_style()

import 変更
===========
なし。

実行 pytest
===========
1. tests/test_phase159_pi4_3_exactness_reason_unification.py
2. tests/test_phase150_rc4_5c_2_exactness_to_map_property.py
3. tests/test_phase50_pi4_3_exactness_bridge.py

完了条件
========
- pi_4^3 に「これより, 完全性より,」が出ない。
- EXACTNESS_TO_KERNEL reason が「完全性より,」で始まる。
- reason sentence に「である.」を重ねない。
- Im Δ の standalone statement は元の1回だけ残る。
- ker E の standalone duplicate は抑制される。
- pi_6^3 の既存 EXACTNESS_TO_MAP_PROPERTY regression が維持される。
- Phase 50 pi_4^3 exactness bridge が維持される。

Phase 境界
==========
- pi_6^3 の数学的 proof structure は変更しない。
- Reference selection は変更しない。
- equation numbering は変更しない。
- 他の prose reason kind は変更しない。
- repository-wide tests は Phase 159 終了時まで実行しない。
