"""Phase 173 R15R17: merge only actually certified steps into the existing model.

All replacements are strict and repeat-safe. They operate on reviewed functions,
not on rendered prose or source-matching n/k specializations.
"""
from __future__ import annotations

from collections.abc import Callable


MODEL = "phase168_r3_3_proof_narrative_model.py"
BINDING = "phase168_r3_12_body_binding.py"
WEB = "web_group_proof_common.py"
PROJECTION = "phase173_r4_r15r9_shared_abstract_renderer/projection.py"
ADAPTER = "phase165_r52_r3_web_adapter.py"

EXPECTED_BLOBS = {
    MODEL: "5bc85174ec5b04924603e7160a3fb262041e00fd",
    BINDING: "ac7d387158b0af8ead4b07f623c216ed1dd561dd",
    WEB: "7604290870e094ae7e67e2a364f986895a41e515",
    PROJECTION: "924fca4ff224e8333028646cf68250e11bee88fb",
    ADAPTER: "6d9b21dd1c180872bbe350035da054e2cca10ead",
}

NEW_STEPS_HELPER = '''def verified_narrative_steps(result: PartialProofResult) -> tuple[ProofStep, ...]:
    """Join actual searched steps and a separately certified tree without inference.

    Search results remain immutable. A certified inference root contributes its
    actual guarded ancestry once, with original ProofStep identities retained.
    The returned sequence is presentation data, never a named proof result.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    existing = list(result.proven_steps)
    structure = result.abstract_structure
    if structure is None:
        return tuple(existing)
    if structure.group != result.target or result.status is ProofSearchStatus.COMPLETE:
        raise ValueError("incompatible abstract certificate for narrative")

    from phase173_r4_r15r16r3_staged_guard_fix.tree_adapter import (
        verified_tree_postorder,
    )
    for step in verified_tree_postorder(structure.proof_step):
        if not any(previous is step for previous in existing):
            existing.append(step)
    return tuple(existing)


'''

ABSTRACT_LATEX = '''  abstract_group = getattr(statement, "group", None)
  abstract_invariants = getattr(statement, "invariant_summands", None)
  if (isinstance(abstract_group, TodaPrimaryGroup)
      and type(abstract_group.group_dimension) is int
      and type(abstract_group.sphere_dimension) is int
      and isinstance(abstract_invariants, tuple)):
    # A typed, already verified abstract invariant has no named generator.
    # This is a generic statement formatter, not an inference or Narrative.
    from phase173_r4_r15r9_shared_abstract_renderer.projection import (
      abstract_invariants_latex,
    )
    invariant_latex = abstract_invariants_latex(abstract_invariants)
    return (
      rf"\\pi_{{{abstract_group.group_dimension}}}^{{{abstract_group.sphere_dimension}}}"
      rf" \\cong {invariant_latex}",
      None,
    )

'''


def replace_once(source: str, original: str, replacement: str, name: str) -> str:
    if source.count(original) != 1:
        raise RuntimeError(f"R15R17 unreviewed or already patched anchor: {name}")
    return source.replace(original, replacement, 1)


def modify_model(source: str) -> str:
    source = replace_once(
        source, "def build_proof_narrative_model(\n",
        NEW_STEPS_HELPER + "def build_proof_narrative_model(\n",
        "new verified_narrative_steps before build_proof_narrative_model",
    )
    return replace_once(
        source, "    steps = result.proven_steps\n",
        "    steps = verified_narrative_steps(result)\n",
        "model step projection",
    )


def modify_binding(source: str) -> str:
    source = replace_once(
        source,
        "from phase168_r3_3_proof_narrative_model import ProofNarrativeModel\n",
        "from phase168_r3_3_proof_narrative_model import ProofNarrativeModel, verified_narrative_steps\n",
        "binding complete import",
    )
    return replace_once(
        source,
        '    if model.steps != result.proven_steps:\n        raise ValueError("model steps must match the searched result")\n',
        '    if model.steps != verified_narrative_steps(result):\n        raise ValueError("model steps must match the verified searched and certified trees")\n',
        "binding proof authenticity guard",
    )


def modify_web(source: str) -> str:
    return replace_once(
        source,
        "  public_group_latex = (\n",
        ABSTRACT_LATEX + "  public_group_latex = (\n",
        "generic typed abstract invariants formatting",
    )


def modify_projection(source: str) -> str:
    return replace_once(
        source,
        '        raise ValueError("unverified Model abstract result cannot be presented")\n    return _render_abstract_claim(model.target, structure)\n',
        '        raise ValueError("unverified Model abstract result cannot be presented")\n'
        '    # The certified root is already a normal ProofStep in the unified Model.\n'
        '    # Do not render the same tree a second time as a separate appendix.\n'
        '    if any(step is structure.proof_step for step in model.steps):\n'
        '        return ""\n'
        '    return _render_abstract_claim(model.target, structure)\n',
        "suppress duplicated abstract appendix when root is in the Model",
    )


def modify_adapter(source: str) -> str:
    return replace_once(
        source,
        "    steps = []\n    for step in result.proven_steps:\n",
        "    steps = []\n"
        "    display_steps = (\n"
        "        narrative_model.steps\n"
        "        if narrative_model is not None and mode != \"trace\"\n"
        "        else result.proven_steps\n"
        "    )\n"
        "    for step in display_steps:\n",
        "Web step view projection of verified model data",
    )


TRANSFORMS: dict[str, Callable[[str], str]] = {
    MODEL: modify_model,
    BINDING: modify_binding,
    WEB: modify_web,
    PROJECTION: modify_projection,
    ADAPTER: modify_adapter,
}
