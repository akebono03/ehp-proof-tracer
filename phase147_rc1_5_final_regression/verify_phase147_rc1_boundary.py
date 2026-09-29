from pathlib import Path


def main():
  selection_path = Path(
    "toda_group_proof_narrative_exactness_selection.py"
  )
  multi_path = Path(
    "toda_group_proof_narrative_argument_multi_renderer.py"
  )

  selection_source = selection_path.read_text(
    encoding="utf-8"
  )
  multi_source = multi_path.read_text(
    encoding="utf-8"
  )

  ownership_name = (
    "select_toda_group_proof_narrative_"
    "argument_primary_exactness_component"
  )
  legacy_name = (
    "select_toda_group_proof_narrative_"
    "primary_exactness_component"
  )

  assert (
    f"def {ownership_name}("
    in selection_source
  ), "RC1 ownership API is missing"

  assert (
    ownership_name
    in multi_source
  ), "multi renderer does not use the RC1 ownership API"

  assert (
    f"{legacy_name}("
    not in multi_source
  ), (
    "multi renderer still performs the old inline "
    "primary-method selection"
  )

  assert (
    "extract_toda_group_proof_narrative_argument_method_evidence("
    in multi_source
  ), (
    "RC1 must not remove method evidence still required "
    "by body/evidence handling"
  )

  print("RC1 boundary verification: PASS")
  print(
    "  Argument -> primary exactness ownership API: present"
  )
  print(
    "  Multi renderer old inline primary selection: absent"
  )
  print(
    "  Method evidence for body handling: preserved"
  )
  print(
    "  RC2 evidence exposure behavior: intentionally unchanged"
  )
  print(
    "  RC3 contribution ordering behavior: intentionally unchanged"
  )


if __name__ == "__main__":
  main()
