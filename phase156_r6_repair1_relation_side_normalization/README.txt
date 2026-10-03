Phase 156-R6 repair1 — relation-side normalization

原因
====
Phase156-R6 では Relation の lhs / rhs を canonical expression に直す際、
完成済み LaTeX 文字列に対して順番に str.replace() していた。

pi_6^3 の equation (2) では:

lhs raw:
  eta_3 E eta_3 eta_5

lhs canonical:
  eta_3 eta_4 eta_5

rhs raw:
  eta_3 eta_4 eta_5

rhs canonical:
  eta_3^3

となる。

lhs を canonical 化した直後、その文字列が rhs raw と一致するため、
rhs の replace が lhs にも再適用され、左辺まで eta_3^3 に潰れる。

修正
====
元の LaTeX 文字列上で lhs span と rhs span を先に確定し、
非重複 span を slicing で一度だけ置換する。

これにより canonicalization が相互干渉しない。

変更対象
========
Production:
- toda_group_proof_generic_narrative_renderer.py
  - _normalize_generic_narrative_step_latex()

Import changes:
- none

Tests:
- tests/test_phase156_r6_repair1_relation_side_normalization.py 新規

既存 Phase156-R6 の canonical / connector / local ordering 実装は変更しない。

期待形
======
$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$

$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$

(1) と (2) より,

$2\nu' = \eta_{3}^{3}\tag{3}$

$\operatorname{ord}(\eta_{3}^{3}) = 2$

Repository-wide pytest is reserved for Phase 156 closure.
