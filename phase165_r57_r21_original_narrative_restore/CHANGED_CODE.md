# 変更コード全文

対象: `phase165_r56_presentation_adapter.py` 全文、`phase165_r52_partial_proof.py` 内 `render_partial_proof_markdown()` 全体。

## 完成証明 Adapter（import 全文）

```python
"""Adapt completed canonical searches to the established public Toda narrative.

All mathematical evidence comes from the typed search's ProofStep ancestry.
The existing public renderer owns headings, citations and mathematical prose.
"""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofRule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Render only the completed search's actual proof ancestry.

    The historical stable-transport branch is not admissible for a root
    lacking a transport inference. Other completed presentations keep their
    existing public renderer path, including historical pi3^2 formatting.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    conclusion = result.conclusion
    if getattr(conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    structure = getattr(conclusion, "rhs", None)
    if not isinstance(structure, (FreeCyclicGroup, FiniteCyclicGroup, DirectSumGroup)):
        raise ValueError("unsupported group structure in completed goal")
    roots = [step for step in result.proven_steps if step.conclusion == conclusion]
    if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
        raise ValueError("completed proof must contain exactly one derived root")
    root = roots[0]
    if isinstance(structure, FreeCyclicGroup):
        generators = (structure.generator,)
        orders = (None,)
    elif isinstance(structure, FiniteCyclicGroup):
        generators = (structure.generator,)
        orders = (structure.order,)
    else:
        raise ValueError("direct-sum presentation requires typed generators")
    entry = ProofRepositoryEntry(key="phase165:typed:completed", step=root, phase="165")
    group_result = TodaGroupResult(
        target=result.target,
        group_structure=structure,
        generators=generators,
        generator_orders=orders,
        source_entry=entry,
        proof_step=root,
    )
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)

    from toda_group_proof_narrative_renderer import (
        _phase160_r7_render_stable_finite_cyclic_transport_narrative,
    )
    from phase165_r57_r10_step_narrative import (
        has_transport_proof_ancestry,
        render_completed_from_proofsteps,
    )
    if (
        not has_transport_proof_ancestry(root)
        and _phase160_r7_render_stable_finite_cyclic_transport_narrative(presentation) is not None
    ):
        return render_completed_from_proofsteps(result, root)
    return render_toda_group_proof_narrative_markdown(presentation)

```

## 置換する公開関数全体

```python
def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Use the original full Narrative for completed search; retain partial display."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    return render_toda_partial_proof_narrative_markdown(result)

```

## テスト全文（import を含む）

```python
"""Focused restoration checks for completed vs incomplete public narrative."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def test_completed_entry_calls_original_adapter(monkeypatch):
    import phase165_r56_presentation_adapter as adapter
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    monkeypatch.setattr(adapter, "render_completed_shared_narrative", lambda _: "ORIGINAL_NARRATIVE_SENTINEL")
    assert render_partial_proof_markdown(result) == "ORIGINAL_NARRATIVE_SENTINEL"


def test_incomplete_entry_stays_partial_renderer(monkeypatch):
    import toda_group_proof_generic_narrative_renderer as generic
    result = search_group_from_registered_goal(n=3, k=1)
    assert result.status is not ProofSearchStatus.COMPLETE
    monkeypatch.setattr(generic, "render_toda_partial_proof_narrative_markdown", lambda _: "PARTIAL_SENTINEL")
    assert render_partial_proof_markdown(result) == "PARTIAL_SENTINEL"


def test_real_completed_pi32_uses_original_narrative():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    actual = render_partial_proof_markdown(result)
    assert actual == render_completed_shared_narrative(result)
    assert "証明" in actual
    assert "以上より" in actual
    assert "前提（出典情報未接続）" not in actual


def test_restored_adapter_preserves_original_call():
    project = Path(__file__).resolve().parent.parent
    source = (project / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    ast.parse(source)
    assert "build_complete_toda_group_result_proof_replay" in source
    assert "render_toda_group_proof_narrative_markdown" in source


def test_restore_is_idempotent():
    from importlib.util import module_from_spec, spec_from_file_location
    folder = Path(__file__).resolve().parent
    spec = spec_from_file_location("phase165_restore_installer", folder / "install.py")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    assert module.install(folder.parent, folder) == "ALREADY_INSTALLED"

```

新規ファイル追加位置: リポジトリ直下に `phase165_r57_r21_original_narrative_restore/` を配置し、そのディレクトリにインストーラー・テストを追加。新規プロダクション関数はなし。

対象 pytest: `python -m pytest -q phase165_r57_r21_original_narrative_restore/test_original_narrative_restore.py`。

完了条件: 旧完成 Renderer を実際に通り、部分証明の表示を維持する。次 Phase R27 では Adapter 廃止監査のみを扱う。
