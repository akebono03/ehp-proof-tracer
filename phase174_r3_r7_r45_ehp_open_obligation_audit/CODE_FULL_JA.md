# Phase 174 R3-R7-R45 コード全文

新規ディレクトリ: `phase174_r3_r7_r45_ehp_open_obligation_audit/`。
既存本番ファイルの変更はありません。

## `__init__.py`

```python
"""Phase 174 R3-R7-R45 read-only EHP open-obligation audit."""
```

## `source_guard.py`

```python
"""Read-only R45 source guard against the reviewed R44 merge on develop."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PREVIOUS_HEAD = "02b9f8d743f57a0ad5c86ce3c63bbb8aee5e2b19"
REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
PINS = {
    "phase165_r52_r9_shared_math.py": "534b552856fefc8315b243fecc3170ee5792ebc7",
    "phase165_r12_r11_prop42_unified.py": "79752ec035244677ff6a54debff312e87a76fbf2",
    "phase165_r12_r12_ehp_consequences.py": "895dc98ad4d25f14fb7aac8fa52460a77fd049bc",
    "phase174_r3_r7_r44_public_zero_image_tree_frontier/audit.py": "42767b1945bcb3e00665c00b88f2ca37c7dd6d3c",
    "phase174_r3_r7_r43_public_ehp_map_property_wiring/audit.py": "de29f36886df76ebd234b88fa02dab8920c36e5c",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase169_r10e2_unpositioned_citation/source_first.py": "b91b97a74d65b843fa8f9c19ffd082f684e461a7",
    "phase166_r3l_reference_order.py": "faefcf0620f92bdf7f6222814467375a075cccf6",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    ).stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\0" + data
    ).hexdigest()


def matches_git_blob(data: bytes, expected: str) -> bool:
    normalized = data.replace(b"\r\n", b"\n")
    variants = (
        data,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )
    return len(expected) == 40 and any(
        git_blob_sha(candidate) == expected for candidate in variants
    )


def verify_checkout() -> dict[str, object]:
    """Require exact reviewed bytes, no staged or tracked edits, and develop."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R45 ZIP must be extracted into repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R45 requires the develop branch")
    remote_line = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_line or remote_line[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; re-audit R45 pins")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_HEAD, REVIEWED_HEAD):
        raise RuntimeError("Local HEAD is not the reviewed R44 handoff or merge")
    staged = git("diff", "--cached", "--name-only").splitlines()
    if staged:
        raise RuntimeError("Staged changes require separate review: " + repr(staged))
    tracked = git("diff", "--name-only").splitlines()
    if tracked:
        raise RuntimeError("Tracked changes require separate review: " + repr(tracked))
    for path, expected_sha in PINS.items():
        file_path = ROOT / path
        if not file_path.is_file() or not matches_git_blob(
            file_path.read_bytes(), expected_sha
        ):
            raise RuntimeError("Reviewed source differs: " + path)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": (
            "R44_MERGED" if local_head == REVIEWED_HEAD
            else "R44_PRE_MERGE_WITH_REVIEWED_AUDIT"
        ),
        "pinned_files": len(PINS),
        "tracked_changes": 0,
        "full_pytest": False,
    }
```

## `audit.py`

```python
"""R45: read-only source-first audit of open Proposition 4.2/EHP obligations.

This deliberately scoped canonical search does not replay R44's entire
zero-image branch and cannot certify the final pi_12^7 group. It determines
whether already-registered general EHP exactness rules are actually usable.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import verify_checkout


def inspect_open_ehp_obligations() -> dict[str, object]:
    """Trace real public proposals and a constrained canonical proof search."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        prop42_exactness_indices,
    )
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement,
        proof_has_general_prop42_ancestor,
    )
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge,
        shared_expansion_provider,
    )
    from phase169_r10e2_unpositioned_citation.source_first import (
        screen_independent_sources_for_derived_goal,
    )
    from phase174_r3_r7_r3_ehp_zero_rule.rule import (
        RULE_NAME as ROOT_RULE,
        ehp_zero_inputs,
    )
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE,
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE,
        upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
        screened_general_law,
    )
    from proof import ProofRule, ProofStep
    from toda_rules import TodaProp42ExactnessStatement
    from unified_statement_registry import AssertionOrigin

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root
    )
    r44_source = screened_general_law(bridge)
    if len(r44_source) != 1:
        raise RuntimeError("R44 Toda (5.9) source was lost")
    source_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == r44_source[0]
    )
    if len(source_ids) != 1:
        raise RuntimeError("The R44 source link is no longer unique")

    universal = TodaProp42GeneralExactnessStatement()
    cited_universal = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and link.step.conclusion == universal
        and bridge.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
        and bridge.registry.assertion(link.assertion_id).content == universal
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).publication_position is not None
        and getattr(
            getattr(link.step.inference_rule, "literature_reference", None),
            "locator", None,
        ) == "Proposition 4.2 (4.4)"
    )
    if len(cited_universal) > 1:
        raise RuntimeError("Duplicated screened Prop. 4.2 source")

    root_inputs = ehp_zero_inputs(root)
    if root_inputs is None or len(root_inputs) != 4:
        raise RuntimeError("R3 zero-root obligation shape changed")
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None or len(upper_inputs) != 4:
        raise RuntimeError("R37 Delta-surjectivity obligation shape changed")
    hopf = upper_inputs[0]
    lower_image_kernel = upper_inputs[1]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None or len(hopf_inputs) != 2:
        raise RuntimeError("R5 Hopf-injectivity obligation shape changed")
    zero_image, hopf_exactness = hopf_inputs
    if (type(zero_image) is not ImageZeroStatement
            or type(lower_image_kernel) is not EHPImageEqualsKernelStatement):
        raise RuntimeError("Typed zero-image or lower EHP obligation changed")

    windows = {
        "root_delta_e": root_inputs[1],
        "root_e_h": root_inputs[2],
        "hopf_e_h": hopf_exactness,
        "lower_h_delta": TodaProp42ExactnessStatement(lower_image_kernel.window),
    }
    expected = {
        "root_delta_e": (6, 12, "delta_e"),
        "root_e_h": (6, 12, "e_h"),
        "hopf_e_h": (5, 11, "e_h"),
        "lower_h_delta": (5, 11, "h_delta"),
    }
    for name, statement in windows.items():
        if (type(statement) is not TodaProp42ExactnessStatement
                or prop42_exactness_indices(statement) != expected[name]):
            raise RuntimeError("The reviewed Prop. 4.2 window changed: " + name)
    values = tuple(windows.values())
    if any(first == second for index, first in enumerate(values)
           for second in values[index + 1:]):
        raise RuntimeError("Distinct EHP windows unexpectedly overlap")

    public = shared_expansion_provider(bridge, proof_target=root)
    exactness_rule_name = "Toda Proposition 4.2: generic consecutive EHP specialization"
    image_kernel_rule_name = "EHP exactness implies image equals kernel"

    def matching(goal: object, name: str, subgoals: tuple):
        return tuple(
            expansion for expansion in public(goal)
            if expansion.rule.name == name and expansion.subgoals == subgoals
        )

    exact_options = {
        name: matching(statement, exactness_rule_name, (universal,))
        for name, statement in windows.items()
    }
    root_options = matching(root, ROOT_RULE, root_inputs)
    upper_options = matching(upper, UPPER_RULE, upper_inputs)
    hopf_options = matching(hopf, HOPF_RULE, hopf_inputs)
    lower_options = matching(
        lower_image_kernel, image_kernel_rule_name,
        (windows["lower_h_delta"],),
    )
    for name, options in (
        ("EHP root", root_options),
        ("upper Delta", upper_options),
        ("Hopf injectivity", hopf_options),
        ("lower image-kernel", lower_options),
    ):
        if len(options) != 1:
            raise RuntimeError("Reviewed public conditional rule changed: " + name)
    if any(len(options) > 1 for options in exact_options.values()):
        raise RuntimeError("Duplicated public Prop. 4.2 specialization candidate")

    # Deliberately exclude the R44 zero-image branch and unexamined providers.
    # The only source leaves remain the actual screened bridge proof links.
    def scoped(goal: object):
        if goal == root:
            return root_options
        if goal == upper:
            return upper_options
        if goal == hopf:
            return hopf_options
        if goal == lower_image_kernel:
            return lower_options
        for name, statement in windows.items():
            if goal == statement:
                return exact_options[name]
        return ()

    result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=source_ids[0],
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    if result.status is ProofSearchStatus.COMPLETE:
        raise RuntimeError("The intentionally restricted R45 proof unexpectedly completed")
    if any(step.conclusion == root for step in result.proven_steps):
        raise RuntimeError("Root was claimed without proving zero image and other goals")
    inferred = {
        name: tuple(
            step for step in result.proven_steps
            if step.conclusion == statement and step.rule is ProofRule.INFERENCE
        )
        for name, statement in windows.items()
    }
    if any(len(steps) > 1 for steps in inferred.values()):
        raise RuntimeError("Duplicate certified exactness steps in bounded proof")
    ancestry = {
        name: (
            len(steps) == 1 and proof_has_general_prop42_ancestor(steps[0])
        )
        for name, steps in inferred.items()
    }
    if any(len(inferred[name]) == 1 and not ancestry[name] for name in windows):
        raise RuntimeError("Inferred exactness has no cited universal source ancestor")
    lower_derived = any(
        step.conclusion == lower_image_kernel and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
    hopf_derived = any(
        step.conclusion == hopf and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
    upper_derived = any(
        step.conclusion == upper and step.rule is ProofRule.INFERENCE
        for step in result.proven_steps
    )
    opened = Counter(type(goal).__name__ for goal in result.open_goals)
    return {
        "root": "pi_12^7 = 0",
        "r44_zero_image_inference_is_prior_evidence_not_replayed": True,
        "toda59_screened_source_count": len(r44_source),
        "prop42_cited_universal_source_count": len(cited_universal),
        "prop42_source_reference_ids": [
            bridge.registry.assertion(link.assertion_id).reference_id
            for link in cited_universal
        ],
        "prop42_window_indices": {
            key: list(value) for key, value in expected.items()
        },
        "prop42_public_specialization_candidates": {
            name: len(options) for name, options in exact_options.items()
        },
        "public_root_candidates": len(root_options),
        "public_upper_delta_candidates": len(upper_options),
        "public_hopf_injective_candidates": len(hopf_options),
        "public_lower_image_kernel_candidates": len(lower_options),
        "canonical_scoped_search_status": result.status.value,
        "canonical_scoped_proven_steps": len(result.proven_steps),
        "canonical_scoped_prop42_inference_steps": {
            name: len(steps) for name, steps in inferred.items()
        },
        "canonical_scoped_prop42_has_cited_ancestor": ancestry,
        "canonical_scoped_lower_image_kernel_inferred": lower_derived,
        "canonical_scoped_hopf_injectivity_inferred": hopf_derived,
        "canonical_scoped_upper_delta_surjectivity_inferred": upper_derived,
        "canonical_scoped_open_goal_types": dict(sorted(opened.items())),
        "canonical_scoped_unresolved_goals": len(result.open_goals),
        "zero_image_deliberately_outside_r45_scoped_proof": True,
        "new_givens": 0,
        "production_files_changed": 0,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    git_state = verify_checkout()
    observation = None if args.dry_run else inspect_open_ehp_obligations()
    if args.dry_run:
        gate = "PASS_R45_R44_MERGE_SOURCE_PREFLIGHT"
    elif (observation["prop42_cited_universal_source_count"] == 1
          and all(value == 1 for value in observation[
              "canonical_scoped_prop42_inference_steps"
          ].values())):
        gate = "PASS_R45_CITED_PROP42_CANONICAL_INFERENCE_ROOT_PENDING"
    elif (observation["prop42_cited_universal_source_count"] == 1
          and all(value == 1 for value in observation[
              "prop42_public_specialization_candidates"
          ].values())):
        gate = "PASS_R45_PUBLIC_PROP42_AVAILABLE_CANONICAL_INFERENCE_PENDING"
    else:
        gate = "PASS_R45_PROP42_SOURCE_OR_PROVIDER_GAP_RECORDED"
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r45"
    )
    directory.mkdir(parents=True, exist_ok=True)
    filename = "preflight.json" if args.dry_run else "ehp_open_obligations.json"
    report = {"phase": "174-R3-R7-R45", "git": git_state,
              "observation": observation, "gate": gate}
    output = directory / filename
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    prefix = "PHASE174_R3R7R45_"
    for key, value in git_state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observation is not None:
        for key, value in observation.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_frontier.py`

```python
"""Read-only typed R45 proof obligations, not a final-root proof."""
from __future__ import annotations

from functools import lru_cache

from phase174_r3_r7_r45_ehp_open_obligation_audit.audit import (
    inspect_open_ehp_obligations,
)


@lru_cache(maxsize=1)
def report() -> dict[str, object]:
    return inspect_open_ehp_obligations()


def test_r44_source_and_four_distinct_ehp_windows_still_exist():
    observed = report()
    assert observed["toda59_screened_source_count"] == 1
    assert observed["prop42_window_indices"] == {
        "root_delta_e": [6, 12, "delta_e"],
        "root_e_h": [6, 12, "e_h"],
        "hopf_e_h": [5, 11, "e_h"],
        "lower_h_delta": [5, 11, "h_delta"],
    }
    assert observed["public_root_candidates"] == 1
    assert observed["public_upper_delta_candidates"] == 1
    assert observed["public_hopf_injective_candidates"] == 1
    assert observed["public_lower_image_kernel_candidates"] == 1


def test_general_prop42_candidates_only_appear_with_cited_source():
    observed = report()
    source_count = observed["prop42_cited_universal_source_count"]
    assert source_count in (0, 1)
    options = observed["prop42_public_specialization_candidates"]
    assert set(options) == {
        "root_delta_e", "root_e_h", "hopf_e_h", "lower_h_delta"
    }
    assert all(value in (0, 1) for value in options.values())
    if source_count == 0:
        assert all(value == 0 for value in options.values())
    else:
        assert all(value == 1 for value in options.values())


def test_real_inference_steps_have_cited_universal_ancestor():
    observed = report()
    steps = observed["canonical_scoped_prop42_inference_steps"]
    ancestry = observed["canonical_scoped_prop42_has_cited_ancestor"]
    assert set(steps) == set(ancestry)
    assert all(value in (0, 1) for value in steps.values())
    assert all(ancestry[name] for name, count in steps.items() if count == 1)
    assert observed["canonical_scoped_search_status"] in (
        "partial", "search_failed"
    )
    assert observed["canonical_scoped_proven_steps"] >= 0


def test_unproved_hopf_and_root_are_not_short_circuited():
    observed = report()
    assert observed["zero_image_deliberately_outside_r45_scoped_proof"] is True
    assert observed["canonical_scoped_hopf_injectivity_inferred"] is False
    assert observed["canonical_scoped_upper_delta_surjectivity_inferred"] is False
    assert observed["root_complete"] is False
    assert observed["new_givens"] == 0
    assert observed["production_files_changed"] == 0
    assert observed["web_http_checked"] is False
    assert observed["full_pytest"] is False
```

## `tests/test_source_guard.py`

```python
"""R45 Git blob checks are content-based and do not mutate the worktree."""
from __future__ import annotations

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    PINS,
    git_blob_sha,
    matches_git_blob,
)


def test_pin_table_reviews_core_and_handoff_sources():
    assert "phase165_r52_r9_shared_math.py" in PINS
    assert "phase165_r12_r11_prop42_unified.py" in PINS
    assert "phase174_r3_r7_r44_public_zero_image_tree_frontier/audit.py" in PINS
    assert "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py" in PINS
    assert all(len(sha) == 40 for sha in PINS.values())


def test_blob_matching_accepts_only_exact_or_whole_file_eol_changes():
    raw = b"alpha\nbeta\n"
    sha = git_blob_sha(raw)
    assert matches_git_blob(raw, sha)
    assert matches_git_blob(b"alpha\r\nbeta\r\n", sha)
    assert not matches_git_blob(b"alpha\nBETA\n", sha)
    assert not matches_git_blob(raw, "0" * 40)
```

## `tests/test_static.py`

```python
"""R45 is a self-contained non-invasive audit-only ZIP."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r45_python_modules_are_complete_and_parse():
    targets = (
        "__init__.py", "source_guard.py", "audit.py",
        "tests/test_frontier.py", "tests/test_source_guard.py",
        "tests/test_static.py",
    )
    for filename in targets:
        source = (PACKAGE / filename).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_runner_performs_no_install_or_full_test_suite():
    source = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "[switch]$DryRun" in source
    assert "--dry-run" in source
    assert "--import-mode=importlib" in source
    assert "git reset" not in source
    assert "git clean" not in source
    assert "install.py" not in source
    assert "FULL_PYTEST=False" in source


def test_no_derived_theorem_is_installed_or_given():
    source = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in source
    assert "ProofRule.GIVEN" in source
    assert "source_guard" in source
    assert "expand_provider=" not in source
    assert "expansion_provider=scoped" in source
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r45_ehp_open_obligation_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R45 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R45_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r45_ehp_open_obligation_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R45 EHP frontier audit failed' }
    $Groups = @(
        @{Name='R45_STATIC'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py'},
        @{Name='R45_GUARD'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_source_guard.py'},
        @{Name='R45_FRONTIER'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_frontier.py'},
        @{Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'},
        @{Name='PROP42_CONSEQUENCE_REGRESSION'; Path='phase165_r12_r12_ehp_consequences/tests/test_phase165_r12_r12_ehp_consequences.py'},
        @{Name='R5_HOPF_REGRESSION'; Path='phase174_r3_r7_r5_zero_image_hopf_injective/tests/test_rule.py'},
        @{Name='R37_DELTA_REGRESSION'; Path='phase174_r3_r7_r37_upper_delta_surjectivity_isolated/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R45_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R45 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R45_RUN=PASS'
    Write-Output 'PHASE174_R3R7R45_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
