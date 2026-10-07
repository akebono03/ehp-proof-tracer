from pathlib import Path
import ast

RENDERER = Path("toda_group_proof_narrative_renderer.py")
TEST_FILE = Path(
  "tests/test_phase159_pi_nplus1_n_stable_transport.py"
)

HELPER = 'def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(\n  presentation: TodaGroupProofPresentation,\n) -> str | None:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  target = (\n    presentation\n    .source_replay\n    .group_result\n    .target\n  )\n  sphere_dimension = (\n    target.sphere_dimension\n  )\n  group_dimension = (\n    target.group_dimension\n  )\n\n  if (\n    not isinstance(\n      sphere_dimension,\n      int,\n    )\n    or not isinstance(\n      group_dimension,\n      int,\n    )\n    or sphere_dimension < 4\n    or group_dimension\n    != sphere_dimension + 1\n  ):\n    return None\n\n  target_n = sphere_dimension\n  suspension_exponent = (\n    target_n - 3\n  )\n  suspension_latex = (\n    "E"\n    if suspension_exponent == 1\n    else (\n      "E^{"\n      + str(\n        suspension_exponent\n      )\n      + "}"\n    )\n  )\n\n  return "\\n".join(\n    (\n      "# Group proof narrative",\n      "",\n      "## 証明対象",\n      "",\n      r"\\[",\n      (\n        r"\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"} = "\n        + r"\\mathbb{Z}/2\\{\\eta_{"\n        + str(\n          target_n\n        )\n        + r"}\\}."\n      ),\n      r"\\]",\n      "",\n      "## 使用する結果",\n      "",\n      "**[R1] (4.5).**",\n      (\n        r"$n \\ge k + 2$ のとき, "\n        r"$E^{m-n}: "\n        r"\\pi_{n+k}^{n} "\n        r"\\to "\n        r"\\pi_{m+k}^{m}$ は同型."\n      ),\n      "",\n      "**[R2] Proposition 5.1.**",\n      (\n        r"$\\pi_{4}^{3} = "\n        r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n      ),\n      "",\n      "---",\n      "",\n      "## 証明",\n      "",\n      (\n        r"$\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"}$ の群構造を決定する."\n      ),\n      "",\n      (\n        r"[R2]より, "\n        r"$\\pi_{4}^{3} = "\n        r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n      ),\n      "",\n      (\n        r"[R1]を "\n        r"$(n,m,k)=(3,"\n        + str(\n          target_n\n        )\n        + r",1)$ に適用すると, "\n        r"$"\n        + suspension_latex\n        + r": \\pi_{4}^{3} "\n        r"\\to "\n        r"\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"}$ は同型."\n      ),\n      "",\n      (\n        r"$"\n        + suspension_latex\n        + r"\\eta_{3} = "\n        r"\\eta_{"\n        + str(\n          target_n\n        )\n        + r"}$."\n      ),\n      "",\n      (\n        r"以上より, "\n        r"$\\pi_{"\n        + str(\n          target_n + 1\n        )\n        + r"}^{"\n        + str(\n          target_n\n        )\n        + r"} = "\n        r"\\mathbb{Z}/2\\{\\eta_{"\n        + str(\n          target_n\n        )\n        + r"}\\}$."\n      ),\n      "",\n      "□",\n      "",\n    )\n  )\n'
RENDER = 'def render_toda_group_proof_narrative_markdown(\n  presentation: TodaGroupProofPresentation,\n) -> str:\n  stable_transport_narrative = (\n    _phase159_render_pi_n_plus_1_n_stable_transport_narrative(\n      presentation\n    )\n  )\n\n  if stable_transport_narrative is not None:\n    return stable_transport_narrative\n\n  rendered = (\n    _phase158_baseline_render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n  rendered = (\n    _phase158_normalize_public_narrative_contract(\n      presentation,\n      rendered,\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_map_property_prose(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning(\n      rendered\n    )\n  )\n  rendered = (\n    _phase159_r1_7c_r4_reorder_public_equation_reference_conclusions(\n      rendered\n    )\n  )\n\n  return (\n    _phase159_r1_6d_finalize_reference_and_linkage(\n      presentation,\n      _phase159_order_public_unique_preimage_definition_premises(\n        presentation,\n        rendered,\n      ),\n    )\n  )\n'
TEST = 'from tests.test_phase143_19_method_evidence import (\n  _method_evidence_data,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\n\n\ndef _render(\n  n: int,\n) -> str:\n  presentation, _, _, _ = (\n    _method_evidence_data(\n      n,\n      1,\n    )\n  )\n\n  return (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n\ndef test_phase159_pi5_4_uses_prop51_and_general_toda45_reference():\n  rendered = _render(\n    4\n  )\n\n  assert (\n    "**[R1] (4.5).**"\n    in rendered\n  )\n  assert (\n    r"$n \\ge k + 2$ のとき, "\n    r"$E^{m-n}: "\n    r"\\pi_{n+k}^{n} "\n    r"\\to "\n    r"\\pi_{m+k}^{m}$ は同型."\n    in rendered\n  )\n  assert (\n    "**[R2] Proposition 5.1.**"\n    in rendered\n  )\n  assert (\n    r"$\\pi_{4}^{3} = "\n    r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n    in rendered\n  )\n\n\ndef test_phase159_pi5_4_specializes_toda45_in_proof_body():\n  rendered = _render(\n    4\n  )\n  proof_body = rendered.split(\n    "## 証明\\n\\n",\n    1,\n  )[1]\n\n  assert (\n    r"[R1]を $(n,m,k)=(3,4,1) "\n    r"に適用すると, "\n    r"$E: \\pi_{4}^{3} "\n    r"\\to \\pi_{5}^{4}$ は同型."\n    in proof_body\n  )\n  assert (\n    r"$E\\eta_{3} = \\eta_{4}$."\n    in proof_body\n  )\n  assert (\n    r"$\\pi_{n + 1}^{n}"\n    not in proof_body\n  )\n  assert (\n    r"\\tag{"\n    not in proof_body\n  )\n\n\ndef test_phase159_pi_nplus1_n_family_uses_same_stable_transport_proof():\n  cases = (\n    (\n      5,\n      r"$E^{2}: \\pi_{4}^{3} "\n      r"\\to \\pi_{6}^{5}$ は同型.",\n      r"$E^{2}\\eta_{3} = \\eta_{5}$.",\n      r"$\\pi_{6}^{5} = "\n      r"\\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n    ),\n    (\n      6,\n      r"$E^{3}: \\pi_{4}^{3} "\n      r"\\to \\pi_{7}^{6}$ は同型.",\n      r"$E^{3}\\eta_{3} = \\eta_{6}$.",\n      r"$\\pi_{7}^{6} = "\n      r"\\mathbb{Z}/2\\{\\eta_{6}\\}$.",\n    ),\n  )\n\n  for (\n    n,\n    isomorphism,\n    generator_transport,\n    conclusion,\n  ) in cases:\n    rendered = _render(\n      n\n    )\n\n    assert (\n      "**[R1] (4.5).**"\n      in rendered\n    )\n    assert (\n      "**[R2] Proposition 5.1.**"\n      in rendered\n    )\n    assert (\n      isomorphism\n      in rendered\n    )\n    assert (\n      generator_transport\n      in rendered\n    )\n    assert (\n      conclusion\n      in rendered\n    )\n\n\ndef test_phase159_pi4_3_does_not_use_stable_transport_family_renderer():\n  rendered = _render(\n    3\n  )\n\n  assert (\n    r"\\pi_{4}^{3} = "\n    r"\\mathbb{Z}/2\\{\\eta_{3}\\}"\n    in rendered\n  )\n  assert (\n    r"$(n,m,k)=(3,3,1)"\n    not in rendered\n  )\n  assert (\n    r"\\operatorname{Im}\\Delta"\n    in rendered\n  )\n'


def function_span(
  source: str,
  name: str,
) -> tuple[int, int]:
  tree = ast.parse(
    source
  )
  node = next(
    (
      item
      for item in tree.body
      if isinstance(
        item,
        (
          ast.FunctionDef,
          ast.AsyncFunctionDef,
        ),
      )
      and item.name == name
    ),
    None,
  )

  if node is None:
    raise RuntimeError(
      f"function not found: {name}"
    )

  lines = source.splitlines(
    keepends=True
  )
  start = sum(
    len(
      line
    )
    for line in lines[
      :node.lineno - 1
    ]
  )
  end = sum(
    len(
      line
    )
    for line in lines[
      :node.end_lineno
    ]
  )
  return (
    start,
    end,
  )


if not RENDERER.exists():
  raise RuntimeError(
    "toda_group_proof_narrative_renderer.py "
    "was not found"
  )

source = RENDERER.read_text(
  encoding="utf-8"
)

required_names = (
  "_phase158_baseline_render_toda_group_proof_narrative_markdown",
  "_phase158_normalize_public_narrative_contract",
  "_phase159_r1_7c_r4_normalize_public_map_property_prose",
  "_phase159_r1_7c_r4_normalize_public_numbered_map_property_reasoning",
  "_phase159_r1_7c_r4_reorder_public_equation_reference_conclusions",
  "_phase159_r1_6d_finalize_reference_and_linkage",
  "_phase159_order_public_unique_preimage_definition_premises",
)

missing = tuple(
  name
  for name in required_names
  if name not in source
)

if missing:
  raise RuntimeError(
    "Current local renderer is missing expected "
    "Phase159 cumulative helpers: "
    + ", ".join(
      missing
    )
    + ". No file was changed."
  )

helper_name = (
  "_phase159_render_pi_n_plus_1_n_stable_transport_narrative"
)

if helper_name in source:
  helper_start, helper_end = (
    function_span(
      source,
      helper_name,
    )
  )
  source = (
    source[:helper_start]
    + source[helper_end:]
  )

render_start, render_end = (
  function_span(
    source,
    "render_toda_group_proof_narrative_markdown",
  )
)

updated = (
  source[:render_start]
  + HELPER
  + "\n\n"
  + RENDER
  + source[render_end:]
)

ast.parse(
  updated
)

RENDERER.write_text(
  updated,
  encoding="utf-8",
  newline="\n",
)

TEST_FILE.write_text(
  TEST,
  encoding="utf-8",
  newline="\n",
)

print(
  "Applied Phase159 pi_(n+1)^n stable "
  "transport repair2."
)
print(
  "Preserved current local cumulative "
  "Phase159 helpers."
)
print(
  f"Wrote {TEST_FILE}"
)
