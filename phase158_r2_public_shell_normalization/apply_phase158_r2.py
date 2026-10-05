from __future__ import annotations

from pathlib import Path
import shutil


REPO_ROOT = Path(__file__).resolve().parent.parent
TARGET = REPO_ROOT / "toda_group_proof_narrative_renderer.py"
BACKUP_DIR = REPO_ROOT / "phase158_r2_backup_before_apply"


HELPER = r'''def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  title = "# Group proof narrative"
  target_header = "## 証明対象"
  reference_header = "## 使用する結果"
  proof_header = "## 証明"
  separator = "---"
  qed = "□"

  source_lines = rendered.rstrip().splitlines()

  if (
    source_lines
    and source_lines[0] == title
  ):
    content_lines = source_lines[1:]
  else:
    content_lines = source_lines[:]

  while (
    content_lines
    and not content_lines[0].strip()
  ):
    content_lines.pop(0)

  def marker_index(
    marker: str,
  ) -> int | None:
    try:
      return content_lines.index(
        marker
      )
    except ValueError:
      return None

  target_index = marker_index(
    target_header
  )
  reference_index = marker_index(
    reference_header
  )
  proof_index = marker_index(
    proof_header
  )

  target_body: list[str] = []

  if target_index is not None:
    target_end_candidates = [
      index
      for index in (
        reference_index,
        proof_index,
        len(
          content_lines
        ),
      )
      if (
        index is not None
        and index > target_index
      )
    ]
    target_end = min(
      target_end_candidates
    )
    target_body = content_lines[
      target_index + 1:
      target_end
    ]

  while (
    target_body
    and not target_body[0].strip()
  ):
    target_body.pop(0)

  while (
    target_body
    and not target_body[-1].strip()
  ):
    target_body.pop()

  if not target_body:
    root_latex = (
      _render_group_proof_narrative_latex(
        presentation.root_step
      )
    )

    if root_latex is not None:
      target_body = [
        r"\[",
        root_latex,
        r"\]",
        "",
        "を示す.",
      ]
    else:
      target_body = [
        (
          _render_group_proof_narrative_fact(
            presentation.root_step
          )
          + "を示す."
        ),
      ]

  reference_body: list[str] = []

  if (
    reference_index is not None
    and proof_index is not None
    and reference_index < proof_index
  ):
    reference_body = content_lines[
      reference_index + 1:
      proof_index
    ]

  while (
    reference_body
    and not reference_body[0].strip()
  ):
    reference_body.pop(0)

  while (
    reference_body
    and not reference_body[-1].strip()
  ):
    reference_body.pop()

  if (
    reference_body
    and reference_body[-1].strip()
    == separator
  ):
    reference_body.pop()

    while (
      reference_body
      and not reference_body[-1].strip()
    ):
      reference_body.pop()

  if proof_index is not None:
    proof_body = content_lines[
      proof_index + 1:
    ]
  elif (
    target_index is None
    and reference_index is None
  ):
    proof_body = content_lines[:]
  else:
    proof_body = []

  while (
    proof_body
    and not proof_body[0].strip()
  ):
    proof_body.pop(0)

  while (
    proof_body
    and not proof_body[-1].strip()
  ):
    proof_body.pop()

  if (
    proof_body
    and proof_body[-1].strip()
    == qed
  ):
    proof_body.pop()

    while (
      proof_body
      and not proof_body[-1].strip()
    ):
      proof_body.pop()

  lines = [
    title,
    "",
    target_header,
    "",
    *target_body,
    "",
    reference_header,
    "",
  ]

  if reference_body:
    lines.extend(
      (
        *reference_body,
        "",
      )
    )

  lines.extend(
    (
      separator,
      "",
      proof_header,
      "",
      *proof_body,
      "",
      qed,
    )
  )

  return (
    "\n".join(
      lines
    ).rstrip()
    + "\n"
  )


'''


NEW_RENDER = r'''def render_toda_group_proof_narrative_markdown(
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

  presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )

  phase134_24_pi15_8 = (
    _phase134_24_render_pi15_8_narrative(
      presentation
    )
  )

  if phase134_24_pi15_8 is not None:
    rendered = (
      _phase153_r3_10_connect_public_reference_section(
        presentation,
        phase134_24_pi15_8,
      )
    )

    return (
      _phase158_normalize_public_narrative_contract(
        presentation,
        rendered,
      )
    )

  if (
    _is_phase134_3_pi6_3_presentation(
      presentation
    )
    or _is_phase150_rc4_generic_route_target(
      presentation
    )
  ):
    semantic_sidecar = (
      build_toda_group_proof_narrative_semantic_sidecar(
        presentation
      )
    )
    blocks = (
      build_toda_group_proof_narrative_blocks(
        presentation,
        semantic_sidecar=semantic_sidecar,
      )
    )
    arguments = (
      build_toda_group_proof_narrative_arguments(
        presentation,
        blocks,
        semantic_sidecar=semantic_sidecar,
      )
    )

    rendered = (
      render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(
        presentation,
        blocks,
        semantic_sidecar,
        arguments,
      )
    )

    if _is_phase150_rc4_generic_route_target(
      presentation
    ):
      rendered = (
        _wrap_phase150_rc4_generic_public_narrative(
          presentation,
          rendered,
        )
      )

    return (
      _phase158_normalize_public_narrative_contract(
        presentation,
        rendered,
      )
    )

  if _is_phase134_9_pi8_5_presentation(
    presentation
  ):
    rendered = (
      _render_phase134_9_pi8_5_narrative_markdown(
        presentation
      )
    )
    rendered = (
      _phase153_r3_10_connect_public_reference_section(
        presentation,
        rendered,
      )
    )

    return (
      _phase158_normalize_public_narrative_contract(
        presentation,
        rendered,
      )
    )

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
    if presentation.max_depth >= 2
    else ()
  )
  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
    if reference_entries
    else {}
  )
  (
    reference_entries,
    statement_lines_by_reference_number,
  ) = (
    exclude_toda_group_proof_narrative_root_reference(
      reference_entries,
      statement_lines_by_reference_number,
      presentation.root_step,
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
  reference_marker_by_step_id = {
    id(proof_step): f"[R{entry.number}]"
    for entry in reference_entries
    for proof_step in entry.proof_steps
  }
  reference_reuse_marker_by_step_id = (
    build_toda_group_proof_narrative_reference_reuse_marker_by_step_id(
      presentation,
      reference_entries,
    )
  )

  lines = [
    "# Group proof narrative",
    "",
  ]

  if reference_section:
    lines.extend(
      (
        "## 使用する結果",
        "",
        reference_section,
        "",
        "## 証明",
        "",
      )
    )

  root_edges = (
    _narrative_edges_for_parent(
      presentation,
      presentation.root_step,
    )
  )

  if root_edges:
    target = (
      presentation
      .source_replay
      .group_result
      .target
    )

    if (
      target.group_dimension == 16
      and target.sphere_dimension == 9
    ):
      lines.extend(
        (
          (
            "$\\sigma_{9}$ の位数を確認し, "
            "これが $\\pi_{16}^{9}$ を生成することを示す。"
          ),
          "",
        )
      )

    _append_narrative_for_step(
      lines,
      presentation,
      presentation.root_step,
      set(),
      set(),
      reference_marker_by_step_id,
      reference_reuse_marker_by_step_id,
    )

    lines.extend(
      (
        "",
        (
          "したがって, "
          + _render_group_proof_narrative_fact(
            presentation.root_step
          )
          + "を得る."
        ),
      )
    )
  else:
    lines.append(
      (
        "したがって, "
        + _render_group_proof_narrative_fact(
          presentation.root_step
        )
        + "である."
      )
    )

  rendered = (
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
        suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry(
          presentation,
          body,
          reference_entries,
        )
      )
      suppressed_body = (
        suppress_toda_group_proof_narrative_reference_body_duplicates(
          suppressed_body,
          statement_lines_by_reference_number,
        )
      )
      suppressed_body = (
        link_toda_group_proof_narrative_reference_body_consumers(
          presentation,
          suppressed_body,
          reference_entries,
        )
      )
      (
        filtered_reference_entries,
        filtered_statement_lines,
        suppressed_body,
      ) = (
        filter_toda_group_proof_narrative_reference_entries_by_body_usage(
          reference_entries,
          statement_lines_by_reference_number,
          suppressed_body,
        )
      )
      filtered_reference_section = (
        render_toda_group_proof_narrative_reference_entries_markdown(
          filtered_reference_entries,
          filtered_statement_lines,
        )
      )
      prefix_lines = [
        "# Group proof narrative",
        "",
      ]

      if filtered_reference_section:
        prefix_lines.extend(
          (
            "## 使用する結果",
            "",
            filtered_reference_section,
            "",
            "## 証明",
            "",
          )
        )

      rendered = (
        "\n".join(
          prefix_lines
        )
        + "\n"
        + suppressed_body
        + "\n"
      )

  return (
    _phase158_normalize_public_narrative_contract(
      presentation,
      rendered,
    )
  )
'''


def main() -> int:
    source = TARGET.read_text(
        encoding="utf-8",
    )

    marker = (
        "def render_toda_group_proof_narrative_markdown(\n"
    )
    index = source.find(
        marker
    )

    if index < 0:
        raise RuntimeError(
            "render_toda_group_proof_narrative_markdown "
            "was not found"
        )

    if (
        "def _phase158_normalize_public_narrative_contract("
        in source
    ):
        print(
            "Phase 158-R2 already appears to be applied."
        )
        return 0

    BACKUP_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    backup = (
        BACKUP_DIR
        / TARGET.name
    )

    if not backup.exists():
        shutil.copy2(
            TARGET,
            backup,
        )

    replacement = (
        source[:index]
        + HELPER
        + NEW_RENDER
        + "\n"
    )

    TARGET.write_text(
        replacement,
        encoding="utf-8",
    )

    print(
        "Phase 158-R2 applied."
    )
    print(
        f"Backup: {backup}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
