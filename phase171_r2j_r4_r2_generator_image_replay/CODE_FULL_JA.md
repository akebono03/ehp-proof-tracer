# Phase 171 R2J-R4-R2-R1 — 更新コード全文

## 変更対象

- `phase171_r2j_r4_r2_generator_image_replay/audit.py`：`scoped_provider()`、`main()`（import 変更なし、以下に関数全文）。
- `phase171_r2j_r4_r2_generator_image_replay/tests/test_audit.py`：import 変更があるためモジュール全文（以下）。
- `phase171_r2j_r4_r2_generator_image_replay/README.md`、`監査仕様.md`：全文更新して同梱。
- 本番ファイル、既存本番テスト、全体ドキュメントは変更しない。

## `audit.py` の関数全文

### `scoped_provider()`

```python
def scoped_provider(available: tuple[object, ...]):
    """Use three existing general rules; never offer a group result as GIVEN."""
    if available != (TodaEtaFamilyGeneralDefinition(),):
        raise ValueError("only the cited general eta definition may enter this scope")

    def expand(goal: object):
        # Match the production provider's precedence: a cited, typed eta
        # composite inference takes priority over the generic composition
        # inference.  Offering both can produce two distinct valid proof trees
        # for one goal, which the shared proof search correctly rejects.
        eta_options = expand_cited_eta_generator(goal)
        composite_options = (
            () if eta_options else expand_composite_generator_image(goal)
        )
        return (
            eta_options
            + composite_options
            + expand_cited_eta_definition(goal, available)
        )

    return expand
```

### `main()`

```python
def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    branch = _git("branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R2J-R4-R2 requires develop; no branch changes are made")
    head = _git("rev-parse", "HEAD")
    before = _git("status", "--porcelain", "--untracked-files=no")
    print("PHASE171_R2J_R4_R2_BRANCH=" + branch, flush=True)
    print("PHASE171_R2J_R4_R2_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R2J_R4_R2_RESULT=PASS_DRY_RUN", flush=True)
        return

    report = replay_image()
    if _git("status", "--porcelain", "--untracked-files=no") != before:
        raise RuntimeError("tracked Git state changed during read-only replay")
    OUTPUT.mkdir(exist_ok=True)
    report.update({
        "phase": "171-R2J-R4-R2",
        "mode": "READ_ONLY_INFERENCE_REPLAY",
        "git_head": head,
        "tracked_status_unchanged": True,
        "production_modified": False,
        "full_pytest": False,
    })
    outfile = OUTPUT / "audit.json"
    outfile.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R2J_R4_R2_IMAGE_REPLAY=" + report["status"], flush=True)
    if report["status"] == "UNFINISHED":
        print("PHASE171_R2J_R4_R2_REASON=" + report["reason"], flush=True)
        for index, item in enumerate(report["open_goals"][:12]):
            print("PHASE171_R2J_R4_R2_OPEN_GOAL_" + str(index) + "=" + item, flush=True)
    else:
        print("PHASE171_R2J_R4_R2_INFERENCES=" + str(report["proof_inferences"]), flush=True)
        print("PHASE171_R2J_R4_R2_GIVEN_LEAVES=" + str(report["proof_given_leaves"]), flush=True)
    print("PHASE171_R2J_R4_R2_GIVEN_ADDED=0", flush=True)
    print("PHASE171_R2J_R4_R2_PI63_PROVEN=False", flush=True)
    print("PHASE171_R2J_R4_R2_TRACKED_STATUS_UNCHANGED=PASS", flush=True)
    print("PHASE171_R2J_R4_R2_REPORT=" + str(outfile), flush=True)
    print("PHASE171_R2J_R4_R2_RUN=PASS", flush=True)
```

## `tests/test_audit.py` の全コード（import を含む）

```python
"""Focused replay and negative tests for the typed triple eta suspension."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e5_composite_generator_image.rule import (
    component_image_obligations,
    expand_composite_generator_image,
)
from phase171_r2j_r4_r2_generator_image_replay.audit import (
    proof_ancestry,
    scoped_provider,
)
from proof import ProofRule, ProofStep
from toda_rules import toda_eta_family_definition_statement


def _eta(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="η" + str(n), dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(n: int) -> Composition:
    return Composition(_eta(n), Composition(_eta(n + 1), _eta(n + 2)))


def _image(source: object, target: object) -> GeneratorImage:
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3)),
        source, target,
    )


def test_general_composition_rule_decomposes_triple_eta_suspension():
    goal = _image(_triple(2), _triple(3))
    obligations = component_image_obligations(goal)
    assert obligations is not None and len(obligations) == 2
    first, rest = obligations
    assert first.source_generator == _eta(2)
    assert first.target_generator == _eta(3)
    next_pair = component_image_obligations(rest)
    assert next_pair is not None and len(next_pair) == 2
    assert tuple(node.source_generator for node in next_pair) == (_eta(3), _eta(4))
    assert tuple(node.target_generator for node in next_pair) == (_eta(4), _eta(5))
    assert len(expand_composite_generator_image(goal)) == 1


def test_invalid_composition_or_map_is_rejected():
    goal = _image(_triple(2), _triple(3))
    bad_target = Composition(_eta(3), Composition(_eta(5), _eta(4)))
    assert component_image_obligations(replace(goal, target_generator=bad_target)) is None
    assert component_image_obligations(replace(
        goal,
        map=TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
    )) is None
    assert component_image_obligations(replace(goal, target_generator=_triple(2))) is None


def test_scoped_provider_requires_only_exact_general_definition():
    general = TodaEtaFamilyGeneralDefinition()
    provider = scoped_provider((general,))
    assert callable(provider)
    with pytest.raises(ValueError):
        scoped_provider(())
    with pytest.raises(ValueError):
        scoped_provider((general, general))
    with pytest.raises(ValueError):
        scoped_provider((general, object()))


def test_cyclic_root_cannot_be_conjured_from_composite_rule():
    from homotopy_groups import FiniteCyclicGroup
    from proof import Relation, RelationType
    goal = Relation(
        TodaPrimaryGroup(6, 3), FiniteCyclicGroup(4, _eta(3)),
        RelationType.EQUALITY,
    )
    provider = scoped_provider((TodaEtaFamilyGeneralDefinition(),))
    assert provider(goal) == ()


def test_proof_ancestry_preserves_real_rule_tags():
    leaf = ProofStep(TodaEtaFamilyGeneralDefinition(), (), ProofRule.GIVEN)
    root = ProofStep("inferred consequence", (leaf,), ProofRule.INFERENCE)
    assert proof_ancestry(root) == (root, leaf)
    assert all(step.rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
               for step in proof_ancestry(root))


def test_scoped_provider_prefers_existing_cited_eta_pair_over_generic_rule():
    eta3 = toda_eta_family_definition_statement(3).element
    eta4 = toda_eta_family_definition_statement(4).element
    eta5 = toda_eta_family_definition_statement(5).element
    goal = GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(5, 3), TodaPrimaryGroup(6, 4),
        ),
        Composition(eta3, eta4),
        Composition(eta4, eta5),
    )
    assert len(expand_composite_generator_image(goal)) == 1
    provider = scoped_provider((TodaEtaFamilyGeneralDefinition(),))
    options = provider(goal)
    assert len(options) == 1
    assert options[0].rule.name == "suspension preserves composition of proved eta generators"
    assert all(not isinstance(item, ProofStep) for item in options[0].subgoals)


def test_scoped_provider_uses_generic_rule_for_nested_triple_composition():
    eta2 = toda_eta_family_definition_statement(2).element
    eta3 = toda_eta_family_definition_statement(3).element
    eta4 = toda_eta_family_definition_statement(4).element
    eta5 = toda_eta_family_definition_statement(5).element
    goal = GeneratorImage(
        TodaSuspensionMap(
            TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 3),
        ),
        Composition(eta2, Composition(eta3, eta4)),
        Composition(eta3, Composition(eta4, eta5)),
    )
    provider = scoped_provider((TodaEtaFamilyGeneralDefinition(),))
    options = provider(goal)
    assert len(options) == 1
    assert options[0].rule.name == "suspension preserves composition of separately proved maps"
    assert len(options[0].subgoals) == 2
    assert all(isinstance(item, GeneratorImage) for item in options[0].subgoals)

```

## `run.ps1` の全コード（既存仕様維持）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -B -m phase171_r2j_r4_r2_generator_image_replay.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 preflight failed" }
    if ($DryRun) {
        Write-Output "PHASE171_R2J_R4_R2_RUN=PASS_DRY_RUN"
        exit 0
    }
    python -B -m pytest -q -p no:cacheprovider phase171_r2j_r4_r2_generator_image_replay/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 focused pytest failed" }
    Write-Output "PHASE171_R2J_R4_R2_FOCUSED_PYTEST=PASS"
    python -B -m phase171_r2j_r4_r2_generator_image_replay.audit
    if ($LASTEXITCODE -ne 0) { throw "R2J-R4-R2 proof replay failed" }
    Write-Output "PHASE171_R2J_R4_R2_RESULT=PASS_AUDIT_ONLY"
}
finally {
    Pop-Location
}

```
