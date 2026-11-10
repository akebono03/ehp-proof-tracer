# Phase 174 R3-R7-R48 追加コード全文

新規ディレクトリ `phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/` の各ファイルに追加。既存コード・クラス・関数は変更しません。


## __init__.py

```python

"""R48: cited lower Delta kernel in a canonical proof tree, read-only."""

```


## source_guard.py

```python

"""R48: independently verify reviewed GitHub HEAD and the R47 handoff bytes."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r46_prop42_dfs_audit.source_guard import (
    ROOT,
    R45_LOCAL_PINS,
    R45_PRODUCTION_PINS,
    REVIEWED_SEARCH_BLOB,
    git,
    matches_git_blob,
    normalized_sha256,
)

PREVIOUS_HEAD = "fe4f07940cdb5557397dc9e610b65b7eeaff0116"
REVIEWED_HEAD = "398ad86615ec8484e5a9fe04143e367c059d4c85"
REVIEWED_RULE_BLOBS = {
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py": "b90fe1fee5db04228ed986083b5214709045a7ea",
    "phase174_r3_r7_r36_cited_kernel_provider_wiring/audit.py": "b3d74e831edb49a60a54c5b609394fd815870068",
    "phase174_r3_r7_r32_lower_delta_kernel_audit/kernel_contract.py": "c2357859b00ed0b446bac7a060a6d0c134fc7de5",
    "phase165_r12_r29_kernel_connection.py": "170fc085a6d7a7aa9a9760647e35196f32f9f5ac",
}
R47_HANDOFF_FILES = {
    "phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/audit.py": "da67d06bd4c558e9bd220cf3b1ea20d0bda7780965d9267b4248394592cb321c",
    "phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/source_guard.py": "3acdc2aa7035fc2ee62190818d3ef2d7f78dcbf87b172feb29a9a733511d1161",
}


def verify_checkout() -> dict[str, object]:
    """Reject changed code, unknown local/remote HEAD, staged/dirty tracked files."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R48 ZIP must be extracted in the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R48 requires branch develop")
    remote_parts = git("ls-remote", "origin", "refs/heads/develop").split()
    if not remote_parts or remote_parts[0] != REVIEWED_HEAD:
        raise RuntimeError("Unreviewed GitHub develop HEAD; review new commits before R48")
    local_head = git("rev-parse", "HEAD")
    if local_head not in (PREVIOUS_HEAD, REVIEWED_HEAD):
        raise RuntimeError("R48 local HEAD differs from both reviewed R47 handoff states")
    staged = git("diff", "--cached", "--name-only").splitlines()
    tracked = git("diff", "--name-only").splitlines()
    if staged or tracked:
        raise RuntimeError("R48 requires no staged/tracked modifications: " + repr((staged, tracked)))
    for relative, blob in {**R45_PRODUCTION_PINS, **REVIEWED_RULE_BLOBS}.items():
        p = ROOT / relative
        if not p.is_file() or not matches_git_blob(p.read_bytes(), blob):
            raise RuntimeError("R48 reviewed mathematical source changed: " + relative)
    search = ROOT / "phase165_r3_recursive_search.py"
    if not search.is_file() or not matches_git_blob(search.read_bytes(), REVIEWED_SEARCH_BLOB):
        raise RuntimeError("R48 reviewed canonical search changed")
    for relative, digest in {**R45_LOCAL_PINS, **R47_HANDOFF_FILES}.items():
        p = ROOT / relative
        if not p.is_file() or normalized_sha256(p.read_bytes()) != digest:
            raise RuntimeError("R48 reviewed handoff file differs: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": local_head,
        "remote_head": REVIEWED_HEAD,
        "mode": "R47_MERGED" if local_head == REVIEWED_HEAD else "R47_REVIEWED_PRE_MERGE",
        "reviewed_mathematical_blobs": len(R45_PRODUCTION_PINS) + len(REVIEWED_RULE_BLOBS) + 1,
        "reviewed_r47_handoff_files": len(R47_HANDOFF_FILES),
        "new_given": 0,
        "production_files_changed": 0,
        "full_pytest": False,
    }

```


## audit.py

```python

"""R48: extend the R47 canonical proof tree across the cited lower Delta kernel.

Read-only source-first search: R35/R36 kernel inference must use one inferred
free-cyclic domain and distinct earlier Toda Proposition 5.8/(5.10) GIVENs.
The Prop. 2.7 upper-Delta witness remains outside scope; no root proof is claimed.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.source_guard import verify_checkout


def inspect_integrated_lower_kernel_frontier() -> dict[str, object]:
    """Run one real canonical DFS through zero-image, Hopf, and lower Delta kernel."""
    from expression import Zero
    from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from map_property_rules import ImageZeroStatement
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from phase165_r12_r12_ehp_consequences import (
        EHPImageEqualsKernelStatement,
        proof_has_general_prop42_ancestor,
    )
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
    from phase169_r10e4_ordered_db_prior.db_prior import admitted_db_step, verified_db_step
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations,
        expand_composite_generator_image,
    )
    from phase169_r10eq_r1_universal_stable_definition.definition import expand_defined_stable_element_image
    from phase174_r3_r7_r3_ehp_zero_rule.rule import RULE_NAME as ROOT_RULE, ehp_zero_inputs
    from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
        RULE_NAME as HOPF_RULE,
        hopf_injectivity_from_zero_image_inputs,
    )
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import (
        RULE_NAME as UPPER_RULE,
        upper_delta_surjectivity_inputs,
    )
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r34_prior_lower_delta_source_wiring.source import checked_prior_statements
    from phase174_r3_r7_r40_adopted_db_zero_image_isolated.rule import RULE_NAME as ZERO_IMAGE_RULE
    from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import screened_general_law
    from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
        left_associated, lifted_stable_composition,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import expand_generator_image_associativity
    from phase174_r3_r7_r7_composite_zero_audit.rule import expand_generator_zero_from_composite
    from phase174_r3_r7_r12_toda59_annihilator_source.rule import expand_cited_annihilator_specialization
    from proof import ProofRule, ProofStep, Relation, RelationType
    from toda_rules import TodaProp42ExactnessStatement

    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    bridge = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    laws = screened_general_law(bridge)
    if len(laws) != 1:
        raise RuntimeError("R44 cited Toda (5.9) source is missing")
    source_links = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == laws[0]
    )
    if len(source_links) != 1:
        raise RuntimeError("R44 cited Toda (5.9) source link changed")
    citing_id = source_links[0].assertion_id
    general_prop42 = TodaProp42GeneralExactnessStatement()
    prop42_links = tuple(
        link for link in bridge.proof_links
        if isinstance(link.step, ProofStep)
        and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == general_prop42
    )
    if len(prop42_links) != 1:
        raise RuntimeError("R46 cited Prop. 4.2 source link changed")

    root_inputs = ehp_zero_inputs(root)
    if root_inputs is None or len(root_inputs) != 4:
        raise RuntimeError("R47 root shape changed")
    upper = root_inputs[0]
    upper_inputs = upper_delta_surjectivity_inputs(upper)
    if upper_inputs is None or len(upper_inputs) != 4:
        raise RuntimeError("R47 upper Delta shape changed")
    hopf = upper_inputs[0]
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(hopf)
    if hopf_inputs is None or len(hopf_inputs) != 2:
        raise RuntimeError("R47 Hopf shape changed")
    zero_image, hopf_exactness = hopf_inputs
    lower_image_kernel = upper_inputs[1]
    lower_kernel_multiple = upper_inputs[2]
    prop27_witness = upper_inputs[3]
    lower_exactness = TodaProp42ExactnessStatement(lower_image_kernel.window)
    if (type(zero_image) is not ImageZeroStatement
            or type(lower_image_kernel) is not EHPImageEqualsKernelStatement):
        raise RuntimeError("R47 reviewed typed EHP proof obligations changed")

    public = shared_expansion_provider(bridge, proof_target=root)
    selected: list[tuple[object, tuple]] = []
    reviewed_counts: dict[str, int] = {}

    def select(goal: object, name: str, subgoals: tuple) -> None:
        """Use the first *existing* matching public rule, never fabricate one."""
        matches = tuple(
            option for option in public(goal)
            if option.rule.name == name and option.subgoals == subgoals
        )
        reviewed_counts[name] = len(matches)
        if not matches:
            raise RuntimeError("Reviewed public proof branch missing: " + name)
        selected.append((goal, (matches[0],)))

    select(root, ROOT_RULE, root_inputs)
    select(upper, UPPER_RULE, upper_inputs)
    select(hopf, HOPF_RULE, hopf_inputs)
    zero_options = tuple(x for x in public(zero_image) if x.rule.name == ZERO_IMAGE_RULE)
    if not zero_options or len(zero_options[0].subgoals) != 2:
        raise RuntimeError("R44 adopted-DB zero-image public branch missing")
    zero_option = zero_options[0]
    selected.append((zero_image, (zero_option,)))
    presentation, zero_generator = zero_option.subgoals
    db_step = admitted_db_step(presentation, proof_target=root, bridge=bridge)
    if (db_step is None or db_step.rule is not ProofRule.GIVEN
            or not verified_db_step(db_step, proof_target=root, bridge=bridge)):
        raise RuntimeError("R44 DB prior admission failed")
    if zero_image.map.source_group != presentation.lhs:
        raise RuntimeError("The image source group is not the cited DB prior group")
    false_zero_group = TodaPrimaryGroupZeroStatement(presentation.lhs)
    if false_zero_group == root:
        raise RuntimeError("R47 target root collided with false zero group")

    right = lifted_stable_composition(presentation.rhs.generator)
    left = left_associated(right) if right is not None else None
    if left is None:
        raise RuntimeError("R44 zero-image associativity data unavailable")
    left_goal = GeneratorImage(zero_image.map, presentation.rhs.generator, left)
    right_goal = GeneratorImage(zero_image.map, presentation.rhs.generator, right)
    annihilator = Relation(left.left, Zero(), RelationType.EQUALITY)
    parts = component_image_obligations(right_goal)
    if parts is None or len(parts) != 2:
        raise RuntimeError("R44 composite generator image obligations changed")

    # R44's exact reviewed public generator-image chain.
    r44_requests = (
        (zero_generator, expand_generator_zero_from_composite(zero_generator, left_goal)),
        (left_goal, expand_generator_image_associativity(left_goal)),
        (right_goal, expand_composite_generator_image(right_goal)),
        (annihilator, expand_cited_annihilator_specialization(annihilator, laws)),
    ) + tuple((part, expand_defined_stable_element_image(part)) for part in parts)
    r44_stage_counts: list[dict[str, object]] = []
    for goal, expected in r44_requests:
        matches = tuple(
            option for option in public(goal)
            if any(
                option.rule.name == candidate.rule.name
                and option.subgoals == candidate.subgoals
                for candidate in expected
            )
        )
        r44_stage_counts.append({
            "goal_type": type(goal).__name__,
            "reviewed_public_matches": len(matches),
        })
        selected.append((goal, (matches[0],) if matches else ()))

    # R46's genuine cited generic exactness rules.  Use source-linked
    # expansions, not saved R46 ProofSteps or synthetic GIVEN leaves.
    exact_rule = "Toda Proposition 4.2: generic consecutive EHP specialization"
    select(hopf_exactness, exact_rule, (general_prop42,))
    select(lower_image_kernel, "EHP exactness implies image equals kernel", (lower_exactness,))
    select(lower_exactness, exact_rule, (general_prop42,))

    # R35/R36: the lower Delta kernel is an inference from one inferred
    # free-cyclic domain and two earlier independently cited printed facts.
    # These are exact typed claims, not an invented kernel/root GIVEN.
    codomain, signed_image = checked_prior_statements()
    domain = Relation(
        lower_kernel_multiple.domain,
        FreeCyclicGroup(lower_kernel_multiple.source_generator),
        RelationType.EQUALITY,
    )
    if (signed_image.map != lower_kernel_multiple.map
            or signed_image.element != lower_kernel_multiple.source_generator
            or codomain.lhs != lower_kernel_multiple.map.target_group
            or lower_kernel_multiple.multiple != 2):
        raise RuntimeError("R48 typed kernel does not match the earlier Toda premises")
    source_claims = (
        (codomain, "Proposition 5.8"),
        (signed_image, "(5.10)"),
    )
    earlier_source_ids: list[str] = []
    for claim, locator in source_claims:
        links = tuple(
            link for link in bridge.proof_links
            if isinstance(link.step, ProofStep)
            and link.step.rule is ProofRule.GIVEN
            and not link.step.premises
            and link.step.conclusion == claim
            and getattr(
                getattr(link.step.inference_rule, "literature_reference", None),
                "locator", None,
            ) == locator
        )
        if not links:
            raise RuntimeError("R48 earlier cited source is missing: " + locator)
        earlier_source_ids.append(links[0].assertion_id)
    select(lower_kernel_multiple, KERNEL_RULE, (domain, codomain, signed_image))
    diagonal_options = tuple(
        option for option in public(domain)
        if option.rule.name == "generic cited typed scalar specialization"
        and len(option.subgoals) == 1
        and any(
            isinstance(link.step, ProofStep)
            and link.step.rule is ProofRule.GIVEN
            and link.step.conclusion == option.subgoals[0]
            and find_inference_matches_for_rule(option.rule, (link.step,))
            for link in bridge.proof_links
        )
    )
    if not diagonal_options:
        raise RuntimeError("R48 general-source diagonal specialization absent")
    # First Successful Proof Search: let canonical DFS stop at its first success.
    selected.append((domain, diagonal_options))
    reviewed_counts["generic cited typed scalar specialization"] = len(diagonal_options)

    # Deliberate frontier: the Prop. 2.7 witness and remaining root branches
    # have not yet been integrated in R48.  Do not fill them by assertion.
    visited: list[str] = []
    def scoped(goal: object) -> tuple:
        if type(goal) is type(prop27_witness) and goal == prop27_witness:
            visited.append("prop27_witness_outside_scope")
            return ()
        for expected_goal, options in selected:
            if type(goal) is type(expected_goal) and goal == expected_goal:
                visited.append(type(goal).__name__)
                return options
        visited.append("outside_scope:" + type(goal).__name__)
        return ()

    result = search_registered_partial_proof(
        n=7, k=5, goal=root, bridge=bridge,
        citing_assertion_id=citing_id,
        expansion_provider=scoped, lookup_mode="typed_reference",
    )
    proven = result.proven_steps
    def inferred(goal: object) -> tuple:
        return tuple(
            step for step in proven
            if step.rule is ProofRule.INFERENCE
            and type(step.conclusion) is type(goal)
            and step.conclusion == goal
        )
    zero_steps = inferred(zero_image)
    hopf_steps = inferred(hopf)
    hopf_exact_steps = inferred(hopf_exactness)
    lower_exact_steps = inferred(lower_exactness)
    lower_image_kernel_steps = inferred(lower_image_kernel)
    lower_kernel_steps = inferred(lower_kernel_multiple)
    domain_steps = inferred(domain)
    if any(step.conclusion == false_zero_group for step in proven):
        raise RuntimeError("Incorrect group zero substituted for image zero")
    if result.status is ProofSearchStatus.COMPLETE or any(step.conclusion == root for step in proven):
        raise RuntimeError("Intentionally bounded R47 claims a completed group proof")

    def cited_source_ancestor(step: ProofStep, claim: object) -> bool:
        seen: set[int] = set()
        def visit(node: ProofStep) -> bool:
            if id(node) in seen:
                return False
            seen.add(id(node))
            if node.rule is ProofRule.GIVEN and node.conclusion == claim:
                return True
            return any(visit(parent) for parent in node.premises)
        return visit(step)

    if hopf_steps and not any(
        cited_source_ancestor(step, laws[0])
        and proof_has_general_prop42_ancestor(step)
        for step in hopf_steps
    ):
        raise RuntimeError("Hopf inference lacks both independent proof ancestries")
    if lower_image_kernel_steps and not all(
        proof_has_general_prop42_ancestor(step) for step in lower_image_kernel_steps
    ):
        raise RuntimeError("Lower EHP image-kernel inference lacks Prop. 4.2 ancestry")

    # Validate the actual accepted canonical tree and its THREE exact parents.
    kernel_cited_ancestry = any(
        tuple(parent.conclusion for parent in step.premises)
        == (domain, codomain, signed_image)
        and tuple(parent.rule for parent in step.premises)
        == (ProofRule.INFERENCE, ProofRule.GIVEN, ProofRule.GIVEN)
        and cited_source_ancestor(step, codomain)
        and cited_source_ancestor(step, signed_image)
        for step in lower_kernel_steps
    )
    if lower_kernel_steps and not kernel_cited_ancestry:
        raise RuntimeError("Lower kernel inference lacks the three prior typed premises")
    if any(step.conclusion in (root, lower_kernel_multiple)
           and step.rule is ProofRule.GIVEN for step in proven):
        raise RuntimeError("R48 kernel/root were incorrectly asserted as GIVEN")

    return {
        "root": "pi_12^7 = 0",
        "source_first_toda59_given": len(source_links),
        "source_first_general_prop42_given": len(prop42_links),
        "r44_db_prior_is_independent_literature": False,
        "r44_db_prior_admitted_in_group_root_scope": True,
        "selected_public_rule_candidate_counts": reviewed_counts,
        "r44_generator_stage_public_matches": r44_stage_counts,
        "canonical_status": result.status.value,
        "canonical_verified_steps": len(proven),
        "canonical_zero_image_inference_count": len(zero_steps),
        "canonical_hopf_exactness_inference_count": len(hopf_exact_steps),
        "canonical_hopf_injectivity_inference_count": len(hopf_steps),
        "canonical_lower_exactness_inference_count": len(lower_exact_steps),
        "canonical_lower_image_kernel_inference_count": len(lower_image_kernel_steps),
        "canonical_hopf_has_toda59_and_prop42_ancestors": any(
            cited_source_ancestor(step, laws[0])
            and proof_has_general_prop42_ancestor(step)
            for step in hopf_steps
        ),
        "canonical_lower_image_kernel_has_prop42_ancestor": any(
            proof_has_general_prop42_ancestor(step)
            for step in lower_image_kernel_steps
        ),
        "canonical_lower_kernel_inference_count": len(lower_kernel_steps),
        "canonical_lower_kernel_three_premises_cited": kernel_cited_ancestry,
        "canonical_lower_kernel_domain_inferred": len(domain_steps) > 0,
        "canonical_lower_kernel_prior_reference_ids": earlier_source_ids,
        "canonical_visited_prop27_frontier": "prop27_witness_outside_scope" in visited,
        "canonical_proven_goal_types": dict(sorted(Counter(
            type(step.conclusion).__name__ for step in proven
        ).items())),
        "canonical_open_goal_types": dict(sorted(Counter(
            type(goal).__name__ for goal in result.open_goals
        ).items())),
        "canonical_scoped_visit_trace": visited,
        "wrong_pi10_5_group_zero_proved": False,
        "kernel_was_not_adopted_as_given": True,
        "isolated_proof_steps_injected": False,
        "new_givens": 0,
        "new_mathematical_rules": 0,
        "production_files_changed": 0,
        "root_complete": False,
        "web_http_checked": False,
        "full_pytest": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    details = None if args.dry_run else inspect_integrated_lower_kernel_frontier()
    connected = details is not None and all((
        details["canonical_zero_image_inference_count"] > 0,
        details["canonical_hopf_exactness_inference_count"] > 0,
        details["canonical_hopf_injectivity_inference_count"] > 0,
        details["canonical_hopf_has_toda59_and_prop42_ancestors"],
        details["canonical_lower_exactness_inference_count"] > 0,
        details["canonical_lower_image_kernel_inference_count"] > 0,
        details["canonical_lower_image_kernel_has_prop42_ancestor"],
        details["canonical_lower_kernel_inference_count"] > 0,
        details["canonical_lower_kernel_three_premises_cited"],
        details["canonical_lower_kernel_domain_inferred"],
        details["canonical_visited_prop27_frontier"],
    ))
    gate = (
        "PASS_R48_REVIEWED_R47_SOURCE_PREFLIGHT" if args.dry_run else
        "PASS_R48_CITED_LOWER_KERNEL_CONNECTED_PROP27_PENDING"
        if connected else
        "PASS_R48_KERNEL_CONNECTION_GAP_RECORDED"
    )
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r48"
    )
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / ("preflight.json" if args.dry_run else "cited_lower_kernel_frontier.json")
    path.write_text(json.dumps({
        "phase": "174-R3-R7-R48", "state": state,
        "details": details, "gate": gate,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R48_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    if details is not None:
        for name, value in details.items():
            print(prefix + name.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(path))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```


## run.ps1

```powershell

param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R48 Source Guard failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R48_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.audit
    if ($LASTEXITCODE -ne 0) { throw 'R48 integrated kernel audit failed' }
    $Groups = @(
        @{Name='R48_STATIC'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_static.py'; Mode='importlib'},
        @{Name='R48_GUARD'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_guard.py'; Mode='importlib'},
        @{Name='R48_FRONTIER'; Path='phase174_r3_r7_r48_cited_lower_kernel_tree_frontier/tests/test_frontier.py'; Mode='importlib'},
        @{Name='R47_FRONTIER_REGRESSION'; Path='phase174_r3_r7_r47_zero_image_prop42_hopf_bridge/tests/test_frontier.py'; Mode='importlib'},
        @{Name='R36_CITED_KERNEL_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'; Mode='importlib'},
        @{Name='R35_GENERIC_KERNEL_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'; Mode='importlib'},
        @{Name='R34_PRIOR_SOURCE_REGRESSION'; Path='phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_public.py'; Mode='importlib'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R48_TEST_GROUP=' + $Group.Name)
        $ImportMode = $Group.Mode
        python -B -m pytest -q "--import-mode=$ImportMode" -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) { throw ('R48 focused pytest failed: ' + $Group.Name) }
    }
    Write-Output 'PHASE174_R3R7R48_RUN=PASS'
    Write-Output 'PHASE174_R3R7R48_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}

```


## tests/test_static.py

```python

"""R48 only adds an auditable scoped proof-search procedure."""
from __future__ import annotations

import ast
from pathlib import Path

PKG = Path(__file__).resolve().parents[1]


def test_new_python_source_parses_without_placeholders() -> None:
    for path in (PKG / "audit.py", PKG / "source_guard.py", PKG / "tests/test_static.py", PKG / "tests/test_frontier.py", PKG / "tests/test_guard.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        assert not any(isinstance(node, ast.Constant) and node.value is Ellipsis for node in ast.walk(tree))


def test_runner_is_read_only_and_runs_only_focused_pytest() -> None:
    script = (PKG / "run.ps1").read_text(encoding="utf-8")
    assert "--dry-run" in script
    assert "--import-mode=$ImportMode" in script
    assert "R36_CITED_KERNEL_REGRESSION" in script
    assert "R47_FRONTIER_REGRESSION" in script
    assert "FULL_PYTEST=False" in script
    assert "git reset" not in script
    assert "git clean" not in script
    assert "install.py" not in script


def test_no_direct_proof_or_new_source_is_installed() -> None:
    source = (PKG / "audit.py").read_text(encoding="utf-8")
    assert "ProofStep(" not in source
    assert "checked_prior_statements()" in source
    assert "search_registered_partial_proof(" in source
    assert "isolated_proof_steps_injected" in source
    assert "R35/R36" in source

```


## tests/test_guard.py

```python

"""R48 verifies a reviewed HEAD and the R47 handoff without production changes."""
from __future__ import annotations

from pathlib import Path

from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.source_guard import (
    REVIEWED_HEAD, REVIEWED_RULE_BLOBS, R47_HANDOFF_FILES,
    ROOT, normalized_sha256, verify_checkout,
)


def test_guard_pins_math_rules_and_the_prior_audit() -> None:
    assert len(REVIEWED_HEAD) == 40
    assert all(len(blob) == 40 for blob in REVIEWED_RULE_BLOBS.values())
    assert len(R47_HANDOFF_FILES) == 2
    assert all(len(digest) == 64 for digest in R47_HANDOFF_FILES.values())
    assert Path(ROOT).is_absolute()


def test_guard_accepts_the_exact_referenced_checkout() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["remote_head"] == REVIEWED_HEAD
    assert state["production_files_changed"] == 0
    assert state["full_pytest"] is False
    for relative, digest in R47_HANDOFF_FILES.items():
        assert normalized_sha256((ROOT / relative).read_bytes()) == digest

```


## tests/test_frontier.py

```python

"""R48 requires genuine canonical R35 kernel proof with two cited prior leaves."""
from __future__ import annotations

from phase174_r3_r7_r48_cited_lower_kernel_tree_frontier.audit import (
    inspect_integrated_lower_kernel_frontier,
)


def test_canonical_kernel_proof_is_inferred_from_three_cited_parents() -> None:
    report = inspect_integrated_lower_kernel_frontier()
    assert report["canonical_status"] == "partial"
    assert report["canonical_lower_kernel_inference_count"] == 1
    assert report["canonical_lower_kernel_three_premises_cited"] is True
    assert report["canonical_lower_kernel_domain_inferred"] is True
    assert len(report["canonical_lower_kernel_prior_reference_ids"]) == 2
    assert report["kernel_was_not_adopted_as_given"] is True


def test_zero_image_and_hopf_inference_survive_the_kernel_connection() -> None:
    report = inspect_integrated_lower_kernel_frontier()
    assert report["canonical_zero_image_inference_count"] == 1
    assert report["canonical_hopf_injectivity_inference_count"] == 1
    assert report["canonical_hopf_has_toda59_and_prop42_ancestors"] is True
    assert report["canonical_lower_image_kernel_inference_count"] == 1
    assert report["canonical_lower_image_kernel_has_prop42_ancestor"] is True
    assert report["canonical_verified_steps"] > 14


def test_prop27_frontier_is_left_unresolved_without_false_completion() -> None:
    report = inspect_integrated_lower_kernel_frontier()
    assert report["canonical_visited_prop27_frontier"] is True
    assert report["canonical_open_goal_types"].get("Prop27TypedHopfDeltaStatement", 0) >= 1
    assert report["root_complete"] is False
    assert report["wrong_pi10_5_group_zero_proved"] is False
    assert report["new_givens"] == 0
    assert report["new_mathematical_rules"] == 0
    assert report["production_files_changed"] == 0
    assert report["web_http_checked"] is False
    assert report["full_pytest"] is False

```
