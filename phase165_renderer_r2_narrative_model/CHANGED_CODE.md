# Phase 165 Renderer R2 — 変更コード全文

変更対象: 新規 `phase165_renderer_narrative_model.py`（`NarrativeProofModel`、`build_narrative_proof_model`）。既存ファイルは無変更。
テスト: 新規 `test_phase165_renderer_r2_narrative_model.py`（全 import と全テスト関数）。
実行器: `install.py`, `run.ps1`。
追加位置: プロジェクト直下。

## phase165_renderer_narrative_model.py

```python
"""Shared, evidence-preserving input model for complete and incomplete narratives.

This module never infers facts, changes proof order, or formats Markdown.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofStep
from toda_group_proof_presentation import TodaGroupProofPresentation


@dataclass(frozen=True)
class NarrativeProofModel:
    """A common snapshot of evidence, not a claim of additional proof."""

    target: TodaPrimaryGroup
    status: ProofSearchStatus
    proven_steps: tuple[ProofStep, ...]
    open_goals: tuple[Any, ...]
    references: tuple[str, ...]
    diagnostics: tuple[str, ...]
    conclusion: Any | None
    root_step: ProofStep | None
    source_kind: str
    source: PartialProofResult | TodaGroupProofPresentation

    def __post_init__(self) -> None:
        if not isinstance(self.target, TodaPrimaryGroup):
            raise TypeError("target must be TodaPrimaryGroup")
        if not isinstance(self.status, ProofSearchStatus):
            raise TypeError("status must be ProofSearchStatus")
        if self.source_kind not in ("search_result", "presentation"):
            raise ValueError("unrecognized narrative source kind")
        if not isinstance(self.proven_steps, tuple) or not all(
            isinstance(step, ProofStep) for step in self.proven_steps
        ):
            raise TypeError("proven_steps must be a tuple of ProofStep")
        if not isinstance(self.open_goals, tuple):
            raise TypeError("open_goals must be a tuple")
        if not isinstance(self.references, tuple) or not all(
            isinstance(ref, str) for ref in self.references
        ):
            raise TypeError("references must be a tuple of strings")
        if not isinstance(self.diagnostics, tuple) or not all(
            isinstance(reason, str) for reason in self.diagnostics
        ):
            raise TypeError("diagnostics must be a tuple of strings")
        if self.root_step is not None and not isinstance(self.root_step, ProofStep):
            raise TypeError("root_step must be ProofStep or None")
        if self.status is ProofSearchStatus.COMPLETE:
            if self.conclusion is None or self.open_goals:
                raise ValueError("completed narrative needs a conclusion and no open goals")
        elif self.conclusion is not None:
            raise ValueError("incomplete narrative cannot claim a conclusion")


def build_narrative_proof_model(
    source: PartialProofResult | TodaGroupProofPresentation,
) -> NarrativeProofModel:
    """Normalize either existing proof input without changing its evidence."""
    if isinstance(source, PartialProofResult):
        roots = tuple(
            step for step in source.proven_steps
            if source.conclusion is not None and step.conclusion == source.conclusion
        )
        return NarrativeProofModel(
            target=source.target,
            status=source.status,
            proven_steps=source.proven_steps,
            open_goals=source.open_goals,
            references=source.references,
            diagnostics=source.diagnostics,
            conclusion=source.conclusion,
            root_step=roots[-1] if roots else None,
            source_kind="search_result",
            source=source,
        )
    if isinstance(source, TodaGroupProofPresentation):
        root = source.root_step
        return NarrativeProofModel(
            target=source.source_replay.group_result.target,
            status=ProofSearchStatus.COMPLETE,
            proven_steps=tuple(node.proof_step for node in source.nodes),
            open_goals=(),
            references=(),
            diagnostics=(),
            conclusion=root.conclusion,
            root_step=root,
            source_kind="presentation",
            source=source,
        )
    raise TypeError("source must be PartialProofResult or TodaGroupProofPresentation")
```

## test_phase165_renderer_r2_narrative_model.py

```python
"""R2 model contract: one evidence shape; no changes to existing renderers."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from phase165_renderer_narrative_model import (
    NarrativeProofModel,
    build_narrative_proof_model,
)
from proof import ProofRule, ProofStep


def test_r2_unsearched_model_keeps_original_target():
    result = make_partial_proof_result(n=200, k=90, status=ProofSearchStatus.NOT_SEARCHED)
    model = build_narrative_proof_model(result)
    assert isinstance(model, NarrativeProofModel)
    assert model.source is result
    assert model.target is result.target
    assert model.status is ProofSearchStatus.NOT_SEARCHED
    assert model.conclusion is None
    assert model.proven_steps == ()
    assert model.root_step is None


def test_r2_partial_keeps_goal_diagnostics_reference_and_step_identity():
    step = ProofStep(conclusion="known", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=3, k=1, status=ProofSearchStatus.PARTIAL,
        proven_steps=(step,), open_goals=("unknown",),
        references=("Toda Proposition 4.2",), diagnostics=("missing premise",),
    )
    model = build_narrative_proof_model(result)
    assert model.source_kind == "search_result"
    assert model.proven_steps[0] is step
    assert model.open_goals == ("unknown",)
    assert model.references == ("Toda Proposition 4.2",)
    assert model.diagnostics == ("missing premise",)
    assert model.conclusion is None


def test_r2_complete_search_model_root_identity_without_rederivation():
    step = ProofStep(conclusion="final", premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(
        n=2, k=1, status=ProofSearchStatus.COMPLETE,
        proven_steps=(step,), conclusion="final",
    )
    model = build_narrative_proof_model(result)
    assert model.status is ProofSearchStatus.COMPLETE
    assert model.root_step is step
    assert model.conclusion == "final"
    assert model.proven_steps == (step,)


def test_r2_presentation_model_keeps_actual_replay_steps():
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r56_presentation_adapter import render_completed_shared_narrative
    from homotopy_groups import FreeCyclicGroup, FiniteCyclicGroup
    from proof import ProofRule
    from proof_repository import ProofRepositoryEntry
    from toda_group_result import TodaGroupResult
    from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
    from toda_group_proof_presentation import build_toda_group_proof_presentation

    search = search_group_from_registered_goal(n=2, k=1)
    assert search.status is ProofSearchStatus.COMPLETE
    structure = search.conclusion.rhs
    assert isinstance(structure, (FreeCyclicGroup, FiniteCyclicGroup))
    root = tuple(
        step for step in search.proven_steps if step.conclusion == search.conclusion
    )
    assert len(root) == 1 and root[0].rule is ProofRule.INFERENCE
    entry = ProofRepositoryEntry(key="r2:model:pi32", step=root[0], phase="165")
    group = TodaGroupResult(
        target=search.target, group_structure=structure,
        generators=(structure.generator,),
        generator_orders=(None if isinstance(structure, FreeCyclicGroup) else structure.order,),
        source_entry=entry, proof_step=root[0],
    )
    presentation = build_toda_group_proof_presentation(
        build_complete_toda_group_result_proof_replay(group)
    )
    model = build_narrative_proof_model(presentation)
    assert model.status is ProofSearchStatus.COMPLETE
    assert model.source is presentation
    assert model.root_step is presentation.root_step
    assert model.proven_steps == tuple(node.proof_step for node in presentation.nodes)
    assert model.target == search.target
    assert model.open_goals == ()
    assert "証明対象" in render_completed_shared_narrative(search)


def test_r2_rejects_unknown_sources():
    with pytest.raises(TypeError):
        build_narrative_proof_model(object())


def test_r2_does_not_mutate_existing_markdown():
    result = make_partial_proof_result(n=3, k=1, status=ProofSearchStatus.NOT_SEARCHED)
    before = render_partial_proof_markdown(result)
    model = build_narrative_proof_model(result)
    after = render_partial_proof_markdown(result)
    assert model.source is result
    assert before == after
```

## install.py

```python
"""Install a single additional R2 module without editing production sources."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def install(project: Path, package: Path) -> str:
    target = project / "phase165_renderer_narrative_model.py"
    source = package / "phase165_renderer_narrative_model.py"
    content = source.read_text(encoding="utf-8")
    ast.parse(content)
    if target.exists():
        old = target.read_text(encoding="utf-8")
        if old == content:
            return "ALREADY_INSTALLED"
        raise RuntimeError("R2 model already exists with different content; not overwriting")
    shutil.copy2(source, target)
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("Phase165 Renderer R2:", install(package.parent, package))
    print("No existing renderer or proof search code changed; full pytest NOT run")
```

## run.ps1

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$env:PYTHONPATH = if ([string]::IsNullOrEmpty($env:PYTHONPATH)) { $project } else { "$project$([IO.Path]::PathSeparator)$env:PYTHONPATH" }
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R2 install failed' }
& $python -m pytest -q (Join-Path $package 'test_phase165_renderer_r2_narrative_model.py')
if ($LASTEXITCODE -ne 0) { throw 'R2 targeted pytest failed' }
Write-Output 'R2 model installed. Targeted pytest passed; existing renderers unchanged; full pytest NOT run.'
```
