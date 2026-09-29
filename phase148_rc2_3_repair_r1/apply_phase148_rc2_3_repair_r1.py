from pathlib import Path

ROOT = Path.cwd()


def replace_once(path, old, new):
  text = path.read_text(encoding="utf-8")
  count = text.count(old)
  if count != 1:
    raise SystemExit(
      f"{path}: expected one replacement target, found {count}"
    )
  path.write_text(
    text.replace(old, new, 1),
    encoding="utf-8",
    newline="\n",
  )


def main():
  path = ROOT / "toda_group_proof_narrative_argument_body_renderer.py"

  old = '''  relocated_direct_premises = (
    ()
    if conclusion_step is None
    else (
      tuple(
        premise_step
        for premise_step in (
          _relocatable_toda_group_proof_narrative_direct_derivation_premises(
            (
              direct_derivation_support_steps
              + direct_derivation_premises
            ),
            step_derivation_sources_by_target_id,
            next(
              block
              for block in blocks
              if conclusion_step in block.steps
            ),
          )
        )
        if (
          id(
            premise_step
          ) not in redundant_direct_premise_step_ids
          and (
            excluded_non_exact_step_ids is None
            or id(
              premise_step
            ) not in excluded_non_exact_step_ids
          )
          and (
            context_hidden_step_ids is None
            or id(
              premise_step
            ) not in context_hidden_step_ids
          )
        )
      )
    )
  )
'''

  new = '''  unowned_recursive_exactness_step_ids = frozenset(
    id(
      proof_step
    )
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
      and exactness_exposure_by_block_id is not None
      and exactness_exposure_by_block_id.get(
        id(
          block
        )
      )
      is TodaGroupProofNarrativeExactnessExposureClass
      .UNOWNED_RECURSIVE
    )
    for proof_step in block.steps
  )
  relocated_direct_premises = (
    ()
    if conclusion_step is None
    else (
      tuple(
        premise_step
        for premise_step in (
          _relocatable_toda_group_proof_narrative_direct_derivation_premises(
            (
              direct_derivation_support_steps
              + direct_derivation_premises
            ),
            step_derivation_sources_by_target_id,
            next(
              block
              for block in blocks
              if conclusion_step in block.steps
            ),
          )
        )
        if (
          id(
            premise_step
          ) not in redundant_direct_premise_step_ids
          and id(
            premise_step
          ) not in unowned_recursive_exactness_step_ids
          and (
            excluded_non_exact_step_ids is None
            or id(
              premise_step
            ) not in excluded_non_exact_step_ids
          )
          and (
            context_hidden_step_ids is None
            or id(
              premise_step
            ) not in context_hidden_step_ids
          )
        )
      )
    )
  )
'''

  replace_once(path, old, new)

  print("RC2-3 Repair R1 applied.")
  print(
    "Changed only: "
    "render_toda_group_proof_narrative_argument_body_markdown"
  )
  print(
    "UNOWNED_RECURSIVE exactness steps no longer bypass "
    "exposure through direct-premise relocation."
  )
  print("RC3 ordering unchanged.")


if __name__ == "__main__":
  main()
