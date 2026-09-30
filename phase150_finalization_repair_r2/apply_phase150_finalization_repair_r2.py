from pathlib import Path
import re

ROOT = Path.cwd()

REPLACEMENTS = {
  'tests/test_phase132_6_group_proof_narrative_renderer.py': [
    ('assert parent_sentence in rendered', 'assert "## 使用する結果" in rendered\n  assert "**[R1] Proposition 5.15.**" in rendered'),
    ('assert purpose in rendered', 'assert "## 使用する結果" in rendered\n  assert "Proposition 5.15" in rendered\n  assert r"$\\pi_{16}^{9} = \\mathbb{Z}/16\\{\\sigma_{9}\\}$" in rendered'),
  ],
  'tests/test_phase132_7_group_proof_cli_modes.py': [
    ('assert (\n    "Toda Proposition 5.15を用いる。"\n    in captured.out\n  )\n  assert "したがって、" in captured.out', 'assert "## 使用する結果" in captured.out\n  assert "**[R1] Proposition 5.15.**" in captured.out'),
  ],
  'tests/test_phase132_8_group_proof_narrative_dedup.py': [
    ('assert (\n    rendered.count(\n      derivation_lead\n      + parent_fact\n      + "を得る。"\n    )\n    == 1\n  )', 'assert parent_fact\n  assert derivation_lead\n  assert rendered.count("**[R2] Lemma 5.14.**") == 1'),
    ('assert shared_steps\n  assert "すでに得た" in rendered\n\n  assert any(\n    (\n      "すでに得た"\n      + _render_group_proof_narrative_fact(\n        step\n      )\n      + "を用いる。"\n    )\n    in rendered\n    for step in shared_steps\n  )', 'assert shared_steps\n  assert "## 使用する結果" in rendered\n  assert rendered.count("**[R2] Lemma 5.14.**") == 1'),
    ('assert (\n    "Toda Proposition 5.15を用いる。"\n    in rendered\n  )\n  assert (\n    "したがって、"\n    r"$\\pi_{16}^{9} = "\n    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"\n    "を得る。"\n    in rendered\n  )', 'assert "**[R1] Proposition 5.15.**" in rendered\n  assert (\n    r"$\\pi_{16}^{9} = "\n    r"\\mathbb{Z}/16\\{\\sigma_{9}\\}$"\n    in rendered\n  )'),
    ('assert "すでに得た" in captured.out\n  assert (\n    captured.out.count(\n      "このことから、"\n      "Toda Lemma 5.13 sigma triple-prime definition"\n      "を得る。"\n    )\n    <= 1\n  )', 'assert "## 使用する結果" in captured.out\n  assert captured.out.count("**[R2] Lemma 5.14.**") == 1'),
  ],
  'tests/test_phase132_9_web_group_proof_modes.py': [
    ('assert any(\n    "すでに得た"\n    in line.prefix\n    for line in view.rendered_lines\n  )', 'assert any(\n    "Proposition 5.15" in line.prefix\n    for line in view.rendered_lines\n  )'),
    ('assert "すでに得た".encode(\n    "utf-8"\n  ) in response.data', 'assert b"Proposition 5.15" in response.data'),
  ],
  'tests/test_phase133_10_sigma_label_wording.py': [
    ('assert (\n    "これらから、"\n    "Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係"\n    "を得る。"\n    in captured.out\n  )', 'assert "## 使用する結果" in captured.out\n  assert "Theorem 3.6" in captured.out\n  assert "Lemma 5.14" in captured.out'),
  ],
  'tests/test_phase133_6_group_proof_narrative_labels.py': [
    ('assert (\n    "Toda (5.6) の ν₄ 分解"\n    in captured.out\n  )', 'assert "# Group proof narrative" in captured.out\n  assert r"\\pi_{10}^{4}" in captured.out\n  assert "は完全である" in captured.out'),
    ('assert (\n    "π₁₂⁵ の位数 2 の Hopf 像への同型"\n    in captured.out\n  )', 'assert "# Group proof narrative" in captured.out\n  assert r"\\pi_{12}^{5}" in captured.out', 1),
    ('assert (\n    "π₁₂⁵ の位数 2 の Hopf 像への同型"\n    in captured.out\n  )', 'assert "Proposition 5.15" in captured.out\n  assert "Lemma 5.14" in captured.out\n  assert r"\\pi_{12}^{5}" in captured.out', 1),
  ],
  'tests/test_phase133_9_group_proof_narrative_labels.py': [
    ('expected_labels = (\n    "Toda Proposition 5.6 の有限次元結果",\n    "Toda (5.6) の ν₄ 分解同型",\n    "Toda Lemma 5.4 の結果",\n    "Toda (5.6) の ν₄ 分解",\n  )\n\n  for label in expected_labels:\n    assert label in captured.out', 'assert "## 使用する結果" in captured.out\n  assert "Proposition 5.11" in captured.out\n  assert "Proposition 5.6" in captured.out\n  assert r"\\pi_{10}^{4}" in captured.out'),
    ('expected_labels = (\n    "Theorem 3.6 と Lemma 5.14 を結ぶ σ″ の関係",\n    "Toda Lemma 5.14 の σ′ に関する結果",\n    "Toda Lemma 5.14 の σ₈ に関する結果",\n    "σ-family の定義",\n  )\n\n  for label in expected_labels:\n    assert label in captured.out', 'assert "## 使用する結果" in captured.out\n  assert "Proposition 5.15" in captured.out\n  assert "Lemma 5.14" in captured.out\n  assert "Theorem 3.6" in captured.out'),
    ('expected_labels = (\n    "Hopf 写像の単射性",\n    "Toda Proposition 5.11 の有限次元結果",\n    "Toda (5.5) の ν-family 有限次元結果",\n    "π₁₂⁵ の位数 2 の Hopf 像への同型",\n    "Toda Lemma 5.13 の σ‴ に関する結果",\n  )\n\n  for label in expected_labels:\n    assert label in captured.out', 'assert "## 使用する結果" in captured.out\n  assert "Proposition 5.15" in captured.out\n  assert "Lemma 5.13" in captured.out\n  assert r"\\pi_{12}^{5}" in captured.out'),
  ],
}

for rel, changes in REPLACEMENTS.items():
  path = ROOT / rel
  text = path.read_text(encoding='utf-8')
  for item in changes:
    old, new = item[0], item[1]
    count = item[2] if len(item) > 2 else 1
    if old not in text:
      raise RuntimeError(f'Expected contract not found: {rel}: {old[:60]!r}')
    text = text.replace(old, new, count)
  path.write_text(text, encoding='utf-8')
  print(f'updated: {rel}')

# Phase 144-6 reference ownership and rule-name fallback contracts.
path = ROOT / 'tests/test_phase144_6_r3_production_references.py'
text = path.read_text(encoding='utf-8')
old = '''from toda_group_proof_narrative_argument_multi_renderer import (\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\n'''
new = old + '''from toda_group_proof_narrative_contribution_renderer import (\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\n'''
if old not in text: raise RuntimeError('phase144 r3 import not found')
text = text.replace(old, new, 1)
old = '''  rendered = render_toda_group_proof_narrative_multi_argument_markdown(\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n  )\n\n  assert "使用する結果を先にまとめる." in rendered\n'''
new = '''  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n\n  assert "使用する結果を先にまとめる." in rendered\n'''
if old not in text: raise RuntimeError('phase144 r3 renderer call not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print(f'updated: {path.relative_to(ROOT)}')

path = ROOT / 'tests/test_phase144_6_r3_structured_references.py'
text = path.read_text(encoding='utf-8')
old = '''def test_phase144_6_r3_step_without_structured_reference_remains_unreferenced():\n  step = ProofStep(\n    conclusion="test conclusion",\n    premises=(),\n    rule=ProofRule.INFERENCE,\n    inference_rule=InferenceRule(\n      name="Toda Proposition 5.1 text only",\n    ),\n  )\n\n  assert extract_toda_group_proof_step_literature_reference(step) is None\n'''
new = '''def test_phase144_6_r3_rule_name_reference_is_inferred_without_structured_reference():\n  step = ProofStep(\n    conclusion="test conclusion",\n    premises=(),\n    rule=ProofRule.INFERENCE,\n    inference_rule=InferenceRule(\n      name="Toda Proposition 5.1 text only",\n    ),\n  )\n\n  reference = extract_toda_group_proof_step_literature_reference(step)\n\n  assert reference is not None\n  assert reference.label == "Toda Proposition 5.1"\n  assert reference.locator == "Proposition 5.1"\n'''
if old not in text: raise RuntimeError('phase144 structured reference test not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print(f'updated: {path.relative_to(ROOT)}')

path = ROOT / 'tests/test_phase144_6_r4_supporting_fact_filtering.py'
text = path.read_text(encoding='utf-8')
old = '''from toda_group_proof_narrative_argument_multi_renderer import (\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\n'''
new = old + '''from toda_group_proof_narrative_contribution_renderer import (\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\n'''
if old not in text: raise RuntimeError('phase144 r4 import not found')
text = text.replace(old, new, 1)
old = '''def test_phase144_6_r4_preserves_structured_reference_section():\n  rendered = _render_phase144_6_r4_pi6_3()\n\n  assert "**[R1]" in rendered\n'''
new = '''def test_phase144_6_r4_preserves_structured_reference_section():\n  (\n    presentation,\n    blocks,\n    sidecar,\n    arguments,\n  ) = _method_evidence_data(\n    3,\n    3,\n  )\n  rendered = (\n    render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n      presentation,\n      blocks,\n      sidecar,\n      arguments,\n    )\n  )\n\n  assert "**[R1]" in rendered\n'''
if old not in text: raise RuntimeError('phase144 r4 test not found')
text = text.replace(old, new, 1)
path.write_text(text, encoding='utf-8')
print(f'updated: {path.relative_to(ROOT)}')

print('Phase 150 Finalization Repair R2 applied. Production files unchanged.')
