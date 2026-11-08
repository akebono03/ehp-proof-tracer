# Phase 174 R3-R7-R28 新規コード全文

既存のクラス、関数、import は変更しない。すべて新規ファイル。

## `registration.py`（新規）

```python
"""Source-gated universal Toda Proposition 2.7 literature registration.

A universal theorem can be a fixed literature premise. Its individual n=6
consequence is INFERENCE only. This module does not install public rules.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult, MigrationRecord, MigrationStatus
from phase174_r3_r7_r26_prop27_source_premise_connection.bridge import (
    Prop27SourceEvidence, audited_prop27_source,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    PROP27_REFERENCE, Prop27GeneralTheoremPremise,
)
from proof import (
    InferenceRule, LiteratureReference, PremisePattern, ProofRule, ProofStep,
    find_inference_match, apply_inference_match,
)
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)

EXPECTED_THEOREM_SHA256 = "5dd846b99e4b5cded30784477fd64c2449d72c4c07895bbff94f5c9a056fb703"
REFERENCE_ID = "typed_literature:toda:prop2.7"
ASSERTION_ID = "typed_literature:assertion:toda:prop2.7"


@dataclass(frozen=True)
class Prop27UniversalLiteratureStatement:
    """General cited theorem only, NOT the evidence hash or an instance."""
    locator: str = "Proposition 2.7"
    variable: str = "n"
    minimum_n: int = 2
    even_n_only: bool = True
    signed_hopf_delta: bool = True
    source_sha256: str = EXPECTED_THEOREM_SHA256


def verified_universal_statement(root: Path) -> Prop27UniversalLiteratureStatement:
    """Require reviewed primary-source bytes and exact general theorem semantics."""
    if not isinstance(root, Path):
        raise TypeError("root must be a Path")
    source = audited_prop27_source(root)
    if (not isinstance(source, Prop27SourceEvidence)
            or source.locator != "Proposition 2.7"
            or source.theorem_sha256 != EXPECTED_THEOREM_SHA256
            or source.only_even_n is not True
            or source.sign_undetermined is not True):
        raise ValueError("Toda Proposition 2.7 source not verified")
    return Prop27UniversalLiteratureStatement()


def register_universal_prop27(root: Path) -> RegistryBridgeResult:
    """Construct an isolated typed source registry without affecting global state.

    A GIVEN leaf represents a verified fixed *general literature statement*,
    following existing typed literature contracts. It is never an n=6 GIVEN.
    """
    theorem = verified_universal_statement(root)
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id=REFERENCE_ID,
        kind=ReferenceKind.PROPOSITION,
        locator=theorem.locator,
        source_id="sources/toda/Toda_02_2.tex",
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id=ASSERTION_ID,
        reference_id=REFERENCE_ID,
        kind=AssertionKind.STATEMENT,
        content=theorem,
        origin=AssertionOrigin.FIXED_STATEMENT,
        scope=("n >= 2", "n even", "sign undetermined"),
    ))
    step = ProofStep(conclusion=theorem, premises=(), rule=ProofRule.GIVEN)
    return RegistryBridgeResult(
        registry=registry,
        records=(MigrationRecord(
            "phase174_r3_r7_r28", "Proposition 2.7", ASSERTION_ID,
            MigrationStatus.STRUCTURED,
            "Source-verified universal literature theorem; no individual instance",
        ),),
        proof_links=(ProofStepLink(assertion_id=ASSERTION_ID, step=step),),
    )


def prop27_literature_to_premise_rule() -> InferenceRule:
    """Derive R25 general premise from an exact source-registered theorem leaf."""
    theorem = Prop27UniversalLiteratureStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and type(premises[0].conclusion) is Prop27UniversalLiteratureStatement
            and premises[0].conclusion == theorem
        )

    return InferenceRule(
        name="Toda Proposition 2.7 typed literature universal premise",
        description="Infer a reusable schema from the source-verified general theorem",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=Prop27UniversalLiteratureStatement,
            statement_pattern=theorem,
        ),),
        conclusion_pattern=Prop27GeneralTheoremPremise(),
        match_guard=guard,
        literature_reference=PROP27_REFERENCE,
    )


def derive_registered_general_premise(bridge: RegistryBridgeResult) -> ProofStep:
    """Use exact Registry link, do not trust arbitrary externally supplied GIVEN."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("expected RegistryBridgeResult")
    record = bridge.registry.assertion(ASSERTION_ID)
    reference = bridge.registry.reference(REFERENCE_ID)
    if (record.origin is not AssertionOrigin.FIXED_STATEMENT
            or record.reference_id != REFERENCE_ID
            or record.content != Prop27UniversalLiteratureStatement()
            or reference.kind is not ReferenceKind.PROPOSITION
            or reference.locator != "Proposition 2.7"):
        raise ValueError("invalid universal literature assertion")
    links = tuple(link for link in bridge.proof_links if link.assertion_id == ASSERTION_ID)
    if len(links) != 1 or links[0].step is None:
        raise ValueError("unique source-bound ProofStepLink required")
    parent = links[0].step
    if (type(parent) is not ProofStep
            or parent.rule is not ProofRule.GIVEN
            or parent.premises != ()
            or parent.conclusion != record.content):
        raise ValueError("invalid universal literature proof step")
    match = find_inference_match(prop27_literature_to_premise_rule(), (parent,))
    if match is None:
        raise ValueError("literature schema inference not available")
    derived = apply_inference_match(match)
    if (derived.rule is not ProofRule.INFERENCE
            or derived.premises != (parent,)
            or derived.conclusion != Prop27GeneralTheoremPremise()):
        raise ValueError("unverified general premise")
    return derived

```

## `audit.py`（新規）

```python
"""R28 source-first preflight and isolated typed literature / inference audit."""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID, REFERENCE_ID, Prop27UniversalLiteratureStatement,
    register_universal_prop27, verified_universal_statement,
    derive_registered_general_premise,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    typed_specialization, prop27_typed_specialization_rule,
)
from proof import ProofRule, find_inference_match, apply_inference_match

ROOT = Path(__file__).resolve().parents[1]
BASE = "7203ed2ced9a4bb05274e2a4380241b328943c33"
ALLOWED = (
    "phase174_r3_r7_r27_certified_premise_registry_audit/",
    "phase174_r3_r7_r28_prop27_typed_literature_registration/",
)
CACHE = ".pytest_cache/v/cache/nodeids"
PROTECTED = (
    "sources/toda/Toda_02_2.tex", "proof.py", "homotopy_groups.py",
    "unified_statement_registry.py", "phase163_r4_registry_bridge.py",
    "phase165_r3_recursive_search.py",
    "phase174_r3_r7_r25_prop27_isolated_inference/rule.py",
    "phase174_r3_r7_r26_prop27_source_premise_connection/bridge.py",
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                          text=True, encoding="utf-8", errors="replace",
                          check=True).stdout.strip()


def allowed_paths(paths: tuple[str, ...]) -> bool:
    bad = tuple(path for path in paths if path != CACHE
                and not any(path.startswith(prefix) for prefix in ALLOWED))
    if bad:
        raise RuntimeError("Unreviewed paths: " + repr(bad))
    return True


def source_guard() -> str:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Expected repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop")
    head = git("rev-parse", "HEAD")
    line = git("ls-remote", "origin", "refs/heads/develop")
    if not line or head != line.split()[0]:
        raise RuntimeError("Local/remote develop differ")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", BASE, head),
                              cwd=ROOT, capture_output=True)
    if ancestor.returncode:
        raise RuntimeError("R27 reviewed HEAD is not an ancestor")
    allowed_paths(tuple(git("diff", "--name-only", BASE, head).splitlines()))
    allowed_paths(tuple(git("diff", "--name-only").splitlines()))
    allowed_paths(tuple(git("diff", "--cached", "--name-only").splitlines()))
    for file in PROTECTED:
        baseline = subprocess.run(("git", "show", BASE + ":" + file),
                                  cwd=ROOT, capture_output=True, check=True).stdout
        working = (ROOT / file).read_bytes()
        normalized = baseline.replace(b"\r\n", b"\n")
        if working not in (baseline, normalized, normalized.replace(b"\n", b"\r\n")):
            raise RuntimeError("Protected source changed: " + file)
    return head


def check_registration() -> dict[str, object]:
    bridge = register_universal_prop27(ROOT)
    assertion = bridge.registry.assertion(ASSERTION_ID)
    ref = bridge.registry.reference(REFERENCE_ID)
    general = derive_registered_general_premise(bridge)
    match = find_inference_match(prop27_typed_specialization_rule(6), (general,))
    if match is None:
        raise RuntimeError("Proposition 2.7 n=6 inference not available")
    instance = apply_inference_match(match)
    if (instance.rule is not ProofRule.INFERENCE
            or instance.premises != (general,)
            or instance.conclusion != typed_specialization(6)):
        raise RuntimeError("n=6 inference chain invalid")
    return {
        "universal_registered": isinstance(assertion.content, Prop27UniversalLiteratureStatement),
        "reference_locator": ref.locator,
        "source_sha256": assertion.content.source_sha256,
        "universal_given_count": 1,
        "n6_direct_given_count": 0,
        "general_inference": general.rule is ProofRule.INFERENCE,
        "n6_inference": instance.rule is ProofRule.INFERENCE,
        "parent_depth": 2,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head = source_guard()
    universal = verified_universal_statement(ROOT)
    print("PHASE174_R3R7R28_HEAD=" + head)
    print("PHASE174_R3R7R28_SOURCE_GUARD=PASS")
    print("PHASE174_R3R7R28_SOURCE_SHA256=" + universal.source_sha256)
    if not args.dry_run:
        for key, value in check_registration().items():
            print("PHASE174_R3R7R28_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R28_PUBLIC_REGISTRATION=False")
    print("PHASE174_R3R7R28_FULL_PYTEST=False")
    print("PHASE174_R3R7R28_ROOT_COMPLETE=False")
    print("PHASE174_R3R7R28_GATE=" + (
        "PASS_R28_SOURCE_PREFLIGHT_ONLY" if args.dry_run else
        "PASS_R28_UNIVERSAL_REGISTERED_ISOLATED_INFERENCE_PUBLIC_PENDING"))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_registration.py`（新規）

```python
"""R28 focused proof-eligibility and type-specific inference guards."""
from dataclasses import replace
from pathlib import Path

import pytest

from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization, prop27_typed_specialization_rule,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID, REFERENCE_ID, Prop27UniversalLiteratureStatement,
    verified_universal_statement, register_universal_prop27,
    prop27_literature_to_premise_rule, derive_registered_general_premise,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.audit import allowed_paths
from proof import ProofRule, ProofStep, find_inference_match, apply_inference_match
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parents[2]


def test_primary_source_general_theorem_checked():
    theorem = verified_universal_statement(ROOT)
    assert theorem.locator == "Proposition 2.7"
    assert theorem.minimum_n == 2
    assert theorem.even_n_only is True
    assert theorem.signed_hopf_delta is True


def test_isolated_typed_registration_and_single_general_given():
    bridge = register_universal_prop27(ROOT)
    record = bridge.registry.assertion(ASSERTION_ID)
    assert record.origin is AssertionOrigin.FIXED_STATEMENT
    assert record.reference_id == REFERENCE_ID
    assert isinstance(record.content, Prop27UniversalLiteratureStatement)
    assert len(bridge.proof_links) == 1
    parent = bridge.proof_links[0].step
    assert parent.rule is ProofRule.GIVEN
    assert parent.conclusion == record.content
    assert parent.premises == ()
    assert not isinstance(parent.conclusion, Prop27GeneralTheoremPremise)
    assert parent.conclusion != typed_specialization(6)


def test_real_registered_chain_generates_n6_only_by_inference():
    bridge = register_universal_prop27(ROOT)
    general = derive_registered_general_premise(bridge)
    assert general.rule is ProofRule.INFERENCE
    assert len(general.premises) == 1
    match = find_inference_match(prop27_typed_specialization_rule(6), (general,))
    assert match is not None
    result = apply_inference_match(match)
    assert result.conclusion == typed_specialization(6)
    assert result.rule is ProofRule.INFERENCE
    assert result.premises == (general,)
    assert result.inference_rule.literature_reference.locator == "Proposition 2.7"


def test_no_premise_cannot_create_schema():
    assert find_inference_match(prop27_literature_to_premise_rule(), ()) is None


def test_source_given_cannot_be_replaced_with_wrong_statement():
    parent = ProofStep(
        conclusion=replace(Prop27UniversalLiteratureStatement(), source_sha256="0" * 64),
        premises=(), rule=ProofRule.GIVEN,
    )
    assert find_inference_match(prop27_literature_to_premise_rule(), (parent,)) is None


def test_specific_n6_given_cannot_satisfy_universal_rule():
    parent = ProofStep(typed_specialization(6), (), ProofRule.GIVEN)
    assert find_inference_match(prop27_literature_to_premise_rule(), (parent,)) is None


def test_wrong_source_bytes_rejected(tmp_path):
    folder = tmp_path / "sources" / "toda"
    folder.mkdir(parents=True)
    (folder / "Toda_02_2.tex").write_text(
        "\\begin{proposition}\\label{prop:2.7}fake\\end{proposition}",
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        verified_universal_statement(tmp_path)


def test_no_public_rules_or_root_claimed():
    bridge = register_universal_prop27(ROOT)
    assert len(bridge.records) == 1
    assert all("n=6" not in str(link.step.conclusion) for link in bridge.proof_links)


def test_source_guard_allowlist_is_narrow():
    assert allowed_paths(("phase174_r3_r7_r27_certified_premise_registry_audit/README.md",
                          "phase174_r3_r7_r28_prop27_typed_literature_registration/audit.py"))
    for path in ("proof.py", "sources/toda/Toda_02_2.tex", ".pytest_cache/v/cache/lastfailed"):
        with pytest.raises(RuntimeError, match="Unreviewed"):
            allowed_paths((path,))

```

## `run.ps1`（新規）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
& python -B -m phase174_r3_r7_r28_prop27_typed_literature_registration.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R28 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R28_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}
& python -B -m phase174_r3_r7_r28_prop27_typed_literature_registration.audit
if ($LASTEXITCODE -ne 0) { throw 'R28 isolated registration audit failed' }
& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r28_prop27_typed_literature_registration/tests/test_registration.py `
  phase174_r3_r7_r27_certified_premise_registry_audit/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_bridge.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_audit.py `
  phase174_r3_r7_r26_prop27_source_premise_connection/tests/test_run_import_mode.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_rule.py `
  phase174_r3_r7_r25_prop27_isolated_inference/tests/test_lineage.py `
  phase174_r3_r7_r24_prop27_general_typed_design/tests/test_audit.py `
  tests/test_phase50_prop27_theorem_semantics.py
if ($LASTEXITCODE -ne 0) { throw 'R28 focused pytest failed' }
Write-Output 'PHASE174_R3R7R28_RUN=PASS'
Write-Output '(END)'

```

