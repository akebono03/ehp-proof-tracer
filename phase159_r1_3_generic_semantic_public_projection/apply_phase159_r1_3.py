from __future__ import annotations

from pathlib import Path
import shutil
from datetime import datetime


ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"

GENERIC_IMPORT_OLD = '''from toda_group_proof_generic_narrative_renderer import (
  _render_generic_narrative_step,
)
'''

GENERIC_IMPORT_NEW = '''from toda_group_proof_generic_narrative_renderer import (
  _GENERIC_INJECTIVE_STATEMENT_TYPES,
  _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
  _GENERIC_SURJECTIVE_STATEMENT_TYPES,
  _render_generic_narrative_group_map_latex,
  _render_generic_narrative_step,
)
'''

BLOCK_IMPORT_OLD = '''from toda_group_proof_narrative_blocks import (
  build_toda_group_proof_narrative_blocks,
)
'''

BLOCK_IMPORT_NEW = '''from toda_group_proof_narrative_blocks import (
  TodaGroupProofNarrativeMathematicalBlockRole,
  build_toda_group_proof_narrative_blocks,
)
from toda_group_proof_narrative_exactness_components import (
  build_toda_group_proof_narrative_exactness_method_components,
)
from toda_group_proof_narrative_exactness_method_renderer import (
  render_toda_group_proof_narrative_exactness_method_component_latex,
)
'''

TARGET_FUNCTION_OLD = r'''def _phase158_public_narrative_target_lines(
  presentation: TodaGroupProofPresentation,
) -> list[str]:
  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  if root_latex is not None:
    return [
      r"\\[",
      root_latex,
      r"\\]",
      "",
      "を示す.",
    ]

  return [
    (
      _render_group_proof_narrative_fact(
        presentation.root_step
      )
      + "を示す."
    ),
  ]
'''

TARGET_FUNCTION_NEW = r'''def _phase158_public_narrative_target_lines(
  presentation: TodaGroupProofPresentation,
) -> list[str]:
  root_latex = (
    _render_group_proof_narrative_latex(
      presentation.root_step
    )
  )

  if root_latex is not None:
    return [
      r"\\[",
      root_latex + ".",
      r"\\]",
    ]

  return [
    _render_group_proof_narrative_fact(
      presentation.root_step
    )
  ]
'''

NORMALIZER_ANCHOR = '''def _phase158_normalize_public_narrative_contract(
  presentation: TodaGroupProofPresentation,
  rendered: str,
) -> str:
'''

PHASE159_HELPERS = r'''def _phase159_public_exactness_component(
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

  if len(
    matching_components
  ) != 1:
    return (
      semantic_presentation,
      None,
    )

  return (
    semantic_presentation,
    matching_components[
      0
    ],
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
  injective_by_map = {}
  surjective_by_map = {}
  isomorphism_steps = []

  for node in presentation.nodes:
    proof_step = node.proof_step
    statement = proof_step.conclusion
    group_map = getattr(
      statement,
      "map",
      None,
    )

    if group_map is None:
      continue

    if isinstance(
      statement,
      _GENERIC_INJECTIVE_STATEMENT_TYPES,
    ):
      injective_by_map.setdefault(
        group_map,
        proof_step,
      )
      continue

    if isinstance(
      statement,
      _GENERIC_SURJECTIVE_STATEMENT_TYPES,
    ):
      surjective_by_map.setdefault(
        group_map,
        proof_step,
      )
      continue

    if isinstance(
      statement,
      _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
    ):
      isomorphism_steps.append(
        proof_step
      )

  triples = []

  for isomorphism_step in isomorphism_steps:
    group_map = (
      isomorphism_step
      .conclusion
      .map
    )
    injective_step = injective_by_map.get(
      group_map
    )
    surjective_step = surjective_by_map.get(
      group_map
    )

    if (
      injective_step is None
      or surjective_step is None
    ):
      continue

    triples.append(
      (
        injective_step,
        surjective_step,
        isomorphism_step,
      )
    )

  return tuple(
    triples
  )


def _phase159_numbered_map_property_line(
  proof_step: ProofStep,
  number: int,
  predicate: str,
) -> str | None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )

  if group_map is None:
    return None

  map_latex = (
    _render_generic_narrative_group_map_latex(
      group_map
    )
  )

  if map_latex is None:
    return None

  return (
    "$"
    + map_latex
    + r"\\tag{"
    + str(
      number
    )
    + "}$ は"
    + predicate
    + "."
  )


def _phase159_plain_map_property_line(
  proof_step: ProofStep,
  predicate: str,
) -> str | None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )

  if group_map is None:
    return None

  map_latex = (
    _render_generic_narrative_group_map_latex(
      group_map
    )
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
  presentation: TodaGroupProofPresentation,
  proof_step: ProofStep,
) -> str | None:
  statement = proof_step.conclusion
  group_map = getattr(
    statement,
    "map",
    None,
  )
  element = getattr(
    statement,
    "element",
    None,
  )
  image = getattr(
    statement,
    "image",
    None,
  )

  if (
    group_map is None
    or element is None
    or image is None
  ):
    return None

  has_isomorphism = any(
    isinstance(
      node.proof_step.conclusion,
      _GENERIC_ISOMORPHISM_STATEMENT_TYPES,
    )
    and getattr(
      node.proof_step.conclusion,
      "map",
      None,
    )
    == group_map
    for node in presentation.nodes
  )

  if not has_isomorphism:
    return None

  map_name = getattr(
    group_map,
    "name",
    None,
  )

  if not isinstance(
    map_name,
    str,
  ):
    return None

  return (
    "この同型写像により, $"
    + map_name
    + "("
    + render_toda_expression_latex(
      element
    )
    + ") = "
    + render_toda_expression_latex(
      image
    )
    + "$ となる $"
    + render_toda_expression_latex(
      element
    )
    + r" \\in "
    + render_toda_primary_group_latex(
      group_map.source_group
    )
    + "$ が一意に存在する."
  )


def _phase159_project_generic_semantics_to_public_proof(
  presentation: TodaGroupProofPresentation,
  proof_body: list[
    str
  ],
) -> list[
  str
]:
  (
    semantic_presentation,
    primary_component,
  ) = (
    _phase159_public_exactness_component(
      presentation
    )
  )

  lines = list(
    proof_body
  )

  if primary_component is not None:
    exactness_step_lines = {
      _render_generic_narrative_step(
        proof_step
      )
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
          projected_lines.append(
            long_exact_sequence
          )
          inserted = True
        continue

      projected_lines.append(
        line
      )

    lines = projected_lines

  next_equation_number = 1

  for line in lines:
    number = (
      _phase158_public_equation_tag_number(
        line
      )
    )

    if (
      number is not None
      and number >= next_equation_number
    ):
      next_equation_number = (
        number + 1
      )

  for (
    injective_step,
    surjective_step,
    isomorphism_step,
  ) in _phase159_public_map_property_triples(
    semantic_presentation
  ):
    injective_rendered = (
      _render_generic_narrative_step(
        injective_step
      )
    )
    surjective_rendered = (
      _render_generic_narrative_step(
        surjective_step
      )
    )
    isomorphism_rendered = (
      _render_generic_narrative_step(
        isomorphism_step
      )
    )

    injective_index = next(
      (
        index
        for index, line in enumerate(
          lines
        )
        if injective_rendered in line
      ),
      None,
    )
    surjective_index = next(
      (
        index
        for index, line in enumerate(
          lines
        )
        if surjective_rendered in line
      ),
      None,
    )
    isomorphism_index = next(
      (
        index
        for index, line in enumerate(
          lines
        )
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

    injective_number = (
      next_equation_number
    )
    surjective_number = (
      next_equation_number + 1
    )
    next_equation_number += 2

    injective_line = (
      _phase159_numbered_map_property_line(
        injective_step,
        injective_number,
        "単射",
      )
    )
    surjective_line = (
      _phase159_numbered_map_property_line(
        surjective_step,
        surjective_number,
        "全射",
      )
    )
    isomorphism_line = (
      _phase159_plain_map_property_line(
        isomorphism_step,
        "同型写像",
      )
    )

    if (
      injective_line is None
      or surjective_line is None
      or isomorphism_line is None
    ):
      continue

    lines[
      injective_index
    ] = lines[
      injective_index
    ].replace(
      injective_rendered,
      injective_line,
      1,
    )
    lines[
      surjective_index
    ] = lines[
      surjective_index
    ].replace(
      surjective_rendered,
      surjective_line,
      1,
    )

    source_line = lines[
      isomorphism_index
    ]
    prefix = source_line[
      :source_line.find(
        isomorphism_rendered
      )
    ]
    derivation_prefixes = (
      "これらから, ",
      "これらより, ",
      "このことから, ",
      "したがって, ",
    )

    if any(
      prefix.endswith(
        candidate
      )
      for candidate in derivation_prefixes
    ):
      prefix = (
        ""
        if prefix in derivation_prefixes
        else prefix
      )
      source_line = (
        prefix
        + "("
        + str(
          injective_number
        )
        + ") と ("
        + str(
          surjective_number
        )
        + ") より, "
        + isomorphism_line
      )
    else:
      source_line = source_line.replace(
        isomorphism_rendered,
        isomorphism_line,
        1,
      )

    lines[
      isomorphism_index
    ] = source_line

  for node in semantic_presentation.nodes:
    proof_step = node.proof_step
    original = (
      _render_generic_narrative_step(
        proof_step
      )
    )
    replacement = (
      _phase159_unique_preimage_definition_line(
        semantic_presentation,
        proof_step,
      )
    )

    if replacement is None:
      continue

    for index, line in enumerate(
      lines
    ):
      if original not in line:
        continue

      prefix = line[
        :line.find(
          original
        )
      ]
      derivation_prefixes = (
        "これらから, ",
        "これらより, ",
        "このことから, ",
        "したがって, ",
      )

      if prefix in derivation_prefixes:
        prefix = ""

      lines[
        index
      ] = (
        prefix
        + replacement
      )
      break

  compacted = []
  previous_blank = False

  for line in lines:
    is_blank = not line.strip()

    if (
      is_blank
      and previous_blank
    ):
      continue

    compacted.append(
      line
    )
    previous_blank = is_blank

  return compacted
'''

NORMALIZER_INSERT_OLD = '''  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )

  lines = [
'''

NORMALIZER_INSERT_NEW = '''  proof_body = (
    _phase158_normalize_public_equation_numbers(
      proof_body
    )
  )
  proof_body = (
    _phase159_project_generic_semantics_to_public_proof(
      presentation,
      proof_body,
    )
  )

  lines = [
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
    report.candidates[
      0
    ].source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  return build_toda_group_proof_presentation(
    replay
  )


def test_phase159_r1_2_pi3_2_definition_uses_semantic_prose():
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
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
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
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
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
  )

  long_exact = (
    r"$\pi_{3}^{2} \xrightarrow{H} "
    r"\pi_{3}^{3} \xrightarrow{\Delta} "
    r"\pi_{1}^{1} \xrightarrow{E} "
    r"\pi_{2}^{2}$ は完全である."
  )

  assert long_exact in rendered
  assert rendered.count(
    long_exact
  ) == 1
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
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
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
  assert rendered.index(
    injective
  ) < rendered.index(
    surjective
  )
  assert rendered.index(
    surjective
  ) < rendered.index(
    isomorphism
  )


def test_phase159_r1_3_pi3_2_public_definition_uses_isomorphism_semantics():
  presentation = (
    _phase159_r1_2_pi3_2_presentation()
  )
  rendered = (
    render_toda_group_proof_narrative_markdown(
      presentation
    )
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


def replace_once(text: str, old: str, new: str, label: str) -> str:
  count = text.count(old)
  if count == 0:
    if new in text:
      print(f"[already applied] {label}")
      return text
    raise RuntimeError(f"anchor not found: {label}")
  if count != 1:
    raise RuntimeError(
      f"anchor is not unique for {label}: {count}"
    )
  print(f"[apply] {label}")
  return text.replace(old, new, 1)


def main() -> None:
  if not RENDERER.exists():
    raise FileNotFoundError(RENDERER)
  if not TEST.exists():
    raise FileNotFoundError(TEST)

  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / f"phase159_r1_3_backup_{stamp}"
  backup_dir.mkdir(parents=True, exist_ok=False)

  shutil.copy2(
    RENDERER,
    backup_dir / RENDERER.name,
  )
  shutil.copy2(
    TEST,
    backup_dir / TEST.name,
  )

  renderer_text = RENDERER.read_text(
    encoding="utf-8-sig"
  )
  renderer_text = replace_once(
    renderer_text,
    GENERIC_IMPORT_OLD,
    GENERIC_IMPORT_NEW,
    "generic renderer imports",
  )
  renderer_text = replace_once(
    renderer_text,
    BLOCK_IMPORT_OLD,
    BLOCK_IMPORT_NEW,
    "exactness component imports",
  )
  renderer_text = replace_once(
    renderer_text,
    TARGET_FUNCTION_OLD,
    TARGET_FUNCTION_NEW,
    "public target rendering",
  )

  if "def _phase159_project_generic_semantics_to_public_proof(" not in renderer_text:
    if NORMALIZER_ANCHOR not in renderer_text:
      raise RuntimeError(
        "normalizer insertion anchor not found"
      )
    renderer_text = renderer_text.replace(
      NORMALIZER_ANCHOR,
      PHASE159_HELPERS + "\n\n" + NORMALIZER_ANCHOR,
      1,
    )
    print("[apply] generic semantic public projection helpers")
  else:
    print("[already applied] generic semantic public projection helpers")

  renderer_text = replace_once(
    renderer_text,
    NORMALIZER_INSERT_OLD,
    NORMALIZER_INSERT_NEW,
    "public semantic projection call",
  )

  RENDERER.write_text(
    renderer_text,
    encoding="utf-8",
    newline="\n",
  )
  TEST.write_text(
    TEST_CONTENT,
    encoding="utf-8",
    newline="\n",
  )

  print("")
  print("Phase 159-R1-3 generic semantic public projection applied.")
  print(f"Backup: {backup_dir}")
  print("Production files changed: 1")
  print("Test files changed: 1")


if __name__ == "__main__":
  main()
