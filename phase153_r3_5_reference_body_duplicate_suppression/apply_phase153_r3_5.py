from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_ROOT.parent


def _replace_once(
    path: Path,
    old: str,
    new: str,
) -> None:
    text = path.read_text(
        encoding="utf-8",
    )
    count = text.count(
        old
    )
    if count != 1:
        raise RuntimeError(
            str(path.relative_to(REPO_ROOT))
            + ": expected exactly one replacement target, found "
            + str(count)
        )
    path.write_text(
        text.replace(
            old,
            new,
            1,
        ),
        encoding="utf-8",
    )


NEW_TEST = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_contribution_renderer import (
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _phase153_r3_5_pi10_6_narrative() -> str:
  report = build_standard_toda_report(
    n=6,
    k=4,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase153_r3_5_suppresses_exact_standalone_statement_line():
  body = (
    "まず、群構造を確認する。\n\n"
    "$E: A \\xrightarrow{\\cong} B$\n\n"
    "したがって結論を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          "$E: A \\xrightarrow{\\cong} B$",
        ),
      },
    )
  )

  assert "$E: A \\xrightarrow{\\cong} B$" not in suppressed
  assert "まず、群構造を確認する。" in suppressed
  assert "したがって結論を得る。" in suppressed


def test_phase153_r3_5_compacts_reference_marker_sentence():
  statement = "$E: A \\xrightarrow{\\cong} B$"
  body = (
    "また、[R2] により、"
    + statement
    + "を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          statement,
        ),
      },
    )
  )

  assert suppressed == "また、[R2]を用いる。"


def test_phase153_r3_5_does_not_suppress_similar_but_nonidentical_statement():
  selected = "$E: A \\xrightarrow{\\cong} B$"
  different = "$E^2: A \\xrightarrow{\\cong} B$"
  body = (
    "また、[R2] により、"
    + different
    + "を得る。"
  )

  suppressed = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      body,
      {
        2: (
          selected,
        ),
      },
    )
  )

  assert suppressed == body


def test_phase153_r3_5_public_pi10_6_keeps_statement_in_reference_and_suppresses_body_copy():
  rendered = (
    _phase153_r3_5_pi10_6_narrative()
  )

  reference_title = "**[R2] (4.5).**"
  proof_header = "## 証明"

  reference_start = rendered.index(
    reference_title
  )
  proof_start = rendered.index(
    proof_header
  )

  reference_part = rendered[
    reference_start:
    proof_start
  ]
  proof_part = rendered[
    proof_start:
  ]

  assert "同型" in reference_part or r"\cong" in reference_part
  assert "[R2]を用いる。" in proof_part
  assert "[R2] により、" not in proof_part
  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in rendered
  )
'''


UPDATED_R2_TEST = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def _phase153_r2_public_pi10_6_narrative() -> str:
  report = build_standard_toda_report(
    n=6,
    k=4,
  )
  group_result = (
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = (
    build_toda_group_proof_presentation(
      replay
    )
  )
  return (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )


def test_phase153_r2_public_pi10_6_keeps_reference_and_uses_toda45_fact_without_body_duplication():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R2] (4.5).**" in rendered
  assert "[R2]を用いる。" in rendered
  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in rendered
  )


def test_phase153_r2_public_pi10_6_keeps_provenance_only_reference_compact():
  rendered = (
    _phase153_r2_public_pi10_6_narrative()
  )

  assert "**[R1] Proposition 5.8.**" in rendered
  assert "Toda Proposition 5.8を用いる。" in rendered
  assert (
    "Toda Proposition 5.8 finite-dimensional integration"
    not in rendered
  )
'''


def main() -> int:
    contribution_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_contribution_renderer.py"
    )
    renderer_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_renderer.py"
    )
    r2_test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r2_public_reference_semantic_fact.py"
    )
    new_test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_5_reference_body_duplicate_suppression.py"
    )

    contribution_marker = r'''def render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
'''

    suppression_helper = r'''def suppress_toda_group_proof_narrative_reference_body_duplicates(
  body_markdown: str,
  statement_lines_by_reference_number: dict[
    int,
    tuple[
      str,
      ...,
    ],
  ],
) -> str:
  if not isinstance(
    body_markdown,
    str,
  ):
    raise TypeError(
      "body_markdown must be a str"
    )

  if not isinstance(
    statement_lines_by_reference_number,
    dict,
  ):
    raise TypeError(
      "statement_lines_by_reference_number must be a dict"
    )

  lines = body_markdown.splitlines()

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

    marker = (
      "[R"
      + str(
        reference_number
      )
      + "]"
    )

    for statement_line in statement_lines:
      if not isinstance(
        statement_line,
        str,
      ):
        raise TypeError(
          "statement_lines_by_reference_number values "
          "must contain only strings"
        )

      if not statement_line:
        continue

      updated_lines = []

      for line in lines:
        if statement_line not in line:
          updated_lines.append(
            line
          )
          continue

        if line.strip() == statement_line:
          continue

        if marker not in line:
          updated_lines.append(
            line
          )
          continue

        prefix = line.split(
          marker,
          1,
        )[0]

        updated_lines.append(
          prefix
          + marker
          + "を用いる。"
        )

      lines = updated_lines

  compacted_lines = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if is_blank and previous_blank:
      continue

    compacted_lines.append(
      line
    )
    previous_blank = is_blank

  return "\n".join(
    compacted_lines
  ).strip()


'''

    contribution_text = contribution_path.read_text(
        encoding="utf-8",
    )
    if contribution_text.count(
        contribution_marker
    ) != 1:
        raise RuntimeError(
            "contribution renderer marker not found exactly once"
        )
    contribution_text = contribution_text.replace(
        contribution_marker,
        suppression_helper + contribution_marker,
        1,
    )
    contribution_path.write_text(
        contribution_text,
        encoding="utf-8",
    )

    old_contribution_reference = r'''  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if not reference_section:
    return rendered

  return (
    reference_section
    + "\n\n"
    + rendered
  )
'''

    new_contribution_reference = r'''  rendered = (
    suppress_toda_group_proof_narrative_reference_body_duplicates(
      rendered,
      statement_lines_by_reference_number,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )

  if not reference_section:
    return rendered

  return (
    reference_section
    + "\n\n"
    + rendered
  )
'''

    _replace_once(
        contribution_path,
        old_contribution_reference,
        new_contribution_reference,
    )

    old_renderer_import = r'''from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
'''

    new_renderer_import = r'''from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
)
'''

    _replace_once(
        renderer_path,
        old_renderer_import,
        new_renderer_import,
    )

    old_final_return = r'''  return (
    "\n".join(
      lines
    )
    + "\n"
  )
'''

    new_final_return = r'''  rendered = (
    "\n".join(
      lines
    )
    + "\n"
  )

  if reference_section:
    proof_section_marker = "## 証明\n\n"
    proof_section_index = rendered.find(
      proof_section_marker
    )

    if proof_section_index >= 0:
      body_start = (
        proof_section_index
        + len(
          proof_section_marker
        )
      )
      body = rendered[
        body_start:
      ]
      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          body,
          statement_lines_by_reference_number,
        )
      )
      rendered = (
        rendered[
          :body_start
        ]
        + suppressed_body
        + "\n"
      )

  return rendered
'''

    renderer_text = renderer_path.read_text(
        encoding="utf-8",
    )
    final_occurrences = renderer_text.count(
        old_final_return
    )
    if final_occurrences < 1:
        raise RuntimeError(
            "fallback renderer return target not found"
        )
    target_index = renderer_text.rfind(
        old_final_return
    )
    renderer_text = (
        renderer_text[
          :target_index
        ]
        + new_final_return
        + renderer_text[
          target_index + len(
            old_final_return
          ):
        ]
    )
    renderer_path.write_text(
        renderer_text,
        encoding="utf-8",
    )

    r2_test_path.write_text(
        UPDATED_R2_TEST,
        encoding="utf-8",
    )
    new_test_path.write_text(
        NEW_TEST,
        encoding="utf-8",
    )

    print(
        "updated: toda_group_proof_narrative_contribution_renderer.py"
    )
    print(
        "updated: toda_group_proof_narrative_renderer.py"
    )
    print(
        "updated: tests\\test_phase153_r2_public_reference_semantic_fact.py"
    )
    print(
        "added: tests\\test_phase153_r3_5_reference_body_duplicate_suppression.py"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
