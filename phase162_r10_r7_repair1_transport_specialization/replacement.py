from collections.abc import Callable

from proof import ProofStep
from toda_stable_group_transport import (
    _concrete_toda_group_matches_structural_group,
)
from toda_group_proof_narrative_transport_facts import (
    extract_suspension_transport_facts,
)


def render_suspension_transport_link(
    root: ProofStep,
    render_step_latex: Callable[[ProofStep], str | None],
) -> str | None:
    """Render a transport used for the current target, not a remote ancestor.

    Legacy concretizations carry the symbolic family transport through a
    non-INFERENCE root.  Preserve that existing display contract, while
    checking target identity for inference-backed reconstructed roots.
    """
    facts = extract_suspension_transport_facts(root)
    if facts is None:
        return None
    if root.conclusion.lhs == facts.source_group_step.conclusion.lhs:
        return None

    destination_matches = _concrete_toda_group_matches_structural_group(
        root.conclusion.lhs,
        facts.transported_group_step.conclusion.lhs,
    )
    if not destination_matches:
        if root.inference_rule is not None:
            return None
        if not root.premises:
            return None
        # The older concrete-specialization proof uses a symbolic family
        # witness; both conclusions must retain the same finite group order.
        if root.conclusion.rhs.order != facts.transported_group_step.conclusion.rhs.order:
            return None

    source = render_step_latex(facts.source_group_step)
    isomorphism = render_step_latex(facts.isomorphism_step)
    transported = render_step_latex(facts.transported_group_step)
    bridge = render_step_latex(facts.generator_bridge_step)
    if not all((source, isomorphism, transported, bridge)):
        return None
    return (
        "証明木に記録された群構造の移送について、"
        f"${source}$ と ${isomorphism}$ から ${transported}$ を得る。"
        f"生成元の対応は ${bridge}$ である。"
    )
