# R43 全コード（新規ファイル全文）

新規ファイルの全文を以下に示す。変更した既存関数 `shared_expansion_provider()` は通常実行直後に検証済み現行ソースから `CHANGED_FUNCTION_FULL.py` に全文を出力し、関数直前までの既存 import 全体を `IMPORTS_FULL.txt` に出力する。変更位置は R41 既存接続直後、`# R4-4 stage4` コメントの直前であり、R43 はその位置に完全な追加 import と関数接続コードを挿入する。

## __init__.py

```python
"""Phase 174 R3-R7-R43: public conditional EHP map property wiring."""
```

## source_guard.py

```python
"""Pin reviewed R42 handoff and both existing conditional EHP rules."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "f604062833ff4dc2756daa96235814983f98fbf2"
REVIEWED_R42_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
TARGET = "phase165_r52_r9_shared_math.py"
BASE_BLOB = "8bb72fe9b3fe22c1917c51971b12338d62be9e9b"
R42_PREFIX = "phase174_r3_r7_r42_canonical_search_frontier_audit/"
PINS = {
    "phase174_r3_r7_r42_canonical_search_frontier_audit/audit.py": "e17f15093dc434eced7755df5769424b86b0cd30",
    "phase174_r3_r7_r42_canonical_search_frontier_audit/tests/test_frontier.py": "412689d808fd5c86f864259a390df8b7d8936603",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "dfa1519c629eef92ca1c5dae265acc050883649b",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca18dc01f072c9738a05f7bdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
}
ANCHOR = "    # R4-4 stage4: exactness-map binding from cited fixed statements only.\n"
INSERT = (
    "    # R43: add only two source-dependent, conditional EHP map-property goals.\n"
    "    # No citation, verified proof, or GIVEN is registered by these providers.\n"
    "    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (\n"
    "        expand_hopf_injective_from_zero_image,\n"
    "    )\n"
    "    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (\n"
    "        expand_upper_delta_surjectivity,\n"
    "    )\n"
    "    extra_providers = (\n"
    "        expand_hopf_injective_from_zero_image,\n"
    "        expand_upper_delta_surjectivity,\n"
    "    ) + tuple(extra_providers)\n"
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True,
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, check=True, capture_output=True,
    ).stdout


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data,
    ).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    canonical = normalize(data)
    return (len(expected) == 40 and expected in (
        blob(data), blob(canonical), blob(canonical.replace(b"\n", b"\r\n")),
    ))


def expected_replacement(original: bytes) -> bytes:
    """Insert only one guardable provider registration, preserving everything else."""
    source = normalize(original)
    anchor = ANCHOR.encode("utf-8")
    inserted = INSERT.encode("utf-8")
    if (not matches_blob(source, BASE_BLOB)
            or source.count(anchor) != 1
            or inserted in source):
        raise RuntimeError("Unexpected shared provider R41 base or insertion anchor")
    return source.replace(anchor, inserted + anchor, 1)


def verify_checkout() -> dict[str, object]:
    """Fail closed unless exactly reviewed R42 history and R43 code state exist."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R43 at the Git repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R43 requires develop branch")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_rows or remote_rows[0] != REVIEWED_R42_HEAD:
        raise RuntimeError("Unreviewed remote HEAD: R42 handoff changed")
    remote = remote_rows[0]
    local = git("rev-parse", "HEAD")
    if local not in (BASE_HEAD, REVIEWED_R42_HEAD):
        raise RuntimeError("Unreviewed local HEAD for R43")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    if local != remote:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote changed during Source Guard")
    status = subprocess.run(
        ("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
        cwd=ROOT, capture_output=True,
    ).returncode
    if status != 0:
        raise RuntimeError("Unreviewed R42 ancestry")
    changed_upstream = tuple(git(
        "diff", "--name-only", BASE_HEAD, remote,
    ).splitlines())
    if (len(changed_upstream) != 11
            or any(not path.startswith(R42_PREFIX) for path in changed_upstream)):
        raise RuntimeError("R42 remote merge changed unrelated files")
    for path, sha in PINS.items():
        p = ROOT / path
        if not p.is_file() or not matches_blob(p.read_bytes(), sha):
            raise RuntimeError("Reviewed source differs: " + path)
    reference = git_bytes("show", "HEAD:" + TARGET)
    if not matches_blob(reference, BASE_BLOB):
        raise RuntimeError("Shared provider source differs from reviewed R41 HEAD")
    expected = expected_replacement(reference)
    current = normalize((ROOT / TARGET).read_bytes())
    if current == normalize(reference):
        mode = "BASELINE"
    elif current == expected:
        mode = "INSTALLED"
    else:
        raise RuntimeError("Shared provider has unreviewed code changes")
    changed = tuple(git("diff", "--name-only").splitlines())
    required = () if mode == "BASELINE" else (TARGET,)
    if changed != required:
        raise RuntimeError("Unexpected tracked working tree edits: " + repr(changed))
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "r42_reviewed_files": len(changed_upstream),
        "reviewed_source_pins": len(PINS) + 1,
        "shared_math_mode": mode,
        "tracked_change": TARGET if mode == "INSTALLED" else "NONE",
        "full_pytest": False,
    }
```

## install.py

```python
"""Guarded atomic installation of two existing generic EHP providers."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
    ROOT, TARGET, expected_replacement, git_bytes, normalize, verify_checkout,
)

PACKAGE = Path(__file__).resolve().parent


def full_changed_function(source: str) -> str:
    """Emit a complete replaceable function rather than an abbreviated diff."""
    marker = "def shared_expansion_provider("
    if source.count(marker) != 1:
        raise RuntimeError("Unexpected shared_expansion_provider definition count")
    start = source.index(marker)
    next_def = source.find("\ndef ", start + len(marker))
    return (source[start:] if next_def < 0 else source[start:next_def]).rstrip() + "\n"


def install(*, dry_run: bool) -> dict[str, object]:
    state = verify_checkout()
    if dry_run:
        state["mode"] = "DRYRUN"
        return state
    target = ROOT / TARGET
    expected = expected_replacement(git_bytes("show", "HEAD:" + TARGET))
    if state["shared_math_mode"] == "BASELINE":
        original = target.read_bytes()
        chosen = expected.replace(b"\n", b"\r\n") if b"\r\n" in original else expected
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=target.parent, prefix="r43_", suffix=".tmp",
                delete=False,
            ) as out:
                temp_path = out.name
                out.write(chosen)
            os.replace(temp_path, target)
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.unlink(temp_path)
    after = verify_checkout()
    if after["shared_math_mode"] != "INSTALLED":
        raise RuntimeError("R43 provider installation could not be verified")
    updated = normalize(target.read_bytes()).decode("utf-8")
    # Documentation artifacts generated from the exact validated replacement.
    (PACKAGE / "CHANGED_FUNCTION_FULL.py").write_text(
        full_changed_function(updated), encoding="utf-8",
    )
    (PACKAGE / "IMPORTS_FULL.txt").write_text(
        updated.split("def shared_expansion_provider(", 1)[0], encoding="utf-8",
    )
    after["mode"] = "INSTALLED"
    after["full_function_emitted"] = True
    return after


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    state = install(dry_run=args.dry_run)
    for key, value in state.items():
        print("PHASE174_R3R7R43_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R43_GATE=PASS_R43_GUARDED_GENERIC_EHP_PROVIDER_INSTALL")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## audit.py

```python
"""Read-only public R5/R37/EHP/zero-image frontier, with scoped real search."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
    verify_checkout,
)


def inspect_public_ehp_frontier() -> dict[str, object]:
    """Verify the public proposals; do not claim a complete root proof."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as ROOT_RULE, ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE, hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE, upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
        RULE_NAME as ZERO_IMAGE_RULE,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        screened_general_law,
    )
    from proof import ProofRule, ProofStep

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    source_laws = screened_general_law(bridge)
    if len(source_laws) != 1:
        raise RuntimeError("The cited source law from Toda (5.9) is missing")
    identifiers = tuple(
        link.assertion_id for link in bridge.proof_links
        if (isinstance(link.step, ProofStep)
            and link.step.rule is ProofRule.GIVEN
            and link.step.conclusion == source_laws[0])
    )
    if len(identifiers) != 1:
        raise RuntimeError("The Toda (5.9) source must have one cited assertion")

    root_subgoals = ehp_zero_inputs(root)
    if root_subgoals is None:
        raise RuntimeError("The typed EHP root contract disappeared")
    upper = root_subgoals[0]
    upper_subgoals = upper_delta_surjectivity_inputs(upper)
    if upper_subgoals is None:
        raise RuntimeError("The R37 generic surjectivity rule is not applicable")
    hopf = upper_subgoals[0]
    hopf_subgoals = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_subgoals is None:
        raise RuntimeError("The R5 generic injectivity rule is not applicable")
    zero_image = hopf_subgoals[0]
    provider = shared_expansion_provider(bridge, proof_target=root)

    def one(goal: object, rule_name: str, expected: tuple[object, ...]):
        options = tuple(x for x in provider(goal)
                        if x.rule.name == rule_name)
        if len(options) != 1 or options[0].subgoals != expected:
            raise RuntimeError("Public conditional expansion differs: " + rule_name)
        return options[0]

    root_expansion = one(root, ROOT_RULE, root_subgoals)
    upper_expansion = one(upper, UPPER_RULE, upper_subgoals)
    hopf_expansion = one(hopf, HOPF_RULE, hopf_subgoals)
    zero_options = tuple(x for x in provider(zero_image)
                         if x.rule.name == ZERO_IMAGE_RULE)
    if len(zero_options) != 1 or len(zero_options[0].subgoals) != 2:
        raise RuntimeError("R41 adopted DB zero-image rule was lost")
    zero_expansion = zero_options[0]
    db_presentation, generator_zero = zero_expansion.subgoals
    db_step = admitted_db_step(db_presentation, proof_target=root, bridge=bridge)
    if (not isinstance(db_step, ProofStep)
            or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("The existing adopted DB prior trust boundary failed")
    if admitted_db_step(db_presentation, proof_target=zero_image, bridge=bridge) is not None:
        raise RuntimeError("Direct map-root DB scope unexpectedly changed")
    if any(link.step is not None
           and link.step.conclusion in (root, upper, hopf, zero_image)
           for link in bridge.proof_links):
        raise RuntimeError("A forbidden direct GIVEN shortcuts the proof chain")

    # A bounded canonical probe observes actual DB admission within the GROUP
    # root scope, but intentionally does not pretend that omitted generator
    # proof branches are a completed proof. No web requests are performed.
    def scoped(candidate: object):
        if candidate == root:
            return (root_expansion,)
        if candidate == upper:
            return (upper_expansion,)
        if candidate == hopf:
            return (hopf_expansion,)
        if candidate == zero_image:
            return (zero_expansion,)
        return ()

    partial = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=identifiers[0],
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    if (partial.status not in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
            or partial.conclusion is not None
            or not any(step.conclusion == db_presentation
                       and step.rule is ProofRule.GIVEN
                       for step in partial.proven_steps)
            or not any(x == generator_zero for x in partial.open_goals)
            or not any(x == upper for x in partial.open_goals)
            or not any(x == root for x in partial.open_goals)):
        raise RuntimeError("Unexpected bounded canonical search observation")

    return {
        "screened_toda59_source_leaves": len(source_laws),
        "public_ehp_root_candidates": 1,
        "public_upper_delta_r37_candidates": 1,
        "public_hopf_injectivity_r5_candidates": 1,
        "public_adopted_db_zero_image_r41_candidates": 1,
        "r37_independent_subgoals": len(upper_subgoals),
        "r5_independent_subgoals": len(hopf_subgoals),
        "root_scoped_db_prior_admitted_by_actual_search": True,
        "direct_zero_image_scope_db_prior_admitted": False,
        "scoped_canonical_search_status": partial.status.value,
        "scoped_canonical_verified_db_prior_steps": sum(
            1 for step in partial.proven_steps
            if step.conclusion == db_presentation and step.rule is ProofRule.GIVEN
        ),
        "scoped_canonical_generator_zero_open": True,
        "r40_isolated_result_not_promoted_to_public_proof": True,
        "new_given_statements": 0,
        "new_mathematical_rules": 0,
        "upper_delta_surjectivity_verified": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
        "gate": "PASS_R43_PUBLIC_R5_R37_CONDITIONAL_EHP_WIRING_ROOT_PENDING",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    state = verify_checkout()
    details = None if args.dry_run else inspect_public_ehp_frontier()
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r43"
    )
    folder.mkdir(parents=True, exist_ok=True)
    dest = folder / ("preflight.json" if args.dry_run else "public_ehp_map_frontier.json")
    gate = "PASS_R43_REVIEWED_R42_PREFLIGHT" if args.dry_run else details["gate"]
    report = {
        "phase": "174-R3-R7-R43", "git_state": state,
        "observed": details, "gate": gate,
    }
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R43_"
    for key, value in state.items():
        print(p + key.upper() + "=" + str(value))
    if details is not None:
        for key, value in details.items():
            if key != "gate":
                print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(dest))
    print(p + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_static.py

```python
"""R43 scope and package integrity; no production math rewrite."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_all_new_modules_parse_without_ellipsis():
    for name in ("__init__.py", "source_guard.py", "install.py", "audit.py"):
        tree = ast.parse((PACKAGE / name).read_text(encoding="utf-8"))
        assert not any(
            isinstance(x, ast.Expr)
            and isinstance(x.value, ast.Constant)
            and x.value.value is Ellipsis
            for x in ast.walk(tree)
        )


def test_r43_wires_only_historical_r5_and_r37_rules():
    from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import INSERT
    assert "expand_hopf_injective_from_zero_image" in INSERT
    assert "expand_upper_delta_surjectivity" in INSERT
    assert "extra_providers" in INSERT
    assert "given_step" not in INSERT
    assert "ProofStep(" not in INSERT
    assert "if n ==" not in INSERT and "if k ==" not in INSERT


def test_runner_supports_dry_run_and_only_focused_tests():
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in script
    assert "--dry-run" in script
    assert "pytest -q --import-mode=importlib" in script
    assert "git reset" not in script and "git clean" not in script
    assert "FULL_PYTEST=False" in script


def test_documentation_and_install_are_present():
    for name in ("README.md", "AUDIT_PLAN_JA.md", "CODE_FULL_JA.md", "TEST_RESULTS_JA.md"):
        assert (PACKAGE / name).is_file()
    assert (PACKAGE / "install.py").is_file()
```

## tests/test_guard.py

```python
"""R43 checked Git patch and fail-closed source constraints."""
from __future__ import annotations

import pytest

from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
    ANCHOR, BASE_BLOB, INSERT, expected_replacement, verify_checkout,
)


def test_r43_uses_only_reviewed_r42_handoff():
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["r42_reviewed_files"] == 11
    assert state["shared_math_mode"] == "INSTALLED"


def test_patch_rejects_unreviewed_or_unpinned_text():
    with pytest.raises(RuntimeError, match="Unexpected shared provider"):
        expected_replacement(b"invalid\n" + ANCHOR.encode("utf-8"))


def test_patch_preserves_exact_single_anchor_and_no_direct_givens():
    from phase174_r3_r7_r43_public_ehp_map_property_wiring.source_guard import (
        ROOT, TARGET, git_bytes, normalize,
    )
    original = git_bytes("show", "HEAD:" + TARGET)
    new = expected_replacement(original)
    assert new.count(INSERT.encode("utf-8")) == 1
    assert new.replace(INSERT.encode("utf-8"), b"", 1) == normalize(original)
    assert b"ProofStep(" not in INSERT.encode("utf-8")
    assert (ROOT / TARGET).is_file()
```

## tests/test_public.py

```python
"""Verify actual public R5/R37 options and bounded canonical-search scope."""
from __future__ import annotations

from phase174_r3_r7_r43_public_ehp_map_property_wiring.audit import (
    inspect_public_ehp_frontier,
)


def test_public_r5_and_r37_conditional_candidates_are_present():
    observed = inspect_public_ehp_frontier()
    assert observed["screened_toda59_source_leaves"] == 1
    assert observed["public_ehp_root_candidates"] == 1
    assert observed["public_upper_delta_r37_candidates"] == 1
    assert observed["public_hopf_injectivity_r5_candidates"] == 1
    assert observed["public_adopted_db_zero_image_r41_candidates"] == 1
    assert observed["r37_independent_subgoals"] == 4
    assert observed["r5_independent_subgoals"] == 2


def test_scoped_search_admits_authentic_db_under_group_root_only():
    observed = inspect_public_ehp_frontier()
    assert observed["root_scoped_db_prior_admitted_by_actual_search"] is True
    assert observed["direct_zero_image_scope_db_prior_admitted"] is False
    assert observed["scoped_canonical_verified_db_prior_steps"] == 1
    assert observed["scoped_canonical_generator_zero_open"] is True
    assert observed["scoped_canonical_search_status"] == "partial"


def test_no_public_root_proof_or_fabricated_source_is_claimed():
    observed = inspect_public_ehp_frontier()
    assert observed["new_given_statements"] == 0
    assert observed["new_mathematical_rules"] == 0
    assert observed["r40_isolated_result_not_promoted_to_public_proof"] is True
    assert observed["upper_delta_surjectivity_verified"] is False
    assert observed["root_complete"] is False
    assert observed["web_http_checked"] is False
    assert observed["full_pytest"] is False
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r43_public_ehp_map_property_wiring.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R43 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R43_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r43_public_ehp_map_property_wiring.install
    if ($LASTEXITCODE -ne 0) { throw 'R43 guarded installation failed' }
    python -B -m phase174_r3_r7_r43_public_ehp_map_property_wiring.audit
    if ($LASTEXITCODE -ne 0) { throw 'R43 public EHP audit failed' }
    $Groups = @(
        @{Name='R43_STATIC'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_static.py'},
        @{Name='R43_GUARD'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_guard.py'},
        @{Name='R43_PUBLIC'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_public.py'},
        @{Name='R41_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R37_UPPER_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'},
        @{Name='R3_EHP_ROOT_REGRESSION'; Path='phase174_r3_r7_r3_ehp_zero_rule/tests/test_rule.py'},
        @{Name='R40_RULE_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R43_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R43 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R43_RUN=PASS'
    Write-Output 'PHASE174_R3R7R43_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
