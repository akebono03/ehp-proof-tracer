# R30R1 コード全文

新規 `provider.py` を空ファイルから置換。以下は全文です。

## `provider.py`（全文）

```python
"""Source-certified Proposition 2.7 proposals in the ordinary shared provider.

This module adds only the reviewed *general* literature fact. Each typed
instance remains a checked INFERENCE from that general fixed reference.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    ASSERTION_ID,
    EXPECTED_THEOREM_SHA256,
    Prop27UniversalLiteratureStatement,
    register_universal_prop27,
)
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise,
    Prop27TypedHopfDeltaStatement,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import (
    AssertionOrigin, ReferenceKind, UnifiedStatementRegistry,
)

MANIFEST_REFERENCE_ID = "toda:Proposition 2.7"
MANIFEST_SOURCE_ID = "toda:tex:ch2:0018"


def _reviewed_position() -> int:
    """Use the exact existing source manifest identity, never a guessed rank."""
    positions, rows, _manifest = _load_manifest_reference_order(DEFAULT_MANIFEST)
    records = rows.get(MANIFEST_REFERENCE_ID, ())
    if (len(records) != 1
            or records[0]["statement_id"] != MANIFEST_SOURCE_ID
            or records[0]["locator"] != "Proposition 2.7"):
        raise ValueError("Proposition 2.7 manifest identity was not uniquely reviewed")
    position = positions.get(MANIFEST_REFERENCE_ID)
    if type(position) is not int or position <= 0:
        raise ValueError("Proposition 2.7 lacks reviewed publication position")
    return position


def register_positioned_prop27(root: Path) -> RegistryBridgeResult:
    """Add a general literature reference with its real source-order identity.

    R28 checks the primary theorem SHA before a GIVEN is constructed. The
    returned isolated bridge can be merged by the ordinary shared bridge.
    """
    if not isinstance(root, Path):
        raise TypeError("root must be Path")
    position = _reviewed_position()
    source = register_universal_prop27(root)
    original = source.registry.reference(next(iter(source.registry._references)))
    if (original.locator != "Proposition 2.7"
            or original.kind is not ReferenceKind.PROPOSITION
            or len(source.proof_links) != 1):
        raise ValueError("reviewed general source registry contract changed")
    registry = UnifiedStatementRegistry()
    registry.add_reference(replace(
        original, source_id=MANIFEST_SOURCE_ID,
        publication_position=position,
    ))
    for assertion in source.registry._assertions.values():
        registry.add_assertion(assertion)
    return RegistryBridgeResult(registry, source.records, source.proof_links)


def has_certified_prop27_leaf(bridge: RegistryBridgeResult) -> bool:
    """Require one exact screened, positioned, typed R28 GIVEN and proof link.

    This checks the reference-and-link contract, not an arbitrary citation label.
    Source-byte certification is performed by register_positioned_prop27().
    """
    if not isinstance(bridge, RegistryBridgeResult):
        return False
    matched = tuple(
        assertion for assertion in bridge.registry._assertions.values()
        if type(assertion.content) is Prop27UniversalLiteratureStatement
    )
    if len(matched) != 1:
        return False
    assertion = matched[0]
    claim = assertion.content
    if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
            or claim != Prop27UniversalLiteratureStatement()
            or claim.source_sha256 != EXPECTED_THEOREM_SHA256
            or assertion.kind.value != "statement"):
        return False
    try:
        reference = bridge.registry.reference(assertion.reference_id)
        position = _reviewed_position()
    except (KeyError, TypeError, ValueError):
        return False
    if (reference.kind is not ReferenceKind.PROPOSITION
            or reference.locator != "Proposition 2.7"
            or reference.source_id != MANIFEST_SOURCE_ID
            or reference.publication_position != position):
        return False
    matching_links = tuple(link for link in bridge.proof_links
                           if link.assertion_id == assertion.assertion_id)
    if len(matching_links) != 1:
        return False
    step = matching_links[0].step
    return (type(step) is ProofStep
            and step.rule is ProofRule.GIVEN
            and step.premises == ()
            and step.conclusion == claim)


def expand_public_cited_prop27_goal(goal: object, bridge: RegistryBridgeResult):
    """Supply only applicable inverse rules when a screened cited leaf exists.

    Do not construct any ProofStep, bypass the recursive proof checker, or
    assert Delta surjectivity or a zero group.
    """
    if type(goal) not in (Prop27GeneralTheoremPremise, Prop27TypedHopfDeltaStatement):
        return ()
    if not has_certified_prop27_leaf(bridge):
        return ()
    from phase174_r3_r7_r29_prop27_canonical_provider.provider import (
        expand_cited_prop27_goal,
    )
    return expand_cited_prop27_goal(goal)
```

## `tests/test_provider_contract.py`（新規、`tests/test_wiring.py` の隣、全文）

```python
"""R30R1 pre-install regression: the missing provider module is implemented."""
from pathlib import Path
from dataclasses import replace

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
    Prop27GeneralTheoremPremise, typed_specialization,
)
from phase174_r3_r7_r28_prop27_typed_literature_registration.registration import (
    Prop27UniversalLiteratureStatement,
)
from phase174_r3_r7_r30_prop27_public_provider_wiring.provider import (
    register_positioned_prop27, has_certified_prop27_leaf,
    expand_public_cited_prop27_goal,
)

ROOT = Path(__file__).resolve().parents[2]


def test_exact_manifest_positioned_universal_source():
    bridge = register_positioned_prop27(ROOT)
    assert has_certified_prop27_leaf(bridge)
    assert len(bridge.proof_links) == 1
    assert type(bridge.proof_links[0].step.conclusion) is Prop27UniversalLiteratureStatement


def test_nonexistent_link_never_proposes_a_theorem():
    bridge = register_positioned_prop27(ROOT)
    no_link = RegistryBridgeResult(bridge.registry, bridge.records, ())
    assert not has_certified_prop27_leaf(no_link)
    assert expand_public_cited_prop27_goal(typed_specialization(6), no_link) == ()


def test_cited_general_and_n6_proposals_are_backward_inferences():
    bridge = register_positioned_prop27(ROOT)
    general = expand_public_cited_prop27_goal(Prop27GeneralTheoremPremise(), bridge)
    concrete = expand_public_cited_prop27_goal(typed_specialization(6), bridge)
    assert len(general) == 1
    assert general[0].subgoals == (Prop27UniversalLiteratureStatement(),)
    assert len(concrete) == 1
    assert concrete[0].subgoals == (Prop27GeneralTheoremPremise(),)


def test_invalid_instance_and_unrelated_root_have_no_candidates():
    bridge = register_positioned_prop27(ROOT)
    forged = replace(typed_specialization(6), sign_undetermined=False)
    assert expand_public_cited_prop27_goal(forged, bridge) == ()
    assert expand_public_cited_prop27_goal("pi_12^7=0", bridge) == ()
```

## `run.ps1`（全置換、全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

& python -B -m phase174_r3_r7_r30_prop27_public_provider_wiring.audit --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R30 Source Guard failed' }
if ($DryRun) {
    Write-Output 'PHASE174_R3R7R30_RUN=DRYRUN_PASS'
    Write-Output '(END)'
    exit 0
}

& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_provider_contract.py
if ($LASTEXITCODE -ne 0) { throw 'R30R1 pre-install provider contract failed' }

& python -B -m phase174_r3_r7_r30_prop27_public_provider_wiring.install
if ($LASTEXITCODE -ne 0) { throw 'R30 guarded installation failed' }
& python -B -m phase174_r3_r7_r30_prop27_public_provider_wiring.audit
if ($LASTEXITCODE -ne 0) { throw 'R30 public shared source audit failed' }

& python -B -m pytest -q --import-mode=importlib -p no:cacheprovider `
  phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_wiring.py `
  phase174_r3_r7_r30_prop27_public_provider_wiring/tests/test_provider_contract.py `
  phase174_r3_r7_r29_prop27_canonical_provider/tests/test_provider.py `
  phase174_r3_r7_r28_prop27_typed_literature_registration/tests/test_registration.py `
  phase174_r3_r7_r27_certified_premise_registry_audit/tests/test_audit.py `
  tests/test_phase50_prop27_theorem_semantics.py
if ($LASTEXITCODE -ne 0) { throw 'R30 focused pytest failed' }

Write-Output 'PHASE174_R3R7R30_RUN=PASS'
Write-Output '(END)'
```

`install.py`、`audit.py`、`tests/test_wiring.py` は R30 配布 ZIP から変更していません。
`phase165_r52_r9_shared_math.py` に対する変更は、検査後のインストール時に R30 と同じ2関数のみです。
