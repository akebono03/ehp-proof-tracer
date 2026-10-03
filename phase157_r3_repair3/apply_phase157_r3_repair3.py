from pathlib import Path

TARGET = Path("toda_group_proof_narrative_contribution_renderer.py")

OLD_START = "def _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism("
OLD_END = "\ndef _phase157_r3_restore_pi6_3_earlier_prop56_reference("

REPLACEMENT = 'def _phase157_r3_find_recursive_proof_step_by_rule_name(\n  root_step: ProofStep,\n  rule_name: str,\n) -> ProofStep | None:\n  if not isinstance(root_step, ProofStep):\n    raise TypeError("root_step must be a ProofStep")\n  if not isinstance(rule_name, str):\n    raise TypeError("rule_name must be a str")\n\n  stack = [\n    root_step,\n  ]\n  visited_step_ids = set()\n\n  while stack:\n    current_step = stack.pop()\n    current_step_id = id(\n      current_step\n    )\n\n    if current_step_id in visited_step_ids:\n      continue\n\n    visited_step_ids.add(\n      current_step_id\n    )\n\n    inference_rule = current_step.inference_rule\n\n    if (\n      inference_rule is not None\n      and inference_rule.name == rule_name\n    ):\n      return current_step\n\n    stack.extend(\n      reversed(\n        current_step.premises\n      )\n    )\n\n  return None\n\n\ndef _phase157_r3_restore_pi6_3_proof_internal_suspension_isomorphism(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n  if not isinstance(markdown, str):\n    raise TypeError("markdown must be a str")\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n\n  if not (\n    target.group_dimension == 6\n    and target.sphere_dimension == 3\n    and presentation.max_depth >= 3\n  ):\n    return markdown\n\n  suspension_step = (\n    _phase157_r3_find_recursive_proof_step_by_rule_name(\n      presentation.root_step,\n      "Toda Proposition 5.3 n=3 suspension isomorphism",\n    )\n  )\n  hopf_step = (\n    _phase157_r3_find_recursive_proof_step_by_rule_name(\n      presentation.root_step,\n      "Toda Proposition 5.3 n=3 Hopf eta_5 surjectivity",\n    )\n  )\n\n  if suspension_step is None:\n    return markdown\n\n  suspension_line = _render_generic_narrative_step(\n    suspension_step\n  )\n\n  if not suspension_line:\n    return markdown\n\n  if suspension_line in markdown:\n    return markdown\n\n  if hopf_step is not None:\n    hopf_line = _render_generic_narrative_step(\n      hopf_step\n    )\n\n    if hopf_line:\n      hopf_index = markdown.find(\n        hopf_line\n      )\n\n      if hopf_index >= 0:\n        return (\n          markdown[:hopf_index]\n          + suspension_line\n          + "\\n\\n"\n          + markdown[hopf_index:]\n        )\n\n  final_group_marker = (\n    "最後に, $\\\\pi_{6}^{3}$ の群構造を決定するために"\n  )\n  final_group_index = markdown.find(\n    final_group_marker\n  )\n\n  if final_group_index >= 0:\n    return (\n      markdown[:final_group_index]\n      + suspension_line\n      + "\\n\\n"\n      + markdown[final_group_index:]\n    )\n\n  return (\n    markdown.rstrip()\n    + "\\n\\n"\n    + suspension_line\n  )\n\n\n'


def main():
    if not TARGET.exists():
        raise SystemExit(f"target not found: {TARGET}")

    text = TARGET.read_text(encoding="utf-8")

    start = text.find(OLD_START)
    if start < 0:
        raise SystemExit(
            "Phase157-R3 repair2 helper not found; "
            "repair3 must be applied after repair2."
        )

    end = text.find(OLD_END, start)
    if end < 0:
        raise SystemExit(
            "Phase157-R3 repair2 helper end anchor not found."
        )

    text = text[:start] + REPLACEMENT + text[end + 1:]
    TARGET.write_text(text, encoding="utf-8", newline="\n")

    print("Phase157-R3 repair3 changes applied.")
    print(f"updated: {TARGET.resolve()}")


if __name__ == "__main__":
    main()
