# R57-R10 変更コード全文

変更ファイル: `phase165_r56_presentation_adapter.py` の `render_completed_shared_narrative`。既存 import に変更なし。新規ファイル: `phase165_r57_r10_step_narrative.py`（ファイル全体）。テストは新規ファイル全体を掲載。

## 置換する関数全文

```python
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

## 新規モジュール全文

```python
"""Shared typed-proof Narrative used when a legacy transport display would misstate ancestry.

This is an internal presentation helper; the one public entry remains
render_toda_group_proof_narrative_markdown. No theorem or premise is invented.
"""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofRule, ProofStep
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from web_group_proof_common import _group_proof_statement_latex


def ordered_proof_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Return deduplicated ancestors before dependents, including the root."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be ProofStep")
    seen: set[int] = set()
    active: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("every proof premise must be ProofStep")
        key = id(step)
        if key in active:
            raise ValueError("cyclic ProofStep ancestry")
        if key in seen:
            return
        active.add(key)
        for premise in step.premises:
            visit(premise)
        active.remove(key)
        seen.add(key)
        ordered.append(step)

    visit(root)
    return tuple(ordered)


def has_transport_proof_ancestry(root: ProofStep) -> bool:
    """Inspect proved inferences, never infer transport from a group number."""
    return any(
        step.rule is ProofRule.INFERENCE
        and (
            "transport" in str(getattr(step.inference_rule, "name", "")).lower()
            or "4.5" in str(getattr(step.inference_rule, "name", ""))
        )
        for step in ordered_proof_ancestry(root)
    )


def _math_statement(statement: object) -> str:
    latex, _fallback = _group_proof_statement_latex(statement)
    if latex is None:
        raise ValueError("typed mathematical statement cannot be rendered")
    return "$" + latex + "$"


def _reference_label(step: ProofStep) -> str:
    metadata = getattr(step.inference_rule, "literature_reference", None)
    locator = getattr(metadata, "locator", None) or getattr(metadata, "label", None)
    if locator:
        return str(locator)
    name = str(getattr(step.inference_rule, "name", ""))
    if name.startswith("Adopted literature "):
        return name.removeprefix("Adopted literature ")
    raise ValueError("GIVEN ProofStep has no source locator; refuse citation-free narrative")


def render_completed_from_proofsteps(result: PartialProofResult, root: ProofStep) -> str:
    """Render facts, citations, and rules from actual completed ProofSteps only."""
    if not isinstance(result, PartialProofResult) or result.status is not ProofSearchStatus.COMPLETE:
        raise ValueError("complete typed proof result required")
    if root.conclusion != result.conclusion or root.rule is not ProofRule.INFERENCE:
        raise ValueError("root must prove the completed conclusion")
    ancestry = ordered_proof_ancestry(root)
    leaves = tuple(step for step in ancestry if step.rule is ProofRule.GIVEN)
    inferences = tuple(step for step in ancestry if step.rule is ProofRule.INFERENCE)
    if not leaves or not inferences:
        raise ValueError("completed proof must contain cited leaves and inference")
    citations: dict[int, str] = {}
    reference_rows: list[str] = []
    for step in leaves:
        label = _reference_label(step)
        number = len(reference_rows) + 1
        citations[id(step)] = f"[R{number}]"
        reference_rows.append(f"**[R{number}] {label}.**")
        reference_rows.append(_render_generic_narrative_step(step))
        reference_rows.append("")

    lines = [
        "## 証明対象", "", _math_statement(root.conclusion), "",
        "## 使用する結果", "", *reference_rows, "---", "", "## 証明", "",
    ]
    for step in inferences:
        rule = getattr(step.inference_rule, "name", None)
        if not rule:
            raise ValueError("inference ProofStep lacks a named inference rule")
        parents = [citations[id(p)] for p in step.premises if id(p) in citations]
        prefix = "、".join(dict.fromkeys(parents)) + "に基づき、" if parents else "前段の導出を用い、"
        if step is root:
            lines.append(f"{prefix}{rule} を適用する。")
        else:
            lines.append(f"{prefix}{rule} により、{_render_generic_narrative_step(step)}")
        lines.append("")
    lines.append("以上より, " + _math_statement(root.conclusion) + ". □")
    return "\n".join(lines)
```

## 新規テスト全文

```python
"""Proof ancestry, not a legacy stable-display branch, controls the public claim."""
from __future__ import annotations

from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r57_r10_step_narrative import has_transport_proof_ancestry, ordered_proof_ancestry
from proof import ProofRule


def _result():
    result = search_group_from_registered_goal(n=4, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    return result


def test_r10_stable_target_is_completed_without_transport_inference():
    result = _result()
    roots = [s for s in result.proven_steps if s.conclusion == result.conclusion]
    assert len(roots) == 1
    assert roots[0].rule is ProofRule.INFERENCE
    assert len(ordered_proof_ancestry(roots[0])) >= 2
    assert not has_transport_proof_ancestry(roots[0])


def test_r10_public_narrative_matches_actual_nontransport_proof():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    text = render_partial_proof_markdown(_result())
    assert "Proposition 5.1" in text
    assert "使用する結果" in text
    assert "証明" in text
    assert "□" in text
    assert "(4.5)" not in text
    assert "安定輸送" not in text


def test_r10_existing_pi32_narrative_is_preserved():
    from phase165_r52_partial_proof import render_partial_proof_markdown
    text = render_partial_proof_markdown(search_group_from_registered_goal(n=2, k=1))
    assert "使用する結果" in text
    assert "証明" in text
    assert "□" in text


def test_r10_adapter_does_not_remove_legacy_renderer():
    text = Path(__file__).resolve().parent.parent.joinpath("toda_group_proof_narrative_renderer.py").read_text(encoding="utf-8")
    assert "_phase160_r7_render_stable_finite_cyclic_transport_narrative" in text
```
