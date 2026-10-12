# Phase 164 R5-R1 — 変更コード全文

変更対象: `phase164_r5_web_registry_connection.py`（全 import と変更対象関数を含むファイル全文）、`web_group_proof.py` の `build_standard_web_group_proof_view` 関数、`tests/test_phase164_r5_r1_common_renderer.py`、`tests/test_phase164_r5_web_registry_connection.py`、`apply_patch.py`、`run.ps1`。新規テスト関数はテストファイル末尾に追加。共通 Renderer 本体は変更しない。

## phase164_r5_web_registry_connection.py

```python
"""Phase 164 R5: live registry-backed pi_5^3 group proof for the Web narrative."""
from __future__ import annotations

from pathlib import Path

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_web_replay import build_phase162_pi5_3_web_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
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

    # Render the actual group-root proof through the shared pipeline.
    # No pi_5^3-specific sentences or concatenated markdown are permitted.
    presentation = build_toda_group_proof_presentation(replay)
    narrative = render_toda_group_proof_narrative_markdown(presentation)
    if not narrative or "## 証明" not in narrative:
        raise ValueError("common group narrative unavailable")
    return replay, narrative

```

## web_group_proof.py: 置換関数全文（import は変更なし）

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
  if n == 3 and k == 2 and mode == "narrative":
    from phase164_r5_web_registry_connection import (
      build_phase164_r5_web_pi5_3_proof,
    )
    replay, _common_markdown = build_phase164_r5_web_pi5_3_proof(
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
    presentation = build_toda_group_proof_presentation(replay)
    if mode == "outline":
      markdown = render_toda_group_proof_outline_markdown(presentation)
    else:
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

## tests/test_phase164_r5_r1_common_renderer.py

```python
"""R5-R1: pi_5^3 uses the same group proof presentation and renderer as other groups."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def proof():
    return build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_group_root_still_derived_from_registry_isomorphism(proof):
    replay, _ = proof
    assert replay.source_entry.phase == "164 R5"
    assert replay.root_step.rule is ProofRule.INFERENCE
    assert len(replay.root_step.premises) == 3
    assert replay.root_step.premises[1].rule is ProofRule.INFERENCE


def test_exact_common_renderer_output_without_pi53_appended_text(proof):
    replay, markdown = proof
    expected = render_toda_group_proof_narrative_markdown(
        build_toda_group_proof_presentation(replay)
    )
    assert markdown == expected
    assert "既存の (5.2) に基づく" not in markdown
    assert "生成元の Suspension（懸垂）に関する内部導出を用いる" not in markdown


def test_web_narrative_uses_shared_presentation(proof):
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.phase == "164 R5"
    assert view.mode == "narrative"
    assert view.rendered_lines
    assert view.conclusion_latex


def test_web_trace_and_other_group_unaffected():
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"


def test_invalid_depth_rejected():
    with pytest.raises((TypeError, ValueError)):
        build_phase164_r5_web_pi5_3_proof(max_depth=-1)

```

## tests/test_phase164_r5_web_registry_connection.py

```python
"""Phase 164 R5 regression tests after R5-R1 shared rendering unification."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown
from toda_group_proof_presentation import build_toda_group_proof_presentation
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


def test_registry_isomorphism_is_an_actual_group_premise(registry_web_proof):
    replay, _ = registry_web_proof
    root = replay.root_step
    isomorphism = root.premises[1]
    assert isomorphism.rule is ProofRule.INFERENCE
    assert len(isomorphism.premises) == 2
    assert all(step.rule is ProofRule.INFERENCE for step in isomorphism.premises)


def test_proof_markdown_comes_from_shared_renderer(registry_web_proof):
    replay, markdown = registry_web_proof
    assert markdown == render_toda_group_proof_narrative_markdown(
        build_toda_group_proof_presentation(replay)
    )
    assert "既存の (5.2) に基づく" not in markdown


def test_group_query_web_narrative_is_phase164():
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.phase == "164 R5"
    assert view.key == "phase164-r5-registry-backed-pi5-3-web"
    assert view.mode == "narrative"
    assert view.rendered_lines


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
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"

```

## apply_patch.py

```python
"""Replace the entire Web group builder, retaining a backup and unchanged imports."""
import ast
from pathlib import Path


def main() -> None:
    project = Path(__file__).resolve().parent.parent
    target = project / "web_group_proof.py"
    source = target.read_text(encoding="utf-8")
    tree = ast.parse(source)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "build_standard_web_group_proof_view"]
    if len(functions) != 1:
        raise ValueError("expected exactly one Web group proof builder")
    previous = functions[0]
    if "phase164_r5_web_registry_connection" not in ast.get_source_segment(source, previous):
        raise ValueError("Phase 164 R5 Web connection not installed; refusing to patch")
    replacement = (Path(__file__).parent / "replacement_web_function.txt").read_text(encoding="utf-8")
    ast.parse(replacement)
    current_lines = source.splitlines(keepends=True)
    start = sum(map(len, current_lines[:previous.lineno - 1]))
    finish = sum(map(len, current_lines[:previous.end_lineno]))
    updated = source[:start] + replacement.rstrip() + "\n" + source[finish:]
    ast.parse(updated)
    backup = project / "web_group_proof.phase164_r5_r1_backup.py"
    if updated == source:
        print("Common Renderer Web builder already installed")
        return
    if not backup.exists():
        backup.write_text(source, encoding="utf-8")
    target.write_text(updated, encoding="utf-8")
    print("Updated Web Group Proof builder; backup:", backup.name)


if __name__ == "__main__":
    main()

```

## run.ps1（ASCII 文字のみ・Windows PowerShell 5.1 対応）

```powershell
$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$env:PYTHONPATH = $Project
$Required = @(
  'web_group_proof.py',
  'phase164_r5_web_registry_connection.py',
  'phase164_r4_r8_registry_reconstruction.py',
  'phase164_r4_r6_typed_binding.py',
  'phase163_r4_r94_output\manifest.json'
)
foreach ($File in $Required) {
  if (-not (Test-Path (Join-Path $Project $File))) { throw "Missing prerequisite: $File" }
}
$Existing = Get-Content (Join-Path $Project 'phase164_r5_web_registry_connection.py') -Raw
if ($Existing -notmatch 'def build_phase164_r5_web_pi5_3_proof') {
  throw 'R5 source changed unexpectedly; aborting'
}
$Backup = Join-Path $Project 'phase164_r5_web_registry_connection.phase164_r5_r1_backup.py'
if (-not (Test-Path $Backup)) { Copy-Item (Join-Path $Project 'phase164_r5_web_registry_connection.py') $Backup }
Copy-Item (Join-Path $PSScriptRoot 'phase164_r5_web_registry_connection.py') (Join-Path $Project 'phase164_r5_web_registry_connection.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r5_r1_common_renderer.py') (Join-Path $Project 'tests\test_phase164_r5_r1_common_renderer.py') -Force
Copy-Item (Join-Path $PSScriptRoot 'tests\test_phase164_r5_web_registry_connection.py') (Join-Path $Project 'tests\test_phase164_r5_web_registry_connection.py') -Force
python -B (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R1 patch failed' }
python -B -m pytest -q `
  tests/test_phase164_r5_r1_common_renderer.py `
  tests/test_phase164_r5_web_registry_connection.py `
  tests/test_phase164_r4_r8_registry_reconstruction.py `
  tests/test_phase164_r4_r6_typed_binding.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R1 focused tests failed' }
Write-Output 'Phase 164 R5-R1 common renderer path installed. Full pytest NOT run.'

```

## テストと完了条件

局所 pytest で共通 Renderer を通過し、Web の pi_5^3 Narrative が生成されること。既存の群構造 ProofStep が根であり、その他の群や trace 経路を変更しないこと。全体 pytest は Phase 164 終了時に限る。次段階は共通 Renderer 自体の品質改善（必要な場合のみ）で、R5-R1 は Renderer 本体を変更しない。
