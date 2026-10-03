Phase 156-R5 repair8 — Reference-owned ancestor closure

診断で確定した事実
==================
Toda (5.3) Reference entry の bracket specialization step と、
Narrative semantic が利用する bracket-membership step は別 ProofStep だった。

Narrative 側 step:
- inference_rule=None
- literature_reference=None
- (5.3) の referenced step を支える premise
- Lemma 5.2 reason と ESTABLISH_DEFINITION argument の conclusion

したがって exact ProofStep identity だけでは Reference boundary を切れない。

一般規則
========
Reference entry の明示的 step に加えて、
そこへ流入する無参照 ancestor を Reference-owned step とする。

ただし安全のため:
- ancestor の全 consumer が既に同じ owned closure 内にある場合だけ所有する
- 別の明示的 LiteratureReference を持つ premise は所有しない
- root step は所有しない

これにより共有 step や別 Reference の根拠を誤って飲み込まない。

Production changes
==================
toda_group_proof_narrative_contribution_renderer.py

新規:
- _toda_group_proof_narrative_reference_owned_step_ids()

変更:
- _toda_group_proof_narrative_reference_internal_step_ids()
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

import changes
==============
None.

Expected pi_6^3 public Narrative
===============================
Reference:
- Toda (5.3) remains
- Lemma 5.2 header absent
- selected consequences remain

Body:
- Lemma 5.2 absent
- nu' bracket definition absent
- 2 eta_3 = 0 absent
- "nu' を定める" absent

Proof graph and semantic sidecar remain intact.

Repository-wide pytest is reserved for Phase 156 closure.
