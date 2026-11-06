# Phase 174 R3-R7-R8R1：完全な置換コード

変更対象は `phase174_r3_r7_r8_composite_image_gap/audit.py` の SHA 定数と `tests/test_audit.py` に新規追加するテスト関数のみです。`run.ps1` は変更しませんが、再実行できるよう同梱・全文提示します。

新規テスト関数は既存 `tests/test_audit.py` の末尾に追加しました。import 変更はありません。既存の関数・クラスを改変しておらず、数学的な推論規則も変更していません。

## 変更一覧と Phase 境界

- `audit.py`: 固定 SHA の39文字から40文字への訂正のみ。Source Guard の意味は不変。
- `tests/test_audit.py`: 全 SHA が40文字の16進 SHA-1 形式であること、および該当 SHA が GitHub 確認値と一致することを回帰テスト。
- `run.ps1`: 変更なし（同梱）。
- 限定 pytest: `run.ps1` が R8、R7、R6、R5、R4、R3、数学的な回帰テストを別プロセスで実施。
- 完了条件: DryRun と通常実行が PASS、Source Guard PASS、監査 JSON 生成。
- 次 R9: 型付き証明の推論候補監査の結果を見てから一般規則の要否を判断。本修正では先取りしない。

## `audit.py`（全文）

```python
"""Phase 174 R3-R7-R8: read-only source-first composite-image frontier audit.

Separate a cited Toda family relation from a verified ProofStep. Inspect the
existing composition-of-suspension rule without registering any new premise,
provider, GIVEN or production inference. Unproved goals remain unproved.
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
PHASE = "174-R3-R7-R8"
BASE_HEAD = "67c57fc9ae63ce783ffdf9b502d472900abad57f"
REVIEWED_R7_HEAD = "95f37f2020a728b4951b8d26506059a8c54a685f"
REVIEWED_PREFIX = "phase174_r3_r7_r7_composite_zero_audit/"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r6_cyclic_generator_zero_image/rule.py": "66407339808ed4ba8a65c04fd3bfbbf05bde6745",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r7_composite_zero_audit/audit.py": "43c2d44f220a5adba151742f254c6cfac2e39575",
}
TODA_CLAUSES = {
    "general_nu_eta_zero": r"\nu_n\circ \eta_{n+3}=0\ (n\ge6)",
    "generator_suspension_composite": (
        r"E(\nu_5\circ\eta_8^2)=\nu_6\circ\eta_9\circ\eta_{10}=0"
    ),
    "whole_suspension_zero_conclusion": r"E\pi_{10}^5=0",
}
EXPECTED_R7 = {
    "isolated_generator_zero_candidate_count": 1,
    "public_composite_image_frontier": 0,
    "public_left_factor_zero_frontier": 1,
    "public_generator_zero_frontier": 0,
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args,
        cwd=cwd, text=True, capture_output=True, check=True,
        encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def accepts_blob(data: bytes, expected_sha: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    return any(blob_sha(candidate) == expected_sha for candidate in (
        data, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def reviewed_head_lineage(
    local: str,
    remote: str,
    successors: tuple[str, ...],
    changed_paths: tuple[str, ...],
) -> str:
    if local != remote or len(local) != 40:
        raise RuntimeError("Local and remote develop HEAD must match")
    if local == BASE_HEAD and not successors and not changed_paths:
        return "REVIEWED_BASE"
    if (
        local == REVIEWED_R7_HEAD
        and successors == (REVIEWED_R7_HEAD,)
        and bool(changed_paths)
        and all(path.startswith(REVIEWED_PREFIX) for path in changed_paths)
    ):
        return "REVIEWED_R7_ONLY_SUCCESSOR"
    raise RuntimeError("Unreviewed develop HEAD or non-R7 changes")


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be directly under the repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    remote_line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = remote_line.split()[0] if remote_line else ""
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes need review")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes need review")
    if local == BASE_HEAD:
        successors: tuple[str, ...] = ()
        changed_paths: tuple[str, ...] = ()
    else:
        subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, local),
            cwd=root, check=True, capture_output=True,
        )
        successors = tuple(git(
            "rev-list", "--reverse", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
        changed_paths = tuple(git(
            "diff", "--name-only", f"{BASE_HEAD}..{local}", cwd=root,
        ).splitlines())
    lineage = reviewed_head_lineage(local, remote, successors, changed_paths)
    for relative, sha in SOURCE_BLOBS.items():
        path = root / relative
        if not path.is_file() or not accepts_blob(path.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "head_lineage": lineage,
        "source_guard": "PASS",
        "reviewed_sources": list(SOURCE_BLOBS),
        "working_tree_status": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def verify_toda_source(root: Path = ROOT) -> dict[str, Any]:
    body = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    start = body.index(r"\begin{proposition}\label{prop:5.9}")
    end = body.index(r"\qed", start)
    text = body[start:end]
    offsets = {key: text.find(clause) for key, clause in TODA_CLAUSES.items()}
    if (any(value < 0 for value in offsets.values())
            or not (offsets["general_nu_eta_zero"]
                    < offsets["generator_suspension_composite"]
                    < offsets["whole_suspension_zero_conclusion"])):
        raise RuntimeError("Toda adopted Proposition 5.9 transcription changed")
    return {
        "source": "sources/toda/Toda_05_2.tex",
        "locator": "Proposition 5.9 proof; equation (5.9)",
        "offsets": offsets,
        "printed_edition_independently_verified": False,
        "general_formula_is_not_a_certified_step": True,
        "derived_generator_image_not_given": True,
    }


def prior_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r7" / "composite_zero_audit.json"


def validate_r7_evidence(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R7"
            or report.get("gate") != "PASS_ISOLATED_COMPOSITE_ZERO_CHILDREN_PENDING"):
        raise RuntimeError("Certified R7 full audit report is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False):
        raise RuntimeError("R7 trust contract changed")
    live = report.get("live") or {}
    if live.get("isolated_generator_zero_candidate_count") != 1:
        raise RuntimeError("R7 isolated candidate count changed")
    for name, expected in EXPECTED_R7.items():
        if name == "isolated_generator_zero_candidate_count":
            continue
        if (live.get(name) or {}).get("proposal_count") != expected:
            raise RuntimeError("R7 observed frontier changed: " + name)
    if (live.get("candidate_from_toda_text_is_not_evidence") is not True
            or live.get("public_provider_unchanged") is not True
            or live.get("new_verified_steps") != 0):
        raise RuntimeError("R7 candidate was incorrectly promoted to proof")
    return {"gate": report["gate"], "observed_counts": EXPECTED_R7.copy()}


def describe_candidate_options(options: object) -> list[dict[str, Any]]:
    """Describe unproved backward proposals; never turn options into proofs."""
    if not isinstance(options, tuple):
        raise TypeError("Backward proposal provider must return a tuple")
    records = []
    for item in options:
        children = getattr(item, "subgoals", None)
        if not isinstance(children, tuple):
            raise TypeError("GoalExpansion.subgoals must be a tuple")
        records.append({
            "rule": getattr(getattr(item, "rule", None), "name", None),
            "child_count": len(children),
            "children": [
                {"type": type(child).__name__, "repr": repr(child)[:1500]}
                for child in children
            ],
        })
    return records


def inspect_source_screened_frontier() -> dict[str, Any]:
    from expression import Composition, GeneratorSymbol, HomotopyElement, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
        cyclic_generator_zero_image_inputs,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        composite_zero_generator_inputs,
    )
    from phase174_r3_r7_source_first_audit.audit import is_exact_given, summarize_proposals
    from proof import ProofRule, Relation, RelationType

    target_zero = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target_zero)
    admitted = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    provider = shared_expansion_provider(screened, proof_target=target_zero)

    presentation = exact_prior_database_result(5, 5)
    if (not isinstance(presentation, Relation)
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != TodaPrimaryGroup(10, 5)):
        raise RuntimeError("Prior presentation no longer matches R7 input")
    suspension = TodaSuspensionMap(
        TodaPrimaryGroup(10, 5), TodaPrimaryGroup(11, 6),
    )
    image_zero = ImageZeroStatement(suspension)
    r6_children = cyclic_generator_zero_image_inputs(image_zero, presentation)
    if r6_children is None:
        raise RuntimeError("R6 typed goals changed")
    generator_zero = r6_children[1]
    nu6 = HomotopyElement(
        "nu_6", dimension=6, source=9, target=6,
        generator=GeneratorSymbol("nu", 6),
    )
    eta9 = HomotopyElement(
        "eta_9", dimension=9, source=10, target=9,
        generator=GeneratorSymbol("eta", 9),
    )
    eta10 = HomotopyElement(
        "eta_10", dimension=10, source=11, target=10,
        generator=GeneratorSymbol("eta", 10),
    )
    left = Composition(nu6, eta9)
    mapped = Composition(left, eta10)
    composite_goal = GeneratorImage(suspension, generator_zero.source_generator, mapped)
    r7_children = composite_zero_generator_inputs(generator_zero, composite_goal)
    if (r7_children is None or r7_children[0] != composite_goal
            or r7_children[1] != Relation(left, Zero(), RelationType.EQUALITY)):
        raise RuntimeError("R7 typed composite and annihilator goals changed")
    left_zero = r7_children[1]
    if any(is_exact_given(item, admitted) for item in (
        target_zero, image_zero, generator_zero, composite_goal, left_zero,
    )):
        raise RuntimeError("Target or source conclusion improperly supplied as GIVEN")

    public_composite = summarize_proposals(provider, composite_goal, admitted)
    public_left = summarize_proposals(provider, left_zero, admitted)
    public_generator = summarize_proposals(provider, generator_zero, admitted)
    if tuple(x["proposal_count"] for x in (
        public_composite, public_left, public_generator,
    )) != (0, 1, 0):
        raise RuntimeError("R7 live candidate frontier changed under source screening")

    independent_children = component_image_obligations(composite_goal)
    existing_options = expand_composite_generator_image(composite_goal)
    if bool(independent_children is not None) != bool(existing_options):
        raise RuntimeError("Existing composite-image rule expansion is inconsistent")
    if existing_options and (len(existing_options) != 1
                             or existing_options[0].subgoals != independent_children):
        raise RuntimeError("Existing composite-image rule changed")
    left_proposals = tuple(provider(left_zero))
    if len(left_proposals) != 1:
        raise RuntimeError("R7 left-factor proposal disappeared")
    from phase165_r3_recursive_search import SourceBoundGoal
    left_children = left_proposals[0].subgoals
    left_child_checks = []
    for child in left_children[:4]:
        actual = child.conclusion if isinstance(child, SourceBoundGoal) else child
        left_child_checks.append({
            "type": type(actual).__name__,
            "repr": repr(actual)[:1500],
            "source_bound": isinstance(child, SourceBoundGoal),
            "is_exact_screened_given": is_exact_given(actual, admitted),
            "is_parent_cycle": actual == left_zero,
        })

    return {
        "source_screening": "independent_source_screened",
        "screened_given_count": len(admitted),
        "typed_left_factor": repr(left)[:1500],
        "source_generator_type": type(generator_zero.source_generator).__name__,
        "source_generator_shape": repr(generator_zero.source_generator)[:1500],
        "target_composite_shape": repr(mapped)[:1500],
        "public_composite_image_frontier": public_composite,
        "public_left_factor_zero_frontier": public_left,
        "public_generator_zero_frontier": public_generator,
        "existing_composite_image_rule_candidate_count": len(existing_options),
        "existing_composite_image_rule_children": describe_candidate_options(existing_options),
        "existing_composite_image_rule_requires_typed_factors": True,
        "left_factor_rule_name": getattr(left_proposals[0].rule, "name", None),
        "left_factor_child_checks": left_child_checks,
        "public_provider_unchanged": True,
        "new_verified_steps": 0,
        "source_claim_promoted_to_given": False,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r8" / "composite_image_gap.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    source = verify_toda_source(root)
    previous = prior_report_path()
    if not previous.is_file():
        raise RuntimeError("R3-R7-R7 certified audit JSON is required")
    prior = validate_r7_evidence(json.loads(previous.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_source_screened_frontier()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_COMPOSITE_IMAGE_GAP",
        "git_state": git_state,
        "source_review": source,
        "prior_evidence": prior,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": (
            "PASS_PREFLIGHT" if dry_run
            else "PASS_READ_ONLY_COMPOSITE_IMAGE_GAP_DIAGNOSIS"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    path = output_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R8_"
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "SOURCE_GUARD=" + report["git_state"]["source_guard"])
    print(prefix + "HEAD_LINEAGE=" + report["git_state"]["head_lineage"])
    print(prefix + "TODA59_GENERAL_ANNIHILATOR=VERIFIED_TRANSCRIPTION")
    print(prefix + "PREVIOUS_PUBLIC_COMPOSITE_IMAGE_PROPOSALS=0")
    if report["live"] is not None:
        live = report["live"]
        for label, key in (
            ("PUBLIC_COMPOSITE_IMAGE", "public_composite_image_frontier"),
            ("PUBLIC_LEFT_FACTOR_ZERO", "public_left_factor_zero_frontier"),
            ("PUBLIC_GENERATOR_ZERO", "public_generator_zero_frontier"),
        ):
            print(prefix + label + "_PROPOSALS=" + str(live[key]["proposal_count"]))
        print(prefix + "EXISTING_COMPOSITE_RULE_PROPOSALS=" + str(
            live["existing_composite_image_rule_candidate_count"]
        ))
        print(prefix + "LEFT_FACTOR_RULE=" + str(live["left_factor_rule_name"]))
        print(prefix + "SOURCE_GENERATOR_TYPE=" + live["source_generator_type"])
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
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

## `tests/test_audit.py`（全文）

```python
"""Pure trust, git lineage and Toda source contracts for R3-R7-R8."""
from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from phase174_r3_r7_r8_composite_image_gap.audit import (
    BASE_HEAD, REVIEWED_R7_HEAD, REVIEWED_PREFIX, EXPECTED_R7,
    SOURCE_BLOBS, TODA_CLAUSES, accepts_blob, blob_sha,
    describe_candidate_options, reviewed_head_lineage,
    validate_r7_evidence, verify_toda_source,
)


def sample_r7() -> dict:
    return {
        "phase": "174-R3-R7-R7",
        "gate": "PASS_ISOLATED_COMPOSITE_ZERO_CHILDREN_PENDING",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "live": {
            "isolated_generator_zero_candidate_count": 1,
            "public_composite_image_frontier": {"proposal_count": 0},
            "public_left_factor_zero_frontier": {"proposal_count": 1},
            "public_generator_zero_frontier": {"proposal_count": 0},
            "candidate_from_toda_text_is_not_evidence": True,
            "public_provider_unchanged": True,
            "new_verified_steps": 0,
        },
    }


def test_accepts_r7_certified_live_report_without_certifying_new_proof() -> None:
    result = validate_r7_evidence(sample_r7())
    assert result["observed_counts"] == EXPECTED_R7
    assert result["observed_counts"]["public_composite_image_frontier"] == 0


@pytest.mark.parametrize("wrong", (
    "phase", "gate", "given", "production", "provider", "completion",
))
def test_invalid_prior_gate_or_proof_mutation_is_rejected(wrong: str) -> None:
    report = sample_r7()
    if wrong == "phase":
        report["phase"] = "174-R3-R7-R6"
    elif wrong == "gate":
        report["gate"] = "PASS_PREFLIGHT"
    elif wrong == "given":
        report["new_group_given"] = 1
    elif wrong == "production":
        report["new_production_inference_rules"] = 1
    elif wrong == "provider":
        report["public_provider_changed"] = True
    else:
        report["completion_claimed"] = True
    with pytest.raises(RuntimeError):
        validate_r7_evidence(report)


@pytest.mark.parametrize("key,count", (
    ("isolated_generator_zero_candidate_count", 0),
    ("public_composite_image_frontier", 1),
    ("public_left_factor_zero_frontier", 0),
    ("public_generator_zero_frontier", 1),
))
def test_prior_live_counts_cannot_be_fabricated(key: str, count: int) -> None:
    report = sample_r7()
    if key == "isolated_generator_zero_candidate_count":
        report["live"][key] = count
    else:
        report["live"][key]["proposal_count"] = count
    with pytest.raises(RuntimeError):
        validate_r7_evidence(report)


@pytest.mark.parametrize("key,value", (
    ("candidate_from_toda_text_is_not_evidence", False),
    ("public_provider_unchanged", False),
    ("new_verified_steps", 1),
))
def test_prior_candidate_must_remain_unproved(key: str, value: object) -> None:
    report = sample_r7()
    report["live"][key] = value
    with pytest.raises(RuntimeError):
        validate_r7_evidence(report)


def test_reviewed_git_lineage_accepts_only_previous_r7_commit() -> None:
    assert reviewed_head_lineage(BASE_HEAD, BASE_HEAD, (), ()) == "REVIEWED_BASE"
    assert reviewed_head_lineage(
        REVIEWED_R7_HEAD, REVIEWED_R7_HEAD,
        (REVIEWED_R7_HEAD,),
        (REVIEWED_PREFIX + "audit.py",),
    ) == "REVIEWED_R7_ONLY_SUCCESSOR"


@pytest.mark.parametrize("local,remote,commits,paths", (
    (BASE_HEAD, REVIEWED_R7_HEAD, (), ()),
    ("a" * 40, "a" * 40, ("a" * 40,), (REVIEWED_PREFIX + "audit.py",)),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (), (REVIEWED_PREFIX + "audit.py",)),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (REVIEWED_R7_HEAD,), ("proof.py",)),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (REVIEWED_R7_HEAD,), ()),
    (REVIEWED_R7_HEAD, REVIEWED_R7_HEAD, (BASE_HEAD, REVIEWED_R7_HEAD),
     (REVIEWED_PREFIX + "audit.py",)),
))
def test_unreviewed_or_mismatched_lineage_rejected(
    local: str, remote: str, commits: tuple[str, ...], paths: tuple[str, ...],
) -> None:
    with pytest.raises(RuntimeError):
        reviewed_head_lineage(local, remote, commits, paths)


def test_blob_guard_normalizes_newlines_only() -> None:
    source = b"source\nclaim\n"
    expected = blob_sha(source)
    assert accepts_blob(source, expected)
    assert accepts_blob(b"source\r\nclaim\r\n", expected)
    assert not accepts_blob(b"source\nfalse\n", expected)


def test_toda_transcription_source_order_and_independent_claims(tmp_path: Path) -> None:
    file = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    file.parent.mkdir(parents=True)
    file.write_text(
        "\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_CLAUSES["general_nu_eta_zero"] + "\n"
        + TODA_CLAUSES["generator_suspension_composite"] + "\n"
        + TODA_CLAUSES["whole_suspension_zero_conclusion"] + "\n"
        + "\\qed\n", encoding="utf-8",
    )
    result = verify_toda_source(tmp_path)
    assert result["general_formula_is_not_a_certified_step"] is True
    assert result["derived_generator_image_not_given"] is True


def test_toda_transcription_rejects_wrong_order(tmp_path: Path) -> None:
    file = tmp_path / "sources" / "toda" / "Toda_05_2.tex"
    file.parent.mkdir(parents=True)
    file.write_text(
        "\\begin{proposition}\\label{prop:5.9}\n"
        + TODA_CLAUSES["whole_suspension_zero_conclusion"] + "\n"
        + TODA_CLAUSES["general_nu_eta_zero"] + "\n"
        + TODA_CLAUSES["generator_suspension_composite"] + "\n"
        + "\\qed\n", encoding="utf-8",
    )
    with pytest.raises(RuntimeError):
        verify_toda_source(tmp_path)


def test_describes_composite_expansions_without_proof_promotion() -> None:
    data = describe_candidate_options((
        SimpleNamespace(rule=SimpleNamespace(name="generic composition"),
                        subgoals=("factor one", "factor two")),
    ))
    assert len(data) == 1
    assert data[0]["rule"] == "generic composition"
    assert data[0]["child_count"] == 2
    assert [child["repr"] for child in data[0]["children"]] == [
        "'factor one'", "'factor two'",
    ]


def test_rejects_bad_proposal_shapes() -> None:
    with pytest.raises(TypeError):
        describe_candidate_options([])
    with pytest.raises(TypeError):
        describe_candidate_options((SimpleNamespace(subgoals=[]),))


def test_no_production_mutation_in_audit_source() -> None:
    script = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(script.read_text(encoding="utf-8"))
    function_names = {
        node.name for node in tree.body if isinstance(node, ast.FunctionDef)
    }
    assert "inspect_source_screened_frontier" in function_names
    assert "validate_r7_evidence" in function_names
    assert not {"install", "patch", "register_given", "modify_production"} & function_names
    assert len(SOURCE_BLOBS) == 12

def test_pinned_sha1_contract_uses_full_40_character_git_blob_hashes() -> None:
    """Prevent the 39-character pinned generic-isomorphism SHA regression."""
    assert all(
        isinstance(sha, str)
        and len(sha) == 40
        and all(letter in "0123456789abcdef" for letter in sha)
        for sha in SOURCE_BLOBS.values()
    )
    assert (
        SOURCE_BLOBS["phase165_r14_r6_generic_iso.py"]
        == "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7"
    )
```

## `run.ps1`（全文）

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PreviousPythonPath = $env:PYTHONPATH
$PreviousNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Isolate same-basename test modules between Phase directories.
    # Retain prepend mode for older file/directory import-name collisions.
    $Groups = @(
        @{ Name = 'R8'; Paths = @(
            '.\phase174_r3_r7_r8_composite_image_gap\tests\test_audit.py'
        ) },
        @{ Name = 'R7'; Paths = @(
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_rule.py',
            '.\phase174_r3_r7_r7_composite_zero_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R6'; Paths = @(
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_rule.py',
            '.\phase174_r3_r7_r6_cyclic_generator_zero_image\tests\test_audit.py'
        ) },
        @{ Name = 'R5'; Paths = @(
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py',
            '.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_audit.py'
        ) },
        @{ Name = 'R4'; Paths = @(
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_audit.py',
            '.\phase174_r3_r7_r4_delta_surjectivity_audit\tests\test_r4_runner_split.py'
        ) },
        @{ Name = 'R3'; Paths = @(
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_rule.py',
            '.\phase174_r3_r7_r3_ehp_zero_rule\tests\test_audit.py'
        ) },
        @{ Name = 'MATH_REGRESSION'; Paths = @(
            '.\phase165_r12_r11_prop42_unified\tests\test_phase165_r12_r11_prop42_unified.py',
            '.\phase165_r12_r12_ehp_consequences\tests\test_phase165_r12_r12_ehp_consequences.py',
            '.\phase165_r14_r9_ehp_exactness\test_phase165_r14_r9_ehp_exactness.py'
        ) }
    )

    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Focused test file missing: $TestPath"
            }
        }
    }

    Write-Output 'PHASE174_R3R7R8_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R8_PYTEST_GROUP=$($Group.Name)"
        $TestPaths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @TestPaths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R8 $($Group.Name) focused pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R8_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r8_composite_image_gap.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r8_composite_image_gap.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R8 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PreviousPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PreviousNoBytecode
    Pop-Location
}
```

## `R8R1_FIX_JA.md`（全文）

```markdown
# Phase 174 R3-R7-R8R1 Source Guard 修正

- 原因: `phase174_r3_r7_r8_composite_image_gap/audit.py` の `SOURCE_BLOBS` における `phase165_r14_r6_generic_iso.py` の SHA が39文字で、末尾の `7` が欠落していた。
- GitHub develop HEAD 確認時点: `95f37f2020a728b4951b8d26506059a8c54a685f`。
- GitHub の同ファイル SHA: `8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7`。
- 変更対象: `audit.py` の定数 `SOURCE_BLOBS`（該当1項目）、`tests/test_audit.py` の末尾に新規テスト関数を追加。
- 変更しないもの: 本体ソース、他の SHA、Git HEAD の受理条件、公開 Proof Search、GIVEN、Renderer、Web、共通5文書。
- 限定 pytest: `python -B -m pytest -q --import-mode=prepend -p no:cacheprovider phase174_r3_r7_r8_composite_image_gap/tests/test_audit.py`。`run.ps1` が R8 と旧 Phase のテストを別プロセスで行う。
- 完了条件: R8・回帰限定 pytest と Source Guard、DryRun、本実行が PASS、監査 JSON が生成される。
- R9 との境界: 今回は出典ガードの転記ミス修正のみ。証明探索の一般規則追加は行わない。
```
