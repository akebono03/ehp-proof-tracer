from __future__ import annotations

import ast
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path.cwd()
RENDERER = ROOT / "toda_group_proof_narrative_renderer.py"
TEST = ROOT / "tests" / "test_phase159_r1_2_pi3_2_closure.py"


def _function_ranges(source: str) -> dict[str, tuple[int, int]]:
    tree = ast.parse(source)
    lines = source.splitlines(keepends=True)
    offsets = [0]
    total = 0

    for line in lines:
        total += len(line)
        offsets.append(total)

    result = {}

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = offsets[node.lineno - 1]
            end = offsets[node.end_lineno]
            while end < len(source) and source[end:end + 1] == "\n":
                end += 1
            result[node.name] = (start, end)

    return result


def _replace_function(
    source: str,
    name: str,
    replacement: str,
) -> str:
    ranges = _function_ranges(source)

    if name not in ranges:
        raise RuntimeError(
            f"function not found: {name}"
        )

    start, end = ranges[name]

    return (
        source[:start]
        + replacement.rstrip()
        + "\n\n"
        + source[end:]
    )


HELPER = 'def _phase159_restore_isomorphism_to_injective_dependency_visibility(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[str],\n) -> list[str]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  dependency_pairs = []\n  visited_step_ids = set()\n\n  def visit(\n    proof_step: ProofStep,\n  ) -> None:\n    step_id = id(\n      proof_step\n    )\n\n    if step_id in visited_step_ids:\n      return\n\n    visited_step_ids.add(\n      step_id\n    )\n\n    if isinstance(\n      proof_step.conclusion,\n      TodaSuspensionInjectiveStatement,\n    ):\n      injective_map = (\n        proof_step.conclusion.map\n      )\n      isomorphism_step = next(\n        (\n          premise_step\n          for premise_step in proof_step.premises\n          if (\n            isinstance(\n              premise_step.conclusion,\n              TodaSuspensionIsomorphismStatement,\n            )\n            and premise_step.conclusion.map\n            == injective_map\n          )\n        ),\n        None,\n      )\n\n      if isomorphism_step is not None:\n        dependency_pairs.append(\n          (\n            isomorphism_step,\n            proof_step,\n          )\n        )\n\n    for premise_step in proof_step.premises:\n      visit(\n        premise_step\n      )\n\n  visit(\n    presentation.root_step\n  )\n\n  rendered = "\\n".join(\n    proof_body\n  )\n\n  for (\n    isomorphism_step,\n    injective_step,\n  ) in dependency_pairs:\n    isomorphism_prose = (\n      _render_generic_narrative_step(\n        isomorphism_step\n      )\n    )\n    injective_prose = (\n      _render_generic_narrative_step(\n        injective_step\n      )\n    )\n\n    if (\n      not isomorphism_prose\n      or not injective_prose\n    ):\n      continue\n\n    has_isomorphism = (\n      isomorphism_prose in rendered\n    )\n    has_injectivity = (\n      injective_prose in rendered\n    )\n\n    if (\n      has_isomorphism\n      and has_injectivity\n    ):\n      continue\n\n    if has_injectivity:\n      rendered = rendered.replace(\n        injective_prose,\n        (\n          isomorphism_prose\n          + "\\n\\n"\n          + "したがって, "\n          + injective_prose\n        ),\n        1,\n      )\n      continue\n\n    if has_isomorphism:\n      rendered = rendered.replace(\n        isomorphism_prose,\n        (\n          isomorphism_prose\n          + "\\n\\n"\n          + "したがって, "\n          + injective_prose\n        ),\n        1,\n      )\n      continue\n\n    dependency_prose = (\n      isomorphism_prose\n      + "\\n\\n"\n      + "したがって, "\n      + injective_prose\n    )\n\n    if rendered:\n      rendered = (\n        dependency_prose\n        + "\\n\\n"\n        + rendered\n      )\n    else:\n      rendered = dependency_prose\n\n  return rendered.splitlines()\n'
TEST_CONTENT = 'from homotopy_groups import (\n  TodaSuspensionIsomorphismStatement,\n)\nfrom toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\nfrom toda_rules import (\n  TodaSuspensionInjectiveStatement,\n)\n\n\ndef _build_phase159_r1_2_pi3_2_presentation():\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n\n  return build_toda_group_proof_presentation(\n    replay\n  )\n\n\ndef _render_phase159_r1_2_pi3_2() -> str:\n  presentation = (\n    _build_phase159_r1_2_pi3_2_presentation()\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef _recursive_ancestry(\n  proof_step,\n):\n  ordered = []\n  visited = set()\n\n  def visit(\n    step,\n  ):\n    step_id = id(\n      step\n    )\n\n    if step_id in visited:\n      return\n\n    visited.add(\n      step_id\n    )\n    ordered.append(\n      step\n    )\n\n    for premise in step.premises:\n      visit(\n        premise\n      )\n\n  visit(\n    proof_step\n  )\n\n  return tuple(\n    ordered\n  )\n\n\ndef test_phase159_r1_2_pi3_2_omits_empty_reference_section():\n  rendered = (\n    _render_phase159_r1_2_pi3_2()\n  )\n\n  assert "## 使用する結果" not in rendered\n  assert "## 証明" in rendered\n\n\ndef test_phase159_r1_2_pi3_2_dependency_exists_in_recursive_ancestry():\n  presentation = (\n    _build_phase159_r1_2_pi3_2_presentation()\n  )\n  ancestry = (\n    _recursive_ancestry(\n      presentation.root_step\n    )\n  )\n\n  injective_step = next(\n    step\n    for step in ancestry\n    if isinstance(\n      step.conclusion,\n      TodaSuspensionInjectiveStatement,\n    )\n  )\n\n  assert any(\n    (\n      isinstance(\n        premise.conclusion,\n        TodaSuspensionIsomorphismStatement,\n      )\n      and premise.conclusion.map\n      == injective_step.conclusion.map\n    )\n    for premise in injective_step.premises\n  )\n\n\ndef test_phase159_r1_2_pi3_2_shows_isomorphism_before_injectivity():\n  rendered = (\n    _render_phase159_r1_2_pi3_2()\n  )\n\n  isomorphism = (\n    "$E: \\\\\\\\pi_{1}^{1} \\\\\\\\to "\n    "\\\\\\\\pi_{2}^{2}$ は同型写像である."\n  )\n  injectivity = (\n    "$E: \\\\\\\\pi_{1}^{1} \\\\\\\\to "\n    "\\\\\\\\pi_{2}^{2}$ は単射である."\n  )\n\n  assert isomorphism in rendered\n  assert injectivity in rendered\n  assert (\n    rendered.index(\n      isomorphism\n    )\n    < rendered.index(\n      injectivity\n    )\n  )\n  assert (\n    "したがって, "\n    + injectivity\n  ) in rendered\n'


def main() -> int:
    if not RENDERER.is_file():
        raise RuntimeError(
            f"missing production file: {RENDERER}"
        )

    renderer = RENDERER.read_text(
        encoding="utf-8"
    )
    compile(
        renderer,
        str(RENDERER),
        "exec",
    )

    renderer = _replace_function(
        renderer,
        "_phase159_restore_isomorphism_to_injective_dependency_visibility",
        HELPER,
    )

    compile(
        renderer,
        str(RENDERER),
        "exec",
    )
    compile(
        TEST_CONTENT,
        str(TEST),
        "exec",
    )

    backup = ROOT / (
        "phase159_r1_2_closure_repair2_backup_"
        + datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )
    backup.mkdir(
        parents=True,
        exist_ok=False,
    )

    shutil.copy2(
        RENDERER,
        backup / RENDERER.name,
    )

    if TEST.is_file():
        shutil.copy2(
            TEST,
            backup / TEST.name,
        )

    RENDERER.write_text(
        renderer,
        encoding="utf-8",
        newline="\n",
    )
    TEST.write_text(
        TEST_CONTENT,
        encoding="utf-8",
        newline="\n",
    )

    print(
        "Phase 159-R1-2 closure repair2 applied."
    )
    print(
        "Production code:"
    )
    print(
        "  toda_group_proof_narrative_renderer.py"
    )
    print(
        "  recursive ancestry dependency visibility repair"
    )
    print(
        "Test:"
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
