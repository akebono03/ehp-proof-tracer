from pathlib import Path

ROOT = Path.cwd()
OLD_TEST = ROOT / "tests" / "test_phase150_rc4_4_reasons.py"
NEW_TEST = ROOT / "tests" / "test_phase150_rc4_5c_2_exactness_to_map_property.py"


def replace_once(text, old, new, path):
  count = text.count(old)
  if count != 1:
    raise RuntimeError(
      f"{path}: expected exactly one replacement target, found {count}"
    )
  return text.replace(old, new, 1)


def patch_old_test():
  path = OLD_TEST
  text = path.read_text(encoding="utf-8")

  old = '''  assert len(
    dependencies
  ) == 1
  assert len(
    reason_sidecar.reasons
  ) == 1

  dependency = dependencies[
    0
  ]
  reason = reason_sidecar.reasons[
    0
  ]

  assert (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  )
'''
  new = '''  assert len(
    dependencies
  ) == 1

  definition_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )
  assert len(
    definition_reasons
  ) == 1

  dependency = dependencies[
    0
  ]
  reason = definition_reasons[
    0
  ]

  assert (
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
  )
'''
  text = replace_once(text, old, new, path)

  old = '''  assert len(
    reason_sidecar.reasons
  ) == expected_count
  assert all(
    reason.kind
    is TodaGroupProofNarrativeReasonKind
    .DEFINITION_APPLICABILITY
    for reason in reason_sidecar.reasons
  )
'''
  new = '''  definition_reasons = tuple(
    reason
    for reason in reason_sidecar.reasons
    if (
      reason.kind
      is TodaGroupProofNarrativeReasonKind
      .DEFINITION_APPLICABILITY
    )
  )

  assert len(
    definition_reasons
  ) == expected_count
'''
  text = replace_once(text, old, new, path)

  path.write_text(text, encoding="utf-8")
  print("Patched:", path)


def patch_new_test():
  path = NEW_TEST
  text = path.read_text(encoding="utf-8")

  old = '''  conclusion = (
    "$E:\\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "
    "は単射である."
  )
'''
  new = '''  conclusion = (
    "$E: \\\\pi_{5}^{2} \\\\to \\\\pi_{6}^{3}$ "
    "は単射である."
  )
'''
  text = replace_once(text, old, new, path)

  path.write_text(text, encoding="utf-8")
  print("Patched:", path)


def main():
  patch_old_test()
  patch_new_test()
  print("RC4-5C-2-R1 test repair applied.")
  print("Production changes: none.")


if __name__ == "__main__":
  main()
