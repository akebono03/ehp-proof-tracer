from pathlib import Path
import ast

RENDERER = Path(
  "toda_group_proof_narrative_renderer.py"
)
TEST_FILE = Path(
  "tests/test_phase159_pi_nplus1_n_stable_transport.py"
)

MARKER = (
  "# Phase159 pi_(n+1)^n stable transport "
  "repair3 public wrapper"
)

HELPER = 'def _phase159_repair3_render_pi_n_plus_1_n_stable_transport_narrative(\n  presentation: TodaGroupProofPresentation,\n) -> str | None:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n  sphere_dimension = target.sphere_dimension\n  group_dimension = target.group_dimension\n\n  if (\n    not isinstance(\n      sphere_dimension,\n      int,\n    )\n    or not isinstance(\n      group_dimension,\n      int,\n    )\n    or sphere_dimension < 4\n    or group_dimension != sphere_dimension + 1\n  ):\n    return None\n\n  target_n = sphere_dimension\n  suspension_exponent = target_n - 3\n  suspension_latex = (\n    "E"\n    if suspension_exponent == 1\n    else (\n      "E^{"\n      + str(\n        suspension_exponent\n      )\n      + "}"\n    )\n  )\n\n  return "\\n".join(\n    (\n      "# Group proof narrative",\n      "",\n      "## 証明対象",\n      "",\n      r"\\[",\n      (\n        r"\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"} = "\n        + r"\\mathbb{Z}/2\\{\\eta_{"\n        + str(\n          target_n\n        )\n        + r"}\\}."\n      ),\n      r"\\]",\n      "",\n      "## 使用する結果",\n      "",\n      "**[R1] (4.5).**",\n      (\n        r"$n \\ge k + 2$ のとき, "\n        r"$E^{m-n}: "\n        r"\\pi_{n+k}^{n} "\n        r"\\to "\n        r"\\pi_{m+k}^{m}$ は同型."\n      ),\n      "",\n      "**[R2] Proposition 5.1.**",\n      (\n        r"$\\pi_{4}^{3} = "\n        r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n      ),\n      "",\n      "---",\n      "",\n      "## 証明",\n      "",\n      (\n        r"$\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"}$ の群構造を決定する."\n      ),\n      "",\n      (\n        r"[R2]より, "\n        r"$\\pi_{4}^{3} = "\n        r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n      ),\n      "",\n      (\n        r"[R1]を "\n        r"$(n,m,k)=(3,"\n        + str(\n          target_n\n        )\n        + r",1)$ に適用すると, "\n        r"$"\n        + suspension_latex\n        + r": \\pi_{4}^{3} "\n        r"\\to "\n        r"\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"}$ は同型."\n      ),\n      "",\n      (\n        r"$"\n        + suspension_latex\n        + r"\\eta_{3} = "\n        r"\\eta_{"\n        + str(\n          target_n\n        )\n        + r"}$."\n      ),\n      "",\n      (\n        r"以上より, "\n        r"$\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"} = "\n        r"\\mathbb{Z}/2\\{\\eta_{"\n        + str(\n          target_n\n        )\n        + r"}\\}$."\n      ),\n      "",\n      "□",\n      "",\n    )\n  )\n'
WRAPPER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  stable_transport_narrative = (\n    _phase159_repair3_render_pi_n_plus_1_n_stable_transport_narrative(\n      presentation\n    )\n  )\n\n  if stable_transport_narrative is not None:\n    return stable_transport_narrative\n\n  return (\n    _phase159_repair3_previous_public_narrative_renderer(\n      presentation\n    )\n  )\n'
TEST = 'from tests.test_phase143_19_method_evidence import (\n  _method_evidence_data,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\n\n\ndef _render(\n  n: int,\n) -> str:\n  presentation, _, _, _ = (\n    _method_evidence_data(\n      n,\n      1,\n    )\n  )\n\n  return (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n\ndef test_phase159_repair3_pi5_4_reference_is_general_toda45_and_prop51():\n  rendered = _render(\n    4\n  )\n\n  assert (\n    "**[R1] (4.5).**"\n    in rendered\n  )\n  assert (\n    r"$n \\ge k + 2$ のとき, "\n    r"$E^{m-n}: "\n    r"\\pi_{n+k}^{n} "\n    r"\\to "\n    r"\\pi_{m+k}^{m}$ は同型."\n    in rendered\n  )\n  assert (\n    "**[R2] Proposition 5.1.**"\n    in rendered\n  )\n  assert (\n    r"$\\pi_{4}^{3} = "\n    r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n    in rendered\n  )\n\n\ndef test_phase159_repair3_pi5_4_body_is_target_local_specialization():\n  rendered = _render(\n    4\n  )\n  proof_body = rendered.split(\n    "## 証明\\n\\n",\n    1,\n  )[1]\n\n  assert (\n    r"[R1]を $(n,m,k)=(3,4,1) "\n    r"に適用すると, "\n    r"$E: \\pi_{4}^{3} "\n    r"\\to \\pi_{5}^{4}$ は同型."\n    in proof_body\n  )\n  assert (\n    r"$E\\eta_{3} = \\eta_{4}$."\n    in proof_body\n  )\n  assert (\n    r"$\\pi_{n + 1}^{n}"\n    not in proof_body\n  )\n  assert (\n    r"\\tag{"\n    not in proof_body\n  )\n\n\ndef test_phase159_repair3_pi_nplus1_n_family_uses_same_proof():\n  cases = (\n    (\n      5,\n      r"$(n,m,k)=(3,5,1)",\n      r"$E^{2}: \\pi_{4}^{3} "\n      r"\\to \\pi_{6}^{5}$ は同型.",\n      r"$E^{2}\\eta_{3} = \\eta_{5}$.",\n      r"$\\pi_{6}^{5} = "\n      r"\\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n    ),\n    (\n      6,\n      r"$(n,m,k)=(3,6,1)",\n      r"$E^{3}: \\pi_{4}^{3} "\n      r"\\to \\pi_{7}^{6}$ は同型.",\n      r"$E^{3}\\eta_{3} = \\eta_{6}$.",\n      r"$\\pi_{7}^{6} = "\n      r"\\mathbb{Z}/2\\{\\eta_{6}\\}$.",\n    ),\n  )\n\n  for (\n    n,\n    specialization,\n    isomorphism,\n    generator_transport,\n    conclusion,\n  ) in cases:\n    rendered = _render(\n      n\n    )\n\n    assert (\n      "**[R1] (4.5).**"\n      in rendered\n    )\n    assert (\n      "**[R2] Proposition 5.1.**"\n      in rendered\n    )\n    assert (\n      specialization\n      in rendered\n    )\n    assert (\n      isomorphism\n      in rendered\n    )\n    assert (\n      generator_transport\n      in rendered\n    )\n    assert (\n      conclusion\n      in rendered\n    )\n\n\ndef test_phase159_repair3_pi4_3_delegates_to_existing_renderer():\n  rendered = _render(\n    3\n  )\n\n  assert (\n    r"\\operatorname{Im}\\Delta"\n    in rendered\n  )\n  assert (\n    r"\\ker E"\n    in rendered\n  )\n  assert (\n    r"$E: \\pi_{3}^{2} "\n    r"\\to \\pi_{4}^{3}$ は全射."\n    in rendered\n  )\n  assert (\n    r"$(n,m,k)=(3,3,1)"\n    not in rendered\n  )\n'


if not RENDERER.exists():
  raise RuntimeError(
    "toda_group_proof_narrative_renderer.py "
    "was not found"
  )

source = RENDERER.read_text(
  encoding="utf-8"
)

tree = ast.parse(
  source
)
public_defs = tuple(
  node
  for node in tree.body
  if isinstance(
    node,
    ast.FunctionDef,
  )
  and node.name
  == "render_toda_group_proof_narrative_markdown"
)

print(
  "Existing top-level public renderer definitions:",
  len(
    public_defs
  ),
)

if not public_defs:
  raise RuntimeError(
    "No public Narrative renderer definition "
    "was found. No file was changed."
  )

if MARKER in source:
  print(
    "repair3 wrapper is already present; "
    "production file unchanged."
  )
else:
  appended = (
    source.rstrip()
    + "\n\n\n"
    + MARKER
    + "\n"
    + "_phase159_repair3_previous_public_narrative_renderer = (\n"
    + "  render_toda_group_proof_narrative_markdown\n"
    + ")\n\n"
    + HELPER
    + "\n\n"
    + WRAPPER
    + "\n"
  )

  ast.parse(
    appended
  )

  RENDERER.write_text(
    appended,
    encoding="utf-8",
    newline="\n",
  )

  print(
    "Appended repair3 public wrapper without "
    "modifying the existing renderer body."
  )

TEST_FILE.write_text(
  TEST,
  encoding="utf-8",
  newline="\n",
)

print(
  f"Wrote {TEST_FILE}"
)
