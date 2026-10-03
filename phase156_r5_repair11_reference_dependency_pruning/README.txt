Phase 156-R5 repair11 — Reference dependency pruning

目的
====
Reference の内部に畳まれた step からしか要求されていない Reference を、
利用側の Reference 一覧から除外する。

一般規則
========
Reference entry の各 step について、
既に internal と判定された step を通らずに root へ到達できるかを調べる。

- 到達できる Reference step:
  利用側 proof が直接必要としているため表示候補に残す。
- internal step を通らないと到達できない Reference step:
  畳まれた Reference proof の内部依存なので利用側一覧から除外する。

raw proof graph と Reference entry 自体は変更しない。
したがって Reference 自身の proof を展開すると内部依存は保持される。

pi_6^3 の期待
==============
raw graph:
- Proposition 5.1 remains.

public Reference section:
- (5.3)
- Proposition 5.3
- Lemma 5.4
- (5.2)

Proposition 5.1 is pruned because its relevant use is only inside the
collapsed proof of (5.3).

Production changes
==================
toda_group_proof_narrative_contribution_renderer.py

新規:
- _toda_group_proof_narrative_reference_externally_used_step_ids()

変更:
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Import changes
==============
None.

Tests
=====
- raw Reference inventory continues to include Proposition 5.1.
- public pi_6^3 Reference section excludes Proposition 5.1.
- Reference numbering remains compact.
- 112 groups at depth 2 and 3 generate without exceptions.

Repository-wide pytest is reserved for Phase 156 closure.
