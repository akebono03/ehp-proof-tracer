"""Phase 165 R12-R34: presentation-only completed proof narrative helpers."""
from __future__ import annotations

from proof import ProofRule


def ordered_display_steps(root):
    """Postorder verified ancestry, no promoted goals and no ProofStep changes."""
    output = []
    seen = set()
    active = set()

    def visit(step):
        identifier = id(step)
        if identifier in active:
            raise ValueError("cyclic completed proof tree")
        if identifier in seen:
            return
        active.add(identifier)
        for premise in step.premises:
            visit(premise)
        active.remove(identifier)
        seen.add(identifier)
        output.append(step)

    visit(root)
    return tuple(output)


def completed_step_text(step, statement_math, fallback):
    """Replace exposed inference names with source-faithful mathematical prose."""
    rule = getattr(step.inference_rule, "name", "") or ""
    if rule == "infinite cyclic quotient structure":
        return "第一同型定理と無限巡回群の商群の構造より, " + statement_math(step.conclusion) + " ."
    if rule == "first isomorphism theorem for generated kernel":
        return "E の全射性と核の決定から, 第一同型定理により商群との同型を得る."
    if rule == "certified cyclic suspension kernel entails kernel multiple":
        return "完全性と核の生成元の記述より, " + statement_math(step.conclusion) + " ."
    if rule == "EHP suspension surjectivity implies whole image":
        return "E の全射性より, 像は終域全体に一致する."
    if rule == "whole image implies surjectivity":
        return "像が終域全体であるため, E は全射である."
    return fallback(step)


def completed_provenance_key(is_complete):
    return "generic-complete-proof" if is_complete else "generic-partial-proof"
