"""R13R8R6 read-only common citation contract audit.

No mathematical inferences, references, or proof steps are added.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import traceback

TARGETS = ((5, 4), (6, 5), (7, 5))
PACKAGE = "phase175_r4r12r13r8r6_binding_contract"
OUTPUT_NAME = "EHP_Phase175_R13R8R6_contract.json"
REQUIRED_FILES = (
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_4_link_bridge.py",
    "phase168_r3_12_body_binding.py",
    "phase168_r3_37c_reference_projection.py",
    "phase168_r3_5_model_renderer.py",
    "web_group_proof.py",
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R13R8R6_GIT_FAILED: " + result.stderr.strip())
    return result.stdout.strip()


def source_guard(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R13R8R6_REPOSITORY_ROOT_MISMATCH")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R13R8R6_EXPECTED_DEVELOP")
    missing = [name for name in REQUIRED_FILES if not (root / name).is_file()]
    if missing:
        raise RuntimeError("R13R8R6_REQUIRED_FILES_MISSING: " + ", ".join(missing))
    code = (root / "phase168_r3_5_model_renderer.py").read_text(encoding="utf-8-sig")
    if "direct_given_premise_citation_numbers" not in code or "matching_direct_given" not in code:
        raise RuntimeError("R13R8R6_RENDERER_CONTRACT_NOT_PRESENT")
    projection = (root / "phase168_r3_37c_reference_projection.py").read_text(encoding="utf-8-sig")
    if "project_reference_bodies" not in projection or "CitedToda511" not in projection:
        raise RuntimeError("R13R8R6_REFERENCE_PROJECTION_NOT_PRESENT")
    return {"head": git(root, "rev-parse", "HEAD"), "branch": "develop", "checked_files": list(REQUIRED_FILES)}


def inspect_binding(model, registry) -> dict[str, object]:
    """Check explicit citation membership; never infer a citation from text."""
    if len(model.step_citation_numbers) != len(model.steps):
        raise RuntimeError("R13R8R6_STEP_MAPPING_LENGTH_INVALID")
    numbers = [entry.number for entry in model.citations]
    if numbers != list(range(1, len(numbers) + 1)):
        raise RuntimeError("R13R8R6_CITATION_NUMBERING_INVALID")
    gaps: list[dict[str, object]] = []
    cite_rows = []
    for citation in model.citations:
        for idx in citation.step_indices:
            if not 0 <= idx < len(model.steps):
                raise RuntimeError("R13R8R6_INVALID_STEP_INDEX")
            if citation.number not in model.step_citation_numbers[idx]:
                raise RuntimeError("R13R8R6_CITATION_STEP_DISAGREEMENT")
        registered_fixed = False
        fixed_statements = []
        for assertion_id in citation.assertion_ids:
            if registry is None:
                raise RuntimeError("R13R8R6_REGISTERED_CITATION_WITHOUT_REGISTRY")
            assertion = registry.assertion(assertion_id)
            if assertion.reference_id not in citation.reference_ids:
                raise RuntimeError("R13R8R6_ASSERTION_REFERENCE_ID_MISMATCH")
            if getattr(assertion.origin, "name", None) == "FIXED_STATEMENT":
                registered_fixed = True
                fixed_statements.append(type(assertion.content).__name__)
        has_body = any(isinstance(body, str) and body.strip() for body in citation.statement_bodies)
        if registered_fixed and not has_body:
            gaps.append({"number": citation.number, "locator": citation.reference.locator,
                         "issue": "REGISTERED_FIXED_BODY_MISSING"})
        direct = []
        for idx, step in enumerate(model.steps):
            if getattr(step.rule, "name", None) != "INFERENCE" or len(step.premises) != 1:
                continue
            parent = step.premises[0]
            if getattr(parent.rule, "name", None) != "GIVEN":
                continue
            matched = [parent_idx for parent_idx in citation.step_indices
                       if model.steps[parent_idx] is parent or model.steps[parent_idx] == parent]
            if matched:
                direct.append({"index": idx, "parent_indices": matched,
                               "child_cited": citation.number in model.step_citation_numbers[idx],
                               "parent_type": type(parent.conclusion).__name__,
                               "child_type": type(step.conclusion).__name__})
        cite_rows.append({
            "number": citation.number, "locator": citation.reference.locator,
            "registered_fixed": registered_fixed, "content_types": fixed_statements,
            "body_count": len(citation.statement_bodies), "has_body": has_body,
            "given_indices": [idx for idx in citation.step_indices
                              if getattr(model.steps[idx].rule, "name", None) == "GIVEN"],
            "direct_consumers": direct,
        })
    for idx, row in enumerate(model.step_citation_numbers):
        for number in row:
            if number not in numbers:
                raise RuntimeError("R13R8R6_STEP_UNKNOWN_CITATION")
            citation = model.citations[number - 1]
            if idx not in citation.step_indices:
                raise RuntimeError("R13R8R6_STEP_CITATION_DISAGREEMENT")
    return {"citations": cite_rows, "registered_fixed_body_gaps": gaps,
            "citation_count": len(model.citations), "step_count": len(model.steps)}


def check_public_lines(lines: tuple[str, ...], *, r3: int, r7: int) -> dict[str, object]:
    """Check reference expressions and body prefixes independently."""
    from re import search
    joined = "\n".join(lines)
    checks = {}
    for tag, number, formula in (
        ("(5.11)", r3, r"\Delta(\eta_9)"),
        ("(5.8)", r7, r"\Delta(\iota_9)"),
    ):
        header = f"[R{number}] {tag}"
        body_prefix = f"[R{number}]より,"
        checks[tag] = {
            "header": header in joined,
            "statement": formula in joined,
            "body_yori": body_prefix in joined,
        }
    checks["pass"] = all(all(v for v in item.values()) for item in checks.values())
    return checks


def inspect_live_target(n: int, k: int) -> dict[str, object]:
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
    from phase165_r52_partial_proof import ProofSearchStatus

    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=n, k=k, bridge=bridge, context_sink=contexts.append)
    if result.status is not ProofSearchStatus.COMPLETE:
        raise RuntimeError(f"R13R8R6_TARGET_NOT_COMPLETE: {n},{k}")
    if not contexts:
        raise RuntimeError("R13R8R6_SEARCH_CONTEXT_MISSING")
    actual = contexts[-1]
    model = build_linked_proof_narrative_model(result, actual)
    inspected = inspect_binding(model, actual.registry)
    narrative = render_model_backed_narrative_markdown(result, model)
    if not isinstance(narrative, str):
        raise RuntimeError("R13R8R6_NARRATIVE_NOT_STRING")
    inspected.update({"target": {"n": n, "k": k}, "search_status": result.status.name,
                      "root_index": model.root_index, "narrative_length": len(narrative)})
    if (n, k) == (5, 4):
        numbers = {citation.reference.locator: citation.number for citation in model.citations}
        if "(5.11)" not in numbers or "(5.8)" not in numbers:
            raise RuntimeError("R13R8R6_TARGET_REFERENCE_MISSING")
        inspected["r3_r7"] = check_public_lines(
            tuple(narrative.splitlines()), r3=numbers["(5.11)"], r7=numbers["(5.8)"],
        )
    return inspected


def run(root: Path, dry_run: bool = False) -> int:
    report: dict[str, object] = {"phase": "175_R4R12R13R8R6", "mode": "READ_ONLY_CONTRACT",
                                 "gate": "FAIL_R13R8R6", "full_pytest": False,
                                 "new_given": 0, "new_mathematical_rules": 0}
    try:
        report["source_guard"] = source_guard(root)
        if dry_run:
            report["gate"] = "PASS_R13R8R6_DRYRUN_SOURCE_GUARD"
        else:
            report["targets"] = [inspect_live_target(n, k) for n, k in TARGETS]
            gaps = [gap for target in report["targets"] for gap in target["registered_fixed_body_gaps"]]
            report["registered_body_gaps"] = gaps
            if gaps:
                raise RuntimeError("R13R8R6_REGISTERED_BODY_GAPS")
            if not report["targets"][0]["r3_r7"]["pass"]:
                raise RuntimeError("R13R8R6_R3_R7_DISPLAY_REGRESSION")
            report["gate"] = "PASS_R13R8R6_COMMON_CITATION_CONTRACT_AUDITED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-5000:]
    output = Path(__import__("os").environ.get("TEMP", "/tmp")) / OUTPUT_NAME
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R13R8R6_GATE=" + str(report["gate"]))
    print("PHASE175_R13R8R6_REPORT=" + str(output))
    if "error" in report:
        print("PHASE175_R13R8R6_ERROR=" + report["error"])
        return 1
    if not dry_run:
        for t in report["targets"]:
            print(f"PHASE175_R13R8R6_TARGET={t['target']['n']}:{t['target']['k']} STEPS={t['step_count']} CITATIONS={t['citation_count']} GAPS={len(t['registered_fixed_body_gaps'])}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
