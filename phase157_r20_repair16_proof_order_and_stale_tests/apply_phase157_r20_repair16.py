from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()

RENDERER = ROOT / "toda_group_proof_narrative_contribution_renderer.py"
PHASE157_TEST = ROOT / "tests" / "test_phase157_r19_pi6_3_reference_dependency_restoration.py"
PHASE156_TEST = ROOT / "tests" / "test_phase156_r5_repair11_reference_dependency_pruning.py"
NEW_TEST = ROOT / "tests" / "test_phase157_r20_repair16_proof_order_and_cleanup.py"

BRIDGE_FUNCTION = 'def insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  for node in presentation.nodes:\n    definition_steps = tuple(\n      premise\n      for premise in node.proof_step.premises\n      if type(\n        premise.conclusion\n      ).__name__\n      == "TodaEtaFamilyDefinitionStatement"\n    )\n\n    if len(\n      definition_steps\n    ) < 2:\n      continue\n\n    ordered = tuple(\n      sorted(\n        definition_steps,\n        key=lambda step: (\n          step.conclusion.index\n        ),\n      )\n    )\n\n    for lower_step, upper_step in zip(\n      ordered,\n      ordered[\n        1:\n      ],\n    ):\n      lower = lower_step.conclusion\n      upper = upper_step.conclusion\n\n      if (\n        not isinstance(\n          lower.index,\n          int,\n        )\n        or isinstance(\n          lower.index,\n          bool,\n        )\n        or not isinstance(\n          upper.index,\n          int,\n        )\n        or isinstance(\n          upper.index,\n          bool,\n        )\n        or upper.index\n        != lower.index + 1\n      ):\n        continue\n\n      bridge = (\n        "$"\n        + render_toda_expression_latex(\n          upper.element\n        )\n        + "=E"\n        + render_toda_expression_latex(\n          lower.element\n        )\n        + "$ である."\n      )\n\n      bridge_key = match_key(\n        bridge\n      )\n\n      if any(\n        match_key(\n          paragraph\n        )\n        == bridge_key\n        for paragraph in paragraphs\n      ):\n        continue\n\n      upper_rendered = (\n        _render_generic_narrative_step(\n          upper_step\n        )\n      )\n\n      if not upper_rendered:\n        continue\n\n      upper_key = match_key(\n        upper_rendered\n      )\n      upper_indices = tuple(\n        index\n        for index, paragraph in enumerate(\n          paragraphs\n        )\n        if match_key(\n          paragraph\n        )\n        == upper_key\n      )\n\n      if len(\n        upper_indices\n      ) != 1:\n        continue\n\n      paragraphs.insert(\n        upper_indices[\n          0\n        ],\n        bridge,\n      )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
REFLEXIVE_FUNCTION = 'def suppress_toda_group_proof_narrative_reflexive_equalities(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  reflexive_keys = set()\n\n  for node in presentation.nodes:\n    statement = node.proof_step.conclusion\n\n    if (\n      not isinstance(\n        statement,\n        Relation,\n      )\n      or statement.relation_type\n      is not RelationType.EQUALITY\n      or statement.lhs != statement.rhs\n    ):\n      continue\n\n    rendered = (\n      _render_generic_narrative_step(\n        node.proof_step\n      )\n    )\n\n    if not rendered:\n      continue\n\n    reflexive_keys.add(\n      _phase157_r11_reference_statement_match_key(\n        rendered\n      )\n    )\n\n  if not reflexive_keys:\n    return markdown\n\n  retained = []\n\n  for paragraph in markdown.split(\n    "\\n\\n"\n  ):\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    key = (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n    if key in reflexive_keys:\n      continue\n\n    retained.append(\n      paragraph\n    )\n\n  return "\\n\\n".join(\n    retained\n  )\n'
ORDER_FUNCTION = 'def order_toda_group_proof_narrative_surjectivity_support(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n  statement_lines_by_reference_number=None,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  if statement_lines_by_reference_number is None:\n    statement_lines_by_reference_number = {}\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def strip_reference_prefix(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if not stripped.startswith(\n      "[R"\n    ):\n      return stripped\n\n    marker_end = stripped.find(\n      "]"\n    )\n\n    if marker_end < 0:\n      return stripped\n\n    suffix = stripped[\n      marker_end + 1:\n    ]\n\n    for prefix in (\n      "より, ",\n      "を用いて, ",\n    ):\n      if suffix.startswith(\n        prefix\n      ):\n        return suffix[\n          len(\n            prefix\n          ):\n        ]\n\n    return stripped\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    return (\n      _phase157_r11_reference_statement_match_key(\n        strip_reference_prefix(\n          paragraph\n        )\n      )\n    )\n\n  def paragraph_index_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered_statement = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered_statement:\n      return None\n\n    target_key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered_statement\n      )\n    )\n\n    matching_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      )\n      == target_key\n    )\n\n    if len(\n      matching_indices\n    ) != 1:\n      return None\n\n    return matching_indices[\n      0\n    ]\n\n  for node in presentation.nodes:\n    map_step = node.proof_step\n\n    if (\n      classify_toda_proof_step_role(\n        map_step\n      )\n      is not TodaProofDependencyRole.MAP_PROPERTY\n    ):\n      continue\n\n    map_index = paragraph_index_for_step(\n      map_step\n    )\n\n    if map_index is None:\n      continue\n\n    equality_premises = tuple(\n      premise\n      for premise in map_step.premises\n      if (\n        isinstance(\n          premise.conclusion,\n          Relation,\n        )\n        and premise.conclusion.relation_type\n        is RelationType.EQUALITY\n      )\n    )\n\n    support_steps = []\n\n    for equality_premise in equality_premises:\n      support_steps.extend(\n        premise\n        for premise in equality_premise.premises\n        if (\n          isinstance(\n            premise.conclusion,\n            Relation,\n          )\n          and premise.conclusion.relation_type\n          is RelationType.EQUALITY\n        )\n      )\n      support_steps.append(\n        equality_premise\n      )\n\n    support_indices = tuple(\n      index\n      for proof_step in support_steps\n      for index in (\n        paragraph_index_for_step(\n          proof_step\n        ),\n      )\n      if index is not None\n    )\n\n    if (\n      support_steps\n      and len(\n        support_indices\n      ) == len(\n        support_steps\n      )\n    ):\n      first_support_index = min(\n        support_indices\n      )\n      last_support_index = max(\n        support_indices\n      )\n\n      if not (\n        first_support_index < map_index\n        and last_support_index < map_index\n      ):\n        support_block = paragraphs[\n          first_support_index:\n          last_support_index + 1\n        ]\n\n        del paragraphs[\n          first_support_index:\n          last_support_index + 1\n        ]\n\n        map_index = paragraph_index_for_step(\n          map_step\n        )\n\n        if map_index is not None:\n          paragraphs[\n            map_index:\n            map_index\n          ] = support_block\n\n  for map_index, paragraph in enumerate(\n    tuple(\n      paragraphs\n    )\n  ):\n    map_paragraph = strip_reference_prefix(\n      paragraph\n    )\n\n    if (\n      not map_paragraph.startswith(\n        "$H:"\n      )\n      or " は全射である." not in map_paragraph\n      or r"\\to " not in map_paragraph\n    ):\n      continue\n\n    if paragraph.strip() != map_paragraph:\n      paragraphs[\n        map_index\n      ] = map_paragraph\n\n    target_fragment = map_paragraph.split(\n      r"\\to ",\n      1,\n    )[1].split(\n      "$",\n      1,\n    )[0].strip()\n\n    group_prefix = (\n      "$"\n      + target_fragment\n      + " = "\n    )\n\n    existing_group_index = next(\n      (\n        index\n        for index, candidate in enumerate(\n          paragraphs\n        )\n        if (\n          index != map_index\n          and strip_reference_prefix(\n            candidate\n          ).startswith(\n            group_prefix\n          )\n        )\n      ),\n      None,\n    )\n\n    if existing_group_index is not None:\n      if existing_group_index > map_index:\n        group_paragraph = paragraphs.pop(\n          existing_group_index\n        )\n        paragraphs.insert(\n          map_index,\n          group_paragraph,\n        )\n    else:\n      reference_matches = []\n\n      for entry in reference_entries:\n        lines = (\n          statement_lines_by_reference_number.get(\n            entry.number,\n            (),\n          )\n        )\n\n        for line in lines:\n          normalized_line = line.strip()\n\n          if not normalized_line.startswith(\n            group_prefix\n          ):\n            continue\n\n          reference_matches.append(\n            (\n              entry.number,\n              normalized_line,\n            )\n          )\n\n      unique_matches = tuple(\n        dict.fromkeys(\n          reference_matches\n        )\n      )\n\n      if len(\n        unique_matches\n      ) == 1:\n        reference_number, statement_line = (\n          unique_matches[\n            0\n          ]\n        )\n        support_paragraph = (\n          "[R"\n          + str(\n            reference_number\n          )\n          + "]より, "\n          + statement_line\n        )\n\n        if support_paragraph not in paragraphs:\n          paragraphs.insert(\n            map_index,\n            support_paragraph,\n          )\n\n    map_index = next(\n      (\n        index\n        for index, candidate in enumerate(\n          paragraphs\n        )\n        if strip_reference_prefix(\n          candidate\n        )\n        == map_paragraph\n      ),\n      None,\n    )\n\n    if map_index is None:\n      continue\n\n    kernel_index = next(\n      (\n        index\n        for index, candidate in enumerate(\n          paragraphs\n        )\n        if (\n          r"\\ker \\Delta"\n          in candidate\n          and r"\\operatorname{Im}H"\n          in candidate\n          and target_fragment\n          in candidate\n        )\n      ),\n      None,\n    )\n\n    if kernel_index is None:\n      continue\n\n    exactness_index = next(\n      (\n        index\n        for index in range(\n          map_index + 1,\n          len(\n            paragraphs\n          ),\n        )\n        if (\n          target_fragment\n          in paragraphs[\n            index\n          ]\n          and "は完全である."\n          in paragraphs[\n            index\n          ]\n        )\n      ),\n      None,\n    )\n\n    kernel_paragraph = paragraphs.pop(\n      kernel_index\n    )\n\n    map_index = next(\n      (\n        index\n        for index, candidate in enumerate(\n          paragraphs\n        )\n        if strip_reference_prefix(\n          candidate\n        )\n        == map_paragraph\n      ),\n      None,\n    )\n\n    if map_index is None:\n      paragraphs.append(\n        kernel_paragraph\n      )\n      continue\n\n    if exactness_index is not None:\n      exactness_index = next(\n        (\n          index\n          for index in range(\n            map_index + 1,\n            len(\n              paragraphs\n            ),\n          )\n          if (\n            target_fragment\n            in paragraphs[\n              index\n            ]\n            and "は完全である."\n            in paragraphs[\n              index\n            ]\n          )\n        ),\n        None,\n      )\n\n    insertion_index = (\n      map_index + 1\n      if exactness_index is None\n      else exactness_index + 1\n    )\n\n    paragraphs.insert(\n      insertion_index,\n      kernel_paragraph,\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
PHASE157_TEST_FUNCTION = 'def test_phase157_r19_pi6_3_has_five_named_public_references():\n  reference, _ = _reference_and_body()\n\n  assert "**[R1] Proposition 5.6.**" in reference\n  assert "**[R2] (5.3).**" in reference\n  assert "**[R3] Proposition 5.3.**" in reference\n  assert "**[R4] Proposition 5.1.**" in reference\n  assert "**[R5] Proposition 2.2.**" in reference\n\n  assert (\n    r"$\\pi_{5}^{2} = \\mathbb{Z}/2\\{\\eta_{2}^{3}\\}$."\n    in reference\n  )\n  assert (\n    r"$\\nu\' \\in \\{\\eta_{3}, 2\\iota_{4}, \\eta_{4}\\}_{1}$ とすると,"\n    in reference\n  )\n  assert (\n    r"$\\nu\' \\in \\pi_{6}^{3}$."\n    in reference\n  )\n  assert (\n    r"$2\\nu\' = \\eta_{3}^{3}$."\n    in reference\n  )\n  assert (\n    r"$H\\left(\\nu\'\\right) = \\eta_{5}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{7}^{5} = \\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$."\n    in reference\n  )\n  assert (\n    r"$\\pi_{6}^{5} = \\mathbb{Z}/2\\{\\eta_{5}\\}$."\n    in reference\n  )\n  assert (\n    r"$H(\\alpha\\circ E\\beta) = H(\\alpha)\\circ E\\beta$."\n    in reference\n  )\n'
PHASE156_DEPTH2_FUNCTION = 'def test_phase156_r5_repair11_public_pi6_keeps_current_proof_required_references_depth2():\n  (\n    raw,\n    presentation,\n    semantic_sidecar,\n    blocks,\n    arguments,\n  ) = _data(\n    2\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      semantic_sidecar,\n      arguments,\n    )\n  )\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  assert headers == [\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n    "Proposition 2.2",\n  ]\n'
PHASE156_DEPTH3_FUNCTION = 'def test_phase156_r5_repair11_public_pi6_keeps_current_proof_required_references_depth3():\n  raw = _data(\n    3\n  )[\n    0\n  ]\n  rendered = render_toda_group_proof_narrative_markdown(\n    raw\n  )\n  headers = re.findall(\n    r"\\*\\*\\[R\\d+\\] ([^\\n]+?)\\.\\*\\*",\n    rendered,\n  )\n\n  for required in (\n    "Proposition 5.6",\n    "(5.3)",\n    "Proposition 5.3",\n    "Proposition 5.1",\n    "Proposition 2.2",\n  ):\n    assert required in headers\n\n  assert "Lemma 5.2" not in rendered\n'
NEW_TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair16() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair16_eta_bridge_preserves_suspension_reason():\n  rendered = _render_pi6_3_repair16()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert r"$\\eta_{6}=E\\eta_{5}$ である." in body\n  assert r"$\\eta_{6}=\\eta_{6}$ である." not in body\n\n\ndef test_phase157_r20_repair16_removes_reflexive_equalities():\n  rendered = _render_pi6_3_repair16()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert r"$\\eta_{3}^{3} = \\eta_{3}^{3}" not in body\n  assert r"$\\eta_{5} = \\eta_{5}" not in body\n\n\ndef test_phase157_r20_repair16_kernel_reason_follows_surjectivity_and_exactness():\n  rendered = _render_pi6_3_repair16()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  surjective = (\n    r"$H: \\pi_{7}^{3} \\to "\n    r"\\pi_{7}^{5}$ は全射である."\n  )\n  exactness = (\n    r"$\\pi_{7}^{3} \\xrightarrow{H} "\n    r"\\pi_{7}^{5} \\xrightarrow{\\Delta} "\n    r"\\pi_{5}^{2} \\xrightarrow{E} "\n    r"\\pi_{6}^{3}$ は完全である."\n  )\n  kernel = (\n    "完全性より, "\n    r"$\\ker \\Delta=\\operatorname{Im}H="\n    r"\\pi_{7}^{5}$ である."\n  )\n  delta_zero = (\n    r"$\\Delta: \\pi_{7}^{5} \\to "\n    r"\\pi_{5}^{2}$ は零写像である."\n  )\n\n  assert surjective in body\n  assert exactness in body\n  assert kernel in body\n  assert delta_zero in body\n\n  assert body.index(\n    surjective\n  ) < body.index(\n    exactness\n  )\n  assert body.index(\n    exactness\n  ) < body.index(\n    kernel\n  )\n  assert body.index(\n    kernel\n  ) < body.index(\n    delta_zero\n  )\n'


def function_range(source: str, name: str):
  tree = ast.parse(source)
  lines = source.splitlines(keepends=True)

  for node in tree.body:
    if (
      isinstance(node, ast.FunctionDef)
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[:node.lineno - 1]
      )
      end = sum(
        len(line)
        for line in lines[:node.end_lineno]
      )

      while (
        end < len(source)
        and source[end:end + 1] == "\n"
      ):
        end += 1

      return start, end

  raise RuntimeError(
    "function not found: " + name
  )


def replace_function(
  source: str,
  name: str,
  replacement: str,
) -> str:
  start, end = function_range(
    source,
    name,
  )

  return (
    source[:start]
    + replacement.rstrip()
    + "\n\n\n"
    + source[end:]
  )


def insert_before_function(
  source: str,
  before_name: str,
  addition: str,
) -> str:
  start, _end = function_range(
    source,
    before_name,
  )

  return (
    source[:start]
    + addition.rstrip()
    + "\n\n\n"
    + source[start:]
  )


def add_reflexive_call(
  source: str,
) -> str:
  call = """  rendered = (
    suppress_toda_group_proof_narrative_reflexive_equalities(
      presentation,
      rendered,
    )
  )
"""

  if call in source:
    return source

  anchor = """  rendered = (
    link_toda_group_proof_narrative_unmarked_reference_consumers(
      presentation,
      rendered,
      reference_entries,
    )
  )
"""

  if source.count(anchor) != 1:
    raise RuntimeError(
      "late unmarked-reference call not found exactly once"
    )

  return source.replace(
    anchor,
    anchor + call,
    1,
  )


def main() -> int:
  for path in (
    RENDERER,
    PHASE157_TEST,
    PHASE156_TEST,
  ):
    if not path.is_file():
      raise RuntimeError(
        "missing file: " + str(path)
      )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = ROOT / (
    "phase157_r20_repair16_backup_"
    + timestamp
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  for path in (
    RENDERER,
    PHASE157_TEST,
    PHASE156_TEST,
  ):
    shutil.copy2(
      path,
      backup / path.name,
    )

  renderer = RENDERER.read_text(
    encoding="utf-8"
  )
  renderer = replace_function(
    renderer,
    "insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges",
    BRIDGE_FUNCTION,
  )
  renderer = replace_function(
    renderer,
    "order_toda_group_proof_narrative_surjectivity_support",
    ORDER_FUNCTION,
  )

  if (
    "def suppress_toda_group_proof_narrative_reflexive_equalities("
    not in renderer
  ):
    renderer = insert_before_function(
      renderer,
      "order_toda_group_proof_narrative_surjectivity_support",
      REFLEXIVE_FUNCTION,
    )

  renderer = add_reflexive_call(
    renderer
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in renderer:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  phase157_source = PHASE157_TEST.read_text(
    encoding="utf-8"
  )
  phase157_source = replace_function(
    phase157_source,
    "test_phase157_r19_pi6_3_has_five_named_public_references",
    PHASE157_TEST_FUNCTION,
  )

  phase156_source = PHASE156_TEST.read_text(
    encoding="utf-8"
  )
  phase156_source = replace_function(
    phase156_source,
    "test_phase156_r5_repair11_public_pi6_prunes_internal_only_proposition51_depth2",
    PHASE156_DEPTH2_FUNCTION,
  )
  phase156_source = replace_function(
    phase156_source,
    "test_phase156_r5_repair11_public_pi6_prunes_internal_only_proposition51_depth3",
    PHASE156_DEPTH3_FUNCTION,
  )

  for path, source in (
    (RENDERER, renderer),
    (PHASE157_TEST, phase157_source),
    (PHASE156_TEST, phase156_source),
    (NEW_TEST, NEW_TEST_SOURCE),
  ):
    compile(
      source,
      str(path),
      "exec",
    )
    path.write_text(
      source,
      encoding="utf-8",
      newline="\n",
    )

  print(
    "Phase157-R20 repair16 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed production file:",
    RENDERER,
  )
  print(
    "Changed tests:",
    PHASE157_TEST,
  )
  print(
    " ",
    PHASE156_TEST,
  )
  print(
    "Added test:",
    NEW_TEST,
  )
  print("")
  print(
    "Architecture preflight:"
  )

  for token in forbidden:
    print(
      " ",
      token,
      "=",
      renderer.count(token),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
