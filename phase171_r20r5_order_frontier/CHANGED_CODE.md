# Phase 171 R20R5 — 追加したソース全文

## 変更対象

既存ファイルは変更しない。追加位置はリポジトリ直下の `phase171_r20r5_order_frontier/`。

## audit.py

```python
"""Read-only frontier inspection for the public nu-prime order-four proof.

A genuine R4-R7 typed ProofStep tree is used solely as an audit oracle.  No
existing completed tree is injected into the public search or into a provider.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
REVIEWED_BLOBS = {
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r9_shared_math.py": "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
    "phase171_r2j_r4_r7_nonzero_nu_order/source.py": "5b95010681f6257dc46a4236c099445281635e53",
    "phase171_r2j_r4_r8_cyclic_structure/source.py": "737ffe8af9b7f4180f73d4d5ef6de3d22592f8d4",
    "phase171_r2j_r4_r9_r9_public_cyclic_structure/source.py": "bd9f28e6ccd93b343bc6124779e1b0fe08f8795b",
}


def git_read(*arguments: str) -> str:
    """Run only explicitly allowed read-only Git queries."""
    if arguments not in {
        ("branch", "--show-current"),
        ("rev-parse", "HEAD"),
        ("status", "--porcelain", "--untracked-files=no"),
    } and not (len(arguments) == 2 and arguments[0] == "hash-object"
              and arguments[1] in REVIEWED_BLOBS):
        raise ValueError("only reviewed read-only Git queries are permitted")
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def preflight() -> dict:
    """Verify the checked implementation by content, not a fixed Git HEAD."""
    branch = git_read("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("develop branch is required")
    head = git_read("rev-parse", "HEAD")
    actual = {}
    for relative, expected in REVIEWED_BLOBS.items():
        if not (ROOT / relative).is_file():
            raise RuntimeError("missing reviewed source: " + relative)
        found = git_read("hash-object", relative)
        actual[relative] = found
        if found != expected:
            raise RuntimeError(
                "reviewed source differs; no audit attempted: "
                + relative + " expected=" + expected + " actual=" + found
            )
    return {"branch": branch, "head": head, "verified_source_blobs": actual}


def analyze_step(name: str, proof: ProofStep, provider) -> dict:
    """Check provider obligations against an actually inferred R4-R7 node.

    Matching a rule name alone is not evidence.  A route must reproduce the
    entire ordered set of subgoals, pass the inference matcher, and recreate
    the original typed conclusion from its real parent ProofSteps.
    """
    if proof.rule is not ProofRule.INFERENCE or proof.inference_rule is None:
        raise RuntimeError("audit oracle has no inferred node: " + name)
    result = {
        "name": name,
        "conclusion_type": type(proof.conclusion).__name__,
        "conclusion": repr(proof.conclusion)[:2000],
        "expected_inference_rule": proof.inference_rule.name,
        "parent_types": [type(item.conclusion).__name__ for item in proof.premises],
        "expected_subgoals": [repr(item.conclusion)[:1600] for item in proof.premises],
        "proposal_count": 0,
        "exact_proposal_count": 0,
        "certified_proposal_count": 0,
        "proposal_rule_names": [],
        "classification": "UNEXAMINED",
    }
    try:
        proposals = provider(proof.conclusion)
        if not isinstance(proposals, tuple):
            raise TypeError("shared expansion provider returned a non-tuple")
        result["proposal_count"] = len(proposals)
        result["proposal_rule_names"] = [
            getattr(option.rule, "name", "<unnamed>")
            for option in proposals[:40]
        ]
        required_goals = tuple(step.conclusion for step in proof.premises)
        for option in proposals:
            if (getattr(option.rule, "name", None) != proof.inference_rule.name
                    or option.subgoals != required_goals):
                continue
            result["exact_proposal_count"] += 1
            matches = find_inference_matches_for_rule(option.rule, proof.premises)
            if any(
                len(match.premises) == len(proof.premises)
                and all(left is right for left, right in zip(match.premises, proof.premises))
                and derive_inference_proof_step(match).conclusion == proof.conclusion
                for match in matches
            ):
                result["certified_proposal_count"] += 1
        result["classification"] = (
            "CERTIFIED_PUBLIC_PROPOSAL_PRESENT"
            if result["certified_proposal_count"] else
            "MISSING_MATCHING_PUBLIC_PROPOSAL"
            if not result["exact_proposal_count"] else
            "PUBLIC_RULE_DOES_NOT_CERTIFY_REAL_PARENTS"
        )
    except Exception as error:
        result["classification"] = "PROVIDER_ERROR"
        result["provider_error"] = type(error).__name__ + ": " + str(error)[:1600]
    return result


def run_audit() -> dict:
    """Compare real source-verified R4-R7 inference ancestry to public routes."""
    state = preflight()
    before = git_read("status", "--porcelain", "--untracked-files=no")
    screened, target, citing_id = _screened_context()
    double_nonzero, order_four, nodes, previous = build_nonzero_nu_order_proof()
    if (
        order_four.rule is not ProofRule.INFERENCE
        or order_four.premises[1] is not double_nonzero
        or previous["nu_prime_order_four_proven"] is not True
        or previous["new_given_added"] != 0
        or any(step.conclusion == target for step in nodes)
    ):
        raise RuntimeError("the independent inferred R4-R7 order tree is invalid")
    if len(double_nonzero.premises) != 2:
        raise RuntimeError("the nonzero double must have exactly two proved parents")
    image_nonzero = double_nonzero.premises[1]
    typed_double = double_nonzero.premises[0]
    cardinality = order_four.premises[0]
    required = (
        ("nu_order_four", order_four),
        ("double_nonzero", double_nonzero),
        ("injected_eta_image_nonzero", image_nonzero),
        ("typed_double_equality", typed_double),
        ("middle_cardinality_four", cardinality),
    )
    provider = shared_expansion_provider(screened, proof_target=target)
    details = [analyze_step(label, step, provider) for label, step in required]
    after = git_read("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked files changed during read-only audit")
    missing = [
        item["name"] for item in details
        if item["classification"] != "CERTIFIED_PUBLIC_PROPOSAL_PRESENT"
    ]
    return {
        "phase": "171-R20R5",
        "mode": "AUDIT_ONLY_PUBLIC_PROPOSAL_FRONTIER",
        "git": state,
        "target": repr(target),
        "citing_assertion_id": citing_id,
        "independent_order_four_root": "INFERRED",
        "independent_inference_count": sum(step.rule is ProofRule.INFERENCE for step in nodes),
        "independent_given_leaves": sum(step.rule is ProofRule.GIVEN for step in nodes),
        "proof_steps_injected_into_public_search": False,
        "new_given_added": 0,
        "steps": details,
        "missing_or_uncertified_public_routes": missing,
        "public_order_route_connected": not any(
            item["name"] == "nu_order_four" for item in details
            if item["classification"] != "CERTIFIED_PUBLIC_PROPOSAL_PRESENT"
        ),
        "tracked_source_unchanged": True,
        "public_complete_asserted": False,
        "web_verified": False,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = preflight()
    print("PHASE171_R20R5_BRANCH=" + state["branch"], flush=True)
    print("PHASE171_R20R5_HEAD=" + state["head"], flush=True)
    print("PHASE171_R20R5_SOURCE_CONTENT_GUARD=PASS", flush=True)
    print("PHASE171_R20R5_SOURCE_CHANGES=0", flush=True)
    if args.dry_run:
        print("PHASE171_R20R5_RESULT=PASS_DRY_RUN", flush=True)
        return
    report = run_audit()
    folder = OUTPUT / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    folder.mkdir(parents=True, exist_ok=False)
    destination = folder / "audit.json"
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R5_INDEPENDENT_ORDER_FOUR=INFERRED", flush=True)
    for item in report["steps"]:
        prefix = "PHASE171_R20R5_" + item["name"].upper()
        print(prefix + "=" + item["classification"], flush=True)
        print(prefix + "_PROPOSALS=" + str(item["proposal_count"]), flush=True)
        print(prefix + "_CERTIFIED=" + str(item["certified_proposal_count"]), flush=True)
        if "provider_error" in item:
            print(prefix + "_ERROR=" + item["provider_error"], flush=True)
    print("PHASE171_R20R5_MISSING_ROUTES=" + ",".join(report["missing_or_uncertified_public_routes"]), flush=True)
    print("PHASE171_R20R5_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R5_PUBLIC_COMPLETE_ASSERTED=False", flush=True)
    print("PHASE171_R20R5_REPORT=" + str(destination), flush=True)
    print("PHASE171_R20R5_RESULT=PASS_AUDIT_ONLY", flush=True)


if __name__ == "__main__":
    main()
```

## run.ps1

```powershell
param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (-not $DryRun -and -not $SkipTests) {
    Write-Host 'PHASE171_R20R5_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_order_four_uses_cardinality_and_nonzero_double' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_nonzero_double_must_have_inferred_equality_and_image' `
        'phase171_r2j_r4_r9_r7_public_cyclic_root/tests/test_audit.py::test_generic_source_anchored_root_is_a_premise_proposal_only'
    if ($LASTEXITCODE -ne 0) { throw 'R20R5 focused pytest failed' }
    Write-Host 'PHASE171_R20R5_FOCUSED_PYTEST=PASS'
}
$arguments = @('-m', 'phase171_r20r5_order_frontier.audit')
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { throw 'R20R5 read-only audit failed' }
git status -sb
```

