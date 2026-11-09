# R41 コード全文（新規ファイル）


既存の `phase165_r52_r9_shared_math.py` の先頭 import は変更しない。変更された `shared_expansion_provider()` の全文は、Source Guard 後の通常実行で `CHANGED_FUNCTION_FULL.py` に生成する（実際の HEAD から全文を抽出）。`IMPORTS_FULL.txt` には変更対象モジュールの冒頭から関数の手前までを省略せず記録する。


## 既存 `shared_expansion_provider()` の追加箇所

`# R4-4 stage4` の直前。以下のコードだけを追加する。


```python
    # R41: retain DB-prior provenance and the actual cited source boundary.
    # This only proposes an inference; it never registers a proof or GIVEN.
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider,
    )
    extra_providers = (
        build_public_adopted_zero_image_provider(
            bridge=bridge, proof_target=proof_target,
        ),
    ) + tuple(extra_providers)
```


## provider.py

```python
"""Cited, root-scoped public connection of R40's verified adopted-DB rule.

No DB result is converted to an independent literature theorem. The R38
source-bound chain remains the prerequisite selector, and the R40 rule
re-checks prior admission at every actual inference match.
"""
from __future__ import annotations

from typing import Callable

from homotopy_groups import TodaPrimaryGroup
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e4_ordered_db_prior.db_prior import group_coordinates
from phase174_r3_r7_r12_toda59_annihilator_source.source import (
    CitedFamilyAnnihilator,
    reviewed_toda59_annihilator_schema,
)
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
    expand_source_bound_zero_image_chain,
)
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import (
    expand_adopted_prior_zero_image,
)
from proof import ProofRule, ProofStep
from unified_statement_registry import AssertionOrigin

PROVIDER_ID = "phase174.r3.r7.r41.cited_adopted_db_zero_image"
SOURCE_LOCATOR = "(5.9)"


def screened_general_law(bridge: RegistryBridgeResult) -> tuple[CitedFamilyAnnihilator, ...]:
    """Require the actual fixed-source, citation-linked Toda (5.9) GIVEN."""
    if not isinstance(bridge, RegistryBridgeResult):
        return ()
    expected = reviewed_toda59_annihilator_schema()
    laws = []
    for link in bridge.proof_links:
        step = link.step
        if (not isinstance(step, ProofStep)
                or step.rule is not ProofRule.GIVEN
                or step.premises
                or type(step.conclusion) is not CitedFamilyAnnihilator
                or step.conclusion != expected):
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        reference = bridge.registry.reference(assertion.reference_id)
        cited = getattr(getattr(step, "inference_rule", None), "literature_reference", None)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or assertion.content != step.conclusion
                or reference.locator != SOURCE_LOCATOR
                or type(reference.publication_position) is not int
                or reference.publication_position < 1
                or cited is None or cited.locator != SOURCE_LOCATOR):
            continue
        laws.append(step.conclusion)
    return tuple(laws) if len(laws) == 1 else ()


def build_public_adopted_zero_image_provider(
    *, bridge: RegistryBridgeResult, proof_target: object,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Return an inert provider unless the root and the source are legitimate.

    Never use a database result to select a final root. Only the caller's
    independently specified group proof root controls the prior-order check.
    """
    lawful = (isinstance(bridge, RegistryBridgeResult)
              and group_coordinates(proof_target) is not None)
    sources = screened_general_law(bridge) if lawful else ()

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if not sources or not isinstance(goal, ImageZeroStatement):
            return ()
        mapping = goal.map
        if (not isinstance(getattr(mapping, "source_group", None), TodaPrimaryGroup)
                or not isinstance(getattr(mapping, "target_group", None), TodaPrimaryGroup)):
            return ()
        # Source-first: R38 must independently propose this exact typed
        # cyclic presentation and generator-image goal from the cited law.
        screened = expand_source_bound_zero_image_chain(goal, sources)
        if len(screened) != 1 or len(screened[0].subgoals) != 2:
            return ()
        presentation, zero_generator = screened[0].subgoals
        proposed = expand_adopted_prior_zero_image(
            goal, presentation, proof_target=proof_target, bridge=bridge,
        )
        if (len(proposed) != 1
                or proposed[0].subgoals != (presentation, zero_generator)):
            return ()
        return proposed

    return expand
```


## source_guard.py

```python
"""Source-first pinned Git and R40/R40R1 preconditions for R41 public wiring."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
TARGET = "phase165_r52_r9_shared_math.py"
BASE_HEAD = "df93c0516dff64cddfebdac69d9755058322cdec"
BASE_BLOB = "6b965aa49db2ad8707c75dcc953d3c78cdd3e458"
UPSTREAM_PREFIXES = (
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/",
    "phase174_r3_r7_r40r1_matcher_order_test_fix/",
)
GIT_BLOB_PINS = {
    "phase165_r6_2_unified_registry_r3_r4/context_provider_registry.py": "a1afa3f733e7dd324cb827ad7a1f6cb6ee90cf40",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
    "phase174_r3_r7_r39_verified_zero_image_frontier/audit.py": "1e3b589bb221daa32c9ee1d21fb10a6dedcd2333",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}
SHA256_PINS = {
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "2df41f2787b76d8d35852c7de2300b90b5391cf9cadbc27b15bc62b122907a83",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/audit.py": "a838e53ca442a523c48a891a071b1860547d418e3c49476de545b6d84f13e0d5",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py": "dabd332aa0cbf036e55e9aacfe992d2a87ef50db9e296780246d3c3d066d4cf8",
}
ANCHOR = "    # R4-4 stage4: exactness-map binding from cited fixed statements only.\n"
INSERT = (
    "    # R41: retain DB-prior provenance and the actual cited source boundary.\n"
    "    # This only proposes an inference; it never registers a proof or GIVEN.\n"
    "    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (\n"
    "        build_public_adopted_zero_image_provider,\n"
    "    )\n"
    "    extra_providers = (\n"
    "        build_public_adopted_zero_image_provider(\n"
    "            bridge=bridge, proof_target=proof_target,\n"
    "        ),\n"
    "    ) + tuple(extra_providers)\n"
)


def git(*args: str) -> str:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(("git",) + args, cwd=ROOT, check=True,
                          capture_output=True).stdout


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    data_lf = normalized(data)
    return len(expected) == 40 and expected in (
        blob(data), blob(data_lf), blob(data_lf.replace(b"\n", b"\r\n")),
    )


def expected_replacement(baseline: bytes) -> bytes:
    """Patch exactly one inspected anchor, without touching surrounding code."""
    original = normalized(baseline)
    anchor = ANCHOR.encode("utf-8")
    if (not matches_blob(original, BASE_BLOB)
            or original.count(anchor) != 1
            or INSERT.encode("utf-8") in original):
        raise RuntimeError("Unreviewed or ambiguous shared provider anchor")
    return original.replace(anchor, INSERT.encode("utf-8") + anchor, 1)


def verified_state() -> dict[str, object]:
    """Refuse unrelated changes or source edits; allow only R40 merge lineage."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R41 in the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R41 requires develop branch")
    local = git("rev-parse", "HEAD")
    remote_rows = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_rows:
        raise RuntimeError("Cannot verify origin/develop")
    remote = remote_rows[0]
    if remote != BASE_HEAD:
        git("fetch", "-q", "origin", "develop")
        if git("rev-parse", "FETCH_HEAD") != remote:
            raise RuntimeError("Remote lineage changed during check")
        if subprocess.run(("git", "merge-base", "--is-ancestor", BASE_HEAD, remote),
                          cwd=ROOT, capture_output=True).returncode != 0:
            raise RuntimeError("Unreviewed remote ancestry")
        changed = tuple(git("diff", "--name-only", BASE_HEAD, remote).splitlines())
        if not changed or any(not name.startswith(UPSTREAM_PREFIXES) for name in changed):
            raise RuntimeError("Remote advanced outside reviewed R40/R40R1 package")
    if local not in (BASE_HEAD, remote):
        raise RuntimeError("Unreviewed local HEAD")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require separate review")
    modified = tuple(git("diff", "--name-only").splitlines())
    if modified not in ((), (TARGET,)):
        raise RuntimeError("Unexpected tracked working-tree changes: " + repr(modified))
    for path, expected in GIT_BLOB_PINS.items():
        file = ROOT / path
        if not file.is_file() or not matches_blob(file.read_bytes(), expected):
            raise RuntimeError("Pinned source differs: " + path)
    for path, expected in SHA256_PINS.items():
        file = ROOT / path
        if (not file.is_file()
                or hashlib.sha256(normalized(file.read_bytes())).hexdigest() != expected):
            raise RuntimeError("R40/R40R1 reviewed file differs: " + path)
    baseline = git_bytes("show", "HEAD:" + TARGET)
    if not matches_blob(baseline, BASE_BLOB):
        raise RuntimeError("Shared math baseline differs from GitHub reviewed blob")
    expected = expected_replacement(baseline)
    current = normalized((ROOT / TARGET).read_bytes())
    base_lf = normalized(baseline)
    if current == base_lf:
        mode = "BASELINE"
    elif current == expected:
        mode = "INSTALLED"
    else:
        raise RuntimeError("Shared math differs from approved original or R41 replacement")
    if (mode == "BASELINE" and modified
            or mode == "INSTALLED" and modified != (TARGET,)):
        raise RuntimeError("Unexpected index/working-tree change state")
    return {
        "local_head": local,
        "remote_head": remote,
        "source_guard": "PASS",
        "shared_math_mode": mode,
        "expected_change": TARGET,
        "reviewed_git_blobs": len(GIT_BLOB_PINS) + 1,
        "reviewed_r40_sha256_files": len(SHA256_PINS),
        "full_pytest": False,
    }
```


## install.py

```python
"""Install only the reviewed R41 shared-provider connection, atomically."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import (
    ROOT, TARGET, expected_replacement, git_bytes, normalized, verified_state,
)

PACKAGE = Path(__file__).resolve().parent


def full_changed_function(source: str) -> str:
    """Extract the whole modified callable for user inspection, never snippets."""
    anchor = "def shared_expansion_provider("
    if source.count(anchor) != 1:
        raise RuntimeError("Unexpected shared_expansion_provider definition count")
    start = source.index(anchor)
    next_def = source.find("\ndef ", start + len(anchor))
    return (source[start:] if next_def < 0 else source[start:next_def]).rstrip() + "\n"


def install(*, dry_run: bool) -> dict[str, object]:
    state = verified_state()
    if dry_run:
        state["mode"] = "DRYRUN"
        return state
    target = ROOT / TARGET
    baseline = git_bytes("show", "HEAD:" + TARGET)
    expected = expected_replacement(baseline)
    if state["shared_math_mode"] == "BASELINE":
        old = target.read_bytes()
        update = expected.replace(b"\n", b"\r\n") if b"\r\n" in old else expected
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="wb", dir=target.parent,
                                             prefix="r41_", suffix=".tmp",
                                             delete=False) as stream:
                temp_path = stream.name
                stream.write(update)
            os.replace(temp_path, target)
        finally:
            if temp_path is not None and os.path.exists(temp_path):
                os.unlink(temp_path)
    after = verified_state()
    if after["shared_math_mode"] != "INSTALLED":
        raise RuntimeError("R41 shared provider patch did not verify")
    # Produce the complete replacement function and import section on disk.
    # This is documentation-only; not imported as another production module.
    source = normalized(target.read_bytes()).decode("utf-8")
    whole = full_changed_function(source)
    (PACKAGE / "CHANGED_FUNCTION_FULL.py").write_text(whole, encoding="utf-8")
    before_function = source.split("def shared_expansion_provider(", 1)[0]
    (PACKAGE / "IMPORTS_FULL.txt").write_text(before_function, encoding="utf-8")
    after["mode"] = "INSTALLED"
    after["full_function_emitted"] = True
    return after


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = install(dry_run=args.dry_run)
    for key, value in state.items():
        print("PHASE174_R3R7R41_" + key.upper() + "=" + str(value))
    print("PHASE174_R3R7R41_GATE=PASS_R41_SOURCE_GUARD_AND_PROVIDER_WIRING")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```


## audit.py

```python
"""Read-only R41 public provider and source-bound zero-image frontier audit."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import verified_state


def inspect_public_r41() -> dict[str, object]:
    """Inspect actual public proposals; never label proposals as root proofs."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
    from map_property_rules import ImageZeroStatement
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.audit import inspect_isolated_zero_image
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        build_public_adopted_zero_image_provider, screened_general_law,
    )
    from proof import ProofRule, ProofStep, Relation

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    screened = screened_general_law(bridge)
    if len(screened) != 1:
        raise RuntimeError("Cited Toda (5.9) root-scoped source was not screened")
    prior = exact_prior_database_result(5, 5)
    if not isinstance(prior, Relation):
        raise RuntimeError("Reviewed prior cyclic relation unavailable")
    source = prior.lhs
    mapping = TodaSuspensionMap(source, TodaPrimaryGroup(
        source.group_dimension + 1, source.sphere_dimension + 1,
    ))
    zero_image_goal = ImageZeroStatement(mapping)
    public = shared_expansion_provider(bridge, proof_target=root)
    selected = tuple(x for x in public(zero_image_goal) if x.rule.name == RULE_NAME)
    if len(selected) != 1:
        raise RuntimeError("One R40-based R41 public option required")
    if selected[0].subgoals[0] != prior or len(selected[0].subgoals) != 2:
        raise RuntimeError("R41 lost exact earlier DB presentation/zero-generator obligations")
    isolated = build_public_adopted_zero_image_provider(bridge=bridge, proof_target=root)
    direct = isolated(zero_image_goal)
    if tuple((x.rule.name, x.subgoals) for x in direct) != tuple(
        (x.rule.name, x.subgoals) for x in selected
    ):
        raise RuntimeError("R41 public option differs from isolated source-screened adapter")
    # Changing a target or stripping cited proof links must fail closed.
    naked = RegistryBridgeResult(bridge.registry, bridge.records, ())
    if build_public_adopted_zero_image_provider(
        bridge=naked, proof_target=root,
    )(zero_image_goal):
        raise RuntimeError("R41 accepted a bridge without cited source steps")
    if build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=TodaPrimaryGroupZeroStatement(source),
    )(zero_image_goal):
        raise RuntimeError("R41 admitted a self-citing/earlier root")
    if build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=None,
    )(zero_image_goal):
        raise RuntimeError("R41 admitted an untyped target")
    cited_steps = tuple(x.step for x in bridge.proof_links if isinstance(x.step, ProofStep))
    if any(s.conclusion in (zero_image_goal, root) for s in cited_steps):
        raise RuntimeError("Forbidden direct zero-image or final-root GIVEN")
    if any(s.rule is not ProofRule.GIVEN for s in cited_steps):
        raise RuntimeError("Source registration contains improper inference leaf")
    preserved = inspect_isolated_zero_image()
    if (preserved["isolated_zero_image_proved"] is not True
            or preserved["db_given_preserved_inside_proof_tree"] is not True
            or preserved["root_complete"] is not False):
        raise RuntimeError("R40 genuine proof ancestry not preserved")
    return {
        "screened_cited_source_locator": "(5.9)",
        "screened_source_leaves": len(screened),
        "public_r41_zero_image_proposals": len(selected),
        "public_r41_subgoals": len(selected[0].subgoals),
        "source_bound_prior_group_matches": True,
        "r40_isolated_zero_image_verified": True,
        "r40_db_given_preserved": True,
        "source_missing_rejected": True,
        "self_citing_root_rejected": True,
        "untyped_root_rejected": True,
        "new_given_statements": 0,
        "new_mathematical_rules": 0,
        "new_root_given_statements": 0,
        "public_provider_connected": True,
        "public_zero_image_root_verified_by_this_audit": False,
        "upper_delta_surjectivity_verified": False,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verified_state()
    observed = None if args.dry_run else inspect_public_r41()
    gate = ("PASS_R41_REVIEWED_SOURCE_PREFLIGHT" if args.dry_run else
            "PASS_R41_VERIFIED_ADOPTED_DB_ZERO_IMAGE_PUBLIC_PROVIDER_CONNECTED_ROOT_PENDING")
    result = {"phase": "174-R3-R7-R41", "source_guard": state,
              "observations": observed, "gate": gate}
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r41"
    )
    folder.mkdir(parents=True, exist_ok=True)
    output = folder / ("preflight.json" if args.dry_run else "public_zero_image_provider.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p = "PHASE174_R3R7R41_"
    for key, value in state.items():
        print(p + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(p + key.upper() + "=" + str(value))
    print(p + "REPORT=" + str(output))
    print(p + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```


## tests/test_public.py

```python
"""R41 typed public integration and source fail-closed contract."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
    build_public_adopted_zero_image_provider, screened_general_law,
)


def fixture():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    prior = exact_prior_database_result(5, 5)
    suspension = TodaSuspensionMap(prior.lhs, TodaPrimaryGroup(11, 6))
    return root, bridge, prior, ImageZeroStatement(suspension)


def test_public_provider_contains_one_source_bound_adopted_db_candidate():
    root, bridge, prior, goal = fixture()
    assert len(screened_general_law(bridge)) == 1
    proposed = tuple(x for x in shared_expansion_provider(bridge, proof_target=root)(goal)
                     if x.rule.name == RULE_NAME)
    assert len(proposed) == 1
    assert proposed[0].subgoals[0] == prior
    assert len(proposed[0].subgoals) == 2


def test_source_stripping_and_invalid_roots_fail_closed():
    root, bridge, prior, goal = fixture()
    source_free = RegistryBridgeResult(bridge.registry, bridge.records, ())
    assert screened_general_law(source_free) == ()
    assert build_public_adopted_zero_image_provider(
        bridge=source_free, proof_target=root,
    )(goal) == ()
    assert build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=TodaPrimaryGroupZeroStatement(prior.lhs),
    )(goal) == ()
    assert build_public_adopted_zero_image_provider(
        bridge=bridge, proof_target=None,
    )(goal) == ()


def test_public_chain_preserves_isolated_proof_and_does_not_claim_root():
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.audit import inspect_public_r41
    result = inspect_public_r41()
    assert result["public_r41_zero_image_proposals"] == 1
    assert result["r40_isolated_zero_image_verified"] is True
    assert result["r40_db_given_preserved"] is True
    assert result["new_given_statements"] == 0
    assert result["upper_delta_surjectivity_verified"] is False
    assert result["root_complete"] is False
```


## tests/test_static.py

```python
"""R41 exact one-file patch and no-target-specific-rule static guards."""
from __future__ import annotations

import ast
from pathlib import Path

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import (
    ANCHOR, INSERT, TARGET, BASE_BLOB, expected_replacement, matches_blob,
)

PACKAGE = Path(__file__).resolve().parents[1]


def test_patch_is_one_callsite_only_and_anchored():
    assert TARGET == "phase165_r52_r9_shared_math.py"
    assert len(BASE_BLOB) == 40
    assert "build_public_adopted_zero_image_provider" in INSERT
    assert "proof_target=proof_target" in INSERT
    assert "    # R4-4 stage4:" in ANCHOR
    assert "GIVEN" in INSERT


def test_no_new_group_specific_result_or_synthetic_givens():
    source = (PACKAGE / "provider.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    assert not any(isinstance(node, ast.Expr)
                   and isinstance(node.value, ast.Constant)
                   and node.value.value is Ellipsis
                   for node in ast.walk(tree))
    assert "TodaPrimaryGroup(12, 7)" not in source
    assert "ProofStep(" not in source
    assert "ProofRule.INFERENCE" not in source
    assert "add_assertion(" not in source
    assert "expand_source_bound_zero_image_chain" in source


def test_complete_functions_and_scripts_present():
    for filename in ("provider.py", "source_guard.py", "install.py", "audit.py", "run.ps1"):
        assert (PACKAGE / filename).is_file()
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "$DryRun" in script
    assert "pytest" in script
    assert "R40_RULE_REGRESSION" in script


def test_expected_replacement_rejects_unknown_or_already_patched_source():
    import pytest
    with pytest.raises(RuntimeError):
        expected_replacement(b"unreviewed\n" + ANCHOR.encode())
    assert matches_blob(b"any data", BASE_BLOB) is False
```


## tests/test_source_guard.py

```python
"""R41 inspected source/installation contract regression."""
from __future__ import annotations

from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.install import (
    full_changed_function,
)
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import (
    BASE_BLOB, INSERT, normalized, verified_state,
)


def test_checked_source_guard_after_install():
    result = verified_state()
    assert result["source_guard"] == "PASS"
    assert result["shared_math_mode"] == "INSTALLED"
    assert result["reviewed_r40_sha256_files"] == 3
    assert len(BASE_BLOB) == 40


def test_complete_function_extractor_preserves_entire_body():
    synthetic = "import os\n\ndef shared_expansion_provider():\n    return 1\n\ndef other():\n    return 2\n"
    assert full_changed_function(synthetic) == "def shared_expansion_provider():\n    return 1\n"


def test_import_and_full_function_emitted_from_actual_file():
    from pathlib import Path
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.source_guard import ROOT, TARGET
    directory = Path(__file__).resolve().parents[1]
    actual = normalized((ROOT / TARGET).read_bytes()).decode("utf-8")
    function = (directory / "CHANGED_FUNCTION_FULL.py").read_text(encoding="utf-8")
    assert function == full_changed_function(actual)
    assert INSERT in function
    imports = (directory / "IMPORTS_FULL.txt").read_text(encoding="utf-8")
    assert imports == actual.split("def shared_expansion_provider(", 1)[0]
```


## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R41 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R41_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.install
    if ($LASTEXITCODE -ne 0) { throw 'R41 guarded public connection installation failed' }
    python -B -m phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.audit
    if ($LASTEXITCODE -ne 0) { throw 'R41 public source and candidate audit failed' }
    $Groups = @(
        @{Name='R41_STATIC'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_static.py'},
        @{Name='R41_GUARD'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_source_guard.py'},
        @{Name='R41_PUBLIC'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R40_RULE_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py'},
        @{Name='R40_PROOF_REGRESSION'; Path='phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_audit.py'},
        @{Name='R39_PROOF_REGRESSION'; Path='phase174_r3_r7_r39_verified_zero_image_frontier/tests/test_proof.py'},
        @{Name='R38_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r38_source_bound_zero_image_public_wiring/tests/test_public.py'},
        @{Name='R6_CYCLIC_REGRESSION'; Path='phase174_r3_r7_r6_cyclic_generator_zero_image/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R41_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R41 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R41_RUN=PASS'
    Write-Output 'PHASE174_R3R7R41_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
