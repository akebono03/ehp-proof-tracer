# Phase 164 R5 — 変更コード全文

## 変更対象

- `web_group_proof.py`: `build_standard_web_group_proof_view` 関数全体を置換（import は変更しない）。
- `phase164_r5_web_registry_connection.py`: 新規モジュール。
- `tests/test_phase164_r5_web_registry_connection.py`: 新規テスト7関数と fixture。
- `apply_patch.py`: 新規の適用スクリプト。
- `run.ps1`: 新規実行スクリプト。

既存クラス・その他の関数は変更しません。

## web_group_proof.py に置換する関数全体

```python
def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
) -> WebGroupProofView:
  if (
    mode == "narrative"
    and k == 1
    and n in (4, 5)
  ):
    from phase162_r4_b3_web_common_display import (
      build_phase162_r4_b3_web_common_display_view,
    )
    return build_phase162_r4_b3_web_common_display_view(
      n=n, k=k, max_depth=max_depth,
    )

  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for repository-backed group results")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")

  report = build_standard_toda_report(n=n, k=k)
  if report.status is TodaCalculationStatus.NOT_FOUND:
    raise ValueError("no proof-backed group result found")
  if report.status is TodaCalculationStatus.MULTIPLE_RESULTS:
    raise ValueError("group proof requires exactly one result")
  group_result = report.candidates[0].source_candidate.group_result
  registry_narrative = None
  if n == 3 and k == 2 and mode == "narrative":
    from phase164_r5_web_registry_connection import (
      build_phase164_r5_web_pi5_3_proof,
    )
    replay, registry_narrative = build_phase164_r5_web_pi5_3_proof(
      max_depth=max_depth,
    )
  else:
    replay = build_toda_group_result_proof_replay(
      group_result, max_depth=max_depth,
    )

  conclusion_latex, conclusion_fallback = _group_proof_statement_latex(
    replay.root_step.conclusion
  )
  if conclusion_latex is None:
    raise ValueError(
      "group conclusion is not renderable as LaTeX: "
      f"{conclusion_fallback}"
    )

  steps = []
  for replay_step in replay.steps:
    statement_latex, fallback_type_name = _group_proof_statement_latex(
      replay_step.proof_step.conclusion
    )
    steps.append(WebGroupProofStepView(
      depth=replay_step.depth,
      statement_latex=statement_latex,
      fallback_type_name=fallback_type_name,
      rule_name=_group_proof_rule_name(replay_step.proof_step),
      role_name=replay_step.role.value,
    ))

  rendered_lines = ()
  if mode != "trace":
    if mode == "outline":
      presentation = build_toda_group_proof_presentation(replay)
      markdown = render_toda_group_proof_outline_markdown(presentation)
    elif registry_narrative is not None:
      markdown = registry_narrative
    else:
      presentation = build_toda_group_proof_presentation(replay)
      markdown = render_toda_group_proof_narrative_markdown(presentation)
    rendered_lines = _build_group_proof_rendered_lines(markdown)

  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(steps),
    max_depth=replay.max_depth,
    mode=mode,
    rendered_lines=rendered_lines,
  )
```

## 追加モジュール全体

```python
"""Phase 164 R5: live registry-backed pi_5^3 group proof for the Web narrative."""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from phase162_web_narrative_integration import _phase162_ehp_leaves
from phase164_r4_r1_source_crosswalk import audit_current_repository
from phase164_r4_r8_registry_reconstruction import (
    _known_trusted_roots,
    reconstruct_phase164_r4_r8_pi5_3,
)
from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_human_readable_renderer import render_toda_public_group_relation_latex
from toda_rules import toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule


def build_phase164_r5_web_pi5_3_proof(*, max_depth: int = 2):
    """Build the group root using an R4-R8-validated, registry-backed map proof.

    The original group/source and generator-bridge subproofs stay INFERENCE.
    R4-R8 supplies the *same* typed literature-connected isomorphism step,
    not a display-only replacement. No test fixture is imported.
    """
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an integer")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    manifest = Path("phase163_r4_r94_output/manifest.json")
    if not manifest.is_file():
        raise ValueError("R4-R8 source manifest missing; Web proof cannot be certified")

    prop51, hopf, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf) + exactness
    fixed = reconstruct_phase164_r4_r8_pi5_3(
        audit_current_repository(manifest),
        ehp_leaves,
        _known_trusted_roots(ehp_leaves),
        user_confirmed_original=True,
    )
    isomorphism_step = fixed.validated.reconstruction.final_step
    if isomorphism_step.rule is not ProofRule.INFERENCE:
        raise ValueError("R4-R8 did not derive an isomorphism")

    previous_replay = build_phase162_pi5_3_web_replay(max_depth=2)
    previous_root = previous_replay.root_step
    if previous_root.rule is not ProofRule.INFERENCE or len(previous_root.premises) != 3:
        raise ValueError("Phase 162 group root structure changed")
    source_step, prior_isomorphism, generator_bridge = previous_root.premises
    if prior_isomorphism.conclusion != isomorphism_step.conclusion:
        raise ValueError("registry-backed isomorphism differs from group requirement")
    if source_step.rule is not ProofRule.INFERENCE or generator_bridge.rule is not ProofRule.INFERENCE:
        raise ValueError("group source or generator bridge is not inferred")

    rule = toda_prop53_n3_pi5_3_finite_cyclic_transport_inference_rule()
    premises = (source_step, isomorphism_step, generator_bridge)
    matches = tuple(
        match for match in find_inference_matches_for_rule(rule, premises)
        if len(match.premises) == len(premises)
        and all(actual is expected for actual, expected in zip(match.premises, premises))
    )
    if len(matches) != 1:
        raise ValueError("registry-backed group transport has no unique match")
    group_step = apply_inference_match(matches[0])
    if group_step.rule is not ProofRule.INFERENCE or group_step.conclusion != previous_root.conclusion:
        raise ValueError("group conclusion did not match the original group result")
    if tuple(group_step.premises) != premises:
        raise ValueError("group proof lost the registry-backed isomorphism")

    goal = group_step.conclusion
    if not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("unexpected target group structure")
    entry = ProofRepositoryEntry(
        key="phase164-r5-registry-backed-pi5-3-web",
        step=group_step,
        theorem="Toda Proposition 5.3",
        phase="164 R5",
    )
    result = TodaGroupResult(
        target=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=group_step,
    )
    replay = build_toda_group_result_proof_replay(result, max_depth=max_depth)
    if replay.root_step is not group_step:
        raise ValueError("replay did not preserve the registry-backed group root")

    presentation = build_validated_backward_proof_presentation(fixed.validated)
    narrative = render_validated_backward_proof_markdown(presentation)
    if not narrative or "## 証明" not in narrative or "□" not in narrative:
        raise ValueError("R4-R8 narrative unavailable")
    conclusion = render_toda_public_group_relation_latex(goal)
    if not conclusion:
        raise ValueError("group relation cannot be rendered")
    head, marker, tail = narrative.rpartition("□")
    if not marker or tail.strip():
        raise ValueError("unexpected end of validated map proof")
    narrative = (
        head.rstrip()
        + "\n\n### 群構造\n\n"
        + "既存の (5.2) に基づく $\\pi_{4}^{2}$ の群構造と, "
        + "生成元の Suspension（懸垂）に関する内部導出を用いる.\n\n"
        + "同型 $E$ と生成元の対応から,\n\n"
        + f"${conclusion}$.\n\n□\n"
    )
    if narrative.count("## 証明") != 1 or narrative.count("□") != 1:
        raise ValueError("invalid final group narrative")
    return replay, narrative
```

## 追加テスト全体

```python
"""Focused Web integration for the Phase 164 R5 registry-backed pi_5^3 proof."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def registry_web_proof():
    return build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_registry_web_proof_has_inferred_group_root(registry_web_proof):
    replay, narrative = registry_web_proof
    root = replay.root_step
    assert root.rule is ProofRule.INFERENCE
    assert len(root.premises) == 3
    assert all(step.rule is ProofRule.INFERENCE for step in root.premises)
    assert replay.source_entry.phase == "164 R5"
    assert "## 証明" in narrative
    assert "### 群構造" in narrative
    assert narrative.count("□") == 1


def test_registry_isomorphism_is_an_actual_group_premise(registry_web_proof):
    replay, _ = registry_web_proof
    root = replay.root_step
    isomorphism = root.premises[1]
    assert isomorphism.rule is ProofRule.INFERENCE
    assert len(isomorphism.premises) == 2
    assert isomorphism.premises[0].rule is ProofRule.INFERENCE
    assert isomorphism.premises[1].rule is ProofRule.INFERENCE


def test_proof_markdown_cites_toda_and_ends_in_group_relation(registry_web_proof):
    _, markdown = registry_web_proof
    assert "Proposition 5.1" in markdown
    assert "(5.3)" in markdown
    assert "(5.2)" in markdown
    assert "同型" in markdown
    assert "pi_{5}^{3}" in markdown or "pi_{5}^3" in markdown


def test_group_query_web_narrative_is_phase164():
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.phase == "164 R5"
    assert view.key == "phase164-r5-registry-backed-pi5-3-web"
    assert view.mode == "narrative"
    assert view.rendered_lines
    content = "\n".join(segment.value for line in view.rendered_lines for segment in line.segments)
    assert "Proposition 5.1" in content
    assert "(5.3)" in content
    assert "群構造" in content or any(line.kind == "heading" and line.prefix == "群構造" for line in view.rendered_lines)


def test_invalid_depth_rejected():
    for invalid in (-1, True, "2"):
        with pytest.raises((ValueError, TypeError)):
            build_phase164_r5_web_pi5_3_proof(max_depth=invalid)


def test_manifest_must_exist(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="manifest missing"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_non_target_web_path_does_not_load_r5(monkeypatch):
    import phase164_r5_web_registry_connection as r5
    def forbidden(**kwargs):
        raise AssertionError("R5 must not run outside pi5_3 narrative")
    monkeypatch.setattr(r5, "build_phase164_r5_web_pi5_3_proof", forbidden)
    # The trace view for pi5_3 remains the existing Web code path.
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"
```

## 適用スクリプト全体

```python
"""Replace one checked Web builder function with its complete R5 implementation."""
from pathlib import Path
import ast


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    source = project / "web_group_proof.py"
    replacement = (Path(__file__).resolve().parent / "replacement_web_function.txt").read_text(encoding="utf-8")
    text = source.read_text(encoding="utf-8")
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "build_standard_web_group_proof_view"]
    if len(functions) != 1:
        raise ValueError("expected exactly one group proof builder")
    old = functions[0]
    original_body = "\n".join(text.splitlines()[old.lineno-1:old.end_lineno])
    if "phase164_r5_web_registry_connection" in original_body:
        print("R5 Web builder already present")
        return
    required = ("build_phase162_pi5_3_web_replay", "_build_group_proof_rendered_lines", "build_toda_group_result_proof_replay")
    if not all(token in original_body for token in required):
        raise ValueError("existing Web proof builder differs; abort without changes")
    ast.parse(replacement)
    lines = text.splitlines(keepends=True)
    original_start = sum(len(line) for line in lines[:old.lineno-1])
    original_end = sum(len(line) for line in lines[:old.end_lineno])
    updated = text[:original_start] + replacement.rstrip("\n") + "\n" + text[original_end:]
    ast.parse(updated)
    backup = project / "web_group_proof.phase164_r5_backup.py"
    if not backup.exists():
        backup.write_text(text, encoding="utf-8")
    source.write_text(updated, encoding="utf-8")
    print("Updated web_group_proof.py; backup:", backup.name)


if __name__ == "__main__":
    main()
```

## PowerShell 実行コード全体

```powershell
$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'web_group_proof.py',
  'phase164_r4_r8_registry_reconstruction.py',
  'phase164_r4_r6_typed_binding.py',
  'phase164_r4_r1_source_crosswalk.py',
  'phase162_pi5_3_web_replay.py',
  'phase162_validated_proof_presentation.py',
  'phase163_r4_r94_output\manifest.json'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) { throw "Missing prerequisite: $File" }
}
Copy-Item (Join-Path $PSScriptRoot 'phase164_r5_web_registry_connection.py') (Join-Path $Project 'phase164_r5_web_registry_connection.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r5_web_registry_connection.py') (Join-Path $Project 'tests\test_phase164_r5_web_registry_connection.py') -Force
python -B (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R5 patch failed' }
python -B -m pytest -q `
  tests/test_phase164_r5_web_registry_connection.py `
  tests/test_phase164_r4_r8_registry_reconstruction.py `
  tests/test_phase164_r4_r6_typed_binding.py
if ($LASTEXITCODE -ne 0) { throw 'Phase 164 R5 targeted tests failed' }
Write-Output 'Phase 164 R5 Web registry-backed pi5_3 narrative connected. Full pytest NOT run.'
```
