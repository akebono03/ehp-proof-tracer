from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent

RENDERER_PATH = (
  REPO_ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST_PATH = (
  REPO_ROOT
  / "tests"
  / "test_phase159_pi6_3_zero_map_reason_order.py"
)


def replace_function(
  source: str,
  start_marker: str,
  next_marker: str,
  replacement: str,
) -> str:
  start = source.find(
    start_marker
  )

  if start < 0:
    raise RuntimeError(
      "function start not found: "
      + start_marker
    )

  end = source.find(
    next_marker,
    start,
  )

  if end < 0:
    raise RuntimeError(
      "function end not found after: "
      + start_marker
    )

  return (
    source[
      :start
    ]
    + replacement.rstrip()
    + "\n\n"
    + source[
      end:
    ]
  )


def main() -> int:
  source = RENDERER_PATH.read_text(
    encoding="utf-8",
  )

  updated = replace_function(
    source,
    "def insert_toda_group_proof_narrative_hidden_zero_map_premises(\n",
    "def trim_toda_group_proof_narrative_redundant_left_ehp_terms(\n",
    'def insert_toda_group_proof_narrative_hidden_zero_map_premises(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def visible_index(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    target_key = match_key(\n      rendered\n    )\n    matches = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matches\n    ) != 1:\n      return None\n\n    return matches[\n      0\n    ]\n\n  def concise_map_property_reason(\n    proof_step: ProofStep,\n  ) -> str | None:\n    rendered = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered:\n      return None\n\n    concise = rendered\n\n    for verbose, short in (\n      (\n        " は単射である.",\n        " は単射.",\n      ),\n      (\n        " は全射である.",\n        " は全射.",\n      ),\n    ):\n      if concise.endswith(\n        verbose\n      ):\n        concise = (\n          concise[\n            :-len(\n              verbose\n            )\n          ]\n          + short\n        )\n        break\n\n    if concise == rendered:\n      return None\n\n    return (\n      "完全性より, "\n      + concise\n    )\n\n  def map_latex(\n    group_map,\n  ) -> str | None:\n    name = getattr(\n      group_map,\n      "name",\n      None,\n    )\n\n    if name is None:\n      return None\n\n    if name in (\n      "Δ",\n      "Delta",\n    ):\n      return r"\\Delta"\n\n    return str(\n      name\n    )\n\n  def exactness_reason(\n    zero_step: ProofStep,\n  ) -> str | None:\n    surjective_step = next(\n      (\n        premise\n        for premise in zero_step.premises\n        if (\n          classify_toda_proof_step_role(\n            premise\n          )\n          is TodaProofDependencyRole.MAP_PROPERTY\n          and "全射である."\n          in (\n            _render_generic_narrative_step(\n              premise\n            )\n            or ""\n          )\n        )\n      ),\n      None,\n    )\n\n    exactness_step = next(\n      (\n        premise\n        for premise in zero_step.premises\n        if classify_toda_proof_step_role(\n          premise\n        )\n        in (\n          TodaProofDependencyRole.EHP_EXACTNESS,\n          TodaProofDependencyRole.EHP_WINDOW,\n        )\n      ),\n      None,\n    )\n\n    if (\n      surjective_step is None\n      or exactness_step is None\n    ):\n      return None\n\n    window = getattr(\n      exactness_step.conclusion,\n      "window",\n      None,\n    )\n\n    if window is None:\n      return None\n\n    first_map = map_latex(\n      window.first_map\n    )\n    second_map = map_latex(\n      window.second_map\n    )\n\n    if (\n      first_map is None\n      or second_map is None\n    ):\n      return None\n\n    return (\n      "完全性より, "\n      r"$\\ker "\n      + second_map\n      + r"=\\operatorname{Im}"\n      + first_map\n      + "="\n      + render_toda_primary_group_latex(\n        window.middle_term\n      )\n      + "$ である."\n    )\n\n  candidate_zero_steps = []\n  seen_zero_step_ids = set()\n\n  for node in presentation.nodes:\n    for proof_step in (\n      node.proof_step,\n      *node.proof_step.premises,\n    ):\n      rendered = (\n        _render_generic_narrative_step(\n          proof_step\n        )\n      )\n\n      if (\n        not rendered\n        or "零写像である."\n        not in rendered\n      ):\n        continue\n\n      proof_step_id = id(\n        proof_step\n      )\n\n      if proof_step_id in seen_zero_step_ids:\n        continue\n\n      seen_zero_step_ids.add(\n        proof_step_id\n      )\n      candidate_zero_steps.append(\n        proof_step\n      )\n\n  for zero_step in candidate_zero_steps:\n    zero_line = (\n      _render_generic_narrative_step(\n        zero_step\n      )\n    )\n\n    if not zero_line:\n      continue\n\n    zero_index = visible_index(\n      zero_step\n    )\n\n    if zero_index is None:\n      consumer_match = next(\n        (\n          (\n            node.proof_step,\n            visible_index(\n              node.proof_step\n            ),\n          )\n          for node in presentation.nodes\n          if (\n            zero_step\n            in node.proof_step.premises\n            and visible_index(\n              node.proof_step\n            )\n            is not None\n          )\n        ),\n        None,\n      )\n\n      if consumer_match is None:\n        continue\n\n      (\n        consumer_step,\n        consumer_index,\n      ) = consumer_match\n      insertion_index = consumer_index\n\n      if insertion_index > 0:\n        previous = paragraphs[\n          insertion_index - 1\n        ]\n        concise_reason = (\n          concise_map_property_reason(\n            consumer_step\n          )\n        )\n\n        if (\n          "零写像"\n          in previous\n          or "Δ=0"\n          in previous\n          or r"\\Delta=0"\n          in previous\n          or (\n            r"\\ker E"\n            in previous\n            and r"\\operatorname{Im}"\n            in previous\n          )\n          or (\n            concise_reason is not None\n            and previous.strip()\n            == concise_reason\n          )\n        ):\n          insertion_index -= 1\n\n      paragraphs.insert(\n        insertion_index,\n        zero_line,\n      )\n      zero_index = insertion_index\n\n    reason = exactness_reason(\n      zero_step\n    )\n\n    if reason is None:\n      continue\n\n    if any(\n      paragraph.strip()\n      == reason\n      for paragraph in paragraphs\n    ):\n      continue\n\n    zero_index = next(\n      (\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if match_key(\n          paragraph\n        )\n        == match_key(\n          zero_line\n        )\n      ),\n      zero_index,\n    )\n\n    paragraphs.insert(\n      zero_index,\n      reason,\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n',
  )

  RENDERER_PATH.write_text(
    updated,
    encoding="utf-8",
  )

  TEST_PATH.write_text(
    (
      Path(__file__).resolve().parent
      / "test_phase159_pi6_3_zero_map_reason_order.py"
    ).read_text(
      encoding="utf-8",
    ),
    encoding="utf-8",
  )

  print(
    "Phase 159 pi6_3 zero-map reason-order repair7 applied."
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
