from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / "proof.py"
BOOTSTRAP = ROOT / "toda_upstream_bootstrap.py"
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_6a_foundational_reference_identity.py"

FOUNDATIONAL_CLASS = '@dataclass(frozen=True)\nclass FoundationalReferenceIdentity:\n  key: str\n  label: str\n\n  def __post_init__(self) -> None:\n    if not isinstance(\n      self.key,\n      str,\n    ):\n      raise TypeError(\n        "key must be a str"\n      )\n\n    if not self.key:\n      raise ValueError(\n        "key must not be empty"\n      )\n\n    if not isinstance(\n      self.label,\n      str,\n    ):\n      raise TypeError(\n        "label must be a str"\n      )\n\n    if not self.label:\n      raise ValueError(\n        "label must not be empty"\n      )\n\n\n'
OLD_PROOF_STEP = '@dataclass(frozen=True)\nclass ProofStep:\n  conclusion: Any\n  premises: tuple[Any, ...]\n  rule: ProofRule\n  note: str | None = None\n  inference_rule: InferenceRule | None = None\n'
NEW_PROOF_STEP = '@dataclass(frozen=True)\nclass ProofStep:\n  conclusion: Any\n  premises: tuple[Any, ...]\n  rule: ProofRule\n  note: str | None = None\n  inference_rule: InferenceRule | None = None\n  foundational_reference: (\n    FoundationalReferenceIdentity\n    | None\n  ) = None\n'
OLD_BUILD = 'def _build_phase49_result():\n  pi_2_1 = TodaPrimaryGroup(\n    group_dimension=2,\n    sphere_dimension=1,\n  )\n  pi_3_2 = TodaPrimaryGroup(\n    group_dimension=3,\n    sphere_dimension=2,\n  )\n  pi_3_3 = TodaPrimaryGroup(\n    group_dimension=3,\n    sphere_dimension=3,\n  )\n  pi_1_1 = TodaPrimaryGroup(\n    group_dimension=1,\n    sphere_dimension=1,\n  )\n  pi_2_2 = TodaPrimaryGroup(\n    group_dimension=2,\n    sphere_dimension=2,\n  )\n\n  premise_steps = (\n    ProofStep(\n      conclusion=pi_2_1_zero_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=pi_3_3_free_cyclic_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=e_pi_1_1_to_pi_2_2_isomorphism_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=TodaProp42ExactnessStatement(\n        window=TodaEHPExactnessWindow(\n          source_term=pi_2_1,\n          middle_term=pi_3_2,\n          target_term=pi_3_3,\n          first_map=EHP_E_MAP,\n          second_map=EHP_H_MAP,\n        ),\n      ),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=TodaProp42ExactnessStatement(\n        window=TodaEHPExactnessWindow(\n          source_term=pi_3_2,\n          middle_term=pi_3_3,\n          target_term=pi_1_1,\n          first_map=EHP_H_MAP,\n          second_map=EHP_DELTA_MAP,\n        ),\n      ),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=TodaProp42ExactnessStatement(\n        window=TodaEHPExactnessWindow(\n          source_term=pi_3_3,\n          middle_term=pi_1_1,\n          target_term=pi_2_2,\n          first_map=EHP_DELTA_MAP,\n          second_map=EHP_E_MAP,\n        ),\n      ),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n  )\n\n  rules = (\n    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),\n    toda_suspension_isomorphism_implies_injective_inference_rule(),\n    toda_exactness_injective_right_implies_delta_zero_inference_rule(),\n    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),\n    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),\n    toda_pi3_2_define_eta2_inference_rule(),\n    toda_pi3_2_eta2_hopf_relation_inference_rule(),\n    toda_pi3_2_free_cyclic_generator_inference_rule(),\n  )\n\n  result = run_inference_until_stable_with_history(\n    rules,\n    premise_steps,\n  )\n\n  return {\n    "premise_steps": premise_steps,\n    "rules": rules,\n    "result": result,\n  }\n'
NEW_BUILD = 'def _build_phase49_result():\n  pi_2_1 = TodaPrimaryGroup(\n    group_dimension=2,\n    sphere_dimension=1,\n  )\n  pi_3_2 = TodaPrimaryGroup(\n    group_dimension=3,\n    sphere_dimension=2,\n  )\n  pi_3_3 = TodaPrimaryGroup(\n    group_dimension=3,\n    sphere_dimension=3,\n  )\n  pi_1_1 = TodaPrimaryGroup(\n    group_dimension=1,\n    sphere_dimension=1,\n  )\n  pi_2_2 = TodaPrimaryGroup(\n    group_dimension=2,\n    sphere_dimension=2,\n  )\n\n  premise_steps = (\n    ProofStep(\n      conclusion=pi_2_1_zero_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n      foundational_reference=(\n        FoundationalReferenceIdentity(\n          key="sphere.circle.higher_zero",\n          label=(\n            "Circle higher homotopy vanishing"\n          ),\n        )\n      ),\n    ),\n    ProofStep(\n      conclusion=pi_3_3_free_cyclic_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n      foundational_reference=(\n        FoundationalReferenceIdentity(\n          key="sphere.identity_group",\n          label="Sphere identity group",\n        )\n      ),\n    ),\n    ProofStep(\n      conclusion=e_pi_1_1_to_pi_2_2_isomorphism_fact(),\n      premises=(),\n      rule=ProofRule.GIVEN,\n      foundational_reference=(\n        FoundationalReferenceIdentity(\n          key=(\n            "sphere.low_dimensional."\n            "suspension_isomorphism"\n          ),\n          label=(\n            "Low-dimensional suspension "\n            "isomorphism"\n          ),\n        )\n      ),\n    ),\n    ProofStep(\n      conclusion=TodaProp42ExactnessStatement(\n        window=TodaEHPExactnessWindow(\n          source_term=pi_2_1,\n          middle_term=pi_3_2,\n          target_term=pi_3_3,\n          first_map=EHP_E_MAP,\n          second_map=EHP_H_MAP,\n        ),\n      ),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=TodaProp42ExactnessStatement(\n        window=TodaEHPExactnessWindow(\n          source_term=pi_3_2,\n          middle_term=pi_3_3,\n          target_term=pi_1_1,\n          first_map=EHP_H_MAP,\n          second_map=EHP_DELTA_MAP,\n        ),\n      ),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n    ProofStep(\n      conclusion=TodaProp42ExactnessStatement(\n        window=TodaEHPExactnessWindow(\n          source_term=pi_3_3,\n          middle_term=pi_1_1,\n          target_term=pi_2_2,\n          first_map=EHP_DELTA_MAP,\n          second_map=EHP_E_MAP,\n        ),\n      ),\n      premises=(),\n      rule=ProofRule.GIVEN,\n    ),\n  )\n\n  rules = (\n    toda_exactness_zero_left_implies_hopf_injective_inference_rule(),\n    toda_suspension_isomorphism_implies_injective_inference_rule(),\n    toda_exactness_injective_right_implies_delta_zero_inference_rule(),\n    toda_exactness_zero_delta_implies_hopf_surjective_inference_rule(),\n    toda_hopf_injective_surjective_implies_isomorphism_inference_rule(),\n    toda_pi3_2_define_eta2_inference_rule(),\n    toda_pi3_2_eta2_hopf_relation_inference_rule(),\n    toda_pi3_2_free_cyclic_generator_inference_rule(),\n  )\n\n  result = run_inference_until_stable_with_history(\n    rules,\n    premise_steps,\n  )\n\n  return {\n    "premise_steps": premise_steps,\n    "rules": rules,\n    "result": result,\n  }\n'
HELPERS = 'def _phase159_foundational_reference_statement(\n  proof_step: ProofStep,\n) -> str:\n  map_property = (\n    _phase159_public_formula_map_property_line(\n      proof_step\n    )\n  )\n\n  if map_property is not None:\n    return map_property\n\n  rendered = (\n    _render_generic_narrative_step(\n      proof_step\n    )\n  )\n\n  if rendered.endswith("$"):\n    return (\n      rendered\n      + "."\n    )\n\n  return rendered\n\n\ndef _phase159_render_foundational_reference_section(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  entries = []\n  index_by_key = {}\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n    identity = (\n      proof_step.foundational_reference\n    )\n\n    if identity is None:\n      continue\n\n    if not isinstance(\n      identity,\n      FoundationalReferenceIdentity,\n    ):\n      raise TypeError(\n        "foundational_reference must be a "\n        "FoundationalReferenceIdentity or None"\n      )\n\n    existing_index = index_by_key.get(\n      identity.key\n    )\n\n    if existing_index is None:\n      index_by_key[\n        identity.key\n      ] = len(\n        entries\n      )\n      entries.append(\n        [\n          identity,\n          [\n            proof_step,\n          ],\n        ]\n      )\n      continue\n\n    entries[\n      existing_index\n    ][\n      1\n    ].append(\n      proof_step\n    )\n\n  if not entries:\n    return ""\n\n  lines = []\n\n  for number, (\n    identity,\n    proof_steps,\n  ) in enumerate(\n    entries,\n    start=1,\n  ):\n    lines.append(\n      "**[F"\n      + str(\n        number\n      )\n      + "] "\n      + identity.label\n      + ".**"\n    )\n\n    seen_statements = set()\n\n    for proof_step in proof_steps:\n      statement = (\n        _phase159_foundational_reference_statement(\n          proof_step\n        )\n      )\n\n      if statement in seen_statements:\n        continue\n\n      seen_statements.add(\n        statement\n      )\n      lines.append(\n        statement\n      )\n\n  return "\\n".join(\n    lines\n  )\n\n\ndef _phase159_inject_foundational_reference_section(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  foundational = (\n    _phase159_render_foundational_reference_section(\n      presentation\n    )\n  )\n\n  if not foundational:\n    return rendered\n\n  reference_marker = (\n    "## 使用する結果\\n\\n"\n  )\n  proof_boundary = (\n    "\\n---\\n\\n## 証明"\n  )\n  reference_start = rendered.find(\n    reference_marker\n  )\n\n  if reference_start < 0:\n    return rendered\n\n  content_start = (\n    reference_start\n    + len(\n      reference_marker\n    )\n  )\n  boundary_index = rendered.find(\n    proof_boundary,\n    content_start,\n  )\n\n  if boundary_index < 0:\n    return rendered\n\n  existing = rendered[\n    content_start:\n    boundary_index\n  ].strip()\n\n  if existing:\n    replacement = (\n      existing\n      + "\\n\\n"\n      + foundational\n    )\n  else:\n    replacement = foundational\n\n  return (\n    rendered[\n      :content_start\n    ]\n    + replacement\n    + rendered[\n      boundary_index:\n    ]\n  )\n'
OLD_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n\n  return (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n'
NEW_RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_normalize_public_map_property_wording(\n      presentation,\n      rendered,\n    )\n  )\n\n  return (\n    _phase159_inject_foundational_reference_section(\n      presentation,\n      rendered,\n    )\n  )\n'
TEST_CONTENT = 'from low_dimensional_facts import (\n  e_pi_1_1_to_pi_2_2_isomorphism_fact,\n  pi_2_1_zero_fact,\n  pi_3_3_free_cyclic_fact,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _phase159_r1_6a_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report.candidates[\n      0\n    ].source_candidate.group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef test_phase159_r1_6a_pi3_2_foundational_premises_keep_identity():\n  presentation = (\n    _phase159_r1_6a_pi3_2_presentation()\n  )\n\n  expected = {\n    pi_2_1_zero_fact():\n      "sphere.circle.higher_zero",\n    pi_3_3_free_cyclic_fact():\n      "sphere.identity_group",\n    e_pi_1_1_to_pi_2_2_isomorphism_fact():\n      (\n        "sphere.low_dimensional."\n        "suspension_isomorphism"\n      ),\n  }\n\n  found = {}\n\n  for node in presentation.nodes:\n    proof_step = node.proof_step\n\n    if proof_step.conclusion not in expected:\n      continue\n\n    identity = (\n      proof_step.foundational_reference\n    )\n\n    assert identity is not None\n\n    found[\n      proof_step.conclusion\n    ] = identity.key\n\n  assert found == expected\n\n\ndef test_phase159_r1_6a_pi3_2_root_is_not_foundational_reference():\n  presentation = (\n    _phase159_r1_6a_pi3_2_presentation()\n  )\n\n  assert (\n    presentation.root_step\n    .foundational_reference\n    is None\n  )\n\n\ndef test_phase159_r1_6a_pi3_2_public_reference_section_shows_foundational_facts():\n  presentation = (\n    _phase159_r1_6a_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  reference_section = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert (\n    "Circle higher homotopy vanishing"\n    in reference_section\n  )\n  assert (\n    "Sphere identity group"\n    in reference_section\n  )\n  assert (\n    "Low-dimensional suspension isomorphism"\n    in reference_section\n  )\n  assert (\n    r"$\\pi_{2}^{1} = 0$."\n    in reference_section\n  )\n  assert (\n    r"$\\pi_{3}^{3} = "\n    r"\\mathbb{Z}\\{\\iota_{3}\\}$."\n    in reference_section\n  )\n  assert (\n    r"$E: \\pi_{1}^{1} \\to "\n    r"\\pi_{2}^{2}$ は同型."\n    in reference_section\n  )\n\n\ndef test_phase159_r1_6a_pi3_2_target_is_not_reintroduced_as_reference():\n  presentation = (\n    _phase159_r1_6a_pi3_2_presentation()\n  )\n  rendered = (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n  reference_section = (\n    rendered.split(\n      "## 使用する結果\\n\\n",\n      1,\n    )[1].split(\n      "\\n---\\n",\n      1,\n    )[0]\n  )\n\n  assert (\n    r"\\pi_{3}^{2} = "\n    r"\\mathbb{Z}\\{\\eta_{2}\\}"\n    not in reference_section\n  )\n  assert (\n    "Proposition 5.1"\n    not in reference_section\n  )\n'

def ensure_import_name(source, module_name, import_name):
  start_marker = "from " + module_name + " import (\n"
  start = source.find(start_marker)
  if start < 0:
    raise RuntimeError("import block not found: " + module_name)
  end = source.find(")\n", start)
  if end < 0:
    raise RuntimeError("import block end not found: " + module_name)
  block = source[start:end + 2]
  line = "  " + import_name + ",\n"
  if line in block:
    return source
  updated = block[:-2] + line + ")\n"
  return source[:start] + updated + source[end + 2:]

def replace_once(source, old, new, label):
  count = source.count(old)
  if count != 1:
    raise RuntimeError(
      label + ": expected exactly one match, found " + str(count)
    )
  return source.replace(old, new, 1)

def main():
  for path in (PROOF, BOOTSTRAP, RENDERER):
    if not path.exists():
      raise FileNotFoundError(path)

  stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
  backup_dir = ROOT / ("phase159_r1_6a_backup_" + stamp)
  backup_dir.mkdir(parents=True, exist_ok=False)

  for path in (PROOF, BOOTSTRAP, RENDERER):
    shutil.copy2(path, backup_dir / path.name)

  proof_source = PROOF.read_text(encoding="utf-8-sig")
  literature_end = (
    "class LiteratureReference:\n"
    "  label: str\n"
    "  author: str | None = None\n"
    "  title: str | None = None\n"
    "  year: int | None = None\n"
    "  locator: str | None = None\n\n\n"
  )
  if "class FoundationalReferenceIdentity:" not in proof_source:
    proof_source = replace_once(
      proof_source,
      literature_end,
      literature_end + FOUNDATIONAL_CLASS,
      "FoundationalReferenceIdentity anchor",
    )
  proof_source = replace_once(
    proof_source,
    OLD_PROOF_STEP,
    NEW_PROOF_STEP,
    "ProofStep",
  )
  PROOF.write_text(proof_source, encoding="utf-8", newline="\n")

  bootstrap_source = BOOTSTRAP.read_text(encoding="utf-8-sig")
  bootstrap_source = ensure_import_name(
    bootstrap_source,
    "proof",
    "FoundationalReferenceIdentity",
  )
  bootstrap_source = replace_once(
    bootstrap_source,
    OLD_BUILD,
    NEW_BUILD,
    "_build_phase49_result",
  )
  BOOTSTRAP.write_text(bootstrap_source, encoding="utf-8", newline="\n")

  renderer_source = RENDERER.read_text(encoding="utf-8-sig")
  renderer_source = ensure_import_name(
    renderer_source,
    "proof",
    "FoundationalReferenceIdentity",
  )
  render_anchor = "def render_toda_group_proof_narrative_markdown("
  render_index = renderer_source.find(render_anchor)
  if render_index < 0:
    raise RuntimeError("public render function not found")
  if "def _phase159_render_foundational_reference_section(" not in renderer_source:
    renderer_source = (
      renderer_source[:render_index]
      + HELPERS.rstrip()
      + "\n\n\n"
      + renderer_source[render_index:]
    )
  renderer_source = replace_once(
    renderer_source,
    OLD_RENDER,
    NEW_RENDER,
    "render_toda_group_proof_narrative_markdown",
  )
  RENDERER.write_text(renderer_source, encoding="utf-8", newline="\n")

  TEST.write_text(TEST_CONTENT, encoding="utf-8", newline="\n")

  print("Phase 159-R1-6a applied.")
  print("Backup:", backup_dir)
  print("Foundational identity is separate from LiteratureReference.")

if __name__ == "__main__":
  main()
