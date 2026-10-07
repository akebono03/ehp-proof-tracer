# Phase 159 $\pi_3^2$ Reference linkage repair21

## 変更対象

- `toda_group_proof_narrative_contribution_renderer.py`
  - `_toda_group_proof_narrative_reference_statement_lines_by_number()`
- `toda_group_proof_narrative_references.py`
  - `render_toda_group_proof_narrative_reference_entries_markdown()`
- `toda_group_proof_narrative_renderer.py`
  - `render_toda_group_proof_narrative_markdown()` の最終返値に既存
    `_phase159_r1_6d_finalize_reference_and_linkage()` を再接続
- `tests/test_phase159_pi3_2_public_definition_premise_locality.py`
  - `[R1]より,` を現行契約 `[R1] より,` に訂正

import の変更はありません。

## 変更方針

Reference 表示用の一般形と、本文 linkage 用の特殊化 statement を分離する。

`statement_lines_by_reference_number` は従来どおり特殊化 statement を保持するため、

- `$π_2^1=0$.`
- `$π_3^3=Z{ι_3}$.`
- `E:π_1^1→π_2^2 は同型.`

を既存 duplicate/linkage 処理が認識できる。

一方、Reference markdown の描画時だけ `(5.1)` の component key を見て一般形へ変換する。

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

## `render_toda_group_proof_narrative_reference_entries_markdown()` 全文

```python
def render_toda_group_proof_narrative_reference_entries_markdown(
  entries: tuple[TodaGroupProofNarrativeReferenceEntry, ...],
  statement_lines_by_reference_number: (
    dict[
      int,
      tuple[
        str,
        ...,
      ],
    ]
    | None
  ) = None,
) -> str:
  if not isinstance(entries, tuple):
    raise TypeError("entries must be a tuple")

  if (
    statement_lines_by_reference_number is not None
    and not isinstance(
      statement_lines_by_reference_number,
      dict,
    )
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be "
      "a dict or None"
    )

  if statement_lines_by_reference_number is not None:
    for reference_number, statement_lines in (
      statement_lines_by_reference_number.items()
    ):
      if (
        isinstance(
          reference_number,
          bool,
        )
        or not isinstance(
          reference_number,
          int,
        )
      ):
        raise TypeError(
          "statement_lines_by_reference_number keys "
          "must be integers"
        )

      if not isinstance(
        statement_lines,
        tuple,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must be tuples"
        )

      if not all(
        isinstance(
          line,
          str,
        )
        for line in statement_lines
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

  if not entries:
    return ""

  lines = []

  for entry in entries:
    if not isinstance(entry, TodaGroupProofNarrativeReferenceEntry):
      raise TypeError(
        "entries must contain only "
        "TodaGroupProofNarrativeReferenceEntry objects"
      )

    title = entry.reference.locator or entry.reference.label
    lines.append(f"**[R{entry.number}] {title}.**")

    if entry.reference.locator == "(5.1)":
      component_keys = {
        boundary.component_key
        for proof_step in entry.proof_steps
        for boundary in (
          classify_toda_literature_statement_step(
            proof_step
          ),
        )
        if (
          boundary is not None
          and boundary.classification
          == TodaLiteratureStatementClassification.FIXED_STATEMENT
          and boundary.reference_locator
          == "(5.1)"
          and boundary.component_key is not None
        )
      }

      if "circle_higher_homotopy_zero" in component_keys:
        lines.append(
          r"$\pi_{i}^{1} = 0\ (i > 1)$."
        )

      if "sphere_connectivity_zero" in component_keys:
        component = (
          get_toda_fixed_statement_component(
            "(5.1)",
            "sphere_connectivity_zero",
          )
        )

        if (
          component is not None
          and component
          .range_is_explicit_in_current_aggregate
        ):
          lines.append(
            r"$\pi_{i}^{n} = 0\ (i < n)$."
          )

      if "diagonal_identity_group" in component_keys:
        lines.append(
          (
            r"$\pi_{n}^{n} = "
            r"\mathbb{Z}\{\iota_{n}\}$."
          )
        )

      continue

    statement_lines = (
      ()
      if statement_lines_by_reference_number is None
      else statement_lines_by_reference_number.get(
        entry.number,
        (),
      )
    )

    for statement_line in statement_lines:
      lines.append(
        statement_line
      )

  return "\n".join(lines)
```

## `render_toda_group_proof_narrative_markdown()`

ローカルの repair18 後の関数全体を置換せず、AST で現在の最終 return expression をそのまま保持して、

```python
_phase159_r1_6d_finalize_reference_and_linkage(
  presentation,
  <現在の最終 return expression>,
)
```

で包む。

これにより repair18 の ordering 処理を壊さない。

## テスト変更

`tests/test_phase159_pi3_2_public_definition_premise_locality.py` 内の

```python
"[R1]より, "
```

をすべて

```python
"[R1] より, "
```

へ訂正する。

これは `tests/test_phase159_r1_6d_specialization_reference_linkage_finalization.py` の既存契約と一致する。

## 実行する pytest

- R1-6c Reference focused 2 tests
- R1-6d specialization/reference-linkage file
- repair18 locality file

全体 pytest は Phase 159 終了時まで実行しない。

## 完了条件

Reference:

```text
[R1] (5.1).
π_i^1 = 0 (i > 1).
π_n^n = Z{iota_n}.
```

本文:

```text
[R1] より, π_2^1 = 0.
...
[R1] より, π_1^1 = Z{iota_1}, π_2^2 = Z{iota_2}.
E(iota_1)=iota_2 であるから, E:π_1^1→π_2^2 は同型.
...
[R1] より, π_3^3 = Z{iota_3}.
```

となり、`[R1]を用いて, この同型写像により, ...` が消えること。

## 次 repair との境界

今回は既存 Reference/body linkage の再接続まで。
E 同型を GIVEN から完全に導出構造へ変更する内部 proof graph 修正には進まない。
