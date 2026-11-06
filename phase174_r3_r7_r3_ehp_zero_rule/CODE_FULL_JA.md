# Phase 174 R3-R7-R3 追加コード全文

新規ディレクトリ `phase174_r3_r7_r3_ehp_zero_rule/` のコードを全収録する。既存の本体ファイル・クラス・メソッドに変更はない。

## 追加位置と変更一覧

`rule.py`、`audit.py`、`tests/test_rule.py`、`tests/test_audit.py`、`run.ps1`、`__init__.py` を新規追加する。追加場所はリポジトリ直下の上記ディレクトリ。import 部分と追加したクラス・関数・テスト関数はすべて全文掲載する。

## `__init__.py`

```python
"""Isolated Phase 174 R3-R7-R3 general EHP zero inference package."""
```

## `rule.py`

```python
"""Source-first generic EHP zero-group inference, not yet production-wired.

If A --Delta--> B --E--> C --H--> D is exact at B and C,
Delta is surjective, and D=0, then C=0. Every premise must be
proved independently. This module creates no GIVEN and no proof leaf.
"""
from __future__ import annotations

from homotopy_groups import (
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r3_recursive_search import GoalExpansion
from proof import InferenceRule, PremisePattern, ProofRule
from toda_rules import TodaProp42ExactnessStatement


RULE_NAME = "EHP exact Delta-E-H sequence with surjective Delta and zero H target"


def ehp_zero_inputs(
    goal: object,
) -> tuple[MapSurjective, TodaProp42ExactnessStatement,
           TodaProp42ExactnessStatement, TodaPrimaryGroupZeroStatement] | None:
    """Construct four independently provable premises from a typed target.

    The EHP indices are derived from the group, not enumerated stems or
    database assertions. A below-diagonal or nonconcrete target is rejected.
    """
    if not isinstance(goal, TodaPrimaryGroupZeroStatement):
        return None
    target = goal.group
    if not isinstance(target, TodaPrimaryGroup):
        return None
    i = target.group_dimension
    sphere = target.sphere_dimension
    if (type(i) is not int or type(sphere) is not int or sphere < 2):
        return None
    n = sphere - 1
    if i < sphere:
        return None

    source = TodaPrimaryGroup(i + 1, 2 * n + 1)
    middle = TodaPrimaryGroup(i - 1, n)
    terminal = TodaPrimaryGroup(i, 2 * n + 1)
    first = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=source,
        middle_term=middle,
        target_term=target,
        first_map=EHP_DELTA_MAP,
        second_map=EHP_E_MAP,
    ))
    second = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=middle,
        middle_term=target,
        target_term=terminal,
        first_map=EHP_E_MAP,
        second_map=EHP_H_MAP,
    ))
    if (prop42_exactness_indices(first) != (n, i, "delta_e")
            or prop42_exactness_indices(second) != (n, i, "e_h")):
        return None
    return (
        MapSurjective(TodaDeltaMap(source, middle)),
        first,
        second,
        TodaPrimaryGroupZeroStatement(terminal),
    )


def ehp_zero_from_delta_surjectivity_rule(
    goal: TodaPrimaryGroupZeroStatement,
) -> InferenceRule:
    """Return a generic checked rule; no cited facts or GIVENs are made."""
    required = ehp_zero_inputs(goal)
    if required is None:
        raise ValueError("invalid EHP zero-group goal")

    def guard(premises, bindings):
        return (
            len(premises) == 4
            and all(step.rule is ProofRule.INFERENCE for step in premises)
            and tuple(step.conclusion for step in premises) == required
            and ehp_zero_inputs(goal) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "Exactness gives im(Delta)=ker(E) and im(E)=ker(H). "
            "Surjectivity of Delta makes E the zero map. If the H "
            "codomain is zero, H is zero and E is surjective. Hence "
            "the middle EHP group is zero. All four premises require "
            "separate certified derivations; no target is a GIVEN."
        ),
        premise_patterns=(
            PremisePattern(statement_type=MapSurjective,
                           statement_pattern=required[0],
                           proof_rule=ProofRule.INFERENCE),
            PremisePattern(statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[1],
                           proof_rule=ProofRule.INFERENCE),
            PremisePattern(statement_type=TodaProp42ExactnessStatement,
                           statement_pattern=required[2],
                           proof_rule=ProofRule.INFERENCE),
            PremisePattern(statement_type=TodaPrimaryGroupZeroStatement,
                           statement_pattern=required[3],
                           proof_rule=ProofRule.INFERENCE),
        ),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_ehp_zero_from_delta_surjectivity(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Propose one generic backward branch, not a verified ProofStep."""
    required = ehp_zero_inputs(goal)
    if required is None:
        return ()
    return (GoalExpansion(
        rule=ehp_zero_from_delta_surjectivity_rule(goal),
        subgoals=required,
    ),)
```

## `audit.py`

```python
"""Phase 174 R3-R7-R3: source-first generic EHP-zero candidate audit.

No production provider is changed by this audit. A backward proposal is not
proof and cannot discharge missing Delta surjectivity or free-group premises.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R3"
BASE_HEAD = "c055e8ddddaee2c0d0552bbdcc3e3afc62b6ff9c"
ALLOWED_NEXT_COMMIT_PREFIX = "phase174_r3_r7_r2_ehp_chain_audit/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r14_r9_ehp_exactness.py": "c39759f0b693ce89100ef8439e8aec7fe325694f",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase165_r55_nk_only_goal.py": "9aa232c8f98a7a75f27266044224eddfa98c5e04",
}
EXPECTED_COUNTS = {
    "delta_e_exactness": 1,
    "e_h_exactness": 1,
    "delta_isomorphism": 1,
    "delta_surjectivity": 0,
    "terminal_zero": 1,
    "target_zero": 0,
}


def git(*args: str, cwd: Path = ROOT) -> str:
    process = subprocess.run(
        ("git",) + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
        errors="replace",
    )
    return process.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def accepted_source_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(
        blob_sha(item) == expected
        for item in (data, normalized, normalized.replace(b"\n", b"\r\n"))
    )


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    repo = Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve()
    if repo != root.resolve():
        raise RuntimeError("The audit must be extracted immediately under the repo root")
    branch = git("branch", "--show-current", cwd=root)
    local_head = git("rev-parse", "HEAD", cwd=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote_head = remote_line.split()[0] if remote_line else ""
    if branch != "develop" or local_head != remote_head:
        raise RuntimeError("Expected develop with local HEAD matching live origin/develop")
    base = git("merge-base", BASE_HEAD, remote_head, cwd=root)
    if base != BASE_HEAD:
        raise RuntimeError("Remote develop is not descended from the reviewed baseline")
    changed = git("diff", "--name-only", BASE_HEAD, remote_head, cwd=root)
    paths = changed.splitlines() if changed else []
    if any(not path.startswith(ALLOWED_NEXT_COMMIT_PREFIX) for path in paths):
        raise RuntimeError("Remote develop changed an unaudited path; redo source review")
    staged = git("diff", "--cached", "--name-only", cwd=root)
    if staged:
        raise RuntimeError("Staged changes must be reviewed separately")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not accepted_source_blob(file.read_bytes(), sha):
            raise RuntimeError("Audited source blob has changed: " + relative)
    toda = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    for clause in (
        r"\pi^{n}_{n+5}=0\ (n\ge7)",
        r"\pi^{13}_{13}\xrightarrow[\cong]{\Delta}\pi^{6}_{11}",
        r"\pi^{6}_{11}\xrightarrow{E}\pi^{7}_{12}",
        r"\pi_{12}^{13}=0",
    ):
        if clause not in toda:
            raise RuntimeError("Toda Proposition 5.9 proof transcription changed")
    return {
        "branch": branch,
        "local_head": local_head,
        "remote_head": remote_head,
        "reviewed_base_head": BASE_HEAD,
        "allowed_followup_paths": paths,
        "source_guard_count": len(SOURCE_BLOBS),
        "staged_changes": [],
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root
        ).splitlines(),
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r2" / "ehp_chain_audit.json"


def verify_r2_evidence(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("phase") != "174-R3-R7-R2":
        raise RuntimeError("Wrong previous audit phase")
    if data.get("gate") != "PASS_READ_ONLY_TYPED_EHP_CHAIN":
        raise RuntimeError("Previous typed EHP audit not certified")
    prior = data.get("previous_audit") or {}
    if prior.get("zero_root_proposal_count") != 0:
        raise RuntimeError("Unexpected previous zero-root proposal count")
    live = data.get("live_obligations") or {}
    counts = {
        key: (live.get("obligations") or {}).get(key, {}).get("proposal_count")
        for key in EXPECTED_COUNTS
    }
    if counts != EXPECTED_COUNTS:
        raise RuntimeError("Previous source-screened proposal counts differ")
    pi = live.get("pi11_6") or {}
    if (pi.get("search_status") != "search_failed"
            or len(pi.get("open_goal_types", ())) != 2):
        raise RuntimeError("Previous pi_11^6 blocker differs")
    if data.get("new_group_given") != 0 or data.get("new_inference_rules") != 0:
        raise RuntimeError("Previous audit introduced unapproved premises")
    return {
        "previous_gate": data["gate"],
        "proposal_counts": counts,
        "pi11_6_open_goal_types": pi["open_goal_types"],
        "pi11_6_frontier": pi.get("candidate_frontier"),
        "delta_isomorphism_candidate_is_not_surjectivity_evidence": True,
    }


def inspect_new_candidate() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_source_first_audit.audit import (
        is_exact_given, summarize_proposals,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        ehp_zero_inputs, expand_ehp_zero_from_delta_surjectivity,
    )
    from proof import ProofRule

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    requirements = ehp_zero_inputs(goal)
    if requirements is None:
        raise RuntimeError("The typed general EHP condition does not apply")
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    screened = prefer_universal_prop42_derivation(screened)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    if is_exact_given(goal, admitted):
        raise RuntimeError("The desired zero-group claim was an admitted GIVEN")
    existing = shared_expansion_provider(screened, proof_target=goal)
    old_root = summarize_proposals(existing, goal, admitted)
    new_root = expand_ehp_zero_from_delta_surjectivity(goal)
    if old_root["proposal_count"] != 0 or len(new_root) != 1:
        raise RuntimeError("Candidate root baseline differs")
    branches = {}
    for name, child in zip(
        ("delta_surjectivity", "delta_e_exactness", "e_h_exactness", "terminal_zero"),
        requirements,
    ):
        branch = summarize_proposals(existing, child, admitted, limit=5)
        branches[name] = {
            "goal": branch["goal"],
            "proposal_count": branch["proposal_count"],
            "proposals": branch["proposals"],
        }
    if branches["delta_surjectivity"]["proposal_count"] != 0:
        raise RuntimeError("A Delta-surjectivity candidate appeared unexpectedly")
    return {
        "source_screening": "independent_source_screened",
        "existing_zero_root_proposals": old_root["proposal_count"],
        "isolated_generic_root_proposals": len(new_root),
        "generic_root_rule": new_root[0].rule.name,
        "separate_premises": branches,
        "delta_surjectivity_still_unproved": True,
        "source_first_proof_steps_created": 0,
        "not_registered_with_production_provider": True,
        "no_target_direct_given": True,
    }


def report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r3" / "generic_zero_rule.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    state = verify_git_and_sources(root)
    report_file = previous_report_path()
    if not report_file.is_file():
        raise RuntimeError("Previous R3-R7-R2 JSON is required: " + str(report_file))
    evidence = verify_r2_evidence(json.loads(report_file.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_new_candidate()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "ISOLATED_GENERIC_RULE_AUDIT",
        "git_state": state,
        "prior_evidence": evidence,
        "new_candidate": live,
        "original_print_edition_verified": False,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_isolated_inference_rules": 1,
        "production_files_modified": False,
        "full_pytest_run": False,
        "generic_zero_group_completion_claimed": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_ISOLATED_RULE_DELTA_SURJECTIVITY_PENDING",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = make_report(dry_run=args.dry_run)
    destination = report_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("PHASE174_R3R7R3_REMOTE_HEAD=" + result["git_state"]["remote_head"])
    print("PHASE174_R3R7R3_LOCAL_HEAD=" + result["git_state"]["local_head"])
    print("PHASE174_R3R7R3_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R3_PREVIOUS_DELTA_SURJECTIVITY_PROPOSALS=0")
    if result["new_candidate"] is not None:
        candidate = result["new_candidate"]
        print("PHASE174_R3R7R3_ISOLATED_ROOT_PROPOSALS=" + str(
            candidate["isolated_generic_root_proposals"]
        ))
        for name, item in candidate["separate_premises"].items():
            print("PHASE174_R3R7R3_CHILD_" + name.upper() + "_PROPOSALS=" + str(
                item["proposal_count"]
            ))
        print("PHASE174_R3R7R3_PUBLIC_PROVIDER_UNCHANGED=True")
    print("PHASE174_R3R7R3_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R7R3_NEW_PRODUCTION_RULES=0")
    print("PHASE174_R3R7R3_FULL_PYTEST=False")
    print("PHASE174_R3R7R3_REPORT=" + str(destination))
    print("PHASE174_R3R7R3_GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_rule.py`

```python
"""Focused contract checks for the generic EHP zero inference."""
from __future__ import annotations

import pytest

from homotopy_groups import (
    TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup,
    TodaPrimaryGroupZeroStatement,
)
from map_facts import EHP_DELTA_MAP, EHP_E_MAP
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r7_r3_ehp_zero_rule.rule import (
    RULE_NAME,
    ehp_zero_from_delta_surjectivity_rule,
    ehp_zero_inputs,
    expand_ehp_zero_from_delta_surjectivity,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, find_inference_matches_for_rule,
)
from toda_rules import TodaProp42ExactnessStatement


def _goal(i: int, sphere: int) -> TodaPrimaryGroupZeroStatement:
    return TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(i, sphere))


def _inferred(statement: object) -> ProofStep:
    """Only a fixture; a real proof tree must verify every such subgoal."""
    return ProofStep(
        conclusion=statement, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="test-only hypothetical premise"),
    )


def test_pi127_exactly_four_typed_premises() -> None:
    root = _goal(12, 7)
    required = ehp_zero_inputs(root)
    assert required is not None
    surjective, de, eh, terminal = required
    assert surjective == MapSurjective(TodaDeltaMap(
        TodaPrimaryGroup(13, 13), TodaPrimaryGroup(11, 6)
    ))
    assert prop42_exactness_indices(de) == (6, 12, "delta_e")
    assert prop42_exactness_indices(eh) == (6, 12, "e_h")
    assert terminal == _goal(12, 13)
    options = expand_ehp_zero_from_delta_surjectivity(root)
    assert len(options) == 1
    assert options[0].subgoals == required
    assert options[0].rule.name == RULE_NAME


@pytest.mark.parametrize("group_dimension,sphere_dimension", (
    (9, 5), (10, 6), (12, 7), (14, 8),
))
def test_generic_no_stem_enumeration(
    group_dimension: int, sphere_dimension: int,
) -> None:
    root = _goal(group_dimension, sphere_dimension)
    goals = ehp_zero_inputs(root)
    assert goals is not None
    n = sphere_dimension - 1
    assert prop42_exactness_indices(goals[1]) == (n, group_dimension, "delta_e")
    assert prop42_exactness_indices(goals[2]) == (n, group_dimension, "e_h")
    assert goals[3] == _goal(group_dimension, 2 * n + 1)


@pytest.mark.parametrize("candidate", (
    object(), "zero", _goal(3, 5), _goal(1, 1),
    TodaPrimaryGroupZeroStatement(TodaPrimaryGroup("12", 7)),
    TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, "7")),
))
def test_invalid_target_has_no_backward_candidate(candidate: object) -> None:
    assert ehp_zero_inputs(candidate) is None
    assert expand_ehp_zero_from_delta_surjectivity(candidate) == ()


def test_valid_premises_derive_only_through_inference_match() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = tuple(_inferred(statement) for statement in goals)
    matches = find_inference_matches_for_rule(rule, proofs)
    assert len(matches) == 1
    result = derive_inference_proof_step(matches[0])
    assert result.conclusion == target
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == proofs
    assert result.inference_rule is rule


def test_direct_given_cannot_replace_independently_inferred_premise() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = list(_inferred(statement) for statement in goals)
    for index in range(4):
        tampered = list(proofs)
        tampered[index] = ProofStep(goals[index], (), ProofRule.GIVEN)
        assert find_inference_matches_for_rule(rule, tuple(tampered)) == ()


def test_wrong_delta_map_and_wrong_terminal_are_rejected() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = tuple(_inferred(statement) for statement in goals)
    bad_delta = _inferred(MapSurjective(TodaDeltaMap(
        TodaPrimaryGroup(15, 15), TodaPrimaryGroup(13, 7)
    )))
    bad_terminal = _inferred(_goal(13, 13))
    assert find_inference_matches_for_rule(rule, (bad_delta,) + proofs[1:]) == ()
    assert find_inference_matches_for_rule(rule, proofs[:3] + (bad_terminal,)) == ()


def test_windows_must_be_consecutive_and_in_correct_order() -> None:
    target = _goal(12, 7)
    goals = ehp_zero_inputs(target)
    assert goals is not None
    rule = ehp_zero_from_delta_surjectivity_rule(target)
    proofs = tuple(_inferred(statement) for statement in goals)
    # The matcher is permutation-insensitive; the ordered proof contract is
    # nevertheless strict for actual reconstructed parent slots.
    assert rule.match_guard((proofs[0], proofs[2], proofs[1], proofs[3]), {}) is False
    bad_window = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(13, 13),
        middle_term=TodaPrimaryGroup(11, 6),
        target_term=TodaPrimaryGroup(12, 7),
        first_map=EHP_E_MAP,
        second_map=EHP_DELTA_MAP,
    ))
    assert find_inference_matches_for_rule(rule, (
        proofs[0], _inferred(bad_window), proofs[2], proofs[3],
    )) == ()


def test_no_target_group_given_is_constructed() -> None:
    root = _goal(12, 7)
    options = expand_ehp_zero_from_delta_surjectivity(root)
    assert len(options) == 1
    assert all(type(goal) is not ProofStep for goal in options[0].subgoals)
    assert root not in options[0].subgoals
```

## `tests/test_audit.py`

```python
"""Pure guard and evidence checks for the isolated R3-R7-R3 audit."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r3_ehp_zero_rule.audit import (
    BASE_HEAD, EXPECTED_COUNTS, SOURCE_BLOBS,
    accepted_source_blob, blob_sha, verify_r2_evidence,
)


def _report() -> dict:
    return {
        "phase": "174-R3-R7-R2",
        "gate": "PASS_READ_ONLY_TYPED_EHP_CHAIN",
        "previous_audit": {"zero_root_proposal_count": 0},
        "live_obligations": {
            "obligations": {
                k: {"proposal_count": v} for k, v in EXPECTED_COUNTS.items()
            },
            "pi11_6": {
                "search_status": "search_failed",
                "open_goal_types": ["Relation", "Relation"],
                "candidate_frontier": [],
            },
        },
        "new_group_given": 0,
        "new_inference_rules": 0,
    }


def test_evidence_accepts_only_observed_source_screened_counts() -> None:
    data = verify_r2_evidence(_report())
    assert data["proposal_counts"] == EXPECTED_COUNTS
    assert data["delta_isomorphism_candidate_is_not_surjectivity_evidence"]


@pytest.mark.parametrize("changed_name,changed_count", (
    ("delta_surjectivity", 1), ("target_zero", 1),
    ("delta_e_exactness", 0), ("e_h_exactness", 0),
))
def test_evidence_fails_closed_when_candidates_change(
    changed_name: str, changed_count: int,
) -> None:
    report = _report()
    report["live_obligations"]["obligations"][changed_name]["proposal_count"] = changed_count
    with pytest.raises(RuntimeError, match="counts differ"):
        verify_r2_evidence(report)


def test_prior_gate_and_pi11_status_fail_closed() -> None:
    data = _report()
    data["gate"] = "PASS_PREFLIGHT"
    with pytest.raises(RuntimeError, match="not certified"):
        verify_r2_evidence(data)
    data = _report()
    data["live_obligations"]["pi11_6"]["search_status"] = "complete"
    with pytest.raises(RuntimeError, match="blocker differs"):
        verify_r2_evidence(data)


def test_prior_direct_group_claims_are_not_admitted() -> None:
    report = _report()
    report["new_group_given"] = 1
    with pytest.raises(RuntimeError, match="unapproved"):
        verify_r2_evidence(report)


def test_sha_guard_accepts_crlf_without_widening() -> None:
    original = b"line1\nline2\n"
    sha = blob_sha(original)
    assert accepted_source_blob(original, sha)
    assert accepted_source_blob(b"line1\r\nline2\r\n", sha)
    assert not accepted_source_blob(b"line1\nwrong\n", sha)


def test_audit_does_not_mutate_production_code() -> None:
    source = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(source.read_text(encoding="utf-8"))
    names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "inspect_new_candidate" in names
    assert "verify_git_and_sources" in names
    assert "install" not in names
    assert "modify_production" not in names
    assert len(SOURCE_BLOBS) == 7
    assert len(BASE_HEAD) == 40
```

## `run.ps1`

```powershell
param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    $FocusedTests = @(
        'phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py',
        'phase174_r3_r7_r3_ehp_zero_rule/tests/test_audit.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_contract.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_repo.py',
        'phase174_r3_r7_r2_ehp_chain_audit/tests/test_runner_import_mode.py',
        'phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py',
        'phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py',
        'phase165_r14_r6_generic_iso/test_phase165_r14_r6_generic_iso.py',
        'phase173_r4_r11_zero_public_connection/tests/test_route.py'
    )
    foreach ($TestFile in $FocusedTests) {
        if (-not (Test-Path -LiteralPath $TestFile)) {
            throw "Missing focused test: $TestFile"
        }
    }

    Write-Output 'PHASE174_R3R7R3_FOCUSED_PYTEST_START'
    & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @FocusedTests
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R3-R7-R3 focused pytest failed'
    }
    Write-Output 'PHASE174_R3R7R3_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r3_ehp_zero_rule.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r3_ehp_zero_rule.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw 'Phase 174 R3-R7-R3 source-first audit failed'
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
```

