from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_proof_narrative_renderer.py'
TEST = ROOT / 'tests' / 'test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py'

text = TARGET.read_text(encoding='utf-8')

old_import = '''from toda_rules import (\n  TodaDeltaImageUpToSignStatement,\n'''
new_import = '''from toda_rules import (\n  Toda56Nu4Prop44SpecializationStatement,\n  TodaDeltaImageUpToSignStatement,\n'''
if '  Toda56Nu4Prop44SpecializationStatement,\n' not in text:
    if old_import not in text:
        raise SystemExit('Could not locate toda_rules import insertion point.')
    text = text.replace(old_import, new_import, 1)

needle = '''def render_toda_proof_statement_latex(\n  statement,\n) -> str | None:\n  if isinstance(\n    statement,\n    Relation,\n  ):\n'''
replacement = '''def render_toda_proof_statement_latex(\n  statement,\n) -> str | None:\n  if isinstance(\n    statement,\n    Toda56Nu4Prop44SpecializationStatement,\n  ):\n    return (\n      "n = "\n      + _render_scalar_latex(\n        statement.n\n      )\n      + r", \\quad \\alpha = "\n      + render_toda_expression_latex(\n        statement.alpha\n      )\n      + r", \\quad "\n      + render_toda_expression_latex(\n        statement.membership.element\n      )\n      + r" \\in "\n      + render_toda_primary_group_latex(\n        statement.membership.group\n      )\n      + r", \\quad "\n      + _render_relation_latex(\n        statement.hopf_relation\n      )\n    )\n\n  if isinstance(\n    statement,\n    Relation,\n  ):\n'''
if 'Toda56Nu4Prop44SpecializationStatement,\n  ):' not in text[text.find('def render_toda_proof_statement_latex'):]:
    if needle not in text:
        raise SystemExit('Could not locate render_toda_proof_statement_latex insertion point.')
    text = text.replace(needle, replacement, 1)

TARGET.write_text(text, encoding='utf-8')

TEST.write_text('''from test_phase63_nu4_prop44_specialization import (\n  build_phase63_2_data,\n)\nfrom toda_group_proof_narrative_renderer import (\n  _render_group_proof_narrative_latex,\n)\nfrom toda_proof_narrative_renderer import (\n  render_toda_proof_statement_latex,\n)\n\n\ndef test_phase143_75aa_renders_specialization_semantics():\n  data = build_phase63_2_data()\n\n  statement = (\n    data[\n      "specialization_step"\n    ].conclusion\n  )\n\n  assert (\n    render_toda_proof_statement_latex(\n      statement\n    )\n    == (\n      r"n = 4, \\quad \\alpha = \\nu_{4}, "\n      r"\\quad \\nu_{4} \\in \\pi_{7}^{4}, "\n      r"\\quad H\\left(\\nu_{4}\\right) = \\iota_{7}"\n    )\n  )\n\n\ndef test_phase143_75aa_group_narrative_uses_semantics_not_rule_name():\n  data = build_phase63_2_data()\n\n  specialization_step = data[\n    "specialization_step"\n  ]\n\n  rendered = (\n    _render_group_proof_narrative_latex(\n      specialization_step\n    )\n  )\n\n  assert rendered is not None\n  assert r"n = 4" in rendered\n  assert r"\\alpha = \\nu_{4}" in rendered\n  assert r"\\nu_{4} \\in \\pi_{7}^{4}" in rendered\n  assert r"H\\left(\\nu_{4}\\right) = \\iota_{7}" in rendered\n  assert (\n    "Toda (5.6) nu_4 Proposition 4.4 specialization premises"\n    not in rendered\n  )\n\n\ndef test_phase143_75aa_does_not_expand_lemma54_statement():\n  data = build_phase63_2_data()\n\n  rendered = (\n    render_toda_proof_statement_latex(\n      data[\n        "specialization_step"\n      ].conclusion\n    )\n  )\n\n  assert rendered is not None\n  assert r"E^{2}" not in rendered\n  assert "literature" not in rendered\n''', encoding='utf-8')

print('Phase 143-75AA patch applied.')
print('Changed: toda_proof_narrative_renderer.py')
print('Added: tests/test_phase143_75aa_toda56_nu4_prop44_specialization_rendering.py')
