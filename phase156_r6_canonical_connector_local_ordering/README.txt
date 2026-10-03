Phase 156-R6 — canonical expression / connector / local ordering

目的
====
Phase156-R5 で Reference boundary / Reference frontier が成立した後の
presentation 側の残存問題を一般規則で修正する。

1. canonical expression
-----------------------
Narrative 表示では Suspension(eta_n) を eta_(n+1) と表示する。

例:
  eta_3 E eta_3 eta_5
-> eta_3 eta_4 eta_5

proof graph / expression object 自体は変更しない。
表示だけを canonical form にする。

2. connector
------------
連続する段落が

  以上より,

  以上で得た群構造, 生成元, および写像に関する結果を合わせると,

となる場合、前者は後者より情報量が少ないため削除する。

3. local ordering
-----------------
番号付き式 (a), (b) を参照する

  (a) と (b) より,

  <derived equation>

を、参照元の最後の式の直後へ配置する。

式内容や group identity は見ない。
equation tag の dependency のみを利用する。

変更対象
========
Production:
- toda_group_proof_generic_narrative_renderer.py
  - import: Suspension を追加
  - _render_generic_narrative_expression_latex()

- toda_group_proof_narrative_contribution_renderer.py
  - normalize_toda_group_proof_narrative_connectors() 新規
  - _toda_group_proof_narrative_equation_tag_number() 新規
  - _toda_group_proof_narrative_two_equation_reference_numbers() 新規
  - order_toda_group_proof_narrative_local_equation_derivations() 新規
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()

Tests:
- old E eta_3 display expectations are updated to eta_4 in related rendering tests
- tests/test_phase156_r6_canonical_connector_local_ordering.py 新規

期待する pi_6^3 の局所形
==========================
$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$

$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$

(1) と (2) より,

$2\nu' = \eta_{3}^{3}\tag{3}$

$\operatorname{ord}(\eta_{3}^{3}) = 2$

全体 pytest
===========
Phase 156 closure まで実行しない。
