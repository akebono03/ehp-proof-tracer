"""Proof-tree-backed transport prose for the existing common narrative.

Never supplies missing premises, literature references, or symbolic substitutions.
"""

from collections.abc import Callable

from proof import ProofStep
from toda_group_proof_narrative_transport_facts import (
    extract_suspension_transport_facts,
)


def render_suspension_transport_link(
    root: ProofStep,
    render_step_latex: Callable[[ProofStep], str | None],
) -> str | None:
    """Describe a verified connected chain using only its stored statements."""
    facts = extract_suspension_transport_facts(root)
    if facts is None:
        return None
    # The stable base may contain a symbolic family-transport proof in its
    # ancestry.  The base itself is not the transported target.  Check the
    # recorded source/target group statements rather than a stem number.
    if root.conclusion.lhs == facts.source_group_step.conclusion.lhs:
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


def add_transport_link_to_common_markdown(
    root: ProofStep,
    markdown: str,
    render_step_latex: Callable[[ProofStep], str | None],
) -> str:
    """Append a tree-backed explanation to proof body, ahead of its QED.

    The source is always the ProofStep graph.  No branch uses the target
    group's stem or reconstructs references.  Existing text is preserved.
    """
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    if "## 証明\n" not in markdown:
        return markdown
    paragraph = render_suspension_transport_link(root, render_step_latex)
    if paragraph is None or paragraph in markdown:
        return markdown
    for qed in ("\n\n$\\square$", "\n\n□"):
        position = markdown.rfind(qed)
        if position >= 0:
            return markdown[:position].rstrip() + "\n\n" + paragraph + markdown[position:]
    return markdown.rstrip() + "\n\n" + paragraph + "\n"
