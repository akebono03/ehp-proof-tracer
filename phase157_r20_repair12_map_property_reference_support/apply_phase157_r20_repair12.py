from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()
TARGET = (
  ROOT
  / "toda_group_proof_narrative_contribution_renderer.py"
)
TEST = (
  ROOT
  / "tests"
  / "test_phase157_r20_repair12_map_property_reference_support.py"
)

LINK_FUNCTION = 'def link_toda_group_proof_narrative_unmarked_reference_consumers(\n  presentation: TodaGroupProofPresentation,\n  body_markdown: str,\n  reference_entries,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    body_markdown,\n    str,\n  ):\n    raise TypeError(\n      "body_markdown must be a str"\n    )\n\n  paragraphs = body_markdown.split(\n    "\\n\\n"\n  )\n  consumers_by_step_id = {}\n\n  for edge in presentation.edges:\n    consumers_by_step_id.setdefault(\n      id(\n        edge.premise_step\n      ),\n      [],\n    ).append(\n      edge.parent_step\n    )\n\n  for entry in reference_entries:\n    marker = (\n      "[R"\n      + str(\n        entry.number\n      )\n      + "]"\n    )\n\n    if marker in "\\n\\n".join(\n      paragraphs\n    ):\n      continue\n\n    visible_non_root_consumers = []\n    visible_root_consumers = []\n\n    for proof_step in entry.proof_steps:\n      for consumer in consumers_by_step_id.get(\n        id(\n          proof_step\n        ),\n        (),\n      ):\n        if (\n          classify_toda_proof_step_role(\n            consumer\n          )\n          is TodaProofDependencyRole.MAP_PROPERTY\n        ):\n          continue\n\n        rendered_consumer = (\n          _render_generic_narrative_step(\n            consumer\n          )\n        )\n\n        if not rendered_consumer:\n          continue\n\n        matching_indices = tuple(\n          index\n          for index, paragraph in enumerate(\n            paragraphs\n          )\n          if rendered_consumer in paragraph\n        )\n\n        if len(\n          matching_indices\n        ) != 1:\n          continue\n\n        consumer_index = matching_indices[\n          0\n        ]\n\n        if consumer is presentation.root_step:\n          visible_root_consumers.append(\n            (\n              id(\n                consumer\n              ),\n              consumer_index,\n            )\n          )\n          continue\n\n        consumer_reference = (\n          extract_toda_group_proof_step_literature_reference(\n            consumer\n          )\n        )\n\n        if consumer_reference is not None:\n          continue\n\n        visible_non_root_consumers.append(\n          (\n            id(\n              consumer\n            ),\n            consumer_index,\n          )\n        )\n\n    non_root_candidates = tuple(\n      dict.fromkeys(\n        visible_non_root_consumers\n      )\n    )\n    root_candidates = tuple(\n      dict.fromkeys(\n        visible_root_consumers\n      )\n    )\n\n    if len(\n      non_root_candidates\n    ) == 1:\n      _, consumer_index = non_root_candidates[\n        0\n      ]\n    elif (\n      not non_root_candidates\n      and len(\n        root_candidates\n      ) == 1\n    ):\n      _, consumer_index = root_candidates[\n        0\n      ]\n    else:\n      continue\n\n    paragraph = paragraphs[\n      consumer_index\n    ]\n\n    if marker in paragraph:\n      continue\n\n    paragraphs[\n      consumer_index\n    ] = (\n      marker\n      + "を用いて, "\n      + paragraph\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
ORDER_FUNCTION = 'def order_toda_group_proof_narrative_surjectivity_support(\n  presentation: TodaGroupProofPresentation,\n  markdown: str,\n  reference_entries=(),\n  statement_lines_by_reference_number=None,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    markdown,\n    str,\n  ):\n    raise TypeError(\n      "markdown must be a str"\n    )\n\n  if not isinstance(\n    reference_entries,\n    tuple,\n  ):\n    raise TypeError(\n      "reference_entries must be a tuple"\n    )\n\n  if statement_lines_by_reference_number is None:\n    statement_lines_by_reference_number = {}\n\n  if not isinstance(\n    statement_lines_by_reference_number,\n    dict,\n  ):\n    raise TypeError(\n      "statement_lines_by_reference_number must be a dict"\n    )\n\n  paragraphs = markdown.split(\n    "\\n\\n"\n  )\n\n  def paragraph_match_key(\n    paragraph: str,\n  ) -> str:\n    stripped = paragraph.strip()\n\n    if stripped.startswith(\n      "[R"\n    ):\n      marker_end = stripped.find(\n        "]より, "\n      )\n\n      if marker_end >= 0:\n        stripped = stripped[\n          marker_end\n          + len(\n            "]より, "\n          ):\n        ]\n\n    return (\n      _phase157_r11_reference_statement_match_key(\n        stripped\n      )\n    )\n\n  def paragraph_index_for_step(\n    proof_step: ProofStep,\n  ) -> int | None:\n    rendered_statement = (\n      _render_generic_narrative_step(\n        proof_step\n      )\n    )\n\n    if not rendered_statement:\n      return None\n\n    target_key = (\n      _phase157_r11_reference_statement_match_key(\n        rendered_statement\n      )\n    )\n\n    matching_indices = tuple(\n      index\n      for index, paragraph in enumerate(\n        paragraphs\n      )\n      if paragraph_match_key(\n        paragraph\n      ) == target_key\n    )\n\n    if len(\n      matching_indices\n    ) != 1:\n      return None\n\n    return matching_indices[\n      0\n    ]\n\n  for node in presentation.nodes:\n    map_step = node.proof_step\n\n    if (\n      classify_toda_proof_step_role(\n        map_step\n      )\n      is not TodaProofDependencyRole.MAP_PROPERTY\n    ):\n      continue\n\n    map_index = paragraph_index_for_step(\n      map_step\n    )\n\n    if map_index is None:\n      continue\n\n    equality_premises = tuple(\n      premise\n      for premise in map_step.premises\n      if (\n        isinstance(\n          premise.conclusion,\n          Relation,\n        )\n        and premise.conclusion.relation_type\n        is RelationType.EQUALITY\n      )\n    )\n\n    support_steps = []\n\n    for equality_premise in equality_premises:\n      support_steps.extend(\n        premise\n        for premise in equality_premise.premises\n        if (\n          isinstance(\n            premise.conclusion,\n            Relation,\n          )\n          and premise.conclusion.relation_type\n          is RelationType.EQUALITY\n        )\n      )\n      support_steps.append(\n        equality_premise\n      )\n\n    support_indices = tuple(\n      index\n      for proof_step in support_steps\n      for index in (\n        paragraph_index_for_step(\n          proof_step\n        ),\n      )\n      if index is not None\n    )\n\n    if (\n      support_steps\n      and len(\n        support_indices\n      ) == len(\n        support_steps\n      )\n    ):\n      first_support_index = min(\n        support_indices\n      )\n      last_support_index = max(\n        support_indices\n      )\n\n      if not (\n        first_support_index < map_index\n        and last_support_index < map_index\n      ):\n        support_block = paragraphs[\n          first_support_index:\n          last_support_index + 1\n        ]\n\n        del paragraphs[\n          first_support_index:\n          last_support_index + 1\n        ]\n\n        map_index = paragraph_index_for_step(\n          map_step\n        )\n\n        if map_index is not None:\n          paragraphs[\n            map_index:\n            map_index\n          ] = support_block\n\n    map_index = paragraph_index_for_step(\n      map_step\n    )\n\n    if map_index is None:\n      continue\n\n    short_exact_reason_index = next(\n      (\n        index\n        for index in range(\n          map_index\n        )\n        if (\n          "右の写像が全射"\n          in paragraphs[\n            index\n          ]\n          and "短完全列"\n          in paragraphs[\n            index\n          ]\n        )\n      ),\n      None,\n    )\n\n    if short_exact_reason_index is None:\n      continue\n\n    support_indices = tuple(\n      index\n      for proof_step in support_steps\n      for index in (\n        paragraph_index_for_step(\n          proof_step\n        ),\n      )\n      if index is not None\n    )\n\n    block_start = (\n      min(\n        support_indices\n      )\n      if support_indices\n      else map_index\n    )\n    block_end = map_index + 1\n\n    if block_start <= short_exact_reason_index:\n      continue\n\n    dependency_block = paragraphs[\n      block_start:\n      block_end\n    ]\n\n    del paragraphs[\n      block_start:\n      block_end\n    ]\n\n    paragraphs[\n      short_exact_reason_index:\n      short_exact_reason_index\n    ] = dependency_block\n\n  for map_index, paragraph in enumerate(\n    tuple(\n      paragraphs\n    )\n  ):\n    stripped = paragraph.strip()\n\n    if (\n      not stripped.startswith(\n        "$H:"\n      )\n      or " は全射である." not in stripped\n      or r"\\to " not in stripped\n    ):\n      continue\n\n    target_fragment = stripped.split(\n      r"\\to ",\n      1,\n    )[1].split(\n      "$",\n      1,\n    )[0].strip()\n\n    group_prefix = (\n      "$"\n      + target_fragment\n      + " = "\n    )\n\n    existing_group_index = next(\n      (\n        index\n        for index in range(\n          len(\n            paragraphs\n          )\n        )\n        if paragraphs[\n          index\n        ].strip().startswith(\n          group_prefix\n        )\n      ),\n      None,\n    )\n\n    if existing_group_index is not None:\n      if existing_group_index > map_index:\n        group_paragraph = paragraphs.pop(\n          existing_group_index\n        )\n        paragraphs.insert(\n          map_index,\n          group_paragraph,\n        )\n      continue\n\n    reference_matches = []\n\n    for entry in reference_entries:\n      lines = (\n        statement_lines_by_reference_number.get(\n          entry.number,\n          (),\n        )\n      )\n\n      for line in lines:\n        normalized_line = line.strip()\n\n        if not normalized_line.startswith(\n          group_prefix\n        ):\n          continue\n\n        reference_matches.append(\n          (\n            entry.number,\n            normalized_line,\n          )\n        )\n\n    unique_matches = tuple(\n      dict.fromkeys(\n        reference_matches\n      )\n    )\n\n    if len(\n      unique_matches\n    ) != 1:\n      continue\n\n    reference_number, statement_line = (\n      unique_matches[\n        0\n      ]\n    )\n    support_paragraph = (\n      "[R"\n      + str(\n        reference_number\n      )\n      + "]より, "\n      + statement_line\n    )\n\n    if support_paragraph in paragraphs:\n      continue\n\n    paragraphs.insert(\n      map_index,\n      support_paragraph,\n    )\n\n  return "\\n\\n".join(\n    paragraphs\n  )\n'
TEST_SOURCE = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_pi6_3_repair12() -> str:\n  report = build_standard_toda_report(\n    n=3,\n    k=3,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase157_r20_repair12_pi7_5_reference_support_precedes_surjectivity():\n  rendered = _render_pi6_3_repair12()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  group_line = (\n    r"[R3]より, $\\pi_{7}^{5} = "\n    r"\\mathbb{Z}/2\\{\\eta_{5}^{2}\\}$"\n  )\n  surjective_line = (\n    r"$H: \\pi_{7}^{3} \\to "\n    r"\\pi_{7}^{5}$ は全射である."\n  )\n\n  assert group_line in body\n  assert surjective_line in body\n  assert body.index(\n    group_line\n  ) < body.index(\n    surjective_line\n  )\n\n\ndef test_phase157_r20_repair12_map_property_is_not_misattributed_to_prop56():\n  rendered = _render_pi6_3_repair12()\n  body = rendered.split(\n    "---",\n    1,\n  )[1]\n\n  assert (\n    r"[R1]より, $H: \\pi_{7}^{3} "\n    r"\\to \\pi_{7}^{5}$ は全射である."\n    not in body\n  )\n\n\ndef test_phase157_r20_repair12_public_references_keep_r1_through_r5():\n  rendered = _render_pi6_3_repair12()\n  reference = rendered.split(\n    "---",\n    1,\n  )[0]\n\n  for header in (\n    "**[R1] Proposition 5.6.**",\n    "**[R2] (5.3).**",\n    "**[R3] Proposition 5.3.**",\n    "**[R4] Proposition 5.1.**",\n    "**[R5] Proposition 2.2.**",\n  ):\n    assert header in reference\n'


def function_range(
  source: str,
  name: str,
):
  tree = ast.parse(
    source
  )
  lines = source.splitlines(
    keepends=True
  )

  for node in tree.body:
    if (
      isinstance(
        node,
        ast.FunctionDef,
      )
      and node.name == name
    ):
      start = sum(
        len(line)
        for line in lines[
          :node.lineno - 1
        ]
      )
      end = sum(
        len(line)
        for line in lines[
          :node.end_lineno
        ]
      )

      while (
        end < len(source)
        and source[
          end:
          end + 1
        ] == "\n"
      ):
        end += 1

      return start, end

  raise RuntimeError(
    "function not found: "
    + name
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


def patch_call_site(
  source: str,
) -> str:
  old = """  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
    )
  )
"""

  new = """  rendered = (
    order_toda_group_proof_narrative_surjectivity_support(
      presentation,
      rendered,
      reference_entries,
      statement_lines_by_reference_number,
    )
  )
"""

  if new in source:
    return source

  if source.count(
    old
  ) != 1:
    raise RuntimeError(
      "surjectivity-support call site was not found exactly once"
    )

  return source.replace(
    old,
    new,
    1,
  )


def main() -> int:
  if not TARGET.is_file():
    raise RuntimeError(
      "Run from repository root."
    )

  timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
  )
  backup = (
    ROOT
    / (
      "phase157_r20_repair12_backup_"
      + timestamp
    )
  )
  backup.mkdir(
    parents=True,
    exist_ok=False,
  )

  shutil.copy2(
    TARGET,
    backup / TARGET.name,
  )

  source = TARGET.read_text(
    encoding="utf-8"
  )

  source = replace_function(
    source,
    "link_toda_group_proof_narrative_unmarked_reference_consumers",
    LINK_FUNCTION,
  )
  source = replace_function(
    source,
    "order_toda_group_proof_narrative_surjectivity_support",
    ORDER_FUNCTION,
  )
  source = patch_call_site(
    source
  )

  forbidden = (
    "_phase157_r19_",
    "is_pi6_3",
    "_phase157_r3_restore_pi6_3_",
  )

  for token in forbidden:
    if token in source:
      raise RuntimeError(
        "target-specific token remains: "
        + token
      )

  compile(
    source,
    str(
      TARGET
    ),
    "exec",
  )
  compile(
    TEST_SOURCE,
    str(
      TEST
    ),
    "exec",
  )

  TARGET.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_SOURCE,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Phase157-R20 repair12 applied."
  )
  print(
    "Backup:",
    backup,
  )
  print(
    "Changed:",
    TARGET,
  )
  print(
    "Added test:",
    TEST,
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
      source.count(
        token
      ),
    )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )
