"""Conditional source-evidence-to-general-theorem bridge for Toda Prop. 2.7.

No source ProofStep is constructed. A caller must supply an independently
certified INFERENCE step; source text and citation metadata are necessary,
not sufficient, evidence of mathematical proof.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from proof import InferenceRule, LiteratureReference, PremisePattern, ProofRule
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    PROP27_REFERENCE,
    Prop27GeneralTheoremPremise,
)

SOURCE_PATH = "sources/toda/Toda_02_2.tex"
SOURCE_START = r"\begin{proposition}\label{prop:2.7}"
SOURCE_END = r"\end{proposition}"
REQUIRED_PARTS = (
    r"$n$ が偶数のとき",
    r"H\!\bigl(\Delta(\iota_{2n+1})\bigr)\ =\ \pm\,2\,\iota_{2n-1}",
)
RULE_NAME = "Toda Proposition 2.7 cited source to general theorem premise"


@dataclass(frozen=True)
class Prop27SourceEvidence:
    source_path: str
    locator: str
    theorem_sha256: str
    only_even_n: bool
    sign_undetermined: bool


def extract_prop27_source(source: str) -> Prop27SourceEvidence:
    """Validate the actual general theorem block, without asserting a proof."""
    normalized = source.replace("\r\n", "\n")
    if normalized.count(SOURCE_START) != 1:
        raise ValueError("Proposition 2.7 start marker missing/ambiguous")
    first = normalized.index(SOURCE_START)
    if normalized.count(SOURCE_END, first) < 1:
        raise ValueError("Proposition 2.7 end marker missing")
    last = normalized.index(SOURCE_END, first) + len(SOURCE_END)
    theorem = normalized[first:last]
    if theorem.count(SOURCE_END) != 1 or any(theorem.count(x) != 1 for x in REQUIRED_PARTS):
        raise ValueError("Proposition 2.7 theorem text ambiguous or changed")
    return Prop27SourceEvidence(
        source_path=SOURCE_PATH,
        locator="Proposition 2.7",
        theorem_sha256=hashlib.sha256(theorem.encode("utf-8")).hexdigest(),
        only_even_n=True,
        sign_undetermined=True,
    )


def audited_prop27_source(root: Path) -> Prop27SourceEvidence:
    return extract_prop27_source((root / SOURCE_PATH).read_text(encoding="utf-8-sig"))


def prop27_source_premise_rule(evidence: Prop27SourceEvidence) -> InferenceRule:
    """Require an independently derived, citation-bearing source evidence step.

    This rule does not establish that an arbitrary input step is trustworthy;
    its independent verification remains a caller/Proof Search obligation.
    """
    if (not isinstance(evidence, Prop27SourceEvidence)
            or evidence.source_path != SOURCE_PATH
            or evidence.locator != "Proposition 2.7"
            or evidence.only_even_n is not True
            or evidence.sign_undetermined is not True
            or len(evidence.theorem_sha256) != 64
            or any(char not in "0123456789abcdef" for char in evidence.theorem_sha256)):
        raise ValueError("Invalid source-evidence contract")

    def guard(premises, bindings):
        if len(premises) != 1:
            return False
        step = premises[0]
        parent_rule = step.inference_rule
        if step.rule is not ProofRule.INFERENCE or step.conclusion != evidence:
            return False
        if not isinstance(parent_rule, InferenceRule):
            return False
        citation = parent_rule.literature_reference
        if not isinstance(citation, LiteratureReference):
            return False
        return (
            citation.locator == PROP27_REFERENCE.locator
            and citation.label == PROP27_REFERENCE.label
            and parent_rule is not rule
            and bool(step.premises)
        )

    rule = InferenceRule(
        name=RULE_NAME,
        description=(
            "A separately certified, cited, source-matching Proposition 2.7 "
            "evidence step permits a general theorem premise. Source text "
            "alone, a citation alone, or an unproved GIVEN is insufficient. "
            "No public source witness is created or registered here."
        ),
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.INFERENCE,
            statement_type=Prop27SourceEvidence,
            statement_pattern=evidence,
        ),),
        conclusion_pattern=Prop27GeneralTheoremPremise(),
        match_guard=guard,
        literature_reference=PROP27_REFERENCE,
    )
    return rule
