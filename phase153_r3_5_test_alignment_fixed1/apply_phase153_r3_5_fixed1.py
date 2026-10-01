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
    test_path = (
        REPO_ROOT
        / "tests"
        / "test_phase153_r3_4_reference_statement_rendering_connection.py"
    )

    old_public_test = r'''def test_phase153_r3_4_public_pi10_6_reference_section_contains_r2_statement():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )

  reference_title = "**[R2] (4.5).**"
  title_index = rendered.index(
    reference_title
  )
  body_reference_index = rendered.index(
    "[R2] により、"
  )

  between = rendered[
    title_index
    + len(
      reference_title
    ):
    body_reference_index
  ]

  assert "同型" in between or r"\cong" in between
'''

    new_public_test = r'''def test_phase153_r3_4_public_pi10_6_reference_section_contains_r2_statement():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )

  reference_title = "**[R2] (4.5).**"
  title_index = rendered.index(
    reference_title
  )
  proof_section_index = rendered.index(
    "## 証明"
  )

  between = rendered[
    title_index
    + len(
      reference_title
    ):
    proof_section_index
  ]

  assert "同型" in between or r"\cong" in between
'''

    _replace_once(
        test_path,
        old_public_test,
        new_public_test,
    )

    old_fallback_test = r'''def test_phase153_r3_4_does_not_render_internal_fallback_name_in_reference_section():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )
  reference_section = rendered.split(
    "[R2] により、",
    1,
  )[0]

  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in reference_section
  )
'''

    new_fallback_test = r'''def test_phase153_r3_4_does_not_render_internal_fallback_name_in_reference_section():
  rendered = (
    render_toda_group_proof_narrative_markdown(
      _phase153_r3_4_pi10_6_presentation()
    )
  )
  reference_section = rendered.split(
    "## 証明",
    1,
  )[0]

  assert (
    "Toda 4.5 stable-range iterated suspension isomorphism"
    not in reference_section
  )
'''

    _replace_once(
        test_path,
        old_fallback_test,
        new_fallback_test,
    )

    print(
        "updated: tests\\test_phase153_r3_4_reference_statement_rendering_connection.py"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
