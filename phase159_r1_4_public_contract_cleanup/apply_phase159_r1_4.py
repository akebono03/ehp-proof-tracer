from pathlib import Path
from datetime import datetime
import shutil

ROOT = Path(__file__).resolve().parents[1]
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_narrative_repair.py"

def replace_once(source, old, new, label):
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected exactly one match, found {count}")
    return source.replace(old, new, 1)

def replace_test_function(source, function_name, replacement):
    marker = "def " + function_name + "("
    start = source.find(marker)
    if start < 0:
        raise RuntimeError("test function not found: " + function_name)
    next_function = source.find("\ndef ", start + len(marker))
    end = len(source) if next_function < 0 else next_function + 1
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]

OLD_EXACTNESS = '  if primary_component is not None:\n    exactness_step_lines = {\n      _render_generic_narrative_step(proof_step)\n      for block in primary_component.evidence_blocks\n      for proof_step in block.steps\n    }\n    long_exact_sequence = (\n      "$"\n      + render_toda_group_proof_narrative_exactness_method_component_latex(\n        primary_component\n      )\n      + "$ は完全である."\n    )\n    projected_lines = []\n    inserted = False\n\n    for line in lines:\n      if any(\n        exactness_line in line\n        for exactness_line in exactness_step_lines\n      ):\n        if not inserted:\n          projected_lines.append(long_exact_sequence)\n          inserted = True\n        continue\n      projected_lines.append(line)\n\n    lines = projected_lines\n'
NEW_EXACTNESS = '  if primary_component is not None:\n    component_latex = (\n      render_toda_group_proof_narrative_exactness_method_component_latex(\n        primary_component\n      )\n    )\n    long_exact_sequence = (\n      "$"\n      + component_latex\n      + "$ は完全である."\n    )\n    projected_lines = []\n    inserted = False\n\n    for line in lines:\n      stripped = line.strip()\n      exactness_latex = None\n\n      if (\n        stripped.startswith("$")\n        and r"\\\\xrightarrow{" in stripped\n      ):\n        closing_math = stripped.rfind(\n          "$"\n        )\n\n        if closing_math > 0:\n          exactness_latex = stripped[\n            1:closing_math\n          ]\n\n      if (\n        exactness_latex is not None\n        and exactness_latex in component_latex\n      ):\n        if not inserted:\n          projected_lines.append(\n            long_exact_sequence\n          )\n          inserted = True\n        continue\n\n      projected_lines.append(\n        line\n      )\n\n    lines = projected_lines\n'
OLD_ISO = '    isomorphism_line = _phase159_plain_map_property_line(\n      isomorphism_step,\n      "同型写像",\n    )\n'
NEW_ISO = '    isomorphism_line = _phase159_plain_map_property_line(\n      isomorphism_step,\n      "同型",\n    )\n'
OLD_CONNECTOR = '    lines[isomorphism_index] = (\n      prefix\n      + "("\n      + str(injective_number)\n      + ") と ("\n      + str(surjective_number)\n      + ") より, "\n      + isomorphism_line\n    )\n'
NEW_CONNECTOR = '    lines[isomorphism_index] = (\n      prefix\n      + "("\n      + str(injective_number)\n      + "), ("\n      + str(surjective_number)\n      + ") より, "\n      + isomorphism_line\n    )\n'
OLD_COMPACT = '  compacted = []\n  previous_blank = False\n\n  for line in lines:\n'
NEW_COMPACT = '  punctuated_lines = []\n\n  for line in lines:\n    stripped = line.rstrip()\n\n    if (\n      stripped\n      and stripped.endswith("$")\n    ):\n      line = stripped + "."\n\n    punctuated_lines.append(\n      line\n    )\n\n  lines = punctuated_lines\n\n  compacted = []\n  previous_blank = False\n\n  for line in lines:\n'

EXACTNESS_TEST = """def test_phase159_r1_4_pi3_2_public_uses_exactly_one_exact_sequence():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  long_exact = (
    r"$\\pi_{2}^{1} \\xrightarrow{E} "
    r"\\pi_{3}^{2} \\xrightarrow{H} "
    r"\\pi_{3}^{3} \\xrightarrow{\\Delta} "
    r"\\pi_{1}^{1} \\xrightarrow{E} "
    r"\\pi_{2}^{2}$ は完全である."
  )

  proof_body = rendered.split(
    "## 証明\\n\\n",
    1,
  )[1]

  exactness_lines = tuple(
    line
    for line in proof_body.splitlines()
    if r"\\xrightarrow{" in line
  )

  assert exactness_lines == (
    long_exact,
  )
"""

MAP_TEST = """def test_phase159_r1_4_pi3_2_public_numbers_map_properties_semantically():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  injective = (
    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"
    r"\\tag{1}$ は単射."
  )
  surjective = (
    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}"
    r"\\tag{2}$ は全射."
  )
  isomorphism = (
    r"$H: \\pi_{3}^{2} \\to \\pi_{3}^{3}$ "
    "は同型."
  )

  assert injective in rendered
  assert surjective in rendered
  assert "(1), (2) より, " + isomorphism in rendered
  assert rendered.index(injective) < rendered.index(surjective)
  assert rendered.index(surjective) < rendered.index(isomorphism)
"""

PERIOD_TEST = """def test_phase159_r1_4_pi3_2_public_math_sentences_end_with_period():
  presentation = _phase159_r1_2_pi3_2_presentation()
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  assert r"$\\pi_{2}^{1} = 0$." in rendered
  assert r"$\\pi_{3}^{3} = \\mathbb{Z}\\{\\iota_{3}\\}$." in rendered
  assert (
    r"以上より, $\\pi_{3}^{2} = "
    r"\\mathbb{Z}\\{\\eta_{2}\\}$."
    in rendered
  )
"""

def main():
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = ROOT / ("phase159_r1_4_backup_" + stamp)
    backup_dir.mkdir(parents=True, exist_ok=False)
    shutil.copy2(RENDERER, backup_dir / RENDERER.name)
    shutil.copy2(TEST, backup_dir / TEST.name)

    renderer = RENDERER.read_text(encoding="utf-8-sig")
    renderer = replace_once(renderer, OLD_EXACTNESS, NEW_EXACTNESS, "exactness")
    renderer = replace_once(renderer, OLD_ISO, NEW_ISO, "isomorphism")
    renderer = replace_once(renderer, OLD_CONNECTOR, NEW_CONNECTOR, "connector")
    renderer = replace_once(renderer, OLD_COMPACT, NEW_COMPACT, "punctuation")
    RENDERER.write_text(renderer, encoding="utf-8", newline="\n")

    tests = TEST.read_text(encoding="utf-8-sig")
    tests = replace_test_function(
        tests,
        "test_phase159_r1_3_pi3_2_public_uses_one_semantic_exactness_component",
        EXACTNESS_TEST,
    )
    tests = replace_test_function(
        tests,
        "test_phase159_r1_3_pi3_2_public_numbers_map_properties_semantically",
        MAP_TEST,
    )
    if "def test_phase159_r1_4_pi3_2_public_math_sentences_end_with_period(" not in tests:
        tests = tests.rstrip() + "\n\n\n" + PERIOD_TEST.rstrip() + "\n"
    TEST.write_text(tests, encoding="utf-8", newline="\n")

    print("Phase 159-R1-4 applied.")
    print("Backup:", backup_dir)

if __name__ == "__main__":
    main()
