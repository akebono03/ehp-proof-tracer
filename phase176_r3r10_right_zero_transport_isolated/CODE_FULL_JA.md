# Phase 176 R3R10 — 変更コード全文

## 変更一覧

既存ファイルは変更しない。追加対象：`phase176_r3r10_right_zero_transport_isolated/` の各新規ファイル。

追加位置：`rule.py` のモジュール先頭に import、その後 `RULE_NAME`、`right_zero_transport_inputs`、`right_zero_transport_rule`、`expand_right_zero_transport`。`audit.py` は新規監査モジュール。`tests/test_rule.py` は新規テストモジュール。

## rule.py（全文）

```python
"""Isolated generic right-composition transport for a zero suspension image.

No provider registration or source/goal assertion is performed here.
A proven E(a)=0 implies E(a o b)=0 for a well-typed composite.
"""
from __future__ import annotations

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r7_composite_zero_audit.rule import expression_endpoints
from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
from proof import InferenceRule, PremisePattern, ProofRule


RULE_NAME = "zero suspension image transports over typed right composition"


def right_zero_transport_inputs(
    goal: object, base: object,
) -> tuple[GeneratorImage] | None:
    """Require the same typed E, zero image, exact source prefix, and one right factor.

    Flattening source factors uses the associativity of composition. The
    source generator is never selected by its display name. Both zero-image
    statements are proof obligations, not assumptions.
    """
    if type(goal) is not GeneratorImage or type(base) is not GeneratorImage:
        return None
    if (type(goal.map) is not TodaSuspensionMap
            or type(base.map) is not TodaSuspensionMap
            or type(goal.target_generator) is not Zero
            or type(base.target_generator) is not Zero):
        return None
    for statement in (goal, base):
        source = statement.map.source_group
        target = statement.map.target_group
        if type(source) is not TodaPrimaryGroup or type(target) is not TodaPrimaryGroup:
            return None
        degree, sphere = source.group_dimension, source.sphere_dimension
        if (type(degree) is not int or type(sphere) is not int
                or sphere < 2 or degree < sphere
                or target != TodaPrimaryGroup(degree + 1, sphere + 1)
                or expression_endpoints(statement.source_generator) != (degree, sphere)):
            return None
    whole_source = goal.map.source_group
    base_source = base.map.source_group
    if (whole_source.sphere_dimension != base_source.sphere_dimension
            or whole_source.group_dimension <= base_source.group_dimension):
        return None
    whole_factors = typed_composition_factors(goal.source_generator)
    base_factors = typed_composition_factors(base.source_generator)
    if (whole_factors is None or base_factors is None
            or len(base_factors) < 2
            or len(whole_factors) != len(base_factors) + 1
            or whole_factors[:len(base_factors)] != base_factors):
        return None
    # Composition is well-typed both before and after suspending, and the
    # extra factor is exactly the final right-hand factor of the goal.
    trailing = whole_factors[-1]
    if expression_endpoints(trailing) != (
        whole_source.group_dimension, base_source.group_dimension,
    ):
        return None
    return (base,)


def right_zero_transport_rule(goal: GeneratorImage, base: GeneratorImage) -> InferenceRule:
    required = right_zero_transport_inputs(goal, base)
    if required is None:
        raise ValueError("right zero transport requires exact typed composite data")

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.INFERENCE
            and premises[0].conclusion == required[0]
            and right_zero_transport_inputs(goal, base) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "For a suspension map, E(a)=0 implies E(a composed on the right "
            "with b)=0 by functoriality and the zero-map law. The exact typed "
            "prefix, map dimensions and inferred antecedent are required."
        ),
        premise_patterns=(PremisePattern(
            statement_type=GeneratorImage,
            statement_pattern=base,
            proof_rule=ProofRule.INFERENCE,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    )


def expand_right_zero_transport(
    goal: object, base: object,
) -> tuple[GoalExpansion, ...]:
    inputs = right_zero_transport_inputs(goal, base)
    if inputs is None:
        return ()
    return (GoalExpansion(
        rule=right_zero_transport_rule(goal, base),
        subgoals=inputs,
    ),)
```

## audit.py（全文）

```python
"""R3R10: isolated generic right-composition zero-image inference audit."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "phase176_r3r10_right_zero_transport_isolated"
REVIEWED_HEAD = "01880f0cb62ffa610a91ef8f474c4d260f0ecf66"
MARKER = "PHASE176_R3R10_WORKER_JSON="
SOURCES = {
    "phase176_r3r9_right_composition_type_boundary/audit.py": (
        "def observe(", "GENERATOR_IMAGE_BASE_ZERO_TO_RIGHT_COMPOSITION_ZERO_TRANSPORT_NOT_CERTIFIED",
    ),
    "phase176_r3r7_lemma57_derived_source_proof/audit.py": (
        "def derive_from_existing_source(",
    ),
    "phase175_r3r9_lemma57_explicit_public/source.py": (
        "def build_explicit_lemma57_source(",
    ),
    "phase175_r3r9_lemma57_explicit_public/rule.py": (
        "def expand_cited_lemma57_explicit_zero(",
    ),
    "phase174_r3_r7_r9_composition_associativity/rule.py": (
        "def typed_composition_factors(",
    ),
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": (
        "def expression_endpoints(",
    ),
    "phase165_r52_r9_shared_math.py": (
        "def build_shared_typed_bridge(",
    ),
    "sources/toda/Toda_05_2.tex": (r"\label{lemma:5.7}", r"E(\eta_2\circ\nu')=0"),
}


def git(*args: str, check: bool = True) -> tuple[int, str]:
    result = subprocess.run(("git",) + args, cwd=ROOT, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", check=False)
    if check and result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(args) + ": " + result.stderr.strip())
    return result.returncode, result.stdout.strip()


def check_sources(root: Path) -> dict[str, str]:
    hashes = {}
    for name, anchors in SOURCES.items():
        path = root / name
        if not path.is_file():
            raise RuntimeError("REQUIRED_SOURCE_MISSING: " + name)
        contents = "".join(path.read_text(encoding="utf-8-sig").split())
        if any("".join(anchor.split()) not in contents for anchor in anchors):
            raise RuntimeError("SOURCE_ANCHOR_MISSING: " + name)
        hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return hashes


def preflight() -> dict[str, object]:
    if Path(git("rev-parse", "--show-toplevel")[1]).resolve() != ROOT.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    if git("branch", "--show-current")[1] != "develop":
        raise RuntimeError("DEVELOP_REQUIRED")
    if git("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD", check=False)[0]:
        raise RuntimeError("REVIEWED_HEAD_NOT_ANCESTOR")
    if git("status", "--porcelain", "--untracked-files=no")[1]:
        raise RuntimeError("TRACKED_FILES_DIRTY")
    return {"head": git("rev-parse", "HEAD")[1],
            "source_sha256": check_sources(ROOT), "full_pytest": "NOT_RUN",
            "historical_source_guards": "FOUR_KNOWN_FAILURES_NOT_PASSING"}


def observe() -> dict[str, object]:
    from expression import Composition, Zero
    from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r9_composition_associativity.rule import typed_composition_factors
    from phase175_r3r6_lemma57_general.source import merge_isolated_cited_source
    from phase175_r3r9_lemma57_explicit_public.rule import expand_cited_lemma57_explicit_zero
    from phase175_r3r9_lemma57_explicit_public.source import (
        TodaLemma57ExplicitNuPrimeZero, build_explicit_lemma57_source,
    )
    from phase176_r3r7_lemma57_derived_source_proof.audit import (
        derive_from_existing_source, selected_source_steps,
    )
    from phase176_r3r8_lemma57_provider_binding.audit import source_bound_provider
    from phase176_r3r10_right_zero_transport_isolated.rule import (
        RULE_NAME, expand_right_zero_transport, right_zero_transport_inputs,
    )
    from phase164_r8_proofstep_factory import derive_inference_proof_step
    from proof import ProofRule, Relation, find_inference_matches_for_rule

    result = search_group_from_registered_goal(n=3, k=5)
    if result.status.value != "search_failed" or len(result.open_goals) != 3:
        raise RuntimeError("PUBLIC_SEARCH_FRONTIER_DRIFT")
    target = next((g for g in result.open_goals
                   if type(g) is Relation and g.lhs == TodaPrimaryGroup(8, 3)), None)
    if target is None:
        raise RuntimeError("TARGET_GOAL_MISSING")
    prior = exact_prior_database_result(2, 5)
    if type(prior) is not Relation or prior.lhs != TodaPrimaryGroup(7, 2):
        raise RuntimeError("PRIOR_GOAL_MISSING")
    factors = typed_composition_factors(prior.rhs.generator)
    if factors is None or len(factors) != 3:
        raise RuntimeError("THREE_FACTOR_GENERATOR_REQUIRED")
    prefix = Composition(factors[0], factors[1])
    base = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        prefix, Zero(),
    )
    whole = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        prior.rhs.generator, Zero(),
    )
    if right_zero_transport_inputs(whole, base) != (base,):
        raise RuntimeError("R3R10_TYPE_CONTRACT_NOT_SATISFIED")
    bridge = merge_isolated_cited_source(
        build_shared_typed_bridge(), build_explicit_lemma57_source(ROOT),
    )
    screened = screen_independent_sources_for_derived_goal(bridge, goal=target)
    sources = selected_source_steps(screened, TodaLemma57ExplicitNuPrimeZero)
    if len(sources) != 1:
        raise RuntimeError("LEMMA57_SOURCE_COUNT_DRIFT")
    ordinary = shared_expansion_provider(screened, proof_target=target)
    bound = source_bound_provider(
        ordinary, sources, TodaLemma57ExplicitNuPrimeZero,
        expand_cited_lemma57_explicit_zero,
    )
    cited = tuple(x for x in bound(base) if
                  x.rule.name == "extract explicit nu-prime zero-suspension clause of Toda Lemma 5.7")
    if len(cited) != 1:
        raise RuntimeError("LEMMA57_CANDIDATE_COUNT_DRIFT")
    base_step = derive_from_existing_source(cited[0], sources[0])
    if base_step.rule is not ProofRule.INFERENCE or base_step.conclusion != base:
        raise RuntimeError("LEMMA57_STEP_NOT_INFERRED")
    options = expand_right_zero_transport(whole, base)
    if len(options) != 1 or options[0].rule.name != RULE_NAME:
        raise RuntimeError("R3R10_ZERO_TRANSPORT_NOT_OFFERED")
    if options[0].subgoals != (base,):
        raise RuntimeError("R3R10_SUBGOAL_MISMATCH")
    matches = tuple(find_inference_matches_for_rule(options[0].rule, (base_step,)))
    if len(matches) != 1:
        raise RuntimeError("R3R10_ACTUAL_MATCH_NOT_UNIQUE")
    whole_step = derive_inference_proof_step(matches[0])
    if (whole_step.rule is not ProofRule.INFERENCE
            or whole_step.conclusion != whole
            or whole_step.premises != (base_step,)):
        raise RuntimeError("R3R10_PROOF_ANCESTRY_INVALID")
    return {
        "target": [3, 5], "search_status": result.status.value,
        "open_goals": len(result.open_goals),
        "source_count": len(sources),
        "base_step_inferred": True,
        "isolated_composite_zero_step_inferred": True,
        "isolated_composite_zero_rule": RULE_NAME,
        "isolated_subgoals": [repr(x) for x in options[0].subgoals],
        "shared_composite_zero_candidates": len(ordinary(whole)),
        "no_direct_root_given": True,
        "root_proof_complete": False,
        "production_modified": False,
        "new_given": 0,
        "new_isolated_mathematical_rules": 1,
        "public_mathematical_rules_added": 0,
        "full_pytest": "NOT_RUN",
    }


def worker(timeout: int) -> dict[str, object]:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    try:
        run = subprocess.run((sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"),
                             cwd=ROOT, env=env, capture_output=True, text=True,
                             encoding="utf-8", errors="replace", timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("WORKER_TIMEOUT") from exc
    lines = [line[len(MARKER):] for line in run.stdout.splitlines() if line.startswith(MARKER)]
    if run.returncode or len(lines) != 1:
        raise RuntimeError("WORKER_FAILED: " + str(run.returncode) + " " + run.stderr[-5000:])
    report = json.loads(lines[0])
    if (report.get("root_proof_complete") is not False
            or report.get("new_given") != 0
            or report.get("isolated_composite_zero_step_inferred") is not True):
        raise RuntimeError("FALSE_ISOLATED_PROOF_CLAIM")
    return report


def report_path() -> Path:
    directory = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir()) / "EHPProofTracerAudit" / PACKAGE
    directory.mkdir(parents=True, exist_ok=True)
    return directory / "report.json"


def execute(dry_run: bool, timeout: int) -> int:
    report = {"phase": "176_R3R10", "dry_run": dry_run,
              "timestamp_utc": datetime.now(timezone.utc).isoformat(),
              "gate": "FAIL_R3R10", "full_pytest": "NOT_RUN",
              "new_given": 0, "public_mathematical_rules_added": 0,
              "root_proof_complete": False}
    try:
        report["preflight"] = preflight()
        if not dry_run:
            report["observed"] = worker(timeout)
        report["gate"] = "PASS_R3R10_READ_ONLY_DRYRUN" if dry_run else "PASS_R3R10_ISOLATED_RIGHT_ZERO_TRANSPORT"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-8000:]
    report_path().write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE176_R3R10_GATE=" + report["gate"])
    print("PHASE176_R3R10_REPORT=" + str(report_path()))
    print("PHASE176_R3R10_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "observed" in report:
        row = report["observed"]
        print("PHASE176_R3R10_SOURCE_COUNT=" + str(row["source_count"]))
        print("PHASE176_R3R10_BASE_STEP_INFERRED=" + str(row["base_step_inferred"]))
        print("PHASE176_R3R10_ISOLATED_COMPOSITE_ZERO_STEP_INFERRED=" + str(row["isolated_composite_zero_step_inferred"]))
        print("PHASE176_R3R10_SHARED_COMPOSITE_ZERO_CANDIDATES=" + str(row["shared_composite_zero_candidates"]))
        print("PHASE176_R3R10_GROUP=(3,5) STATUS=" + row["search_status"] + " OPEN=" + str(row["open_goals"]))
    if "error" in report:
        print("PHASE176_R3R10_ERROR=" + report["error"])
    print("PHASE176_R3R10_FULL_PYTEST=NOT_RUN")
    print("(END)")
    return 0 if report["gate"].startswith("PASS_") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()
    if args.worker:
        try:
            print(MARKER + json.dumps(observe(), ensure_ascii=False))
            return 0
        except Exception:
            traceback.print_exc()
            return 1
    return execute(args.dry_run, args.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_rule.py（全文）

```python
"""Focused contracts for the isolated general zero-right-composition rule."""
from __future__ import annotations

from dataclasses import replace
import json

import pytest

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase176_r3r10_right_zero_transport_isolated import audit
from phase176_r3r10_right_zero_transport_isolated.rule import (
    RULE_NAME, expand_right_zero_transport, right_zero_transport_inputs,
    right_zero_transport_rule,
)
from proof import ProofRule, ProofStep, find_inference_matches_for_rule


def fixture():
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    base = GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
                          Composition(a, b), Zero())
    goal = GeneratorImage(TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
                          Composition(a, Composition(b, c)), Zero())
    return base, goal


def test_isolated_rule_infers_actual_proof_step() -> None:
    base, goal = fixture()
    assert right_zero_transport_inputs(goal, base) == (base,)
    options = expand_right_zero_transport(goal, base)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    assert options[0].subgoals == (base,)
    parent = ProofStep(base, (), ProofRule.INFERENCE)
    matches = find_inference_matches_for_rule(options[0].rule, (parent,))
    assert len(matches) == 1
    step = derive_inference_proof_step(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == (parent,)


def test_missing_parent_and_direct_given_rejected() -> None:
    base, goal = fixture()
    rule = right_zero_transport_rule(goal, base)
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (ProofStep(base, (), ProofRule.GIVEN),)) == ()


def test_wrong_prefix_rejected() -> None:
    base, goal = fixture()
    bad = replace(base, source_generator=Composition(base.source_generator.right,
                                                     base.source_generator.left))
    assert right_zero_transport_inputs(goal, bad) is None
    assert expand_right_zero_transport(goal, bad) == ()


def test_wrong_dimension_or_map_rejected() -> None:
    base, goal = fixture()
    bad = replace(base, map=TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(8, 3)))
    assert right_zero_transport_inputs(goal, bad) is None
    bad_goal = replace(goal, map=TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(9, 3)))
    assert right_zero_transport_inputs(bad_goal, base) is None


def test_nonzero_base_and_nonzero_goal_rejected() -> None:
    base, goal = fixture()
    assert right_zero_transport_inputs(goal, replace(base, target_generator=base.source_generator)) is None
    assert right_zero_transport_inputs(replace(goal, target_generator=goal.source_generator), base) is None


def test_different_last_factor_rejected() -> None:
    base, goal = fixture()
    fourth = HomotopyElement("d", dimension=7, source=8, target=7)
    extended = replace(goal, source_generator=Composition(goal.source_generator, fourth),
                       map=TodaSuspensionMap(TodaPrimaryGroup(8, 2), TodaPrimaryGroup(9, 3)))
    assert right_zero_transport_inputs(extended, base) is None


def test_source_contract_fails_closed(tmp_path) -> None:
    for name, anchors in audit.SOURCES.items():
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(anchors), encoding="utf-8")
    assert set(audit.check_sources(tmp_path)) == set(audit.SOURCES)
    (tmp_path / next(iter(audit.SOURCES))).write_text("unrelated", encoding="utf-8")
    with pytest.raises(RuntimeError, match="SOURCE_ANCHOR_MISSING"):
        audit.check_sources(tmp_path)


def test_dry_run_never_executes_worker(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(audit, "preflight", lambda: {"head": "fixture"})
    monkeypatch.setattr(audit, "worker", lambda timeout: pytest.fail("worker started"))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert audit.execute(True, 5) == 0
    report = json.loads((tmp_path / "EHPProofTracerAudit" / audit.PACKAGE / "report.json").read_text(encoding="utf-8"))
    assert report["root_proof_complete"] is False
    assert report["full_pytest"] == "NOT_RUN"
```

## run.ps1（全文）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
$oldAddopts = $env:PYTEST_ADDOPTS
$oldBytecode = $env:PYTHONDONTWRITEBYTECODE
$oldEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTEST_ADDOPTS = "$oldAddopts -p no:cacheprovider".Trim()
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'
    if ($DryRun) {
        python -B -m phase176_r3r10_right_zero_transport_isolated.audit --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3R10 DryRun failed' }
    } else {
        python -B -m pytest -q -p no:cacheprovider phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'R3R10 focused pytest failed' }
        python -B -m phase176_r3r10_right_zero_transport_isolated.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3R10 audit failed' }
    }
} finally {
    $env:PYTEST_ADDOPTS = $oldAddopts
    $env:PYTHONDONTWRITEBYTECODE = $oldBytecode
    $env:PYTHONIOENCODING = $oldEncoding
    Pop-Location
}
```

## 実行する pytest

`python -B -m pytest -q -p no:cacheprovider phase176_r3r10_right_zero_transport_isolated/tests/test_rule.py`

## 次工程

R3R10 は独立した一般推論ステップだけを実証する。公開検索の Root を直接解決する接続、像・核・有限巡回構造の導出は次の Phase の範囲であり、本変更に含めない。
