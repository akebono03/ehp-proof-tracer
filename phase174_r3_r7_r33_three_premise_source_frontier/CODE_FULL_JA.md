# R33 新規コード全文

既存コードは一切変更しない。次の新規ファイル群はリポジトリ直下 `phase174_r3_r7_r33_three_premise_source_frontier/` に追加する。

## `__init__.py` — 全文

```python
"""R33 read-only source-first audit of three lower Delta kernel premises."""
```

## `source_contract.py` — 全文

```python
"""Read-only provenance contract for the three lower-Delta kernel inputs.

Only the order and exact printed clauses are certified here. A printed clause
is not an admitted proof step, and the later printed kernel must not be copied
into any source premise or proof provider.
"""
from __future__ import annotations

from dataclasses import dataclass

PROP58 = r"\begin{proposition}\label{prop:5.8}"
PROP59 = r"\begin{proposition}\label{prop:5.9}"
EQ510 = r"\begin{equation}\label{eq:5.10}"
END_PROPOSITION = r"\end{proposition}"
END_EQUATION = r"\end{equation}"
CODOMAIN_CLAUSE = r"\pi^{5}_{9}=\mathbb Z_2\gen{\nu_{5}\circ\eta_8}"
IMAGE_CLAUSE = r"\Delta(\iota_{11})=\nu_5\circ\eta_8"
DIAGONAL_CLAUSE = r"\pis{n}{S^n} = \z\gen{\iota_n}"
DERIVED_KERNEL = r"\ker\Delta=\gen{2\iota_{11}}"


@dataclass(frozen=True)
class SourceEvidence:
    name: str
    locator: str
    appears_before_prop59: bool
    statement_is_verified_proof_step: bool


def inspect_prior_three_clauses(text: str) -> tuple[SourceEvidence, ...]:
    """Verify order and source interval, never adopt a printed result."""
    if type(text) is not str:
        raise TypeError("Source text must be str")
    for boundary in (PROP58, PROP59, EQ510):
        if text.count(boundary) != 1:
            raise ValueError("Missing or ambiguous source boundary: " + boundary)
    p58 = text.index(PROP58)
    eq = text.index(EQ510)
    p59 = text.index(PROP59)
    if not (p58 < eq < p59):
        raise ValueError("Incorrect provenance order")
    end58 = text.find(END_PROPOSITION, p58)
    endeq = text.find(END_EQUATION, eq)
    if end58 == -1 or endeq == -1 or end58 >= eq or endeq >= p59:
        raise ValueError("Source boundary nesting is invalid")
    before = text[:p58]
    prop = text[p58:end58]
    equation = text[eq:endeq]
    later = text[p59:]
    if before.count(DIAGONAL_CLAUSE) != 1:
        raise ValueError("Earlier diagonal free-cyclic clause not unique")
    if prop.count(CODOMAIN_CLAUSE) != 1:
        raise ValueError("Proposition 5.8 codomain clause missing or ambiguous")
    if equation.count(IMAGE_CLAUSE) != 1:
        raise ValueError("Equation (5.10) generator image missing or ambiguous")
    if DERIVED_KERNEL not in later:
        raise ValueError("Later kernel statement missing; provenance unclear")
    if DERIVED_KERNEL in text[:p59]:
        raise ValueError("Derived kernel appears before the target proof")
    return (
        SourceEvidence("diagonal_domain", "general diagonal relation", True, False),
        SourceEvidence("finite_codomain", "Proposition 5.8", True, False),
        SourceEvidence("delta_generator_image", "equation (5.10)", True, False),
    )


def classify_three_premises(*, domain: bool, codomain: bool, image: bool) -> dict[str, object]:
    """False is a blocker, not a license to insert a direct GIVEN."""
    if any(type(x) is not bool for x in (domain, codomain, image)):
        raise TypeError("Every premise availability flag must be bool")
    evidence = {
        "domain_presentation": domain,
        "codomain_presentation": codomain,
        "signed_generator_image": image,
    }
    return {"premises": evidence, "all_screened": all(evidence.values()),
            "missing": tuple(k for k, v in evidence.items() if not v)}
```

## `audit.py` — 全文

```python
"""R33 read-only audit: independent source and public proof-leaf availability.

This package changes no production provider, no mathematical rule, and no
GIVEN. A cited text, a typed goal, and a verified ProofStep are distinct.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
    classify_three_premises, inspect_prior_three_clauses,
)

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "02f694b27a4239052bfa9d27a116fca6bbbff6b5"
SOURCE = "sources/toda/Toda_05_2.tex"
REVIEWED_SUCCESSOR_DIRS = (
    "phase174_r3_r7_r32_lower_delta_kernel_audit/",
    "phase174_r3_r7_r32r1_reviewed_head_handoff_fix/",
)
GIT_BLOB_PINS = {
    SOURCE: "579661138928499ba04a51327f686d9b971b5314",
    "phase165_r52_r9_shared_math.py": "742451ea67ede314f99246afbb470a5e8a7f008f",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase165_r57_r19_delta_image_backward.py": "c5b3447258f41e15219ead8daeeb17cbb5605b6d",
    "phase174_r3_r7_r18_delta_image_surjectivity/rule.py": "f8da1f6fb7d5fb66feae33b4a4847fbad6891342",
    "phase170_r3_r6_prop58_source.py": "f0223668e60bb9d18f10b0e8721dece79d7e705a",
    "phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py": "bc78a9732230ce4af021bbc9b218a4153d3af96e",
    "phase174_r3_r7_r30_prop27_public_provider_wiring/provider.py": "b54a73a5cb98803c9872973cbf194b0068ba6c8c",
    "phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py": "12487ac30e214facd786f106e8e2934b635e60cf",
}
LOCAL_SHA256_PINS = {
    "phase174_r3_r7_r31_delta_surjectivity_general_audit/audit.py":
        "ab6f81dbbb32c6fd46dfb85c639534f7eff15062e2cc42c58b32f44efc0bc191",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/audit.py":
        "c191d8a9c25007e1d42b4a7faa6898b1d118a3b60f021f2dbb5ec713f0aa7656",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py":
        "c4ff7d4eb1d24569fdb97c87eec9fa4689ff0bc7b224a3e29bbbda2439ca995a",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/run.ps1":
        "6e070729ce6c5ae809be0f564a87372df179ab49ce971f7a3af41efdd0044103",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob_pin(data: bytes, sha: str) -> bool:
    canonical = data.replace(b"\r\n", b"\n")
    return len(sha) == 40 and any(
        git_blob_sha(candidate) == sha
        for candidate in (data, canonical, canonical.replace(b"\n", b"\r\n"))
    )


def canonical_sha256(data: bytes) -> str:
    return hashlib.sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Permit only an exact reviewed tree or successor adding R32 files only."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R33 must be extracted at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R33 requires develop")
    local = git("rev-parse", "HEAD")
    remote_line = git("ls-remote", "origin", "refs/heads/develop")
    remote = remote_line.split()[0] if remote_line else ""
    if not remote:
        raise RuntimeError("Cannot verify current GitHub develop")
    reviewed_additions: tuple[str, ...] = ()
    if remote != BASE_HEAD:
        # Only inspect upstream history; this does not change the working tree.
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("GitHub HEAD changed while fetching")
        ancestor = subprocess.run(
            ("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
            cwd=ROOT, capture_output=True,
        )
        if ancestor.returncode != 0:
            raise RuntimeError("New GitHub history is not a reviewed successor")
        reviewed_additions = tuple(git("diff", "--name-only", BASE_HEAD, remote).splitlines())
        if not reviewed_additions or any(
            not path.startswith(REVIEWED_SUCCESSOR_DIRS) for path in reviewed_additions
        ):
            raise RuntimeError("GitHub changed files outside the reviewed R32-only handoff")
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Local HEAD differs from reviewed local/remote versions")
    if git("diff", "--name-only") or git("diff", "--cached", "--name-only"):
        raise RuntimeError("Unexpected tracked edits; preserve and review manually")
    for path, sha in GIT_BLOB_PINS.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob_pin(file.read_bytes(), sha):
            raise RuntimeError("Reviewed production/source blob differs: " + path)
    for path, sha in LOCAL_SHA256_PINS.items():
        file = ROOT / path
        if not file.is_file() or canonical_sha256(file.read_bytes()) != sha:
            raise RuntimeError("Reviewed R31/R32 package differs: " + path)
    return {
        "local_head": local, "remote_head": remote,
        "reviewed_successor_r32_files": list(reviewed_additions),
        "checked_pinned_github_files": len(GIT_BLOB_PINS),
        "checked_pinned_handoff_files": len(LOCAL_SHA256_PINS),
        "source_guard": "PASS", "r30_r31_r32_preserved": True,
    }


def inspect_registered_frontier() -> dict[str, object]:
    """Read public screens and DB prior without inventing or attaching steps."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import (
        FiniteCyclicGroup, FreeCyclicGroup, TodaDeltaMap,
        TodaPrimaryGroup, TodaPrimaryGroupZeroStatement,
    )
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import (
        exact_prior_database_result, precedes_db_goal,
    )
    from phase174_r3_r7_r32_lower_delta_kernel_audit.kernel_contract import (
        conditional_kernel_premises, generator_has_group_coordinates,
    )
    from proof import ProofRule, Relation, RelationType
    from toda_rules import TodaDeltaImageUpToSignStatement
    from unified_statement_registry import AssertionOrigin

    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    domain = TodaPrimaryGroup(11, 11)
    target = TodaPrimaryGroup(9, 5)
    lower = TodaDeltaMap(domain, target)
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    leaves = tuple(link.step for link in screened.proof_links
                   if link.step is not None and link.step.rule is ProofRule.GIVEN)
    domain_leaves = tuple(step for step in leaves
                          if type(step.conclusion) is Relation
                          and step.conclusion.relation_type is RelationType.EQUALITY
                          and step.conclusion.lhs == domain
                          and type(step.conclusion.rhs) is FreeCyclicGroup)
    target_leaves = tuple(step for step in leaves
                          if type(step.conclusion) is Relation
                          and step.conclusion.relation_type is RelationType.EQUALITY
                          and step.conclusion.lhs == target
                          and type(step.conclusion.rhs) is FiniteCyclicGroup
                          and step.conclusion.rhs.order == 2)
    image_leaves = tuple(step for step in leaves
                         if type(step.conclusion) is TodaDeltaImageUpToSignStatement
                         and step.conclusion.map == lower)
    direct_kernel = tuple(step for step in leaves
                          if type(step.conclusion) is KernelMultipleStatement
                          and step.conclusion.map == lower)
    direct_root = tuple(step for step in leaves if step.conclusion == goal)
    if direct_kernel or direct_root:
        raise RuntimeError("A forbidden direct kernel/root source leaf was exposed")
    all_screened = classify_three_premises(
        domain=len(domain_leaves) == 1,
        codomain=len(target_leaves) == 1,
        image=len(image_leaves) == 1,
    )
    fixed_candidates = tuple(
        a for a in bridge.registry._assertions.values()
        if a.origin is AssertionOrigin.FIXED_STATEMENT
    )
    fixed_group_candidates = tuple(
        a for a in fixed_candidates if type(a.content) is Relation
        and a.content.relation_type is RelationType.EQUALITY
        and a.content.lhs in (domain, target)
    )
    fixed_lower_delta_candidates = tuple(
        a for a in fixed_candidates
        if type(a.content) is TodaDeltaImageUpToSignStatement
        and a.content.map == lower
    )
    db = exact_prior_database_result(5, 4)
    if db is None:
        raise RuntimeError("Previously verified pi_9^5 DB prior is absent")
    db_valid = (type(db) is Relation and db.relation_type is RelationType.EQUALITY
                and db.lhs == target and type(db.rhs) is FiniteCyclicGroup
                and db.rhs.order == 2 and precedes_db_goal(5, 4, 7, 5))
    if not db_valid:
        raise RuntimeError("DB prior has changed or is not strictly earlier")
    db_generator = db.rhs.generator
    # Avoid fake HomotopyElement substitutions: inspect the real typed object.
    accepts_db_generator = generator_has_group_coordinates(db_generator, target)
    generator = HomotopyElement(
        "iota_11", 11, 11, 11, GeneratorSymbol("iota", 11),
    )
    expected_kernel = KernelMultipleStatement(lower, domain, generator, 2)
    synthetic_target = Relation(
        target, FiniteCyclicGroup(2, HomotopyElement(
            "nu_5_eta_8", 9, 9, 5, GeneratorSymbol("nu_eta", 5),
        )), RelationType.EQUALITY,
    )
    synthetic_domain = Relation(
        domain, FreeCyclicGroup(generator), RelationType.EQUALITY,
    )
    synthetic_signed = TodaDeltaImageUpToSignStatement(
        lower, generator, synthetic_target.rhs.generator,
    )
    if conditional_kernel_premises(
        expected_kernel, synthetic_domain, synthetic_target, synthetic_signed,
    ) != (synthetic_domain, synthetic_target, synthetic_signed):
        raise RuntimeError("R32 isolated conditional lemma changed")
    # Never substitute the synthetic representation for an actual DB generator.
    db_pair_accepts_contract = conditional_kernel_premises(
        expected_kernel, synthetic_domain, db, TodaDeltaImageUpToSignStatement(
            lower, generator, db_generator,
        ),
    ) is not None
    return {
        "screened_domain_premises": len(domain_leaves),
        "screened_codomain_premises": len(target_leaves),
        "screened_generator_image_premises": len(image_leaves),
        "screened_completeness": all_screened,
        "registry_fixed_group_candidates": len(fixed_group_candidates),
        "registry_fixed_lower_delta_candidates": len(fixed_lower_delta_candidates),
        "strictly_earlier_db_prior_present": True,
        "db_prior_generator_type": type(db_generator).__name__,
        "r32_contract_accepts_db_generator": accepts_db_generator,
        "r32_contract_accepts_actual_db_relation": db_pair_accepts_contract,
        "db_prior_is_an_independent_literature_citation": False,
        "hypothetical_group_and_map_steps_not_certified": True,
        "kernel_direct_given_inserted": False,
        "root_direct_given_inserted": False,
    }


def report(*, dry_run: bool) -> dict[str, object]:
    git_state = verify_checkout()
    source_text = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    source_facts = inspect_prior_three_clauses(source_text)
    frontier = None if dry_run else inspect_registered_frontier()
    return {
        "phase": "174-R3-R7-R33",
        "git_state": git_state,
        "source_evidence": [vars(x) for x in source_facts],
        "frontier": frontier,
        "new_givens": 0, "new_inference_rules": 0,
        "production_files_changed": 0,
        "kernel_proved": False, "root_complete": False,
        "full_pytest": False,
        "gate": ("PASS_R33_SOURCE_PREFLIGHT_ONLY" if dry_run else
                 "PASS_R33_INDEPENDENT_THREE_PREMISE_FRONTIER_AUDITED_SOURCE_WIRING_PENDING"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = report(dry_run=args.dry_run)
    output_dir = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r33"
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / ("preflight.json" if args.dry_run else "source_frontier.json")
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R33_"
    for key in ("local_head", "remote_head", "source_guard", "r30_r31_r32_preserved"):
        print(p + key.upper() + "=" + str(result["git_state"][key]))
    print(p + "THREE_PRINTED_SOURCES_PRECEDE_PROP59=True")
    if result["frontier"] is not None:
        for key, value in result["frontier"].items():
            if key == "screened_completeness":
                for subkey, subvalue in value.items():
                    if subkey != "premises":
                        print(p + "FRONTIER_" + subkey.upper() + "=" + str(subvalue))
            elif isinstance(value, (bool, int, str)):
                print(p + key.upper() + "=" + str(value))
    print(p + "NEW_GIVENS=0")
    print(p + "NEW_INFERENCE_RULES=0")
    print(p + "KERNEL_PROVED=False")
    print(p + "ROOT_COMPLETE=False")
    print(p + "FULL_PYTEST=False")
    print(p + "REPORT=" + str(path))
    print(p + "GATE=" + result["gate"])
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_source_contract.py` — 全文

```python
"""Pure R33 source contract regression tests (no repository required)."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
    CODOMAIN_CLAUSE, DERIVED_KERNEL, DIAGONAL_CLAUSE, END_EQUATION,
    END_PROPOSITION, EQ510, IMAGE_CLAUSE, PROP58, PROP59,
    classify_three_premises, inspect_prior_three_clauses,
)


def source_fixture() -> str:
    return "\n".join((
        DIAGONAL_CLAUSE, PROP58, CODOMAIN_CLAUSE, END_PROPOSITION,
        EQ510, IMAGE_CLAUSE, END_EQUATION, PROP59, DERIVED_KERNEL,
    ))


def test_source_evidence_is_prior_and_not_a_proof_step() -> None:
    evidence = inspect_prior_three_clauses(source_fixture())
    assert len(evidence) == 3
    assert tuple(x.name for x in evidence) == (
        "diagonal_domain", "finite_codomain", "delta_generator_image",
    )
    assert all(x.appears_before_prop59 for x in evidence)
    assert all(not x.statement_is_verified_proof_step for x in evidence)


@pytest.mark.parametrize("missing", (
    DIAGONAL_CLAUSE, CODOMAIN_CLAUSE, IMAGE_CLAUSE,
    PROP58, PROP59, EQ510, DERIVED_KERNEL,
))
def test_missing_required_text_rejected(missing: str) -> None:
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(source_fixture().replace(missing, "DELETED"))


def test_duplicated_source_statement_rejected() -> None:
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(source_fixture().replace(
            IMAGE_CLAUSE, IMAGE_CLAUSE + "\n" + IMAGE_CLAUSE,
        ))


def test_reversed_provenance_rejected() -> None:
    prior = source_fixture()
    prior = prior.replace(PROP58, "PLACEHOLDER").replace(PROP59, PROP58).replace("PLACEHOLDER", PROP59)
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(prior)


def test_earlier_kernel_conclusion_rejected() -> None:
    prior = source_fixture().replace(PROP58, DERIVED_KERNEL + "\n" + PROP58)
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(prior)


def test_three_independent_premises_are_required() -> None:
    full = classify_three_premises(domain=True, codomain=True, image=True)
    assert full["all_screened"] and full["missing"] == ()
    for key in ("domain", "codomain", "image"):
        flags = {"domain": True, "codomain": True, "image": True}
        flags[key] = False
        result = classify_three_premises(**flags)
        assert not result["all_screened"]
        assert len(result["missing"]) == 1


def test_unknown_proof_availability_is_rejected() -> None:
    with pytest.raises(TypeError):
        classify_three_premises(domain=1, codomain=True, image=True)
    with pytest.raises(TypeError):
        inspect_prior_three_clauses(None)
```

## `tests/test_audit.py` — 全文

```python
"""R33 real-repository source, guard and typed frontier tests."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r7_r33_three_premise_source_frontier.audit import (
    GIT_BLOB_PINS, LOCAL_SHA256_PINS, ROOT, SOURCE,
    canonical_sha256, inspect_registered_frontier, matches_blob_pin,
    report, verify_checkout,
)
from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
    inspect_prior_three_clauses,
)


def test_source_guard_and_all_reviewed_pins() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["r30_r31_r32_preserved"] is True
    assert len(GIT_BLOB_PINS) >= 10
    assert len(LOCAL_SHA256_PINS) == 4


def test_full_adopted_toda_has_independent_prior_clauses() -> None:
    text = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    refs = inspect_prior_three_clauses(text)
    assert len(refs) == 3
    assert all(not value.statement_is_verified_proof_step for value in refs)


def test_source_mutation_is_fail_closed() -> None:
    from phase174_r3_r7_r33_three_premise_source_frontier.source_contract import (
        IMAGE_CLAUSE,
    )
    text = (ROOT / SOURCE).read_text(encoding="utf-8-sig")
    with pytest.raises(ValueError):
        inspect_prior_three_clauses(text.replace(IMAGE_CLAUSE, "INVALID"))


def test_canonical_hash_rejects_arbitrary_changes() -> None:
    content = b"one\ntwo\n"
    assert canonical_sha256(content) == canonical_sha256(content.replace(b"\n", b"\r\n"))
    assert not matches_blob_pin(content, "0" * 40)


def test_screened_frontier_and_db_prior_are_not_proof() -> None:
    frontier = inspect_registered_frontier()
    assert frontier["strictly_earlier_db_prior_present"] is True
    assert frontier["db_prior_is_an_independent_literature_citation"] is False
    assert frontier["hypothetical_group_and_map_steps_not_certified"] is True
    assert frontier["kernel_direct_given_inserted"] is False
    assert frontier["root_direct_given_inserted"] is False
    assert frontier["db_prior_generator_type"]
    assert all(isinstance(frontier[key], int) for key in (
        "screened_domain_premises", "screened_codomain_premises",
        "screened_generator_image_premises",
    ))


def test_preflight_does_not_assert_completion() -> None:
    result = report(dry_run=True)
    assert result["gate"] == "PASS_R33_SOURCE_PREFLIGHT_ONLY"
    assert result["kernel_proved"] is False
    assert result["root_complete"] is False
    assert result["new_givens"] == 0
    assert result["new_inference_rules"] == 0
```

## `run.ps1` — 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r33_three_premise_source_frontier.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R33 Source Guard / DryRun failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R33_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m phase174_r3_r7_r33_three_premise_source_frontier.audit
if ($LASTEXITCODE -ne 0) { throw 'R33 source frontier audit failed' }

$Groups = @(
    @{ Name='R33_SOURCE_CONTRACT'; Files=@('.\phase174_r3_r7_r33_three_premise_source_frontier\tests\test_source_contract.py') },
    @{ Name='R33_REPO_AUDIT'; Files=@('.\phase174_r3_r7_r33_three_premise_source_frontier\tests\test_audit.py') },
    @{ Name='R32_KERNEL_CONTRACT'; Files=@('.\phase174_r3_r7_r32_lower_delta_kernel_audit\tests\test_kernel_contract.py') },
    @{ Name='R18_SURJECTIVITY'; Files=@('.\phase174_r3_r7_r18_delta_image_surjectivity\tests\test_rule.py') },
    @{ Name='R5_HOPF_INJECTIVITY'; Files=@('.\phase174_r3_r7_r5_zero_image_hopf_injective\tests\test_rule.py') }
)
foreach ($Group in $Groups) {
    Write-Output ('PHASE174_R3R7R33_TEST_GROUP=' + $Group.Name)
    & python -B -m pytest -q --import-mode=importlib -p no:cacheprovider @($Group.Files)
    if ($LASTEXITCODE -ne 0) { throw ('R33 focused pytest failed: ' + $Group.Name) }
}
Write-Output 'PHASE174_R3R7R33_RUN=PASS'
Write-Output 'PHASE174_R3R7R33_FULL_PYTEST=False'
Write-Output '(END)'
```
