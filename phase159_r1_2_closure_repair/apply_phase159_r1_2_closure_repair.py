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


def _replace_function(source: str, name: str, replacement: str) -> str:
    ranges = _function_ranges(source)
    if name not in ranges:
        raise RuntimeError(f"function not found: {name}")
    start, end = ranges[name]
    return source[:start] + replacement.rstrip() + "\n\n" + source[end:]


def _insert_before_function(source: str, name: str, addition: str) -> str:
    ranges = _function_ranges(source)
    if name not in ranges:
        raise RuntimeError(f"function not found: {name}")
    start, _ = ranges[name]
    return source[:start] + addition.rstrip() + "\n\n\n" + source[start:]


HELPER = 'def _phase159_restore_isomorphism_to_injective_dependency_visibility(\n  presentation: TodaGroupProofPresentation,\n  proof_body: list[str],\n) -> list[str]:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    proof_body,\n    list,\n  ):\n    raise TypeError(\n      "proof_body must be a list"\n    )\n\n  rendered = "\\n".join(\n    proof_body\n  )\n\n  for node in presentation.nodes:\n    injective_step = node.proof_step\n\n    if not isinstance(\n      injective_step.conclusion,\n      TodaSuspensionInjectiveStatement,\n    ):\n      continue\n\n    injective_map = (\n      injective_step.conclusion.map\n    )\n    isomorphism_step = next(\n      (\n        premise_step\n        for premise_step in injective_step.premises\n        if (\n          isinstance(\n            premise_step.conclusion,\n            TodaSuspensionIsomorphismStatement,\n          )\n          and premise_step.conclusion.map\n          == injective_map\n        )\n      ),\n      None,\n    )\n\n    if isomorphism_step is None:\n      continue\n\n    injective_prose = (\n      _render_generic_narrative_step(\n        injective_step\n      )\n    )\n    isomorphism_prose = (\n      _render_generic_narrative_step(\n        isomorphism_step\n      )\n    )\n\n    if (\n      not injective_prose\n      or not isomorphism_prose\n      or injective_prose not in rendered\n      or isomorphism_prose in rendered\n    ):\n      continue\n\n    replacement = (\n      isomorphism_prose\n      + "\\n\\n"\n      + "したがって, "\n      + injective_prose\n    )\n    rendered = rendered.replace(\n      injective_prose,\n      replacement,\n      1,\n    )\n\n  return rendered.splitlines()\n'
NORMALIZE = 'def _phase158_normalize_public_narrative_contract(\n  presentation: TodaGroupProofPresentation,\n  rendered: str,\n) -> str:\n  if not isinstance(\n    presentation,\n    TodaGroupProofPresentation,\n  ):\n    raise TypeError(\n      "presentation must be a "\n      "TodaGroupProofPresentation"\n    )\n\n  if not isinstance(\n    rendered,\n    str,\n  ):\n    raise TypeError(\n      "rendered must be a str"\n    )\n\n  if presentation.max_depth < 2:\n    return rendered\n\n  title = "# Group proof narrative"\n  target_header = "## 証明対象"\n  reference_header = "## 使用する結果"\n  separator = "---"\n  proof_header = "## 証明"\n  qed = "□"\n\n  source_lines = (\n    rendered.rstrip().splitlines()\n  )\n\n  if (\n    source_lines\n    and source_lines[0] == title\n  ):\n    content_lines = source_lines[1:]\n  else:\n    content_lines = source_lines[:]\n\n  while (\n    content_lines\n    and not content_lines[0].strip()\n  ):\n    content_lines.pop(0)\n\n  def exact_index(\n    marker: str,\n  ) -> int | None:\n    try:\n      return content_lines.index(\n        marker\n      )\n    except ValueError:\n      return None\n\n  target_index = exact_index(\n    target_header\n  )\n  reference_index = exact_index(\n    reference_header\n  )\n  proof_index = exact_index(\n    proof_header\n  )\n\n  if target_index is not None:\n    target_end_candidates = [\n      index\n      for index in (\n        reference_index,\n        proof_index,\n        len(\n          content_lines\n        ),\n      )\n      if (\n        index is not None\n        and index > target_index\n      )\n    ]\n    target_end = min(\n      target_end_candidates\n    )\n    target_body = content_lines[\n      target_index + 1:\n      target_end\n    ]\n  else:\n    target_body = (\n      _phase158_public_narrative_target_lines(\n        presentation\n      )\n    )\n\n  while (\n    target_body\n    and not target_body[0].strip()\n  ):\n    target_body.pop(0)\n\n  while (\n    target_body\n    and not target_body[-1].strip()\n  ):\n    target_body.pop()\n\n  reference_body: list[str] = []\n\n  if (\n    reference_index is not None\n    and proof_index is not None\n    and reference_index < proof_index\n  ):\n    reference_body = content_lines[\n      reference_index + 1:\n      proof_index\n    ]\n\n  while (\n    reference_body\n    and not reference_body[0].strip()\n  ):\n    reference_body.pop(0)\n\n  while (\n    reference_body\n    and not reference_body[-1].strip()\n  ):\n    reference_body.pop()\n\n  if (\n    reference_body\n    and reference_body[-1].strip()\n    == separator\n  ):\n    reference_body.pop()\n\n    while (\n      reference_body\n      and not reference_body[-1].strip()\n    ):\n      reference_body.pop()\n\n  if proof_index is not None:\n    proof_body = content_lines[\n      proof_index + 1:\n    ]\n  elif (\n    target_index is None\n    and reference_index is None\n  ):\n    proof_body = content_lines[:]\n  else:\n    proof_body = []\n\n  while (\n    proof_body\n    and not proof_body[0].strip()\n  ):\n    proof_body.pop(0)\n\n  proof_body = (\n    _phase158_strip_terminal_qed_lines(\n      proof_body\n    )\n  )\n  proof_body = (\n    _phase158_normalize_public_equation_numbers(\n      proof_body\n    )\n  )\n  proof_body = (\n    _phase159_restore_isomorphism_to_injective_dependency_visibility(\n      presentation,\n      proof_body,\n    )\n  )\n\n  lines = [\n    title,\n    "",\n    target_header,\n    "",\n    *target_body,\n    "",\n  ]\n\n  if reference_body:\n    lines.extend(\n      (\n        reference_header,\n        "",\n        *reference_body,\n        "",\n        separator,\n        "",\n      )\n    )\n\n  lines.extend(\n    (\n      proof_header,\n      "",\n      *proof_body,\n      "",\n      qed,\n    )\n  )\n\n  return (\n    "\\n".join(\n      lines\n    ).rstrip()\n    + "\\n"\n  )\n'
TEST_CONTENT = 'from toda_calculation_facade import (\n  build_standard_toda_report,\n)\nfrom toda_group_proof_narrative_renderer import (\n  render_toda_group_proof_narrative_markdown,\n)\nfrom toda_group_proof_presentation import (\n  build_toda_group_proof_presentation,\n)\nfrom toda_group_result_proof_replay import (\n  build_toda_group_result_proof_replay,\n)\n\n\ndef _render_phase159_r1_2_pi3_2() -> str:\n  report = build_standard_toda_report(\n    n=2,\n    k=1,\n  )\n  group_result = (\n    report\n    .candidates[0]\n    .source_candidate\n    .group_result\n  )\n  replay = build_toda_group_result_proof_replay(\n    group_result,\n    max_depth=2,\n  )\n  presentation = build_toda_group_proof_presentation(\n    replay\n  )\n\n  return render_toda_group_proof_narrative_markdown(\n    presentation\n  )\n\n\ndef test_phase159_r1_2_pi3_2_omits_empty_reference_section():\n  rendered = (\n    _render_phase159_r1_2_pi3_2()\n  )\n\n  assert "## 使用する結果" not in rendered\n  assert "## 証明" in rendered\n\n\ndef test_phase159_r1_2_pi3_2_shows_isomorphism_before_injectivity():\n  rendered = (\n    _render_phase159_r1_2_pi3_2()\n  )\n\n  isomorphism = (\n    "$E: \\\\\\\\pi_{1}^{1} \\\\\\\\to "\n    "\\\\\\\\pi_{2}^{2}$ は同型写像である."\n  )\n  injectivity = (\n    "$E: \\\\\\\\pi_{1}^{1} \\\\\\\\to "\n    "\\\\\\\\pi_{2}^{2}$ は単射である."\n  )\n\n  assert isomorphism in rendered\n  assert injectivity in rendered\n  assert (\n    rendered.index(\n      isomorphism\n    )\n    < rendered.index(\n      injectivity\n    )\n  )\n  assert (\n    "したがって, "\n    + injectivity\n  ) in rendered\n'


def main() -> int:
    if not RENDERER.is_file():
        raise RuntimeError(f"missing production file: {RENDERER}")

    renderer = RENDERER.read_text(encoding="utf-8")
    compile(renderer, str(RENDERER), "exec")

    if "_phase159_restore_isomorphism_to_injective_dependency_visibility" not in renderer:
        renderer = _insert_before_function(
            renderer,
            "_phase158_normalize_public_narrative_contract",
            HELPER,
        )

    renderer = _replace_function(
        renderer,
        "_phase158_normalize_public_narrative_contract",
        NORMALIZE,
    )

    compile(renderer, str(RENDERER), "exec")
    compile(TEST_CONTENT, str(TEST), "exec")

    backup = ROOT / (
        "phase159_r1_2_closure_repair_backup_"
        + datetime.now().strftime("%Y%m%d_%H%M%S")
    )
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(RENDERER, backup / RENDERER.name)

    if TEST.exists():
        shutil.copy2(TEST, backup / TEST.name)

    RENDERER.write_text(renderer, encoding="utf-8", newline="\n")
    TEST.parent.mkdir(parents=True, exist_ok=True)
    TEST.write_text(TEST_CONTENT, encoding="utf-8", newline="\n")

    print("Phase 159-R1-2 closure repair applied.")
    print("Production: toda_group_proof_narrative_renderer.py")
    print("Test: tests/test_phase159_r1_2_pi3_2_closure.py")
    print("Backup:", backup)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
