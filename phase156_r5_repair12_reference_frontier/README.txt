Phase 156-R5 repair12 — Reference frontier

診断結果
========
Proposition 5.1 の step は root へ到達できるが、その経路は:

- Proposition 5.1 -> (5.3) -> root
- Proposition 5.1 -> Proposition 5.3 -> root
- Proposition 5.1 -> Lemma 5.4 -> root

だった。

したがって Proposition 5.1 は parent proof が直接使う Reference ではなく、
別の Reference を証明するための内部依存である。

一般規則
========
Reference frontier を導入する。

ある Reference step から root へ向かう際、
別の非root LiteratureReference に入った時点でその path は打ち切る。

別 Reference を跨がず、
- same Reference step
- unreferenced bridge step
のみを経由して root へ到達できる Reference step だけを
parent proof の public Reference 候補とする。

これにより Reference の内部依存が sibling Reference として漏れない。

Production changes
==================
toda_group_proof_narrative_contribution_renderer.py

新規:
- _toda_group_proof_narrative_reference_frontier_step_ids()

変更:
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Import changes
==============
None. deque and reference extraction are already imported.

pi_6^3 expected public frontier
===============================
- (5.3)
- Proposition 5.3
- Lemma 5.4
- (5.2)

Proposition 5.1 remains in the raw proof graph but is not shown as a
parent-level sibling Reference.

Repository-wide pytest is reserved for Phase 156 closure.
