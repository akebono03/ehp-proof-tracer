# R15 新規コード全文

変更した既存ファイル・関数はありません。以下は新規ファイルの全文です。

## `audit.py`

```python
"""Phase 174 R3-R7-R15: audit the remaining E(pi_10^5) proof frontier.

No production source, registered GIVEN, proof rule, saved proof, or narrative
is changed by this module. Isolated GoalExpansion objects are NOT proofs.
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
PHASE = "174-R3-R7-R15"
PRE_R14_HEAD = "1ad9e3aeba5dc9e28785230fe46fbcd2632ddee0"
REVIEWED_REMOTE_HEAD = "380a5b17414075e7ec5ebbb17c310e8dad49fa60"
SHARED_MATH = "phase165_r52_r9_shared_math.py"
PRE_R14_SHARED_BLOB = "0a06dcb0a721e5a79e866cd96909eeeec69303d6"
R14_SHARED_BLOB = "7f81769776278b46a220fb90771970a9dd7c73c2"
R14_DIR = "phase174_r3_r7_r14_public_annihilator_connection/"
PINS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r13_cited_annihilator_bridge/registry.py": "489380d974d9e3a2869743325d21b15b4d64f808",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10b_registered_stable_family_binding/family_registry.py": "4e461795954cc3e7a34fe9e3b47f77d00e5faeda",
    "phase174_r3_r7_r14_public_annihilator_connection/tests/test_public.py": "a5a798b5c7b7ae148c45db5ffc3be86654fdf69b",
    "phase174_r3_r7_r14_public_annihilator_connection/audit.py": "1e76f6ec08e68a610235e81114a0b51f3ef4b055",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
}


def git(*args: str, root: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args,
        cwd=root,
        check=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        text=True,
    )
    return result.stdout.strip()


def git_bytes(*args: str, root: Path = ROOT) -> bytes:
    return subprocess.run(
        ("git",) + args,
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout


def blob_sha(value: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(value)).encode("ascii") + b"\0" + value,
    ).hexdigest()


def matches_pinned_blob(value: bytes, expected: str) -> bool:
    """Allow a uniform LF/CRLF checkout, never mixed EOL or changed text."""
    if len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
        return False
    non_crlf = value.replace(b"\r\n", b"")
    if b"\r" in non_crlf or (b"\r\n" in value and b"\n" in non_crlf):
        return False
    normalized = value.replace(b"\r\n", b"\n")
    return any(blob_sha(candidate) == expected for candidate in (
        value, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_lineage(
    local: str, remote: str, committed_paths: tuple[str, ...],
    tracked_paths: tuple[str, ...],
) -> str:
    """Accept the handoff state or the exact reviewed R14 merged state."""
    if remote != REVIEWED_REMOTE_HEAD:
        raise RuntimeError("GitHub develop changed since R15 review")
    if not committed_paths or not set(committed_paths).issubset(
        {SHARED_MATH} | {x for x in committed_paths if x.startswith(R14_DIR)}
    ) or SHARED_MATH not in committed_paths or not any(
        path.startswith(R14_DIR) for path in committed_paths
    ):
        raise RuntimeError("R14 commit lineage changed outside its reviewed paths")
    if local == PRE_R14_HEAD and tracked_paths == (SHARED_MATH,):
        return "LOCAL_PRE_R14_WITH_EXACT_WORKTREE_PATCH"
    if local == REVIEWED_REMOTE_HEAD and tracked_paths == ():
        return "R14_MERGED_CLEAN"
    raise RuntimeError("Unreviewed local HEAD or tracked changes; do not reset or overwrite")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    """Read-only source guard for both legitimate R14 handoff layouts."""
    actual_root = Path(git("rev-parse", "--show-toplevel", root=root)).resolve()
    if actual_root != root.resolve():
        raise RuntimeError("Extract the R15 package directly beneath repository root")
    if git("branch", "--show-current", root=root) != "develop":
        raise RuntimeError("Only the audited develop branch is accepted")
    local = git("rev-parse", "HEAD", root=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", root=root)
    remote = remote_line.split()[0] if remote_line else ""
    if git("diff", "--cached", "--name-only", root=root):
        raise RuntimeError("Staged changes require separate review")
    tracked = tuple(git("diff", "--name-only", root=root).splitlines())
    if local not in (PRE_R14_HEAD, REVIEWED_REMOTE_HEAD):
        raise RuntimeError("Unreviewed local HEAD; no automatic merge will be attempted")
    git_bytes("merge-base", "--is-ancestor", PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, root=root)
    commits = git("rev-list", "--reverse", PRE_R14_HEAD + ".." + REVIEWED_REMOTE_HEAD, root=root).splitlines()
    if len(commits) != 2:
        raise RuntimeError("Expected exactly two reviewed R14 merge-lineage commits")
    committed_paths = tuple(git("diff", "--name-only", PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, root=root).splitlines())
    lineage = reviewed_lineage(local, remote, committed_paths, tracked)
    before = git_bytes("show", PRE_R14_HEAD + ":" + SHARED_MATH, root=root)
    after = git_bytes("show", REVIEWED_REMOTE_HEAD + ":" + SHARED_MATH, root=root)
    if not matches_pinned_blob(before, PRE_R14_SHARED_BLOB):
        raise RuntimeError("Pre-R14 shared math Git blob mismatch")
    if not matches_pinned_blob(after, R14_SHARED_BLOB):
        raise RuntimeError("Merged R14 shared math Git blob mismatch")
    current = (root / SHARED_MATH).read_bytes()
    if not matches_pinned_blob(current, R14_SHARED_BLOB):
        raise RuntimeError("Local shared math is not exactly the committed R14 output")
    for relative, expected in PINS.items():
        file = root / relative
        if not file.is_file() or not matches_pinned_blob(file.read_bytes(), expected):
            raise RuntimeError("Source Guard failed for " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "lineage": lineage,
        "r14_commits_since_handoff": len(commits),
        "tracked_changes": list(tracked),
        "pinned_source_files": len(PINS) + 1,
        "r14_shared_math_identical_to_remote": True,
        "full_pytest_run": False,
    }


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r14" / "public_annihilator_connection.json"


def validate_r14_report(report: dict[str, Any]) -> dict[str, Any]:
    if report.get("phase") != "174-R3-R7-R14":
        raise RuntimeError("R14 audit evidence phase mismatch")
    if report.get("gate") != "PASS_PUBLIC_CITED_GENERAL_SOURCE_N6_INFERENCE_ROOT_PENDING":
        raise RuntimeError("R14 did not pass its published gate")
    if (report.get("new_group_given") != 0
            or report.get("new_direct_concrete_relation_given") != 0
            or report.get("full_pytest_run") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R14 trust boundary changed")
    live = report.get("live") or {}
    if (live.get("public_general_source_givens") != 1
            or live.get("public_n6_specialization_proposals") != 1
            or live.get("public_n6_cited_parent") is not True
            or live.get("new_group_given") != 0
            or live.get("goal_complete_claimed") is not False):
        raise RuntimeError("R14 cited source / n6 inference evidence missing")
    return {
        "gate": report["gate"],
        "cited_general_source": True,
        "n6_inference_has_cited_parent": True,
        "root_complete": False,
    }


def summarize_options(options: tuple[object, ...]) -> dict[str, Any]:
    if not isinstance(options, tuple):
        raise TypeError("Public provider must return tuple of GoalExpansions")
    items = []
    for option in options:
        children = getattr(option, "subgoals", None)
        rule = getattr(option, "rule", None)
        if not isinstance(children, tuple) or not isinstance(getattr(rule, "name", None), str):
            raise TypeError("Invalid unproved expansion proposal")
        items.append({
            "rule": rule.name,
            "child_types": [type(x).__name__ for x in children],
            "child_reprs": [repr(x)[:350] for x in children],
        })
    return {"count": len(items), "proposals": items[:20], "truncated": len(items) > 20}


def classify_frontier(public_rule_names: tuple[str, ...], isolated_rule_name: str) -> str:
    """Absence of a named rule never establishes unprovability."""
    if isolated_rule_name in public_rule_names:
        return "NAMED_RULE_PRESENT_CANDIDATE_NOT_PROOF"
    if public_rule_names:
        return "OTHER_PUBLIC_CANDIDATES_UNVERIFIED"
    return "NO_PUBLIC_CANDIDATE_OBSERVED"


def inspect_live_chain() -> dict[str, Any]:
    """Rebuild typed premises; compare public and isolated unproved frontiers."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10b_registered_stable_family_binding.family_registry import (
        read_registered_stable_families, registered_family_of,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        RULE_NAME as CYCLIC_RULE, cyclic_generator_zero_image_inputs,
        expand_zero_image_from_cyclic_generator,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        RULE_NAME as COMPOSITE_ZERO_RULE, composite_zero_generator_inputs,
        expand_generator_zero_from_composite,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import (
        RULE_NAME as ASSOCIATIVITY_RULE, generator_image_associativity_inputs,
        expand_generator_image_associativity,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        RULE_NAME as ANN_RULE, canonical_annihilator_instance,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import CitedFamilyAnnihilator
    from phase174_r3_r7_r14_public_annihilator_connection.audit import inspect_public_source_and_proof
    from proof import ProofRule, ProofStep, Relation, RelationType
    from unified_statement_registry import AssertionOrigin

    r14 = inspect_public_source_and_proof()
    if (r14["public_general_source_givens"] != 1
            or r14["public_n6_specialization_proposals"] != 1
            or r14["public_n6_cited_parent"] is not True):
        raise RuntimeError("R14 public cited ancestry was lost")

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    fixed_steps = tuple(
        link.step for link in screened.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and screened.registry.assertion(link.assertion_id).content == link.step.conclusion
    )
    source_laws = tuple(
        step.conclusion for step in fixed_steps
        if isinstance(step.conclusion, CitedFamilyAnnihilator)
    )
    if len(source_laws) != 1:
        raise RuntimeError("Exactly one reviewed general annihilator source is required")
    n6_goal = canonical_annihilator_instance(source_laws[0], 6)
    if n6_goal is None:
        raise RuntimeError("Reviewed typed n=6 source instance not found")
    provider = shared_expansion_provider(screened, proof_target=target)

    prior = exact_prior_database_result(5, 5)
    domain = TodaPrimaryGroup(10, 5)
    codomain = TodaPrimaryGroup(11, 6)
    if (not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != domain
            or getattr(prior.rhs, "order", None) != 2):
        raise RuntimeError("Canonical finite-cyclic database candidate changed")
    families = read_registered_stable_families()
    nu = tuple(f for f in families if f.family_id == 4 and f.symbol_family == "ν" and f.stem == 3)
    eta = tuple(f for f in families if f.family_id == 2 and f.symbol_family == "η" and f.stem == 1)
    if len(nu) != 1 or len(eta) != 1:
        raise RuntimeError("Registered family IDs and stems changed")

    def member(family: object, index: int) -> HomotopyElement:
        value = HomotopyElement(
            family.name_at(index), dimension=index,
            source=index + family.stem, target=index,
            generator=GeneratorSymbol(family.symbol_family, index),
        )
        if registered_family_of(value) != family:
            raise RuntimeError("Unregistered canonical typed family member")
        return value

    nu5, nu6 = member(nu[0], 5), member(nu[0], 6)
    eta8, eta9, eta10 = member(eta[0], 8), member(eta[0], 9), member(eta[0], 10)
    g = Composition(nu5, Composition(eta8, eta9))
    if prior.rhs.generator != g:
        raise RuntimeError("DB generator differs from registered canonical factorization")
    suspension = TodaSuspensionMap(domain, codomain)
    image_zero = ImageZeroStatement(suspension)
    generator_zero = GeneratorImage(suspension, g, Zero())
    left_image = GeneratorImage(suspension, g, Composition(Composition(nu6, eta9), eta10))
    right_image = GeneratorImage(suspension, g, Composition(nu6, Composition(eta9, eta10)))
    fact = Relation(Composition(nu6, eta9), Zero(), RelationType.EQUALITY)
    if fact != n6_goal:
        raise RuntimeError("The ν6η9 statement does not match registered family identity")
    isolated_cyclic = expand_zero_image_from_cyclic_generator(image_zero, prior)
    isolated_composite = expand_generator_zero_from_composite(generator_zero, left_image)
    isolated_rebracket = expand_generator_image_associativity(left_image)
    isolated_factorization = expand_composite_generator_image(right_image)
    if (cyclic_generator_zero_image_inputs(image_zero, prior) != (prior, generator_zero)
            or composite_zero_generator_inputs(generator_zero, left_image) != (left_image, fact)
            or generator_image_associativity_inputs(left_image) != (right_image,)
            or component_image_obligations(right_image) is None
            or len(isolated_cyclic) != 1
            or len(isolated_composite) != 1
            or len(isolated_rebracket) != 1
            or len(isolated_factorization) != 1):
        raise RuntimeError("Existing isolated general rules no longer type-check")
    nu_image, eta_square_image = component_image_obligations(right_image)
    if (isolated_cyclic[0].subgoals != (prior, generator_zero)
            or isolated_composite[0].subgoals != (left_image, fact)
            or isolated_rebracket[0].subgoals != (right_image,)
            or isolated_factorization[0].subgoals != (nu_image, eta_square_image)):
        raise RuntimeError("Isolated generic candidate subgoals changed")

    goals = {
        "source_n6_annihilator": fact,
        "cyclic_presentation_pi10_5": prior,
        "suspension_image_zero": image_zero,
        "generator_image_zero": generator_zero,
        "generator_image_left_composite": left_image,
        "generator_image_right_composite": right_image,
        "canonical_nu_image": nu_image,
        "canonical_eta_square_image": eta_square_image,
        "final_pi12_7_zero": target,
    }
    direct_givens = [
        name for name, value in goals.items()
        if any(step.conclusion == value for step in fixed_steps)
    ]
    if any(name in direct_givens for name in (
        "source_n6_annihilator", "suspension_image_zero", "generator_image_zero",
        "generator_image_left_composite", "generator_image_right_composite", "final_pi12_7_zero",
    )):
        raise RuntimeError("Direct GIVEN shortcut for a derived or terminal goal")
    public = {name: summarize_options(tuple(provider(goal))) for name, goal in goals.items()}
    named = {
        "source_n6_annihilator": ANN_RULE,
        "suspension_image_zero": CYCLIC_RULE,
        "generator_image_zero": COMPOSITE_ZERO_RULE,
        "generator_image_left_composite": ASSOCIATIVITY_RULE,
        "generator_image_right_composite": "suspension preserves composition of separately proved maps",
    }
    for name, rule in named.items():
        names = tuple(item["rule"] for item in public[name]["proposals"])
        public[name]["stage"] = classify_frontier(names, rule)
        public[name]["named_rule"] = rule
    if public["source_n6_annihilator"]["named_rule"] not in (
        item["rule"] for item in public["source_n6_annihilator"]["proposals"]
    ):
        raise RuntimeError("Public R14 cited specialization is missing")

    return {
        "prior_result_is_candidate_not_verified_proof": True,
        "public_source_n6_inference_ancestry_checked": True,
        "canonical_family_identity_exact": True,
        "direct_given_intermediate_names": direct_givens,
        "isolated_existing_general_candidates": {
            "cyclic_generator_to_zero_image": len(isolated_cyclic),
            "composite_zero_to_generator_zero": len(isolated_composite),
            "rebracket_composite_image": len(isolated_rebracket),
            "decompose_composite_image": len(isolated_factorization),
        },
        "public_goal_frontiers": public,
        "new_verified_proof_steps": 0,
        "production_files_changed": False,
        "public_provider_changed": False,
        "new_group_given": 0,
        "completion_claimed": False,
        "full_pytest_run": False,
    }


def report_path(*, dry_run: bool) -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    filename = "chain_frontier_preflight.json" if dry_run else "chain_frontier_audit.json"
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r15" / filename


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    prior_path = prior_report_path()
    if not prior_path.is_file():
        raise RuntimeError("R14 completed local evidence missing: " + str(prior_path))
    previous = validate_r14_report(json.loads(prior_path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_live_chain()
    gate = "PASS_PREFLIGHT" if dry_run else "PASS_READ_ONLY_CHAIN_FRONTIER_NO_ROOT_CLAIM"
    return {
        "phase": PHASE,
        "mode": "READ_ONLY_PREFLIGHT" if dry_run else "READ_ONLY_CHAIN_FRONTIER",
        "git_state": git_state,
        "prior_evidence": previous,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "production_files_changed": False,
        "full_pytest_run": False,
        "completion_claimed": False,
        "gate": gate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = report_path(dry_run=args.dry_run)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R15_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["lineage"])
    print(prefix + "SOURCE_GUARD=PASS")
    if report["live"] is not None:
        live = report["live"]
        for name, item in live["public_goal_frontiers"].items():
            print(prefix + "FRONTIER_" + name.upper() + "=" + str(item["count"]))
            if "stage" in item:
                print(prefix + "STAGE_" + name.upper() + "=" + item["stage"])
        print(prefix + "ISOLATED_EXISTING_RULES=" + str(sum(
            live["isolated_existing_general_candidates"].values()
        )))
        print(prefix + "VERIFIED_NEW_PROOF_STEPS=0")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_contract.py`

```python
"""Read-only audit guards; intentionally no production source modification."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase174_r3_r7_r15_chain_frontier_audit.audit import (
    PINS, PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, R14_DIR, R14_SHARED_BLOB,
    SHARED_MATH, blob_sha, classify_frontier, matches_pinned_blob,
    reviewed_lineage, summarize_options, validate_r14_report,
)


def sample_committed_paths() -> tuple[str, ...]:
    return (SHARED_MATH, R14_DIR + "audit.py", R14_DIR + "tests/test_public.py")


def sample_r14_report() -> dict:
    return {
        "phase": "174-R3-R7-R14",
        "gate": "PASS_PUBLIC_CITED_GENERAL_SOURCE_N6_INFERENCE_ROOT_PENDING",
        "new_group_given": 0,
        "new_direct_concrete_relation_given": 0,
        "full_pytest_run": False,
        "completion_claimed": False,
        "live": {
            "public_general_source_givens": 1,
            "public_n6_specialization_proposals": 1,
            "public_n6_cited_parent": True,
            "new_group_given": 0,
            "goal_complete_claimed": False,
        },
    }


def test_handoff_and_merged_lineages_are_both_guarded() -> None:
    paths = sample_committed_paths()
    assert reviewed_lineage(
        PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, paths, (SHARED_MATH,),
    ) == "LOCAL_PRE_R14_WITH_EXACT_WORKTREE_PATCH"
    assert reviewed_lineage(
        REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, paths, (),
    ) == "R14_MERGED_CLEAN"


@pytest.mark.parametrize("local,remote,paths,tracked", (
    (PRE_R14_HEAD, PRE_R14_HEAD, sample_committed_paths(), (SHARED_MATH,)),
    ("a" * 40, REVIEWED_REMOTE_HEAD, sample_committed_paths(), ()),
    (REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, (SHARED_MATH, "proof.py"), ()),
    (REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, (R14_DIR + "audit.py",), ()),
    (PRE_R14_HEAD, REVIEWED_REMOTE_HEAD, sample_committed_paths(), ("proof.py",)),
    (REVIEWED_REMOTE_HEAD, REVIEWED_REMOTE_HEAD, sample_committed_paths(), (SHARED_MATH,)),
))
def test_lineage_rejects_unreviewed_state(
    local: str, remote: str, paths: tuple[str, ...], tracked: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_lineage(local, remote, paths, tracked)


def test_pinned_blobs_allow_only_uniform_line_ends() -> None:
    raw = b"a\nb\n"
    sha = blob_sha(raw)
    assert matches_pinned_blob(raw, sha)
    assert matches_pinned_blob(b"a\r\nb\r\n", sha)
    assert not matches_pinned_blob(b"a\r\nb\n", sha)
    assert not matches_pinned_blob(b"a\rb\r", sha)
    assert not matches_pinned_blob(raw + b"c", sha)
    assert not matches_pinned_blob(raw, sha[:39])
    assert len(R14_SHARED_BLOB) == 40
    assert len(PINS) >= 10


def test_r14_success_is_read_as_inference_not_root_completion() -> None:
    checked = validate_r14_report(sample_r14_report())
    assert checked["n6_inference_has_cited_parent"] is True
    assert checked["root_complete"] is False


@pytest.mark.parametrize("key,value", (
    ("gate", "PASS_PREFLIGHT"),
    ("new_group_given", 1),
    ("new_direct_concrete_relation_given", 1),
    ("full_pytest_run", True),
    ("completion_claimed", True),
))
def test_bad_r14_top_level_evidence_fails_closed(key: str, value: object) -> None:
    report = sample_r14_report()
    report[key] = value
    with pytest.raises(RuntimeError):
        validate_r14_report(report)


@pytest.mark.parametrize("key,value", (
    ("public_general_source_givens", 0),
    ("public_n6_specialization_proposals", 0),
    ("public_n6_cited_parent", False),
    ("new_group_given", 1),
    ("goal_complete_claimed", True),
))
def test_bad_r14_proof_evidence_fails_closed(key: str, value: object) -> None:
    report = deepcopy(sample_r14_report())
    report["live"][key] = value
    with pytest.raises(RuntimeError):
        validate_r14_report(report)


def test_cannot_promote_isolated_candidate_to_proof() -> None:
    assert classify_frontier((), "generic") == "NO_PUBLIC_CANDIDATE_OBSERVED"
    assert classify_frontier(("other",), "generic") == "OTHER_PUBLIC_CANDIDATES_UNVERIFIED"
    assert classify_frontier(("generic",), "generic") == "NAMED_RULE_PRESENT_CANDIDATE_NOT_PROOF"


def test_provider_summary_rejects_non_expansion() -> None:
    with pytest.raises(TypeError):
        summarize_options((object(),))
    with pytest.raises(TypeError):
        summarize_options([])
```

## `tests/test_public_frontier.py`

```python
"""Focused public proof-frontier integration: no completion claim."""
from __future__ import annotations

from phase174_r3_r7_r15_chain_frontier_audit.audit import inspect_live_chain


def test_canonical_chain_has_only_independent_candidate_obligations() -> None:
    live = inspect_live_chain()
    assert live["public_source_n6_inference_ancestry_checked"] is True
    assert live["canonical_family_identity_exact"] is True
    assert live["prior_result_is_candidate_not_verified_proof"] is True
    assert live["new_verified_proof_steps"] == 0
    assert live["new_group_given"] == 0
    assert live["completion_claimed"] is False
    assert live["production_files_changed"] is False
    assert live["public_provider_changed"] is False
    isolated = live["isolated_existing_general_candidates"]
    assert isolated == {
        "cyclic_generator_to_zero_image": 1,
        "composite_zero_to_generator_zero": 1,
        "rebracket_composite_image": 1,
        "decompose_composite_image": 1,
    }
    for key in (
        "source_n6_annihilator", "suspension_image_zero", "generator_image_zero",
        "generator_image_left_composite", "generator_image_right_composite",
        "final_pi12_7_zero",
    ):
        assert key not in live["direct_given_intermediate_names"]
    frontiers = live["public_goal_frontiers"]
    source = frontiers["source_n6_annihilator"]
    assert any(item["rule"] == source["named_rule"] for item in source["proposals"])
    assert "stage" in frontiers["suspension_image_zero"]
    assert "stage" in frontiers["generator_image_zero"]
```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$OldPythonPath = $env:PYTHONPATH
$OldNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Fetch only; never pull, checkout, reset, stash, or touch tracked sources.
    & git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw "Unable to fetch reviewed develop history" }
    & python -B -m phase174_r3_r7_r15_chain_frontier_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R15 source-first DryRun failed" }

    $FocusedGroups = @(
        @{ Name = 'R15_CONTRACT'; Paths = @(
            '.\phase174_r3_r7_r15_chain_frontier_audit\tests\test_contract.py'
        ) },
        @{ Name = 'R14_PUBLIC'; Paths = @(
            '.\phase174_r3_r7_r14_public_annihilator_connection\tests\test_public.py'
        ) },
        @{ Name = 'R12_SPECIALIZATION'; Paths = @(
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_rule.py'
        ) },
        @{ Name = 'R6_CYCLIC'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py'
        ) },
        @{ Name = 'R7_COMPOSITE_ZERO'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py'
        ) },
        @{ Name = 'R9_ASSOCIATIVITY'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py'
        ) }
    )
    foreach ($Group in $FocusedGroups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) { throw "Missing focused test: $TestPath" }
        }
        Write-Output "PHASE174_R3R7R15_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) { throw "Focused pytest failed: $($Group.Name)" }
    }
    Write-Output 'PHASE174_R3R7R15_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R15_GATE=PASS_PREFLIGHT'
    }
    else {
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
            '.\phase174_r3_r7_r15_chain_frontier_audit\tests\test_public_frontier.py'
        if ($LASTEXITCODE -ne 0) { throw 'R15 public frontier integration pytest failed' }
        & python -B -m phase174_r3_r7_r15_chain_frontier_audit.audit
        if ($LASTEXITCODE -ne 0) { throw 'R15 read-only proof-frontier audit failed' }
    }
    Write-Output '(END)'
}
finally {
    $env:PYTHONPATH = $OldPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $OldNoBytecode
    Pop-Location
}
```

