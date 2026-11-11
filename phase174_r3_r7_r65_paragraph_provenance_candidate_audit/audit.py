"""Phase 174 R65: map R64 unreviewed paragraphs to *candidate* typed ProofSteps.

Read only. Exact text overlap and citation ancestry establish candidate provenance,
not semantic correctness of a complete Japanese proof sentence. Ambiguous or
unmatched sentences remain unreviewed. Neither proof nor renderer is changed.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r65_paragraph_provenance_candidate_audit"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_27_typed_statement_projection.py": "5b7bf647a7f7f427e2790cbe915709f014480d11",
    "phase174_r3_r7_r56_cyclic_generator_bridge/audit.py": "868e4dfad4d97bb3e5d5da462260bab3759d4af8",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
    "phase174_r3_r7_r63_sentence_witness_audit/audit.py": "115b1bccb657035ef5ed002157c9487509190013",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py": "639b2290aeb09ead23367d0ed8a02e8f64ad6d6f",
}


def git_blob_sha(data: bytes) -> str:
    """Compute an exact Git blob identity."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Pin reviewed artifacts, allowing only whole-file CRLF/LF normalization."""
    checked: list[str] = []
    for relative, expected in PINS.items():
        data = (root / relative).read_bytes()
        lf = data.replace(b"\r\n", b"\n")
        candidates = (data, lf, lf.replace(b"\n", b"\r\n"))
        if expected not in {git_blob_sha(candidate) for candidate in candidates}:
            raise RuntimeError("R65_SOURCE_GUARD_FAILED: " + relative)
        checked.append(relative)
    return tuple(checked)


def local_head(root: Path) -> str:
    """Record local HEAD; commit changes outside pinned source do not block R65."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        text=True, capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("R65_GIT_HEAD_UNAVAILABLE")
    return result.stdout.strip()


def matching_projection_candidates(
    paragraph: str, catalog: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    """Find unmodified typed/LaTeX projections literally present in a paragraph.

    A match is not a mathematical attribution certificate. No fuzzy string,
    rule-name, generator-name or numerical group heuristic is permitted.
    """
    if not isinstance(paragraph, str) or not paragraph:
        raise ValueError("paragraph must be nonempty text")
    if not isinstance(catalog, tuple):
        raise TypeError("catalog must be tuple")
    matches: list[dict[str, object]] = []
    seen: set[int] = set()
    for item in catalog:
        if (not isinstance(item, dict)
                or type(item.get("step_index")) is not int
                or not isinstance(item.get("projections"), tuple)):
            raise ValueError("invalid catalog item")
        idx = item["step_index"]
        if idx in seen:
            raise RuntimeError("R65_DUPLICATE_CATALOG_STEP")
        seen.add(idx)
        matching_kinds = []
        for kind, projection in item["projections"]:
            if (kind not in ("typed_sentence", "body_latex")
                    or not isinstance(projection, str) or not projection):
                raise ValueError("invalid catalog projection")
            if projection in paragraph:
                matching_kinds.append(kind)
        if matching_kinds:
            matches.append({"step_index": idx, "matched_by": matching_kinds})
    return tuple(matches)


def classify_candidate(
    tags: tuple[int, ...],
    matches: tuple[dict[str, object], ...],
    ancestry: dict[int, dict[str, tuple[int, ...]]],
) -> str:
    """Conservative triage; a verified sentence must be proved independently."""
    if not isinstance(tags, tuple) or any(type(t) is not int or t <= 0 for t in tags):
        raise ValueError("invalid citation tags")
    if not isinstance(matches, tuple):
        raise TypeError("matches must be tuple")
    if not matches:
        return "NO_LITERAL_TYPED_WITNESS"
    if len(matches) != 1:
        return "AMBIGUOUS_TYPED_WITNESS"
    index = matches[0]["step_index"]
    if index not in ancestry:
        raise RuntimeError("R65_CANDIDATE_ANCESTRY_MISSING")
    if not tags:
        return "UNIQUE_CANDIDATE_UNCITED"
    sources = set(ancestry[index]["given_citations"])
    if set(tags).issubset(sources):
        return "UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE"
    all_ancestors = set(ancestry[index]["all_ancestor_citations"])
    if set(tags).issubset(all_ancestors):
        return "UNIQUE_CANDIDATE_OTHER_ANCESTOR_ELIGIBLE"
    return "UNIQUE_CANDIDATE_TAG_NOT_IN_ANCESTRY"


def projected_step_catalog(result, model) -> tuple[dict[str, object], ...]:
    """Produce text that the existing common projectors really output."""
    from phase168_r3_12_body_binding import build_narrative_body_lines
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices

    if model.root_index is None:
        raise RuntimeError("R65_VERIFIED_ROOT_MISSING")
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    body_lines = {line.step_index: line for line in build_narrative_body_lines(result, model)}
    catalog = []
    for index in sorted(scope):
        step = model.steps[index]
        projections = []
        typed = typed_sentence(step.conclusion, step)
        if isinstance(typed, str) and "$" in typed and len(typed) >= 10:
            projections.append(("typed_sentence", typed.strip()))
        body = body_lines.get(index)
        if body is not None and len(body.statement_latex) >= 8:
            projections.append(("body_latex", "$" + body.statement_latex + "$"))
        if projections:
            catalog.append({"step_index": index, "projections": tuple(projections),
                            "conclusion_type": type(step.conclusion).__name__})
    return tuple(catalog)


def verified_citation_ancestry(model, catalog: tuple[dict[str, object], ...]) -> dict[int, dict[str, tuple[int, ...]]]:
    """Read actual certified ProofStep ancestry, with ambiguous premise rejection."""
    from phase174_r3_r7_r63_sentence_witness_audit.audit import verified_ancestor_indices
    from proof import ProofRule
    result = {}
    for entry in catalog:
        index = entry["step_index"]
        ancestors = verified_ancestor_indices(model, index)
        all_sources = set()
        givens = set()
        for ancestor in ancestors:
            citations = model.step_citation_numbers[ancestor]
            all_sources.update(citations)
            if model.steps[ancestor].rule is ProofRule.GIVEN:
                givens.update(citations)
        result[index] = {
            "all_ancestor_citations": tuple(sorted(all_sources)),
            "given_citations": tuple(sorted(givens)),
        }
    return result


def classify_unreviewed_paragraphs(
    inventory: dict[str, object],
    catalog: tuple[dict[str, object], ...],
    ancestry: dict[int, dict[str, tuple[int, ...]]],
) -> dict[str, object]:
    """Account for EVERY unreviewed paragraph; never silently drop a sentence."""
    lines = inventory["lines"]
    unreviewed = [item for item in lines if item["attribution_review"] == "UNREVIEWED_SENTENCE_RELEVANCE"]
    if len(unreviewed) != inventory["sentence_relevance_not_yet_audited"]:
        raise RuntimeError("R65_R64_UNREVIEWED_COUNT_DRIFT")
    records = []
    counts: dict[str, int] = {}
    for item in unreviewed:
        tags = tuple(item["citation_numbers"])
        candidates = matching_projection_candidates(item["text"], catalog)
        status = classify_candidate(tags, candidates, ancestry)
        counts[status] = counts.get(status, 0) + 1
        records.append({
            "paragraph_number": item["paragraph_number"],
            "text": item["text"],
            "reference_tags": list(tags),
            "r64_priority": item["priority"],
            "candidate_status": status,
            "candidate_steps": [
                {
                    "step_index": match["step_index"],
                    "matching_projections": match["matched_by"],
                    "given_ancestor_references": list(ancestry[match["step_index"]]["given_citations"]),
                    "all_ancestor_references": list(ancestry[match["step_index"]]["all_ancestor_citations"]),
                } for match in candidates
            ],
            "sentence_level_semantic_relevance_proved": False,
        })
    if len(records) != len(unreviewed):
        raise RuntimeError("R65_INCOMPLETE_FRONTIER_ACCOUNTING")
    return {
        "unreviewed_paragraphs": len(records),
        "triage_counts": counts,
        "fully_certified_sentences_added": 0,
        "sentence_level_relevance_fully_proved": False,
        "records": records,
    }


def inspect_public() -> dict[str, object]:
    """Rebuild the published complete trees and attach conservative candidates."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r63_sentence_witness_audit.audit import inspect_group
    from phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit import audited_line_inventory
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r60_reference_ownership_audit.audit import audit_narrative_ownership

    bridge = build_shared_typed_bridge()
    groups = {}
    for n, k, label, total, targeted, remaining, references in (
        (6, 5, "pi11_6", 14, 3, 11, 7),
        (7, 5, "pi12_7", 6, 2, 4, 3),
    ):
        result, model = _search_with_model(n, k, bridge)
        rendered = render_model_backed_narrative_markdown(result, model)
        ownership = audit_narrative_ownership(result, model, rendered)
        if ownership["reference_count"] != references:
            raise RuntimeError("R65_REFERENCE_COUNT_CHANGED: " + label)
        evidence = inspect_group(result, model, rendered, n)
        inventory = audited_line_inventory(
            rendered, tuple(citation.number for citation in model.citations),
            evidence["targeted_lines"],
        )
        if (inventory["total_proof_paragraphs"] != total
                or inventory["r63_targeted_paragraphs"] != targeted
                or inventory["sentence_relevance_not_yet_audited"] != remaining):
            raise RuntimeError("R65_R64_COVERAGE_BASELINE_CHANGED: " + label)
        catalog = projected_step_catalog(result, model)
        ancestry = verified_citation_ancestry(model, catalog)
        classified = classify_unreviewed_paragraphs(inventory, catalog, ancestry)
        if classified["unreviewed_paragraphs"] != remaining:
            raise RuntimeError("R65_INCOMPLETE_GROUP_FRONTIER: " + label)
        classified["total_proof_paragraphs"] = total
        classified["r63_targeted"] = targeted
        classified["reference_count"] = references
        classified["candidate_catalog_steps"] = len(catalog)
        groups[label] = classified
    return groups


def markdown_report(groups: dict[str, object]) -> str:
    """Create a complete, reviewable listing of still-unverified sentences."""
    lines = ["# Phase 174 R65 — 未監査文章と候補証明ステップ", "",
             "この一覧は候補の一致を示すのみであり、数学的な引用妥当性を確定しません。", ""]
    for key, value in groups.items():
        lines.extend([f"## {key}", "", f"未監査段落：{value['unreviewed_paragraphs']}", ""])
        for item in value["records"]:
            steps = ", ".join(str(x["step_index"]) for x in item["candidate_steps"]) or "なし"
            tags = ", ".join(f"[R{tag}]" for tag in item["reference_tags"]) or "なし"
            lines.extend([
                f"### 段落 {item['paragraph_number']}", "",
                item["text"], "",
                f"- 引用：{tags}",
                f"- 候補：{steps}",
                f"- 判定：{item['candidate_status']}",
                "- 数学的な引用妥当性：未認定", "",
            ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    opts = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    checked = source_guard(root)
    head = local_head(root)
    print("PHASE174_R65_SOURCE_GUARD=PASS")
    print("PHASE174_R65_SOURCE_PINS=" + str(len(checked)))
    print("PHASE174_R65_LOCAL_HEAD=" + head)
    print("PHASE174_R65_PRODUCTION_CHANGES=0")
    if opts.dry_run:
        print("PHASE174_R65_GATE=PASS_R65_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    groups = inspect_public()
    target = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE)
    target.mkdir(parents=True, exist_ok=True)
    report = {
        "phase": "174-R3-R7-R65",
        "reviewed_local_head": head,
        "source_pins": list(checked),
        "groups": groups,
        "claim": "Only candidate formula-to-step matching and certified ancestor ownership. No new sentence-level proof certificate.",
        "production_changes": 0,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest_run": False,
    }
    json_path = target / "report.json"
    md_path = target / "frontier.md"
    json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(markdown_report(groups) + "\n", encoding="utf-8")
    for label, result in groups.items():
        prefix = "PHASE174_R65_" + label.upper() + "_"
        print(prefix + "UNREVIEWED_PARAGRAPHS=" + str(result["unreviewed_paragraphs"]))
        print(prefix + "PROJECTION_CANDIDATE_COUNTS=" + repr(result["triage_counts"]))
        print(prefix + "FULL_SENTENCE_ATTRIBUTION_AUDITED=False")
    print("PHASE174_R65_TOTAL_RECORDED_FRONTIER=" + str(sum(group["unreviewed_paragraphs"] for group in groups.values())))
    print("PHASE174_R65_NEW_GIVEN=0")
    print("PHASE174_R65_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R65_REPORT=" + str(json_path))
    print("PHASE174_R65_FRONTIER=" + str(md_path))
    print("PHASE174_R65_GATE=PASS_R65_ALL_UNREVIEWED_PARAGRAPHS_CATALOGUED")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
