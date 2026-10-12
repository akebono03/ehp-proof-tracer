"""Phase 163 R4-R64: read-only proposals to split source spans into references/assertions.

Do not register statements, allocate IDs, or infer mathematical verification.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path


# These are editorial *proposals*, not verified mathematical identifiers.
SUBJECTS = {
    "unit_sphere": ("S^n",),
    "pointed_homotopy_classes": ("[X,Y]",),
    "composition_homotopy_classes": ("beta circ alpha",),
    "iterated_suspension": ("E^n X",),
    "addition_inverse_suspension": ("f+g", "-f"),
    "secondary_composition": ("secondary composition",),
    "reduced_cone": ("CX",),
    "extension": ("extension alpha",),
    "coextension": ("coextension gamma",),
    "stable_homotopy_group": ("G_k", "E^infty"),
    "stable_composition": ("composition on G",),
    "stable_toda_bracket": ("stable Toda bracket",),
    "nu4_generator_notation": ("nu_4",),
    "nu_n_notation": ("nu_n", "nu"),
    "eta_n_cubed_notation": ("eta_n^3", "eta^3"),
    "nu_n_squared_notation": ("nu_n^2", "nu^2"),
}

# A concise source marker for each *suggested* assertion; no mathematical parsing.
MARKERS = {
    "unit_sphere": (r"S^n=",),
    "pointed_homotopy_classes": (r"[X,Y]=",),
    "composition_homotopy_classes": (r"\beta\circ \alpha",),
    "iterated_suspension": (r"\Ex^n X",),
    "addition_inverse_suspension": (r"(f+g)(", r"(-f)("),
    "secondary_composition": (r"\{\alpha,",),
    "reduced_cone": (r"CX=",),
    "extension": (r"\emph{extension}",),
    "coextension": (r"\emph{coextension}",),
    "stable_homotopy_group": (r"G_k\ :=", r"\Ex^\infty:"),
    "stable_composition": (r"\circ:G_k",),
    "stable_toda_bracket": (r"\langle \alpha,\beta,\gamma\rangle",),
    "nu4_generator_notation": (r"\nu_{4}:=",),
    "nu_n_notation": (r"\nu_n:=", r"\nu:=E"),
    "eta_n_cubed_notation": (r"\eta^{3}_{n}:=", r"\eta^{3}:="),
    "nu_n_squared_notation": (r"\nu_n^2:=", r"\nu^2:="),
}


def load_source(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("phase") != "163 R4-R63" or len(data.get("records", [])) != 16:
        raise ValueError("R4-R63 input is not the 16-candidate source-span inventory")
    if data.get("production_registry_modified") is not False:
        raise ValueError("R4-R63 production provenance is not read-only")
    return data


def make_proposals(data: dict) -> dict:
    records = data["records"]
    keys = [item["editorial_key"] for item in records]
    if len(keys) != len(set(keys)) or set(keys) != set(SUBJECTS):
        raise ValueError("Candidate identities are missing, duplicated, or unexpected")
    result = []
    for item in records:
        key = item["editorial_key"]
        if not item.get("excerpt_exactly_contained") or not item.get("source_anchor_in_span"):
            raise ValueError(f"Source span evidence is not verified: {key}")
        if item.get("production_reference_id") is not None or item.get("production_assertion_id") is not None:
            raise ValueError(f"A production ID is unexpectedly present: {key}")
        if item.get("semantic_registration_allowed") is not False:
            raise ValueError(f"Semantic registration boundary was violated: {key}")
        if not item.get("source_file_sha256") or not item.get("source_span_text"):
            raise ValueError(f"Missing source evidence: {key}")
        subjects = SUBJECTS[key]
        markers = MARKERS[key]
        if len(subjects) != len(markers):
            raise ValueError(f"Editorial marker count mismatch: {key}")
        for marker in markers:
            if marker not in item["source_span_text"]:
                raise ValueError(f"Source marker absent: {key}: {marker}")
        assert_count = len(subjects)
        warnings = item["warning_codes"]
        if ("POTENTIAL_MULTIPLE_ASSERTIONS" in warnings) != (assert_count > 1):
            raise ValueError(f"Multiplicity conflicts with R4-R63 warning: {key}")
        assertions = [{
            "editorial_component_key": f"{key}:part:{index}",
            "component_position_proposal": index,
            "editorial_subject_unverified": subject,
            "source_marker": marker,
            "kind_proposal": "DEFINITION",
            "semantic_verification": "NOT_VERIFIED",
            "production_assertion_id": None,
        } for index, (subject, marker) in enumerate(zip(subjects, markers), 1)]
        result.append({
            "editorial_reference_key": f"source-span:{item['source_file']}:{item['proposed_start_line']}:{item['proposed_end_line']}:{key}",
            "editorial_key": key,
            "chapter": item["chapter"],
            "source_file": item["source_file"],
            "source_file_sha256": item["source_file_sha256"],
            "start_line": item["proposed_start_line"],
            "end_line": item["proposed_end_line"],
            "source_text_sha256": hashlib.sha256(item["source_span_text"].encode("utf-8")).hexdigest(),
            "source_span_provisional": True,
            "reference_boundary_status": "EDITORIAL_PROPOSAL_NOT_VERIFIED",
            "assertions": assertions,
            "assertion_count_proposed": assert_count,
            "external_context_review_required": "MATHEMATICAL_CONTEXT_OUTSIDE_SPAN" in warnings,
            "adjacent_notation_review_required": "SHARED_ADJACENT_NOTATION_BLOCK" in warnings,
            "publication_position": None,
            "production_reference_id": None,
            "registration_action": "NONE",
        })
    result.sort(key=lambda x: (x["chapter"], x["start_line"], x["editorial_key"]))
    if sum(x["assertion_count_proposed"] for x in result) != 21:
        raise ValueError("Unexpected proposed assertion count")
    return {
        "phase": "163 R4-R64",
        "mode": "READ_ONLY_REFERENCE_ASSERTION_SPLIT_PROPOSAL",
        "source_candidate_count": 16,
        "reference_proposal_count": len(result),
        "assertion_proposal_count": sum(x["assertion_count_proposed"] for x in result),
        "multi_assertion_reference_count": sum(x["assertion_count_proposed"] > 1 for x in result),
        "external_context_review_count": sum(x["external_context_review_required"] for x in result),
        "shared_adjacent_notation_count": sum(x["adjacent_notation_review_required"] for x in result),
        "mathematical_boundary_verified_count": 0,
        "semantic_registration_allowed_count": 0,
        "publication_position_verified_count": 0,
        "production_registry_modified": False,
        "production_ids_allocated": False,
        "proof_search_connected": False,
        "original_edition_verified": False,
        "pending_other_candidates_count": data["pending_other_candidates_count"],
        "records": result,
    }


def write_reports(result: dict, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "split_proposals.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (output_dir / "split_proposals.csv").open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=["chapter", "editorial_key", "source_file", "start_line", "end_line", "editorial_reference_key", "component_position_proposal", "editorial_subject_unverified", "source_marker", "external_context_review_required"])
        writer.writeheader()
        for ref in result["records"]:
            for assertion in ref["assertions"]:
                writer.writerow({"chapter": ref["chapter"], "editorial_key": ref["editorial_key"], "source_file": ref["source_file"], "start_line": ref["start_line"], "end_line": ref["end_line"], "editorial_reference_key": ref["editorial_reference_key"], "component_position_proposal": assertion["component_position_proposal"], "editorial_subject_unverified": assertion["editorial_subject_unverified"], "source_marker": assertion["source_marker"], "external_context_review_required": ref["external_context_review_required"]})
    lines = ["# Phase 163 R4-R64 Reference / Assertion 分割案", "", "原文に対する編集上の提案であり、正式な登録単位・数学的意味は未確定。", "", "|章|暫定 Reference|出典行|Assertion 候補|注意|", "|---:|---|---|---|---|"]
    for ref in result["records"]:
        review = []
        if ref["external_context_review_required"]:
            review.append("外部文脈の確認が必要")
        if ref["adjacent_notation_review_required"]:
            review.append("隣接記法との境界要確認")
        names = ", ".join(item["editorial_subject_unverified"] for item in ref["assertions"])
        lines.append(f"|{ref['chapter']}|`{ref['editorial_key']}`|{ref['start_line']}–{ref['end_line']}|{names}|{' / '.join(review) or '—'}|")
    lines.extend(["", "掲載順・正式 ID の付与、原本照合、数学的意味の検証、証明利用は行わない。", "全体 pytest は実施しない。", ""])
    (output_dir / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only R4-R64 Reference/Assertion split proposal")
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    arguments = parser.parse_args()
    result = make_proposals(load_source(arguments.source))
    write_reports(result, arguments.output)
    print(json.dumps({key: val for key, val in result.items() if key != "records"}, ensure_ascii=False, indent=2))
    print("R4-R64 read-only split proposal complete. Full pytest not run.")


if __name__ == "__main__":
    main()
