from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"


def _replace_function(source: str, function_name: str, replacement: str) -> str:
  marker = "def " + function_name + "("
  start = source.find(marker)
  if start < 0:
    raise RuntimeError("function not found: " + function_name)
  next_function = source.find("\ndef ", start + len(marker))
  end = len(source) if next_function < 0 else next_function + 1
  return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


def _ensure_import_name(
  source: str,
  module_name: str,
  import_name: str,
) -> str:
  start_marker = "from " + module_name + " import (\n"
  block_start = source.find(start_marker)
  if block_start < 0:
    raise RuntimeError("import block not found: " + module_name)
  block_end = source.find(")\n", block_start)
  if block_end < 0:
    raise RuntimeError("import block end not found: " + module_name)
  block = source[block_start:block_end + 2]
  if "\n  " + import_name + ",\n" in block:
    return source
  updated = block[:-2] + "  " + import_name + ",\n)\n"
  return source[:block_start] + updated + source[block_end + 2:]


def _ensure_import_block(
  source: str,
  block: str,
  anchor_module: str,
) -> str:
  if block.splitlines()[0] in source:
    return source
  anchor = "from " + anchor_module + " import (\n"
  anchor_start = source.find(anchor)
  if anchor_start < 0:
    raise RuntimeError("anchor import block not found: " + anchor_module)
  anchor_end = source.find(")\n", anchor_start)
  if anchor_end < 0:
    raise RuntimeError("anchor import block end not found: " + anchor_module)
  anchor_end += 2
  return source[:anchor_end] + block + source[anchor_end:]


TARGET_FUNCTION = r'''def _phase158_public_narrative_target_lines(
  presentation: TodaGroupProofPresentation,
) -> list[str]:
  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  if root_latex is not None:
    return [
      r"\[",
      root_latex + ".",
      r"\]",
    ]

  return [
    _render_group_proof_narrative_fact(
      presentation.root_step
    )
  ]
'''


PHASE159_HELPERS = r'''def _phase159_public_semantic_projection_context(
  presentation: TodaGroupProofPresentation,
):
  semantic_presentation = (
    build_toda_group_proof_narrative_semantic_closure_presentation(
      presentation
    )
  )
  semantic_sidecar = (
    build_toda_group_proof_narrative_semantic_sidecar(
      semantic_presentation
    )
  )
  blocks = (
    build_toda_group_proof_narrative_blocks(
      semantic_presentation,
      semantic_sidecar=semantic_sidecar,
    )
  )
  exactness_blocks = tuple(
    block
    for block in blocks
    if (
      block.role
      is TodaGroupProofNarrativeMathematicalBlockRole
      .EXACTNESS
    )
  )
  components = (
    build_toda_group_proof_narrative_exactness_method_components(
      exactness_blocks
    )
  )
  target = (
    semantic_presentation
    .source_replay
    .group_result
    .target
  )
  matching_components = tuple(
    component
    for component in components
    if any(
      target
      in (
        window.source_term,
        window.middle_term,
        window.target_term,
      )
      for window in component.windows
    )
  )
  primary_component = (
    matching_components[0]
    if len(matching_components) == 1
    else None
  )

  return (
    semantic_presentation,
    semantic_sidecar,
    primary_component,
  )


def _phase159_matching_map_property_step(
  presentation: TodaGroupProofPresentation,
  statement_types: tuple,
  group_map,
) -> ProofStep | None:
  return next(
    (
      node.proof_step
      for node in presentation.nodes
      if (
        isinstance(
          node.proof_step.conclusion,
          statement_types,
        )
        and getattr(
          node.proof_step.conclusion,
          "map",
          None,
        )
        == group_map
      )
    ),
    None,
  )


def _phase159_public_map_property_triples(
  presentation: TodaGroupProofPresentation,
) -> tuple[
  tuple[
    ProofStep,
    ProofStep,
    ProofStep,
  ],
  ...,
]:
  triples = []

  for node in presentation.nodes:
    isomorphism_step = node.proof_step
    statement = isomorphism_step.conclusion

    if not isinstance(
      statement,
      _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
    ):
      continue

    group_map = getattr(
      statement,
      "map",
      None,
    )

    if group_map is None:
      continue

    injective_step = _phase159_matching_map_property_step(
      presentation,
      _GENERIC_INJECTIVE_STATEMENT_TYPES,
      group_map,
    )
    surjective_step = _phase159_matching_map_property_step(
      presentation,
      _GENERIC_SURJECTIVE_STATEMENT_TYPES,
      group_map,
    )

    if injective_step is None or surjective_step is None:
      continue

    triples.append(
      (
        injective_step,
        surjective_step,
        isomorphism_step,
      )
    )

  return tuple(triples)


def _phase159_numbered_map_property_line(
  proof_step: ProofStep,
  number: int,
  predicate: str,
) -> str | None:
  group_map = getattr(
    proof_step.conclusion,
    "map",
    None,
  )
  if group_map is None:
    return None

  map_latex = _render_generic_narrative_group_map_latex(
    group_map
  )
  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + r"\tag{"
    + str(number)
    + "}$ は"
    + predicate
    + "."
  )


def _phase159_plain_map_property_line(
  proof_step: ProofStep,
  predicate: str,
) -> str | None:
  group_map = getattr(
    proof_step.conclusion,
    "map",
    None,
  )
  if group_map is None:
    return None

  map_latex = _render_generic_narrative_group_map_latex(
    group_map
  )
  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + "$ は"
    + predicate
    + "."
  )


def _phase159_unique_preimage_definition_line(
  semantic_sidecar,
  proof_step: ProofStep,
) -> str | None:
  dependency = next(
    (
      candidate
      for candidate in semantic_sidecar.dependency_semantics
      if (
        candidate.dependent_step is proof_step
        and candidate.role
        is TodaGroupProofNarrativeDependencySemanticRole
        .PRECONDITION_FOR_DEFINITION
        and isinstance(
          candidate.prerequisite_step.conclusion,
          _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
        )
      )
    ),
    None,
  )

  if dependency is None:
    return None

  statement = proof_step.conclusion
  prerequisite_statement = dependency.prerequisite_step.conclusion
  group_map = getattr(statement, "map", None)
  prerequisite_map = getattr(prerequisite_statement, "map", None)
  element = getattr(statement, "element", None)
  image = getattr(statement, "image", None)

  if (
    group_map is None
    or prerequisite_map is None
    or group_map != prerequisite_map
    or element is None
    or image is None
  ):
    return None

  map_name = getattr(group_map, "name", None)
  if not isinstance(map_name, str):
    return None

  return (
    "この同型写像により, $"
    + map_name
    + "("
    + render_toda_expression_latex(element)
    + ") = "
    + render_toda_expression_latex(image)
    + "$ となる $"
    + render_toda_expression_latex(element)
    + r" \in "
    + render_toda_primary_group_latex(group_map.source_group)
    + "$ が一意に存在する."
  )


def _phase159_project_generic_semantics_to_public_proof(
  presentation: TodaGroupProofPresentation,
  proof_body: list[str],
) -> list[str]:
  (
    semantic_presentation,
    semantic_sidecar,
    primary_component,
  ) = _phase159_public_semantic_projection_context(
    presentation
  )

  lines = list(proof_body)

  if primary_component is not None:
    exactness_step_lines = {
      _render_generic_narrative_step(proof_step)
      for block in primary_component.evidence_blocks
      for proof_step in block.steps
    }
    long_exact_sequence = (
      "$"
      + render_toda_group_proof_narrative_exactness_method_component_latex(
        primary_component
      )
      + "$ は完全である."
    )
    projected_lines = []
    inserted = False

    for line in lines:
      if any(
        exactness_line in line
        for exactness_line in exactness_step_lines
      ):
        if not inserted:
          projected_lines.append(long_exact_sequence)
          inserted = True
        continue
      projected_lines.append(line)

    lines = projected_lines

  next_equation_number = 1
  for line in lines:
    number = _phase158_public_equation_tag_number(line)
    if (
      number is not None
      and number >= next_equation_number
    ):
      next_equation_number = number + 1

  for (
    injective_step,
    surjective_step,
    isomorphism_step,
  ) in _phase159_public_map_property_triples(
    semantic_presentation
  ):
    injective_rendered = _render_generic_narrative_step(
      injective_step
    )
    surjective_rendered = _render_generic_narrative_step(
      surjective_step
    )
    isomorphism_rendered = _render_generic_narrative_step(
      isomorphism_step
    )

    injective_index = next(
      (
        index
        for index, line in enumerate(lines)
        if injective_rendered in line
      ),
      None,
    )
    surjective_index = next(
      (
        index
        for index, line in enumerate(lines)
        if surjective_rendered in line
      ),
      None,
    )
    isomorphism_index = next(
      (
        index
        for index, line in enumerate(lines)
        if isomorphism_rendered in line
      ),
      None,
    )

    if (
      injective_index is None
      or surjective_index is None
      or isomorphism_index is None
    ):
      continue

    injective_number = next_equation_number
    surjective_number = next_equation_number + 1
    next_equation_number += 2

    injective_line = _phase159_numbered_map_property_line(
      injective_step,
      injective_number,
      "単射",
    )
    surjective_line = _phase159_numbered_map_property_line(
      surjective_step,
      surjective_number,
      "全射",
    )
    isomorphism_line = _phase159_plain_map_property_line(
      isomorphism_step,
      "同型写像",
    )

    if (
      injective_line is None
      or surjective_line is None
      or isomorphism_line is None
    ):
      continue

    lines[injective_index] = lines[injective_index].replace(
      injective_rendered,
      injective_line,
      1,
    )
    lines[surjective_index] = lines[surjective_index].replace(
      surjective_rendered,
      surjective_line,
      1,
    )

    source_line = lines[isomorphism_index]
    marker_index = source_line.find(isomorphism_rendered)
    prefix = (
      source_line[:marker_index]
      if marker_index >= 0
      else ""
    )
    derivation_prefixes = (
      "これらから, ",
      "これらより, ",
      "このことから, ",
      "したがって, ",
    )
    if prefix in derivation_prefixes:
      prefix = ""

    lines[isomorphism_index] = (
      prefix
      + "("
      + str(injective_number)
      + ") と ("
      + str(surjective_number)
      + ") より, "
      + isomorphism_line
    )

  for dependency in semantic_sidecar.dependency_semantics:
    if (
      dependency.role
      is not TodaGroupProofNarrativeDependencySemanticRole
      .PRECONDITION_FOR_DEFINITION
    ):
      continue

    proof_step = dependency.dependent_step
    original = _render_generic_narrative_step(proof_step)
    replacement = _phase159_unique_preimage_definition_line(
      semantic_sidecar,
      proof_step,
    )
    if replacement is None:
      continue

    for index, line in enumerate(lines):
      if original not in line:
        continue

      prefix = line[:line.find(original)]
      if prefix in (
        "これらから, ",
        "これらより, ",
        "このことから, ",
        "したがって, ",
      ):
        prefix = ""

      lines[index] = prefix + replacement
      break

  compacted = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()
    if is_blank and previous_blank:
      continue
    compacted.append(line)
    previous_blank = is_blank

  return compacted
'''


NORMALIZER_FUNCTION = r'''def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
  if not isinstance(
    presentation,
    TodaGroupProofPresentation,
  ):
    raise TypeError(
      "presentation must be a "
      "TodaGroupProofPresentation"
    )

  if not isinstance(
    rendered,
    str,
  ):
    raise TypeError(
      "rendered must be a str"
    )

  if presentation.max_depth < 2:
    return rendered

  title = "# Group proof narrative"
  target_header = "## 証明対象"
  reference_header = "## 使用する結果"
  separator = "---"
  proof_header = "## 証明"
  qed = "□"

  source_lines = rendered.rstrip().splitlines()

  if source_lines and source_lines[0] == title:
    content_lines = source_lines[1:]
  else:
    content_lines = source_lines[:]

  while content_lines and not content_lines[0].strip():
    content_lines.pop(0)

  def exact_index(
    marker: str,
  ) -> int | None:
    try:
      return content_lines.index(marker)
    except ValueError:
      return None

  target_index = exact_index(target_header)
  reference_index = exact_index(reference_header)
  proof_index = exact_index(proof_header)

  target_body = _phase158_public_narrative_target_lines(
    presentation
  )

  reference_body: list[str] = []

  if (
    reference_index is not None
    and proof_index is not None
    and reference_index < proof_index
  ):
    reference_body = content_lines[
      reference_index + 1:
      proof_index
    ]

  while reference_body and not reference_body[0].strip():
    reference_body.pop(0)

  while reference_body and not reference_body[-1].strip():
    reference_body.pop()

  if (
    reference_body
    and reference_body[-1].strip() == separator
  ):
    reference_body.pop()
    while reference_body and not reference_body[-1].strip():
      reference_body.pop()

  if proof_index is not None:
    proof_body = content_lines[proof_index + 1:]
  elif target_index is None and reference_index is None:
    proof_body = content_lines[:]
  else:
    proof_body = []

  while proof_body and not proof_body[0].strip():
    proof_body.pop(0)

  proof_body = _phase158_strip_terminal_qed_lines(
    proof_body
  )
  proof_body = _phase158_normalize_public_equation_numbers(
    proof_body
  )
  proof_body = _phase159_project_generic_semantics_to_public_proof(
    presentation,
    proof_body,
  )

  lines = [
    title,
    "",
    target_header,
    "",
    *target_body,
    "",
    reference_header,
    "",
  ]

  if reference_body:
    lines.extend(
      (
        *reference_body,
        "",
      )
    )

  lines.extend(
    (
      separator,
      "",
      proof_header,
      "",
      *proof_body,
      "",
      qed,
    )
  )

  return "\n".join(lines).rstrip() + "\n"
'''


TEST_CONTENT = r'''from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)
from toda_rules import (
  TodaPi32Eta2DefinitionStatement,
)


def _phase159_r1_2_pi3_2_presentation():
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[0]
    .source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_r1_2_pi3_2_definition_uses_semantic_prose():
  presentation = _phase159_r1_2_pi3_2_presentation()
  definition_step = next(
    node.proof_step
    for node in presentation.nodes
    if isinstance(
      node.proof_step.conclusion,
      TodaPi32Eta2DefinitionStatement,
    )
  )

  rendered = _render_generic_narrative_step(
    definition_step
  )

  assert "Toda pi_3^2 define eta_2 as unique Hopf preimage" not in rendered
  assert r"H(\eta_{2}) = \iota_{3}" in rendered
  assert r"\eta_{2} \in \pi_{3}^{2}" in rendered
  assert "を定める." in rendered


def test_phase159_r1_3_pi3_2_public_target_has_no_show_sentence():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  target = (
    "## 証明対象\n\n"
    "\\[\n"
    r"\pi_{3}^{2} = \mathbb{Z}\{\eta_{2}\}."
    "\n\\]"
  )

  assert target in rendered
  assert "を示す." not in rendered
  assert "を示す。" not in rendered


def test_phase159_r1_3_pi3_2_public_uses_one_semantic_exactness_component():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  long_exact = (
    r"$\pi_{2}^{1} \xrightarrow{E} "
    r"\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$ は完全である."
  )

  assert long_exact in rendered
  assert rendered.count(long_exact) == 1
  assert (
    r"$\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$ は完全である."
    not in rendered
  )
  assert (
    r"$\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1}$ は完全である."
    not in rendered
  )


def test_phase159_r1_3_pi3_2_public_numbers_map_properties_semantically():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  injective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\tag{1}$ は単射."
  )
  surjective = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}"
    r"\tag{2}$ は全射."
  )
  isomorphism = (
    r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ "
    "は同型写像."
  )

  assert injective in rendered
  assert surjective in rendered
  assert "(1) と (2) より, " + isomorphism in rendered
  assert rendered.index(injective) < rendered.index(surjective)
  assert rendered.index(surjective) < rendered.index(isomorphism)


def test_phase159_r1_3_pi3_2_public_definition_uses_isomorphism_semantics():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert (
    "この同型写像により, "
    r"$H(\eta_{2}) = \iota_{3}$ となる "
    r"$\eta_{2} \in \pi_{3}^{2}$ が一意に存在する."
    in rendered
  )
  assert "Toda pi_3^2 define eta_2 as unique Hopf preimage" not in rendered
  assert rendered.rstrip().endswith("□")
'''


def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(RENDERER)
  if not TEST.exists():
    raise FileNotFoundError(TEST)

  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / ("phase159_r1_3_repair1_backup_" + stamp)
  backup_dir.mkdir(parents=True, exist_ok=False)
  shutil.copy2(RENDERER, backup_dir / RENDERER.name)
  shutil.copy2(TEST, backup_dir / TEST.name)

  source = RENDERER.read_text(encoding="utf-8-sig")

  for import_name in (
    "_GENERIC_INJECTIVE_STATEMENT_TYPES",
    "_GENERIC_ISOMORPHISM_STATEMENT_TYPES",
    "_GENERIC_SURJECTIVE_STATEMENT_TYPES",
    "_render_generic_narrative_group_map_latex",
    "_render_generic_narrative_step",
  ):
    source = _ensure_import_name(
      source,
      "toda_group_proof_generic_narrative_renderer",
      import_name,
    )

  source = _ensure_import_name(
    source,
    "toda_group_proof_narrative_blocks",
    "TodaGroupProofNarrativeMathematicalBlockRole",
  )

  source = _ensure_import_block(
    source,
    '''from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
''',
    "toda_group_proof_narrative_blocks",
  )

  source = _ensure_import_block(
    source,
    '''from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_component_latex,
)
''',
    "toda_group_proof_narrative_exactness_components",
  )

  source = _ensure_import_name(
    source,
    "toda_group_proof_narrative_semantics",
    "TodaGroupProofNarrativeDependencySemanticRole",
  )

  source = _replace_function(
    source,
    "_phase158_public_narrative_target_lines",
    TARGET_FUNCTION,
  )

  helper_markers = (
    "def _phase159_public_exactness_component(",
    "def _phase159_public_semantic_projection_context(",
  )
  helper_start = min(
    (
      source.find(marker)
      for marker in helper_markers
      if source.find(marker) >= 0
    ),
    default=-1,
  )
  normalizer_start = source.find(
    "def _phase158_normalize_public_narrative_contract("
  )
  if normalizer_start < 0:
    raise RuntimeError("public narrative normalizer not found")

  if helper_start >= 0 and helper_start < normalizer_start:
    source = (
      source[:helper_start]
      + PHASE159_HELPERS.rstrip()
      + "\n\n"
      + source[normalizer_start:]
    )
  else:
    source = (
      source[:normalizer_start]
      + PHASE159_HELPERS.rstrip()
      + "\n\n"
      + source[normalizer_start:]
    )

  source = _replace_function(
    source,
    "_phase158_normalize_public_narrative_contract",
    NORMALIZER_FUNCTION,
  )

  RENDERER.write_text(
    source,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_CONTENT,
    encoding="utf-8",
    newline="\n",
  )

  print("Phase 159-R1-3 repair1 applied.")
  print("Backup:", backup_dir)
  print(
    "Partial imports left by the failed R1-3 run are accepted."
  )


if __name__ == "__main__":
  main()
