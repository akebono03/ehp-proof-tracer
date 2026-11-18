# Phase 175 R4R12R10R1R2 — 変更コード全文

今回の変更対象: `audit.py` の定数・新規 `validate_reviewed_lineage()`（`verify_git()` の直前に追加）・`verify_git()` 全体、`installer.py` の定数・`plan()` 全体、`tests/test_lineage.py` 新規、`run.ps1` 全体。既存の `tests/test_cited_511.py` は変更なし。

以下は読み替えなしの修正後コードをファイル単位で全文掲載する。import 部分も含む。

## audit.py

```python
"""Source-first (5.11) citation and public-provider wiring audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import traceback

from . import installer

PACKAGE = "phase175_r4r12r10r1_cited_511_public"
REVIEWED_HEAD = "3ec001a59044aeb056ec7190c43c6066eaf5abae"
REVIEWED_R9_HEAD = "bf0d7be3081c61f2feec075a3c82c2004c29bbf2"
REVIEWED_R9_COMMITTED_PATHS = frozenset({
    "phase165_r52_r9_shared_math.py",
    "phase175_r4r12r8_delta_generator_source_audit/AUDIT_PLAN_JA.md",
    "phase175_r4r12r8_delta_generator_source_audit/CODE_FULL_JA.md",
    "phase175_r4r12r8_delta_generator_source_audit/README.md",
    "phase175_r4r12r8_delta_generator_source_audit/__init__.py",
    "phase175_r4r12r8_delta_generator_source_audit/audit.py",
    "phase175_r4r12r8_delta_generator_source_audit/output/audit_report.json",
    "phase175_r4r12r8_delta_generator_source_audit/output/preflight.json",
    "phase175_r4r12r8_delta_generator_source_audit/run.ps1",
    "phase175_r4r12r8_delta_generator_source_audit/tests/test_audit.py",
    "phase175_r4r12r9_delta_generator_image_bridge/AUDIT_PLAN_JA.md",
    "phase175_r4r12r9_delta_generator_image_bridge/CODE_FULL_JA.md",
    "phase175_r4r12r9_delta_generator_image_bridge/README.md",
    "phase175_r4r12r9_delta_generator_image_bridge/__init__.py",
    "phase175_r4r12r9_delta_generator_image_bridge/audit.py",
    "phase175_r4r12r9_delta_generator_image_bridge/installer.py",
    "phase175_r4r12r9_delta_generator_image_bridge/output/SHARED_PROVIDER_FULL_AFTER.py",
    "phase175_r4r12r9_delta_generator_image_bridge/output/audit_report.json",
    "phase175_r4r12r9_delta_generator_image_bridge/output/preflight.json",
    "phase175_r4r12r9_delta_generator_image_bridge/rule.py",
    "phase175_r4r12r9_delta_generator_image_bridge/run.ps1",
    "phase175_r4r12r9_delta_generator_image_bridge/tests/test_lineage.py",
    "phase175_r4r12r9_delta_generator_image_bridge/tests/test_rule.py",
})


def validate_reviewed_lineage(head: str, committed_paths: frozenset[str],
                              ancestor_check: bool, commit_count: int) -> str:
    """Accept only verified HEADs, and the exact R9 commit change-set."""
    if head == REVIEWED_HEAD:
        if committed_paths or commit_count != 0:
            raise RuntimeError("R10R1_UNREVIEWED_OLD_HEAD_DIFF")
        return "R9_LOCAL_PATCH_BEFORE_COMMIT"
    if head == REVIEWED_R9_HEAD:
        if not ancestor_check or commit_count != 1 or committed_paths != REVIEWED_R9_COMMITTED_PATHS:
            raise RuntimeError("R10R1_UNREVIEWED_R9_COMMIT_DIFF")
        return "R9_REVIEWED_COMMITTED"
    raise RuntimeError("R10R1_UNREVIEWED_HEAD: " + head)


def verify_git(root: Path) -> dict[str, object]:
    if Path(installer.git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R10R1_WRONG_ROOT")
    if installer.git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R10R1_WRONG_BRANCH")
    head = installer.git(root, "rev-parse", "HEAD")
    from subprocess import run
    # Require Git to verify the exact reviewed ancestor and one-commit diff.
    ancestor = run(
        ["git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head],
        cwd=root, capture_output=True, check=False,
    ).returncode == 0
    count = int(installer.git(root, "rev-list", "--count", REVIEWED_HEAD + ".." + head))
    paths = frozenset(installer.git(
        root, "diff", "--name-only", REVIEWED_HEAD, head,
    ).splitlines())
    lineage = validate_reviewed_lineage(head, paths, ancestor, count)
    dirty = set(installer.git(root, "diff", "--name-only").splitlines())
    dirty.update(installer.git(root, "diff", "--cached", "--name-only").splitlines())
    if dirty - {str(installer.TARGET), ".pytest_cache/v/cache/nodeids"}:
        raise RuntimeError("R10R1_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(dirty)))
    return {"head": head, "dirty": sorted(dirty), "lineage": lineage}


def inspect(root: Path, *, dry_run: bool) -> dict[str, object]:
    from .provider import expand_cited_511, RULE_NAME
    from .source import CitedToda511, canonical_511, verify_cited_511
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality
    from phase175_r4r12_public_two_summand_quotient.provider import expand_public_two_summand_quotient
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result

    git = verify_git(root)
    position = verify_cited_511(root)
    root_goal = exact_prior_database_result(5, 4)
    cyclic = CyclicStructureStatement(root_goal.lhs, root_goal.rhs.generator, 2)
    options = expand_public_two_summand_quotient(cyclic, proof_target=root_goal)
    if len(options) != 2:
        raise RuntimeError("R10R1_QUOTIENT_ROUTE_DRIFT")
    delta_goal = options[1].subgoals[2]
    if not isinstance(delta_goal, GeneratorImage) or delta_image_equality(delta_goal) != canonical_511():
        raise RuntimeError("R10R1_ORIENTATION1_TYPED_MISMATCH")
    isolated = expand_cited_511(canonical_511(), (CitedToda511(canonical_511()),))
    if len(isolated) != 1 or isolated[0].subgoals != (CitedToda511(canonical_511()),):
        raise RuntimeError("R10R1_CITED_INFERENCE_MISSING")
    output = root / PACKAGE / "output"
    changed = installer.install(root, dry_run=dry_run, output=output)
    public = None
    if not dry_run:
        bridge = build_shared_typed_bridge()
        shared = shared_expansion_provider(bridge, proof_target=root_goal)
        relation_candidates = tuple(shared(canonical_511()))
        selected = [x for x in relation_candidates if x.rule.name == RULE_NAME]
        image_candidates = tuple(shared(delta_goal))
        if len(selected) != 1:
            raise RuntimeError("R10R1_CITED_511_NOT_PUBLIC")
        if not any(x.rule.name == "proved typed Delta equality implies generator image"
                   and x.subgoals == (canonical_511(),) for x in image_candidates):
            raise RuntimeError("R10R1_R9_IMAGE_BRIDGE_NOT_PUBLIC")
        public = {"cited_relation_candidates": len(selected),
                  "generator_image_candidates": len(image_candidates),
                  "cited_subgoal": repr(selected[0].subgoals[0])}
    return {"phase": PACKAGE, "git": git, "source_position": position,
            "installation": changed, "public": public, "new_group_result_given": 0,
            "cited_equation_given": 1, "new_mathematical_rules": 0,
            "full_pytest_executed": False, "group_complete": False,
            "recursive_proof_search_executed": False,
            "gate": "PASS_R4R12R10R1_CITED_511_CONNECTED_PROOF_PENDING"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    root = Path.cwd().resolve()
    output = root / PACKAGE / "output" / ("preflight.json" if args.dry_run else "audit_report.json")
    try:
        result = inspect(root, dry_run=args.dry_run)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("PHASE175_R4R12R10R1_GATE=" + result["gate"])
        print("PHASE175_R4R12R10R1_GROUP_COMPLETE=False")
        print("PHASE175_R4R12R10R1_REPORT=" + str(output))
        return 0
    except Exception as error:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps({"gate": "FAIL_R4R12R10R1", "error": str(error),
                                     "traceback": traceback.format_exc()}, ensure_ascii=False,
                                     indent=2) + "\n", encoding="utf-8")
        print("PHASE175_R4R12R10R1_GATE=FAIL_R4R12R10R1")
        print("PHASE175_R4R12R10R1_ERROR=" + str(error))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## installer.py

```python
"""Only append citation registration/provider to two entire shared functions."""
from __future__ import annotations

import ast
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path("phase165_r52_r9_shared_math.py")
COMMITTED_BLOB = "81d234c31e1af176457a35556045aed78d30b343"
REVIEWED_R9_COMMITTED_BLOB = "83f278ec98512a763cdfba2552c70f972b169eac"
BRIDGE_NAME = "build_shared_typed_bridge"
PROVIDER_NAME = "shared_expansion_provider"
BRIDGE_ANCHOR = '''        sources = sources + (build_cited_58_prop25_sources(),)
'''
BRIDGE_INSERT = '''        # Phase 175 R4R12R10R1: cite Toda (5.11) without re-proving it.
        from phase175_r4r12r10r1_cited_511_public.source import (
            build_cited_511_source,
        )
        sources = sources + (build_cited_511_source(),)
'''
PROVIDER_ANCHOR = '''    # Phase 175 R4R10: screened literature claims produce only open subgoals.
'''
PROVIDER_INSERT = '''    # Phase 175 R4R12R10R1: cited (5.11) becomes an inferred typed equality.
    from phase175_r4r12r10r1_cited_511_public.provider import (
        build_cited_511_provider,
    )
    extra_providers = (build_cited_511_provider(bridge),) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    process = subprocess.run(("git",) + args, cwd=root, capture_output=True,
                             text=True, encoding="utf-8", errors="replace")
    if process.returncode:
        raise RuntimeError("R10R1_GIT_FAILURE: " + process.stderr.strip())
    return process.stdout.strip()


def update_function(module: str, name: str, anchor: str, addition: str) -> tuple[str, str]:
    tree = ast.parse(module)
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(nodes) != 1:
        raise RuntimeError("R10R1_FUNCTION_NOT_UNIQUE " + name)
    node = nodes[0]
    lines = module.splitlines(keepends=True)
    before = "".join(lines[node.lineno - 1:node.end_lineno])
    if before.count(anchor) != 1 or before.count(addition) > 1:
        raise RuntimeError("R10R1_UNREVIEWED_FUNCTION " + name)
    after = before if addition in before else before.replace(anchor, anchor + addition, 1)
    updated = "".join(lines[:node.lineno - 1]) + after + "".join(lines[node.end_lineno:])
    ast.parse(updated)
    return updated, after


def plan(root: Path) -> tuple[bytes, bytes, dict[str, str]]:
    path = root / TARGET
    original = path.read_bytes()
    if b"\n" in original.replace(b"\r\n", b"") and b"\r\n" in original:
        raise RuntimeError("R10R1_MIXED_EOL_REQUIRES_REVIEW")
    committed = git(root, "rev-parse", "HEAD:" + TARGET.as_posix())
    if committed not in (COMMITTED_BLOB, REVIEWED_R9_COMMITTED_BLOB):
        raise RuntimeError("R10R1_UNREVIEWED_COMMITTED_PRODUCTION")
    normalized = original.replace(b"\r\n", b"\n").decode("utf-8")
    from phase175_r4r12r9_delta_generator_image_bridge.installer import replacement as r9_replacement
    r9_expected, _ = r9_replacement(normalized)
    if normalized != r9_expected:
        raise RuntimeError("R10R1_R9_NOT_INSTALLED")
    updated, bridge = update_function(normalized, BRIDGE_NAME, BRIDGE_ANCHOR, BRIDGE_INSERT)
    updated, provider = update_function(updated, PROVIDER_NAME, PROVIDER_ANCHOR, PROVIDER_INSERT)
    eol = b"\r\n" if b"\r\n" in original else b"\n"
    new = updated.encode("utf-8").replace(b"\n", eol) if eol == b"\r\n" else updated.encode("utf-8")
    return original, new, {BRIDGE_NAME: bridge, PROVIDER_NAME: provider}


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    before, after, functions = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    for name, function in functions.items():
        (output / (name + "_FULL_AFTER.py")).write_text(function, encoding="utf-8")
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    if not dry_run and before != after:
        fd, name = tempfile.mkstemp(prefix="r10r1_", suffix=".py", dir=root)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(after)
            os.replace(name, root / TARGET)
        finally:
            if os.path.exists(name):
                os.unlink(name)
    return {"target": str(TARGET), "patch_required": before != after,
            "patch_applied": not dry_run and before != after,
            "whole_functions_exported": sorted(functions)}
```

## tests/test_cited_511.py

```python
"""Focused R4R12R10R1 contracts; no recursive whole-suite search."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r12r10r1_cited_511_public import installer, provider, source
from proof import ProofRule, ProofStep, apply_inference_match, find_inference_matches_for_rule


def test_canonical_citation_matches_typed_delta_orientation() -> None:
    from phase165_r14_r6_generic_iso import GeneratorImage
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from phase175_r4r12r9_delta_generator_image_bridge.rule import delta_image_equality

    equality = source.canonical_511()
    delta = TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4))
    image = GeneratorImage(delta, equality.lhs.expression, equality.rhs)
    assert delta_image_equality(image) == equality


def test_cited_511_requires_exact_given() -> None:
    statement = source.canonical_511()
    citation = source.CitedToda511(statement)
    options = provider.expand_cited_511(statement, (citation,))
    assert len(options) == 1
    assert options[0].subgoals == (citation,)
    assert not provider.expand_cited_511(statement, ())
    assert not provider.expand_cited_511(statement, (citation, citation))
    assert not provider.expand_cited_511(source.CitedToda511(statement), (citation,))


def test_cited_511_inferred_relation_requires_given_parent() -> None:
    statement = source.canonical_511()
    citation = source.CitedToda511(statement)
    expansion = provider.expand_cited_511(statement, (citation,))[0]
    parent = ProofStep(citation, (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(expansion.rule, (parent,))
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == statement
    assert not find_inference_matches_for_rule(
        expansion.rule,
        (ProofStep(citation, (), ProofRule.INFERENCE,
                   inference_rule=expansion.rule),),
    )


def test_source_token_must_be_unique(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    chapter = tmp_path / "Toda_05_2.tex"
    chapter.write_text(source.LABEL + source.FORMULA + r"\end{equation}"
                       + r"\begin{proposition}\label{prop:5.8}"
                       + r"\begin{proposition}\label{prop:5.9}", encoding="utf-8")
    monkeypatch.setattr(source, "vetted_source", lambda path, pin: chapter.read_text(encoding="utf-8"))
    with pytest.raises(RuntimeError, match="SOURCE_ORDER_CHANGED"):
        source.verify_cited_511(tmp_path, tmp_path / "manifest.json")


def test_only_two_entire_functions_are_replaced() -> None:
    # BRIDGE_ANCHOR is indented eight spaces inside the actual if block.
    # A synthetic fixture must preserve that nesting before ast.parse().
    module = (
        "def build_shared_typed_bridge():\n"
        "    if True:\n"
        + installer.BRIDGE_ANCHOR
        + "    return None\n\n"
        + "def shared_expansion_provider():\n"
        + installer.PROVIDER_ANCHOR
        + "    return None\n"
    )
    ast.parse(module)
    after_provider, full_provider = installer.update_function(
        module, installer.PROVIDER_NAME,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_INSERT,
    )
    assert installer.PROVIDER_INSERT in full_provider
    assert after_provider.count(installer.PROVIDER_INSERT) == 1
    assert installer.BRIDGE_INSERT not in after_provider

    updated, full_bridge = installer.update_function(
        after_provider, installer.BRIDGE_NAME,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_INSERT,
    )
    assert installer.BRIDGE_INSERT in full_bridge
    assert updated.count(installer.BRIDGE_INSERT) == 1
    assert updated.count(installer.PROVIDER_INSERT) == 1
    ast.parse(updated)

    again, _ = installer.update_function(
        updated, installer.PROVIDER_NAME,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_INSERT,
    )
    again, _ = installer.update_function(
        again, installer.BRIDGE_NAME,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_INSERT,
    )
    assert again == updated


def test_readme_does_not_claim_group_completion() -> None:
    assert "pi_9^5" not in provider.RULE_NAME
    assert source.REFERENCE_ID == "toda:(5.11)"
```

## tests/test_lineage.py

```python
"""Focused regression contracts for the reviewed R10R1R2 Git handoff."""
from __future__ import annotations

import pytest

from phase175_r4r12r10r1_cited_511_public import audit, installer


def test_reviewed_r9_commit_exact_change_set_is_accepted() -> None:
    assert audit.validate_reviewed_lineage(
        audit.REVIEWED_R9_HEAD, audit.REVIEWED_R9_COMMITTED_PATHS, True, 1,
    ) == "R9_REVIEWED_COMMITTED"
    assert installer.REVIEWED_R9_COMMITTED_BLOB == "83f278ec98512a763cdfba2552c70f972b169eac"


def test_prior_head_is_accepted_only_without_later_commits() -> None:
    assert audit.validate_reviewed_lineage(
        audit.REVIEWED_HEAD, frozenset(), True, 0,
    ) == "R9_LOCAL_PATCH_BEFORE_COMMIT"
    with pytest.raises(RuntimeError, match="OLD_HEAD_DIFF"):
        audit.validate_reviewed_lineage(
            audit.REVIEWED_HEAD, audit.REVIEWED_R9_COMMITTED_PATHS, True, 1,
        )


def test_r9_commit_drift_and_unreviewed_head_are_rejected() -> None:
    with pytest.raises(RuntimeError, match="R9_COMMIT_DIFF"):
        audit.validate_reviewed_lineage(
            audit.REVIEWED_R9_HEAD, frozenset(), True, 1,
        )
    with pytest.raises(RuntimeError, match="R9_COMMIT_DIFF"):
        audit.validate_reviewed_lineage(
            audit.REVIEWED_R9_HEAD, audit.REVIEWED_R9_COMMITTED_PATHS, False, 1,
        )
    with pytest.raises(RuntimeError, match="UNREVIEWED_HEAD"):
        audit.validate_reviewed_lineage("0" * 40, frozenset(), False, 0)
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
python -B -m pytest -q --import-mode=prepend -p no:cacheprovider `
  phase175_r4r12r10r1_cited_511_public/tests/test_cited_511.py `
  phase175_r4r12r10r1_cited_511_public/tests/test_lineage.py
if ($LASTEXITCODE -ne 0) { throw 'R4R12R10R1 focused pytest failed' }
$argsList = @('-B', '-m', 'phase175_r4r12r10r1_cited_511_public.audit')
if ($DryRun) { $argsList += '--dry-run' }
python @argsList
if ($LASTEXITCODE -ne 0) { throw 'R4R12R10R1 source/public audit failed' }
```
