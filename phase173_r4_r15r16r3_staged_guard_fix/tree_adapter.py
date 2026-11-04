"""Render any already-verified proof subtree with the canonical Narrative Model.

This adapter owns no statement-specific sentences and no source discovery.
The original searched result remains intact; the scoped display view exists
only to feed a second verified tree to the *same* public model renderer.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, ProofStep


def verified_tree_postorder(root: ProofStep) -> tuple[ProofStep, ...]:
    """Visit every actual premise once, with cycle and inference guards."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    active: set[int] = set()
    visited: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("proof ancestry contains a non-ProofStep")
        identity = id(step)
        if identity in active:
            raise ValueError("cyclic proof ancestry")
        if identity in visited:
            return
        active.add(identity)
        if step.rule is ProofRule.GIVEN and step.premises:
            raise ValueError("a given step cannot consume premises")
        if step.rule is ProofRule.INFERENCE:
            rule = step.inference_rule
            if rule is None:
                raise ValueError("an inferred step requires its actual inference rule")
            guard = rule.match_guard
            if guard is not None and not guard(step.premises, ()):
                raise ValueError("unverified inference guard in proof ancestry")
        for premise in step.premises:
            visit(premise)
        active.remove(identity)
        visited.add(identity)
        ordered.append(step)

    visit(root)
    if not ordered or ordered[-1] is not root:
        raise ValueError("verified root missing from the ordered ancestry")
    return tuple(ordered)


def render_verified_tree_progress(
    target: TodaPrimaryGroup,
    root: ProofStep,
) -> tuple[str, ...]:
    """Reuse the exact canonical model-backed renderer for a certified tree.

    This presentation-only scope is not a second search and cannot create a
    named-group conclusion. Its public output is limited to source-backed
    Reference entries and renderable ProofSteps. Unsupported GIVEN types stay
    in the proof tree but are not fabricated into mathematical assertions.
    """
    if not isinstance(target, TodaPrimaryGroup):
        raise TypeError("target must be a TodaPrimaryGroup")
    steps = verified_tree_postorder(root)
    if root.rule is not ProofRule.INFERENCE:
        raise ValueError("a verified evidence root must be an inference")
    # This view is never published as a search result or used to decide status.
    # The real PartialProofResult retains all named open goals and diagnostics.
    scope = PartialProofResult(
        target=target,
        status=ProofSearchStatus.PARTIAL,
        proven_steps=steps,
    )
    model = build_proof_narrative_model(scope)
    markdown = render_model_backed_narrative_markdown(scope, model)
    reference_header = "## 使用する結果"
    proof_header = "## 証明"
    step_header = "### 確認済み ProofStep（与件を含む）"
    heading_lines = markdown.splitlines()
    if (heading_lines.count(reference_header) != 1
            or heading_lines.count(proof_header) != 1
            or heading_lines.count(step_header) != 1):
        raise ValueError("canonical renderer output has changed")
    source_section = markdown.split(reference_header, 1)[1].split("\n---\n", 1)[0]
    body_section = markdown.split(step_header, 1)[1]
    source_lines = [line.strip() for line in source_section.splitlines() if line.strip()]
    if "参照情報を持つ ProofStep はありません。" in source_lines:
        source_lines.remove("参照情報を持つ ProofStep はありません。")
    if not model.citations:
        raise ValueError("verified tree has no source-backed Reference")
    if not any(f"[R{citation.number}]" in line for line in source_lines
               for citation in model.citations):
        raise ValueError("the shared renderer dropped proof-tree citations")
    proof_lines = [
        line.strip() for line in body_section.splitlines()
        if line.lstrip().startswith(("- 与件:", "- 推論:"))
        and "（数式表示未対応）" not in line
    ]
    if not proof_lines:
        raise ValueError("verified evidence tree has no renderable ProofStep")
    return tuple([
        "### 検証済み証明木の Reference", "",
        *source_lines, "",
        "### 検証済み ProofStep", "",
        *proof_lines,
    ])
