from pathlib import Path

ROOT = Path.cwd()

multi = ROOT / "toda_group_proof_narrative_argument_multi_renderer.py"
text = multi.read_text(encoding="utf-8-sig")

old = '    for block in local_body_blocks:\n      if (\n        block.role\n        is not TodaGroupProofNarrativeMathematicalBlockRole\n        .EXACTNESS\n      ):\n        seen_non_exact_block_ids.add(\n          id(\n            block\n          )\n        )\n        continue\n'
new = '    for block in local_body_blocks:\n      if (\n        block.role\n        is not TodaGroupProofNarrativeMathematicalBlockRole\n        .EXACTNESS\n      ):\n        if not any(\n          id(\n            proof_step\n          ) in context_hidden_step_ids\n          for proof_step in block.steps\n        ):\n          seen_non_exact_block_ids.add(\n            id(\n              block\n            )\n          )\n        continue\n'
if old not in text:
    raise RuntimeError("multi-renderer seen-block anchor not found")
multi.write_text(text.replace(old, new, 1), encoding="utf-8")
print("Updated:", multi)

route = ROOT / "tests" / "test_phase144_6_pi6_generic_production_route.py"
t = route.read_text(encoding="utf-8-sig")
old_import = 'from toda_group_proof_narrative_argument_multi_renderer import (\n  render_toda_group_proof_narrative_multi_argument_markdown,\n)\n'
new_import = 'from toda_group_proof_narrative_contribution_renderer import (\n  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,\n)\n'
if old_import not in t:
    raise RuntimeError("route test import anchor not found")
t = t.replace(old_import, new_import, 1)
t = t.replace("render_toda_group_proof_narrative_multi_argument_markdown(\n", "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown(\n", 1)
t = t.replace('  assert "**[R1]" not in captured.out\n', '  assert "**[R1]" in captured.out\n', 1)
t = t.replace('    "render_toda_group_proof_narrative_multi_argument_markdown"\n    in pi6_branch\n', '    "render_toda_group_proof_narrative_multi_argument_with_contributions_markdown"\n    in pi6_branch\n', 1)
route.write_text(t, encoding="utf-8")
print("Updated:", route)

eqtest = ROOT / "tests" / "test_phase144_5_generic_definition_order_equations.py"
e = eqtest.read_text(encoding="utf-8-sig")
old_test = 'def test_phase144_5_r2_numbers_only_calculation_chain_equations():\n  markdown = (\n    "$u=v$\\n\\n"\n    "$a=b$\\n\\n"\n    "$b=c$\\n\\n"\n    "これらより、\\n\\n"\n    "$a=c$\\n\\n"\n    "$x=y$"\n  )\n\n  rendered = (\n    number_toda_group_proof_narrative_equations(\n      markdown\n    )\n  )\n\n  assert "$u=v$" in rendered\n  assert r"$a=b\\tag{1}$" in rendered\n  assert r"$b=c\\tag{2}$" in rendered\n  assert "(1) と (2) より、" in rendered\n  assert r"$a=c\\tag{3}$" in rendered\n  assert "$x=y$" in rendered\n  assert r"$u=v\\tag{" not in rendered\n  assert r"$x=y\\tag{" not in rendered\n'
new_test = 'def test_phase144_5_r2_numbers_only_calculation_chain_equations():\n  rendered = _render_multi_argument(\n    3,\n    3,\n  )\n\n  assert r"$2\\nu\' = \\eta_{3}E\\eta_{3}\\eta_{5}\\tag{1}$" in rendered\n  assert (\n    r"$\\eta_{3}E\\eta_{3}\\eta_{5} = "\n    r"\\eta_{3}^{3}\\tag{2}$"\n    in rendered\n  )\n  assert "(1) と (2) より、" in rendered\n  assert r"$2\\nu\' = \\eta_{3}^{3}\\tag{3}$" in rendered\n  assert (\n    r"$\\pi_{4}^{3} = \\mathbb{Z}/2\\{\\eta_{3}\\}\\tag{"\n    not in rendered\n  )\n  assert (\n    r"$\\pi_{6}^{3} = \\mathbb{Z}/4\\{\\nu\'\\}\\tag{"\n    not in rendered\n  )\n'
if old_test not in e:
    raise RuntimeError("Phase 144-5 stale API test anchor not found")
eqtest.write_text(e.replace(old_test, new_test, 1), encoding="utf-8")
print("Updated:", eqtest)