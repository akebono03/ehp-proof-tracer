from pathlib import Path

RENDERER = Path("toda_group_proof_narrative_renderer.py")
MULTI = Path("toda_group_proof_narrative_argument_multi_renderer.py")
CONTRIB = Path("toda_group_proof_narrative_contribution_renderer.py")


def replace_once(text, old, new, label):
    if old not in text:
        if new in text:
            print(label + ": already applied")
            return text
        raise RuntimeError("target not found: " + label)
    print(label + ": applied")
    return text.replace(old, new, 1)


def patch_renderer():
    text = RENDERER.read_text(encoding="utf-8")

    old = """    premise_reference_marker = (
      None
      if reference_marker_by_step_id is None
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
"""
    new = """    premise_reference_marker = (
      None
      if (
        reference_marker_by_step_id is None
        or isinstance(
          premise_step.conclusion,
          TodaProp42ExactnessStatement,
        )
      )
      else reference_marker_by_step_id.get(
        premise_id
      )
    )
"""
    text = replace_once(
        text,
        old,
        new,
        "preserve exactness mathematical content",
    )
    RENDERER.write_text(text, encoding="utf-8")


def patch_multi_renderer():
    text = MULTI.read_text(encoding="utf-8")

    old_import = """from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
"""
    text = replace_once(
        text,
        old_import,
        "",
        "remove low-level Reference imports",
    )

    old_tail = """  rendered = "\\n\\n".join(
    rendered_arguments
  )

  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )

  parts = tuple(
    part
    for part in (
      reference_section,
      "\\n\\n".join(
        rendered_arguments
      ),
    )
    if part
  )

  return number_toda_group_proof_narrative_equations(
    "\\n\\n".join(
      parts
    ),
    presentation,
    blocks,
  )
"""
    new_tail = """  rendered = "\\n\\n".join(
    rendered_arguments
  )

  return number_toda_group_proof_narrative_equations(
    rendered,
    presentation,
    blocks,
  )
"""
    text = replace_once(
        text,
        old_tail,
        new_tail,
        "restore low-level multi-Argument return contract",
    )
    MULTI.write_text(text, encoding="utf-8")


def patch_contribution_renderer():
    text = CONTRIB.read_text(encoding="utf-8")

    anchor = """from toda_group_proof_narrative_reasons import (
  build_toda_group_proof_narrative_reason_sidecar,
)
"""
    addition = """from toda_group_proof_narrative_references import (
  build_toda_group_proof_narrative_reference_entries,
  render_toda_group_proof_narrative_reference_entries_markdown,
)
"""
    if addition not in text:
        if anchor not in text:
            raise RuntimeError(
                "target not found: contribution renderer import insertion"
            )
        text = text.replace(
            anchor,
            anchor + addition,
            1,
        )
        print("add contribution-layer Reference imports: applied")
    else:
        print("add contribution-layer Reference imports: already applied")

    old_return = """  return insert_toda_group_proof_narrative_reason_prose(
    contribution_markdown,
    reason_sidecar,
  )
"""
    new_return = """  rendered = (
    insert_toda_group_proof_narrative_reason_prose(
      contribution_markdown,
      reason_sidecar,
    )
  )
  reference_entries = (
    build_toda_group_proof_narrative_reference_entries(
      presentation
    )
  )
  reference_section = (
    render_toda_group_proof_narrative_reference_entries_markdown(
      reference_entries
    )
  )

  if not reference_section:
    return rendered

  return (
    reference_section
    + "\\n\\n"
    + rendered
  )
"""
    text = replace_once(
        text,
        old_return,
        new_return,
        "move Reference section to public contribution layer",
    )
    CONTRIB.write_text(text, encoding="utf-8")


def main():
    patch_renderer()
    patch_multi_renderer()
    patch_contribution_renderer()
    print("RC4-7A regression repair R1 applied.")


if __name__ == "__main__":
    main()
