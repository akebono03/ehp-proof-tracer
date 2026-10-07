from pathlib import Path

TEST_FILE = Path(
  "tests/test_phase159_pi_nplus1_n_stable_transport.py"
)

TEST = 'from tests.test_phase143_19_method_evidence import (\n  _method_evidence_data,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\n\n\ndef _render(\n  n: int,\n) -> str:\n  presentation, _, _, _ = (\n    _method_evidence_data(\n      n,\n      1,\n    )\n  )\n\n  return (\n    render_toda_group_proof_narrative_markdown(\n      presentation\n    )\n  )\n\n\ndef test_phase159_repair3_pi5_4_reference_is_general_toda45_and_prop51():\n  rendered = _render(\n    4\n  )\n\n  assert (\n    "**[R1] (4.5).**"\n    in rendered\n  )\n  assert (\n    r"$n \\ge k + 2$ のとき, "\n    r"$E^{m-n}: "\n    r"\\pi_{n+k}^{n} "\n    r"\\to "\n    r"\\pi_{m+k}^{m}$ は同型."\n    in rendered\n  )\n  assert (\n    "**[R2] Proposition 5.1.**"\n    in rendered\n  )\n  assert (\n    r"$\\pi_{4}^{3} = "\n    r"\\mathbb{Z}/2\\{\\eta_{3}\\}$."\n    in rendered\n  )\n\n\ndef test_phase159_repair3_pi5_4_body_is_target_local_specialization():\n  rendered = _render(\n    4\n  )\n  proof_body = rendered.split(\n    "## 証明\\n\\n",\n    1,\n  )[1]\n\n  assert (\n    r"[R1]を $(n,m,k)=(3,4,1)$ "\n    r"に適用すると, "\n    r"$E: \\pi_{4}^{3} "\n    r"\\to \\pi_{5}^{4}$ は同型."\n    in proof_body\n  )\n  assert (\n    r"$E\\eta_{3} = \\eta_{4}$."\n    in proof_body\n  )\n  assert (\n    r"$\\pi_{n + 1}^{n}"\n    not in proof_body\n  )\n  assert (\n    r"\\tag{"\n    not in proof_body\n  )\n\n\ndef test_phase159_repair3_pi_nplus1_n_family_uses_same_proof():\n  cases = (\n    (\n      5,\n      r"$(n,m,k)=(3,5,1)",\n      r"$E^{2}: \\pi_{4}^{3} "\n      r"\\to \\pi_{6}^{5}$ は同型.",\n      r"$E^{2}\\eta_{3} = \\eta_{5}$.",\n      r"$\\pi_{6}^{5} = "\n      r"\\mathbb{Z}/2\\{\\eta_{5}\\}$.",\n    ),\n    (\n      6,\n      r"$(n,m,k)=(3,6,1)",\n      r"$E^{3}: \\pi_{4}^{3} "\n      r"\\to \\pi_{7}^{6}$ は同型.",\n      r"$E^{3}\\eta_{3} = \\eta_{6}$.",\n      r"$\\pi_{7}^{6} = "\n      r"\\mathbb{Z}/2\\{\\eta_{6}\\}$.",\n    ),\n  )\n\n  for (\n    n,\n    specialization,\n    isomorphism,\n    generator_transport,\n    conclusion,\n  ) in cases:\n    rendered = _render(\n      n\n    )\n\n    assert (\n      "**[R1] (4.5).**"\n      in rendered\n    )\n    assert (\n      "**[R2] Proposition 5.1.**"\n      in rendered\n    )\n    assert (\n      specialization\n      in rendered\n    )\n    assert (\n      isomorphism\n      in rendered\n    )\n    assert (\n      generator_transport\n      in rendered\n    )\n    assert (\n      conclusion\n      in rendered\n    )\n\n\ndef test_phase159_repair3_pi4_3_delegates_to_existing_renderer():\n  rendered = _render(\n    3\n  )\n\n  assert (\n    r"\\operatorname{Im}\\Delta"\n    in rendered\n  )\n  assert (\n    r"\\ker E"\n    in rendered\n  )\n  assert (\n    r"$E: \\pi_{3}^{2} "\n    r"\\to \\pi_{4}^{3}$ は全射."\n    in rendered\n  )\n  assert (\n    r"$(n,m,k)=(3,3,1)"\n    not in rendered\n  )\n'

if not TEST_FILE.exists():
  raise RuntimeError(
    "Focused test file was not found. "
    "No file was changed."
  )

TEST_FILE.write_text(
  TEST,
  encoding="utf-8",
  newline="\n",
)

print(
  "Updated only the stale whitespace "
  "expectation in the focused test."
)
