Phase 156-R6-3 — reason prose canonicalization

目的
====
Phase156-R6 / repair2 で、本文の canonical expression は次の形になった。

$2\nu' = \eta_{3}\eta_{4}\eta_{5}\tag{1}$

$\eta_{3}\eta_{4}\eta_{5} = \eta_{3}^{3}\tag{2}$

(1) と (2) より,

$2\nu' = \eta_{3}^{3}\tag{3}$

$\operatorname{ord}(\eta_{3}^{3}) = 2$

しかし MULTIPLE_RELATION_TO_ORDER の reason prose は
render_toda_expression_latex() を直接使っていたため、

$\operatorname{ord}(\eta_{3}\eta_{4}\eta_{5})=2$
かつ
$2\nu'=\eta_{3}\eta_{4}\eta_{5}$

という expanded form に戻っていた。

一般規則
========
reason prose も、本文と同じ
_render_generic_narrative_expression_latex()
を使って expression を表示する。

proof graph や reason classification は変更しない。
式 (3) の文字列を検索・再利用する処理も追加しない。

同じ semantic expression に対して同じ canonical renderer を使うだけとする。

変更対象
========
Production:
- toda_group_proof_narrative_reason_renderer.py
  - import:
    _render_generic_narrative_expression_latex を追加
  - render_toda_group_proof_narrative_reason_sentence()

Tests:
- tests/test_phase156_r6_3_reason_prose_canonicalization.py 新規

変更後 import
=============
from toda_human_readable_renderer import (
  render_toda_expression_latex,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_expression_latex,
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_reasons import (
  TodaGroupProofNarrativeReason,
  TodaGroupProofNarrativeReasonKind,
  TodaGroupProofNarrativeReasonSidecar,
)

期待する reason prose
======================
$\operatorname{ord}(\eta_{3}^{3})=2$
かつ
$2\nu'=\eta_{3}^{3}$
より,
$4\nu'=0$ かつ $2\nu'\neq0$ である.

Repository-wide pytest は Phase 156 closure でのみ実行する。
