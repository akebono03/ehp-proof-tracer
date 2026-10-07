Phase 159 R1-7c R4 repair9 fix3

目的
====
fix2 の focused failure を受け、repair9 を current generic route 契約に合わせて修正する。

確認済み事実
============
1. pi_6^3
   - eta5_reflexive=1 は genuine regression。
   - fix2 の後、必要な `2 nu' = eta_3^3` が消えた。
   - よって graph-based reflexive suppression を最後に再実行するのは強すぎる。

2. pi_15^8
   - Phase 158-R5-5b で dedicated renderer から generic route に移行済み。
   - current public body は transported group relation -> final target の generic order。
   - Proposition 4.4 を使用する可視 consumer prose は存在しない。
   - よって Reference だけ残して marker を強制するのではなく、
     orphan Reference を final output から除くのが current generic contract に合う。

変更対象
========
Production:
- toda_group_proof_narrative_contribution_renderer.py

追加 helper:
- suppress_toda_group_proof_narrative_literal_reflexive_equalities()

変更関数:
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

import 変更:
- なし

group-specific branch:
- 追加しない

R9-A
====
最終 Markdown paragraph が literal に

  $A = A$

である場合だけ除去する。

proof graph statement identity や eta canonicalization relation を使って
reflexive 判定しない。

したがって

  eta_5 = eta_5

は消すが、

  2 nu' = eta_3^3

や

  eta_3 eta_4 eta_5 = eta_3^3

は消さない。

R9-C
====
最終 body-usage filtering の段階で本文に `[Rk]` が1つも無い場合は、
final public Reference entries を空にする。

これは「public Reference を出すなら body linkage が必要」という一般契約を
final output に適用するもの。

Phase157 stale test
===================
次の test file は dedicated pi15_8 renderer 前提:

- tests/test_phase157_r20_repair53_r3c_legacy_reference_marker_remapping.py

Phase158-R5-5b で pi15_8 は generic route に移行したため、
repair9 fix3 の合格条件には使用しない。

この substep では stale test 自体は変更しない。
必要なら Phase159 closure test cleanup で整理する。

全体 pytest
===========
実行しない。
Phase 159 最後まで保留。
