from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parent.parent
SOURCE_ROOT = Path(__file__).resolve().parent


def replace_once(
  path: Path,
  old: str,
  new: str,
) -> None:
  text = path.read_text(
    encoding="utf-8"
  )

  count = text.count(
    old
  )

  if count != 1:
    raise RuntimeError(
      f"{path}: expected exactly one replacement anchor, found {count}"
    )

  path.write_text(
    text.replace(
      old,
      new,
      1,
    ),
    encoding="utf-8",
  )

  print(
    f"updated {path}"
  )


def main() -> None:
  body = (
    ROOT
    / "toda_group_proof_narrative_argument_body_renderer.py"
  )

  replace_once(
    body,
    """      _relocatable_toda_group_proof_narrative_direct_derivation_premises(
        direct_derivation_premises,
        step_derivation_sources_by_target_id,
        next(
          block
          for block in blocks
          if conclusion_step in block.steps
        ),
      )
""",
    """      tuple(
        premise_step
        for premise_step in (
          _relocatable_toda_group_proof_narrative_direct_derivation_premises(
            direct_derivation_premises,
            step_derivation_sources_by_target_id,
            next(
              block
              for block in blocks
              if conclusion_step in block.steps
            ),
          )
        )
        if id(
          premise_step
        ) not in redundant_direct_premise_step_ids
      )
""",
  )

  copies = (
    (
      SOURCE_ROOT
      / "tests"
      / "test_phase143_61b_direct_premise_narrative.py",
      ROOT
      / "tests"
      / "test_phase143_61b_direct_premise_narrative.py",
    ),
    (
      SOURCE_ROOT
      / "tests"
      / "test_phase143_61b_r_semantic_suppression_priority.py",
      ROOT
      / "tests"
      / "test_phase143_61b_r_semantic_suppression_priority.py",
    ),
  )

  for source, destination in copies:
    shutil.copyfile(
      source,
      destination,
    )
    print(
      f"updated {destination}"
    )


if __name__ == "__main__":
  main()
