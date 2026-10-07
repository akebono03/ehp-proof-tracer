# Phase 159 $\pi_3^2$ Reference component-filter repair20b

## 変更対象

`import` の変更はありません。

- `toda_group_proof_narrative_contribution_renderer.py`
  - `_phase157_r20_canonical_fixed_reference_line()`
  - `_toda_group_proof_narrative_reference_statement_lines_by_number()`

テストファイルは変更しません。

## `_phase157_r20_canonical_fixed_reference_line()` 全文

```python
def _phase157_r20_canonical_fixed_reference_line(
  proof_step: ProofStep,
  rendered_statement: str,
) -> str:
  boundary = (
    classify_toda_literature_statement_step(
      proof_step
    )
  )

  if (
    boundary is not None
    and boundary.component_key
    == "hopf_right_composition_formula"
  ):
    return (
      r"$H(\alpha\circ E\beta)"
      r" = H(\alpha)\circ E\beta$."
    )

  return rendered_statement
```

repair20 以前の共通 helper に戻します。これは proof-body ordering からも利用されるため、Toda (5.1) の一般化をここでは行いません。

## `_toda_group_proof_narrative_reference_statement_lines_by_number()` 全文

```python
def _toda_group_proof_narrative_reference_statement_lines_by_number(
  presentation: TodaGroupProofPresentation,
  reference_entries,
) -> dict[
  int,
  tuple[
    str,
    ...,
  ],
]:
  statement_lines_by_reference_number = {}

  def reference_display_line(
    proof_step: ProofStep,
    rendered_statement: str,
  ) -> str:
    boundary = (
      classify_toda_literature_statement_step(
        proof_step
      )
    )

    if (
      boundary is not None
      and boundary.reference_locator
      == "(5.1)"
      and boundary.component_key
      == "circle_higher_homotopy_zero"
    ):
      return (
        r"$\pi_{i}^{1} = 0\ (i > 1)$."
      )

    if (
      boundary is not None
      and boundary.reference_locator
      == "(5.1)"
      and boundary.component_key
      == "sphere_connectivity_zero"
    ):
      return (
        r"$\pi_{i}^{n} = 0\ (i < n)$."
      )

    if (
      boundary is not None
      and boundary.reference_locator
      == "(5.1)"
      and boundary.component_key
      == "diagonal_identity_group"
    ):
      return (
        r"$\pi_{n}^{n} = "
        r"\mathbb{Z}\{\iota_{n}\}$."
      )

    return (
      _phase157_r20_canonical_fixed_reference_line(
        proof_step,
        rendered_statement,
      )
    )

  for entry in reference_entries:
    candidate_steps = []
    rendered_by_step_id = {}
    seen_rendered_statements = set()

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is not None
        and boundary.classification
        is TodaLiteratureStatementClassification.FIXED_STATEMENT
        and boundary.component_key is not None
      ):
        component = (
          get_toda_fixed_statement_component(
            boundary.reference_locator,
            boundary.component_key,
          )
        )

        if not (
          component
          .range_is_explicit_in_current_aggregate
        ):
          continue

      rendered_statement = (
        _render_generic_narrative_step(
          proof_step
        )
      )
      rendered_statement = (
        reference_display_line(
          proof_step,
          rendered_statement,
        )
      )

      if not (
        _is_toda_group_proof_narrative_reference_statement_candidate(
          proof_step,
          rendered_statement,
        )
      ):
        continue

      if (
        rendered_statement
        in seen_rendered_statements
      ):
        continue

      seen_rendered_statements.add(
        rendered_statement
      )
      candidate_steps.append(
        proof_step
      )
      rendered_by_step_id[
        id(
          proof_step
        )
      ] = rendered_statement

    selected_steps = (
      select_toda_group_proof_narrative_reference_statement_steps(
        entry,
        tuple(
          candidate_steps
        ),
        presentation.edges,
        root_step=presentation.root_step,
      )
    )

    aggregate_specializations = tuple(
      (
        proof_step,
        _phase153_r6_reference_aggregate_component(
          presentation,
          entry,
          proof_step,
        ),
      )
      for proof_step in selected_steps
      if is_dataclass(
        proof_step.conclusion
      )
    )
    aggregate_specializations = tuple(
      pair
      for pair in aggregate_specializations
      if pair[
        1
      ] is not None
    )

    if len(
      aggregate_specializations
    ) == 1:
      selected_steps = (
        aggregate_specializations[
          0
        ][
          0
        ],
      )

    rendered_selected_by_step_id = {
      id(
        proof_step
      ): (
        reference_display_line(
          proof_step,
          _phase153_r6_render_reference_statement(
            presentation,
            entry,
            proof_step,
            rendered_by_step_id[
              id(
                proof_step
              )
            ],
          ),
        )
      )
      for proof_step in selected_steps
    }

    statement_lines = (
      _phase157_r5_r7_order_and_connect_fixed_definition_reference_lines(
        selected_steps,
        rendered_selected_by_step_id,
      )
    )

    if statement_lines:
      statement_lines_by_reference_number[
        entry.number
      ] = statement_lines

  return statement_lines_by_reference_number
```

## 変更内容

- 共通 canonical helper は特殊化 statement を維持する。
- Toda (5.1) の一般形変換は Reference section の statement-line rendering 内だけで行う。
- `range_is_explicit_in_current_aggregate=False` の component は Reference 表示からだけ除外する。
- proof body、dependency ordering、repair18 locality には影響させない。

## 完了条件

Reference:

```text
[R1] (5.1).
$\pi_{n}^{n} = \mathbb{Z}\{\iota_{n}\}$.
$\pi_{i}^{1} = 0\ (i > 1)$.
```

Proof body:

```text
$\pi_{2}^{1} = 0$.
...
$\pi_{3}^{3} = \mathbb{Z}\{\iota_{3}\}$.
```

を維持し、repair18 の3 tests が PASS すること。

## 次 repair との境界

今回は Reference/general と proof/specialized の分離のみです。
`E(\iota_1)=\iota_2` の復元にはまだ進みません。
