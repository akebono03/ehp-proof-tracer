# R7 新規ファイル全文

## audit.py

```python
"""Read-only layer-by-layer diagnosis of source-backed Toda (5.11) visibility."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import traceback

PACKAGE = "phase175_r4r12r10r1r7_public_visibility_diagnostic"
CITED_RULE = "read cited Toda (5.11) as verified typed Delta equality"
IMAGE_RULE = "proved typed Delta equality implies generator image"


def git(root: Path, *args: str) -> str:
    process = subprocess.run(("git",) + args, cwd=root, capture_output=True,
                             encoding="utf-8", errors="replace", text=True, check=False)
    if process.returncode:
        raise RuntimeError("R7_GIT_FAILED: " + " ".join(args) + ": " + process.stderr)
    return process.stdout.strip()


def count_named(options: tuple[object, ...], name: str) -> int:
    return sum(getattr(getattr(item, "rule", None), "name", None) == name for item in options)


def source_link_state(bridge: object, citation: object) -> dict[str, object]:
    from proof import ProofRule
    from unified_statement_registry import AssertionOrigin
    relevant = []
    for link in bridge.proof_links:
        if getattr(getattr(link, "step", None), "conclusion", None) != citation:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        relevant.append({
            "assertion_id": link.assertion_id,
            "origin": str(assertion.origin),
            "fixed_statement": assertion.origin is AssertionOrigin.FIXED_STATEMENT,
            "step_given": link.step.rule is ProofRule.GIVEN,
            "source_matches_content": assertion.content == citation,
            "reference_id": assertion.reference_id,
            "locator": bridge.registry.reference(assertion.reference_id).locator,
        })
    return {"count": len(relevant), "links": relevant}


def investigate(root: Path) -> dict[str, object]:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    from phase175_r4r12r10r1_cited_511_public.source import CitedToda511, canonical_511, verify_cited_511
    from phase175_r4r12r10r1_cited_511_public.provider import (
        build_cited_511_provider, expand_cited_511, screened_cited_facts,
        same_registered_cited_511,
    )
    from phase175_r4r12r10r1_cited_511_public import installer
    from phase175_r4r12r10r1_cited_511_public.source import build_cited_511_source
    import inspect
    from phase165_r52_r9_shared_math import build_shared_typed_bridge as shared_bridge_fn
    from phase165_r52_r9_shared_math import shared_expansion_provider as shared_provider_fn

    head = git(root, "rev-parse", "HEAD")
    branch = git(root, "branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("R7_WRONG_BRANCH: " + branch)
    target = root / installer.TARGET
    current = target.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
    in_bridge = installer.BRIDGE_INSERT in current
    in_provider = installer.PROVIDER_INSERT in current
    result = {"head": head, "branch": branch,
              "target_dirty": installer.TARGET.as_posix() in git(root, "diff", "--name-only").splitlines(),
              "bridge_insert_present": in_bridge,
              "provider_insert_present": in_provider,
              "source_position": verify_cited_511(root),
              "full_pytest_executed": False,
              "group_complete": False}
    cited = CitedToda511(canonical_511())
    direct_bridge = build_cited_511_source(root)
    result["direct_source"] = source_link_state(direct_bridge, cited)
    prior = exact_prior_database_result(5, 4)
    if prior is None:
        raise RuntimeError("R7_ROOT_DB_UNAVAILABLE")
    cycled = CyclicStructureStatement(prior.lhs, prior.rhs.generator, 2)
    routes = expand_public_two_summand_quotient(cycled, proof_target=prior)
    if len(routes) != 2:
        raise RuntimeError("R7_ORIENTATION_COUNT: " + str(len(routes)))
    delta_goal = routes[1].subgoals[2]
    equation_goal = delta_image_equality(delta_goal)
    result["orientation1_registered_match"] = same_registered_cited_511(equation_goal)
    isolated = tuple(expand_cited_511(equation_goal, (cited,)))
    result["isolated_count"] = count_named(isolated, CITED_RULE)
    bridge = build_shared_typed_bridge()
    result["shared_source"] = source_link_state(bridge, cited)
    screened = screened_cited_facts(bridge)
    result["screened_citation_count"] = screened.count(cited)
    direct_provider = build_cited_511_provider(bridge)
    direct = tuple(direct_provider(equation_goal))
    result["direct_provider_count"] = count_named(direct, CITED_RULE)
    shared_provider = shared_expansion_provider(bridge, proof_target=prior)
    shared_relation = tuple(shared_provider(equation_goal))
    shared_image = tuple(shared_provider(delta_goal))
    result["shared_relation_count"] = count_named(shared_relation, CITED_RULE)
    result["shared_image_count"] = count_named(shared_image, IMAGE_RULE)
    result["shared_relation_names"] = [getattr(x.rule, "name", "") for x in shared_relation][:40]
    result["shared_image_names"] = [getattr(x.rule, "name", "") for x in shared_image][:40]
    result["raw_provider_wired"] = "build_cited_511_provider" in inspect.getsource(shared_provider_fn)
    result["raw_source_wired"] = "build_cited_511_source" in inspect.getsource(shared_bridge_fn)
    result["equation_repr"] = repr(equation_goal)
    result["delta_generator_repr"] = repr(delta_goal)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    root = Path.cwd().resolve()
    output_dir = root / PACKAGE / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_file = output_dir / ("preflight.json" if args.dry_run else "audit_report.json")
    report = {"phase": "175-R4R12R10R1R7", "gate": "FAIL_R7", "dry_run": args.dry_run}
    try:
        report["diagnostic"] = investigate(root)
        report["gate"] = "PASS_R7_PUBLIC_VISIBILITY_DIAGNOSED_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = str(exc)
        report["traceback"] = traceback.format_exc()
    report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R12R10R1R7_GATE=" + report["gate"])
    for key in ("bridge_insert_present", "provider_insert_present", "isolated_count", "screened_citation_count", "direct_provider_count", "shared_relation_count", "shared_image_count", "raw_provider_wired", "raw_source_wired"):
        if key in report.get("diagnostic", {}):
            print("R7_" + key.upper() + "=" + str(report["diagnostic"][key]))
    print("R7_REPORT=" + str(report_file))
    if "error" in report:
        print("R7_ERROR=" + report["error"])
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

```

## tests/test_audit.py

```python
"""Pure diagnostic contract checks, without constructing mathematical evidence."""
from __future__ import annotations
from types import SimpleNamespace
from phase175_r4r12r10r1r7_public_visibility_diagnostic import audit


def test_count_named_exact_name() -> None:
    objects = (SimpleNamespace(rule=SimpleNamespace(name="citation")),
               SimpleNamespace(rule=SimpleNamespace(name="other")),
               SimpleNamespace(rule=SimpleNamespace(name="citation")))
    assert audit.count_named(objects, "citation") == 2
    assert audit.count_named(objects, "missing") == 0


def test_diagnostic_never_declares_group_complete() -> None:
    import inspect
    source = inspect.getsource(audit.investigate)
    assert '"group_complete": False' in source
    assert 'installer.install(' not in source


def test_report_gate_is_diagnostic_only() -> None:
    import inspect
    body = inspect.getsource(audit.main)
    assert "PASS_R7_PUBLIC_VISIBILITY_DIAGNOSED_NOT_COMPLETE" in body
    assert 'group proof complete' not in body


def test_no_git_mutations_in_diagnostic() -> None:
    import inspect
    body = inspect.getsource(audit.investigate)
    for command in ('"reset"', '"checkout"', '"commit"', '"add"'):
        assert command not in body

```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m pytest -q phase175_r4r12r10r1r7_public_visibility_diagnostic/tests/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R7 focused pytest failed' }
    $flags = @()
    if ($DryRun) { $flags += '--dry-run' }
    python -m phase175_r4r12r10r1r7_public_visibility_diagnostic.audit @flags
    if ($LASTEXITCODE -ne 0) { throw 'R7 read-only audit failed' }
} finally { Pop-Location }

```

## README.md

```markdown
# Phase 175 R4R12R10R1R7 — Public Visibility Diagnostic

This is a read-only investigation following an R10R1 DryRun PASS and an execution failure with `R10R1_CITED_511_NOT_PUBLIC`. It does **not** reinstall or modify the shared provider, sources, rules, or previous tests. It records the precise number of citation-bearing source links and proposals available at each layer.

Unzip into the `develop` checkout and run `run.ps1 -DryRun` followed by `run.ps1`. The generated JSON under `output/` distinguishes a missing citation, a screened-out citation, a public wiring issue, or duplicate candidates. This package does not claim that the EHP quotient proof is complete. Full-suite pytest is intentionally not run.

The previously failed R10R1 installer may already have modified `phase165_r52_r9_shared_math.py`; this package deliberately does not undo or repeat that installation.

```

## AUDIT_PLAN_JA.md

```markdown
# Phase 175 R4R12R10R1R7 — 公開候補の階層監査

## 背景

R10R1R6 の DryRun は PASS したが、本実行で `R10R1_CITED_511_NOT_PUBLIC` が発生した。このエラーは共有候補が 0 件、または複数件である場合のいずれも意味する。ログだけでは判断できない。

## 対象ファイル・関数

- 新規 `phase175_r4r12r10r1r7_public_visibility_diagnostic/audit.py`: `git`, `count_named`, `source_link_state`, `investigate`, `main`
- 新規 `tests/test_audit.py`: `test_count_named_exact_name`, `test_diagnostic_never_declares_group_complete`, `test_report_gate_is_diagnostic_only`, `test_no_git_mutations_in_diagnostic`
- 新規 `run.ps1`, `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `__init__.py`
- 既存ファイルの変更なし

## 調査項目

1. Toda (5.11) の直接 Source Bridge での GIVEN リンク
2. 統合した共有 Bridge に残る GIVEN リンク
3. `screened_cited_facts()` が認識した GIVEN
4. 単独の `build_cited_511_provider` の候補
5. 共有 `shared_expansion_provider` での Relation / GeneratorImage 候補
6. 既存 Installer の挿入箇所が現時点のソースに存在するか

## 制約・完了条件

文献とデータベースの証明境界は変更しない。新規 GIVEN=0、新規数学規則=0。本番ファイル編集=0。全体 pytest は実施しない。Gate `PASS_R7_PUBLIC_VISIBILITY_DIAGNOSED_NOT_COMPLETE` は候補数の記録にのみ対応する。

```

## __init__.py

```python
"""Read-only public visibility diagnostics for Toda (5.11)."""

```
