from pathlib import Path


TARGET = Path("toda_group_proof_narrative_contribution_ordering.py")

OLD = """def _group_key(
  occurrence: _ContributionOccurrence,
) -> tuple:
  return (
    type(occurrence.proof_step.conclusion),
    repr(occurrence.proof_step.conclusion),
    occurrence.provider_keys,
  )
"""

NEW = """def _group_key(
  occurrence: _ContributionOccurrence,
) -> tuple:
  rendered = _render_generic_narrative_step(
    occurrence.proof_step
  )
  return (
    type(
      occurrence.proof_step.conclusion
    ),
    _normalized(
      rendered
    ),
    occurrence.provider_keys,
  )
"""


def main() -> None:
  if not TARGET.is_file():
    raise FileNotFoundError(
      f"target production file not found: {TARGET}"
    )

  text = TARGET.read_text(
    encoding="utf-8-sig"
  )

  if NEW in text:
    print(
      "R25-11 production repair already applied."
    )
    return

  count = text.count(
    OLD
  )

  if count != 1:
    raise RuntimeError(
      "expected exactly one current recursive-repr "
      f"_group_key implementation, found {count}"
    )

  TARGET.write_text(
    text.replace(
      OLD,
      NEW,
      1,
    ),
    encoding="utf-8",
  )

  print(
    "R25-11 production repair applied."
  )
  print(
    "Changed only: "
    "toda_group_proof_narrative_contribution_ordering._group_key"
  )
  print(
    "Semantic closure, argument construction, "
    "connector assembly: unchanged."
  )


if __name__ == "__main__":
  main()
