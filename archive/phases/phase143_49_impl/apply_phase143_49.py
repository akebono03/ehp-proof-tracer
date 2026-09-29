from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8",
  )

  if old not in text:
    raise RuntimeError(
      f"expected source block not found in {path}"
    )

  updated = text.replace(
    old,
    new,
    1,
  )
  path.write_text(
    updated,
    encoding="utf-8",
  )
  print(
    f"updated {path}"
  )


def main() -> None:
  generic_path = (
    ROOT
    / "toda_group_proof_generic_narrative_renderer.py"
  )
  body_path = (
    ROOT
    / "toda_group_proof_narrative_argument_body_renderer.py"
  )

  old_generic = """def _render_generic_narrative_proof_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
) -> tuple[
  str,
  ...,
]:
  block = blocks[
    block_index
  ]
  dependency_labels = (
    _generic_narrative_dependency_labels(
      presentation,
      blocks,
      block_index,
    )
  )
  sentence_lead = (
    _generic_narrative_sentence_lead(
      block.role,
      dependency_labels,
    )
  )

  lines = []

  if sentence_lead:
    lines.append(
      sentence_lead
    )
    lines.append(
      ""
    )

  for proof_step in block.steps:
    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )

    short_exact_sequence_latex = (
      _generic_short_exact_sequence_latex(
        presentation,
        proof_step,
      )
    )

    if short_exact_sequence_latex is not None:
      lines.append(
        "この完全性と両端の写像の性質より, "
        "次の短完全列を得る."
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + short_exact_sequence_latex
        + "$"
      )
      lines.append(
        ""
      )

  return tuple(
    lines
  )
"""

  new_generic = """def _render_generic_narrative_proof_block(
  presentation: TodaGroupProofPresentation,
  blocks: tuple[
    TodaGroupProofNarrativeBlock,
    ...,
  ],
  block_index: int,
  show_dependency_labels: bool = True,
) -> tuple[
  str,
  ...,
]:
  if not isinstance(
    show_dependency_labels,
    bool,
  ):
    raise TypeError(
      "show_dependency_labels must be a bool"
    )

  block = blocks[
    block_index
  ]

  if show_dependency_labels:
    dependency_labels = (
      _generic_narrative_dependency_labels(
        presentation,
        blocks,
        block_index,
      )
    )
  else:
    dependency_labels = ()

  sentence_lead = (
    _generic_narrative_sentence_lead(
      block.role,
      dependency_labels,
    )
  )

  lines = []

  if sentence_lead:
    lines.append(
      sentence_lead
    )
    lines.append(
      ""
    )

  for proof_step in block.steps:
    lines.append(
      _render_generic_narrative_step(
        proof_step
      )
    )
    lines.append(
      ""
    )

    short_exact_sequence_latex = (
      _generic_short_exact_sequence_latex(
        presentation,
        proof_step,
      )
    )

    if short_exact_sequence_latex is not None:
      lines.append(
        "この完全性と両端の写像の性質より, "
        "次の短完全列を得る."
      )
      lines.append(
        ""
      )
      lines.append(
        "$"
        + short_exact_sequence_latex
        + "$"
      )
      lines.append(
        ""
      )

  return tuple(
    lines
  )
"""

  replace_once(
    generic_path,
    old_generic,
    new_generic,
  )

  old_exactness = """    dependency_labels = (
      _generic_narrative_dependency_labels(
        presentation,
        blocks,
        block_index,
      )
    )
    sentence_lead = (
      _generic_narrative_sentence_lead(
        block.role,
        dependency_labels,
      )
    )
"""

  new_exactness = """    sentence_lead = (
      _generic_narrative_sentence_lead(
        block.role,
        (),
      )
    )
"""

  replace_once(
    body_path,
    old_exactness,
    new_exactness,
  )

  old_generic_call = """    lines.extend(
      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
      )
    )
"""

  new_generic_call = """    lines.extend(
      _render_generic_narrative_proof_block(
        presentation,
        blocks,
        block_index,
        show_dependency_labels=False,
      )
    )
"""

  replace_once(
    body_path,
    old_generic_call,
    new_generic_call,
  )

  test_source = (
    Path(__file__).resolve().parent
    / "tests"
    / "test_phase143_49_dependency_label_narrative_policy.py"
  )
  test_destination = (
    ROOT
    / "tests"
    / "test_phase143_49_dependency_label_narrative_policy.py"
  )
  test_destination.write_text(
    test_source.read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )
  print(
    f"copied {test_source} -> {test_destination}"
  )


if __name__ == "__main__":
  main()
