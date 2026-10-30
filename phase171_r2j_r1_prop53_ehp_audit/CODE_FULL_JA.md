# Phase 171 R2J-R1 — 完全な新規コード

本番ファイルの変更なし。以下はすべて新規追加ファイルの全文である。

## `audit.py` の全文
```python
"""Phase 171 R2J-R1: read-only Proposition 5.3 / EHP obligation audit.

No group result, map surjectivity, or missing premise is inserted as GIVEN.
R2I remains an independently reconstructed, cited INFERENCE Proof Tree.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from expression import Composition, MapApplication
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaEHPExactnessWindow,
    TodaHopfInvariantMap,
    TodaPrimaryGroup,
)
from map_facts import EHP_DELTA_MAP, EHP_H_MAP
from phase165_r12_r11_prop42_unified import (
    TodaProp42GeneralExactnessStatement,
    expand_cited_prop42_exactness,
    prop42_exactness_indices,
)
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import (
    registered_group_goal_candidates,
    search_group_from_registered_goal,
)
from phase166_r3aj_structured_generator import database_structured_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r2_8_4_generic_specialization.specialization import (
    specialize_registered_higher_stem,
)
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative
from phase171_r2i_eta_hopf_bridge.audit import (
    _screened_context,
    build_cited_r2i_proof,
)
from proof import ProofRule, Relation, RelationType
from toda_rules import TodaDeltaZeroStatement, TodaProp42ExactnessStatement
from unified_statement_registry import AssertionOrigin

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = Path(__file__).resolve().parent / "output"
PROP53_SOURCE = ROOT / "sources" / "toda" / "Toda_05_2.tex"


def _git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def hopf_map() -> TodaHopfInvariantMap:
    return TodaHopfInvariantMap(
        TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 5),
    )


def delta_map() -> TodaDeltaMap:
    return TodaDeltaMap(
        TodaPrimaryGroup(7, 5), TodaPrimaryGroup(5, 2),
    )


def h_delta_exactness_goal() -> TodaProp42ExactnessStatement:
    return TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=TodaPrimaryGroup(7, 3),
        middle_term=TodaPrimaryGroup(7, 5),
        target_term=TodaPrimaryGroup(5, 2),
        first_map=EHP_H_MAP,
        second_map=EHP_DELTA_MAP,
    ))


def _source_claim_audit() -> dict:
    """Check adopted transcription bytes, not historical original-edition provenance."""
    raw = PROP53_SOURCE.read_text(encoding="utf-8-sig")
    start = raw.find(r"\begin{proposition}\label{prop:5.3}")
    end = raw.find(r"\end{proposition}", start)
    if start < 0 or end <= start:
        raise RuntimeError("Toda adopted Proposition 5.3 block is missing")
    body = raw[start:end]
    tokens = (r"\pi^{n}_{n+2}", r"\eta_n^{2}", r"\mathbb Z_2", r"n\ge2")
    if any(token not in body for token in tokens):
        raise RuntimeError("Toda adopted Proposition 5.3 block has changed")
    return {
        "adopted_text_contains_statement": True,
        "locator": "Proposition 5.3",
        "printed_scope": "n >= 2",
        "original_printed_edition_independently_verified": False,
        "audit_does_not_upgrade_registration": True,
    }


def _registry_prop53(bridge, citing: str, screened) -> list[dict]:
    screened_ids = {link.assertion_id for link in screened.proof_links}
    rows = []
    for assertion in bridge.registry._assertions.values():
        ref = bridge.registry.reference(assertion.reference_id)
        if ref.locator != "Proposition 5.3":
            continue
        record = next(
            (r for r in bridge.records if r.assertion_id == assertion.assertion_id),
            None,
        )
        concrete = None
        try:
            concrete = specialize_registered_higher_stem(assertion.content, 5)
        except (ValueError, TypeError):
            concrete = None
        is_pi75 = (
            isinstance(concrete, Relation)
            and concrete.relation_type is RelationType.EQUALITY
            and concrete.lhs == TodaPrimaryGroup(7, 5)
            and isinstance(concrete.rhs, FiniteCyclicGroup)
            and concrete.rhs.order == 2
        )
        rows.append({
            "assertion_id": assertion.assertion_id,
            "content_type": type(assertion.content).__name__,
            "origin": assertion.origin.value,
            "publication_position": ref.publication_position,
            "component_position": assertion.component_position,
            "precedence": precedes_citing_assertion(
                bridge, assertion.assertion_id, citing
            ) if assertion.origin is AssertionOrigin.FIXED_STATEMENT else False,
            "screened_given": assertion.assertion_id in screened_ids,
            "record_detail": None if record is None else record.detail,
            "specializes_to_pi75": is_pi75,
            "specialized_relation": repr(concrete) if is_pi75 else None,
        })
    return rows


def _r2i_report():
    proof, chain, ancestry = build_cited_r2i_proof()
    if (proof.rule is not ProofRule.INFERENCE
            or not isinstance(proof.conclusion.lhs, MapApplication)
            or proof.conclusion.lhs.map != EHP_H_MAP
            or not isinstance(proof.conclusion.rhs, Composition)
            or chain.alpha.source != 6 or chain.alpha.target != 3
            or chain.eta_next.source != 7 or chain.eta_next.target != 6
            or chain.beta.source != 6 or chain.beta.target != 5):
        raise RuntimeError("R2I root does not have the expected EHP type")
    if proof.conclusion != chain.conclusion:
        raise RuntimeError("R2I returned an unexpected Hopf equality")
    return chain, {
        "typed_root_reconstructed": True,
        "root": repr(proof.conclusion),
        "inferences": sum(step.rule is ProofRule.INFERENCE for step in ancestry),
        "given_leaves": sum(step.rule is ProofRule.GIVEN for step in ancestry),
        "pi63_group_proven_by_this_root": False,
    }


def _pi75_status(bridge, expected: Relation) -> dict:
    """Observe an independent search; never import the result as a proof premise."""
    db_candidates = database_structured_group_goal_candidates(n=5, k=2)
    registered_candidates = registered_group_goal_candidates(bridge, n=5, k=2)
    chosen = db_candidates[0] if len(db_candidates) == 1 else (
        registered_candidates[0] if len(registered_candidates) == 1 else None
    )
    out = {
        "db_goal_count": len(db_candidates),
        "registered_goal_count": len(registered_candidates),
        "chosen_goal": repr(chosen),
        "expected_target": repr(expected),
        "generator_exact_identity_with_r2i": bool(
            isinstance(chosen, Relation)
            and isinstance(chosen.rhs, FiniteCyclicGroup)
            and chosen.rhs.generator == expected.rhs.generator
        ),
        "target_structure_compatible": bool(
            isinstance(chosen, Relation)
            and chosen.lhs == expected.lhs
            and isinstance(chosen.rhs, FiniteCyclicGroup)
            and chosen.rhs.order == 2
        ),
        "search_status": "NOT_SEARCHED",
        "trust_boundary_verified": False,
        "eligible_as_imported_proof_in_this_audit": False,
        "open_goals": [],
        "diagnostics": [],
        "verification_error": None,
    }
    if chosen is None:
        return out
    # This result is recorded for diagnosis only. It is NEVER made a GIVEN
    # or supplied to the R2I search or the EHP surjectivity rule.
    context_holder = []
    try:
        search = search_group_from_registered_goal(
            n=5, k=2, bridge=bridge, goal=chosen,
            context_sink=context_holder.append,
        )
    except Exception as error:
        out["search_status"] = "SEARCH_RAISED"
        out["verification_error"] = f"{type(error).__name__}: {error}"
        return out
    out["search_status"] = search.status.value
    out["open_goals"] = [repr(goal) for goal in search.open_goals]
    out["diagnostics"] = [str(message) for message in search.diagnostics]
    if search.status is ProofSearchStatus.COMPLETE:
        citing = resolve_specialized_goal_citing_id(bridge, chosen)
        if not citing or not context_holder:
            out["verification_error"] = "no positioned source/context for completed pi75 search"
        else:
            try:
                verify_proof_tree_for_narrative(
                    search, context_holder[-1], citing_assertion_id=citing,
                )
            except Exception as error:
                out["verification_error"] = f"{type(error).__name__}: {error}"
            else:
                out["trust_boundary_verified"] = True
    return out


def inspect() -> dict:
    """Report evidence and gaps; no Math theorem is certified by this report."""
    if _git("branch", "--show-current") != "develop":
        raise RuntimeError("R2J-R1 audit requires develop; no checkout permitted")
    source = _source_claim_audit()
    chain, r2i = _r2i_report()
    bridge = build_shared_typed_bridge()
    screened, pi63_goal, citing = _screened_context()
    registry_rows = _registry_prop53(bridge, citing, screened)
    eligible_general = [row for row in registry_rows
                        if row["specializes_to_pi75"] and row["precedence"]]
    h = hopf_map()
    delta = delta_map()
    exact = h_delta_exactness_goal()
    indices = prop42_exactness_indices(exact)
    if indices != (2, 7, "h_delta"):
        raise RuntimeError("R2J H->Delta EHP indices are invalid: " + repr(indices))
    source_candidates = [link for link in screened.proof_links
                         if link.step is not None
                         and link.step.rule is ProofRule.GIVEN
                         and link.step.conclusion == TodaProp42GeneralExactnessStatement()]
    source_values = tuple(link.step.conclusion for link in source_candidates)
    proof42 = None
    if len(source_values) == 1:
        proof42 = reconstruct_registered_goal(
            exact, screened, citing,
            lambda goal: expand_cited_prop42_exactness(goal, source_values),
            lookup_mode="typed_reference_publication",
        )
        if (proof42.rule is not ProofRule.INFERENCE
                or proof42.conclusion != exact):
            raise RuntimeError("Prop4.2 exactness specialization not reconstructed")
    surj_options = expand_generic_ehp_hopf_goal(MapSurjective(h))
    expected_delta = TodaDeltaZeroStatement(delta)
    exactness_requires_delta_zero = (
        len(surj_options) == 1
        and surj_options[0].subgoals == (expected_delta, exact)
    )
    if not exactness_requires_delta_zero:
        raise RuntimeError("existing EHP surjectivity direction changed")
    expected_group = Relation(
        TodaPrimaryGroup(7, 5),
        FiniteCyclicGroup(order=2, generator=chain.conclusion.rhs),
        RelationType.EQUALITY,
    )
    pi75 = _pi75_status(bridge, expected_group)
    blockers = []
    if not eligible_general:
        blockers.append("No positioned Proposition 5.3 general pi75 specialization")
    if any("source-unverified" in str(row["record_detail"]).lower()
           for row in eligible_general):
        blockers.append("Proposition 5.3 registration retains SOURCE_UNVERIFIED metadata")
    if not pi75["trust_boundary_verified"]:
        blockers.append("Independent pi75 completion/proof-tree verification not confirmed")
    if not proof42:
        blockers.append("Proposition 4.2 source is not independently screened")
    blockers.append("Cyclic-generator-in-image -> Hopf-surjective typed rule not established here")
    blockers.append("Do not infer Hopf surjectivity from Delta=0 before proving Delta=0")
    return {
        "phase": "171-R2J-R1",
        "mode": "AUDIT_ONLY",
        "git_head": _git("rev-parse", "HEAD"),
        "git_branch": "develop",
        "pi63_goal": repr(pi63_goal),
        "citing_assertion_id": citing,
        "proposition53_source": source,
        "proposition53_rows": registry_rows,
        "positioned_pi75_schema_count": len(eligible_general),
        "r2i": r2i,
        "pi75": pi75,
        "h_map": repr(h),
        "delta_map": repr(delta),
        "h_delta_exactness": {
            "indices": indices,
            "source_count": len(source_values),
            "derived_from_cited_prop42": proof42 is not None,
            "conclusion": repr(exact),
        },
        "existing_h_surjectivity_rule": {
            "name": surj_options[0].rule.name,
            "requires_delta_zero": exactness_requires_delta_zero,
            "subgoals": [repr(q) for q in surj_options[0].subgoals],
            "unsuitable_to_prove_delta_zero_from_h_surjectivity": True,
        },
        "next_obligations": blockers,
        "pi63_group_proven": False,
        "new_given_count": 0,
        "production_modified": False,
        "full_pytest_run": False,
    }


def _markdown(report: dict) -> str:
    pi75 = report["pi75"]
    source = report["h_delta_exactness"]
    lines = [
        "# Phase 171 R2J-R1 — Proposition 5.3・EHP 型付き監査", "",
        f"- HEAD：`{report['git_head']}`",
        "- モード：AUDIT_ONLY（本番コードと既存テストの変更なし）",
        "- R2I 出典付き Hopf 結論：再構成済み",
        f"- Proposition 5.3 の先行・型付き一般式候補：{report['positioned_pi75_schema_count']} 件",
        f"- π₇⁵ 独立検索：`{pi75['search_status']}`",
        f"- π₇⁵ Trust Boundary 検証：`{pi75['trust_boundary_verified']}`",
        f"- Proposition 4.2 の H→Δ 完全列：`{source['derived_from_cited_prop42']}`",
        f"- Hopf 全射を Δ=0 から示す既存規則：`{report['existing_h_surjectivity_rule']['name']}`",
        "", "## 次段階の論証上の課題", "",
    ]
    lines.extend("- " + x for x in report["next_obligations"])
    lines.extend([
        "", "## 信頼境界", "",
        "採用済み翻刻の Proposition 5.3 を検査しても、SOURCE_UNVERIFIED の旧登録を自動で文献証明に昇格させない。",
        "π₇⁵ の DB 結果や独立検索結果は、本監査では GIVEN として再利用しない。",
        "R2I の式、群の巡回生成元の根拠、Hopf 全射性の型付き推論を別々に確認する。",
        "この監査は π₆³ の完成証明を宣言しない。", "",
    ])
    return "\n".join(lines)


def main() -> None:
    before = _git("status", "--porcelain", "--untracked-files=no")
    report = inspect()
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (OUTPUT / "audit.md").write_text(_markdown(report), encoding="utf-8")
    after = _git("status", "--porcelain", "--untracked-files=no")
    if before != after:
        raise RuntimeError("tracked Git status changed during read-only audit")
    print("PHASE171_R2J_R1_R2I_ROOT=PASS", flush=True)
    print("PHASE171_R2J_R1_PROP53_SOURCE=ADOPTED_TEXT_MATCH", flush=True)
    print("PHASE171_R2J_R1_PROP53_POSITIONED=" + str(report["positioned_pi75_schema_count"]), flush=True)
    print("PHASE171_R2J_R1_PI75_SEARCH=" + report["pi75"]["search_status"], flush=True)
    print("PHASE171_R2J_R1_PI75_TRUST_VERIFIED=" + str(report["pi75"]["trust_boundary_verified"]), flush=True)
    print("PHASE171_R2J_R1_PROP42_EXACTNESS=" + str(report["h_delta_exactness"]["derived_from_cited_prop42"]), flush=True)
    print("PHASE171_R2J_R1_SURJ_FROM_DELTA_IS_CIRCULAR_FOR_THIS_GOAL=True", flush=True)
    print("PHASE171_R2J_R1_GIVEN_ADDED=0", flush=True)
    print("PHASE171_R2J_R1_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R1_FULL_PYTEST=False", flush=True)
    print("PHASE171_R2J_R1_RESULT=PASS_AUDIT_ONLY", flush=True)
    print("PHASE171_R2J_R1_REPORT=" + str(OUTPUT / "audit.md"), flush=True)


if __name__ == "__main__":
    main()
```

## `tests/test_audit.py` の全文
```python
"""Focused R2J-R1 tests of EHP indices and the existing inference direction."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prop42_exactness_indices
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r14_r9_ehp_exactness import expand_generic_ehp_hopf_goal
from phase171_r2j_r1_prop53_ehp_audit.audit import (
    _source_claim_audit,
    delta_map,
    h_delta_exactness_goal,
    hopf_map,
)
from toda_rules import TodaDeltaZeroStatement


def test_r2j_earlier_prop53_adopted_source_has_explicit_scope():
    result = _source_claim_audit()
    assert result["adopted_text_contains_statement"] is True
    assert result["printed_scope"] == "n >= 2"
    assert result["original_printed_edition_independently_verified"] is False
    assert result["audit_does_not_upgrade_registration"] is True


def test_r2j_hopf_and_delta_maps_have_compatible_source_targets():
    h = hopf_map()
    delta = delta_map()
    assert h.source_group == TodaPrimaryGroup(7, 3)
    assert h.target_group == delta.source_group == TodaPrimaryGroup(7, 5)
    assert delta.target_group == TodaPrimaryGroup(5, 2)


def test_r2j_h_delta_exactness_is_valid_toda_prop42_window():
    statement = h_delta_exactness_goal()
    assert prop42_exactness_indices(statement) == (2, 7, "h_delta")
    assert statement.window.source_term == TodaPrimaryGroup(7, 3)
    assert statement.window.target_term == TodaPrimaryGroup(5, 2)


def test_r2j_existing_hopf_surjectivity_direction_requires_delta_zero():
    options = expand_generic_ehp_hopf_goal(MapSurjective(hopf_map()))
    assert len(options) == 1
    assert options[0].subgoals == (
        TodaDeltaZeroStatement(delta_map()), h_delta_exactness_goal(),
    )
    assert options[0].rule.name == (
        "EHP: subsequent zero delta and exactness imply Hopf surjectivity"
    )


def test_r2j_mistyped_hopf_map_has_no_generic_ehp_expansion():
    from homotopy_groups import TodaHopfInvariantMap
    wrong = TodaHopfInvariantMap(TodaPrimaryGroup(7, 3), TodaPrimaryGroup(7, 6))
    assert expand_generic_ehp_hopf_goal(MapSurjective(wrong)) == ()
```

## `run.ps1` の全文
```powershell
param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Module = 'phase171_r2j_r1_prop53_ehp_audit'
Push-Location $Root
try {
    $Branch = (& git branch --show-current).Trim()
    if ($LASTEXITCODE -ne 0 -or $Branch -ne 'develop') {
        throw 'R2J-R1 requires existing develop branch; no checkout/reset is performed'
    }
    $Head = (& git rev-parse HEAD).Trim()
    if ($LASTEXITCODE -ne 0) { throw 'git rev-parse failed' }
    foreach ($Needed in @(
        'phase171_r2i_eta_hopf_bridge\audit.py',
        'phase171_r2i_eta_hopf_bridge\source.py',
        'phase171_r2h_prop22_cited_hopf\source.py',
        'phase165_r52_r9_shared_math.py',
        'sources\toda\Toda_05_2.tex'
    )) {
        if (-not (Test-Path (Join-Path $Root $Needed) -PathType Leaf)) {
            throw ('missing expected file: ' + $Needed)
        }
    }
    $Shared = [System.IO.File]::ReadAllText((Join-Path $Root 'phase165_r52_r9_shared_math.py'))
    if (-not $Shared.Contains('expand_cited_eta_hopf_power')) {
        throw 'R2I provider hook not installed; do not overwrite the existing math file'
    }
    Write-Output ('PHASE171_R2J_R1_BRANCH=' + $Branch)
    Write-Output ('PHASE171_R2J_R1_HEAD=' + $Head)
    Write-Output 'PHASE171_R2J_R1_R2I_PRESERVED=PASS'
    Write-Output 'PHASE171_R2J_R1_PREFLIGHT=PASS'
    if ($DryRun) {
        Write-Output 'PHASE171_R2J_R1_RESULT=PASS_DRY_RUN'
        exit 0
    }
    $Before = ((& git status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0) { throw 'git status before audit failed' }
    $env:PYTHONDONTWRITEBYTECODE = '1'
    & python -B -m pytest -q -p no:cacheprovider `
        (Join-Path $Module 'tests\test_audit.py')
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R1 focused pytest failed' }
    Write-Output 'PHASE171_R2J_R1_FOCUSED_PYTEST=PASS'
    & python -B -m phase171_r2j_r1_prop53_ehp_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2J-R1 live audit failed' }
    $After = ((& git status --porcelain --untracked-files=no) -join "`n")
    if ($LASTEXITCODE -ne 0 -or $After -ne $Before) {
        throw 'tracked changes detected; audit must be read-only'
    }
    Write-Output 'PHASE171_R2J_R1_TRACKED_STATUS_UNCHANGED=PASS'
    Write-Output 'PHASE171_R2J_R1_RUN=PASS'
}
finally {
    Pop-Location
}
```

## `__init__.py` の全文
```python
"""Phase 171 R2J-R1: non-mutating proof dependency audit."""
```

## `tests/__init__.py` の全文
```python
"""Targeted R2J-R1 audit regression tests."""
```
