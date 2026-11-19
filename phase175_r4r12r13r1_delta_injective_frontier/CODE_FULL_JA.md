# Phase 175 R4R12R13R1 コード全文

変更対象は新規監査パッケージ内の `audit.py`、`tests/test_audit.py`、`run.ps1`、`__init__.py` のみ。既存コードは変更しない。

## audit.py

```python
"""Read-only R13R1 audit of the Toda (5.8) Delta-injectivity route.

No proof-tree node, theorem leaf, inference registration or production code is
created. Candidate availability is not a claim that recursive proof succeeds.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import inspect
import json
from pathlib import Path
import subprocess
import sys
import traceback

PACKAGE = "phase175_r4r12r13r1_delta_injective_frontier"
REQUIRED_PATHS = (
    "homotopy_groups.py",
    "phase165_r14_r6_generic_iso.py",
    "phase165_r12_r11_prop42_unified.py",
    "phase165_r12_r12_ehp_consequences.py",
    "phase165_r52_r9_shared_math.py",
    "sources/toda/Toda_05_2.tex",
)


def git(root: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("GIT_FAILED: " + " ".join(arguments) + " " + result.stderr.strip())
    return result.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("WRONG_REPOSITORY_ROOT")
    branch = git(root, "branch", "--show-current")
    if branch != "develop":
        raise RuntimeError("WRONG_BRANCH: " + branch)
    missing = [p for p in REQUIRED_PATHS if not (root / p).is_file()]
    if missing:
        raise RuntimeError("MISSING_REQUIRED_PATHS: " + repr(missing))
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "branch": branch,
        "dirty_tracked_paths": sorted(set(
            git(root, "diff", "--name-only").splitlines()
            + git(root, "diff", "--cached", "--name-only").splitlines()
        )),
    }


def source_formula_present(text: str) -> bool:
    """Check printed equation only; a string match is never a ProofStep."""
    start = text.find(r"\begin{equation}\label{eq:5.8}")
    if start < 0:
        return False
    end = text.find(r"\end{equation}", start)
    if end < 0:
        return False
    normalized = "".join(text[start:end].split())
    return r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" in normalized


def typed_frontier() -> dict[str, object]:
    from homotopy_groups import (
        TodaDeltaMap, TodaEHPExactnessWindow, TodaPrimaryGroup, TodaSuspensionMap,
    )
    from map_facts import EHP_E_MAP, EHP_H_MAP, EHP_DELTA_MAP
    from phase165_r12_r11_prop42_unified import prop42_exactness_indices
    from phase165_r14_r6_generic_iso import MapInjective, MapSurjective
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from toda_rules import TodaProp42ExactnessStatement

    a = TodaPrimaryGroup(9, 9)
    b = TodaPrimaryGroup(7, 4)
    e_src = TodaPrimaryGroup(8, 4)
    e_dst = TodaPrimaryGroup(9, 5)
    h_dst = TodaPrimaryGroup(9, 9)
    delta = TodaDeltaMap(a, b)
    suspension = TodaSuspensionMap(e_src, e_dst)
    h_delta = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=e_dst, middle_term=h_dst, target_term=b,
        first_map=EHP_H_MAP, second_map=EHP_DELTA_MAP,
    ))
    e_h = TodaProp42ExactnessStatement(TodaEHPExactnessWindow(
        source_term=e_src, middle_term=e_dst, target_term=h_dst,
        first_map=EHP_E_MAP, second_map=EHP_H_MAP,
    ))
    indices = (prop42_exactness_indices(h_delta), prop42_exactness_indices(e_h))
    if any(index is None for index in indices):
        raise RuntimeError("EHP_WINDOWS_REJECTED")
    bridge = build_shared_typed_bridge()
    provider = shared_expansion_provider(bridge)
    injective = tuple(provider(MapInjective(delta)))
    surjective = tuple(provider(MapSurjective(suspension)))
    return {
        "delta_goal": repr(MapInjective(delta)),
        "e_goal": repr(MapSurjective(suspension)),
        "h_delta_indices": repr(indices[0]),
        "e_h_indices": repr(indices[1]),
        "delta_injective_candidates": [x.rule.name for x in injective],
        "e_surjective_candidates": [x.rule.name for x in surjective],
        "delta_injective_expansion_count": len(injective),
        "e_surjective_expansion_count": len(surjective),
        "recursive_search_executed": False,
        "candidate_is_verified_proof": False,
    }


def run(root: Path, dry_run: bool) -> int:
    report: dict[str, object] = {
        "phase": "175-R4R12R13R1", "dry_run": dry_run,
        "gate": "FAIL_R13R1_AUDIT", "new_given": 0,
        "new_mathematical_rules": 0, "production_changes": [],
        "full_pytest_executed": False, "pi95_complete": False,
    }
    try:
        report["preflight"] = preflight(root)
        report["toda58_formula_present"] = source_formula_present(
            (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8")
        )
        if not report["toda58_formula_present"]:
            raise RuntimeError("TODA58_FORMULA_NOT_VERIFIED")
        report["frontier"] = typed_frontier()
        report["gate"] = "PASS_R13R1_READ_ONLY_FRONTIER_NOT_COMPLETE"
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
    output = root / PACKAGE / "output"
    output.mkdir(parents=True, exist_ok=True)
    report_path = output / "report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R13R1_GATE=" + str(report["gate"]))
    print("PHASE175_R13R1_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    if "frontier" in report:
        print("PHASE175_R13R1_DELTA_CANDIDATES=" + repr(report["frontier"]["delta_injective_candidates"]))
        print("PHASE175_R13R1_E_CANDIDATES=" + repr(report["frontier"]["e_surjective_candidates"]))
        print("PHASE175_R13R1_EHP_INDICES=" + repr((report["frontier"]["h_delta_indices"], report["frontier"]["e_h_indices"])))
    print("PHASE175_R13R1_NEW_GIVEN=0")
    print("PHASE175_R13R1_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R13R1_REPORT=" + str(report_path))
    if "error" in report:
        print("PHASE175_R13R1_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
```

## tests/test_audit.py

```python
"""Focused read-only R13R1 tests."""
from pathlib import Path
import pytest
from phase175_r4r12r13r1_delta_injective_frontier import audit


def test_toda58_checks_exact_equation_only() -> None:
    good = (r"\begin{equation}\label{eq:5.8}" + "\n"
            + r"\Delta(\iota_9) = \pm(2\nu_4 - E\nu')" + "\n"
            + r"\end{equation}")
    assert audit.source_formula_present(good)
    assert not audit.source_formula_present(good.replace(r"\iota_9", r"\eta_9"))
    assert not audit.source_formula_present(good.replace(r"\label{eq:5.8}", r"\label{eq:5.9}"))


def test_git_failure_is_not_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    class Failed:
        returncode = 1
        stdout = ""
        stderr = "simulated failure"
    monkeypatch.setattr(audit.subprocess, "run", lambda *args, **kwargs: Failed())
    with pytest.raises(RuntimeError, match="GIT_FAILED"):
        audit.git(Path("."), "rev-parse", "HEAD")


def test_required_dependencies_are_explicit() -> None:
    assert "sources/toda/Toda_05_2.tex" in audit.REQUIRED_PATHS
    assert "phase165_r12_r11_prop42_unified.py" in audit.REQUIRED_PATHS
    assert "phase165_r52_r9_shared_math.py" in audit.REQUIRED_PATHS
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$module = 'phase175_r4r12r13r1_delta_injective_frontier.audit'
$arguments = @('-m', $module, '--root', $root)
if ($DryRun) { $arguments += '--dry-run' }
python @arguments
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q phase175_r4r12r13r1_delta_injective_frontier/tests/test_audit.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
exit 0
```

## __init__.py

```python
"""Read-only Phase 175 R13R1 audit package."""
```

