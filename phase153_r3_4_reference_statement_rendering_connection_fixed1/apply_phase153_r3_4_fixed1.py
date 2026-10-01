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


def main() -> int:
    renderer_path = (
        REPO_ROOT
        / "toda_group_proof_narrative_renderer.py"
    )

    old_import = r'''from toda_group_proof_narrative_contribution_renderer import (
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
'''

    new_import = r'''from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
)
'''

    _replace_once(
        renderer_path,
        old_import,
        new_import,
    )

    old_fallback_reference = r'''  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )
'''

    new_fallback_reference = r'''  statement_lines_by_reference_number = (
    _toda_group_proof_narrative_reference_statement_lines_by_number(
      presentation,
      reference_entries,
    )
    if reference_entries
    else {}
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
'''

    _replace_once(
        renderer_path,
        old_fallback_reference,
        new_fallback_reference,
    )

    print(
        "updated: toda_group_proof_narrative_renderer.py"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
