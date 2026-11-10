"""R60: read-only audit of citations projected from verified proof trees.

No new literature GIVEN, inference rule, group-specific narrative, or database
admission is introduced. The report explicitly distinguishes citation-link
integrity from the still-distributed wording of reference attributions.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r60_reference_ownership_audit"
REVIEWED_HEAD = "17b96a63c1ee400d587c14c785c4c1e697334206"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_37c_reference_projection.py": "3800dc72a2e09808f15b8ee78ae76d4d39c2eede",
    "phase174_r3_r7_r56_cyclic_generator_bridge/audit.py": "868e4dfad4d97bb3e5d5da462260bab3759d4af8",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
}


def git_blob_sha(data: bytes) -> str:
    """Compute Git's SHA-1 for an unmodified file's bytes."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Pin all reviewed production and prior audit dependencies, CRLF tolerant."""
    reviewed = []
    for relative, sha in PINS.items():
        data = (root / relative).read_bytes()
        lf = data.replace(b"\r\n", b"\n")
        if sha not in (
            git_blob_sha(data), git_blob_sha(lf),
            git_blob_sha(lf.replace(b"\n", b"\r\n")),
        ):
            raise RuntimeError("R60_SOURCE_GUARD_FAILED: " + relative)
        reviewed.append(relative)
    return tuple(reviewed)


def local_head(root: Path) -> str:
    """Read the local commit without modifying Git metadata or working files."""
    process = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if process.returncode != 0:
        raise RuntimeError("R60 cannot inspect local Git HEAD")
    return process.stdout.strip()


def reference_heading_numbers(markdown: str) -> tuple[int, ...]:
    """Read Reference headings only; ignore [R#] mentions inside prose."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a string")
    return tuple(int(item) for item in re.findall(r"(?m)^\*\*\[R(\d+)\]", markdown))


def renderer_attribution_paths(root: Path) -> tuple[str, ...]:
    """Record surviving local attribution paths; do not rewrite the Renderer."""
    path = root / "phase168_r3_5_model_renderer.py"
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    required = (
        "cited_general_ancestor_numbers",
        "direct_given_premise_citation_numbers",
        "single_source_ancestor_numbers",
    )
    if not all(name in names for name in required):
        raise RuntimeError("R60 attribution paths changed; re-audit the renderer")
    return required


def audit_narrative_ownership(result, model, markdown: str) -> dict[str, object]:
    """Check actual ProofStep-to-citation bidirectional ownership, not labels.

    This is an audit of model integrity, not a claim that every sentence's
    selected source has a unique or philosophically complete explanation.
    """
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase168_r3_12_body_binding import build_narrative_body_lines

    if result.status is not ProofSearchStatus.COMPLETE:
        raise RuntimeError("R60 audited group is not complete")
    if model.root_index is None:
        raise RuntimeError("R60 complete result has no root")
    in_root = root_ancestor_step_indices(model.steps, model.root_index)
    numbers = tuple(c.number for c in model.citations)
    expected = tuple(range(1, len(numbers) + 1))
    if not numbers or numbers != expected:
        raise RuntimeError("R60 citation numbers are not contiguous and ordered")
    if reference_heading_numbers(markdown) != expected:
        raise RuntimeError("R60 reference headings disagree with the verified model")
    if len(model.steps) != len(model.step_citation_numbers):
        raise RuntimeError("R60 step/citation arrays differ")
    if len({id(s) for s in model.steps}) != len(model.steps):
        raise RuntimeError("R60 duplicated ProofStep identities")
    all_links = 0
    for citation in model.citations:
        if not citation.step_indices:
            raise RuntimeError("R60 orphaned citation")
        if len(set(citation.step_indices)) != len(citation.step_indices):
            raise RuntimeError("R60 citation duplicate step indices")
        for index in citation.step_indices:
            if index not in in_root or citation.number not in model.step_citation_numbers[index]:
                raise RuntimeError("R60 citation is outside root or lacks owning step")
            all_links += 1
    for index, step_numbers in enumerate(model.step_citation_numbers):
        if index not in in_root and step_numbers:
            raise RuntimeError("R60 unrelated search step has attached source")
        if len(set(step_numbers)) != len(step_numbers):
            raise RuntimeError("R60 repeated citation on a step")
        for number in step_numbers:
            if number not in expected or index not in model.citations[number - 1].step_indices:
                raise RuntimeError("R60 step cites an unrelated or nonexistent reference")
    body_lines = build_narrative_body_lines(result, model)
    for line in body_lines:
        if line.citation_numbers != model.step_citation_numbers[line.step_index]:
            raise RuntimeError("R60 body-line reference drift")
    # This checks the known source count and tree ownership, not literal text
    # equality of all source-formula paragraphs or provenance interpretation.
    return {
        "status": "COMPLETE",
        "step_count": len(model.steps),
        "root_ancestor_count": len(in_root),
        "reference_count": len(model.citations),
        "citation_link_count": all_links,
        "validated_body_line_count": len(body_lines),
        "reference_heading_count": len(reference_heading_numbers(markdown)),
        "no_unowned_reference": True,
        "bidirectional_step_links": True,
        "no_outside_root_citation": True,
    }


def inspect_public(root: Path) -> dict[str, object]:
    """Re-run the two focused existing proof searches and inspect common links."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase174_r3_r7_r57_narrative_source_cleanup.audit import inspect_public as r57_inspect
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    previous = r57_inspect()
    if not (previous["pi11_6_complete"] and previous["pi12_7_complete"]
            and previous["pi11_reference_count"] == 7
            and previous["pi12_reference_count"] == 3
            and previous["pi12_7_prop27_absent"]):
        raise RuntimeError("R60 prior complete-proof checkpoint failed")
    bridge = build_shared_typed_bridge()
    first, model1 = _search_with_model(6, 5, bridge)
    second, model2 = _search_with_model(7, 5, bridge)
    md1 = render_model_backed_narrative_markdown(first, model1)
    md2 = render_model_backed_narrative_markdown(second, model2)
    a = audit_narrative_ownership(first, model1, md1)
    b = audit_narrative_ownership(second, model2, md2)
    if a["reference_count"] != 7 or b["reference_count"] != 3:
        raise RuntimeError("R60 unexpected Reference count change")
    if "[R7]より" not in md1 or "Proposition 2.7" not in md1:
        raise RuntimeError("R60 pi11-6 lost the cited Proposition 2.7 proof")
    if "Proposition 2.7" in md2:
        raise RuntimeError("R60 pi12-7 revived a redundant proposition")
    if "[R1]より" not in md2:
        raise RuntimeError("R60 pi12-7 prior result attribution missing")
    return {"pi11_6": a, "pi12_7": b}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    guarded = source_guard(root)
    head = local_head(root)
    if head != REVIEWED_HEAD:
        raise RuntimeError("R60_REVIEWED_HEAD_MISMATCH: " + head)
    paths = renderer_attribution_paths(root)
    print("PHASE174_R60_SOURCE_GUARD=PASS")
    print("PHASE174_R60_SOURCE_PINS=" + str(len(guarded)))
    print("PHASE174_R60_LOCAL_HEAD=" + head)
    print("PHASE174_R60_RENDERER_LOCAL_ATTRIBUTION_PATHS=" + str(len(paths)))
    if options.dry_run:
        print("PHASE174_R60_PRODUCTION_CHANGES=0")
        print("PHASE174_R60_GATE=PASS_R60_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    inspected = inspect_public(root)
    report = {
        "reviewed_head": REVIEWED_HEAD,
        "checked_source_files": list(guarded),
        "renderer_attribution_paths": list(paths),
        "fully_centralized_renderer_citation_selection": False,
        "pi11_6": inspected["pi11_6"],
        "pi12_7": inspected["pi12_7"],
        "production_changes": 0,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest_run": False,
        "next_boundary": (
            "R60 certifies ownership consistency only. Future refactoring, "
            "if needed, must independently verify sentence-level source relevance."
        ),
    }
    output = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE / "report.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for key in ("pi11_6", "pi12_7"):
        info = inspected[key]
        print("PHASE174_R60_" + key.upper() + "_REFERENCE_COUNT=" + str(info["reference_count"]))
        print("PHASE174_R60_" + key.upper() + "_BIDIRECTIONAL_LINKS=" + str(info["bidirectional_step_links"]))
        print("PHASE174_R60_" + key.upper() + "_NO_ORPHANS=" + str(info["no_unowned_reference"]))
    print("PHASE174_R60_REFERENCE_OWNER_MODEL=VERIFIED")
    print("PHASE174_R60_RENDERER_CENTRALIZATION=PARTIAL_REVIEW_REQUIRED")
    print("PHASE174_R60_NEW_GIVEN=0")
    print("PHASE174_R60_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R60_PRODUCTION_CHANGES=0")
    print("PHASE174_R60_REPORT=" + str(output))
    print("PHASE174_R60_GATE=PASS_R60_TREE_OWNERSHIP_AUDIT_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
