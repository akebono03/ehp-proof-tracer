"""Phase 174 R62: read-only proof citation attribution policy review.

Verify the three different *presentation* policies before any refactor.
No ProofStep is created; no source, assertion, inference or renderer is changed.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import json
import os
from pathlib import Path
import subprocess
import tempfile


PACKAGE = "phase174_r3_r7_r62_attribution_policy_boundary_audit"
PINS = {
    "phase168_r3_3_proof_narrative_model.py": "6a298aae5f7cbc8ec1be5b02a931b6b7a72e9d52",
    "phase168_r3_12_body_binding.py": "ad8797c141216e410e81bafae284507f7797c3e4",
    "phase168_r3_5_model_renderer.py": "cb6989871ea4ad3964f714bfc5ada2a5099424a0",
    "phase168_r3_37c_reference_projection.py": "3800dc72a2e09808f15b8ee78ae76d4d39c2eede",
    "phase174_r3_r7_r57_narrative_source_cleanup/audit.py": "7cc7e7ac7f63c4bf28142c1d84c5d8ddd249cc8a",
    "phase174_r3_r7_r61_reference_attribution_route_audit/audit.py": "e399a0307408a779f35b9f08a8795977a23a7b4b",
    "phase174_r3_r7_r61_reference_attribution_route_audit/tests/test_audit.py": "7ae18b44ad0e1cfde66734b82fbdcbf5a29313db",
}
ROUTES = (
    "cited_general_ancestor_numbers",
    "direct_given_premise_citation_numbers",
    "single_source_ancestor_numbers",
)


def git_blob_sha(value: bytes) -> str:
    """Hash exact Git blob bytes."""
    return sha1(b"blob " + str(len(value)).encode("ascii") + b"\x00" + value).hexdigest()


def source_guard(root: Path) -> tuple[str, ...]:
    """Fail closed on reviewed code changes; HEAD changes are not errors."""
    passed = []
    for relative, expected in PINS.items():
        data = (root / relative).read_bytes()
        lf = data.replace(b"\r\n", b"\n")
        if expected not in (
            git_blob_sha(data), git_blob_sha(lf),
            git_blob_sha(lf.replace(b"\n", b"\r\n")),
        ):
            raise RuntimeError("R62_SOURCE_BLOB_MISMATCH: " + relative)
        passed.append(relative)
    return tuple(passed)


def renderer_policy_contract(text: str) -> dict[str, object]:
    """Check three separate route guards by AST without executing them."""
    tree = ast.parse(text)
    renderer = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "render_model_backed_narrative_markdown"
    ]
    if len(renderer) != 1:
        raise RuntimeError("R62_RENDERER_ENTRY_MISMATCH")
    nested = {
        node.name: node for node in renderer[0].body
        if isinstance(node, ast.FunctionDef)
    }
    required = {
        "cited_general_ancestor_numbers": (
            "ancestor.rule is ProofRule.GIVEN",
            "isinstance(ancestor.conclusion, given_type)",
            "model.step_citation_numbers",
        ),
        "direct_given_premise_citation_numbers": (
            "step.rule is not ProofRule.INFERENCE",
            "len(step.premises) != 1",
            "given_step.rule is not ProofRule.GIVEN",
            "is_direct_relation",
            "is_typed_zero",
            "model.step_citation_numbers",
        ),
        "single_source_ancestor_numbers": (
            "ancestor.rule is ProofRule.GIVEN",
            "len(sources) == 1",
            "model.step_citation_numbers",
        ),
    }
    for name, required_markers in required.items():
        if name not in nested:
            raise RuntimeError("R62_ROUTE_MISSING: " + name)
        segment = ast.get_source_segment(text, nested[name])
        if segment is None or any(needle not in segment for needle in required_markers):
            raise RuntimeError("R62_ROUTE_SEMANTICS_CHANGED: " + name)
    calls = sorted((item.lineno, item.func.id)
        for item in ast.walk(renderer[0])
        if isinstance(item, ast.Call) and isinstance(item.func, ast.Name)
        and item.func.id in ROUTES)
    if len(calls) != 7 or {name for _, name in calls} != set(ROUTES):
        raise RuntimeError("R62_CALLSITE_CONTRACT_CHANGED")
    return {
        "distinct_policy_routes": len(ROUTES),
        "call_sites": [{"line": line, "route": name} for line, name in calls],
        "typed_general_filter": True,
        "direct_given_and_statement_family_filter": True,
        "unique_only_filter": True,
        "safe_to_replace_with_unconditional_all_ancestors": False,
    }


def validate_number_set(numbers: tuple[int, ...]) -> tuple[int, ...]:
    """Reject unknown shapes or duplicate references in candidate sets."""
    if not isinstance(numbers, tuple):
        raise TypeError("citation set must be a tuple")
    if any(type(number) is not int or number < 1 for number in numbers):
        raise ValueError("invalid citation number")
    if len(numbers) != len(set(numbers)):
        raise ValueError("duplicate citation in candidate set")
    return numbers


def hypothetical_route_choices(
    all_ancestors: tuple[int, ...],
    typed_general: tuple[int, ...],
    direct_given: tuple[int, ...],
) -> dict[str, tuple[int, ...]]:
    """Illustrate distinct *eligibility* policies; not a live renderer API.

    Inputs are already certified candidate numbers. This routine does not
    compute source ancestry, choose a reference for a sentence, or prove one.
    """
    all_ancestors = validate_number_set(all_ancestors)
    typed_general = validate_number_set(typed_general)
    direct_given = validate_number_set(direct_given)
    if not set(typed_general).issubset(all_ancestors):
        raise ValueError("typed citation is not a known ancestor")
    if not set(direct_given).issubset(all_ancestors):
        raise ValueError("direct citation is not a known ancestor")
    return {
        "typed_general": typed_general,
        "direct_given": direct_given,
        "unique_ancestor": all_ancestors if len(all_ancestors) == 1 else (),
    }


def counterexample_contract() -> dict[str, object]:
    """Show why collapsing all three routes changes citation behavior."""
    two_sources = hypothetical_route_choices((1, 2), (2,), ())
    direct_source = hypothetical_route_choices((1, 2), (), (1,))
    one_source = hypothetical_route_choices((3,), (3,), ())
    if two_sources != {
        "typed_general": (2,), "direct_given": (), "unique_ancestor": (),
    } or direct_source["direct_given"] != (1,) or one_source["unique_ancestor"] != (3,):
        raise RuntimeError("R62_POLICY_COUNTEREXAMPLE_FAILED")
    return {
        "typed_general_can_select_from_multiple_ancestors": True,
        "direct_given_does_not_cite_other_ancestors": True,
        "unique_ancestor_suppresses_ambiguous_attribution": True,
        "unconditional_cite_all_equivalent": False,
        "counterexamples_are_fixture_logic_only": True,
    }


def local_git_head(root: Path) -> str:
    """Report lineage without making a new commit block reviewed files."""
    proc = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root,
        capture_output=True, text=True, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError("R62_GIT_HEAD_UNAVAILABLE")
    return proc.stdout.strip()


def inspect_public_models() -> dict[str, object]:
    """Re-run existing certified proofs, not claims about sentence relevance."""
    from phase174_r3_r7_r57_narrative_source_cleanup.audit import inspect_public
    from phase174_r3_r7_r61_reference_attribution_route_audit.audit import (
        inspect_public as r61_inspect_public,
    )

    prior = inspect_public()
    groups = r61_inspect_public()
    if prior["pi11_reference_count"] != 7 or prior["pi12_reference_count"] != 3:
        raise RuntimeError("R62_REFERENCE_COUNT_REGRESSION")
    report = {}
    for key, expected in (("pi11_6", 7), ("pi12_7", 3)):
        item = groups[key]
        if (item["reference_count"] != expected
                or item["model_owned_tags_only"] is not True
                or item["sentence_level_relevance_fully_proved"] is not False):
            raise RuntimeError("R62_PROOF_OWNERSHIP_REGRESSION: " + key)
        counts = item["candidate_classifications"]
        if any(type(count) is not int or count < 0 for count in counts.values()):
            raise RuntimeError("R62_INVALID_CANDIDATE_CENSUS: " + key)
        report[key] = {
            "references": expected,
            "model_owned_tags_only": True,
            "candidate_classifications": counts,
            "sentence_level_relevance_fully_proved": False,
        }
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    pinned = source_guard(root)
    head = local_git_head(root)
    renderer = (root / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
    policies = renderer_policy_contract(renderer)
    examples = counterexample_contract()
    print("PHASE174_R62_SOURCE_GUARD=PASS")
    print("PHASE174_R62_SOURCE_PINS=" + str(len(pinned)))
    print("PHASE174_R62_LOCAL_HEAD=" + head)
    print("PHASE174_R62_DISTINCT_ROUTES=" + str(policies["distinct_policy_routes"]))
    print("PHASE174_R62_CALL_SITES=" + str(len(policies["call_sites"])))
    print("PHASE174_R62_CITE_ALL_IS_NOT_EQUIVALENT=True")
    print("PHASE174_R62_PRODUCTION_CHANGES=0")
    if args.dry_run:
        print("PHASE174_R62_GATE=PASS_R62_POLICY_PREFLIGHT_ONLY")
        print("(END)")
        return 0
    groups = inspect_public_models()
    report = {
        "local_head": head,
        "source_pins": list(pinned),
        "renderer_policies": policies,
        "counterexamples": examples,
        "groups": groups,
        "decision": "RETAIN_DISTINCT_SEMANTIC_POLICIES",
        "reason": "Typed-general, direct-GIVEN and unique-ancestor rules are not equivalent. A later shared traversal helper must preserve these selections and prove each displayed sentence's witness.",
        "sentence_level_relevance_fully_proved": False,
        "production_changes": 0,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": False,
    }
    destination = (Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
                   / "EHPProofTracerAudit" / PACKAGE / "report.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for key, value in groups.items():
        print("PHASE174_R62_" + key.upper() + "_REFERENCES=" + str(value["references"]))
        print("PHASE174_R62_" + key.upper() + "_MODEL_OWNED_TAGS_ONLY=True")
        print("PHASE174_R62_" + key.upper() + "_SENTENCE_LEVEL_RELEVANCE_FULLY_PROVED=False")
    print("PHASE174_R62_DECISION=RETAIN_DISTINCT_SEMANTIC_POLICIES")
    print("PHASE174_R62_NEW_GIVEN=0")
    print("PHASE174_R62_NEW_MATHEMATICAL_RULES=0")
    print("PHASE174_R62_REPORT=" + str(destination))
    print("PHASE174_R62_GATE=PASS_R62_REFERENCE_POLICY_BOUNDARY_AUDIT_ONLY")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
