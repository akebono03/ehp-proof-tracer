# Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1 fix2

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

import の変更はありません。

変更関数:
- `merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows`

変更後の関数全体:

```python
def merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows(
  presentation: TodaGroupProofPresentation,
  markdown: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a TodaGroupProofPresentation"
    )

  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\n\n"
  )
  exactness_steps = tuple(
    node.proof_step
    for node in presentation.nodes
    if classify_toda_proof_step_role(
      node.proof_step
    )
    is TodaProofDependencyRole.EHP_EXACTNESS
  )

  for left_step in exactness_steps:
    left_window = getattr(
      left_step.conclusion,
      "window",
      None,
    )

    if left_window is None:
      continue

    for right_step in exactness_steps:
      if right_step is left_step:
        continue

      right_window = getattr(
        right_step.conclusion,
        "window",
        None,
      )

      if right_window is None:
        continue

      if not (
        left_window.middle_term
        == right_window.source_term
        and left_window.target_term
        == right_window.middle_term
        and _toda_group_proof_narrative_map_name_latex(
          left_window.second_map
        )
        == _toda_group_proof_narrative_map_name_latex(
          right_window.first_map
        )
      ):
        continue

      left_line = (
        _render_generic_narrative_step(
          left_step
        )
      )
      right_line = (
        _render_generic_narrative_step(
          right_step
        )
      )

      left_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if paragraph.strip()
          == left_line.strip()
        ),
        None,
      )
      right_index = next(
        (
          index
          for index, paragraph in enumerate(
            paragraphs
          )
          if paragraph.strip()
          == right_line.strip()
        ),
        None,
      )

      if (
        left_index is None
        or right_index is None
      ):
        continue

      first_map = (
        _toda_group_proof_narrative_map_name_latex(
          left_window.first_map
        )
      )
      second_map = (
        _toda_group_proof_narrative_map_name_latex(
          left_window.second_map
        )
      )
      third_map = (
        _toda_group_proof_narrative_map_name_latex(
          right_window.second_map
        )
      )

      if None in (
        first_map,
        second_map,
        third_map,
      ):
        continue

      bare_sequence = (
        "$"
        + render_toda_primary_group_latex(
          left_window.source_term
        )
        + r" \xrightarrow{"
        + first_map
        + "} "
        + render_toda_primary_group_latex(
          left_window.middle_term
        )
        + r" \xrightarrow{"
        + second_map
        + "} "
        + render_toda_primary_group_latex(
          left_window.target_term
        )
        + r" \xrightarrow{"
        + third_map
        + "} "
        + render_toda_primary_group_latex(
          right_window.target_term
        )
        + "$"
      )
      merged = (
        bare_sequence
        + " は完全である."
      )

      bare_indices = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if paragraph.strip().rstrip(
          "."
        )
        == bare_sequence
      )

      sequence_core = bare_sequence[
        1:
        -1
      ]
      sequence_arrow_count = (
        sequence_core.count(
          r"\xrightarrow{"
        )
      )
      longer_prefix_indices = tuple(
        index
        for index, paragraph in enumerate(
          paragraphs
        )
        if (
          paragraph.strip().startswith(
            "$"
            + sequence_core
          )
          and paragraph.count(
            r"\xrightarrow{"
          )
          > sequence_arrow_count
        )
      )

      removal_indices = {
        left_index,
        right_index,
      }
      removal_indices.update(
        bare_indices
      )

      if longer_prefix_indices:
        for index in sorted(
          removal_indices,
          reverse=True,
        ):
          paragraphs.pop(
            index
          )

        return "\n\n".join(
          paragraphs
        )

      introduction_index = (
        bare_indices[
          0
        ]
        if len(
          bare_indices
        ) == 1
        else None
      )

      if introduction_index is not None:
        insertion_index = (
          introduction_index
        )
      else:
        insertion_index = min(
          left_index,
          right_index,
        )

      for index in sorted(
        removal_indices,
        reverse=True,
      ):
        paragraphs.pop(
          index
        )

      removed_before_insertion = sum(
        1
        for index in removal_indices
        if index < insertion_index
      )
      insertion_index -= (
        removed_before_insertion
      )

      paragraphs.insert(
        insertion_index,
        merged,
      )

      return "\n\n".join(
        paragraphs
      )

  return markdown
```

テストファイルの変更はありません。

## 修正内容

repair1 の

```text
short sequence is contained anywhere in a longer sequence
```

という判定を、

```text
short sequence is a strict prefix of a longer sequence
```

へ狭める。

これにより、

- $\pi_3^2$ の先頭から重なる短い完全列は抑制する。
- $\pi_6^3$ の longer sequence 内部にある必要な exactness window は維持する。

## 完了条件

- $\pi_3^2$ focused regression が PASS。
- $\pi_6^3$ Phase157 repair32 regression が PASS。
- generator canonicalization regression が PASS。
- $\eta_2$ の文言は変更しない。
- full pytest は実行しない。

## 次 Phase との境界

この fix2 は exact-sequence duplicate suppression の判定範囲だけを修正する。
prose、Reference、stable 判定、generator 表記には触れない。
