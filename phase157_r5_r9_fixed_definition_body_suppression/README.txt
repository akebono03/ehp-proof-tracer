Phase157-R5-R9 — fixed definition body suppression

目的:
Reference に移した fixed definition に対応する
definition-introduction と、その内部適用専用 precondition を
Proof body から除外する一般規則を実装する。

一般規則:
1. Reference に実際に選ばれた FIXED_STATEMENT のうち
   component_key が *_definition の step を特定する。
2. その fixed definition step の本文再掲を除外する。
3. semantic dependency が
   PRECONDITION_FOR_DEFINITION
   で、dependent_step がその fixed definition の場合、
   prerequisite_step を本文から除外する。
4. 同じ definition argument の purpose sentence
   「〜を定める.」
   も除外する。
5. 名前 `(5.3)`, `nu_prime`, `eta_3` による特例判定は行わない。

今回 pi_6^3 で消えるもの:
- まず, $\nu'$ を定める.
- $2\eta_3=0$
- body 側の
  $\nu'\in\{\eta_3,2\iota_4,\eta_4\}_1$

Reference 側には残る:
- bracket definition とすると,
- membership,
- double relation.

変更対象:
- toda_group_proof_narrative_contribution_renderer.py
- tests/test_phase157_r5_r6_53_bracket_definition_reference.py
- tests/test_phase144_6_r25_9b_nu_prime_definition_depth2.py
- tests/test_phase157_r5_r9_fixed_definition_body_suppression.py (new)

import:
- TodaGroupProofNarrativeDependencySemanticRole を追加。

class変更:
- なし。

production変更:
- 新規 helper:
  _phase157_r5_r9_selected_fixed_definition_step_ids()
- 変更:
  suppress_toda_group_proof_narrative_reference_internal_body()
- 変更:
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
  （semantic_sidecar を suppression に渡すだけ）

Phase境界:
- Reference selection/catalog は変更しない。
- order / exactness / group-structure 本文は変更しない。
- repository-wide pytest は Phase157 closure まで実行しない。
