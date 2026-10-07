# Phase 159 R1-7c R4 exact-sequence subsequence suppression repair2

## 変更対象

### `toda_group_proof_narrative_contribution_renderer.py`

import の変更はありません。

変更関数:
- `merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows`
- `render_toda_group_proof_narrative_multi_argument_with_contributions_markdown`

新規関数:
- `suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements`
- 追加位置: public contribution renderer の直前。

### 復帰後の merge 関数全体

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

      introduction_index = (
        bare_indices[
          0
        ]
        if len(
          bare_indices
        ) == 1
        else None
      )

      removal_indices = {
        left_index,
        right_index,
      }

      if introduction_index is not None:
        removal_indices.add(
          introduction_index
        )
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

### 新規 helper 全体

```python
def suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  retained = []
  prior_sequence_cores = []

  for paragraph in markdown.split(
    "\n\n"
  ):
    stripped = paragraph.strip()

    if (
      not stripped.startswith(
        "$"
      )
      or r"\xrightarrow{"
      not in stripped
    ):
      retained.append(
        paragraph
      )
      continue

    closing_math_index = stripped.find(
      "$",
      1,
    )

    if closing_math_index < 0:
      retained.append(
        paragraph
      )
      continue

    sequence_core = stripped[
      1:
      closing_math_index
    ]
    arrow_count = sequence_core.count(
      r"\xrightarrow{"
    )

    if arrow_count < 1:
      retained.append(
        paragraph
      )
      continue

    is_late_prefix_restatement = any(
      prior_core.startswith(
        sequence_core
      )
      and prior_core != sequence_core
      and prior_core.count(
        r"\xrightarrow{"
      ) > arrow_count
      for prior_core in prior_sequence_cores
    )

    if is_late_prefix_restatement:
      continue

    prior_sequence_cores.append(
      sequence_core
    )
    retained.append(
      paragraph
    )

  return "\n\n".join(
    retained
  )
```

### 新規テスト全文

```python
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements,
)


def test_phase159_r1_7c_r4_late_shorter_prefix_is_suppressed():
  longer = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$."
  )
  shorter = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$."
  )
  markdown = (
    longer
    + "\n\n"
    + r"$\pi_{2}^{1}=0$."
    + "\n\n"
    + shorter
  )

  rendered = (
    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
      markdown
    )
  )

  assert longer in rendered
  assert shorter not in rendered


def test_phase159_r1_7c_r4_earlier_shorter_exactness_is_preserved():
  shorter = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3}$ は完全である."
  )
  longer = (
    r"$\pi_{7}^{3} \xrightarrow{H} "
    r"\pi_{7}^{5} \xrightarrow{\Delta} "
    r"\pi_{5}^{2} \xrightarrow{E} "
    r"\pi_{6}^{3} \xrightarrow{H} "
    r"\pi_{6}^{5}$."
  )
  markdown = (
    shorter
    + "\n\n"
    + longer
  )

  rendered = (
    suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements(
      markdown
    )
  )

  assert shorter in rendered
  assert longer in rendered
```

## 一般規則

すでに前方に長い完全列を表示済みで、その後に同じ始点からの strict prefix
（真の接頭部分列）が現れた場合だけ、後者を重複として抑制する。

逆順、すなわち短い exactness statement が先で、長い列が後なら抑制しない。

## 完了条件

- helper contract 2 tests PASS。
- $\pi_3^2$ focused regression PASS。
- $\pi_6^3$ existing repair32 regression PASS。
- generator canonicalization regression PASS。
- $\eta_2$ wording unchanged。
- full pytest は実行しない。
