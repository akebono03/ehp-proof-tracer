"""Phase 174 R61: audit the three renderer-local citation selection routes.

This phase is read only. An attributed source is never certified merely by a
rendered [R#] string. Only verified proof-tree steps and model-owned citation
numbers are eligible. This audit is not a sentence-by-sentence correctness proof.
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


PACKAGE = "phase174_r3_r7_r61_reference_attribution_route_audit"
REVIEWED_REMOTE_BASE = "17b96a63c1ee400d587c14c785c4c1e697334206"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_37c_reference_projection.py": "3800dc72a2e09808f15b8ee78ae76d4d39c2eede",
    "phase174_r3_r7_r56_cyclic_generator_bridge/audit.py": "868e4dfad4d97bb3e5d5da462260bab3759d4af8",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
}
ROUTES = (
    "cited_general_ancestor_numbers",
    "direct_given_premise_citation_numbers",
    "single_source_ancestor_numbers",
)


def git_blob_sha(data: bytes) -> str:
    """Git blob hash for exact source content."""
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Pin code and related audits; permit only whole-file CRLF/LF variants.

    The repository HEAD is recorded, not equality-gated. A new commit that
    touches none of these six pinned files must not invalidate the audit.
    """
    checked = []
    for relative, expected in PINS.items():
        raw = (root / relative).read_bytes()
        lf = raw.replace(b"\r\n", b"\n")
        if expected not in (
            git_blob_sha(raw), git_blob_sha(lf),
            git_blob_sha(lf.replace(b"\n", b"\r\n")),
        ):
            raise RuntimeError("R61_REVIEWED_BLOB_MISMATCH: " + relative)
        checked.append(relative)
    return tuple(checked)


def local_git_head(root: Path) -> str:
    """Report HEAD as lineage metadata, never weaken the file source guard."""
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("R61_GIT_HEAD_UNAVAILABLE")
    return proc.stdout.strip()


def renderer_route_contract(source: str) -> dict[str, object]:
    """Inspect the current renderer AST without reimplementing its decisions."""
    tree = ast.parse(source)
    renderers = tuple(
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == "render_model_backed_narrative_markdown"
    )
    if len(renderers) != 1:
        raise RuntimeError("R61_RENDERER_ENTRY_MISMATCH")
    main = renderers[0]
    nested = {
        node.name: node for node in main.body
        if isinstance(node, ast.FunctionDef)
    }
    for name in ROUTES:
        if name not in nested:
            raise RuntimeError("R61_ATTRIBUTION_ROUTE_MISSING: " + name)
        func = nested[name]
        required_attributes = {"steps", "step_citation_numbers"}
        actual_attributes = {
            item.attr for item in ast.walk(func)
            if isinstance(item, ast.Attribute)
            and isinstance(item.value, ast.Name)
            and item.value.id == "model"
        }
        if not required_attributes.issubset(actual_attributes):
            raise RuntimeError("R61_ROUTE_NO_LONGER_OWNED_BY_MODEL: " + name)
    calls = []
    for node in ast.walk(main):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
                and node.func.id in ROUTES):
            calls.append((node.lineno, node.func.id))
    used = {name for _, name in calls}
    if used != set(ROUTES):
        raise RuntimeError("R61_ATTRIBUTION_ROUTE_UNUSED")
    # A call site is a presentation decision, not permission to add a source.
    return {
        "local_route_count": len(ROUTES),
        "route_definitions": {key: nested[key].lineno for key in ROUTES},
        "route_call_sites": [
            {"line": line, "route": route} for line, route in sorted(calls)
        ],
        "source_of_citation_numbers": "ProofNarrativeModel.step_citation_numbers",
        "fully_centralized": False,
    }


def source_numbers_in_rendered_proof(markdown: str, allowed: tuple[int, ...]) -> tuple[int, ...]:
    """Reject unknown [R#] tags without claiming they cite a specific sentence."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be text")
    # Check the complete markdown: headings and proof body both must be owned.
    numbers = tuple(int(v) for v in re.findall(r"\[R(\d+)\]", markdown))
    invalid = set(numbers).difference(allowed)
    if invalid:
        raise RuntimeError("R61_UNKNOWN_RENDERED_REFERENCE: " + repr(sorted(invalid)))
    return numbers


def given_source_numbers_for_step(model, step_index: int) -> tuple[int, ...]:
    """Collect actual GIVEN ancestors' model citations, not locator labels.

    Missing or value-ambiguous premises fail closed; this routine never changes
    the proof tree or chooses between ambiguous antecedents.
    """
    from proof import ProofRule

    if not 0 <= step_index < len(model.steps):
        raise ValueError("invalid step index")
    steps = model.steps
    by_identity = {id(step): index for index, step in enumerate(steps)}
    pending = [step_index]
    visited = set()
    numbers: set[int] = set()
    while pending:
        index = pending.pop()
        if index in visited:
            continue
        visited.add(index)
        step = steps[index]
        if step.rule is ProofRule.GIVEN:
            numbers.update(model.step_citation_numbers[index])
        for premise in step.premises:
            match = by_identity.get(id(premise))
            if match is None:
                candidates = [i for i, other in enumerate(steps) if other == premise]
                if len(candidates) != 1:
                    raise RuntimeError("R61_MISSING_OR_AMBIGUOUS_PREMISE")
                match = candidates[0]
            pending.append(match)
    return tuple(sorted(numbers))


def inspect_verified_group(result, model, markdown: str) -> dict[str, object]:
    """Classify eligible ancestry; do not equate eligibility with display use."""
    from proof import ProofRule
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase168_r3_3_proof_narrative_model import root_ancestor_step_indices
    from phase174_r3_r7_r60_reference_ownership_audit.audit import (
        audit_narrative_ownership,
    )
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement

    ownership = audit_narrative_ownership(result, model, markdown)
    if result.status is not ProofSearchStatus.COMPLETE or model.root_index is None:
        raise RuntimeError("R61_REQUIRES_COMPLETE_VERIFIED_ROOT")
    root_scope = root_ancestor_step_indices(model.steps, model.root_index)
    allowed = tuple(citation.number for citation in model.citations)
    displayed = source_numbers_in_rendered_proof(markdown, allowed)
    classifications = {"unique_source_ancestor_candidates": 0,
                       "multiple_source_ancestor_candidates": 0,
                       "direct_given_single_premise_candidates": 0,
                       "typed_general_source_ancestor_candidates": 0,
                       "noncited_ancestor_candidates": 0}
    typed_general = (
        TodaProp42GeneralExactnessStatement,
        TodaEtaFamilyGeneralDefinition,
        TodaProp44UniversalStatement,
    )
    for index in sorted(root_scope):
        step = model.steps[index]
        if step.rule is not ProofRule.INFERENCE:
            continue
        sources = given_source_numbers_for_step(model, index)
        if len(sources) == 1:
            classifications["unique_source_ancestor_candidates"] += 1
        elif len(sources) > 1:
            classifications["multiple_source_ancestor_candidates"] += 1
        else:
            classifications["noncited_ancestor_candidates"] += 1
        if len(step.premises) == 1 and step.premises[0].rule is ProofRule.GIVEN:
            classifications["direct_given_single_premise_candidates"] += 1
        if any(
            any(candidate.rule is ProofRule.GIVEN
                and isinstance(candidate.conclusion, typed_general)
                and candidate is ancestor
                for candidate in model.steps)
            for ancestor in step.premises
        ):
            classifications["typed_general_source_ancestor_candidates"] += 1
    return {
        "reference_count": ownership["reference_count"],
        "root_ancestor_count": ownership["root_ancestor_count"],
        "rendered_reference_mentions": len(displayed),
        "model_owned_tags_only": True,
        "provenance_links_validated": True,
        "candidate_classifications": classifications,
        "sentence_level_relevance_fully_proved": False,
    }


def inspect_public() -> dict[str, object]:
    """Use already published proof construction, without adding any proof step."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase174_r3_r7_r56_cyclic_generator_bridge.audit import _search_with_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    bridge = build_shared_typed_bridge()
    groups = {}
    for n, k, label in ((6, 5, "pi11_6"), (7, 5, "pi12_7")):
        result, model = _search_with_model(n, k, bridge)
        markdown = render_model_backed_narrative_markdown(result, model)
        groups[label] = inspect_verified_group(result, model, markdown)
    if groups["pi11_6"]["reference_count"] != 7:
        raise RuntimeError("R61_PI11_REFERENCE_REGRESSION")
    if groups["pi12_7"]["reference_count"] != 3:
        raise RuntimeError("R61_PI12_REFERENCE_REGRESSION")
    return groups


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    reviewed = source_guard(root)
    head = local_git_head(root)
    renderer = (root / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
    structure = renderer_route_contract(renderer)
    print("PHASE174_R61_SOURCE_GUARD=PASS")
    print("PHASE174_R61_SOURCE_PINS=" + str(len(reviewed)))
    print("PHASE174_R61_LOCAL_HEAD=" + head)
    print("PHASE174_R61_RENDERER_LOCAL_ATTRIBUTION_ROUTES=" + str(structure["local_route_count"]))
    print("PHASE174_R61_RENDERER_ROUTE_CALL_SITES=" + str(len(structure["route_call_sites"])))
    print("PHASE174_R61_PRODUCTION_CHANGES=0")
    if options.dry_run:
        print("PHASE174_R61_GATE=PASS_R61_READ_ONLY_DRYRUN")
        print("(END)")
        return 0

    groups = inspect_public()
    report = {
        "reviewed_remote_base": REVIEWED_REMOTE_BASE,
        "local_head": head,
        "pinned_source_files": list(reviewed),
        "renderer": structure,
        "groups": groups,
        "review_result": "PRESENTATION_POLICY_STILL_DISTRIBUTED",
        "next_boundary": "Assess sentence-level relevance before moving any attribution route.",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": 0,
        "full_pytest_run": False,
    }
    target = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
              / "EHPProofTracerAudit" / PACKAGE / "report.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for label, detail in groups.items():
        prefix = "PHASE174_R61_" + label.upper() + "_"
        print(prefix + "REFERENCE_COUNT=" + str(detail["reference_count"]))
        print(prefix + "MODEL_OWNED_TAGS_ONLY=" + str(detail["model_owned_tags_only"]))
        print(prefix + "SENTENCE_LEVEL_RELEVANCE_FULLY_PROVED=False")
    print("PHASE174_R61_RENDERER_CENTRALIZATION=POLICY_REVIEW_REQUIRED")
    print("PHASE174_R61_NEW_GIVEN=0")
    print("PHASE174_R61_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R61_REPORT=" + str(target))
    print("PHASE174_R61_GATE=PASS_R61_ATTRIBUTION_ROUTE_AUDIT_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
