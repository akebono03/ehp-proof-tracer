# Phase 173 R4-R1 — 追加コード全文

以下は新規ファイルの全文である。既存の実装ファイルは変更しない。

## __init__.py

```python
"""Phase 173 R4-R1 read-only proof-dependency audit."""
```

## audit.py

```python
"""Phase 173 R4-R1: read-only inspection of the Toda (5.6) proof boundary.

The report records proof *candidates*, not a constructed ProofStep.  It never
patches the repository, adds GIVENs, or promotes a DB relation into a theorem.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from typing import Any

BASELINE = "a7763513ce18c17f95bf919fa232968134df5f66"
REVIEWED_DEVELOP = "2a3f37cf8e19e06fda5bf19a4abd5a3c2eb81b3f"
REVIEWED_BLOBS = {
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
    "sources/toda/Toda_04_2.tex": "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7",
    "phase165_r52_r9_shared_math.py": "2718c55789af7f442ac2c086d016d3d6f7ca3133",
    "phase165_r52_r16_web_citation_gate.py": "d1138c0450f234b6da761902ed7358b6038a19c8",
    "phase165_r55_nk_only_goal.py": "b207b8169590e634229d412324d857ffb3857939",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase169_r4b_prop44_injectivity/rule.py": "aba4c769f2e6bc9a3359c2f8e4b4fa7d869aac4b",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
}
RULE_NAMES = (
    "toda_prop44_isomorphism_inference_rule",
    "toda_prop56_pi7_4_decomposition_inference_rule",
    "toda_56_nu4_decomposition_integration_inference_rule",
    "toda_56_nu4_prop44_specialization_inference_rule",
    "toda_56_nu4_prop44_isomorphism_inference_rule",
    "toda_56_nu4_decomposition_isomorphism_inference_rule",
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=True,
    )
    return result.stdout.strip()


def verify_audit_only_changes(changes: str) -> list[str]:
    """Accept only added R3 audit artifacts beyond the reviewed R3 baseline."""
    files = []
    for record in changes.splitlines():
        parts = record.split("\t")
        if len(parts) != 2:
            raise RuntimeError("Unexpected Git diff status: " + repr(record))
        status, path = parts
        if (status != "A"
                or not (path.startswith("phase173_r3_portable/")
                        or path.startswith("phase173_r3_frontier_readout/"))
                or "\\" in path or ".." in Path(path).parts):
            raise RuntimeError("Non-audit committed change detected: " + repr(record))
        files.append(path)
    return files


def verify_source_text(chapter5: str, chapter4: str) -> dict[str, Any]:
    """Audit exact cited formulations without asserting they are usable leaves."""
    eq_start = chapter5.index(r"\begin{equation}\label{eq:5.6}")
    eq_end = chapter5.index(r"\end{equation}", eq_start)
    equation = chapter5[eq_start:eq_end]
    required = (
        r"\pi^{\,3}_{i-1}",
        r"\pi^{\,7}_{i}",
        r"\pi_{\,i}^{4}",
        r"\nu_{4}\circ\beta",
        r"\cong",
    )
    if any(token not in equation for token in required):
        raise RuntimeError("Toda (5.6) formula differs from reviewed equation")
    prelude = chapter5[max(0, eq_start - 120):eq_start]
    if "Prop 4.4" not in prelude or "Lem 5.4" not in prelude:
        raise RuntimeError("Toda (5.6) no longer cites Prop 4.4 and Lem 5.4")
    lemma_start = chapter5.find(r"\begin{lemma}\label{lem:5.4}")
    lemma_tokens = (r"H(\nu_{4})=\iota_7", r"2E \nu_{4}=E^{2}\nu'")
    # Toda also repeats Lemma 5.4 in a side-column as a summary; check the chapter.
    if any(token not in chapter5 for token in lemma_tokens):
        raise RuntimeError("Reviewed Lemma 5.4 Hopf/generator conditions absent")
    prop_start = chapter4.index(r"\begin{proposition}\label{prop:4.4}")
    prop_end = chapter4.index(r"\end{proposition}", prop_start)
    prop = chapter4[prop_start:prop_end]
    if not all(token in prop for token in (r"\pit{i-1}{n-1}", r"\pit{i}{2n-1}", "同型")):
        raise RuntimeError("Toda Proposition 4.4 formula differs")
    return {
        "equation": "(5.6)",
        "map": "(alpha,beta) -> E alpha + nu_4 o beta",
        "source_groups": ["pi_(i-1)^3", "pi_i^7"],
        "target_group": "pi_i^4",
        "specialization_i": 7,
        "specialized_source_groups": ["pi_6^3", "pi_7^7"],
        "specialized_target": "pi_7^4",
        "prop44_and_lemma54_required": True,
        "pi77_free_cyclic_proved_here": False,
        "lemma54_statement_found": lemma_start >= 0 or all(t in chapter5 for t in lemma_tokens),
        "source_excerpt_sha256": hashlib.sha256(equation.encode("utf-8")).hexdigest(),
    }


def inspect_named_function(source: str, name: str) -> dict[str, Any]:
    """Extract one full top-level function from a large historical rule module."""
    pattern = re.compile(r"^def " + re.escape(name) + r"\s*\(", flags=re.MULTILINE)
    matches = list(pattern.finditer(source))
    if len(matches) != 1:
        return {"function": name, "defined_exactly_once": False,
                "count": len(matches)}
    begin = matches[0].start()
    following = re.search(r"^(?:def |class |@dataclass\b)", source[matches[0].end():], re.MULTILINE)
    finish = matches[0].end() + following.start() if following else len(source)
    block = source[begin:finish]
    return {
        "function": name,
        "defined_exactly_once": True,
        "line": source.count("\n", 0, begin) + 1,
        "sha256": hashlib.sha256(block.encode("utf-8")).hexdigest(),
        "mentions_premise_pattern": "PremisePattern" in block,
        "mentions_literature_reference": "LiteratureReference" in block,
        "mentions_direct_sum": "DirectSumGroup" in block,
        "mentions_pi77": "pi7_7" in block or "TodaPrimaryGroup(7, 7)" in block,
    }


def preflight(root: Path) -> dict[str, Any]:
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Phase 173 R4-R1 requires develop")
    head = git(root, "rev-parse", "HEAD")
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASELINE, head],
        cwd=root, capture_output=True, check=False,
    )
    if ancestor.returncode != 0:
        raise RuntimeError("The reviewed Phase 173 R3 baseline is not an ancestor")
    additions = verify_audit_only_changes(
        git(root, "diff", "--name-status", "--no-renames", BASELINE, head)
    )
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise RuntimeError("Tracked files are modified; no automatic clean/reset")
    for path, expected in REVIEWED_BLOBS.items():
        actual = git(root, "rev-parse", "HEAD:" + path)
        if actual != expected:
            raise RuntimeError("Reviewed source changed: " + path)
    chapter5 = (root / "sources/toda/Toda_05_2.tex").read_text(encoding="utf-8-sig")
    chapter4 = (root / "sources/toda/Toda_04_2.tex").read_text(encoding="utf-8-sig")
    math = verify_source_text(chapter5, chapter4)
    source = (root / "toda_rules.py").read_text(encoding="utf-8-sig")
    rules = [inspect_named_function(source, name) for name in RULE_NAMES]
    return {
        "head": head,
        "github_reviewed_head": REVIEWED_DEVELOP,
        "equals_reviewed_head": head == REVIEWED_DEVELOP,
        "baseline": BASELINE,
        "committed_audit_additions": additions,
        "reviewed_source_blob_count": len(REVIEWED_BLOBS),
        "toda": math,
        "existing_rule_inventory": rules,
        "untracked_directories_preserved": True,
        "tracked_files_unchanged": True,
    }


def inspect_public_root() -> dict[str, Any]:
    """Reproduce R3's public root inspection for (n,k)=(4,3), without proof search."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase166_r3t_goal_source_binding.goal_source import (
        resolve_specialized_goal_citing_id,
    )
    from phase169_r3m_prior_result_catalog.prior_results import (
        resolve_prior_group_result,
    )
    from phase165_r52_r27_r5_literature import TodaProp44UniversalStatement
    from proof import ProofRule

    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=4, k=3)
    if len(candidates) != 1:
        raise RuntimeError("pi_7^4 must have exactly one typed DB goal")
    goal = candidates[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    if citing is None:
        raise RuntimeError("pi_7^4 lacks uniquely positioned citation")
    screened = screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    screened = prefer_universal_prop42_derivation(screened)
    given_links = [
        link for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    ]
    given = tuple(link.step.conclusion for link in given_links)
    if any(type(item) is type(goal) and item == goal for item in given):
        raise RuntimeError("Target DB goal was incorrectly promoted to GIVEN")
    prop44 = [
        link for link in given_links
        if type(link.step.conclusion) is TodaProp44UniversalStatement
        and link.step.conclusion == TodaProp44UniversalStatement()
    ]
    provider = shared_expansion_provider(screened, proof_target=goal)
    roots = []
    examined_children: list[object] = []
    for option in provider(goal):
        children = []
        for child in option.subgoals:
            available = any(type(s) is type(child) and s == child for s in given)
            item: dict[str, Any] = {
                "type": type(child).__name__,
                "repr": repr(child)[:900],
                "exact_screened_given": available,
            }
            if any(type(old) is type(child) and old == child for old in examined_children):
                item["duplicate_subgoal"] = True
            else:
                examined_children.append(child)
                try:
                    item["immediate_child_rule_names"] = [
                        proposal.rule.name for proposal in provider(child)
                    ]
                except Exception as exc:
                    item["child_probe_error"] = type(exc).__name__ + ": " + str(exc)
            children.append(item)
        roots.append({"rule": option.rule.name, "children": children})
    prior = resolve_prior_group_result(
        screened, source_n=3, source_k=3, citing_assertion_id=citing,
    )
    pi77 = registered_group_goal_candidates(bridge, n=7, k=0)
    return {
        "goal": "pi_7^4 = Z{nu_4} + Z/4{E nu_prime}",
        "source_citing_assertion_id": citing,
        "screened_given_count": len(given),
        "target_is_screened_given": False,
        "prop44_cited_universal_given_count": len(prop44),
        "screened_given_statement_types": sorted({type(statement).__name__ for statement in given}),
        "toda56_decomposition_direct_given_count": sum(
            type(statement).__name__ == "Toda56Nu4DecompositionIsomorphismStatement"
            for statement in given
        ),
        "prior_pi63": {"eligible": prior.eligible, "reason": prior.reason,
                       "source_assertion_id": prior.source_assertion_id,
                       "proven_in_this_audit": False},
        "pi77_db_goal_count": len(pi77),
        "pi77_proven_in_this_audit": False,
        "root_proposals": roots,
        "root_candidate_count": len(roots),
        "discovered_complete_proof": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only Toda (5.6) pi_7^4 audit")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    print("PHASE173_R4_R1_MODE=AUDIT_ONLY")
    report: dict[str, Any] = {
        "phase": "173-R4-R1", "scope": "AUDIT_ONLY",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preflight": preflight(root),
    }
    print("PHASE173_R4_R1_SOURCE_GUARD=PASS")
    if not args.dry_run:
        report["public_root"] = inspect_public_root()
        print("PHASE173_R4_R1_RUNTIME_ROOTS=" + str(
            report["public_root"]["root_candidate_count"]
        ))
    else:
        report["public_root"] = "SKIPPED_DRY_RUN"
    report["status"] = "OBSERVATION_ONLY_NOT_A_PROOF"
    report["production_changes"] = []
    destination = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / (
        "EHPProofTracerRecovery/phase173_r4_r1_audit_only/audit.json"
    )
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R1_REPORT=" + str(destination))
    print("PHASE173_R4_R1_OBSERVATION_IS_NOT_PROOF=True")
    print("PHASE173_R4_R1_TRACKED_UNCHANGED=True")
    print("PHASE173_R4_R1_AUDIT=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## run.ps1

```powershell
param(
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
Push-Location -LiteralPath $root
$oldPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = $root
    Write-Output 'PHASE173_R4_R1_FOCUSED_PYTEST_START'
    & python -m pytest -q '.\phase173_r4_r1_audit_only\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 focused pytest failed' }
    Write-Output 'PHASE173_R4_R1_FOCUSED_PYTEST=PASS'
    $arguments = @('.\phase173_r4_r1_audit_only\audit.py', '--root', $root)
    if ($DryRun) { $arguments += '--dry-run' }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4-R1 audit failed' }
}
finally {
    $env:PYTHONPATH = $oldPythonPath
    Pop-Location
}
```

## tests/test_audit.py

```python
"""Focused tests for the read-only Phase 173 R4-R1 auditor."""
from __future__ import annotations

import pytest

from phase173_r4_r1_audit_only.audit import (
    inspect_named_function,
    verify_audit_only_changes,
    verify_source_text,
)


def test_accepts_only_reviewed_r3_additions() -> None:
    changes = (
        "A\tphase173_r3_portable/audit.py\n"
        "A\tphase173_r3_frontier_readout/readout.py"
    )
    assert verify_audit_only_changes(changes) == [
        "phase173_r3_portable/audit.py",
        "phase173_r3_frontier_readout/readout.py",
    ]


@pytest.mark.parametrize("record", [
    "M\tphase165_r52_r9_shared_math.py",
    "A\tphase173_r4_r1_audit_only/audit.py",
    "D\tphase173_r3_portable/audit.py",
    "A\tphase173_r3_portable/../wrong.py",
    "R100\tphase173_r3_portable/old.py\tphase173_r3_portable/new.py",
])
def test_rejects_unauthorized_changed_paths(record: str) -> None:
    with pytest.raises(RuntimeError):
        verify_audit_only_changes(record)


def test_extracts_one_named_function_without_patching() -> None:
    source = (
        "def f(x):\n"
        "    return x\n\n"
        "def g(y):\n"
        "    return y\n"
    )
    result = inspect_named_function(source, "f")
    assert result["defined_exactly_once"] is True
    assert result["line"] == 1
    assert result["mentions_direct_sum"] is False
    assert inspect_named_function(source, "missing")["defined_exactly_once"] is False


def test_rejects_duplicate_rule_definitions() -> None:
    source = "def f():\n    return 1\ndef f():\n    return 2\n"
    report = inspect_named_function(source, "f")
    assert report["defined_exactly_once"] is False
    assert report["count"] == 2


def test_toda_source_specialization_metadata() -> None:
    chapter5 = (
        "Prop 4.4 とLem 5.4 から,\n"
        "\\begin{equation}\\label{eq:5.6}\n"
        "\\pi^{\\,3}_{i-1}\\oplus\\pi^{\\,7}_{i} "
        "\\xrightarrow{\\cong}\\pi_{\\,i}^{4} "
        "\\nu_{4}\\circ\\beta\n"
        "\\end{equation}\n"
        "\\begin{lemma}\\label{lem:5.4}"
        "H(\\nu_{4})=\\iota_7, 2E \\nu_{4}=E^{2}\\nu'"
    )
    chapter4 = (
        "\\begin{proposition}\\label{prop:4.4}\n"
        "\\pit{i-1}{n-1}\\oplus\\pit{i}{2n-1} X 同型\n"
        "\\end{proposition}"
    )
    report = verify_source_text(chapter5, chapter4)
    assert report["specialization_i"] == 7
    assert report["specialized_source_groups"] == ["pi_6^3", "pi_7^7"]
    assert report["pi77_free_cyclic_proved_here"] is False


def test_rejects_source_without_mandatory_map() -> None:
    chapter5 = (
        "Prop 4.4 とLem 5.4 から,"
        "\\begin{equation}\\label{eq:5.6}"
        "\\pi^{\\,3}_{i-1}\\oplus\\pi^{\\,7}_{i} "
        "\\xrightarrow{\\cong}\\pi_{\\,i}^{4}"
        "\\end{equation}"
    )
    with pytest.raises(RuntimeError, match="equation"):
        verify_source_text(chapter5, "")
```

