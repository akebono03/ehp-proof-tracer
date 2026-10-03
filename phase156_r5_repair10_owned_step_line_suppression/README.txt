Phase 156-R5 repair10 — owned-step line suppression

原因
====
repair8 で Reference-owned ancestor step IDs は正しく求められるようになった。

しかし suppress_toda_group_proof_narrative_reference_internal_body() は、
実際に削除する statement line を entry.proof_steps からしか収集していなかった。

そのため、無参照 ancestor である Narrative bracket-membership step は
internal_step_ids に含まれていても、行削除対象には入らなかった。

修正
====
internal statement line を presentation.nodes 全体から収集し、
internal_step_ids に含まれる全 step の rendered line を削除対象にする。

これにより:
- Lemma 5.2 reason は非表示
- "nu' を定める" argument purpose は非表示
- bracket-membership line も非表示
- (5.3) の selected public consequences は Reference に残る

Production changes
==================
toda_group_proof_narrative_contribution_renderer.py

変更関数:
- suppress_toda_group_proof_narrative_reference_internal_body()

Import changes
==============
Production: none.

Test changes
============
- Phase150 parametrized test の duplicate decorator を1つに修正
- repair9 focused tests
- new repair10 focused test

Audit
=====
112 groups × depth 2/3 generation.
pi_6^3 は全文に対して internal bracket が存在しないことを確認する。
"次に..." で本文を切って見落とす監査は廃止する。

Repository-wide pytest is reserved for Phase 156 closure.
