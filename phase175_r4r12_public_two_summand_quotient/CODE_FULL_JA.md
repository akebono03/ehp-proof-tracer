# Phase 175 R4R12 — 変更コード・テスト全文

既存 `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` だけを既存関数全文単位で置き換えます。import の変更・既存クラス変更なし。変更後の当該関数およびモジュール全文は DryRun／本実行が保存する `shared_expansion_provider_FULL_AFTER.py` および `phase165_r52_r9_shared_math_FULL_AFTER.py` に出力します。

以下は今回の新規ファイル・新規 import・新規関数・全テスト関数です。省略はありません。追加位置は ZIP に記載したフォルダー内です。

## `provider.py`

```python
"""Source-first public access to the EXISTING general two-summand EHP quotient rule.

Database rows are used only to propose earlier group-structure subgoals.
No proof, Delta value, E-image, surjectivity or group conclusion is asserted.
Two conditional alternatives are intentionally retained: the actual Delta
image must be independently proved before one can complete the quotient.
"""
from __future__ import annotations

from collections.abc import Callable

from homotopy_groups import (
    DirectSumGroup,
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaPrimaryGroup,
    TodaSuspensionMap,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import (
    exact_prior_database_result,
    precedes_db_goal,
)
from phase175_r4r3_two_summand_quotient.rule import (
    expand_two_summand_quotient,
)
from proof import Relation, RelationType


def ordered_summand_inputs(
    goal: object,
    *,
    proof_target: object,
    database_lookup: Callable[[int, int], object] = exact_prior_database_result,
) -> tuple[Relation, Relation] | None:
    """Retrieve only two explicit, genuinely earlier typed DB candidates.

    The rows themselves are NOT ProofSteps. The canonical resolver must still
    admit and verify their independent earlier provenance during search.
    This function has no target-specific dimension branch or generator label.
    """
    if (
        type(goal) is not CyclicStructureStatement
        or type(goal.group) is not TodaPrimaryGroup
        or type(goal.order) is not int
        or goal.order != 2
        or type(proof_target) is not Relation
        or proof_target.relation_type is not RelationType.EQUALITY
        or proof_target.lhs != goal.group
        or proof_target.rhs != FiniteCyclicGroup(2, goal.generator)
    ):
        return None
    q, n = goal.group.group_dimension, goal.group.sphere_dimension
    if not all(type(x) is int for x in (q, n)) or n < 3 or q <= n:
        return None
    middle_n, middle_k = n - 1, q - n
    delta_n, delta_k = 2 * n - 1, (q + 1) - (2 * n - 1)
    if (
        middle_k < 0 or delta_k < 0
        or not precedes_db_goal(middle_n, middle_k, n, q - n)
        or not precedes_db_goal(delta_n, delta_k, n, q - n)
    ):
        return None
    middle = database_lookup(middle_n, middle_k)
    source = database_lookup(delta_n, delta_k)
    if (
        type(middle) is not Relation
        or middle.relation_type is not RelationType.EQUALITY
        or middle.lhs != TodaPrimaryGroup(q - 1, n - 1)
        or type(middle.rhs) is not DirectSumGroup
        or type(middle.rhs.summands) is not tuple
        or len(middle.rhs.summands) != 2
        or any(type(part) is not FiniteCyclicGroup or part.order != 2
               for part in middle.rhs.summands)
        or middle.rhs.summands[0].generator == middle.rhs.summands[1].generator
        or type(source) is not Relation
        or source.relation_type is not RelationType.EQUALITY
        or source.lhs != TodaPrimaryGroup(q + 1, 2 * n - 1)
        or type(source.rhs) is not FiniteCyclicGroup
        or source.rhs.order != 2
    ):
        return None
    return middle, source


def expand_public_two_summand_quotient(
    goal: object,
    *,
    proof_target: object,
    database_lookup: Callable[[int, int], object] = exact_prior_database_result,
) -> tuple[GoalExpansion, ...]:
    """Offer both valid conditional quotient routes, without proving either.

    The published source Delta value and the suspension image must be proved
    by separate typed rules. The correct killed summand is NOT chosen from
    the requested result; both possibilities remain conditional subgoals.
    """
    sources = ordered_summand_inputs(
        goal, proof_target=proof_target, database_lookup=database_lookup,
    )
    if sources is None:
        return ()
    middle, delta_source = sources
    source_group, middle_group = delta_source.lhs, middle.lhs
    delta_map = TodaDeltaMap(source_group, middle_group)
    e_map = TodaSuspensionMap(middle_group, goal.group)
    parts = middle.rhs.summands
    results: list[GoalExpansion] = []
    for killed_index in (0, 1):
        killed = parts[killed_index].generator
        survivor = parts[1 - killed_index].generator
        delta_image = GeneratorImage(
            map=delta_map,
            source_generator=delta_source.rhs.generator,
            target_generator=killed,
        )
        e_image = GeneratorImage(
            map=e_map,
            source_generator=survivor,
            target_generator=goal.generator,
        )
        candidates = expand_two_summand_quotient(
            goal, middle, delta_source, delta_image, e_image,
        )
        for candidate in candidates:
            if candidate not in results:
                results.append(candidate)
    return tuple(results)


def build_public_two_summand_quotient_provider(*, proof_target: object):
    """Inject an ordinary backward candidate into the shared provider chain."""
    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return expand_public_two_summand_quotient(
            goal, proof_target=proof_target,
        )

    return expand
```

## `installer.py`

```python
"""Full-function, guarded R4R12 installation after verified R4R11 wiring.

No mathematical module is edited. Only shared_expansion_provider() changes.
The installer exports the complete updated function and complete updated file.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

from phase175_r4r11_signed_eta_torsion_public import installer as previous

TARGET = Path("phase165_r52_r9_shared_math.py")
HEAD = "abf619040d52aa9fd61c5bca60db81e28912e24d"
FUNCTION = "shared_expansion_provider"
ANCHOR = (
    "    extra_providers = (build_signed_eta_torsion_provider(bridge),) "
    "+ tuple(extra_providers)\n"
)
ADDITION = '''    # Phase 175 R4R12: propose the already-audited generic EHP quotient.
    # All six independent proof obligations remain mandatory.
    from phase175_r4r12_public_two_summand_quotient.provider import (
        build_public_two_summand_quotient_provider,
    )
    extra_providers = (
        build_public_two_summand_quotient_provider(proof_target=proof_target),
    ) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R12_GIT_ERROR: " + " ".join(args)
                           + ": " + result.stderr.strip())
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def function_replacement(original: str) -> tuple[str, str, str]:
    """Recheck the complete R4R11 module before changing a single function."""
    parsed = ast.parse(original)
    functions = [node for node in parsed.body
                 if isinstance(node, ast.FunctionDef) and node.name == FUNCTION]
    if len(functions) != 1:
        raise RuntimeError("R4R12_SHARED_FUNCTION_NOT_UNIQUE")
    fn = functions[0]
    lines = original.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if before.count(ANCHOR) != 1 or before.count(ADDITION) > 1:
        raise RuntimeError("R4R12_ANCHOR_OR_ADDITION_DRIFT")
    # Remove only our own exact addition; R4R11 validates ALL remaining code.
    baseline = original.replace(ADDITION, "", 1) if ADDITION in before else original
    validated, _, _ = previous.function_replacement(baseline)
    if validated != baseline:
        raise RuntimeError("R4R12_R4R11_NOT_INSTALLED")
    after_fn = before if ADDITION in before else before.replace(
        ANCHOR, ANCHOR + ADDITION, 1,
    )
    updated = "".join(lines[:fn.lineno - 1]) + after_fn + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    return updated, after_fn, baseline


def plan(root: Path) -> tuple[Path, bytes, bytes, str]:
    """Preserve the checked-out EOL style and refuse unreviewed committed code."""
    file = root / TARGET
    if not file.is_file():
        raise RuntimeError("R4R12_PRODUCTION_SOURCE_MISSING")
    if git(root, "rev-parse", "HEAD") != HEAD:
        raise RuntimeError("R4R12_UNREVIEWED_HEAD")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != previous.BASE_WORKING_BLOB:
        raise RuntimeError("R4R12_UNREVIEWED_BASE_PRODUCTION")
    original = file.read_bytes()
    normalized = original.replace(b"\r\n", b"\n").decode("utf-8")
    after, entire_fn, _ = function_replacement(normalized)
    payload = after.encode("utf-8")
    if b"\r\n" in original:
        payload = payload.replace(b"\n", b"\r\n")
    return file, original, payload, entire_fn


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    file, before, after, whole_fn = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "shared_expansion_provider_FULL_AFTER.py").write_text(
        whole_fn, encoding="utf-8",
    )
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    if before != after and not dry_run:
        descriptor, temp_name = tempfile.mkstemp(prefix="r4r12_", suffix=".py", dir=file.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(after)
            os.replace(temp_name, file)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    return {
        "production_path": TARGET.as_posix(),
        "patch_required": before != after,
        "patch_applied": before != after and not dry_run,
        "after_git_blob": git_blob_sha(after.replace(b"\r\n", b"\n")),
        "full_function_exported": True,
        "complete_module_exported": True,
    }
```

## `audit.py`

```python
"""R4R12: source-first public candidate for the already-existing EHP quotient.

No new rule, GIVEN, PDF claim, proof certificate or saved root proof is created.
An expansion is an UNPROVED obligation until normal search discharges it.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

from phase175_r4r12_public_two_summand_quotient import installer
from phase175_r4r11_signed_eta_torsion_public.audit import reviewed_eol_blob_matches

PACKAGE = "phase175_r4r12_public_two_summand_quotient"
PRIOR_PACKAGE = "phase175_r4r11_signed_eta_torsion_public"
PRIOR_GATE = "PASS_R4R11_SIGNED_ETA_TORSION_SHARED_CONNECTED_PI95_PENDING"
DRY_GATE = "PASS_R4R12_TWO_SUMMAND_QUOTIENT_DRYRUN"
FINAL_GATE = "PASS_R4R12_TWO_SUMMAND_QUOTIENT_ROOT_CANDIDATE_PI95_PENDING"
HEAD = installer.HEAD
PINNED_COMMITTED = {
    "phase175_r4r3_two_summand_quotient/rule.py": "0fdb4c5efa1f2e66470a0735f58f781aafe18d44",
    "phase165_r12_r2_quotient_rules.py": "2b3e8e0449382e9245ee22f08501e9cede0a5b59",
    "phase165_r12_r24_web_search_connection.py": "71d0c6c365a46e833a2bfe304c771d2e010178ca",
    "phase165_r14_r6_generic_iso.py": "8e8f5a4245f3dbbc5707b3a0042a1274e4b3e6b7",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
}
PINNED_PRIOR_UNTRACKED = {
    "phase175_r4r11_signed_eta_torsion_public/rule.py": "613bcd5049be0ac431c556dfc413c410287e8bf0",
    "phase175_r4r11_signed_eta_torsion_public/provider.py": "a30d0a28ae7cb174d22ff0ac11b611413e8e596b",
    "phase175_r4r11_signed_eta_torsion_public/installer.py": "b113829a0871d788bd41f4c3271d3d3287d394ff",
    "phase175_r4r11_signed_eta_torsion_public/audit.py": "331833f0ea3b3b4474f759b5713b994315f9a5a3",
}


def git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", *args], cwd=root, check=False, capture_output=True,
        text=True, encoding="utf-8", errors="replace",
    )
    if process.returncode:
        raise RuntimeError("R4R12_GIT_FAILED: " + " ".join(args)
                           + " " + process.stderr.strip())
    return process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root.resolve():
        raise RuntimeError("R4R12_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R4R12_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")
    if head != HEAD:
        raise RuntimeError("R4R12_UNREVIEWED_HEAD: " + head)
    changed = sorted(set(
        git(root, "diff", "--name-only").splitlines()
        + git(root, "diff", "--cached", "--name-only").splitlines()
    ))
    if any(path not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for path in changed):
        raise RuntimeError("R4R12_UNREVIEWED_TRACKED_FILE: " + repr(changed))
    for path, sha in PINNED_COMMITTED.items():
        if git(root, "rev-parse", "HEAD:" + path) != sha:
            raise RuntimeError("R4R12_COMMITTED_SOURCE_DRIFT: " + path)
        file = root / path
        if not file.is_file() or not reviewed_eol_blob_matches(file.read_bytes(), sha):
            raise RuntimeError("R4R12_WORKING_SOURCE_DRIFT: " + path)
    for path, sha in PINNED_PRIOR_UNTRACKED.items():
        file = root / path
        if not file.is_file() or not reviewed_eol_blob_matches(file.read_bytes(), sha):
            raise RuntimeError("R4R12_PREVIOUS_MODULE_DRIFT: " + path)
    target, before, after, _ = installer.plan(root)
    if target != root / installer.TARGET:
        raise RuntimeError("R4R12_UNREVIEWED_INSTALL_TARGET")
    return {
        "head": head,
        "changed_tracked": changed,
        "pinned_committed_modules": len(PINNED_COMMITTED),
        "pinned_prior_modules": len(PINNED_PRIOR_UNTRACKED),
        "patch_required": before != after,
        "expected_after_blob": installer.git_blob_sha(after.replace(b"\r\n", b"\n")),
    }


def validate_prior(report: object) -> dict[str, object]:
    if not isinstance(report, dict):
        raise RuntimeError("R4R12_PRIOR_REPORT_NOT_OBJECT")
    expected = {
        "phase": "175-R4R11",
        "dry_run": False,
        "gate": PRIOR_GATE,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    if any(report.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R12_PRIOR_GATE_OR_SCOPE_INVALID")
    before = report.get("preflight")
    public = report.get("public")
    install = report.get("install")
    if (
        not isinstance(before, dict) or before.get("head") != HEAD
        or not isinstance(public, dict)
        or not all(public.get(x) is True for x in (
            "r4r10_signed_delta_route_present",
            "r4r11_exact_delta_route_present",
            "prior_eta7_order_two_route_present",
            "exact_database_generator_identity_reused",
            "three_proof_obligations_preserved",
        ))
        or public.get("group_conclusion_completed") is not False
        or not isinstance(install, dict)
        or install.get("production_path") != installer.TARGET.as_posix()
        or install.get("full_function_exported") is not True
    ):
        raise RuntimeError("R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC")
    return {"r4r11_success_verified": True, "prior_head": before["head"]}


def find_prior(path: Path | None) -> Path:
    if path is not None:
        result = path.expanduser().resolve()
        if not result.is_file():
            raise RuntimeError("R4R12_PRIOR_REPORT_MISSING: " + str(result))
        return result
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(candidate.read_text(encoding="utf-8")))
            return candidate
        except (OSError, ValueError, TypeError, UnicodeError, RuntimeError):
            continue
    raise RuntimeError("R4R12_SUCCESSFUL_R4R11_REPORT_NOT_FOUND: " + str(folder))


def inspect_public_root() -> dict[str, object]:
    """Confirm real typed candidate paths; never replay the six actual proofs."""
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase165_r12_r2_quotient_rules import CyclicStructureStatement
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, verified_db_step,
    )
    from phase175_r4r3_two_summand_quotient.rule import RULE_NAME, two_summand_quotient_inputs
    from phase175_r4r12_public_two_summand_quotient.provider import (
        ordered_summand_inputs, expand_public_two_summand_quotient,
    )
    from proof import ProofStep, Relation, RelationType

    root = exact_prior_database_result(5, 4)
    if (not isinstance(root, Relation)
            or root.relation_type is not RelationType.EQUALITY
            or root.lhs != TodaPrimaryGroup(9, 5)
            or not isinstance(root.rhs, FiniteCyclicGroup)
            or root.rhs.order != 2):
        raise RuntimeError("R4R12_UNEXPECTED_PI95_ROOT_GOAL")
    goal = CyclicStructureStatement(root.lhs, root.rhs.generator, 2)
    sources = ordered_summand_inputs(goal, proof_target=root)
    if sources is None:
        raise RuntimeError("R4R12_ORDERED_EARLIER_DB_CANDIDATES_MISSING")
    middle, source = sources
    for relation in (middle, source):
        admitted = admitted_db_step(relation, proof_target=root)
        if admitted is None or not verified_db_step(admitted, proof_target=root):
            raise RuntimeError("R4R12_INAUTHENTIC_DB_PRIOR")
    initial = expand_public_two_summand_quotient(goal, proof_target=root)
    if not initial:
        raise RuntimeError("R4R12_ISOLATED_ROOT_QUOTIENT_PROPOSAL_MISSING")
    bridge = build_shared_typed_bridge()
    public = shared_expansion_provider(bridge, proof_target=root)
    found = tuple(exp for exp in public(goal) if exp.rule.name == RULE_NAME)
    if not found or any(exp not in initial for exp in found):
        raise RuntimeError("R4R12_PUBLIC_ROOT_QUOTIENT_PROPOSAL_MISSING")
    for exp in found:
        values = exp.subgoals
        if (len(values) != 6 or any(isinstance(item, ProofStep) for item in values)
                or values[0] != middle or values[1] != source
                or two_summand_quotient_inputs(goal, middle, source,
                                               values[2], values[5]) != values):
            raise RuntimeError("R4R12_UNVERIFIED_OR_MALFORMED_SUBGOALS")
    return {
        "target_group": "pi_9^5",
        "earlier_db_candidates": 2,
        "isolated_root_candidates": len(initial),
        "public_root_candidates": len(found),
        "each_candidate_proof_obligations": 6,
        "existing_r4r3_rule_reused": True,
        "new_given": 0,
        "root_group_completed": False,
        "actual_proof_search_executed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    result = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    result.mkdir(parents=True, exist_ok=False)
    return result


def run(root: Path, *, dry_run: bool, prior_report: Path | None) -> int:
    folder = report_folder()
    report = {
        "phase": "175-R4R12",
        "dry_run": dry_run,
        "gate": "FAIL_R4R12_TWO_SUMMAND_QUOTIENT",
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [installer.TARGET.as_posix()],
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        chosen = find_prior(prior_report)
        report["prior_report"] = str(chosen)
        report["prior"] = validate_prior(json.loads(chosen.read_text(encoding="utf-8")))
        report["install"] = installer.install(root, dry_run=dry_run, output=folder)
        report["public"] = None if dry_run else inspect_public_root()
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R12 — 既存一般商群規則の公開接続\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "R4R3 の数学規則を再利用。未解決の6前提は真とみなさない。\n"
        + "π₉⁵ の完成証明は宣言しない。\n", encoding="utf-8",
    )
    print("PHASE175_R4R12_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R12_NEW_GIVEN=0")
    print("PHASE175_R4R12_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R12_ROOT_PROVIDER=" + (
        "CONNECTED" if isinstance(report.get("public"), dict)
        and report["public"].get("public_root_candidates", 0) > 0 else "NOT_CHECKED"
    ))
    print("PHASE175_R4R12_PI95=NOT_COMPLETE")
    print("PHASE175_R4R12_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R12_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R12_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R12_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r11-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_report=args.r4r11_report)


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_provider.py`

```python
"""Regression: existing generic rank-two quotient is only an unproved proposal."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase175_r4r3_two_summand_quotient.rule import (
    RULE_NAME, two_summand_quotient_inputs,
)
from phase175_r4r3_two_summand_quotient.tests.test_rule import fixture
from phase175_r4r12_public_two_summand_quotient.provider import (
    ordered_summand_inputs,
    expand_public_two_summand_quotient,
    build_public_two_summand_quotient_provider,
)
from proof import ProofStep, Relation, RelationType


def sample():
    goal, domain, delta_source, delta_image, suspension_image = fixture()
    root = Relation(goal.group, FiniteCyclicGroup(2, goal.generator))
    prior = {(4, 4): domain, (9, 1): delta_source}
    calls = []

    def lookup(n: int, k: int):
        calls.append((n, k))
        return prior.get((n, k))

    return goal, root, domain, delta_source, lookup, calls


def test_only_two_earlier_db_candidates_are_read() -> None:
    goal, root, middle, source, lookup, calls = sample()
    assert ordered_summand_inputs(goal, proof_target=root, database_lookup=lookup) == (
        middle, source,
    )
    assert calls == [(4, 4), (9, 1)]


def test_two_conditional_routes_preserve_all_six_obligations() -> None:
    goal, root, middle, source, lookup, _ = sample()
    routes = expand_public_two_summand_quotient(
        goal, proof_target=root, database_lookup=lookup,
    )
    assert len(routes) == 2
    assert all(route.rule.name == RULE_NAME for route in routes)
    for option in routes:
        required = option.subgoals
        assert len(required) == 6
        assert required[:2] == (middle, source)
        assert not any(isinstance(item, ProofStep) for item in required)
        assert two_summand_quotient_inputs(
            goal, middle, source, required[2], required[5],
        ) == required
    assert {route.subgoals[2].target_generator for route in routes} == {
        part.generator for part in middle.rhs.summands
    }


def test_proof_target_must_match_actual_group_and_generator() -> None:
    goal, root, _, _, lookup, calls = sample()
    assert not expand_public_two_summand_quotient(
        goal, proof_target=replace(root, lhs=TodaPrimaryGroup(9, 6)),
        database_lookup=lookup,
    )
    assert not expand_public_two_summand_quotient(
        replace(goal, order=4), proof_target=root, database_lookup=lookup,
    )
    assert not expand_public_two_summand_quotient(
        goal, proof_target=None, database_lookup=lookup,
    )
    assert not calls


def test_incomplete_or_forged_prior_data_is_rejected() -> None:
    goal, root, middle, source, lookup, _ = sample()
    malformed = replace(middle, rhs=DirectSumGroup((
        FiniteCyclicGroup(4, middle.rhs.summands[0].generator),
        middle.rhs.summands[1],
    )))
    assert not expand_public_two_summand_quotient(
        goal, proof_target=root,
        database_lookup=lambda n, k: malformed if (n, k) == (4, 4) else source,
    )
    assert not expand_public_two_summand_quotient(
        goal, proof_target=root,
        database_lookup=lambda n, k: middle if (n, k) == (4, 4) else None,
    )
    bad_delta = replace(source, rhs=FiniteCyclicGroup(4, source.rhs.generator))
    assert not expand_public_two_summand_quotient(
        goal, proof_target=root,
        database_lookup=lambda n, k: middle if (n, k) == (4, 4) else bad_delta,
    )


def test_group_relation_is_never_accepted_directly_as_cyclic_goal() -> None:
    goal, root, _, _, lookup, calls = sample()
    assert not expand_public_two_summand_quotient(
        root, proof_target=root, database_lookup=lookup,
    )
    assert not calls


def test_unrelated_concrete_root_is_not_searched_as_earlier_db_prior() -> None:
    goal, root, _, _, lookup, _ = sample()
    target = replace(goal, group=TodaPrimaryGroup(7, 5))
    assert not expand_public_two_summand_quotient(
        target, proof_target=root, database_lookup=lookup,
    )


def test_real_public_builder_does_not_materialize_proof() -> None:
    goal, root, _, _, _, _ = sample()
    factory = build_public_two_summand_quotient_provider(proof_target=root)
    assert callable(factory)
    assert factory("untyped literature text") == ()
    # Under real repository data the two authenticated DB rows are obtained
    # dynamically; proposals remain unproved until the ordinary resolver runs.
    assert all(not isinstance(exp, ProofStep) for exp in factory(goal))
```

## `tests/test_installer.py`

```python
"""Function replacement is AST-scoped, source-validated and idempotent."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r12_public_two_summand_quotient import installer


def miniature() -> str:
    return (
        "from __future__ import annotations\n\n"
        "def untouched():\n    return 17\n\n"
        "def shared_expansion_provider(bridge):\n"
        + installer.ANCHOR
        + "    return bridge\n"
    )


def test_only_entire_shared_function_changes_and_is_idempotent(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        installer.previous, "function_replacement",
        lambda baseline: (baseline, "", baseline),
    )
    original = miniature()
    updated, whole_fn, baseline = installer.function_replacement(original)
    assert baseline == original
    assert updated.count(installer.ADDITION) == 1
    assert updated.count("def untouched()") == 1
    assert "def untouched():\n    return 17" in updated
    assert whole_fn.startswith("def shared_expansion_provider(bridge):")
    assert installer.function_replacement(updated)[:2] == (updated, whole_fn)
    ast.parse(updated)


def test_duplicate_insertion_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        installer.previous, "function_replacement",
        lambda baseline: (baseline, "", baseline),
    )
    original = miniature().replace(installer.ANCHOR, installer.ANCHOR + installer.ADDITION * 2)
    with pytest.raises(RuntimeError, match="R4R12_ANCHOR_OR_ADDITION_DRIFT"):
        installer.function_replacement(original)


def test_unreviewed_prior_module_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        installer.previous, "function_replacement",
        lambda baseline: (baseline + "# fake source drift", "", baseline),
    )
    with pytest.raises(RuntimeError, match="R4R12_R4R11_NOT_INSTALLED"):
        installer.function_replacement(miniature())


def test_missing_target_function_rejected() -> None:
    with pytest.raises(RuntimeError, match="R4R12_SHARED_FUNCTION_NOT_UNIQUE"):
        installer.function_replacement("def untouched():\n    pass\n")


def test_duplicate_function_rejected() -> None:
    with pytest.raises(RuntimeError, match="R4R12_SHARED_FUNCTION_NOT_UNIQUE"):
        installer.function_replacement(miniature() + "\ndef shared_expansion_provider(x):\n    return x\n")
```

## `tests/test_audit.py`

```python
"""Strict R4R11 report, source and full-install gate contracts."""
from __future__ import annotations

from copy import deepcopy

import pytest

from phase175_r4r12_public_two_summand_quotient import audit


def prior_success_report() -> dict[str, object]:
    return {
        "phase": "175-R4R11",
        "dry_run": False,
        "gate": audit.PRIOR_GATE,
        "new_given": 0,
        "new_mathematical_rules": 1,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
        "preflight": {"head": audit.HEAD},
        "public": {
            "r4r10_signed_delta_route_present": True,
            "r4r11_exact_delta_route_present": True,
            "prior_eta7_order_two_route_present": True,
            "exact_database_generator_identity_reused": True,
            "three_proof_obligations_preserved": True,
            "group_conclusion_completed": False,
        },
        "install": {
            "production_path": "phase165_r52_r9_shared_math.py",
            "full_function_exported": True,
        },
    }


def test_prior_success_is_not_a_root_proof_certificate() -> None:
    result = audit.validate_prior(prior_success_report())
    assert result["r4r11_success_verified"]
    assert "pi95_completed" not in result


@pytest.mark.parametrize("field,value", (
    ("gate", "PASS_R4R11_SIGNED_ETA_TORSION_DRYRUN"),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 0),
    ("pi95_proof_complete", True),
    ("full_pytest_executed", True),
    ("prior_proof_search_executed", True),
))
def test_invalid_prior_gate_rejected(field: str, value: object) -> None:
    report = prior_success_report()
    report[field] = value
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior(report)


@pytest.mark.parametrize("field", (
    "r4r10_signed_delta_route_present",
    "r4r11_exact_delta_route_present",
    "prior_eta7_order_two_route_present",
    "exact_database_generator_identity_reused",
    "three_proof_obligations_preserved",
))
def test_no_missing_public_evidence_accepted(field: str) -> None:
    report = deepcopy(prior_success_report())
    report["public"][field] = False
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC"):
        audit.validate_prior(report)


def test_wrong_prior_head_rejected() -> None:
    report = prior_success_report()
    report["preflight"]["head"] = "0" * 40
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC"):
        audit.validate_prior(report)


def test_wrong_production_path_rejected() -> None:
    report = prior_success_report()
    report["install"]["production_path"] = "proof.py"
    with pytest.raises(RuntimeError, match="R4R12_PRIOR_EVIDENCE_NOT_AUTHENTIC"):
        audit.validate_prior(report)
```

## `run.ps1`

```powershell
param(
    [switch] $DryRun,
    [string] $R4R11Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r12_public_two_summand_quotient/tests/test_provider.py',
        'phase175_r4r12_public_two_summand_quotient/tests/test_installer.py',
        'phase175_r4r12_public_two_summand_quotient/tests/test_audit.py',
        'phase175_r4r3_two_summand_quotient/tests/test_rule.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_rule.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_provider.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_installer.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_audit.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 focused pytest failed' }
    Write-Output 'PHASE175_R4R12_FOCUSED_PYTEST=PASS'

    $arguments = @(
        '-B', '-m', 'phase175_r4r12_public_two_summand_quotient.audit',
        '--root', $root
    )
    if ($DryRun) { $arguments += '--dry-run' }
    if ($R4R11Report -ne '') { $arguments += @('--r4r11-report', $R4R11Report) }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R12 public quotient audit failed' }
    Write-Output 'PHASE175_R4R12_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R12_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R12_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
```
