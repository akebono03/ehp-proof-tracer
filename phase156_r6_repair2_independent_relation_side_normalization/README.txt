Phase 156-R6 repair2 — independent relation-side normalization

原因
====
repair1 では Relation の lhs / rhs の canonicalization が相互干渉しないよう、
元 LaTeX 上の非重複 span を使うようにした。

しかし lhs と rhs の両方を expression renderer で描画できることを
前提にしていた。

ORDER relation:
  lhs = Composition(eta_3, eta_4, eta_5)
  rhs = 2

では rhs が scalar int のため expression renderer は None を返す。
repair1 はそこで relation 全体の canonicalization を中止した。

結果:
  ord(eta_3 eta_4 eta_5) = 2

のまま残っていた。

修正
====
lhs / rhs を独立に扱う。

- expression renderer で描画できる側だけ canonicalize
- 描画できない scalar / group side はそのまま保持
- 元 LaTeX 上で各 span を確定
- replacement は後ろから適用して位置ずれを防ぐ

これにより:

Equality:
  eta_3 eta_4 eta_5 = eta_3^3

Order:
  ord(eta_3^3) = 2

を同時に維持する。

変更対象
========
Production:
- toda_group_proof_generic_narrative_renderer.py
  - _normalize_generic_narrative_step_latex()

Import changes:
- none

Tests:
- tests/test_phase156_r6_repair2_independent_relation_side_normalization.py 新規

既存 Phase156-R6 の connector / local ordering は変更しない。

Repository-wide pytest is reserved for Phase 156 closure.
