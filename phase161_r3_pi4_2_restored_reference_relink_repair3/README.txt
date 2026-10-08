Phase 161-R3 repair3

前提
====
renderer recovery により production renderer は復旧済み。

復旧確認:
- 9841 lines
- py_compile PASS
- target render function exists
- restore/body-usage/relink helpers exist

既知の非R3 failure
==================
tests/test_phase157_r20_repair12_map_property_reference_support.py

のうち2件は Phase 161-R3 前から存在する current Narrative contract との
不整合として扱う。

Phase 161-R3 の gate には使用しない。

変更対象
========
production:
- toda_group_proof_narrative_contribution_renderer.py
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

test:
- tests/test_phase161_pi4_2_restored_reference_relink.py

import の変更なし。

変更
====
restore_toda_group_proof_narrative_fixed_reference_entries_after_body_usage()
の直後に既存 helper

link_toda_group_proof_narrative_unmarked_reference_consumers()

を再適用する。

final body-usage filter は維持する。

完了条件
========
- public Reference に (5.2) が残る
- Proposition 4.4 も残る
- body に [R1], [R2] linkage が存在する
- pi_4^2 結論と QED が維持される
- Phase 161 focused test PASS
- R2 までの baseline 43 tests PASS

全体 pytest は Phase 161 最後にのみ実行する。
