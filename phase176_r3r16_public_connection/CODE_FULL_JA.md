# Phase 176 R3R16 — コード全文

既存ファイルについては、インストーラが現在の Git blob を照合して2関数のみにブロックを追加します。変更後の関数全文は `python -m phase176_r3r16_public_connection.emit_full_functions` により出力します。

## provider.py

```python
"""Public bridge for the already-verified typed two-step right-zero inference.

No newly asserted group relation or generator image is inserted as a GIVEN.
Both children remain proof obligations of the ordinary recursive search.
"""
from __future__ import annotations

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
from phase176_r3r15_shared_extra_provider_probe.provider import build_screened_extra_provider
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin


def build_public_lemma57_right_provider(bridge: RegistryBridgeResult):
    """Use only a uniquely screened, cited Lemma 5.7 fixed-statement leaf."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("typed screened source bridge required")
    accepted = []
    for link in bridge.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep)
                or step.rule is not ProofRule.GIVEN
                or step.premises
                or type(step.conclusion) is not TodaLemma57ExplicitNuPrimeZero):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        citation = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content != step.conclusion
                or reference.publication_position is None
                or citation is None
                or citation.locator != "Lemma 5.7"):
            continue
        accepted.append(step)
    if len(accepted) == 1:
        return build_screened_extra_provider(tuple(accepted))

    def no_candidates(goal: object) -> tuple:
        return ()

    return no_candidates

```

## installer.py

```python
"""Guarded installer: edit exactly two existing full function bodies via anchors."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "phase165_r52_r9_shared_math.py"
EXPECTED_BLOB = "f276170b3a3832ee9a9489becfbc5bbf2120727b"
SOURCE_ANCHOR = "        sources = sources + (build_cited_511_source(),)\n"
SOURCE_ADD = """        # Phase 176 R3R16: cited particular clause, not a direct image GIVEN.
        from phase175_r3r9_lemma57_explicit_public.source import (
            build_explicit_lemma57_source,
        )
        sources = sources + (
            build_explicit_lemma57_source(Path(__file__).resolve().parent),
        )
"""
PROVIDER_ANCHOR = """    # Phase 175 R4R12R13R4: retain H=0 as a verified intermediate ProofStep.
"""
PROVIDER_ADD = """    # Phase 176 R3R16: source-screened Lemma 5.7 and generic typed
    # right-composition zero-image inference; both remain open DFS subgoals.
    from phase176_r3r16_public_connection.provider import (
        build_public_lemma57_right_provider,
    )
    extra_providers = (
        build_public_lemma57_right_provider(bridge),
    ) + tuple(extra_providers)
"""


def git(*args: str) -> str:
    p = subprocess.run(("git",) + args, cwd=ROOT, text=True,
                       encoding="utf-8", errors="replace", capture_output=True)
    if p.returncode:
        raise RuntimeError("git " + " ".join(args) + ": " + p.stderr.strip())
    return p.stdout.strip()


def preflight() -> tuple[str, str]:
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPO")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    old = TARGET.read_bytes().decode("utf-8")
    normalized = old.replace("\r\n", "\n")
    if SOURCE_ADD in normalized and PROVIDER_ADD in normalized:
        return old, "ALREADY_INSTALLED"
    if SOURCE_ADD in normalized or PROVIDER_ADD in normalized:
        raise RuntimeError("PARTIAL_INSTALLATION")
    blob = git("hash-object", "--", str(TARGET.relative_to(ROOT)))
    if blob != EXPECTED_BLOB:
        raise RuntimeError("SOURCE_BLOB_DRIFT: " + blob)
    for label, anchor in (("source", SOURCE_ANCHOR), ("provider", PROVIDER_ANCHOR)):
        if normalized.count(anchor) != 1:
            raise RuntimeError("ANCHOR_DRIFT_" + label)
    if "def build_shared_typed_bridge(" not in old or "def shared_expansion_provider(" not in old:
        raise RuntimeError("FUNCTIONS_MISSING")
    return old, "READY"


def install(dry_run: bool) -> str:
    original, status = preflight()
    if dry_run or status == "ALREADY_INSTALLED":
        return status
    newline = "\r\n" if "\r\n" in original else "\n"
    updated = original.replace("\r\n", "\n").replace(SOURCE_ANCHOR, SOURCE_ANCHOR + SOURCE_ADD)
    updated = updated.replace(PROVIDER_ANCHOR, PROVIDER_ADD + PROVIDER_ANCHOR)
    if newline != "\n":
        updated = updated.replace("\n", newline)
    compile(updated, str(TARGET), "exec")
    TARGET.write_bytes(updated.encode("utf-8"))
    return "INSTALLED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        status = install(args.dry_run)
        print("PHASE176_R3R16_INSTALL=" + status)
        print("PHASE176_R3R16_NEW_DIRECT_GROUP_GIVEN=0")
        print("PHASE176_R3R16_FULL_PYTEST=NOT_RUN")
        return 0
    except Exception as exc:
        print("PHASE176_R3R16_INSTALL_ERROR=" + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

```

## audit.py

```python
"""R3R16 focused public connection audit; no invented complete-proof status."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r16_public_connection"


def report_file() -> Path:
    folder = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    folder.mkdir(parents=True, exist_ok=True)
    return folder / "report.json"


def observe() -> dict:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r9_lemma57_explicit_public.source import TodaLemma57ExplicitNuPrimeZero
    from phase175_r3r9_lemma57_explicit_public.rule import RULE_NAME as CITED_RULE
    from phase176_r3r10_right_zero_transport_isolated.rule import RULE_NAME as RIGHT_RULE
    from phase176_r3r16_public_connection.provider import build_public_lemma57_right_provider
    from proof import Relation

    root = search_group_from_registered_goal(n=3, k=5)
    goal = next((g for g in root.open_goals if type(g) is Relation and g.lhs == TodaPrimaryGroup(8, 3)), None)
    # A completed search has no open goal; use registered DB target only as a goal if needed.
    if goal is None:
        from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
        goal = exact_prior_database_result(3, 5)
    if goal is None:
        raise RuntimeError("TARGET_RELATION_NOT_AVAILABLE")
    prior = exact_prior_database_result(2, 5)
    if prior is None:
        raise RuntimeError("PRIOR_NOT_AVAILABLE")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("EXPECTED_TYPED_COMPOSITION_MISSING")
    base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        Composition(factors[0], factors[1]), Zero(),
    )
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        prior.rhs.generator, Zero(),
    )
    bridge = build_shared_typed_bridge()
    screened = screen_independent_sources_for_derived_goal(bridge, goal=goal)
    accepted = tuple(link.step for link in screened.proof_links if
                     link.step is not None and type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero)
    if len(accepted) != 1:
        raise RuntimeError("CITED_SOURCE_SCREEN_COUNT_NOT_ONE")
    provider = shared_expansion_provider(screened, proof_target=goal)
    cited = tuple(o for o in provider(base) if o.rule.name == CITED_RULE)
    right = tuple(o for o in provider(whole) if o.rule.name == RIGHT_RULE)
    if len(cited) != 1 or len(right) != 1 or right[0].subgoals != (base,):
        raise RuntimeError("PUBLIC_TWO_STEP_PROPOSAL_MISSING")
    from proof import ProofRule, find_inference_matches_for_rule
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    cited_matches = tuple(find_inference_matches_for_rule(cited[0].rule, accepted))
    if len(cited_matches) != 1:
        raise RuntimeError("PUBLIC_CITED_PROOF_STEP_NOT_MATCHED")
    step1 = derive_inference_proof_step(cited_matches[0])
    matches2 = tuple(find_inference_matches_for_rule(right[0].rule, (step1,)))
    if len(matches2) != 1:
        raise RuntimeError("PUBLIC_RIGHT_PROOF_STEP_NOT_MATCHED")
    step2 = derive_inference_proof_step(matches2[0])
    if (step1.rule is not ProofRule.INFERENCE or step2.rule is not ProofRule.INFERENCE
            or step2.premises != (step1,)):
        raise RuntimeError("PUBLIC_NESTED_PROOF_INVALID")
    # Exercise the genuine recursive proof engine, not just manual rule matching.
    from phase165_r3_recursive_search import reconstruct_registered_goal
    citation_id = next(link.assertion_id for link in screened.proof_links
                       if link.step is not None
                       and type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero)
    recursively_proved = reconstruct_registered_goal(
        whole, screened, citation_id, provider, lookup_mode="typed_reference",
    )
    if recursively_proved.conclusion != whole or recursively_proved.rule is not ProofRule.INFERENCE:
        raise RuntimeError("RECURSIVE_PUBLIC_PROOF_MISSING")
    return {
        "recursive_public_two_stage_proved": True,
        "screened_cited_source_steps": len(accepted),
        "public_base_cited_candidates": len(cited),
        "public_whole_right_candidates": len(right),
        "public_nested_inference_steps": 2,
        "public_search_status": root.status.value,
        "public_open_goals": len(root.open_goals),
        "root_proof_complete": root.status.value == "complete",
        "new_direct_group_given": 0,
        "full_pytest": "NOT_RUN",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    report = {"phase": "176_R3R16", "dry_run": args.dry_run,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R16", "full_pytest": "NOT_RUN"}
    try:
        from phase176_r3r16_public_connection.installer import preflight
        _, status = preflight()
        if args.dry_run:
            report["gate"] = "PASS_R3R16_DRYRUN_" + status
        else:
            if status != "ALREADY_INSTALLED":
                raise RuntimeError("PUBLIC_INSTALL_MISSING")
            report["observed"] = observe()
            report["gate"] = "PASS_R3R16_PUBLIC_TWO_STEP_CONNECTED"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
    target = report_file()
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R16_GATE=" + report["gate"])
    if "observed" in report:
        for key, value in report["observed"].items():
            print("PHASE176_R3R16_" + key.upper() + "=" + str(value))
    if "error" in report:
        print("PHASE176_R3R16_ERROR=" + report["error"])
    print("PHASE176_R3R16_REPORT=" + str(target))
    print("PHASE176_R3R16_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_r3r16_connection.py

```python
"""Focused tests of the R3R16 public source and generic right-zero connection."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase175_r3r9_lemma57_explicit_public.source import (
    TodaLemma57ExplicitNuPrimeZero,
    build_explicit_lemma57_source,
)
from phase176_r3r16_public_connection.provider import build_public_lemma57_right_provider
from proof import ProofRule, ProofStep
from unified_statement_registry import UnifiedStatementRegistry
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_no_screened_source_means_no_proposals():
    empty = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    provider = build_public_lemma57_right_provider(empty)
    assert provider(object()) == ()


def test_real_source_only_is_not_direct_image_given():
    source = build_explicit_lemma57_source(ROOT)
    provider = build_public_lemma57_right_provider(source)
    assert all(link.step.rule is ProofRule.GIVEN for link in source.proof_links)
    assert all(type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero for link in source.proof_links)
    assert provider(object()) == ()


def test_wrong_source_content_is_rejected():
    source = build_explicit_lemma57_source(ROOT)
    bad_link = replace(source.proof_links[0], step=ProofStep("fake", (), ProofRule.GIVEN))
    bad = RegistryBridgeResult(source.registry, source.records, (bad_link,))
    assert build_public_lemma57_right_provider(bad)(object()) == ()


def test_typed_generic_right_zero_requires_three_factors():
    from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        Composition(a, Composition(b, c)), Zero(),
    )
    assert preceding_zero_image(goal) is not None
    assert preceding_zero_image(replace(goal, source_generator=Composition(a, b))) is None

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r16_public_connection.installer --dry-run
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        python -B -m phase176_r3r16_public_connection.audit --dry-run
        exit $LASTEXITCODE
    }
    python -B -m phase176_r3r16_public_connection.installer
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase176_r3r16_public_connection/tests/test_r3r16_connection.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase175_r3r9_lemma57_explicit_public/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m pytest -q -p no:cacheprovider phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    python -B -m phase176_r3r16_public_connection.audit
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $fullCode = python -B -m phase176_r3r16_public_connection.emit_full_functions
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    $fullCode | Set-Content -Encoding UTF8 -Path (Join-Path $PSScriptRoot 'MODIFIED_FUNCTIONS_FULL_JA.md')
    exit 0
} finally {
    Pop-Location
}

```

