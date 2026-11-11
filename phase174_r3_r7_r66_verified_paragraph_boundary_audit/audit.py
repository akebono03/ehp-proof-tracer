"""Phase 174 R66: verify typed citation ancestry and exactness display boundaries.

This read-only audit does not equate a text match with semantic proof of a whole
Japanese sentence. It matches EHP exactness display lines to already certified
exactness windows and checks candidate references against actual GIVEN ancestry.
No new theorem, GIVEN, registry entry, ProofStep, renderer or inference rule.
"""
from __future__ import annotations

import argparse
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r66_verified_paragraph_boundary_audit"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_26_exactness_projection.py": "a62fef3bce2150510e1c487ac6c381227b9a0860",
    "phase168_r3_27_typed_statement_projection.py": "5b7bf647a7f7f427e2790cbe915709f014480d11",
    "phase174_r3_r7_r63_sentence_witness_audit/audit.py": "115b1bccb657035ef5ed002157c9487509190013",
    "phase174_r3_r7_r64_sentence_coverage_frontier_audit/audit.py": "639b2290aeb09ead23367d0ed8a02e8f64ad6d6f",
    "phase174_r3_r7_r65_paragraph_provenance_candidate_audit/audit.py": "4d6bbf1d31ba92178bb17416c6dbfabba8088d00",
    "phase174_r3_r7_r65_paragraph_provenance_candidate_audit/tests/test_audit.py": "ea78c5a1d2a93a23b3928db05fb4c791fdd75ce5",
}
EXPECTED = {
    "pi11_6": {"unreviewed": 11, "NO_LITERAL_TYPED_WITNESS": 1,
               "UNIQUE_CANDIDATE_UNCITED": 6,
               "UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE": 4,
               "references": 7},
    "pi12_7": {"unreviewed": 4, "NO_LITERAL_TYPED_WITNESS": 1,
               "UNIQUE_CANDIDATE_UNCITED": 1,
               "UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE": 2,
               "references": 3},
}


def git_blob_sha(data: bytes) -> str:
    """Return a Git blob identity for a byte sequence."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Reject changed audited code, accepting only whole-file LF/CRLF conversion."""
    checked = []
    for relative, expected in PINS.items():
        original = (root / relative).read_bytes()
        lf = original.replace(b"\r\n", b"\n")
        if b"\r" in lf:
            raise RuntimeError("R66_MIXED_OR_CR_ONLY_EOL: " + relative)
        accepted = (original, lf, lf.replace(b"\n", b"\r\n"))
        if expected not in {git_blob_sha(value) for value in accepted}:
            raise RuntimeError("R66_REVIEWED_BLOB_MISMATCH: " + relative)
        checked.append(relative)
    return tuple(checked)


def local_head(root: Path) -> str:
    """Report Git HEAD without requiring equality with an old audit commit."""
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("R66_GIT_HEAD_UNAVAILABLE")
    return result.stdout.strip()


def certified_exactness_line_index(model) -> dict[str, tuple[int, ...]]:
    """Reconstruct only the renderer's existing EHP chain from typed windows.

    A chain's original ProofSteps must all belong to the certified root tree.
    A line match proves the rendering is derived from those windows, not an
    independent validation of Toda's theorem or all surrounding prose.
    """
    from phase168_r3_26_exactness_projection import project_exactness_chains
    from phase168_r3_27_typed_statement_projection import group_tex
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP

    if model.root_index is None:
        raise RuntimeError("R66_NO_CERTIFIED_ROOT")
    scope = root_ancestor_step_indices(model.steps, model.root_index)
    labels = {EHP_E_MAP: "E", EHP_H_MAP: "H", EHP_DELTA_MAP: r"\Delta"}
    lines: dict[str, tuple[int, ...]] = {}
    for chain in project_exactness_chains(model):
        if not all(index in scope for index in chain.step_indices):
            continue
        source = group_tex(chain.arrows[0][0])
        if source is None:
            raise RuntimeError("R66_UNSUPPORTED_CHAIN_SOURCE")
        expression = source
        previous_group = chain.arrows[0][0]
        for domain, symbol, target in chain.arrows:
            target_tex = group_tex(target)
            if domain != previous_group or symbol not in labels or target_tex is None:
                raise RuntimeError("R66_INVALID_CERTIFIED_CHAIN")
            expression += rf" \xrightarrow{{{labels[symbol]}}} {target_tex}"
            previous_group = target
        line = f"${expression}$."
        if line in lines:
            raise RuntimeError("R66_DUPLICATED_CERTIFIED_CHAIN_LINE")
        lines[line] = tuple(chain.step_indices)
    return lines


def actual_step_detail(model, index: int) -> dict[str, object]:
    """Obtain step role and exact GIVEN ancestry, without label/word search."""
    from phase174_r3_r7_r63_sentence_witness_audit.audit import verified_ancestor_indices
    from proof import ProofRule

    ancestors = verified_ancestor_indices(model, index)
    given = tuple(sorted({number for i in ancestors
                          if model.steps[i].rule is ProofRule.GIVEN
                          for number in model.step_citation_numbers[i]}))
    all_sources = tuple(sorted({number for i in ancestors
                                for number in model.step_citation_numbers[i]}))
    return {
        "step_index": index,
        "step_rule": model.steps[index].rule.name,
        "ancestor_indices": tuple(sorted(ancestors)),
        "given_ancestor_references": given,
        "all_ancestor_references": all_sources,
        "own_references": tuple(model.step_citation_numbers[index]),
    }


def validate_frontier_record(
    record: dict[str, object],
    scope: frozenset[int],
    detail_by_index: dict[int, dict[str, object]],
    chain_lines: dict[str, tuple[int, ...]],
) -> dict[str, object]:
    """Fail closed on false candidate/source ownership; never auto-add tags."""
    status = record.get("candidate_status")
    text = record.get("text")
    tags = record.get("reference_tags")
    candidates = record.get("candidate_steps")
    number = record.get("paragraph_number")
    if (type(number) is not int or number < 1 or not isinstance(text, str)
            or not text or not isinstance(tags, list)
            or any(type(tag) is not int or tag < 1 for tag in tags)
            or not isinstance(candidates, list)):
        raise ValueError("R66_INVALID_FRONTIER_RECORD")

    result = {
        "paragraph_number": number,
        "text": text,
        "reference_tags": tags,
        "r65_candidate_status": status,
        "sentence_level_semantic_relevance_proved": False,
    }
    if status == "NO_LITERAL_TYPED_WITNESS":
        if candidates:
            raise RuntimeError("R66_UNEXPECTED_NONLITERAL_CANDIDATE")
        chain_steps = chain_lines.get(text)
        if chain_steps is not None and (not chain_steps or
                                        any(step not in scope for step in chain_steps)):
            raise RuntimeError("R66_CHAIN_OUTSIDE_CERTIFIED_ROOT")
        result.update({
            "verification_boundary": (
                "CERTIFIED_EXACTNESS_CHAIN_DISPLAY" if chain_steps is not None
                else "NO_LITERAL_STEP_OR_CHAIN_WITNESS"
            ),
            "certified_chain_step_indices": list(chain_steps) if chain_steps is not None else [],
        })
        return result

    if status not in ("UNIQUE_CANDIDATE_UNCITED", "UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE"):
        raise RuntimeError("R66_NEW_UNREVIEWED_CLASSIFICATION: " + repr(status))
    if len(candidates) != 1:
        raise RuntimeError("R66_UNIQUE_CANDIDATE_REQUIRED")
    candidate = candidates[0]
    index = candidate.get("step_index")
    if type(index) is not int or index not in scope or index not in detail_by_index:
        raise RuntimeError("R66_CANDIDATE_OUTSIDE_VERIFIED_ROOT")
    detail = detail_by_index[index]
    if (tuple(candidate.get("given_ancestor_references", ())) != detail["given_ancestor_references"]
            or tuple(candidate.get("all_ancestor_references", ())) != detail["all_ancestor_references"]):
        raise RuntimeError("R66_RECORDED_ANCESTRY_DISAGREES_WITH_PROOF_TREE")
    if status == "UNIQUE_CANDIDATE_UNCITED":
        if tags:
            raise RuntimeError("R66_UNCITED_PARAGRAPH_HAS_REFERENCE_TAG")
        boundary = "UNCITED_TYPED_PROJECTION_WITH_VERIFIED_STEP"
    else:
        if not tags or not set(tags).issubset(detail["given_ancestor_references"]):
            raise RuntimeError("R66_TAG_NOT_OWNED_BY_GIVEN_ANCESTRY")
        boundary = "CITED_TYPED_PROJECTION_WITH_GIVEN_ANCESTRY"
    result.update({
        "verification_boundary": boundary,
        "step_index": index,
        "step_rule": detail["step_rule"],
        "candidate_projections": list(candidate.get("matching_projections", ())),
        "given_ancestor_references": list(detail["given_ancestor_references"]),
        "all_ancestor_references": list(detail["all_ancestor_references"]),
        "ancestor_step_indices": list(detail["ancestor_indices"]),
    })
    return result


def inspect_public() -> dict[str, object]:
    """Re-run the certified published searches and account for all 15 paragraphs."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r63_sentence_witness_audit.audit import inspect_group
    from phase174_r3_r7_r64_sentence_coverage_frontier_audit.audit import audited_line_inventory
    from phase174_r3_r7_r65_paragraph_provenance_candidate_audit.audit import (
        classify_unreviewed_paragraphs, matching_projection_candidates,
        projected_step_catalog, verified_citation_ancestry,
    )
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase174_r3_r7_r60_reference_ownership_audit.audit import audit_narrative_ownership

    bridge = build_shared_typed_bridge()
    groups: dict[str, object] = {}
    for n, k, label in ((6, 5, "pi11_6"), (7, 5, "pi12_7")):
        expected = EXPECTED[label]
        result, model = _search_with_model(n, k, bridge)
        markdown = render_model_backed_narrative_markdown(result, model)
        ownership = audit_narrative_ownership(result, model, markdown)
        if ownership["reference_count"] != expected["references"]:
            raise RuntimeError("R66_REFERENCE_REGRESSION: " + label)
        evidence = inspect_group(result, model, markdown, n)
        inventory = audited_line_inventory(markdown, tuple(c.number for c in model.citations),
                                             evidence["targeted_lines"])
        catalog = projected_step_catalog(result, model)
        ancestry = verified_citation_ancestry(model, catalog)
        classified = classify_unreviewed_paragraphs(inventory, catalog, ancestry)
        if classified["unreviewed_paragraphs"] != expected["unreviewed"]:
            raise RuntimeError("R66_UNREVIEWED_COUNT_CHANGED: " + label)
        for kind in ("NO_LITERAL_TYPED_WITNESS", "UNIQUE_CANDIDATE_UNCITED",
                     "UNIQUE_CANDIDATE_GIVEN_ANCESTOR_ELIGIBLE"):
            if classified["triage_counts"].get(kind, 0) != expected[kind]:
                raise RuntimeError("R66_CANDIDATE_CLASS_CHANGED: " + label + " " + kind)
        if sum(classified["triage_counts"].values()) != expected["unreviewed"]:
            raise RuntimeError("R66_UNEXPECTED_CANDIDATE_CLASS: " + label)
        scope = root_ancestor_step_indices(model.steps, model.root_index)
        details = {item["step_index"]: actual_step_detail(model, item["step_index"])
                   for record in classified["records"] for item in record["candidate_steps"]}
        chain_lines = certified_exactness_line_index(model)
        records = []
        for record in classified["records"]:
            exact_matches = matching_projection_candidates(record["text"], catalog)
            if tuple(item["step_index"] for item in record["candidate_steps"]) != tuple(
                item["step_index"] for item in exact_matches
            ):
                raise RuntimeError("R66_CANDIDATE_PROJECTION_DRIFT")
            records.append(validate_frontier_record(record, scope, details, chain_lines))
        counts: dict[str, int] = {}
        for record in records:
            code = record["verification_boundary"]
            counts[code] = counts.get(code, 0) + 1
        groups[label] = {
            "reference_count": expected["references"],
            "total_proof_paragraphs": inventory["total_proof_paragraphs"],
            "r63_targeted_paragraphs": inventory["r63_targeted_paragraphs"],
            "unreviewed_paragraphs": len(records),
            "r65_candidate_counts": classified["triage_counts"],
            "r66_boundary_counts": counts,
            "records": records,
            "full_sentence_semantic_relevance_proved": False,
        }
    if sum(g["unreviewed_paragraphs"] for g in groups.values()) != 15:
        raise RuntimeError("R66_FRONTIER_NOT_FULLY_ACCOUNTED")
    return groups


def markdown_report(groups: dict[str, object]) -> str:
    """Write full proof paragraph text and structural provenance boundary."""
    parts = ["# Phase 174 R66 — 段落と出典の構造的検証境界", "",
             "この監査は数式投影と証明木の祖先関係を照合します。文章全体の数学的妥当性は未認定です。", ""]
    for name, group in groups.items():
        parts.extend(("## " + name, "", "未監査対象: " + str(group["unreviewed_paragraphs"]), ""))
        for item in group["records"]:
            parts.extend(("### 段落 " + str(item["paragraph_number"]), "",
                          item["text"], "", "判定: " + item["verification_boundary"],
                          "Reference: " + (", ".join("[R" + str(n) + "]" for n in item["reference_tags"]) or "なし"),
                          "数学的な文章全体の妥当性: 未認定", ""))
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    guarded = source_guard(root)
    head = local_head(root)
    print("PHASE174_R66_SOURCE_GUARD=PASS")
    print("PHASE174_R66_SOURCE_PINS=" + str(len(guarded)))
    print("PHASE174_R66_LOCAL_HEAD=" + head)
    print("PHASE174_R66_PRODUCTION_CHANGES=0")
    if args.dry_run:
        print("PHASE174_R66_GATE=PASS_R66_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    groups = inspect_public()
    target = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE)
    target.mkdir(parents=True, exist_ok=True)
    report = {"phase": "174-R66", "source_pins": list(guarded), "local_head": head,
              "groups": groups, "new_given": 0, "new_mathematical_rules": 0,
              "production_changes": 0, "full_pytest": False,
              "sentence_level_semantics_fully_audited": False}
    (target / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (target / "frontier.md").write_text(markdown_report(groups) + "\n", encoding="utf-8")
    for label, group in groups.items():
        prefix = "PHASE174_R66_" + label.upper() + "_"
        print(prefix + "TOTAL_UNREVIEWED=" + str(group["unreviewed_paragraphs"]))
        for kind, count in sorted(group["r66_boundary_counts"].items()):
            print(prefix + kind + "=" + str(count))
        for item in group["records"]:
            preview = item["text"].replace("\n", " ")[:130]
            print(prefix + "PARAGRAPH_" + str(item["paragraph_number"]) + "=" + item["verification_boundary"] + " | " + preview)
        print(prefix + "FULL_SENTENCE_SEMANTICS_AUDITED=False")
    print("PHASE174_R66_NEW_GIVEN=0")
    print("PHASE174_R66_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R66_REPORT=" + str(target / "report.json"))
    print("PHASE174_R66_FRONTIER=" + str(target / "frontier.md"))
    print("PHASE174_R66_GATE=PASS_R66_PARAGRAPH_STRUCTURAL_BOUNDARIES_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
