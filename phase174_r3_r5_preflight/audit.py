"""Phase 174 R3-R5: read-only audit of finite cyclic extension obligations.

No mathematical claim is proved by inspecting a source or creating a goal.
No repository file, citation, proof engine or renderer is modified.
"""
from __future__ import annotations

import ast
import json
import os
from pathlib import Path
import subprocess
import tempfile
from typing import Any

from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaDeltaZeroStatement


BASE_HEAD = "b5f5208a7e23397834e4a38ad307c660a4f26b59"
REVIEWED_REMOTE_HEAD = "7ad6ae86714251a88f7002981c0aa20fb51e7069"
SOURCE_FILE = "phase165_r52_r9_shared_math.py"
DELTA_HOOK = "options.extend(expand_delta_zero_from_injection(goal))"


def run_git(*arguments: str) -> str:
    process = subprocess.run(
        ("git",) + arguments,
        check=True, capture_output=True, text=True,
        encoding="utf-8", errors="replace",
    )
    return process.stdout.strip()


def check_transcription(root: Path) -> dict[str, Any]:
    """Check the complete original conditions, not a displayed result."""
    chapter4 = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8-sig")
    chapter5 = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    clauses = {
        "toda48_delta_zero_condition": (chapter4, r"\Delta(\iota_{2n-1})=0"),
        "toda48_injective_double_suspension": (chapter4, r"E^{2}:\pit{2n-2}{\,n-1}"),
        "toda48_index_two_quotient": (chapter4, r"\pit{2n}{\,n+1}/E^{2}"),
        "toda55_family_condition": (chapter5, r"n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu'"),
        "toda56_prior_group_statement": (chapter5, r"\pi^{3}_{6}=\gen{\nu'}\cong \mathbb Z_{4}"),
    }
    missing = [name for name, (source, fragment) in clauses.items() if fragment not in source]
    if missing:
        raise ValueError("Source transcription changed: " + ", ".join(missing))
    return {name: True for name in clauses}


def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Compare against the pinned current HEAD or the exact reviewed new provider."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    import subprocess
    from phase174_r3_r6_r2_prop44_lemma54.patch import git_blob, normalize, patch_shared

    original = subprocess.run(
        ("git", "show", "HEAD:" + SOURCE_FILE),
        cwd=root, check=True, capture_output=True,
    ).stdout
    if git_blob(original) != "bf5bc76c842a6fcac65fc88846f96a95917d0624":
        raise ValueError("Unexpected committed R3-R6 source")
    original_text = normalize(original.decode("utf-8-sig"))
    expected = patch_shared(original_text)
    normalized_current = normalize(source.decode("utf-8-sig"))
    if normalized_current not in (original_text, expected):
        raise ValueError("Unreviewed production source modifications")
    state = "COMMITTED" if normalized_current == original_text else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }


def inspect_public_frontier() -> dict[str, Any]:
    """Inspect genuine screened proposals without manufacturing a ProofStep."""
    bridge = build_shared_typed_bridge()
    registered = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(registered) != 1:
        raise ValueError("Exactly one typed public pi_8^5 goal is required")
    goal = registered[0]
    if not (
        isinstance(goal, Relation)
        and goal.relation_type is RelationType.EQUALITY
        and goal.lhs == TodaPrimaryGroup(8, 5)
        and isinstance(goal.rhs, FiniteCyclicGroup)
        and type(goal.rhs.order) is int
        and goal.rhs.order == 8
    ):
        raise ValueError("Unexpected public pi_8^5 goal")
    citing_id = resolve_specialized_goal_citing_id(bridge, goal)
    if citing_id is None:
        raise ValueError("Public citation position for pi_8^5 is missing")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    ))
    provider = shared_expansion_provider(screened, proof_target=goal)
    child = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    delta = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    cited = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if child in cited or delta in cited or goal in cited:
        raise ValueError("A derived goal has appeared as a direct GIVEN")
    root_options = tuple(provider(goal))
    cyclic_options = tuple(provider(child))
    delta_options = tuple(provider(delta))
    delta_count = sum(
        getattr(proposal.rule, "name", "")
        == "EHP injective suspension and Delta-E exactness imply zero Delta"
        for proposal in delta_options
    )
    if delta_count != 1:
        raise ValueError("R3-R4 public Delta-zero option is not unique")
    return {
        "root_goal_type": type(goal).__name__,
        "cyclic_child_type": type(child).__name__,
        "root_proposal_count": len(root_options),
        "cyclic_child_proposal_count": len(cyclic_options),
        "cyclic_child_proposal_rules": [getattr(x.rule, "name", type(x.rule).__name__) for x in cyclic_options],
        "delta_zero_proposal_count": delta_count,
        "proven_named_group": False,
        "new_given": 0,
        "new_proof_steps": 0,
    }


def inspect_head() -> dict[str, Any]:
    branch = run_git("branch", "--show-current")
    local = run_git("rev-parse", "HEAD")
    remote = run_git("ls-remote", "origin", "refs/heads/develop").split()[0]
    if branch != "develop":
        raise ValueError("Expected the develop working branch")
    if local not in (BASE_HEAD, REVIEWED_REMOTE_HEAD):
        raise ValueError("Local HEAD differs from both reviewed R3-R4 baselines")
    if remote != REVIEWED_REMOTE_HEAD:
        raise ValueError("Remote HEAD changed: re-audit before any implementation")
    return {
        "branch": branch,
        "local_head": local,
        "remote_head": remote,
        "same_head": local == remote,
        "requires_worktree_reconciliation_before_implementation": local != remote,
    }


def make_report(root: Path) -> dict[str, Any]:
    return {
        "phase": "174-R3-R5-PREFLIGHT",
        "mode": "READ_ONLY_FINITE_CYCLIC_EXTENSION",
        "head": inspect_head(),
        "transcription": check_transcription(root),
        "provider": inspect_source_provider(root),
        "frontier": inspect_public_frontier(),
        "implementation_obligations": [
            "Cite Toda (4.8) as a general conditional theorem, not as a concluded group result",
            "Infer index-two quotient and E^2 injectivity from the proved Delta-zero condition",
            "Reconstruct the n>=5 Toda (5.5) doubled generator relation from a cited source",
            "Reuse pi_6^3 = Z/4{nu-prime} only through admitted earlier proof ancestry",
            "Use a group-independent finite cyclic extension rule with typed map compatibility",
        ],
        "production_files_modified": [],
        "new_given": 0,
        "new_proof_steps": 0,
        "whole_pytest_performed": False,
        "r3_r5_proof_implemented": False,
    }


def main() -> int:
    report = make_report(Path.cwd())
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = folder / "EHPProofTracerAudit" / "phase174_r3_r5_preflight"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "audit.json"
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R5_REVIEWED_REMOTE_HEAD=" + report["head"]["remote_head"])
    print("PHASE174_R3R5_LOCAL_HEAD=" + report["head"]["local_head"])
    print("PHASE174_R3R5_HEADS_MATCH=" + str(report["head"]["same_head"]))
    print("PHASE174_R3R5_R3R4_STATE=" + report["provider"]["state"])
    print("PHASE174_R3R5_SOURCE_CLAUSES=5_PASS")
    print("PHASE174_R3R5_ROOT_PROPOSALS=" + str(report["frontier"]["root_proposal_count"]))
    print("PHASE174_R3R5_CYCLIC_PROPOSALS=" + str(report["frontier"]["cyclic_child_proposal_count"]))
    print("PHASE174_R3R5_PUBLIC_DELTA_PROPOSALS=" + str(report["frontier"]["delta_zero_proposal_count"]))
    print("PHASE174_R3R5_NEW_GIVEN=0")
    print("PHASE174_R3R5_PRODUCTION_MODIFIED=False")
    print("PHASE174_R3R5_PREFLIGHT_GATE=PASS")
    print("PHASE174_R3R5_REPORT=" + str(path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
