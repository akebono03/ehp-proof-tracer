Phase 143-75AP R17

変更対象
========
実装:
- toda_group_proof_narrative_argument_body_renderer.py
  - render_toda_group_proof_narrative_argument_body_markdown()

import:
- 変更なし

テスト:
- 新規変更なし
- R16-R2 で現在仕様へ更新済みの focused tests を再実行

修正内容
========
R16-R2 の provenance-only statement 判定による救済を廃止する。

既存分類をそのまま利用し、
preserve_provenance_block_ids に含まれる block 内で
redundant_direct_premise_step_ids に含まれる step だけを
redundant suppression から保持する。

relocated_direct_premise_ids の suppression は解除しない。

意味
====
pi_15^8:
transported decomposition は final group conclusion の redundant direct premise
として分類されるが、DERIVATION source block として semantic 表示が必要なので保持。

pi_8^5:
2 nu_5 = E^2 nu' は redundant ではなく relocatable premise なので、
元位置では除去され、既存 relocation 処理で結論直前に1回だけ表示される。

変更しないもの
==============
- import
- 数学規則
- proof repository
- public API
- group calculation
- generic renderer
- Phase144以降
- documentation

完全な変更関数
==============
実行時に現行ローカル関数全体を抽出し、
phase143_75ap_r17/
render_toda_group_proof_narrative_argument_body_markdown.txt
へ保存する。

focused pytest
==============
- Phase143-51A
- Phase143-51B
- Phase143-59B
- Phase143-61B
- Phase143-61B-R
- Phase134-24 pi15^8 Narrative

完了条件
========
1. pi_15^8 transported decomposition が semantic LaTeX で表示される。
2. pi_15^8 final group conclusion も維持される。
3. pi_8^5 direct premise は1回だけ表示される。
4. pi_8^5 relocation 順序を維持する。
5. internal rule-name fallback を表示しない。
6. focused regression 全通過。

次Phaseとの境界
===============
Phase143 の semantic Narrative 整合性だけを修正する。
Phase144 の機能は含めない。
