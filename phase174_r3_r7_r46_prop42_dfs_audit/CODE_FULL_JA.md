# R46 コード全文

既存の本番ファイル・クラス・関数・メソッドの変更はありません。以下は新規監査ディレクトリに追加するファイルの全文です。既存 `README.md`、`docs/design.md`、`development_log.md`、`roadmap.md`、`proof_records.md` は変更しません。

## `__init__.py`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/__init__.py`）

```python
"""R46 read-only cited Proposition 4.2 depth-first frontier audit."""
```

## `source_guard.py`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/source_guard.py`）

```python
"""Read-only verification of R45R1's audited handoff and reviewed search sources."""
from __future__ import annotations

from hashlib import sha256
from pathlib import Path

from phase174_r3_r7_r45_ehp_open_obligation_audit.source_guard import (
    ROOT,
    git,
    matches_git_blob,
    verify_checkout as verify_r45_checkout,
)

REVIEWED_HEAD = "4b06ef96628b39e591cfa0b423fa0e0dec366a3b"
REVIEWED_SEARCH_BLOB = "06009bfcf57f99cac58c229d99c53f16324692d0"
R45_LOCAL_PINS = {
    "phase174_r3_r7_r45_ehp_open_obligation_audit/audit.py": "4339a6281208edb27896cb5aa0e27315c655324de9876862c28ea27d4d1aeef5",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/source_guard.py": "726c99fae70021670eeacaa71584dec0f2c34cc1c87e7a7395c40a6dfd6426de",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1": "47e13f0876f0ac97292a0b55acb681c8763b7552cdf15211e0083bfa9fa5db89",
    "phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_static.py": "a22bd2634bc22976793a8d4e205f3374117317e79b5323e1566670b5471b17ac",
}


def normalized_sha256(data: bytes) -> str:
    """Permit whole-file CRLF/LF conversions, not content drift."""
    return sha256(data.replace(b"\r\n", b"\n")).hexdigest()


def verify_checkout() -> dict[str, object]:
    """Fail closed on changed HEAD, modified production files or R45 handoff."""
    parent = verify_r45_checkout()
    if parent["local_head"] != REVIEWED_HEAD or parent["remote_head"] != REVIEWED_HEAD:
        raise RuntimeError("R46 requires the exact reviewed merged develop HEAD")
    core_path = ROOT / "phase165_r3_recursive_search.py"
    if not core_path.is_file() or not matches_git_blob(
        core_path.read_bytes(), REVIEWED_SEARCH_BLOB
    ):
        raise RuntimeError("Canonical depth-first search source changed")
    for relative, pin in R45_LOCAL_PINS.items():
        file_path = ROOT / relative
        if not file_path.is_file() or normalized_sha256(file_path.read_bytes()) != pin:
            raise RuntimeError("R45R1 reviewed local handoff changed: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": parent["local_head"],
        "remote_head": parent["remote_head"],
        "r45r1_local_pins": len(R45_LOCAL_PINS),
        "search_core_pin": REVIEWED_SEARCH_BLOB,
        "tracked_changes": parent["tracked_changes"],
        "production_files_changed": 0,
        "full_pytest": False,
    }
```

## `audit.py`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/audit.py`）

```python
"""Read-only audit: isolate cited Prop. 4.2 inferences from root DFS blocking.

The R45 first-child stop is audited without rewriting the existing search
order, installing inferred steps, or claiming pi_12^7 has been proved.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import verify_checkout


def inspect_prop42_dfs_frontier() -> dict[str, object]:
    """Observe independent real canonical subproofs and the bounded R45 traversal."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from phase165_r12_r11_prop42_unified import (
        TodaProp42GeneralExactnessStatement,
        build_prop42_specialization_provider,
        prop42_exactness_indices,
    )
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement,
        proof_has_general_prop42_ancestor,
    )
    from phase165_r3_recursive_search import (
        RegisteredGoalUnresolved,
        reconstruct_registered_goal,
    )
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
        build_shared_typed_bridge(), goal=root,
    )
    toda59 = screened_general_law(bridge)
    if len(toda59) != 1:
        raise RuntimeError("The R44 independently cited Toda (5.9) source is missing")
    citing_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == toda59[0]
    )
    if len(citing_ids) != 1:
        raise RuntimeError("R44 source must identify precisely one citation")
    citing_id = citing_ids[0]

    universal = TodaProp42GeneralExactnessStatement()
    prop42_sources = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and not link.step.premises
        and link.step.conclusion == universal
        and bridge.registry.assertion(link.assertion_id).origin is AssertionOrigin.FIXED_STATEMENT
        and bridge.registry.assertion(link.assertion_id).content == universal
        and bridge.registry.reference(
            bridge.registry.assertion(link.assertion_id).reference_id
        ).publication_position is not None
        and getattr(
            getattr(link.step.inference_rule, "literature_reference", None),
            "locator", None,
        ) == "Proposition 4.2 (4.4)"
    )
    if len(prop42_sources) != 1:
        raise RuntimeError("An exact, cited Proposition 4.2 universal source is required")

    root_inputs = ehp_zero_inputs(root)
    if root_inputs is None or len(root_inputs) != 4:
        raise RuntimeError("Typed EHP root expansion changed")
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None or len(upper_inputs) != 4:
        raise RuntimeError("Typed upper-Delta expansion changed")
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None or len(hopf_inputs) != 2:
        raise RuntimeError("Typed Hopf injection expansion changed")
    zero_image, hopf_exactness = hopf_inputs
    lower_image_kernel = upper_inputs[1]
    if type(lower_image_kernel) is not EHPImageEqualsKernelStatement:
        raise RuntimeError("Lower image-kernel Goal has changed type")
    windows = {
        "root_delta_e": root_inputs[1],
        "root_e_h": root_inputs[2],
        "hopf_e_h": hopf_exactness,
        "lower_h_delta": TodaProp42ExactnessStatement(lower_image_kernel.window),
    }
    expected_indices = {
        "root_delta_e": (6, 12, "delta_e"),
        "root_e_h": (6, 12, "e_h"),
        "hopf_e_h": (5, 11, "e_h"),
        "lower_h_delta": (5, 11, "h_delta"),
    }
    if any(
        prop42_exactness_indices(window) != expected_indices[name]
        for name, window in windows.items()
    ):
        raise RuntimeError("Reviewed four Prop. 4.2 windows changed")

    public = shared_expansion_provider(bridge, proof_target=root)
    def match(goal: object, rule_name: str, subgoals: tuple):
        return tuple(
            option for option in public(goal)
            if option.rule.name == rule_name and option.subgoals == subgoals
        )

    exact_rule = "Toda Proposition 4.2: generic consecutive EHP specialization"
    exact_options = {
        name: match(window, exact_rule, (universal,))
        for name, window in windows.items()
    }
    root_options = match(root, ROOT_RULE, root_inputs)
    upper_options = match(upper, UPPER_RULE, upper_inputs)
    hopf_options = match(hopf, HOPF_RULE, hopf_inputs)
    lower_options = match(
        lower_image_kernel,
        "EHP exactness implies image equals kernel",
        (windows["lower_h_delta"],),
    )
    if any(len(options) != 1 for options in (
        root_options, upper_options, hopf_options, lower_options,
        *exact_options.values(),
    )):
        raise RuntimeError("A reviewed public Prop. 4.2 or EHP proposal was lost")

    # The exact same R45 scope is used, with the zero-image subproof omitted.
    # A trace observes which child goals the real depth-first engine requests.
    traversal: list[str] = []
    def bounded_r45(goal: object):
        for name, comparison, options in (
            ("root", root, root_options),
            ("upper_delta", upper, upper_options),
            ("hopf_injective", hopf, hopf_options),
            ("lower_image_kernel", lower_image_kernel, lower_options),
        ):
            if type(goal) is type(comparison) and goal == comparison:
                traversal.append(name)
                return options
        for name, comparison in windows.items():
            if type(goal) is type(comparison) and goal == comparison:
                traversal.append(name)
                return exact_options[name]
        if type(goal) is type(zero_image) and goal == zero_image:
            traversal.append("zero_image_outside_scope")
            return ()
        traversal.append(type(goal).__name__)
        return ()

    bounded_result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citing_id,
        expansion_provider=bounded_r45, lookup_mode="typed_reference",
    )
    if any(step.conclusion == root for step in bounded_result.proven_steps):
        raise RuntimeError("Restricted R45 traversal unexpectedly proves the target")

    def only_exactness(goal: object):
        for name, statement in windows.items():
            if type(goal) is type(statement) and goal == statement:
                return exact_options[name]
        if type(goal) is type(lower_image_kernel) and goal == lower_image_kernel:
            return lower_options
        return ()

    # Independently start canonical recursive search *at each actual typed
    # obligation*. These proofs are certified subproofs, not the root proof.
    verified: dict[str, dict[str, object]] = {}
    for name, target in (
        *tuple(windows.items()),
        ("lower_image_kernel", lower_image_kernel),
    ):
        observed: list[ProofStep] = []
        def note(kind: str, goal: object, step: ProofStep | None) -> None:
            if kind == "proved" and isinstance(step, ProofStep):
                observed.append(step)
        try:
            step = reconstruct_registered_goal(
                target, bridge, citing_id, only_exactness,
                lookup_mode="typed_reference", progress_observer=note,
            )
        except RegisteredGoalUnresolved as error:
            verified[name] = {
                "status": "unresolved", "inference": False,
                "general_prop42_ancestor": False,
                "accepted_steps": len(observed),
                "diagnostic": str(error)[:300],
            }
            continue
        inference = (
            isinstance(step, ProofStep)
            and step.rule is ProofRule.INFERENCE
            and type(step.conclusion) is type(target)
            and step.conclusion == target
        )
        ancestor = inference and proof_has_general_prop42_ancestor(step)
        if inference and not ancestor:
            raise RuntimeError("Inferred Prop. 4.2 result lacks cited ancestor")
        verified[name] = {
            "status": "proved" if inference else "not_inferred",
            "inference": inference,
            "general_prop42_ancestor": ancestor,
            "accepted_steps": len(observed),
            "premise_rule_types": [s.rule.value for s in step.premises],
        }

    # Screening out the universal source must prevent exactness specialization.
    screened_without_prop42 = RegistryBridgeResult(
        bridge.registry, bridge.records,
        tuple(link for link in bridge.proof_links
              if link.assertion_id != prop42_sources[0].assertion_id),
    )
    missing_source_provider = build_prop42_specialization_provider(screened_without_prop42)
    absent_candidates = {
        name: len(missing_source_provider(window))
        for name, window in windows.items()
    }
    if any(absent_candidates.values()):
        raise RuntimeError("Prop. 4.2 specialization bypassed the source gate")

    open_types = Counter(type(goal).__name__ for goal in bounded_result.open_goals)
    proof_types = Counter(type(step.conclusion).__name__ for step in bounded_result.proven_steps)
    return {
        "root": "pi_12^7 = 0",
        "source_first_universal_count": len(prop42_sources),
        "cited_prop42_source_reference_id": bridge.registry.assertion(
            prop42_sources[0].assertion_id
        ).reference_id,
        "prop42_public_candidates": {name: len(options) for name, options in exact_options.items()},
        "prop42_when_source_removed": absent_candidates,
        "r45_bounded_status": bounded_result.status.value,
        "r45_bounded_verified_steps": len(bounded_result.proven_steps),
        "r45_bounded_proven_types": dict(sorted(proof_types.items())),
        "r45_bounded_open_goal_types": dict(sorted(open_types.items())),
        "r45_public_provider_visit_trace": traversal,
        "r45_first_unexpanded_subgoal_is_zero_image": (
            "zero_image_outside_scope" in traversal
            and not any(name in traversal for name in windows)
        ),
        "isolated_canonical_subproofs": verified,
        "isolated_proofs_not_added_to_root_search": True,
        "r44_zero_image_not_replayed": True,
        "root_complete": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observed = None if args.dry_run else inspect_prop42_dfs_frontier()
    inferred = () if observed is None else tuple(
        data["inference"] and data["general_prop42_ancestor"]
        for data in observed["isolated_canonical_subproofs"].values()
    )
    if args.dry_run:
        gate = "PASS_R46_REVIEWED_R45R1_SOURCE_PREFLIGHT"
    elif all(inferred) and observed["r45_first_unexpanded_subgoal_is_zero_image"]:
        gate = "PASS_R46_CITED_PROP42_SUBPROOFS_VERIFIED_DFS_ROOT_PENDING"
    else:
        gate = "PASS_R46_PROP42_INFERENCE_OR_DFS_GAP_RECORDED"
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r46"
    )
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / ("preflight.json" if args.dry_run else "prop42_dfs_audit.json")
    destination.write_text(json.dumps(
        {"phase": "174-R3-R7-R46", "state": state,
         "observation": observed, "gate": gate},
        ensure_ascii=False, indent=2,
    ) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R46_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if observed is not None:
        for key, value in observed.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/run.ps1`）

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r46_prop42_dfs_audit.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R46 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R46_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r46_prop42_dfs_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R46 cited exactness/DFS audit failed' }
    $Groups = @(
        @{Name='R46_STATIC'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_static.py'; ImportMode='importlib'},
        @{Name='R46_GUARD'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_guard.py'; ImportMode='importlib'},
        @{Name='R46_FRONTIER'; Path='phase174_r3_r7_r46_prop42_dfs_audit/tests/test_audit.py'; ImportMode='importlib'},
        @{Name='R45_FRONTIER_REGRESSION'; Path='phase174_r3_r7_r45_ehp_open_obligation_audit/tests/test_frontier.py'; ImportMode='importlib'},
        @{Name='PROP42_SPECIALIZATION_REGRESSION'; Path='phase165_r12_r11_prop42_unified/tests/test_phase165_r12_r11_prop42_unified.py'; ImportMode='prepend'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R46_TEST_GROUP=' + $Group.Name)
        $ImportMode = $Group.ImportMode
        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R46 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R46_RUN=PASS'
    Write-Output 'PHASE174_R3R7R46_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

## `tests/test_audit.py`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/tests/test_audit.py`）

```python
"""R46 explicitly distinguishes isolated subproofs from a completed group proof."""
from __future__ import annotations

from functools import lru_cache

from phase174_r3_r7_r46_prop42_dfs_audit.audit import inspect_prop42_dfs_frontier


@lru_cache(maxsize=1)
def observed() -> dict[str, object]:
    return inspect_prop42_dfs_frontier()


def test_cited_source_controls_public_prop42_specializations():
    report = observed()
    assert report["source_first_universal_count"] == 1
    assert report["prop42_public_candidates"] == {
        "root_delta_e": 1,
        "root_e_h": 1,
        "hopf_e_h": 1,
        "lower_h_delta": 1,
    }
    assert all(value == 0 for value in report["prop42_when_source_removed"].values())


def test_actual_canonical_subproofs_never_claim_unsupported_ancestry():
    report = observed()
    assert set(report["isolated_canonical_subproofs"]) == {
        "root_delta_e", "root_e_h", "hopf_e_h", "lower_h_delta",
        "lower_image_kernel",
    }
    for proof in report["isolated_canonical_subproofs"].values():
        assert proof["status"] in ("proved", "unresolved", "not_inferred")
        if proof["inference"]:
            assert proof["general_prop42_ancestor"] is True
            assert proof["accepted_steps"] >= 2


def test_r45_first_unresolved_branch_is_not_promoted_to_root_proof():
    report = observed()
    assert report["r45_bounded_status"] in ("partial", "search_failed")
    assert report["r45_public_provider_visit_trace"][0] == "root"
    assert "zero_image_outside_scope" in report["r45_public_provider_visit_trace"]
    assert report["isolated_proofs_not_added_to_root_search"] is True
    assert report["r44_zero_image_not_replayed"] is True
    assert report["root_complete"] is False


def test_no_new_math_source_or_unreviewed_web_completion():
    report = observed()
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False
```

## `tests/test_guard.py`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/tests/test_guard.py`）

```python
"""R46 pinning allows line-ending conversion but not code mutation."""
from __future__ import annotations

from hashlib import sha256

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import (
    R45_LOCAL_PINS,
    REVIEWED_HEAD,
    REVIEWED_SEARCH_BLOB,
    normalized_sha256,
)


def test_hand_off_pins_cover_r45r1_and_canonical_search():
    assert len(REVIEWED_HEAD) == 40
    assert len(REVIEWED_SEARCH_BLOB) == 40
    assert len(R45_LOCAL_PINS) == 4
    assert "phase174_r3_r7_r45_ehp_open_obligation_audit/run.ps1" in R45_LOCAL_PINS
    assert all(len(value) == 64 for value in R45_LOCAL_PINS.values())


def test_normalized_hash_changes_only_on_non_eol_modifications():
    text = b"a\nb\n"
    expected = sha256(text).hexdigest()
    assert normalized_sha256(text) == expected
    assert normalized_sha256(b"a\r\nb\r\n") == expected
    assert normalized_sha256(b"a\nB\n") != expected
```

## `tests/test_static.py`（新規追加：`phase174_r3_r7_r46_prop42_dfs_audit/tests/test_static.py`）

```python
"""R46 remains a standalone audit-only ZIP with no production patch."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_r46_source_has_no_ellipsis_expressions():
    for relative in (
        "__init__.py", "source_guard.py", "audit.py",
        "tests/test_audit.py", "tests/test_guard.py", "tests/test_static.py",
    ):
        source = (PACKAGE / relative).read_text(encoding="utf-8")
        tree = ast.parse(source)
        assert not any(
            isinstance(node, ast.Constant) and node.value is Ellipsis
            for node in ast.walk(tree)
        )


def test_r46_does_not_install_a_proof_or_modify_production():
    audit = (PACKAGE / "audit.py").read_text(encoding="utf-8")
    runner = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "reconstruct_registered_goal" in audit
    assert "search_registered_partial_proof" in audit
    assert "ProofStep(" not in audit
    assert "expansion_provider=bounded_r45" in audit
    assert "git reset" not in runner and "git clean" not in runner
    assert "install.py" not in runner
    assert "FULL_PYTEST=False" in runner
    assert "[switch]$DryRun" in runner


def test_documentation_and_test_files_exist():
    for relative in (
        "README.md", "AUDIT_PLAN_JA.md", "CODE_FULL_JA.md",
        "TEST_RESULTS_JA.md", "run.ps1", "tests/test_audit.py",
    ):
        assert (PACKAGE / relative).is_file()
```

