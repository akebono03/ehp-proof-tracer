# Phase 159-R1-6a repair1

## 変更対象

- `toda_group_proof_narrative_renderer.py`
  - `_phase159_render_foundational_reference_section()`
  - `_phase159_inject_foundational_reference_section()`

import 変更:
- なし

テスト変更:
- なし

## `_phase159_render_foundational_reference_section()` 全体

```python
def _phase159_render_foundational_reference_section(
  presentation: TodaGroupProofPresentation,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  entries = []
  index_by_key = {}
  seen_step_ids = set()

  def visit(
    proof_step: ProofStep,
  ) -> None:
    step_id = id(
      proof_step
    )

    if step_id in seen_step_ids:
      return

    seen_step_ids.add(
      step_id
    )

    identity = (
      proof_step.foundational_reference
    )

    if identity is not None:
      if not isinstance(
        identity,
        FoundationalReferenceIdentity,
      ):
        raise TypeError(
          "foundational_reference must be a "
          "FoundationalReferenceIdentity or None"
        )

      existing_index = (
        index_by_key.get(
          identity.key
        )
      )

      if existing_index is None:
        index_by_key[
          identity.key
        ] = len(
          entries
        )
        entries.append(
          [
            identity,
            [
              proof_step,
            ],
          ]
        )
      else:
        entries[
          existing_index
        ][
          1
        ].append(
          proof_step
        )

    for premise in proof_step.premises:
      if isinstance(
        premise,
        ProofStep,
      ):
        visit(
          premise
        )

  visit(
    presentation.root_step
  )

  if not entries:
    return ""

  lines = []

  for number, (
    identity,
    proof_steps,
  ) in enumerate(
    entries,
    start=1,
  ):
    lines.append(
      "**[F"
      + str(
        number
      )
      + "] "
      + identity.label
      + ".**"
    )

    seen_statements = set()

    for proof_step in proof_steps:
      statement = (
        _phase159_foundational_reference_statement(
          proof_step
        )
      )

      if statement in seen_statements:
        continue

      seen_statements.add(
        statement
      )
      lines.append(
        statement
      )

  return "\n".join(
    lines
  )
```

## `_phase159_inject_foundational_reference_section()` 全体

```python
def _phase159_inject_foundational_reference_section(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  foundational = (
    _phase159_render_foundational_reference_section(
      presentation
    )
  )

  if not foundational:
    return rendered

  reference_marker = (
    "## 使用する結果\n\n"
  )
  proof_boundary = (
    "---\n\n## 証明"
  )
  reference_start = rendered.find(
    reference_marker
  )

  if reference_start < 0:
    return rendered

  content_start = (
    reference_start
    + len(
      reference_marker
    )
  )
  boundary_index = rendered.find(
    proof_boundary,
    content_start,
  )

  if boundary_index < 0:
    return rendered

  existing = rendered[
    content_start:
    boundary_index
  ].strip()

  if existing:
    replacement = (
      existing
      + "\n\n"
      + foundational
    )
  else:
    replacement = foundational

  return (
    rendered[
      :content_start
    ]
    + replacement
    + "\n\n"
    + rendered[
      boundary_index:
    ]
  )
```

## 修正理由

1. `presentation.nodes` は selected proof depth のノードだけなので、
   depth 2 より深い foundational premise を拾えなかった。
2. root step から `ProofStep.premises` を再帰的にたどれば、
   実際に証明で使用された ancestry だけを取得できる。
3. Reference separator の検索文字列に余分な先頭改行があったため、
   foundational section が注入されなかった。

## 完了条件

- R1-6a focused tests 4件 PASS。
- Phase 159 focused tests PASS。
- Phase 49 / Phase 157 related tests PASS。
- `git diff --check` PASS。
- `使用する結果` に3つの `[F...]` が出る。
- target `pi_3^2=Z{eta_2}` と Proposition 5.1 は foundational Reference に出ない。

## 次 Phase との境界

- `[F1] より` などの proof-body linkage はまだ追加しない。
- literature boundary は変更しない。
- full pytest は Phase 159 最後のみ。
