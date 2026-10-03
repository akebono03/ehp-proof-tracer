Phase 156-R5 repair6 — Reference boundary collapse

目的
====
ある result を Reference として採用した場合、その Reference 自体を証明する
internal proof dependency は利用側 Narrative では展開しない。

pi_6^3 では:
- Toda (5.3) を Reference source とする。
- (5.3) の内部で使う Lemma 5.2 は group proof 本文へ出さない。
- nu' bracket definition, 2 eta_3 = 0, nu' の再定義も本文へ出さない。
- (5.3) の selected consequence だけを Reference として利用する。

Production changes
==================
1. toda_group_proof_narrative_contribution_renderer.py
   - Reference boundary step collection
   - unselected internal Reference step suppression
   - Reference-owned reason prose suppression
   - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

2. toda_group_proof_narrative_reason_renderer.py
   - repair5 で加えた global prose changes を repair5 前の generic baseline に戻す。

import changes
==============
None.

Test changes
============
- Phase144 Reference contract
- Phase150 reason-renderer unit contract restored
- Phase156-R5 intermediate contracts aligned
- superseded repair5 focused test removed
- new repair6 focused test added

Boundary
========
Proof graph / semantic sidecar / InferenceRule は保持する。
Reference を利用する Narrative 表示だけで内部 proof を畳む。
したがって将来、Reference 自体を proof expansion する機能を妨げない。

Repository-wide pytest is reserved for Phase 156 closure.
