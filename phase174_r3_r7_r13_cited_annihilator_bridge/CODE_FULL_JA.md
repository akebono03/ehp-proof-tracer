# Phase 174 R3-R7-R13 変更コード全文

R13 の変更は新規ディレクトリ内のファイルだけです。既存の production files は変更しません。各ファイルは import を含む全文であり、関数の省略はありません。

## 変更ファイル一覧

- `registry.py`: 文献マニフェスト照合と隔離された一般命題 GIVEN 登録
- `audit.py`: Source Guard と独立 ProofStep の検証
- `tests/test_registry.py`: 全テスト
- `tests/test_audit.py`: 全テスト
- `run.ps1`: DryRun と本実行
- `__init__.py`, `README.md`, `AUDIT_PLAN_JA.md`

## 全文

### `registry.py`

```python
"""Isolated, source-checked Toda (5.9) bridge; not installed in production.

Only the general published n>=6 annihilator is a source GIVEN. The n=6
relation is a distinct INFERENCE goal, never a source assertion or direct GIVEN.
"""
from __future__ import annotations

import json
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, TODA_CLAUSE, reviewed_toda59_annihilator_schema,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "phase163_r4_r94_output" / "manifest.json"
REF_ID = "isolated:toda:(5.9):nu_eta_general"
ASSERTION_ID = "isolated:toda:(5.9):nu_eta_general:statement"
SOURCE_REFERENCE_ID = "toda:(5.9)"


def reviewed_toda59_source_position(manifest_path: Path = MANIFEST) -> int:
    """Use the reviewed adopted source-order record, never guess a print rank."""
    document = json.loads(Path(manifest_path).read_text(encoding="utf-8-sig"))
    if (document.get("mode") != "ORDERED_SOURCE_ONLY_MANIFEST"
            or document.get("publication_order_scope")
            != "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION"):
        raise RuntimeError("Unexpected source-order manifest metadata")
    rows = tuple(
        x for x in document.get("assertions", ())
        if x.get("reference_id") == SOURCE_REFERENCE_ID
    )
    if len(rows) != 1:
        raise RuntimeError("Toda (5.9) must have exactly one position record")
    record = rows[0]
    pos = record.get("publication_position")
    if (type(pos) is not int or pos <= 0
            or record.get("source_file") != "Toda_05_2.tex"
            or record.get("chapter") != 5
            or record.get("review_needed") is not False
            or TODA_CLAUSE not in record.get("source_text", "")):
        raise RuntimeError("Unreviewed or incorrect Toda (5.9) position")
    return pos


def build_isolated_toda59_annihilator_bridge(
    source_path: Path | None = None,
    manifest_path: Path = MANIFEST,
) -> RegistryBridgeResult:
    """Register exactly one typed general law, with its cited source identity."""
    from phase174_r3_r7_r12_toda59_annihilator_source.source import TODA_SOURCE

    path = TODA_SOURCE if source_path is None else Path(source_path)
    schema = reviewed_toda59_annihilator_schema(path)
    position = reviewed_toda59_source_position(manifest_path)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REF_ID,
        kind=ReferenceKind.EQUATION,
        locator="(5.9)",
        source_id="sources/toda/Toda_05_2.tex (adopted; printed edition unchecked)",
        publication_position=position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REF_ID,
        kind=AssertionKind.STATEMENT,
        content=schema,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope="nu_n composed eta_(n+3) = 0, n>=6",
    ))
    step = ProofStep(
        conclusion=schema,
        premises=(),
        rule=ProofRule.GIVEN,
        inference_rule=InferenceRule(
            name="Cited general annihilator source (5.9)",
            literature_reference=LiteratureReference(
                label="Toda (5.9)", locator="(5.9)",
            ),
        ),
    )
    return RegistryBridgeResult(
        registry=registry, records=(),
        proof_links=(ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )


def join_isolated_source_bridge(
    existing: RegistryBridgeResult,
    added: RegistryBridgeResult,
) -> RegistryBridgeResult:
    """Build a new in-memory registry; never mutate the public existing bridge."""
    if not isinstance(existing, RegistryBridgeResult) or not isinstance(added, RegistryBridgeResult):
        raise TypeError("Two typed bridges are required")
    if len(added.proof_links) != 1 or added.proof_links[0].assertion_id != ASSERTION_ID:
        raise ValueError("Only one Toda (5.9) source link can be attached")
    link = added.proof_links[0]
    fixed_schema = reviewed_toda59_annihilator_schema()
    try:
        assertion = added.registry.assertion(ASSERTION_ID)
        reference = added.registry.reference(REF_ID)
    except KeyError as exc:
        raise ValueError("Checked Toda (5.9) assertion/reference missing") from exc
    if (link.step is None or link.step.rule is not ProofRule.GIVEN
            or link.step.premises
            or link.step.conclusion != fixed_schema
            or assertion.content != fixed_schema
            or assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or assertion.reference_id != REF_ID
            or reference.locator != "(5.9)"
            or reference.publication_position != reviewed_toda59_source_position()
            or link.step.inference_rule is None
            or link.step.inference_rule.literature_reference is None
            or link.step.inference_rule.literature_reference.locator != "(5.9)"):
        raise ValueError("Only the independently checked cited general source may be joined")
    registry = UnifiedStatementRegistry()
    for bridge in (existing, added):
        for entry in bridge.registry._references.values():
            registry.add_reference(entry)
        for entry in bridge.registry._assertions.values():
            registry.add_assertion(entry)
    return RegistryBridgeResult(
        registry=registry,
        records=existing.records + added.records,
        proof_links=existing.proof_links + added.proof_links,
    )
```

### `audit.py`

```python
"""Phase 174 R3-R7-R13: read-only source registration and local proof-chain audit.

Unlike R12, the independently cited *general* Toda (5.9) law is put into an
isolated typed registry. Its n=6 instance is inferred, never made a GIVEN.
The public shared registry, search providers, and target-group proof are untouched.
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

from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (
    ASSERTION_ID, REF_ID, build_isolated_toda59_annihilator_bridge,
    join_isolated_source_bridge, reviewed_toda59_source_position,
)

ROOT = Path(__file__).resolve().parents[1]
PHASE = "174-R3-R7-R13"
REVIEWED_HEAD = "9a8a3e953fe7d3bc7d8d989188aef15525b3a414"
SOURCE_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "phase163_r4_r94_output/manifest.json": "8f6fc9bdcb28e7eb038d2a01cedcbbbcc2bc2457",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "unified_statement_registry.py": "be220ca9f95f20ef243ec295457912cd5ea99d0b",
    "phase163_r4_registry_bridge.py": "aa76059a51cb1f22d966dc9467b3e35919f51eae",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase165_r52_r9_shared_math.py": "0a06dcb0a721e5a79e866cd96909eeeec69303d6",
    "phase174_r3_r7_r12_toda59_annihilator_source/source.py": "10b03ec879cb6f5ad1ae01f3e8ffa1dd0af6c01f",
    "phase174_r3_r7_r12_toda59_annihilator_source/rule.py": "32a5a2723cc19506695d4423e7ccb331d6f36ae2",
    "phase174_r3_r7_r12_toda59_annihilator_source/audit.py": "db27bcf483c1e7a05b85648eeb5bdb1c0a254ea0",
}


def git(*args: str, cwd: Path = ROOT) -> str:
    result = subprocess.run(
        ("git",) + args, cwd=cwd, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    return result.stdout.strip()


def git_blob_sha(value: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(value)).encode("ascii") + b"\0" + value).hexdigest()


def matches_source_blob(value: bytes, expected: str) -> bool:
    if len(expected) != 40 or any(ch not in "0123456789abcdef" for ch in expected):
        return False
    normalized = value.replace(b"\r\n", b"\n")
    return any(git_blob_sha(v) == expected for v in (
        value, normalized, normalized.replace(b"\n", b"\r\n"),
    ))


def verify_git_and_sources(root: Path = ROOT) -> dict[str, Any]:
    if Path(git("rev-parse", "--show-toplevel", cwd=root)).resolve() != root.resolve():
        raise RuntimeError("Package must be a direct child of repository root")
    if git("branch", "--show-current", cwd=root) != "develop":
        raise RuntimeError("Expected develop branch")
    local = git("rev-parse", "HEAD", cwd=root)
    line = git("ls-remote", "origin", "refs/heads/develop", cwd=root)
    remote = line.split()[0] if line else ""
    if local != remote or local != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed develop HEAD, or local/remote mismatch")
    if git("diff", "--cached", "--name-only", cwd=root):
        raise RuntimeError("Staged changes must be reviewed")
    if git("diff", "--name-only", cwd=root):
        raise RuntimeError("Tracked changes must be reviewed")
    for relative, sha in SOURCE_BLOBS.items():
        file = root / relative
        if not file.is_file() or not matches_source_blob(file.read_bytes(), sha):
            raise RuntimeError("Pinned source changed: " + relative)
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "reviewed_paths": list(SOURCE_BLOBS),
        "untracked": git(
            "status", "--porcelain=v1", "--untracked-files=normal", cwd=root,
        ).splitlines(),
    }


def previous_report_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r12" / "toda59_annihilator.json"


def validate_r12_report(report: dict[str, Any]) -> dict[str, Any]:
    if (report.get("phase") != "174-R3-R7-R12"
            or report.get("gate") != "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED"):
        raise RuntimeError("Completed R12 source-first audit is required")
    if (report.get("new_group_given") != 0
            or report.get("new_production_inference_rules") != 0
            or report.get("public_provider_changed") is not False
            or report.get("completion_claimed") is not False
            or report.get("full_pytest_run") is not False):
        raise RuntimeError("R12 proof trust boundary changed")
    live = report.get("live") or {}
    expected = {
        "independent_source_candidate_count": 1,
        "production_source_given_count": 0,
        "production_cited_specialization_count": 0,
        "new_verified_steps": 0,
    }
    for key, value in expected.items():
        if live.get(key) != value:
            raise RuntimeError("R12 previous evidence changed: " + key)
    if ((live.get("production_left_zero_proposals") or {}).get("proposal_count") != 1
            or live.get("production_left_zero_rule_names") != ["equality symmetry"]
            or live.get("source_as_proof_leaf_created") is not False
            or live.get("public_provider_unchanged") is not True):
        raise RuntimeError("R12 equality-symmetry-only boundary changed")
    return {"gate": report["gate"], "public_source_count": 0}


def inspect_isolated_registration_and_proof() -> dict[str, Any]:
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
        canonical_annihilator_instance, cited_annihilator_specialization_rule,
        expand_cited_annihilator_specialization,
    )
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        CitedFamilyAnnihilator,
    )
    from proof import ProofRule, ProofStep, find_inference_matches_for_rule
    from unified_statement_registry import AssertionOrigin

    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    public = build_shared_typed_bridge()
    public_screened = screen_independent_sources_for_derived_goal(public, goal=target)
    public_source_steps = tuple(
        link.step for link in public_screened.proof_links
        if isinstance(link.step, ProofStep)
        and isinstance(link.step.conclusion, CitedFamilyAnnihilator)
    )
    if public_source_steps:
        raise RuntimeError("Source already registered publicly: R13 assumptions changed")

    cited = build_isolated_toda59_annihilator_bridge()
    combined = join_isolated_source_bridge(public, cited)
    screened = screen_independent_sources_for_derived_goal(combined, goal=target)
    fixed_links = tuple(
        link for link in screened.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and isinstance(link.step.conclusion, CitedFamilyAnnihilator)
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and screened.registry.assertion(link.assertion_id).content == link.step.conclusion
        and screened.registry.reference(
            screened.registry.assertion(link.assertion_id).reference_id
        ).publication_position == reviewed_toda59_source_position()
    )
    if len(fixed_links) != 1 or fixed_links[0].assertion_id != ASSERTION_ID:
        raise RuntimeError("Exactly one independently screened cited general law is required")
    cited_step = fixed_links[0].step
    schema = cited_step.conclusion
    instance = canonical_annihilator_instance(schema, 6)
    if instance is None:
        raise RuntimeError("Typed n=6 annihilator instance unavailable")
    if cited_step.conclusion == instance or cited_step.conclusion == target:
        raise RuntimeError("Source schema may not be a concrete target result")

    proposals = expand_cited_annihilator_specialization(instance, (schema,))
    if len(proposals) != 1 or proposals[0].subgoals != (schema,):
        raise RuntimeError("R12 cited specialization goal has changed")
    rule = cited_annihilator_specialization_rule(instance, schema)
    matches = find_inference_matches_for_rule(rule, (cited_step,))
    if len(matches) != 1:
        raise RuntimeError("Cited premise failed typed inference matching")
    inferred = derive_inference_proof_step(matches[0])
    if (inferred.rule is not ProofRule.INFERENCE
            or inferred.conclusion != instance
            or inferred.premises != (cited_step,)
            or inferred.inference_rule is not rule):
        raise RuntimeError("Provenance or inference ancestry was lost")

    original_provider = shared_expansion_provider(public_screened, proof_target=target)
    public_options = tuple(original_provider(instance))
    public_names = [getattr(x.rule, "name", "") for x in public_options]
    if public_names != ["equality symmetry"]:
        raise RuntimeError("Public equality symmetry frontier unexpectedly changed")
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if isinstance(link.step, ProofStep) and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and link.step.conclusion == screened.registry.assertion(link.assertion_id).content
    )

    def isolated_annihilator_provider(goal):
        return expand_cited_annihilator_specialization(goal, available)

    isolated_provider = shared_expansion_provider(
        screened, extra_providers=(isolated_annihilator_provider,), proof_target=target,
    )
    combined_options = tuple(isolated_provider(instance))
    names = [getattr(x.rule, "name", "") for x in combined_options]
    if (names.count(rule.name) != 1
            or len(combined_options) < len(public_options) + 1):
        raise RuntimeError("Isolated general source not exposed as a distinct typed GoalExpansion")
    return {
        "isolated_general_source_screened_count": len(fixed_links),
        "isolated_general_source_reference": REF_ID,
        "isolated_general_source_position": reviewed_toda59_source_position(),
        "printed_edition_independently_verified": False,
        "isolated_n6_inference_count": len(matches),
        "isolated_n6_inference_rule": inferred.inference_rule.name,
        "isolated_n6_inference_has_cited_parent": inferred.premises == (cited_step,),
        "isolated_source_type": type(schema).__name__,
        "isolated_n6_conclusion_type": type(instance).__name__,
        "public_general_source_given_count": len(public_source_steps),
        "public_n6_goal_proposal_count": len(public_options),
        "public_n6_goal_proposal_rule_names": public_names,
        "isolated_n6_goal_proposal_count": len(combined_options),
        "isolated_n6_goal_proposal_rule_names": names,
        "production_files_changed": False,
        "public_provider_unchanged": True,
        "root_proof_completed": False,
    }


def output_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    return base / "EHPProofTracerAudit" / "phase174_r3_r7_r13" / "cited_annihilator_bridge.json"


def make_report(*, dry_run: bool, root: Path = ROOT) -> dict[str, Any]:
    git_state = verify_git_and_sources(root)
    manifest_position = reviewed_toda59_source_position(root / "phase163_r4_r94_output" / "manifest.json")
    if manifest_position <= 0:
        raise RuntimeError("Source order must be positive")
    from phase174_r3_r7_r12_toda59_annihilator_source.source import (
        verify_toda59_annihilator_text,
    )
    source = verify_toda59_annihilator_text(root / "sources/toda/Toda_05_2.tex")
    path = previous_report_path()
    if not path.is_file():
        raise RuntimeError("Certified R12 JSON report is required")
    previous = validate_r12_report(json.loads(path.read_text(encoding="utf-8-sig")))
    live = None if dry_run else inspect_isolated_registration_and_proof()
    return {
        "phase": PHASE,
        "mode": "PREFLIGHT" if dry_run else "READ_ONLY_ISOLATED_REGISTRY_INFERENCE",
        "git_state": git_state,
        "source_review": source,
        "source_order_position": manifest_position,
        "prior_evidence": previous,
        "live": live,
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "new_production_source_given": 0,
        "new_isolated_general_source_given": 0 if dry_run else 1,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "gate": "PASS_PREFLIGHT" if dry_run else "PASS_ISOLATED_CITED_SOURCE_INFERENCE_PUBLIC_UNCHANGED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = make_report(dry_run=args.dry_run)
    destination = output_path()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    prefix = "PHASE174_R3R7R13_"
    print(prefix + "LOCAL_HEAD=" + report["git_state"]["local_head"])
    print(prefix + "REMOTE_HEAD=" + report["git_state"]["remote_head"])
    print(prefix + "SOURCE_GUARD=PASS")
    print(prefix + "TODA59_SOURCE_ORDER_POSITION=" + str(report["source_order_position"]))
    if report["live"] is not None:
        live = report["live"]
        for name, key in (
            ("ISOLATED_CITED_SOURCE_GIVENS", "isolated_general_source_screened_count"),
            ("ISOLATED_N6_INFERENCE_MATCHES", "isolated_n6_inference_count"),
            ("PUBLIC_SOURCE_GIVENS", "public_general_source_given_count"),
            ("PUBLIC_LEFT_ZERO_PROPOSALS", "public_n6_goal_proposal_count"),
            ("ISOLATED_LEFT_ZERO_PROPOSALS", "isolated_n6_goal_proposal_count"),
        ):
            print(prefix + name + "=" + str(live[key]))
        print(prefix + "ISOLATED_N6_INFERENCE_HAS_CITED_PARENT=" + str(
            live["isolated_n6_inference_has_cited_parent"]
        ))
        print(prefix + "PUBLIC_PROVIDER_UNCHANGED=True")
    print(prefix + "NEW_GROUP_GIVEN=0")
    print(prefix + "NEW_PRODUCTION_RULES=0")
    print(prefix + "NEW_PRODUCTION_SOURCE_GIVEN=0")
    print(prefix + "FULL_PYTEST=False")
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + report["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `tests/test_registry.py`

```python
"""R13 cited source registration, screening and inference provenance tests."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    canonical_annihilator_instance, cited_annihilator_specialization_rule,
    expand_cited_annihilator_specialization,
)
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator, TODA_CLAUSE,
)
from phase174_r3_r7_r13_cited_annihilator_bridge.registry import (
    ASSERTION_ID, REF_ID, build_isolated_toda59_annihilator_bridge,
    join_isolated_source_bridge, reviewed_toda59_source_position,
)
from proof import ProofRule, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin, UnifiedStatementRegistry


def manifest_fixture(tmp_path: Path, *, position: int = 9300, clause: str = TODA_CLAUSE) -> Path:
    path = tmp_path / "manifest.json"
    path.write_text(json.dumps({
        "mode": "ORDERED_SOURCE_ONLY_MANIFEST",
        "publication_order_scope": "SOURCE_TEX_ORDER_NOT_ORIGINAL_EDITION",
        "assertions": [{
            "reference_id": "toda:(5.9)",
            "source_file": "Toda_05_2.tex",
            "chapter": 5,
            "review_needed": False,
            "publication_position": position,
            "source_text": "\\begin{equation} " + clause + " \\end{equation}",
        }],
    }), encoding="utf-8")
    return path


def test_manifest_source_order_is_grounded_not_an_original_edition_rank(tmp_path: Path) -> None:
    assert reviewed_toda59_source_position(manifest_fixture(tmp_path)) == 9300


@pytest.mark.parametrize("change", ("wrong_clause", "no_position", "unreviewed", "duplicate", "wrong_scope"))
def test_manifest_without_exact_reviewed_unique_clause_fails_closed(
    tmp_path: Path, change: str,
) -> None:
    path = manifest_fixture(tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if change == "wrong_clause":
        data["assertions"][0]["source_text"] = "different theorem"
    elif change == "no_position":
        data["assertions"][0]["publication_position"] = None
    elif change == "unreviewed":
        data["assertions"][0]["review_needed"] = True
    elif change == "duplicate":
        data["assertions"].append(dict(data["assertions"][0]))
    elif change == "wrong_scope":
        data["publication_order_scope"] = "PRINTED_ORIGINAL_EDITION"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(RuntimeError):
        reviewed_toda59_source_position(path)


def test_isolated_source_bridge_has_only_one_general_cited_given() -> None:
    bridge = build_isolated_toda59_annihilator_bridge()
    assert isinstance(bridge, RegistryBridgeResult)
    assert len(bridge.proof_links) == 1
    link = bridge.proof_links[0]
    assert link.assertion_id == ASSERTION_ID
    assert link.step.rule is ProofRule.GIVEN
    assert link.step.premises == ()
    assert isinstance(link.step.conclusion, CitedFamilyAnnihilator)
    entry = bridge.registry.assertion(ASSERTION_ID)
    reference = bridge.registry.reference(REF_ID)
    assert entry.content == link.step.conclusion
    assert entry.origin is AssertionOrigin.FIXED_STATEMENT
    assert reference.publication_position == reviewed_toda59_source_position()
    assert reference.locator == "(5.9)"
    assert link.step.inference_rule.literature_reference.locator == "(5.9)"


def test_source_screening_retains_cited_general_schema_but_not_instance_as_given() -> None:
    target = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(
        build_isolated_toda59_annihilator_bridge(), goal=target,
    )
    assert len(screened.proof_links) == 1
    cited = screened.proof_links[0].step
    goal = canonical_annihilator_instance(cited.conclusion, 6)
    assert goal is not None
    assert goal != target
    assert goal != cited.conclusion
    assert all(link.step.conclusion != goal for link in screened.proof_links)
    expansions = expand_cited_annihilator_specialization(goal, (cited.conclusion,))
    assert len(expansions) == 1
    assert expansions[0].subgoals == (cited.conclusion,)


def test_proved_source_ancestor_creates_real_n6_inference_not_given() -> None:
    bridge = build_isolated_toda59_annihilator_bridge()
    cited = bridge.proof_links[0].step
    goal = canonical_annihilator_instance(cited.conclusion, 6)
    assert goal is not None
    inference = cited_annihilator_specialization_rule(goal, cited.conclusion)
    matches = find_inference_matches_for_rule(inference, (cited,))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (cited,)
    assert step.inference_rule is inference
    assert step.conclusion != TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))


def test_missing_cited_given_cannot_close_instance() -> None:
    bridge = build_isolated_toda59_annihilator_bridge()
    given = bridge.proof_links[0].step
    goal = canonical_annihilator_instance(given.conclusion, 6)
    rule = cited_annihilator_specialization_rule(goal, given.conclusion)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert expand_cited_annihilator_specialization(goal, ()) == ()


def test_join_builds_fresh_registry_leaves_input_unchanged() -> None:
    existing = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    cited = build_isolated_toda59_annihilator_bridge()
    joined = join_isolated_source_bridge(existing, cited)
    assert joined.registry is not existing.registry
    assert len(existing.registry._references) == 0
    assert len(existing.registry._assertions) == 0
    assert len(joined.proof_links) == 1
    assert joined.registry.assertion(ASSERTION_ID).content == cited.proof_links[0].step.conclusion


def test_join_rejects_duplicate_cited_source_registration() -> None:
    source = build_isolated_toda59_annihilator_bridge()
    with pytest.raises(ValueError, match="duplicate"):
        join_isolated_source_bridge(source, source)


def test_join_rejects_invalid_or_missing_source_links() -> None:
    existing = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    with pytest.raises(ValueError):
        join_isolated_source_bridge(existing, existing)
    with pytest.raises(TypeError):
        join_isolated_source_bridge(object(), existing)
```

### `tests/test_audit.py`

```python
"""R13 audit contracts, source guards and no-public-wiring checks."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase174_r3_r7_r13_cited_annihilator_bridge.audit import (
    REVIEWED_HEAD, SOURCE_BLOBS, git_blob_sha, matches_source_blob,
    validate_r12_report,
)


def sample_r12() -> dict:
    return {
        "phase": "174-R3-R7-R12",
        "gate": "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED",
        "new_group_given": 0,
        "new_production_inference_rules": 0,
        "public_provider_changed": False,
        "completion_claimed": False,
        "full_pytest_run": False,
        "live": {
            "independent_source_candidate_count": 1,
            "production_source_given_count": 0,
            "production_cited_specialization_count": 0,
            "production_left_zero_proposals": {"proposal_count": 1},
            "production_left_zero_rule_names": ["equality symmetry"],
            "source_as_proof_leaf_created": False,
            "new_verified_steps": 0,
            "public_provider_unchanged": True,
        },
    }


def test_valid_r12_report_is_a_gate_not_cited_source() -> None:
    result = validate_r12_report(sample_r12())
    assert result["gate"] == "PASS_ISOLATED_CITED_ANNIHILATOR_SOURCE_UNWIRED"
    assert result["public_source_count"] == 0


@pytest.mark.parametrize("field,bad", (
    ("gate", "PASS_PREFLIGHT"), ("new_group_given", 1),
    ("new_production_inference_rules", 1), ("public_provider_changed", True),
    ("completion_claimed", True), ("full_pytest_run", True),
))
def test_changed_r12_trust_boundary_fails_closed(field: str, bad: object) -> None:
    report = sample_r12()
    report[field] = bad
    with pytest.raises(RuntimeError):
        validate_r12_report(report)


@pytest.mark.parametrize("field,bad", (
    ("independent_source_candidate_count", 0),
    ("production_source_given_count", 1),
    ("production_cited_specialization_count", 1),
    ("new_verified_steps", 1),
    ("source_as_proof_leaf_created", True),
    ("public_provider_unchanged", False),
    ("production_left_zero_rule_names", ["cited Toda (5.9)"]),
))
def test_unproved_r12_live_claims_cannot_be_promoted(field: str, bad: object) -> None:
    report = sample_r12()
    report["live"][field] = bad
    with pytest.raises(RuntimeError):
        validate_r12_report(report)


def test_unexpected_left_zero_candidate_count_rejected() -> None:
    report = sample_r12()
    report["live"]["production_left_zero_proposals"]["proposal_count"] = 2
    with pytest.raises(RuntimeError):
        validate_r12_report(report)


def test_40_character_blob_guard_with_crlf_and_mutation() -> None:
    value = b"one\ntwo\n"
    sha = git_blob_sha(value)
    assert matches_source_blob(value, sha)
    assert matches_source_blob(b"one\r\ntwo\r\n", sha)
    assert not matches_source_blob(value, sha[:-1])
    assert not matches_source_blob(value + b"modified", sha)
    assert all(len(sha) == 40 for sha in SOURCE_BLOBS.values())
    assert len(REVIEWED_HEAD) == 40


def test_registry_does_not_import_narrative_or_public_patcher() -> None:
    registry_file = Path(__file__).resolve().parents[1] / "registry.py"
    tree = ast.parse(registry_file.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"build_isolated_toda59_annihilator_bridge", "reviewed_toda59_source_position", "join_isolated_source_bridge"} <= functions
    assert not {"patch", "install", "write_production"} & functions
    names = registry_file.read_text(encoding="utf-8")
    assert "TodaPrimaryGroupZeroStatement" not in names
    assert "pi_12" not in names
    assert "ProofRule.GIVEN" in names


def test_audit_contains_no_production_installer() -> None:
    audit_file = Path(__file__).resolve().parents[1] / "audit.py"
    tree = ast.parse(audit_file.read_text(encoding="utf-8"))
    functions = {node.name for node in tree.body if isinstance(node, ast.FunctionDef)}
    assert {"verify_git_and_sources", "validate_r12_report", "inspect_isolated_registration_and_proof"} <= functions
    assert not {"install", "patch", "mutate_production", "register_group_given"} & functions
```

### `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$PriorPythonPath = $env:PYTHONPATH
$PriorNoBytecode = $env:PYTHONDONTWRITEBYTECODE

Push-Location -LiteralPath $RepoRoot
try {
    $env:PYTHONPATH = $RepoRoot
    $env:PYTHONDONTWRITEBYTECODE = '1'

    # Each Phase group runs in a separate Python process because older test
    # directories contain repeated test_audit.py and test_rule.py basenames.
    $Groups = @(
        @{ Name = 'R13'; Paths = @(
            '.\phase174_r3_r7_r13_cited_annihilator_bridge\tests\test_registry.py',
            '.\phase174_r3_r7_r13_cited_annihilator_bridge\tests\test_audit.py'
        ) },
        @{ Name = 'R12'; Paths = @(
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_source.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_rule.py',
            '.\phase174_r3_r7_r12_toda59_annihilator_source\tests\test_audit.py'
        ) },
        @{ Name = 'R11'; Paths = @(
            '.\phase174_r3_r7_r11_canonical_fixture_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R10'; Paths = @(
            '.\phase174_r3_r7_r10_cited_family_gap_audit\tests\test_audit.py'
        ) },
        @{ Name = 'R9'; Paths = @(
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_rule.py',
            '.\phase174_r3_r7_r9_composition_associativity\tests\test_audit.py'
        ) },
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
        ) },
        @{ Name = 'FAMILY_REGRESSION'; Paths = @(
            '.\phase169_r10d2_general_family_definition\tests\test_r10d2_general_family.py'
        ) }
    )

    foreach ($Group in $Groups) {
        foreach ($TestPath in $Group.Paths) {
            if (-not (Test-Path -LiteralPath $TestPath)) {
                throw "Missing focused test: $TestPath"
            }
        }
    }
    Write-Output 'PHASE174_R3R7R13_FOCUSED_PYTEST_START'
    foreach ($Group in $Groups) {
        Write-Output "PHASE174_R3R7R13_PYTEST_GROUP=$($Group.Name)"
        $Paths = [string[]]$Group.Paths
        & python -B -m pytest -q --import-mode=prepend -p no:cacheprovider @Paths
        if ($LASTEXITCODE -ne 0) {
            throw "Phase 174 R3-R7-R13 $($Group.Name) pytest failed: $LASTEXITCODE"
        }
    }
    Write-Output 'PHASE174_R3R7R13_FOCUSED_PYTEST=PASS'

    if ($DryRun) {
        & python -B -m phase174_r3_r7_r13_cited_annihilator_bridge.audit --dry-run
    }
    else {
        & python -B -m phase174_r3_r7_r13_cited_annihilator_bridge.audit
    }
    if ($LASTEXITCODE -ne 0) {
        throw "Phase 174 R3-R7-R13 audit failed: $LASTEXITCODE"
    }
}
finally {
    $env:PYTHONPATH = $PriorPythonPath
    $env:PYTHONDONTWRITEBYTECODE = $PriorNoBytecode
    Pop-Location
}
```

### `__init__.py`

```python
"""Phase 174 R3-R7-R13 isolated cited general-annihilator bridge."""
```

### `README.md`

````markdown
# Phase 174 R3-R7-R13 — Isolated Cited Toda (5.9) Bridge

This read-only audit registers the **general** Toda (5.9) ν–η annihilator in a fresh, in-memory, source-qualified `RegistryBridgeResult`. It screens the fixed general law through the project's existing Source-first path and derives the concrete instance with the existing R12 typed inference rule. The production source registry, default proof provider, rendered narrative, and target-group proof are **not modified**.

## Requirements

- Git branch `develop` and the reviewed GitHub HEAD. The script rejects unreviewed source changes.
- Previously completed R12 full audit JSON in `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r12\toda59_annihilator.json`.
- Python, pytest, PowerShell, and the repository's normal dependencies.
- Extract `R13.zip` directly into the repository root.

## Execute

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\R13.zip" -DestinationPath "." -Force
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r13_cited_annihilator_bridge\run.ps1" -DryRun
if ($LASTEXITCODE -ne 0) { throw "R13 DryRun failed" }
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase174_r3_r7_r13_cited_annihilator_bridge\run.ps1"
if ($LASTEXITCODE -ne 0) { throw "R13 audit failed" }
git status -sb
```

Focused tests run in separate pytest processes to avoid identical test-module name collisions. There is no full test suite run within this step.

The full audit report is stored under `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r13\cited_annihilator_bridge.json`.

## Proof boundary

The adopted Toda transcription is checked against the `(5.9)` manifest record and the source text. The manifest's publication position is **only adopted-source order**, not independently verified printed-edition order. The only new fixed assertion is the **general** relation `nu_n o eta_(n+3) = 0` for `n >= 6`, in an isolated bridge. The `n = 6` instance is an inference from this citation-qualified general statement; it is never directly registered as a GIVEN. No public proof completion is claimed.
````

### `AUDIT_PLAN_JA.md`

```markdown
# Phase 174 R3-R7-R13 — 一般消滅関係の独立文献登録と型付き証明監査

## 目的と前提

R12 において Toda (5.9) の一般命題の転写と独立特殊化規則を検証した。しかし、公開 Registry の一般命題 GIVEN は0件、公開の左因子零関係候補1件は等式の対称性のみだった。

今回、採用 TeX `sources/toda/Toda_05_2.tex` の一般関係 `$\nu_n\circ\eta_{n+3}=0\ (n\ge6)$` を、文献マニフェストの `(5.9)` source-order position と照合し、独立した `RegistryBridgeResult` に一般命題だけを出典付き GIVEN として登録する。`$\nu_6\circ\eta_9=0$` は R12 の型付き推論で導き、GIVEN にはしない。

## 変更ファイルと全関数

既存ファイルは一切変更しない。新規ディレクトリ `phase174_r3_r7_r13_cited_annihilator_bridge/` のみ。

- `registry.py`：`reviewed_toda59_source_position()`、`build_isolated_toda59_annihilator_bridge()`、`join_isolated_source_bridge()`。
- `audit.py`：`git()`、`git_blob_sha()`、`matches_source_blob()`、`verify_git_and_sources()`、`previous_report_path()`、`validate_r12_report()`、`inspect_isolated_registration_and_proof()`、`output_path()`、`make_report()`、`main()`。
- `tests/test_registry.py`：`manifest_fixture()` と文献・型付き推論・独立 Registry に関する全テスト。
- `tests/test_audit.py`：`sample_r12()` と前工程・Source Guard・非公開接続に関する全テスト。
- `run.ps1`：限定 pytest の分割実行、DryRun、本監査。
- `README.md`：英語の実行説明。
- `AUDIT_PLAN_JA.md`：本計画。
- `CODE_FULL_JA.md`：import・クラス・関数・テスト・スクリプトの全文。

新規クラスは定義しない。新規関数は上記の各新規ファイルの冒頭 import 群の直後から定義する。

## 証拠の独立性・禁止事項

- Source-first：文献原文、掲載位置、型付き生成元 ID をそれぞれ検査。
- source-order position 9300 は採用テキストの順序であり、原著印刷版の位置は未検証。
- 一般命題のみ Source GIVEN とし、具体的零関係、ImageZero(E)、目標群零の直接 GIVEN を禁止。
- R12 の全監査 JSON を必須とし、DryRun のみの JSON を拒否。
- 出典・HEAD の固定 SHA と改行正規化による Source Guard を維持。
- 独立した Registry のみを構築し、公開 Provider・GIVEN・Narrative・Web を変更しない。
- First Successful Proof Search 方針を維持し、唯一性検査や群専用 Narrative を追加しない。

## テスト・完了条件と次段階の境界

DryRun → 本実行で R13 と R12〜R3・数学/系列の限定回帰テスト、Source Guard を実行する。一般命題の source-screened GIVEN が隔離環境で1件、具体例の検証済み INFERENCE が1件、公開一般命題は0件のまま、という実測を JSON に記録する。**これらは根の完成証明を意味しない。**

次の R14 以降で公開経路への最小接続と、合成零→巡回群の零像→EHP 完全列の公開証明再評価を行う。全体 pytest は Phase 174 終了時にのみ行う。
```

