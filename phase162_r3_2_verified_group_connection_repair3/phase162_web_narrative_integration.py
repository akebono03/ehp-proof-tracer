"""Phase 162 R5: add a separately validated map-isomorphism proof to web narrative."""

from homotopy_groups import TodaEHPExactnessWindow, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase161_r5_backward_proof_reconstruction import phase161_r5_target_goal
from phase161_r7_premise_provenance_validation import (
    reconstruct_phase161_r7_validated_goal,
)
from phase162_validated_proof_presentation import (
    build_validated_backward_proof_presentation,
    render_validated_backward_proof_markdown,
)
from probes.probe_phase55_capabilities import build_phase55_representative_result
from probes.probe_phase58_capabilities import build_phase58_representative_result
from proof import ProofRule, ProofStep
from toda_rules import TodaProp42ExactnessStatement


from homotopy_groups import FiniteCyclicGroup, TodaSuspensionMap
from phase162_r2_existing_proof_connection import (
    reconstruct_phase162_r2_from_existing_proofs,
)
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from probes.probe_phase50_capabilities import build_phase50_representative_result
from probes.probe_phase56_capabilities import build_phase56_representative_result
from proof import Relation, RelationType, apply_inference_match, find_inference_match
from toda_rules import (
    toda_52_pi4_2_finite_cyclic_transport_inference_rule,
    toda_eta_family_definition_statement,
    toda_prop53_n3_eta_square_suspension_bridge_inference_rule,
)

def _format_phase162_proof_sentences(markdown: str) -> str:
    """Use ASCII prose punctuation and separate sentences in the proof body.

    Preserve the reference block and math strings unchanged.  All newlines are
    paragraph boundaries because the web narrative Markdown renderer may
    collapse a single newline inside a paragraph.
    """
    if "## 証明\n" not in markdown:
        return markdown
    prefix, proof = markdown.split("## 証明\n", 1)
    paragraphs = []
    for block in proof.split("\n\n"):
        if not block.strip():
            continue
        if block.startswith("### ") or block.strip() == "□":
            paragraphs.append(block.strip())
            continue
        parts = block.split("。")
        for index, part in enumerate(parts):
            sentence = part.strip().replace("、", ", ")
            if not sentence:
                continue
            # The delimiter was a Japanese full stop.  Existing English
            # periods (including math source numbers) are not split.
            if index < len(parts) - 1:
                sentence += "."
            paragraphs.append(sentence)
    return prefix + "## 証明\n\n" + "\n\n".join(paragraphs) + "\n"


def _compose_phase162_group_conclusion(markdown: str) -> str:
    """Connect the verified map goal to this existing n=3, k=2 group result.

    This is a Web presentation of a separately known pi_4^2 group and its
    generator suspension, not an additional R7-validated inference step.
    """
    if "## 証明\n" not in markdown or "### 結論\n" not in markdown:
        return markdown
    introduction = (
        "EHP 完全列を考える.\n\n"
        r"$\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}"
        r"\xrightarrow{\Delta}\pi_{4}^{2}"
        r"\xrightarrow{E}\pi_{5}^{3}"
        r"\xrightarrow{H}\pi_{5}^{5}"
        r"\xrightarrow{\Delta}\pi_{3}^{2}$."
        "\n\n"
    )
    markdown = markdown.replace("## 証明\n\n", "## 証明\n\n" + introduction, 1)
    conclusion_prefix, conclusion = markdown.split("### 結論\n", 1)
    if "□" not in conclusion:
        return markdown
    conclusion_body, ending = conclusion.rsplit("□", 1)
    addition = (
        r"既知の $\pi_{4}^{2}=\mathbb{Z}/2\{\eta_{2}^{2}\}$ と "
        r"$E(\eta_{2}^{2})=\eta_{3}^{2}$ を用いると, "
        "同型 $E$ は生成元を生成元へ送る.\n\n"
        r"$\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}$."
    )
    return conclusion_prefix + "### 結論\n" + conclusion_body.rstrip() + "\n\n" + addition + "\n\n□" + ending


def _build_phase162_legacy_validated_isomorphism_markdown() -> str:
    """Render only after the exact provenance roots pass R7 validation."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = build_phase58_representative_result()["final_hopf_step"]

    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)

    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        ProofStep(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    leaves = (prop51, hopf_eta5) + exactness
    trusted = {}
    visited = set()

    def collect(step: ProofStep) -> None:
        key = id(step)
        if key in visited:
            return
        visited.add(key)
        if step.rule is ProofRule.GIVEN:
            trusted[key] = step
        for premise in step.premises:
            collect(premise)

    for leaf in leaves:
        collect(leaf)

    validated = reconstruct_phase161_r7_validated_goal(
        phase161_r5_target_goal(), leaves, tuple(trusted.values())
    )
    presentation = build_validated_backward_proof_presentation(validated)
    markdown = render_validated_backward_proof_markdown(presentation)
    return _format_phase162_proof_sentences(
        _compose_phase162_group_conclusion(markdown)
    )


def _build_phase162_existing_group_connection():
    """Build the group-root proof from independently derived existing evidence."""
    phase50 = build_phase50_representative_result()
    phase56 = build_phase56_representative_result()
    pi4_3_steps = phase50["final_group_steps"]
    toda52_steps = phase56["composition_isomorphism_steps"]
    if len(pi4_3_steps) != 1 or len(toda52_steps) != 1:
        raise ValueError("Expected one independently derived source premise of each kind")
    transport = toda_52_pi4_2_finite_cyclic_transport_inference_rule()
    match = find_inference_match(transport, (pi4_3_steps[0], toda52_steps[0]))
    if match is None:
        raise ValueError("Could not derive pi_4^2 from the existing Toda (5.2) evidence")
    source_step = apply_inference_match(match)
    if source_step.rule is not ProofRule.INFERENCE:
        raise ValueError("Source group must be derived")

    pi4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    if source_step.conclusion.lhs != pi4_2 or not isinstance(source_step.conclusion.rhs, FiniteCyclicGroup):
        raise ValueError("Existing source proof does not establish expected cyclic group")
    eta_definitions = tuple(
        ProofStep(
            conclusion=toda_eta_family_definition_statement(index),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for index in (3, 4)
    )
    source_generator = source_step.conclusion.rhs.generator
    bridge_rule = toda_prop53_n3_eta_square_suspension_bridge_inference_rule()
    bridge_match = find_inference_match(bridge_rule, eta_definitions)
    if bridge_match is None:
        raise ValueError("Existing eta-family definitions do not derive the image")
    bridge_step = apply_inference_match(bridge_match)
    from expression import Composition, Suspension
    if (
        not isinstance(bridge_step.conclusion, Relation)
        or bridge_step.conclusion.relation_type is not RelationType.EQUALITY
        or bridge_step.conclusion.lhs != Suspension(expression=source_generator)
        or not isinstance(bridge_step.conclusion.rhs, Composition)
        or bridge_step.conclusion.rhs.left.generator.family != "η"
        or bridge_step.conclusion.rhs.left.generator.index != 3
        or bridge_step.conclusion.rhs.right.generator.family != "η"
        or bridge_step.conclusion.rhs.right.generator.index != 4
    ):
        raise ValueError("Eta-family bridge does not match the source and target generators")
    goal = Relation(
        lhs=pi5_3,
        rhs=FiniteCyclicGroup(
            order=source_step.conclusion.rhs.order,
            generator=bridge_step.conclusion.rhs,
        ),
        relation_type=RelationType.EQUALITY,
    )
    suspension_map = TodaSuspensionMap(source_group=pi4_2, target_group=pi5_3)
    prop51, hopf_eta5, exactness = _phase162_ehp_leaves()
    ehp_leaves = (prop51, hopf_eta5) + exactness
    roots = {}
    seen = set()

    def collect(step: ProofStep) -> None:
        identity = id(step)
        if identity in seen:
            return
        seen.add(identity)
        if step.rule is ProofRule.GIVEN:
            roots[identity] = step
        for premise in step.premises:
            collect(premise)

    for step in (source_step,) + eta_definitions + ehp_leaves:
        collect(step)
    return reconstruct_phase162_r2_from_existing_proofs(
        goal=goal,
        suspension_map=suspension_map,
        source_structure_steps=(source_step,),
        eta_definition_steps=eta_definitions,
        ehp_leaf_steps=ehp_leaves,
        trusted_given_roots=tuple(roots.values()),
    )


def _phase162_ehp_leaves():
    """Reuse the original independent EHP input leaves, not an iso conclusion."""
    prop51 = build_phase55_representative_result()["prop51_steps"][0]
    hopf_eta5 = build_phase58_representative_result()["final_hopf_step"]
    pi_3_2 = TodaPrimaryGroup(group_dimension=3, sphere_dimension=2)
    pi_4_2 = TodaPrimaryGroup(group_dimension=4, sphere_dimension=2)
    pi_5_3 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=3)
    pi_5_5 = TodaPrimaryGroup(group_dimension=5, sphere_dimension=5)
    pi_6_3 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=3)
    pi_6_5 = TodaPrimaryGroup(group_dimension=6, sphere_dimension=5)
    windows = (
        (pi_5_3, pi_5_5, pi_3_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_4_2, pi_5_3, pi_5_5, EHP_E_MAP, EHP_H_MAP),
        (pi_6_3, pi_6_5, pi_4_2, EHP_H_MAP, EHP_DELTA_MAP),
        (pi_6_5, pi_4_2, pi_5_3, EHP_DELTA_MAP, EHP_E_MAP),
    )
    exactness = tuple(
        ProofStep(
            conclusion=TodaProp42ExactnessStatement(
                window=TodaEHPExactnessWindow(
                    source_term=source,
                    middle_term=middle,
                    target_term=target,
                    first_map=first,
                    second_map=second,
                )
            ),
            premises=(),
            rule=ProofRule.GIVEN,
        )
        for source, middle, target, first, second in windows
    )
    return prop51, hopf_eta5, exactness


def build_phase162_web_validated_isomorphism_markdown() -> str:
    """Render the validated group-root proof into the existing lower Web panel.

    The historical public function name is kept for Web compatibility, although
    the proved root is now a group-structure equality, not map isomorphism.
    Existing reference text is retained for R3-3 reference attribution audit.
    """
    connection = _build_phase162_existing_group_connection()
    legacy_reference_source = _build_phase162_legacy_validated_isomorphism_markdown()
    rendered = render_phase162_r3_narrative(
        connection, existing_public_markdown=legacy_reference_source
    )
    if rendered.root_step is not connection.reconstruction.final_step:
        raise ValueError("Web proof root differs from the derived group goal")
    return rendered.markdown
