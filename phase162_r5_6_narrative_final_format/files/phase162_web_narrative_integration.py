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


def build_phase162_web_validated_isomorphism_markdown() -> str:
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
