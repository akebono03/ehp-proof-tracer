"""Pure, read-only formatting checks for R4D Web narratives."""
from __future__ import annotations

import re
from collections import Counter


def split_narrative(markdown: str) -> tuple[str, str]:
    """Split the renderer's reference section from its proof section."""
    header, separator, proof = markdown.partition("\n証明\n")
    if not separator:
        raise ValueError("complete narrative has no proof-section delimiter")
    return header, proof


def citation_usage(markdown: str, citation_numbers: tuple[int, ...]) -> dict:
    """Inspect printed tags without inventing missing citations."""
    header, body = split_narrative(markdown)
    heading_numbers = tuple(int(x) for x in re.findall(r"\*\*\[R(\d+)\]", header))
    body_numbers = tuple(int(x) for x in re.findall(r"\[R(\d+)\]", body))
    known = set(citation_numbers)
    return {
        "model_numbers": list(citation_numbers),
        "reference_heading_numbers": list(heading_numbers),
        "proof_tag_numbers": list(body_numbers),
        "heading_count_matches": Counter(heading_numbers) == Counter(citation_numbers),
        "uncited_in_proof": sorted(known - set(body_numbers)),
        "unknown_in_proof": sorted(set(body_numbers) - known),
        "duplicate_reference_headings": sorted(
            number for number, count in Counter(heading_numbers).items() if count > 1
        ),
    }


def visual_findings(markdown: str, usage: dict) -> list[str]:
    """Return review points; visual concerns do not alter mathematical proof status."""
    header, body = split_narrative(markdown)
    findings = []
    if not usage["heading_count_matches"]:
        findings.append("REFERENCE_HEADING_MISMATCH")
    if usage["uncited_in_proof"]:
        findings.append("REFERENCES_NOT_TAGGED_IN_BODY")
    if usage["unknown_in_proof"]:
        findings.append("UNKNOWN_REFERENCE_TAG_IN_BODY")
    if usage["duplicate_reference_headings"]:
        findings.append("DUPLICATED_REFERENCE_HEADING")
    if body.count("$") % 2 or header.count("$") % 2:
        findings.append("ODD_INLINE_MATH_DELIMITER_COUNT")
    if "未解決 Goal" in body or "部分証明・未完成" in body:
        findings.append("INCOMPLETE_PROOF_LABEL_IN_COMPLETE_NARRATIVE")
    if not body.rstrip().endswith("□"):
        findings.append("NO_FINAL_PROOF_SYMBOL")
    if r"\pi_{6}^{4}" not in markdown:
        findings.append("TARGET_GROUP_TEX_NOT_FOUND")
    if r"\eta_{4}" not in markdown and r"\eta_4" not in markdown:
        findings.append("ETA4_TEX_NOT_FOUND")
    return findings

