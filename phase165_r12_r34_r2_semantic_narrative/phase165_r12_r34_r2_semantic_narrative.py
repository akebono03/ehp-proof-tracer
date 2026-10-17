"""Phase 165 R12-R34-R2: typed, evidence-preserving completed Narrative."""
from __future__ import annotations

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from proof import ProofRule, Relation, RelationType
from phase165_r12_r2_quotient_rules import (
    CyclicStructureStatement, KernelMultipleStatement, QuotientIsomorphismStatement,
)


def semantic_completed_lines(steps, root, target, statement_math, label, citation_numbers):
    """Render completed ancestry; never infer a statement or invent a citation."""
    from toda_group_proof_narrative_shared_components import _render_generic_narrative_step
    from phase165_r12_r2_quotient_rules import HomomorphismPresentationStatement
    from map_property_rules import ImageWholeStatement, SurjectiveMapStatement
    from phase165_r14_r6_generic_iso import MapSurjective
    from toda_rules import TodaProp42ExactnessStatement

    output = []
    mentioned = set()
    primary_exactness = None
    for step in steps:
        statement = step.conclusion
        if isinstance(statement, TodaProp42ExactnessStatement):
            window = statement.window
            if target in (window.source_term, window.middle_term, window.target_term):
                if window.middle_term == target or primary_exactness is None:
                    primary_exactness = step
    seen_exactness = False
    quoted_earlier = set()
    for step in steps:
        if step is root:
            continue
        statement = step.conclusion
        rule = str(getattr(getattr(step, "inference_rule", None), "name", "") or "")
        locator = label(step) if step.rule is ProofRule.GIVEN else None
        # Never silently suppress an uncited proof leaf.
        if step.rule is ProofRule.GIVEN and locator is None:
            output.extend(["要出典確認（証明木の GIVEN）: " + statement_math(statement), ""])
            continue
        # Cite the fixed literature in the reference section, not once more as raw prose.
        if step.rule is ProofRule.GIVEN:
            continue
        if isinstance(statement, TodaProp42ExactnessStatement):
            if not seen_exactness and step is primary_exactness:
                try:
                    from map_facts import EHP_E_MAP, EHP_H_MAP
                    w = statement.window
                    if w.first_map == EHP_E_MAP and w.second_map == EHP_H_MAP:
                        output.extend(["EHP 完全列 $"+_group(w.source_term)+r"\xrightarrow{E}"+_group(w.middle_term)+r"\xrightarrow{H}"+_group(w.target_term)+"$ を考える。",""])
                    else:
                        output.extend(["EHP 完全性を用いる。",""])
                except (AttributeError, TypeError):
                    output.extend(["EHP 完全性を用いる。", ""])
                seen_exactness = True
            continue
        # A completed earlier-group statement can be cited without replaying its steps
        # only when its actual inference proof tree is preserved as an ancestor.
        if (isinstance(statement, Relation) and statement.relation_type is RelationType.EQUALITY
                and isinstance(statement.lhs, TodaPrimaryGroup) and statement.lhs != target
                and isinstance(statement.rhs, FreeCyclicGroup)
                and step.rule is ProofRule.INFERENCE):
            earlier = statement.lhs
            if earlier not in quoted_earlier:
                quoted_earlier.add(earlier)
                output.extend(["先に導出した " + statement_math(statement) + " を用いる。", ""])
            continue
        if isinstance(statement, KernelMultipleStatement):
            expression = _element(statement.source_generator)
            output.extend([r"完全性より, $\ker E=\langle "+str(statement.multiple)+expression+r"\rangle$ である。", ""])
            continue
        if isinstance(statement, QuotientIsomorphismStatement):
            output.extend(["全射性と核の決定から, 第一同型定理より " +
                "$"+_group(statement.codomain)+r"\cong "+_group(statement.domain)+r"/\langle "+str(statement.multiple)+_element(statement.source_generator)+r"\rangle$ を得る。", ""])
            continue
        if isinstance(statement, CyclicStructureStatement):
            if statement.group == target:
                output.extend(["無限巡回群の商群構造より, " + _group(target)+r" は位数 "+str(statement.order)+" の巡回群である。", ""])
            continue
        if isinstance(statement, (ImageWholeStatement, SurjectiveMapStatement, MapSurjective)):
            if "surjective" not in mentioned:
                mentioned.add("surjective")
                output.extend(["完全性と後続項の消滅より, $E$ は全射である。", ""])
            continue
        if isinstance(statement, HomomorphismPresentationStatement):
            continue
        if rule in ("infinite cyclic quotient structure", "proved free cyclic group relation implies infinite cyclic structure",
                    "first isomorphism theorem for generated kernel", "EHP exactness implies image equals kernel",
                    "EHP Delta image and exactness imply concrete suspension kernel",
                    "certified cyclic suspension kernel entails kernel multiple",
                    "cited eta generator suspension yields presentation in target notation"):
            continue
        # Detailed derivations of a different group should not flood the current body;
        # they remain fully present in the immutable ProofStep ancestry.
        if isinstance(statement, Relation) and isinstance(statement.lhs, TodaPrimaryGroup) and statement.lhs != target:
            continue
        text = _render_generic_narrative_step(step)
        if text and not (text == rule and text.isascii()):
            if text not in mentioned and "数式表示未対応" not in text:
                mentioned.add(text)
                output.extend([text, ""])
    return output


def _group(group):
    if not isinstance(group, TodaPrimaryGroup):
        raise ValueError("expected typed Toda group")
    return r"\pi_{"+str(group.group_dimension)+"}^{"+str(group.sphere_dimension)+"}"


def _element(element):
    from web_group_proof_common import _group_proof_statement_latex
    from expression import HomotopyElement
    if not isinstance(element, HomotopyElement):
        raise ValueError("expected typed generator")
    family = getattr(element.generator,"family",None)
    index = getattr(element.generator,"index",None)
    if family is None or type(index) is not int:
        raise ValueError("generator requires a typed family and index")
    return str(family)+"_{"+str(index)+"}"
