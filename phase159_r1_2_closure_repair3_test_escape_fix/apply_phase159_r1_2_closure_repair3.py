from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_closure.py"

TEST_CONTENT = r'from homotopy_groups import (\n  TodaSuspensionIsomorphismStatement,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  TodaSuspensionInjectiveStatement,\n)\n\n\ndef _build_phase159_r1_2_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef _render_phase159_r1_2_pi3_2() -> str:\n  presentation = (\n    _build_phase159_r1_2_pi3_2_presentation()\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef _recursive_ancestry(\n  proof_step,\n):\n  ordered = []\n  visited = set()\n\n  def visit(\n    step,\n  ):\n    step_id = id(\n      step\n    )\n\n    if step_id in visited:\n      return\n\n    visited.add(\n      step_id\n    )\n    ordered.append(\n      step\n    )\n\n    for premise in step.premises:\n      visit(\n        premise\n      )\n\n  visit(\n    proof_step\n  )\n\n  return tuple(\n    ordered\n  )\n\n\ndef test_phase159_r1_2_pi3_2_omits_empty_reference_section():\n  rendered = (\n    _render_phase159_r1_2_pi3_2()\n  )\n\n  assert "## 使用する結果" not in rendered\n  assert "## 証明" in rendered\n\n\ndef test_phase159_r1_2_pi3_2_dependency_exists_in_recursive_ancestry():\n  presentation = (\n    _build_phase159_r1_2_pi3_2_presentation()\n  )\n  ancestry = (\n    _recursive_ancestry(\n      presentation.root_step\n    )\n  )\n\n  injective_step = next(\n    step\n    for step in ancestry\n    if isinstance(\n      step.conclusion,\n      TodaSuspensionInjectiveStatement,\n    )\n  )\n\n  assert any(\n    (\n      isinstance(\n        premise.conclusion,\n        TodaSuspensionIsomorphismStatement,\n      )\n      and premise.conclusion.map\n      == injective_step.conclusion.map\n    )\n    for premise in injective_step.premises\n  )\n\n\ndef test_phase159_r1_2_pi3_2_shows_isomorphism_before_injectivity():\n  rendered = (\n    _render_phase159_r1_2_pi3_2()\n  )\n\n  isomorphism = (\n    "$E: \\\\pi_{1}^{1} \\\\to "\n    "\\\\pi_{2}^{2}$ は同型写像である."\n  )\n  injectivity = (\n    "$E: \\\\pi_{1}^{1} \\\\to "\n    "\\\\pi_{2}^{2}$ は単射である."\n  )\n\n  assert isomorphism in rendered\n  assert injectivity in rendered\n  assert (\n    rendered.index(\n      isomorphism\n    )\n    < rendered.index(\n      injectivity\n    )\n  )\n  assert (\n    "したがって, "\n    + injectivity\n  ) in rendered\n'


def main() -> int:
    if not TEST.is_file():
        raise RuntimeError(
            f"missing test file: {TEST}"
        )

    compile(
        TEST_CONTENT,
        str(TEST),
        "exec",
    )

    backup = ROOT / (
        "phase159_r1_2_closure_repair3_backup_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )
    backup.mkdir(
        parents=True,
        exist_ok=False,
    )
    shutil.copy2(
        TEST,
        backup / TEST.name,
    )

    TEST.write_text(
        TEST_CONTENT,
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Phase 159-R1-2 closure repair3 applied."
    )
    print(
        "Production code changes: none"
    )
    print(
        "Test-only escape correction:"
    )
    print(
        "  tests/test_phase159_r1_2_pi3_2_closure.py"
    )
    print(
        "Backup:",
        backup,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
