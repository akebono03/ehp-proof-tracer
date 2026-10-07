# Phase 159 $\pi_3^2$ Reference component-filter repair20a

## 変更対象

- `toda_group_proof_narrative_references.py`
  - `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()`
- `toda_group_proof_narrative_contribution_renderer.py`
  - import block
  - `_toda_group_proof_narrative_reference_statement_lines_by_number()`

テストファイルは変更しません。

## import 変更後全文

```python
from toda_literature_statement_boundary import (
  TodaLiteratureStatementClassification,
  classify_toda_literature_statement_step,
  get_toda_fixed_statement_component,
)
```

## `filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary()` 全文

```python
def filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary(
  entries: tuple[
    TodaGroupProofNarrativeReferenceEntry,
    ...,
  ],
  root_step: ProofStep,
) -> tuple[
  TodaGroupProofNarrativeReferenceEntry,
  ...,
]:
  if not isinstance(
    entries,
    tuple,
  ):
    raise TypeError(
      "entries must be a tuple"
    )

  if not all(
    isinstance(
      entry,
      TodaGroupProofNarrativeReferenceEntry,
    )
    for entry in entries
  ):
    raise TypeError(
      "entries must contain only "
      "TodaGroupProofNarrativeReferenceEntry objects"
    )

  if not isinstance(
    root_step,
    ProofStep,
  ):
    raise TypeError(
      "root_step must be a ProofStep"
    )

  root_boundary = (
    classify_toda_literature_statement_step(
      root_step
    )
  )

  target_reference_locator = (
    None
    if root_boundary is None
    else root_boundary.reference_locator
  )
  target_component_key = (
    None
    if root_boundary is None
    else root_boundary.component_key
  )

  retained_entries = []

  for entry in entries:
    retained_steps = []

    for proof_step in entry.proof_steps:
      boundary = (
        classify_toda_literature_statement_step(
          proof_step
        )
      )

      if (
        boundary is None
        or boundary.classification
        != TodaLiteratureStatementClassification.FIXED_STATEMENT
      ):
        continue

      if boundary.component_key is None:
        fixed_components = (
          get_toda_fixed_statement_components(
            boundary.reference_locator
          )
        )

        if fixed_components:
          retained_steps.append(
            proof_step
          )

        continue

      component = (
        get_toda_fixed_statement_component(
          boundary.reference_locator,
          boundary.component_key,
        )
      )

      if component is None:
        continue

      if (
        target_reference_locator is not None
        and target_component_key is not None
        and not is_toda_fixed_statement_component_reference_eligible(
          component,
          target_reference_locator,
          target_component_key,
        )
      ):
        continue

      retained_steps.append(
        proof_step
      )

    if not retained_steps:
      continue

    retained_entries.append(
      replace(
        entry,
        number=len(
          retained_entries
        ) + 1,
        proof_steps=tuple(
          retained_steps
        ),
      )
    )

  retained_entries = sorted(
    retained_entries,
    key=lambda entry: (
      0
      if entry.reference.locator
      == "(5.1)"
      else 1
    ),
  )

  return tuple(
    replace(
      entry,
      number=number,
    )
    for number, entry in enumerate(
      retained_entries,
      start=1,
    )
  )
```

これは repair20 で変更する前の既存実装へ戻します。

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
        _phase157_r20_canonical_fixed_reference_line(
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
        _phase157_r20_canonical_fixed_reference_line(
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

## 変更一覧

- Reference entry の `proof_steps` を削らない。
- `range_is_explicit_in_current_aggregate` は表示行生成時だけ参照する。
- repair18 が使う proof dependency / linkage を保持する。
- repair20 で導入した `(5.1)` component の一般形描画は維持する。
- テスト契約は追加・変更しない。

## 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_r1_6c_source_faithful_reference_linkage.py::test_phase159_r1_6c_toda_51_reference_is_source_faithful" `
  ".\tests\test_phase159_r1_6b_toda51_attribution.py::test_phase159_r1_6b_pi3_2_public_reference_uses_single_toda_51_entry"

python -m pytest -q `
  ".\tests\test_phase159_pi3_2_public_definition_premise_locality.py"
```

## 完了条件

Reference:

```text
[R1] (5.1).
π_i^1 = 0  (i > 1).
π_n^n = Z{iota_n}.
```

本文では repair18 の dependency chain がすべて復活し、3 tests が PASS すること。

## 次 repair との境界

`E(\iota_1)=\iota_2` の復元や GIVEN の整理にはまだ進みません。
