"""Immutable public narrative baselines for Phase 165 R4."""
from __future__ import annotations

import difflib
import hashlib
import json
from pathlib import Path

from phase165_r52_r4_flask_bridge import build_group_proof_progress_view
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown

BASE = Path(__file__).resolve().parent / "baselines"
CASES = (("pi3_2", 2, 1), ("pi4_3", 3, 1))


def capture(name: str, n: int, k: int) -> dict:
    result = search_group_from_registered_goal(n=n, k=k)
    if result.status is not ProofSearchStatus.COMPLETE:
        raise AssertionError(f"{name} search not complete: {result.status}: {result.diagnostics}")
    markdown = render_partial_proof_markdown(result)
    view = build_group_proof_progress_view(n=n, k=k, max_depth=2)
    if view.key != "generic-complete-proof" or view.mode != "narrative" or view.partial_result:
        raise AssertionError(f"{name} wrong public view contract")
    if len(view.steps) != len(result.proven_steps) or not view.rendered_lines:
        raise AssertionError(f"{name} proof steps or display lines missing")
    lines = [dict(kind=line.kind, prefix=line.prefix, statement_latex=line.statement_latex,
                  suffix=line.suffix, segments=[dict(kind=s.kind, value=s.value) for s in line.segments])
             for line in view.rendered_lines]
    if name == "pi4_3":
        from phase165_r12_r2_quotient_rules import KernelMultipleStatement, QuotientIsomorphismStatement
        types = {type(step.conclusion) for step in result.proven_steps}
        if not {KernelMultipleStatement, QuotientIsomorphismStatement}.issubset(types):
            raise AssertionError("pi4_3 proof tree lacks kernel or quotient")
        ker = markdown.find(r"\ker E")
        quotient = markdown.find(r"\cong")
        if ker < 0 or quotient < 0 or quotient <= ker or "第一同型定理" not in markdown:
            raise AssertionError("pi4_3 narrative lacks ordered kernel and quotient")
        web_text = "\n".join((l["prefix"] + (l["statement_latex"] or "") + l["suffix"]) for l in lines)
        if r"\ker E" not in web_text or r"\cong" not in web_text:
            raise AssertionError("pi4_3 web rendered lines omit kernel or quotient")
    return {"case": name, "n": n, "k": k, "markdown": markdown,
            "markdown_sha256": hashlib.sha256(markdown.encode("utf-8")).hexdigest(),
            "web_rendered_lines": lines}


def baseline_path(name: str) -> Path:
    return BASE / f"{name}.json"


def compare(actual: dict, expected: dict) -> None:
    if actual == expected:
        return
    before = json.dumps(expected, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    after = json.dumps(actual, ensure_ascii=False, indent=2, sort_keys=True).splitlines()
    diff = "\n".join(difflib.unified_diff(before, after, fromfile="baseline", tofile="actual", lineterm=""))
    raise AssertionError(f"{actual['case']} golden baseline mismatch:\n{diff[:12000]}")


def verify_all() -> None:
    for name, n, k in CASES:
        path = baseline_path(name)
        if not path.is_file():
            raise AssertionError(f"missing frozen baseline: {path}; first run capture_baseline.py")
        expected = json.loads(path.read_text(encoding="utf-8"))
        compare(capture(name, n, k), expected)
