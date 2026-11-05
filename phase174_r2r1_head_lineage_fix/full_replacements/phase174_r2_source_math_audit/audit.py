"""Phase 174 R2: read-only source and typed-goal frontier audit.

This does not create GIVEN steps, register inference rules, certify an abstract
group, or promote a named generator conclusion.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any


REVIEWED_HEAD = "3558d713fd7939ded656f2458aacc62d71c7e0b3"
R1_BASELINE_HEAD = "cb85913905b2f7452bda2a2c4428e6fe5a3a793a"
TARGETS = ((5, 3), (4, 8), (4, 9))
SOURCE_SPECS = (
    ("sources/toda/Toda_04_2.tex", "4.8", r"\begin{equation}", r"\end{equation}"),
    ("sources/toda/Toda_05_2.tex", "lem:5.4", r"\begin{lemma}", r"\end{lemma}"),
    ("sources/toda/Toda_05_2.tex", "eq:5.5", r"\begin{equation}", r"\end{equation}"),
    ("sources/toda/Toda_05_2.tex", "eq:5.6", r"\begin{equation}", r"\end{equation}"),
    ("sources/toda/Toda_05_2.tex", "prop:5.6", r"\begin{proposition}", r"\end{proposition}"),
)


def git(*args: str) -> str:
    process = subprocess.run(
        ("git",) + args,
        check=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    return process.stdout.strip()


def extract_labeled_environment(
    source: str, label: str, opener: str, closer: str,
) -> str:
    """Extract a complete source-labeled environment, not adjacent references."""
    marker = r"\label{" + label + "}"
    found = source.find(marker)
    if found < 0 or source.find(marker, found + len(marker)) >= 0:
        raise ValueError("Missing or ambiguous source label: " + label)
    start = source.rfind(opener, 0, found)
    end = source.find(closer, found)
    if start < 0 or end < 0 or source.find(closer, start, found) >= 0:
        raise ValueError("Unbounded source label: " + label)
    return source[start:end + len(closer)]


def source_evidence(root: Path) -> dict[str, object]:
    segments: dict[str, str] = {}
    for relative, label, opener, closer in SOURCE_SPECS:
        raw = (root / relative).read_text(encoding="utf-8-sig")
        segments[label] = extract_labeled_environment(
            raw, label, opener, closer,
        )

    if r"\Delta(\iota_{2n-1})=0" not in segments["4.8"]:
        raise ValueError("Toda (4.8) conditional Delta=0 branch absent")
    if r"\pit{2n}{\,n+1}/E^{2}" not in segments["4.8"]:
        raise ValueError("Toda (4.8) quotient branch absent")
    if r"\pi^{4}_{7}" not in segments["lem:5.4"]:
        raise ValueError("Toda Lemma 5.4 is not the reviewed lemma")
    if r"2E \nu_{4}=E^{2}\nu'" not in segments["lem:5.4"]:
        raise ValueError("Toda Lemma 5.4 double-suspension relation absent")
    if r"2\nu_n=E^{\,n-3}\nu'" not in segments["eq:5.5"]:
        raise ValueError("Toda (5.5) family double relation absent")
    if r"4\nu_{n}=\eta_n^{3}" not in segments["eq:5.5"]:
        raise ValueError("Toda (5.5) eta-cube relation absent")
    if r"\pi^{n}_{n+3}" not in segments["prop:5.6"]:
        raise ValueError("Toda Proposition 5.6 general conclusion absent")

    return {
        "source_labels": tuple(segments.keys()),
        "source_segments": segments,
        "mathematical_obligations": (
            {
                "name": "prior_order_four",
                "source": "Toda Proposition 5.6 prior case n=3",
                "required": "A verified proof of pi_6^3 = Z/4{nu_prime}",
                "verified_by_this_audit": False,
            },
            {
                "name": "delta_iota7_zero",
                "source": "Condition in Toda (4.8), n=4",
                "required": "An independently verified typed proof Delta(iota_7)=0",
                "verified_by_this_audit": False,
            },
            {
                "name": "e2_mono_and_index_two",
                "source": "Conditional branch of Toda (4.8), n=4",
                "required": "Typed injectivity of E^2 and quotient pi_8^5/im(E^2) of order two",
                "verified_by_this_audit": False,
            },
            {
                "name": "nu5_double",
                "source": "Toda Lemma 5.4 and formula (5.5), n=5",
                "required": "Typed equality 2 nu_5 = E^2 nu_prime",
                "verified_by_this_audit": False,
            },
            {
                "name": "finite_cyclic_root",
                "source": "Group-theoretic consequence, not a new GIVEN",
                "required": "From injected Z/4, index two, and 2 nu_5, derive Z/8{nu_5}",
                "verified_by_this_audit": False,
            },
        ),
        "editorial_note": (
            'Toda Proposition 5.6 proof prints "(4.8) と (5.6)?" with a '
            "question mark; it must not be silently interpreted as a "
            "separately verified citation."
        ),
    }


def record_goal(goal: object) -> dict[str, object]:
    return {"type": type(goal).__name__, "repr": repr(goal)}


def audit_prior_record() -> dict[str, object]:
    parent = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    path = parent / "EHPProofTracerAudit" / "phase174_r1" / "audit.json"
    if not path.is_file():
        raise FileNotFoundError("Original R1 audit report absent: " + str(path))
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    if payload.get("local_head") != R1_BASELINE_HEAD:
        raise ValueError("R1 audit report HEAD differs from reviewed source")
    observed: dict[tuple[int, int], dict[str, object]] = {}
    for row in payload["rows"]:
        key = (row["n"], row["k"])
        observed[key] = row
    expected = {(5, 3): (3, False), (4, 8): (3, True), (4, 9): (2, True)}
    for coords, (count, abstract) in expected.items():
        row = observed[coords]
        if row.get("runtime_error") is not None:
            raise ValueError("Prior R1 group failed: " + str(coords))
        result = row["result"]
        if (
            result["status"] != "search_failed"
            or result["open_goal_count"] != count
            or result["proven_step_count"] != 0
            or (result["abstract_certificate"] is not None) != abstract
        ):
            raise ValueError("R1 baseline has changed: " + str(coords))
    return {
        "report_path": str(path),
        "verified_head": payload["local_head"],
        "rows": [
            {
                "n": coords[0],
                "k": coords[1],
                "status": observed[coords]["result"]["status"],
                "open_goal_count": observed[coords]["result"]["open_goal_count"],
                "open_goals": observed[coords]["result"]["open_goals"],
                "abstract_certified": observed[coords]["result"]["abstract_certificate"] is not None,
                "named_complete": False,
            }
            for coords in TARGETS
        ],
    }


def inspect_pi85_root() -> dict[str, object]:
    """Inspect real source-screened proposals; never run a synthetic proof step."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge,
        shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError(
            "Expected exactly one typed pi_8^5 Goal, found " + str(len(goals))
        )
    goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        screened = screen_independent_sources_for_derived_goal(
            bridge, goal=goal,
        )
        screen_mode = "independently_screened_unpositioned"
    else:
        screened = screen_shared_proof_context(
            bridge,
            goal=goal,
            citing_assertion_id=citing_id,
            explicit_publication_target=True,
        )
        screen_mode = "publication_screened"
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion
        for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if any(type(item) is type(goal) and item == goal for item in admitted):
        raise ValueError("Target goal was incorrectly admitted as GIVEN")

    provider = shared_expansion_provider(screened, proof_target=goal)
    proposals = provider(goal)
    result = {
        "typed_goal": record_goal(goal),
        "source_screening": screen_mode,
        "citing_assertion_id": citing_id,
        "screened_given_count": len(admitted),
        "target_direct_given_count": 0,
        "proposal_count": len(proposals),
        "proposals": [],
        "new_proof_steps": 0,
    }
    for proposal in proposals:
        children = []
        for child in proposal.subgoals:
            children.append({
                **record_goal(child),
                "exact_screened_given": any(
                    type(child) is type(item) and child == item
                    for item in admitted
                ),
            })
        result["proposals"].append({
            "rule_name": getattr(proposal.rule, "name", type(proposal.rule).__name__),
            "subgoal_count": len(children),
            "subgoals": children,
        })
    return result


def report_directory() -> Path:
    path = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    path = path / "EHPProofTracerAudit" / "phase174_r2"
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_report(root: Path) -> dict[str, object]:
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R2 requires branch develop")
    if git("rev-parse", "HEAD") != REVIEWED_HEAD:
        raise RuntimeError("R2 local HEAD differs from reviewed GitHub HEAD")

    return {
        "phase": "174-R2",
        "mode": "READ_ONLY_SOURCE_FIRST",
        "head": REVIEWED_HEAD,
        "r1_baseline": audit_prior_record(),
        "source_evidence": source_evidence(root),
        "pi85_root_frontier": inspect_pi85_root(),
        "new_given": 0,
        "new_inference_rules": 0,
        "new_proof_steps": 0,
        "new_completed_named_proofs": 0,
        "full_pytest_performed": False,
    }


def main() -> int:
    report = make_report(Path.cwd())
    out = report_directory() / "audit.json"
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    root = report["pi85_root_frontier"]
    print("PHASE174_R2_REVIEWED_HEAD=" + report["head"])
    print("PHASE174_R2_PRIOR_R1_BASELINE=PASS")
    print("PHASE174_R2_SOURCE_ANCHORS=PASS")
    print("PHASE174_R2_PI85_SOURCE_SCREENING=" + root["source_screening"])
    print("PHASE174_R2_PI85_SCREENED_GIVEN=" + str(root["screened_given_count"]))
    print("PHASE174_R2_PI85_ROOT_PROPOSALS=" + str(root["proposal_count"]))
    for index, item in enumerate(root["proposals"], 1):
        print("PHASE174_R2_PROPOSAL_{0}={1} SUBGOALS={2}".format(
            index, item["rule_name"], item["subgoal_count"],
        ))
    print("PHASE174_R2_NEW_GIVEN=0")
    print("PHASE174_R2_NEW_PROOF_STEPS=0")
    print("PHASE174_R2_REPORT=" + str(out))
    print("PHASE174_R2_AUDIT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
