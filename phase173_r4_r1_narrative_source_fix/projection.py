"""Show the already-proved Toda (5.6) isomorphism without inventing proof facts.

This projector accepts only the canonical seven-step, four-source, completed
pi_7^4 proof. It never registers a new axiom or changes proof search. The
citation numbers come exclusively from the actual ProofNarrativeModel.
"""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import (
    ProofNarrativeModel, root_ancestor_step_indices,
)
from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
from phase173_r4_r1_lemma54_source_bridge.source import (
    TodaLemma54TypedSource, canonical_hopf_relation,
)
from phase173_r4_r1_source_bound_56.rule import _target_generators
from proof import ProofRule, ProofStep

ROOT_RULE = "Toda (5.6) pi_7^4 source-bound direct-sum presentation"


def _step_index(model: ProofNarrativeModel, step: ProofStep) -> int:
    matches = tuple(
        i for i, candidate in enumerate(model.steps)
        if candidate is step
    )
    if len(matches) == 1:
        return matches[0]
    matches = tuple(
        i for i, candidate in enumerate(model.steps)
        if candidate == step
    )
    if len(matches) != 1:
        raise ValueError("A pi_7^4 source step is absent or ambiguous")
    return matches[0]


def _unique_citation(
    model: ProofNarrativeModel, step: ProofStep, locator: str,
) -> int:
    index = _step_index(model, step)
    numbers = model.step_citation_numbers[index]
    if len(numbers) != 1:
        raise ValueError("A pi_7^4 source must have exactly one cited Reference")
    number = numbers[0]
    citations = tuple(c for c in model.citations if c.number == number)
    if len(citations) != 1:
        raise ValueError("A pi_7^4 Reference number is not unique")
    citation = citations[0]
    actual = citation.reference.locator or citation.reference.label
    if actual != locator or index not in citation.step_indices:
        raise ValueError("A pi_7^4 Reference does not identify its actual source")
    return number


def project_verified_pi74_narrative(
    result: PartialProofResult, model: ProofNarrativeModel, markdown: str,
) -> str:
    """Render only the proven pi_7^4 direct sum, with its verified citation IDs.

    No rendered claim is sourced from a DB target or an unproved candidate.
    An unexpected tree or bibliography raises, rather than fabricating a proof.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be a PartialProofResult")
    if not isinstance(model, ProofNarrativeModel):
        raise TypeError("model must be a ProofNarrativeModel")
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")
    if (result.status is not ProofSearchStatus.COMPLETE or result.open_goals
            or model.status is not ProofSearchStatus.COMPLETE
            or model.open_goals or result.conclusion is None
            or _target_generators(result.conclusion) is None
            or model.root_index is None
            or "使用する結果" not in markdown
            or "証明" not in markdown or "□" not in markdown):
        raise ValueError("Only a completed pi_7^4 narrative may be projected")
    root = model.steps[model.root_index]
    if (root.conclusion != result.conclusion or root.rule is not ProofRule.INFERENCE
            or root.inference_rule is None
            or root.inference_rule.name != ROOT_RULE
            or len(root.premises) != 4
            or not root.inference_rule.match_guard(root.premises, {})):
        raise ValueError("The verified Toda (5.6) inference root is missing")
    prop, prior, diagonal, hopf = root.premises
    if (prop.rule is not ProofRule.GIVEN
            or type(prop.conclusion) is not TodaProp44UniversalStatement
            or prop.conclusion != TodaProp44UniversalStatement()
            or prior.rule is not ProofRule.GIVEN
            or diagonal.rule is not ProofRule.INFERENCE
            or len(diagonal.premises) != 1
            or diagonal.premises[0].rule is not ProofRule.GIVEN
            or hopf.rule is not ProofRule.INFERENCE
            or hopf.conclusion != canonical_hopf_relation()
            or len(hopf.premises) != 1
            or hopf.premises[0].rule is not ProofRule.GIVEN
            or type(hopf.premises[0].conclusion) is not TodaLemma54TypedSource
            or hopf.premises[0].conclusion != TodaLemma54TypedSource()):
        raise ValueError("A required cited pi_7^4 source or inference is absent")
    ancestors = root_ancestor_step_indices(model.steps, model.root_index)
    if (len(ancestors) != 7 or len(model.citations) != 4
            or any(_step_index(model, step) not in ancestors for step in (
                prop, prior, diagonal.premises[0], hopf.premises[0],
            ))):
        raise ValueError("The four-source pi_7^4 proof ancestry differs")
    from phase169_r10e4_ordered_db_prior.db_prior import DB_LOCATOR_PREFIX
    from phase172_r5_prior_reference_display.projection import (
        display_prior_reference_locator,
    )
    prop_n = _unique_citation(model, prop, "Proposition 4.4")
    prior_index = _step_index(model, prior)
    prior_numbers = model.step_citation_numbers[prior_index]
    if len(prior_numbers) != 1:
        raise ValueError("Missing cited pi_6^3 prior")
    prior_n = prior_numbers[0]
    prior_citation = next(
        (citation for citation in model.citations if citation.number == prior_n),
        None,
    )
    if (prior_citation is None
            or not (prior_citation.reference.locator or "").startswith(DB_LOCATOR_PREFIX)
            or display_prior_reference_locator(prior_citation, model) is None):
        raise ValueError("The pi_6^3 DB prior is not an authenticated citation")
    diagonal_n = _unique_citation(model, diagonal.premises[0], "(5.1)")
    lemma_n = _unique_citation(model, hopf.premises[0], "Lemma 5.4")
    if len({prop_n, prior_n, diagonal_n, lemma_n}) != 4:
        raise ValueError("Distinct pi_7^4 sources were conflated")
    if set(range(1, 5)) != {prop_n, prior_n, diagonal_n, lemma_n}:
        raise ValueError("The pi_7^4 citation model includes unexpected sources")

    # Source order and numbers are taken from the already-screened proof tree.
    reference_entries = {
        prop_n: (
            f"**[R{prop_n}] Proposition 4.4.**",
            r"$\alpha\in\pi_{2n-1}^{n}$ と "
            r"$H(\alpha)=\pm\iota_{2n-1}$ を仮定する.",
            r"任意の $i$ に対して, "
            r"$\pi_{i-1}^{n-1}\oplus\pi_i^{2n-1}"
            r"\xrightarrow{\ \cong\ }\pi_i^n$ は "
            r"$(\beta,\gamma)\mapsto E\beta+\alpha\circ\gamma$ による同型である.",
            r"特に $E$ は単射である.",
        ),
        prior_n: (
            f"**[R{prior_n}] 先行データベース結果** "
            r"$\pi_{6}^{3}$（sphere.csv, n=3, k=3）"
            "［参考: Proposition 5.6］.",
        ),
        diagonal_n: (
            f"**[R{diagonal_n}] (5.1).**",
            r"$\pi_n^n=\mathbb{Z}\{\iota_n\}\quad(n\ge1)$.",
        ),
        lemma_n: (
            f"**[R{lemma_n}] Lemma 5.4.**",
            r"ある元 $\nu_4\in\pi_7^4$ が存在し, "
            r"$H(\nu_4)=\iota_7$ および "
            r"$2E\nu_4=E^2\nu'$ を満たす.",
        ),
    }
    lines = ["使用する結果", ""]
    for number in range(1, 5):
        lines.extend(reference_entries[number])
        lines.append("")
    lines.extend((
        "証明", "",
        r"$\pi_7^4$ の群構造を決定する.", "",
        f"[R{prior_n}]より, " + r"$\pi_6^3\cong\mathbb{Z}/4\{\nu'\}$.", "",
        f"[R{diagonal_n}]より, " + r"$\pi_7^7\cong\mathbb{Z}\{\iota_7\}$.", "",
        f"[R{lemma_n}]より, " + r"$H(\nu_4)=\iota_7$.", "",
        rf"[R{prop_n}]を $n=4$, $i=7$, $\alpha=\nu_4$ に適用すると, "
        "次の同型を得る.", "",
        r"$\Phi:\pi_6^3\oplus\pi_7^7\xrightarrow{\ \cong\ }\pi_7^4,"
        r"\quad(\beta,\gamma)\longmapsto E\beta+\nu_4\circ\gamma$", "",
        "したがって, "
        r"$\pi_7^4\cong\mathbb{Z}\{\nu_4\}\oplus"
        r"\mathbb{Z}/4\{E\nu'\}$.", "",
        "□", "",
    ))
    return "\n".join(lines)
