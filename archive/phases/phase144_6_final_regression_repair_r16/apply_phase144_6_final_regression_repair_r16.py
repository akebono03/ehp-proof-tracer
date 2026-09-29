from pathlib import Path

ROOT = Path.cwd()
multi_path = ROOT / 'toda_group_proof_narrative_argument_multi_renderer.py'
multi = multi_path.read_text(encoding='utf-8-sig')

# Revert only the ineffective R15 CALCULATION ownership exception.
r15_calc = """        if (
          block.role
          is TodaGroupProofNarrativeMathematicalBlockRole
          .CALCULATION
        ):
          continue

"""
if r15_calc in multi:
    multi = multi.replace(r15_calc, '', 1)

# Extend the existing direct-premise relocation input with each premise's
# immediate prerequisites. This is generic and contains no group-specific branch.
anchor = """    direct_derivation_premises = (
      ()
      if conclusion_step is None
      else (
        extract_toda_group_proof_narrative_argument_conclusion_direct_derivation_premises(
          argument,
          arguments,
        )
      )
    )
"""
replacement = anchor + """    direct_derivation_prerequisites = tuple(
      prerequisite_step
      for premise_step in direct_derivation_premises
      for prerequisite_step in premise_step.premises
      if all(
        prerequisite_step is not existing_step
        for existing_step in direct_derivation_premises
      )
    )
    direct_derivation_premises = (
      direct_derivation_prerequisites
      + direct_derivation_premises
    )
"""
if 'direct_derivation_prerequisites = tuple(' not in multi:
    if anchor not in multi:
        raise RuntimeError('direct_derivation_premises anchor not found')
    multi = multi.replace(anchor, replacement, 1)
multi_path.write_text(multi, encoding='utf-8')

# Phase144-5 intentionally numbers calculation-chain equations.
# Update only stale Phase143 exact-string expectations.
p57 = ROOT / 'tests/test_phase143_57c_step_derivation_connector.py'
t = p57.read_text(encoding='utf-8-sig')
pairs57 = [
    ("r\"$2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5}$\"", "r\"$2\\nu' = \\eta_{3}E\\eta_{3}\\eta_{5}\\tag{1}$\""),
    ("r\"$\\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}^{3}$\"", "r\"$\\eta_{3}E\\eta_{3}\\eta_{5} = \\eta_{3}^{3}\\tag{2}$\""),
    ("r\"$2\\nu' = \\eta_{3}^{3}$\"", "r\"$2\\nu' = \\eta_{3}^{3}\\tag{3}$\""),
    ("r\"$H\\left(\\nu'\\right) = E^{2}\\eta_{3}$\"", "r\"$H\\left(\\nu'\\right) = E^{2}\\eta_{3}\\tag{4}$\""),
    ("r\"$E^{2}\\eta_{3} = \\eta_{5}$\"", "r\"$E^{2}\\eta_{3} = \\eta_{5}\\tag{5}$\""),
    ("r\"$H\\left(\\nu'\\right) = \\eta_{5}$\"", "r\"$H\\left(\\nu'\\right) = \\eta_{5}\\tag{6}$\""),
]
for old, new in pairs57:
    t = t.replace(old, new)
t = t.replace('connector = "これらより、"', 'connector = "(1) と (2) より、"', 1)
t = t.replace('connector = "これらより、"', 'connector = "(4) と (5) より、"', 1)
old_count = '  assert rendered.count(\n    "これらより、"\n  ) == 2'
new_count = '  assert "(1) と (2) より、" in rendered\n  assert "(4) と (5) より、" in rendered'
t = t.replace(old_count, new_count)
p57.write_text(t, encoding='utf-8')

p61 = ROOT / 'tests/test_phase143_61b_direct_premise_narrative.py'
t = p61.read_text(encoding='utf-8-sig')
for old, new in pairs57[:3]:
    t = t.replace(old, new)
t = t.replace('      "これらより、",', '      "(1) と (2) より、",', 1)
p61.write_text(t, encoding='utf-8')

print('Phase 144-6 R16 applied.')
print('Production: toda_group_proof_narrative_argument_multi_renderer.py')
print('Tests: Phase143-57c and Phase143-61b stale numbering expectations updated.')
