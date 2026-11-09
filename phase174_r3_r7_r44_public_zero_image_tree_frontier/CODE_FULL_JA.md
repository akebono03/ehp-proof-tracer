# R44 新規コード全文

既存コードへの変更はありません。以下は新規ファイルの全文です。

## `__init__.py`

```python
"""R44 read-only public zero-image proof-tree frontier audit."""
```

## `source_guard.py`

```python
"""Read-only Git/working-tree verification for the reviewed R43 completion."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE_HEAD = "f5b6899b124d435c224870476b2448454f77b1b5"
MERGED_HEAD = "02b9f8d743f57a0ad5c86ce3c63bbb8aee5e2b19"
TARGET = "phase165_r52_r9_shared_math.py"
BASE_SHA = "8bb72fe9b3fe22c1917c51971b12338d62be9e9b"
MERGED_SHA = "534b552856fefc8315b243fecc3170ee5792ebc7"
PINS = {
    "phase174_r3_r7_r43_public_ehp_map_property_wiring/audit.py": "de29f36886df76ebd234b88fa02dab8920c36e5c",
    "phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_public.py": "fbc4dcdad82c36e21ff16f032dd1e95096949817",
    "phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/provider.py": "9cf9dfa4b77a22bcbbe60b0c0b85dbf25cad50b2",
    "phase174_r3_r7_r40_adopted_db_zero_image_isolated/rule.py": "dfa1519c629eef92ca1c5dae265acc050883649b",
    "phase174_r3_r7_r39_verified_zero_image_frontier/audit.py": "1e3b589bb221daa32c9ee1d21fb10a6dedcd2333",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r5_zero_image_hopf_injective/rule.py": "62da3cb6f2d4e500d0a87af1028eb3b637bf9cdc",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(*arguments: str) -> str:
    return subprocess.run(
        ("git",) + arguments, cwd=ROOT, check=True, text=True,
        capture_output=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def normalize(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def matches_blob(data: bytes, expected: str) -> bool:
    normalized = normalize(data)
    return len(expected) == 40 and expected in (
        git_blob(data), git_blob(normalized),
        git_blob(normalized.replace(b"\n", b"\r\n")),
    )


def verify_checkout() -> dict[str, object]:
    """Accept only a clean R43 merge or its exactly reviewed unmerged patch."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("Extract R44 at repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R44 requires develop branch")
    remote_lines = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_lines or remote_lines[0] != MERGED_HEAD:
        raise RuntimeError("R43 remote HEAD changed: independent review required")
    head = git("rev-parse", "HEAD")
    if head not in (BASE_HEAD, MERGED_HEAD):
        raise RuntimeError("Unreviewed local HEAD")
    staged = tuple(git("diff", "--cached", "--name-only").splitlines())
    if staged:
        raise RuntimeError("Staged paths require review: " + repr(staged))
    tracked = tuple(git("diff", "--name-only").splitlines())
    if head == MERGED_HEAD:
        if tracked:
            raise RuntimeError("Tracked change outside reviewed R43 merged HEAD: " + repr(tracked))
        mode = "MERGED_R43_CLEAN"
    else:
        if tracked != (TARGET,):
            raise RuntimeError("Only the reviewed unmerged R43 code change is accepted: " + repr(tracked))
        baseline = subprocess.run(
            ("git", "show", "HEAD:" + TARGET), cwd=ROOT,
            check=True, capture_output=True,
        ).stdout
        if not matches_blob(baseline, BASE_SHA):
            raise RuntimeError("Unmerged R43 predecessor differs")
        mode = "REVIEWED_R43_UNMERGED"
    if not matches_blob((ROOT / TARGET).read_bytes(), MERGED_SHA):
        raise RuntimeError("Shared provider must equal the exact reviewed R43 merged blob")
    for path, expected_sha in PINS.items():
        source = ROOT / path
        if not source.is_file() or not matches_blob(source.read_bytes(), expected_sha):
            raise RuntimeError("Pinned source differs: " + path)
    return {
        "local_head": head,
        "remote_head": MERGED_HEAD,
        "source_guard": "PASS",
        "handoff_mode": mode,
        "reviewed_source_pins": len(PINS) + 1,
        "production_files_changed": 0,
        "full_pytest": False,
    }
```

## `audit.py`

```python
"""Read-only canonical-search audit of E(pi_10^5)=0 versus pi_10^5=0.

This probe deliberately restricts the search to an inspected R43/R41/R38
backward branch. It never claims to exercise every Web branch or the HTTP UI.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r44_public_zero_image_tree_frontier.source_guard import verify_checkout


def inspected_frontier() -> dict[str, object]:
    """Observe genuine canonical steps, without manually installing a proof."""
    from expression import Zero
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations, expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as EHP_RULE, ehp_zero_inputs
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import RULE_NAME as HOPF_RULE, hopf_injectivity_from_zero_image_inputs
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import RULE_NAME as UPPER_RULE, upper_delta_surjectivity_inputs
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME as ZERO_IMAGE_RULE
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import screened_general_law
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import expand_cited_annihilator_specialization
    from phase165_r14_r6_generic_iso import GeneratorImage
    from proof import ProofRule, ProofStep, Relation, RelationType

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    laws = screened_general_law(bridge)
    if len(laws) != 1:
        raise RuntimeError("Required independently cited Toda (5.9) source not screened")
    citation_ids = tuple(
        link.assertion_id for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == laws[0]
    )
    if len(citation_ids) != 1:
        raise RuntimeError("Cited source lacks exactly one concrete proof link")
    public = shared_expansion_provider(bridge, proof_target=root)
    root_inputs = ehp_zero_inputs(root)
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    zero_image = hopf_inputs[0]
    if type(zero_image) is not ImageZeroStatement:
        raise RuntimeError("Hopf injectivity requires zero-image, not zero-group")

    def single_public(goal, name, expected):
        options = tuple(
            item for item in public(goal)
            if item.rule.name == name and item.subgoals == expected
        )
        if len(options) != 1:
            raise RuntimeError("Reviewed R43 public provider disappeared or became ambiguous: " + name)
        return options[0]

    root_exp = single_public(root, EHP_RULE, root_inputs)
    upper_exp = single_public(upper, UPPER_RULE, upper_inputs)
    hopf_exp = single_public(hopf, HOPF_RULE, hopf_inputs)
    candidates = tuple(x for x in public(zero_image) if x.rule.name == ZERO_IMAGE_RULE)
    if len(candidates) != 1 or len(candidates[0].subgoals) != 2:
        raise RuntimeError("R41 source-bound zero-image option missing")
    image_exp = candidates[0]
    prior, zero_generator_goal = image_exp.subgoals
    db_step = admitted_db_step(prior, proof_target=root, bridge=bridge)
    if (db_step is None or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("Source-first DB prior trust boundary did not validate")
    if zero_image.map.source_group != prior.lhs:
        raise RuntimeError("Cyclic prior group does not match suspension domain")
    false_zero_group = TodaPrimaryGroupZeroStatement(prior.lhs)
    if false_zero_group == zero_image:
        raise RuntimeError("A zero-group and zero-image statement were conflated")
    if any(step.conclusion == false_zero_group for step in (db_step,)):
        raise RuntimeError("DB adopted prior incorrectly asserts group is zero")
    if any(false_zero_group in item.subgoals for item in (root_exp, upper_exp, hopf_exp, image_exp)):
        raise RuntimeError("The selected R41 chain acquired an incorrect zero-group premise")
    right = lifted_stable_composition(prior.rhs.generator)
    left = left_associated(right) if right is not None else None
    if left is None:
        raise RuntimeError("R38 composite cannot be lifted and reassociated")
    left_goal = GeneratorImage(zero_image.map, prior.rhs.generator, left)
    right_goal = GeneratorImage(zero_image.map, prior.rhs.generator, right)
    annihilator = Relation(left.left, Zero(), RelationType.EQUALITY)
    parts = component_image_obligations(right_goal)
    if parts is None or len(parts) != 2:
        raise RuntimeError("Wrong number of defined composition-image obligations")

    requested = (
        (zero_generator_goal, expand_generator_zero_from_composite(zero_generator_goal, left_goal)),
        (left_goal, expand_generator_image_associativity(left_goal)),
        (right_goal, expand_composite_generator_image(right_goal)),
        (annihilator, expand_cited_annihilator_specialization(annihilator, laws)),
    ) + tuple((part, expand_defined_stable_element_image(part)) for part in parts)
    selected = [(root, (root_exp,)), (upper, (upper_exp,)),
                (hopf, (hopf_exp,)), (zero_image, (image_exp,))]
    stages = {}
    for typed_goal, expected_options in requested:
        seen = public(typed_goal)
        matches = tuple(
            item for item in seen
            if any(item.rule.name == expected.rule.name
                   and item.subgoals == expected.subgoals
                   for expected in expected_options)
        )
        name = type(typed_goal).__name__
        stages[name] = stages.get(name, []) + [{
            "matching_public_options": len(matches),
            "isolated_options": len(expected_options),
        }]
        # An absent or ambiguous stage is a reported open goal, not a proof.
        selected.append((typed_goal, matches if len(matches) == 1 else ()))

    def scoped(goal):
        for candidate, options in selected:
            if type(goal) is type(candidate) and goal == candidate:
                return options
        return ()

    result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citation_ids[0],
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    proven = result.proven_steps
    inferred_zero_image = tuple(
        step for step in proven
        if step.conclusion == zero_image and step.rule is ProofRule.INFERENCE
    )
    false_zero_proved = any(step.conclusion == false_zero_group for step in proven)
    if false_zero_proved:
        raise RuntimeError("The canonical scoped search produced an incorrect zero-group claim")
    if result.status is ProofSearchStatus.COMPLETE:
        raise RuntimeError("The intentionally bounded R44 search unexpectedly completed the final root")
    return {
        "reviewed_root": "pi_12^7 = 0",
        "screened_toda59_sources": len(laws),
        "public_r43_ehp_root_options": 1,
        "public_r43_upper_delta_options": 1,
        "public_r43_hopf_options": 1,
        "public_r41_zero_image_options": 1,
        "r41_prior_adopted_as_db_given": True,
        "r41_prior_is_independent_literature": False,
        "zero_image_is_not_domain_zero_group": True,
        "wrong_pi10_5_zero_group_is_r41_direct_premise": False,
        "wrong_pi10_5_zero_group_was_proved": False,
        "source_bound_stage_public_options": stages,
        "canonical_bounded_search_status": result.status.value,
        "canonical_bounded_verified_steps": len(proven),
        "canonical_bounded_zero_image_inferred": len(inferred_zero_image) > 0,
        "canonical_bounded_zero_image_steps": len(inferred_zero_image),
        "canonical_bounded_open_goal_types": [type(x).__name__ for x in result.open_goals],
        "canonical_bounded_proven_step_types": [type(s.conclusion).__name__ for s in proven],
        "probe_is_not_full_web_search": True,
        "web_http_checked": False,
        "root_complete": False,
        "new_givens": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    state = verify_checkout()
    details = None if arguments.dry_run else inspected_frontier()
    gate = (
        "PASS_R44_R43_MERGE_SOURCE_PREFLIGHT" if arguments.dry_run else
        "PASS_R44_TYPED_ZERO_IMAGE_VERSUS_ZERO_GROUP_CANONICAL_FRONTIER_AUDITED"
    )
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r44"
    )
    directory.mkdir(parents=True, exist_ok=True)
    output = directory / ("preflight.json" if arguments.dry_run else "zero_image_tree_frontier.json")
    output.write_text(json.dumps({"phase": "174-R3-R7-R44", "state": state,
                                  "details": details, "gate": gate},
                                 ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R44_"
    for key, value in state.items():
        print(prefix + key.upper() + "=" + str(value))
    if details is not None:
        for key, value in details.items():
            print(prefix + key.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(output))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_source_guard.py`

```python
"""R44 reviewed source and no-write contract."""
from __future__ import annotations

from phase174_r3_r7_r44_public_zero_image_tree_frontier.source_guard import (
    BASE_HEAD, MERGED_HEAD, BASE_SHA, MERGED_SHA, PINS,
    matches_blob, normalize,
)


def test_reviewed_head_and_sha_pins_are_complete():
    assert len(BASE_HEAD) == len(MERGED_HEAD) == 40
    assert len(BASE_SHA) == len(MERGED_SHA) == 40
    assert all(len(pin) == 40 for pin in PINS.values())
    assert len(PINS) >= 8


def test_source_guard_normalization_accepts_equivalent_line_endings():
    payload = b"one\ntwo\n"
    from phase174_r3_r7_r44_public_zero_image_tree_frontier.source_guard import git_blob
    assert matches_blob(payload, git_blob(payload))
    assert matches_blob(payload.replace(b"\n", b"\r\n"), git_blob(payload))
    assert normalize(payload.replace(b"\n", b"\r\n")) == payload


def test_invalid_blob_pin_rejected_without_disabling_guard():
    assert matches_blob(b"something", "z" * 40) is False
    assert matches_blob(b"something", "123") is False
```

## `tests/test_static.py`

```python
"""R44 is audit-only, never another hidden production implementation."""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_audit_only_package_has_no_production_replacement():
    assert not (ROOT / "install.py").exists()
    assert not (ROOT / "replacement").exists()
    assert not (ROOT / "patch.py").exists()
    assert (ROOT / "run.ps1").is_file()


def test_audit_uses_canonical_search_and_typed_goal_separation():
    source = (ROOT / "audit.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
    calls = {node.func.id for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)}
    assert "search_registered_partial_proof" in calls
    assert "TodaPrimaryGroupZeroStatement" in calls
    assert "ImageZeroStatement" in names
    assert "ProofStep" in names and "ProofRule" in names
    assert "git" not in calls


def test_dry_run_is_implemented_and_does_not_modify_source():
    source = (ROOT / "run.ps1").read_text(encoding="utf-8")
    assert "param([switch]$DryRun)" in source
    assert "--dry-run" in source
    assert "python -B -m pytest" in source
    assert "-p no:cacheprovider" in source
```

## `tests/test_frontier.py`

```python
"""Public evidence is distinguished from optional inferred outcomes."""
from __future__ import annotations

from phase174_r3_r7_r44_public_zero_image_tree_frontier.audit import inspected_frontier


def test_actual_typed_r41_cannot_be_confused_with_pi10_5_zero_group():
    report = inspected_frontier()
    assert report["screened_toda59_sources"] == 1
    assert report["zero_image_is_not_domain_zero_group"] is True
    assert report["wrong_pi10_5_zero_group_is_r41_direct_premise"] is False
    assert report["wrong_pi10_5_zero_group_was_proved"] is False
    assert report["r41_prior_adopted_as_db_given"] is True
    assert report["r41_prior_is_independent_literature"] is False


def test_bounded_canonical_search_never_claims_web_completion():
    report = inspected_frontier()
    assert report["probe_is_not_full_web_search"] is True
    assert report["web_http_checked"] is False
    assert report["root_complete"] is False
    assert report["new_givens"] == 0
    assert report["production_files_changed"] == 0
    assert report["canonical_bounded_search_status"] in ("partial", "search_failed")
    assert report["canonical_bounded_verified_steps"] >= 1
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r44_public_zero_image_tree_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R44 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R44_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r44_public_zero_image_tree_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R44 canonical frontier audit failed' }
    $Groups = @(
        @{Name='R44_STATIC'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_static.py'},
        @{Name='R44_GUARD'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_source_guard.py'},
        @{Name='R44_FRONTIER'; Path='phase174_r3_r7_r44_public_zero_image_tree_frontier/tests/test_frontier.py'},
        @{Name='R43_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r43_public_ehp_map_property_wiring/tests/test_public.py'},
        @{Name='R41_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r41_adopted_db_zero_image_public_wiring/tests/test_public.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R44_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R44 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R44_RUN=PASS'
    Write-Output 'PHASE174_R3R7R44_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```

