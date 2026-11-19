"""Audit actual source-bound citation projection without modifying any proof or renderer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any

PACKAGE = "phase175_r4r12r13r8r5_reference_binding_audit"
TRACKED_ALLOWED = frozenset({
    "phase168_r3_37c_reference_projection.py",
    "phase168_r3_5_model_renderer.py",
})
REQUIRED = (
    "phase168_r3_3_proof_narrative_model.py",
    "phase168_r3_37c_reference_projection.py",
    "phase168_r3_5_model_renderer.py",
    "phase168_r3_12_body_binding.py",
    "phase168_r3_4_link_bridge.py",
    "phase175_r4r12r10r1_cited_511_public/source.py",
    "phase175_r4r10_cited_58_prop25_public/source.py",
)
DEFAULT_TARGETS = ((5, 4), (6, 5), (7, 5))


def git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        errors="replace", capture_output=True, check=False,
    )
    if done.returncode:
        raise RuntimeError("GIT_COMMAND_FAILED: " + done.stderr.strip())
    return done.stdout.strip()


def parse_targets(text: str) -> tuple[tuple[int, int], ...]:
    result = []
    for part in text.split(","):
        hit = re.fullmatch(r"\s*(\d+):(\d+)\s*", part)
        if hit is None:
            raise ValueError("TARGET_FORMAT_INVALID: use n:k,n:k")
        n, k = (int(hit.group(1)), int(hit.group(2)))
        if n < 2 or k < 0 or (n, k) in result:
            raise ValueError("TARGET_RANGE_OR_DUPLICATE")
        result.append((n, k))
    if not result:
        raise ValueError("TARGETS_EMPTY")
    return tuple(result)


def source_guard(root: Path) -> dict[str, Any]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    missing = [path for path in REQUIRED if not (root / path).is_file()]
    if missing:
        raise RuntimeError("REQUIRED_SOURCES_MISSING: " + repr(missing))
    dirty = git(root, "diff", "--name-only").splitlines()
    unexpected = sorted(set(dirty) - TRACKED_ALLOWED)
    if unexpected:
        raise RuntimeError("UNREVIEWED_TRACKED_MODIFICATIONS: " + repr(unexpected))
    return {
        "branch": "develop", "head": git(root, "rev-parse", "HEAD"),
        "tracked_changes": dirty,
        "source_blob_sha": {
            path: git(root, "hash-object", path) for path in REQUIRED
        },
    }


def direct_given_sources(model: object, step_index: int) -> tuple[dict[str, Any], ...]:
    """Use exact parent ProofSteps, not a locator string or statement text search."""
    from proof import ProofRule

    steps = model.steps
    step = steps[step_index]
    if step.rule is not ProofRule.INFERENCE or len(step.premises) != 1:
        return ()
    parent = step.premises[0]
    if parent.rule is not ProofRule.GIVEN:
        return ()
    matches = [i for i, candidate in enumerate(steps)
               if candidate is parent or candidate == parent]
    if len(matches) != 1:
        return ()
    parent_index = matches[0]
    wrapped = getattr(parent.conclusion, "statement", None)
    typed_equal = wrapped is not None and type(wrapped) is type(step.conclusion) and wrapped == step.conclusion
    direct_relation = type(parent.conclusion) is type(step.conclusion)
    numbers = tuple(model.step_citation_numbers[parent_index])
    if not numbers:
        return ()
    return ({
        "parent_index": parent_index,
        "parent_type": type(parent.conclusion).__name__,
        "child_type": type(step.conclusion).__name__,
        "typed_wrapper_equal": typed_equal,
        "direct_type_match": direct_relation,
        "source_numbers": list(numbers),
        "child_numbers": list(model.step_citation_numbers[step_index]),
    },)


def citation_rows(model: object, bridge: object) -> list[dict[str, Any]]:
    """Report all references, including source-only and non-renderable entries."""
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin

    rows = []
    for citation in model.citations:
        assertions = [bridge.registry.assertion(key) for key in citation.assertion_ids]
        fixed = [assertion for assertion in assertions
                 if assertion.origin is AssertionOrigin.FIXED_STATEMENT]
        children = []
        for index, step in enumerate(model.steps):
            for source in direct_given_sources(model, index):
                if citation.number in source["source_numbers"]:
                    children.append({"index": index, **source})
        rows.append({
            "number": citation.number,
            "locator": citation.reference.locator or citation.reference.label,
            "step_indices": list(citation.step_indices),
            "given_indices": [i for i in citation.step_indices
                              if model.steps[i].rule is ProofRule.GIVEN],
            "assertion_ids": list(citation.assertion_ids),
            "reference_ids": list(citation.reference_ids),
            "registered_fixed_statement": bool(fixed),
            "registered_content_types": [type(item.content).__name__ for item in assertions],
            "has_wrapped_statement": [hasattr(item.content, "statement") for item in assertions],
            "statement_body_count": len(citation.statement_bodies),
            "statement_bodies": list(citation.statement_bodies),
            "registered_fixed_body_missing": bool(fixed) and not citation.statement_bodies,
            "direct_given_consumers": children,
        })
    return rows


def inspect_target(n: int, k: int, *, check_web: bool) -> dict[str, Any]:
    """Inspect one actual screened search and its own linked narrative model."""
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
    from phase168_r3_12_body_binding import build_narrative_body_lines
    from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown

    bridge = build_shared_typed_bridge()
    search_contexts = []
    result = search_group_from_registered_goal(
        n=n, k=k, bridge=bridge, context_sink=search_contexts.append,
    )
    if not search_contexts:
        raise RuntimeError("SEARCH_CONTEXT_MISSING")
    model = build_linked_proof_narrative_model(result, search_contexts[-1])
    body_lines = build_narrative_body_lines(result, model)
    markdown = render_model_backed_narrative_markdown(result, model)
    citations = citation_rows(model, search_contexts[-1])
    for citation in citations:
        number = citation["number"]
        citation["narrative_has_heading"] = bool(re.search(
            rf"\[R{number}\]", markdown,
        ))
        citation["narrative_uses_yori"] = f"[R{number}]より" in markdown
        citation["narrative_uses_mochiite"] = f"[R{number}]を用いて" in markdown
    bound_indices = {line.step_index for line in body_lines}
    direct = [
        {"step_index": index,
         "renderable_body": index in bound_indices,
         **source}
        for index in range(len(model.steps))
        for source in direct_given_sources(model, index)
    ]
    report = {
        "target": {"n": n, "k": k},
        "status": result.status.name,
        "complete": result.status.name == "COMPLETE",
        "root_index": model.root_index,
        "proof_step_count": len(model.steps),
        "citation_count": len(citations),
        "citations": citations,
        "direct_given_consumers": direct,
        "registered_body_gaps": [
            {"number": row["number"], "locator": row["locator"]}
            for row in citations if row["registered_fixed_body_missing"]
        ],
        "narrative_text_length": len(markdown),
        "web_checked": check_web,
    }
    if check_web:
        from web_group_proof import build_standard_web_group_proof_view
        view = build_standard_web_group_proof_view(n, k, mode="narrative")
        rendered = "\n".join(
            str(getattr(line, "prefix", "")) + " " +
            str(getattr(line, "statement_latex", "") or "") + " " +
            str(getattr(line, "suffix", ""))
            for line in view.rendered_lines
        )
        expected = ("(5.11)", "(5.8)") if (n, k) == (5, 4) else ()
        verified = {}
        for locator in expected:
            rows = [row for row in citations if row["locator"] == locator]
            if len(rows) != 1:
                raise RuntimeError("EXPECTED_CITATION_NOT_UNIQUE: " + locator)
            row = rows[0]
            tag = f"[R{row['number']}]"
            verified[locator] = {
                "number": row["number"],
                "reference_body_present": bool(row["statement_bodies"]),
                "proof_body_yori": tag + "より" in rendered,
                "direct_typed_consumer": any(
                    consumer["typed_wrapper_equal"]
                    for consumer in row["direct_given_consumers"]
                ),
            }
        report["web"] = {
            "key": view.key,
            "expected_citation_checks": verified,
        }
        if (n, k) == (5, 4):
            # The registered source may use a different, independently verified
            # notation from its derived proof step.  Object identity/equality
            # is diagnostic only, not a condition for citation display.
            # Check the two user-visible guarantees, using the real Web view.
            report["web"]["display_regression"] = (
                view.key != "generic-complete-proof"
                or any(
                    not value["reference_body_present"]
                    or not value["proof_body_yori"]
                    for value in verified.values()
                )
            )
    return report


def run(root: Path, targets: tuple[tuple[int, int], ...], *, dry_run: bool) -> int:
    report: dict[str, Any] = {
        "phase": "175_R4R12R13R8R5",
        "mode": "READ_ONLY_GENERAL_BINDING_AUDIT",
        "dry_run": dry_run,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_files_modified": False,
        "full_pytest_executed": False,
    }
    before = ""
    try:
        before = git(root, "status", "--porcelain")
        report["source_guard"] = source_guard(root)
        if dry_run:
            report["gate"] = "PASS_R13R8R5_SOURCE_GUARD_ONLY"
        else:
            report["targets"] = [
                inspect_target(n, k, check_web=(n, k) == (5, 4))
                for n, k in targets
            ]
            report["registered_body_gaps"] = [
                {"target": t["target"], **gap}
                for t in report["targets"]
                for gap in t["registered_body_gaps"]
            ]
            report["gate"] = "PASS_R13R8R5_GENERAL_BINDING_AUDITED_GAPS_RECORDED"
            regressions = [
                t["target"] for t in report["targets"]
                if t.get("web", {}).get("display_regression", False)
            ]
            if regressions:
                report["gate"] = "FAIL_R13R8R5_ACTUAL_WEB_DISPLAY_REGRESSION"
                report["display_regressions"] = regressions
        if git(root, "status", "--porcelain") != before:
            raise RuntimeError("REPOSITORY_STATUS_CHANGED")
    except Exception as exc:
        report["gate"] = "FAIL_R13R8R5_AUDIT"
        report["error"] = type(exc).__name__ + ": " + str(exc)
    path = Path(tempfile.gettempdir()) / "EHP_Phase175_R13R8R5_general_binding_audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")
    print("PHASE175_R13R8R5_GATE=" + report["gate"])
    print("PHASE175_R13R8R5_REPORT=" + str(path))
    for target in report.get("targets", []):
        n, k = target["target"]["n"], target["target"]["k"]
        print(f"PHASE175_R13R8R5_TARGET={n},{k} STATUS={target['status']} CITATIONS={target['citation_count']}")
        for gap in target["registered_body_gaps"]:
            print(f"PHASE175_R13R8R5_BODY_GAP={n},{k},R{gap['number']} {gap['locator']}")
    if "error" in report:
        print("PHASE175_R13R8R5_ERROR=" + report["error"])
        return 1
    if report["gate"].startswith("FAIL_"):
        print("PHASE175_R13R8R5_DISPLAY_REGRESSIONS=" + repr(report["display_regressions"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--targets", default="5:4,6:5,7:5")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), parse_targets(args.targets), dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
