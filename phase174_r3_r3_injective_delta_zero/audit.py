"""Read-only inspection of real citation-screened EHP premises for Delta(iota7).

An in-memory proof step derived from independently reconstructed premises is
recorded as a local capability only. Public proof search is not modified.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r3_injective_delta_zero.rule import (
    delta_e_injectivity_inputs,
    expand_delta_zero_from_injection,
)

REVIEWED_HEADS = (
    "8687759569d7820e26c53aac6f38aedb8ea04f0b",
    "ae2fdbffc4ce15b4141933dc9e529ff450265be1",
)
R3R2_BASELINE_HEAD = "8687759569d7820e26c53aac6f38aedb8ea04f0b"


def git(*args: str) -> str:
    run = subprocess.run(
        ("git",) + args, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return run.stdout.strip()


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r2" / "audit.json"


def validate_prior_r3r2(previous: object) -> dict[str, object]:
    """Do not promote the original unfinished cyclic goal to a proof."""
    if not isinstance(previous, dict):
        raise ValueError("missing R3-R2 mapping")
    if (
        previous.get("phase") != "174-R3-R2"
        or previous.get("mode") != "READ_ONLY_CYCLIC_EXTENSION_GAP"
        or previous.get("local_head") != R3R2_BASELINE_HEAD
    ):
        raise ValueError("R3-R2 origin does not match the reviewed report")
    if (
        previous.get("cyclic_children_count") != 2
        or previous.get("cyclic_children_no_second_hop") is not True
        or previous.get("cyclic_children_exact_target_match") != [True, True]
        or previous.get("new_given") != 0
        or previous.get("new_proof_steps") != 0
        or previous.get("full_pytest_performed") is not False
    ):
        raise ValueError("R3-R2 frontier has been altered or promoted")
    obligations = previous.get("extension_obligations")
    if not isinstance(obligations, dict) or len(obligations.get("requirements", ())) != 5:
        raise ValueError("R3-R2 extension obligations changed")
    return previous


def validate_source_passage(root: Path) -> dict[str, object]:
    """Review exact source labels, including the Lemma 4.5 injectivity range."""
    text = (root / "sources" / "toda" / "Toda_04_2.tex").read_text(encoding="utf-8-sig")
    anchors = {
        "Lemma 4.5": (r"\begin{lemma}\label{lem:4.5}", r"\end{lemma}"),
        "Proposition 4.4": (r"\begin{proposition}\label{prop:4.4}", r"\end{proposition}"),
        "Equation (4.8)": (r"\begin{equation}\label{4.8}", r"\end{equation}"),
    }
    passages = {}
    for name, (start_marker, end_marker) in anchors.items():
        if text.count(start_marker) != 1:
            raise ValueError("source anchor missing or ambiguous: " + name)
        start = text.index(start_marker)
        end = text.find(end_marker, start)
        if end < 0:
            raise ValueError("unbounded source: " + name)
        passages[name] = text[start:end + len(end_marker)]
    if "$n=2,4,8$" not in passages["Lemma 4.5"] or "単射" not in passages["Lemma 4.5"]:
        raise ValueError("Lemma 4.5 n=4 injectivity scope absent")
    if r"H(\alpha)=\pm\iota_{2n-1}" not in passages["Proposition 4.4"]:
        raise ValueError("Proposition 4.4 conditional premise absent")
    if r"\Delta(\iota_{2n-1})=0" not in passages["Equation (4.8)"]:
        raise ValueError("Toda (4.8) conditional zero branch absent")
    return {
        "labels": tuple(passages),
        "lemma45_n4_applies": True,
        "prop44_hopf_condition_explicit": True,
        "eq48_is_conditional": True,
        "source_segments": passages,
    }


def proof_has_cited_leaf(step: object, conclusion: object) -> bool:
    """Require the exact registered universal premise in the proof ancestry."""
    from proof import ProofRule
    seen: set[int] = set()

    def walk(node: object) -> bool:
        if id(node) in seen:
            return False
        seen.add(id(node))
        if (
            getattr(node, "conclusion", None) == conclusion
            and getattr(node, "rule", None) is ProofRule.GIVEN
        ):
            return True
        return any(walk(child) for child in getattr(node, "premises", ()))

    return walk(step)


def inspect_verified_delta_inputs() -> dict[str, object]:
    """Try both public citation-screened premises without changing providers."""
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        prefer_universal_prop42_derivation,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r3_recursive_search import (
        RegisteredGoalUnresolved,
        reconstruct_registered_goal,
    )
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
    from proof import ProofRule, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from toda_rules import TodaDeltaZeroStatement

    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("pi_8^5 has an unreviewed typed goal count")
    group_goal = goals[0]
    citing_id = resolve_specialized_goal_citing_id(bridge, group_goal)
    if citing_id is None:
        raise ValueError("pi_8^5 goal has no positioned publication source")
    screened = screen_shared_proof_context(
        bridge, goal=group_goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    provider = shared_expansion_provider(screened, proof_target=group_goal)

    delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    requirements = delta_e_injectivity_inputs(delta)
    if requirements is None:
        raise ValueError("reviewed Delta-E map dimensions are inconsistent")
    injection, exactness = requirements
    sources = (TodaProp44UniversalStatement(), TodaProp42GeneralExactnessStatement())
    source_presence = [
        sum(
            link.step is not None
            and link.step.rule is ProofRule.GIVEN
            and type(link.step.conclusion) is type(statement)
            and link.step.conclusion == statement
            for link in screened.proof_links
        )
        for statement in sources
    ]
    proposed = [provider(statement) for statement in requirements]
    results = []
    verified = []
    for index, (statement, options, cited) in enumerate(zip(requirements, proposed, sources)):
        entry = {
            "premise_type": type(statement).__name__,
            "premise_repr": repr(statement),
            "source_count": source_presence[index],
            "proposal_count": len(options),
            "proposal_rules": [getattr(item.rule, "name", None) for item in options],
            "proof_status": "UNRESOLVED",
            "inference_from_source": False,
            "proof_rule_name": None,
        }
        try:
            step = reconstruct_registered_goal(
                statement, screened, citing_id, provider,
                lookup_mode="typed_reference",
            )
        except RegisteredGoalUnresolved as exc:
            entry["failure_class"] = type(exc).__name__
        else:
            entry["proof_rule_name"] = getattr(step.inference_rule, "name", None)
            entry["inference_from_source"] = (
                step.rule is ProofRule.INFERENCE
                and proof_has_cited_leaf(step, cited)
            )
            entry["proof_status"] = (
                "VERIFIED_SOURCE_INFERENCE"
                if entry["inference_from_source"]
                else "INFERENCE_WITH_UNCONFIRMED_SOURCE"
            )
            verified.append(step if entry["inference_from_source"] else None)
        results.append(entry)
        if len(verified) < len(results):
            verified.append(None)

    proposal = expand_delta_zero_from_injection(delta)
    if len(proposal) != 1 or proposal[0].subgoals != requirements:
        raise ValueError("generic delta-zero obligation has changed")
    derived = None
    if all(item is not None for item in verified):
        matches = find_inference_matches_for_rule(proposal[0].rule, tuple(verified))
        if len(matches) != 1:
            raise ValueError("certified premises do not match the generic EHP consequence")
        derived = derive_inference_proof_step(matches[0])
        if derived.rule is not ProofRule.INFERENCE or derived.conclusion != delta:
            raise ValueError("derived inference has an incorrect Delta conclusion")

    return {
        "publication_citing_assertion_id": citing_id,
        "goal_repr": repr(group_goal),
        "delta_goal_repr": repr(delta),
        "exactness_indices": (3, 6, "delta_e"),
        "source_occurrences": {
            "Proposition 4.4": source_presence[0],
            "Proposition 4.2": source_presence[1],
        },
        "premises": results,
        "new_rule_name": proposal[0].rule.name,
        "verified_in_memory_delta_zero": derived is not None,
        "public_expansion_provider_modified": False,
        "public_named_group_completed": False,
        "new_given": 0,
    }


def make_report(root: Path) -> dict[str, object]:
    head = git("rev-parse", "HEAD")
    if git("branch", "--show-current") != "develop" or head not in REVIEWED_HEADS:
        raise RuntimeError("Current local Git HEAD is not among the reviewed develop commits")
    previous_file = prior_report_path()
    if not previous_file.is_file():
        raise FileNotFoundError("R3-R2 audit report missing: " + str(previous_file))
    previous = validate_prior_r3r2(json.loads(previous_file.read_text(encoding="utf-8-sig")))
    return {
        "phase": "174-R3-R3",
        "mode": "ISOLATED_GENERIC_INJECTION_TO_DELTA_ZERO",
        "local_head": head,
        "r3r2_provenance_head": previous["local_head"],
        "source_evidence": validate_source_passage(root),
        "typed_inference_trial": inspect_verified_delta_inputs(),
        "production_code_changed": False,
        "new_public_proof_steps": 0,
        "full_pytest_performed": False,
    }


def main() -> int:
    data = make_report(Path.cwd())
    outdir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    outdir = outdir / "EHPProofTracerAudit" / "phase174_r3_r3"
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "audit.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    trial = data["typed_inference_trial"]
    print("PHASE174_R3R3_HEAD=" + data["local_head"])
    print("PHASE174_R3R3_PRIOR_PROVENANCE=PASS")
    print("PHASE174_R3R3_TODA_SOURCE=PASS")
    for entry in trial["premises"]:
        print("PHASE174_R3R3_PREMISE={0} SOURCE={1} PROPOSALS={2} STATUS={3}".format(
            entry["premise_type"], entry["source_count"],
            entry["proposal_count"], entry["proof_status"],
        ))
    print("PHASE174_R3R3_DELTA_ZERO_DERIVED_IN_MEMORY=" + str(trial["verified_in_memory_delta_zero"]))
    print("PHASE174_R3R3_PUBLIC_SEARCH_UNCHANGED=True")
    print("PHASE174_R3R3_REPORT=" + str(out))
    print("PHASE174_R3R3_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
