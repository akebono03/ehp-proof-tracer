"""Phase 163 R4-R78: transient registry validation of R77 proof attachments."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)

OWNERS = {
    "prop:1-6": (ReferenceKind.PROPOSITION, "Proposition 1.6"),
    "thm:2.4": (ReferenceKind.THEOREM, "Theorem 2.4"),
    "prop:2.5": (ReferenceKind.PROPOSITION, "Proposition 2.5"),
    "prop:4.2": (ReferenceKind.PROPOSITION, "Proposition 4.2"),
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def create_preview(r77: dict, r75: dict) -> dict:
    if r77.get("phase") != "163 R4-R77" or r77.get("candidate_count") != 11:
        raise ValueError("Expected complete R77 result")
    if r75.get("phase") != "163 R4-R75" or r75.get("focused_boundary_count") != 11:
        raise ValueError("Expected complete R75 proposals")
    proposals = {r["r48_index"]: r for r in r75["focused_proposals"]}
    records = r77["records"]
    if len(records) != 11 or len(proposals) != 11:
        raise ValueError("Expected exactly 11 distinct candidates")
    if len({r["r48_index"] for r in records}) != 11:
        raise ValueError("Duplicate R77 candidate")
    registry = UnifiedStatementRegistry()
    preview = []
    seen_owner = set()
    for record in records:
        index = record["r48_index"]
        proposal = proposals.get(index)
        if proposal is None or proposal["excerpt_sha256"] != hashlib.sha256(proposal["excerpt"].encode("utf-8")).hexdigest():
            raise ValueError(f"Missing or changed R75 proposal for {index}")
        if (proposal["source_line"] != record["source_line"] or
                proposal["source_file"] != record["source_file"]):
            raise ValueError("R75 and R77 source locations differ")
        if not record.get("source_hash_verified"):
            raise ValueError("Source hash not verified")
        if record.get("registration_allowed") or record.get("mathematical_role_verified"):
            raise ValueError("Input must remain unapproved")
        attachment = record["structural_attachment"]
        owner = record["source_owner_label"]
        if attachment == "EXPLICIT_POST_STATEMENT_PARAPHRASE":
            if index != 66 or owner != "prop:1-5":
                raise ValueError("Unexpected paraphrase relation")
            preview.append({"r48_index": index, "source_owner_label": owner,
                            "preview_reference_id": None, "preview_assertion_id": None,
                            "preview_status": "PARAPHRASE_HOLD",
                            "original_excerpt_sha256": proposal["excerpt_sha256"],
                            "reason": "Statement follows Proposition 1.5; no independent assertion staged"})
            continue
        if attachment != "WITHIN_EXPLICIT_PROOF_SEGMENT" or owner not in OWNERS:
            raise ValueError("Unknown proof attachment")
        if record["proof_start_line"] is None or record["source_line"] <= record["proof_start_line"]:
            raise ValueError("Invalid proof ordering")
        kind, locator = OWNERS[owner]
        ref_id = "preview:" + owner
        if owner not in seen_owner:
            registry.add_reference(LiteratureEntry(ref_id, kind, locator,
                                                   source_id=record["source_file"]))
            seen_owner.add(owner)
        assertion_id = f"preview:proof-step:r48-{index}"
        registry.add_assertion(AssertionEntry(
            assertion_id, ref_id, AssertionKind.STATEMENT, proposal["excerpt"],
            origin=AssertionOrigin.PROOF_INTERNAL,
            component_position=None, available_after_position=None,
            scope={"r48_index": index, "source_line": record["source_line"],
                   "review_only": True},
        ))
        preview.append({"r48_index": index, "source_owner_label": owner,
                        "preview_reference_id": ref_id, "preview_assertion_id": assertion_id,
                        "preview_status": "PROOF_INTERNAL_PREVIEW",
                        "original_excerpt_sha256": proposal["excerpt_sha256"],
                        "reason": "Validated as transient proof-internal entry; not fixed literature claim"})
    refs = [{"preview_reference_id": "preview:" + owner,
             "locator": registry.reference("preview:" + owner).locator,
             "assertion_candidate_count": len(registry.assertions_for("preview:" + owner))}
            for owner in sorted(seen_owner)]
    counts = Counter(r["preview_status"] for r in preview)
    if dict(counts) != {"PROOF_INTERNAL_PREVIEW": 10, "PARAPHRASE_HOLD": 1}:
        raise ValueError("Unexpected role distribution")
    return {"phase": "163 R4-R78", "mode": "TRANSIENT_REGISTRY_PROOF_INTERNAL_VALIDATION",
            "source_phase": "163 R4-R77", "candidate_count": 11,
            "preview_reference_count": len(refs), "preview_proof_internal_count": 10,
            "paraphrase_hold_count": 1,
            "preview_fixed_statement_count": 0, "formal_source_boundary_verified_count": 0,
            "mathematical_role_verified_count": 0, "semantic_registration_allowed_count": 0,
            "production_registry_modified": False, "production_ids_allocated": False,
            "proof_search_connected": False, "full_suite_run": False,
            "reference_previews": refs, "records": preview}



def write_reports(result: dict, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    (output / "registry_preview.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# Phase 163 R4-R78：一時 Registry 検証", "",
             "既存 Registry 型を用いたメモリ内の検証のみ。正式登録・ID 採番・数学的認定なし。", "",
             f"- 一時 Reference: {result['preview_reference_count']}",
             f"- Proof-internal の一時 Assertion: {result['preview_proof_internal_count']}",
             f"- 言い換えとして保留: {result['paraphrase_hold_count']}", "",
             "| Reference（仮） | Proof-internal 候補 |", "|---|---:|"]
    for ref in result["reference_previews"]:
        lines.append(f"| {ref['locator']} | {ref['assertion_candidate_count']} |")
    lines += ["", "全て preview: 接頭辞を持つ一時キーであり、正式な Statement ID ではない。", ""]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--r77", type=Path, required=True)
    parser.add_argument("--r75", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = create_preview(load_json(args.r77), load_json(args.r75))
    write_reports(result, args.output)
    print(json.dumps({k: v for k, v in result.items() if k not in ("records", "reference_previews")},
                     ensure_ascii=False, indent=2))
    print("R78 transient registry validation complete. No production modifications.")


if __name__ == "__main__":
    main()
