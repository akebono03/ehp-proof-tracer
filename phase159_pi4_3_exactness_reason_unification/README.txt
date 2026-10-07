Phase 159 - pi_4^3 exactness reason unification

目的
====
π_4^3 の証明で、Delta image と E kernel の一致が EHP exactness による導出であるにもかかわらず、
public Narrative に「完全性より」が表示されない不統一を修正する。

今回の境界
==========
- π_4^3 固有の文章差し込みは行わない。
- TodaSuspensionKernelFreeCyclicStatement が
  TodaDeltaImageFreeCyclicStatement と TodaProp42ExactnessStatement を
  compatible direct premises として持つ場合に、
  generic typed reason EXACTNESS_TO_KERNEL を構築する。
- 既存の EXACTNESS_TO_MAP_PROPERTY は変更しない。
- equation numbering、他の prose 規則、Reference 選択には触れない。
- repository-wide test は実行しない。

変更対象
========
1. toda_group_proof_narrative_reasons.py
   - toda_rules import
   - TodaGroupProofNarrativeReasonKind
   - _exactness_to_kernel_reason() を新規追加
   - build_toda_group_proof_narrative_reason_sidecar()

2. toda_group_proof_narrative_reason_renderer.py
   - import
   - render_toda_group_proof_narrative_reason_sentence()

3. tests/test_phase159_pi4_3_exactness_reason_unification.py
   - 新規

実行方法
========
PowerShell で repository root に移動し、この zip を repository root に展開する。

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_pi4_3_exactness_reason_unification\run_phase159_pi4_3_exactness_reason_unification.ps1"

完了条件
========
- π_4^3 の E kernel 導出に EXACTNESS_TO_KERNEL reason が1件構築される。
- public Narrative で kernel conclusion の直前に「完全性より」が1回表示される。
- π_4^3 / η_2 / rule name の hard-code が新しい reason builder に存在しない。
- 既存 EXACTNESS_TO_MAP_PROPERTY focused regression が通る。
- Phase 50 の π_4^3 exactness bridge regression が通る。
