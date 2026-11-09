# R53 コード全文（省略なし）

変更する既存ファイル: `phase165_r55_nk_only_goal.py`。変更する関数: `search_group_from_registered_goal()`。
新規 Provider: `phase174_r3_r7_r53_public_source_bound_kernel/provider.py`。

既存ファイルの top-level import に変更はありません。変更後も同じ import 全文を示します。

```python
from __future__ import annotations

from dataclasses import fields, is_dataclass, replace

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus, make_partial_proof_result
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from proof import Relation, RelationType
from unified_statement_registry import AssertionOrigin
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
```

## 変更後の関数全体（既存クラスの変更なし）

```python
def search_group_from_registered_goal(*, n: int, k: int, bridge=None, proof_order_catalog=None, goal=None, context_sink=None):
    """Search typed goals. Zero goals use the same evidenced backward engine."""
    from homotopy_groups import TodaPrimaryGroupZeroStatement

    from phase166_r3af_goal_adapter import database_zero_group_goal_candidates

    target = TodaPrimaryGroup(n + k, n)
    make_partial_proof_result(n=n, k=k, status=ProofSearchStatus.NOT_SEARCHED)

    if goal is not None:
        valid_relation = (
            isinstance(goal, Relation)
            and goal.relation_type is RelationType.EQUALITY
            and goal.lhs == target
            and isinstance(goal.rhs, _GROUP_STRUCTURES)
        )
        valid_zero = (
            isinstance(goal, TodaPrimaryGroupZeroStatement)
            and goal.group == target
        )
        if not valid_relation and not valid_zero:
            raise ValueError("goal must be a typed group statement for the requested n,k")

    if goal is None:
        zeros = database_zero_group_goal_candidates(n=n, k=k)
        if len(zeros) == 1:
            candidate = zeros[0]
        else:
            if bridge is None:
                bridge = build_shared_typed_bridge()
            candidates = registered_group_goal_candidates(bridge, n=n, k=k)
            if len(candidates) != 1:
                explanation = (
                    "群構造・生成元の型付き証明目標を指定してください"
                    if not candidates else
                    "群構造の型付き候補が複数あり、証明目標を一意に選択できない"
                )
                return make_partial_proof_result(
                    n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                    open_goals=(target,), diagnostics=(explanation,),
                )
            candidate = candidates[0]
    else:
        candidate = goal

    if bridge is None:
        bridge = build_shared_typed_bridge()

    if isinstance(candidate, TodaPrimaryGroupZeroStatement):
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        from phase165_r52_r2_search_adapter import search_registered_partial_proof

        from phase165_r52_r9_shared_math import shared_expansion_provider

        assertions = tuple(bridge.registry._assertions.values())
        if not assertions:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=("型付き命題台帳が空です",),
            )
        # The DB target has no publication position. Cite only independently
        # positioned fixed source statements; invent no target citation ID.
        context_id = assertions[0].assertion_id
        from phase173_r4_r11_zero_public_connection.route import (
            prepare_zero_toda56_public_connection,
        )
        zero_connection = prepare_zero_toda56_public_connection(
            bridge=bridge, goal=candidate,
        )
        if zero_connection is None:
            screened = screen_independent_sources_for_derived_goal(
                bridge, goal=candidate,
            )
            provider = shared_expansion_provider(
                screened, proof_target=candidate,
            )
        else:
            screened, provider = zero_connection
        if context_sink is not None:
            context_sink(screened)
        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
            build_public_source_bound_kernel_provider,
        )
        provider = build_public_source_bound_kernel_provider(provider, screened)
        return search_registered_partial_proof(
            n=n, k=k, goal=candidate, bridge=screened,
            citing_assertion_id=context_id,
            expansion_provider=provider, lookup_mode="typed_reference",
        )

    if proof_order_catalog is None:
        from phase165_r57_r16_web_proof_order import resolve_reviewed_order_catalog

        proof_order_catalog, order_diagnostic = resolve_reviewed_order_catalog(
            bridge, n=n, k=k,
        )
        if order_diagnostic is not None:
            pending = make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
            if n == 4 and k >= 3:
                from phase173_r4_r15r8_public_abstract_sidecar.attach import (
                    attach_certified_abstract_structure,
                )
                return attach_certified_abstract_structure(
                    pending, n=n, k=k, goal=candidate, bridge=bridge,
                )
            return pending
    citing_id = resolve_specialized_goal_citing_id(bridge, candidate)
    search_kwargs = dict(
        n=n, k=k, group_structure=candidate.rhs, bridge=bridge,
        proof_order_catalog=proof_order_catalog,
        context_sink=context_sink,
    )
    if citing_id is not None:
        search_kwargs["citing_assertion_id"] = citing_id
    result = search_shared_group_goal(**search_kwargs)
    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    if n == 4 and k >= 3:
        from phase173_r4_r15r8_public_abstract_sidecar.attach import (
            attach_certified_abstract_structure,
        )
        return attach_certified_abstract_structure(
            result, n=n, k=k, goal=candidate, bridge=bridge,
        )
    return result
```

## provider.py

```python
"""Source-certified inferred-domain preference for generic cyclic Delta kernels.

R53 makes R52's successful *ordinary inference obligation* reusable in the
public zero-group search. This module registers no source, GIVEN, proof step,
or new mathematical inference rule. All earlier candidate expansions remain.
"""
from __future__ import annotations

from typing import Callable

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import GoalExpansion, SourceBoundGoal
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import (
    RULE_NAME as KERNEL_RULE,
)
from proof import ProofRule, ProofStep, Relation, find_inference_matches_for_rule
from unified_statement_registry import AssertionOrigin

SPECIALIZATION_RULE = "generic cited typed scalar specialization"


def cited_inferred_domain_sources(
    domain: Relation,
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> tuple[object, ...]:
    """Find only linked, positioned GIVEN sources matching a real inference.

    A registered DB group result, an unattached fact, or a citation label alone
    cannot supply a SourceBoundGoal premise.
    """
    if type(domain) is not Relation or not isinstance(bridge, RegistryBridgeResult):
        return ()
    valid: list[object] = []
    for option in provider(domain):
        if (type(option) is not GoalExpansion
                or option.rule.name != SPECIALIZATION_RULE
                or len(option.subgoals) != 1):
            continue
        source = option.subgoals[0]
        for link in bridge.proof_links:
            step = link.step
            if (not isinstance(step, ProofStep)
                    or step.rule is not ProofRule.GIVEN
                    or step.premises
                    or step.conclusion != source):
                continue
            assertion = bridge.registry.assertion(link.assertion_id)
            reference = bridge.registry.reference(assertion.reference_id)
            if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                    or assertion.content != source
                    or type(reference.publication_position) is not int
                    or reference.publication_position < 1
                    or getattr(getattr(step.inference_rule, "literature_reference", None),
                               "locator", None) != reference.locator):
                continue
            if not find_inference_matches_for_rule(option.rule, (step,)):
                continue
            if not any(type(old) is type(source) and old == source for old in valid):
                valid.append(source)
    return tuple(valid)


def build_public_source_bound_kernel_provider(
    provider: Callable[[object], tuple[GoalExpansion, ...]],
    bridge: RegistryBridgeResult,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Prepend sourced domain obligations to existing general R35 proposals.

    This is strictly a preferred *search candidate*, not evidence. Its
    subgoal resolves by checked INFERENCE; the existing R35 guard continues
    to require one inferred free-cyclic group and two cited GIVEN parents.
    For goals without the exact typed rule or positioned source, return the
    original candidates unchanged and in the original order.
    """
    if not callable(provider) or not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("expected a shared provider and screened source bridge")

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        original = provider(goal)
        if type(goal) is not KernelMultipleStatement:
            return original
        bound: list[GoalExpansion] = []
        for option in original:
            if (type(option) is not GoalExpansion
                    or option.rule.name != KERNEL_RULE
                    or len(option.subgoals) != 3
                    or type(option.subgoals[0]) is not Relation):
                continue
            domain = option.subgoals[0]
            for source in cited_inferred_domain_sources(domain, provider, bridge):
                proposal = GoalExpansion(
                    rule=option.rule,
                    subgoals=(SourceBoundGoal(conclusion=domain, source=source),)
                    + option.subgoals[1:],
                )
                if proposal not in bound:
                    bound.append(proposal)
        return tuple(bound) + original

    return expand
```

## source_guard.py

```python
"""R53 source guard: pin the R52-merged GitHub develop and reviewed code blobs."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVIEWED_HEAD = "1151d6a3044fd7fae2ff1fb864a83afdaefc285d"
TARGET = "phase165_r55_nk_only_goal.py"
TARGET_BLOB = "9aa232c8f98a7a75f27266044224eddfa98c5e04"
REVIEWED_BLOBS = {
    "phase165_r52_r9_shared_math.py": "534b552856fefc8315b243fecc3170ee5792ebc7",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase165_r52_r2_search_adapter.py": "c1d08b803a4d9f9e4e1ad5180a1487422f1cd191",
    "web_group_proof.py": "2c66da9c8e80a13812a63b6adda34c9414d8413c",
    "phase174_r3_r7_r52_public_kernel_source_bound_probe/probe.py": "1e7d44acd7829fad858c2c88139174fe61c59fa7",
    "phase174_r3_r7_r35_isolated_cyclic_delta_kernel/rule.py": "fac88c852cd4c18e8d013e3dc12ab95ad57d7b03",
    "phase174_r3_r7_r37_upper_delta_surjectivity_isolated/rule.py": "e388d8d20710d1d3e7df4bee115c98a0116e32b4",
    "phase174_r3_r7_r3_ehp_zero_rule/rule.py": "8834cbefbfca5bcca18dc01f072c9738a05f7bdc",
    "phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/audit.py": "033410427c965f73080d6a9c3ed42f93129b0950",
    "phase174_r3_r7_r51_public_route_gap_audit/audit.py": "9f48c852950be09f44ef2ffe653c54a5fc59a090",
    "phase174_r3_r7_r52r2_registry_assertion_id_fix/replacement/audit.py": "233f6b4a0283309cbde0a5ebee9235a2e303506b",
}


def git(*args: str) -> str:
    return subprocess.run(
        ("git",) + args,
        cwd=ROOT, capture_output=True, check=True,
        text=True, encoding="utf-8", errors="replace",
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, cwd=ROOT, capture_output=True, check=True,
    ).stdout


def git_blob(data: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(data)).encode("ascii") + b"\x00" + data
    ).hexdigest()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def verify_checkout() -> dict[str, object]:
    """Fail closed for unreviewed HEAD, source edits, staged paths and blobs."""
    if Path(git("rev-parse", "--show-toplevel")).resolve() != ROOT.resolve():
        raise RuntimeError("R53 must be unpacked under the repository root")
    if git("branch", "--show-current") != "develop":
        raise RuntimeError("R53 expects the develop branch")
    head = git("rev-parse", "HEAD")
    remote = git("ls-remote", "origin", "refs/heads/develop")
    remote_head = remote.split()[0] if remote else ""
    if head != REVIEWED_HEAD or remote_head != REVIEWED_HEAD:
        raise RuntimeError("Reviewed R52 HEAD differs: source audit required")
    if git("diff", "--cached", "--name-only"):
        raise RuntimeError("Staged modifications require review before R53")
    changed = tuple(git("diff", "--name-only").splitlines())
    if any(item != TARGET for item in changed):
        raise RuntimeError("Unreviewed tracked working change: " + repr(changed))
    reviewed = {TARGET: TARGET_BLOB, **REVIEWED_BLOBS}
    for relative, expected in reviewed.items():
        contents = git_bytes("show", "HEAD:" + relative)
        if git_blob(contents) != expected:
            raise RuntimeError("GitHub-reviewed committed blob changed: " + relative)
        if relative != TARGET and normalized((ROOT / relative).read_bytes()) != normalized(contents):
            raise RuntimeError("Pinned mathematical or public code changed locally: " + relative)
    return {
        "source_guard": "PASS",
        "local_head": head,
        "remote_head": remote_head,
        "reviewed_blob_count": len(reviewed),
        "tracked_changes": changed,
        "full_pytest": False,
    }
```

## install.py

```python
"""R53: guarded, minimal public-zero-group provider integration.

Replaces one complete existing function with a checked copy that wraps its
already screened provider. The independent R35 mathematical rule is unchanged.
"""
from __future__ import annotations

import argparse
import ast
from pathlib import Path

from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import (
    ROOT, TARGET, git_bytes, normalized, verify_checkout,
)

PACKAGE = Path(__file__).resolve().parent
OLD_ANCHOR = (
    "        if context_sink is not None:\n"
    "            context_sink(screened)\n"
    "        return search_registered_partial_proof(\n"
)
NEW_ANCHOR = (
    "        if context_sink is not None:\n"
    "            context_sink(screened)\n"
    "        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (\n"
    "            build_public_source_bound_kernel_provider,\n"
    "        )\n"
    "        provider = build_public_source_bound_kernel_provider(provider, screened)\n"
    "        return search_registered_partial_proof(\n"
)


def function_source(source: str, function: str) -> str:
    """Extract a whole top-level definition, not a few patch lines."""
    parsed = ast.parse(source)
    matches = tuple(
        item for item in parsed.body
        if isinstance(item, ast.FunctionDef) and item.name == function
    )
    if len(matches) != 1:
        raise RuntimeError("Expected one callable to replace: " + function)
    lines = source.splitlines(keepends=True)
    return "".join(lines[matches[0].lineno - 1:matches[0].end_lineno])


def patched_source(original: str) -> str:
    """Only change the exact public zero-group search branch, once."""
    current_function = function_source(original, "search_group_from_registered_goal")
    if OLD_ANCHOR in current_function and NEW_ANCHOR not in current_function:
        if current_function.count(OLD_ANCHOR) != 1:
            raise RuntimeError("R53 public zero-branch anchor was repeated")
        replacement = current_function.replace(OLD_ANCHOR, NEW_ANCHOR)
        if original.count(current_function) != 1:
            raise RuntimeError("R53 source has a nonunique function")
        updated = original.replace(current_function, replacement, 1)
    elif NEW_ANCHOR in current_function and OLD_ANCHOR not in current_function:
        updated = original
    else:
        raise RuntimeError("Unreviewed public search hook shape")
    # The ZIP carries the entire expected replacement, not an abbreviated diff.
    expected = (PACKAGE / "CHANGED_FUNCTIONS_FULL.py").read_text(encoding="utf-8")
    observed = function_source(updated, "search_group_from_registered_goal")
    if ast.dump(ast.parse(observed), include_attributes=False) != ast.dump(
        ast.parse(expected), include_attributes=False
    ):
        raise RuntimeError("R53 complete function differs from the reviewed replacement")
    if updated.count("build_public_source_bound_kernel_provider(provider, screened)") != 1:
        raise RuntimeError("R53 wrapper was not inserted exactly once")
    return updated


def prepare() -> tuple[bytes, str, str]:
    """Check the exact committed file and one safe idempotent replacement."""
    baseline = git_bytes("show", "HEAD:" + TARGET)
    old = normalized(baseline).decode("utf-8-sig")
    updated = patched_source(old)
    working_bytes = (ROOT / TARGET).read_bytes()
    working = normalized(working_bytes).decode("utf-8-sig")
    if working not in (old, updated):
        raise RuntimeError("Unreviewed public group search working source")
    return working_bytes, old, updated


def apply(*, dry_run: bool) -> dict[str, object]:
    """Preserve Windows EOL when replacing the complete reviewed function."""
    state = verify_checkout()
    current, old, updated = prepare()
    mode = "ALREADY_INSTALLED" if normalized(current).decode("utf-8-sig") == updated else "INSTALL"
    if not dry_run and mode == "INSTALL":
        line_ending = b"\r\n" if b"\r\n" in current else b"\n"
        replacement = updated.encode("utf-8").replace(b"\n", line_ending)
        (ROOT / TARGET).write_bytes(replacement)
        if normalized((ROOT / TARGET).read_bytes()).decode("utf-8-sig") != updated:
            raise RuntimeError("R53 public function replacement was not applied")
    return {
        **state,
        "target": TARGET,
        "install_mode": mode,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "changed_production_files": 0 if dry_run else 1,
        "full_pytest": False,
        "gate": (
            "PASS_R53_GENERIC_PROVIDER_PREFLIGHT" if dry_run else
            "PASS_R53_GENERIC_PROVIDER_WIRING_INSTALLED"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    details = apply(dry_run=args.dry_run)
    prefix = "PHASE174_R3R7R53_"
    for name, value in details.items():
        print(prefix + name.upper() + "=" + str(value))
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## audit.py

```python
"""R53: verify the real public zero-group search and shared verified Web route.

No precomputed R50 or R52 proof is injected. Only the production public entry
is called; the common proof engine checks every sourced candidate normally.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
import os
from pathlib import Path
import tempfile

from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import verify_checkout


def inspect_public_root_completion() -> dict[str, object]:
    """Compare real public search and source-verified model-backed Web view."""
    from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase165_r3_recursive_search import SourceBoundGoal
    from phase165_r52_partial_proof import ProofSearchStatus
    from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
    from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
    from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
    from phase174_r3_r7_r53_public_source_bound_kernel.provider import build_public_source_bound_kernel_provider
    from proof import ProofRule, ProofStep
    from web_group_proof import build_standard_web_group_proof_view

    n, k = 7, 5
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(n + k, n))
    bridge = build_shared_typed_bridge()
    contexts = []
    public = search_group_from_registered_goal(n=n, k=k, bridge=bridge,
                                               context_sink=contexts.append)
    if len(contexts) != 1:
        raise RuntimeError("R53 could not observe the exact screened context")
    screened = contexts[0]
    provider = shared_expansion_provider(screened, proof_target=goal)
    wrapped = build_public_source_bound_kernel_provider(provider, screened)
    root_inputs = ehp_zero_inputs(goal)
    if root_inputs is None:
        raise RuntimeError("EHP zero root changed")
    upper_inputs = upper_delta_surjectivity_inputs(root_inputs[0])
    if upper_inputs is None:
        raise RuntimeError("Upper Delta exactness contract changed")
    kernel_goal = upper_inputs[2]
    if not isinstance(kernel_goal, KernelMultipleStatement):
        raise RuntimeError("R53 missing typed lower Delta kernel")
    original = tuple(item for item in provider(kernel_goal)
                     if item.rule.name == KERNEL_RULE)
    offered = tuple(item for item in wrapped(kernel_goal)
                    if item.rule.name == KERNEL_RULE)
    bound = tuple(item for item in offered
                  if any(type(sub) is SourceBoundGoal for sub in item.subgoals))
    if not original or not bound:
        raise RuntimeError("R53 missing checked source-bound kernel option")

    proof_root = tuple(step for step in public.proven_steps
                       if step.conclusion == goal and step.rule is ProofRule.INFERENCE)
    kernel_steps = tuple(step for step in public.proven_steps
                         if step.conclusion == kernel_goal and step.rule is ProofRule.INFERENCE)
    four = any(len(step.premises) == 4
               and tuple(parent.conclusion for parent in step.premises) == root_inputs
               and all(parent.rule is ProofRule.INFERENCE for parent in step.premises)
               for step in proof_root)
    three = any(len(step.premises) == 3
                and step.premises[0].rule is ProofRule.INFERENCE
                and step.premises[1].rule is ProofRule.GIVEN
                and step.premises[2].rule is ProofRule.GIVEN
                for step in kernel_steps)

    def cited_ancestors(step: ProofStep) -> set[str]:
        found: set[str] = set()
        seen: set[int] = set()
        def walk(node: ProofStep) -> None:
            if id(node) in seen:
                return
            seen.add(id(node))
            if node.rule is ProofRule.GIVEN:
                reference = getattr(getattr(node.inference_rule, "literature_reference", None),
                                    "locator", None)
                if isinstance(reference, str):
                    found.add(reference)
            for ancestor in node.premises:
                walk(ancestor)
        walk(step)
        return found

    required = {
        "(5.9)", "Proposition 4.2 (4.4)",
        "Proposition 5.8", "(5.10)",
        "Proposition 2.7", "(5.1)",
    }
    provenance = any(required.issubset(cited_ancestors(step)) for step in proof_root)
    web = build_standard_web_group_proof_view(
        n=n, k=k, max_depth=2, mode="narrative", citation_source="model",
    )
    complete = (public.status is ProofSearchStatus.COMPLETE
                and public.conclusion == goal and not public.open_goals)
    web_complete = web.key == "generic-complete-proof" and web.partial_result is False
    if (web_complete != complete or (complete and (not four or not three or not provenance))):
        raise RuntimeError("R53 public model or citation proof trust contract failed")
    return {
        "root": "pi_12^7 = 0",
        "public_status": public.status.value,
        "public_verified_steps": len(public.proven_steps),
        "public_open_goal_types": dict(sorted(Counter(type(x).__name__ for x in public.open_goals).items())),
        "public_diagnostics": list(public.diagnostics),
        "public_root_inference_count": len(proof_root),
        "public_kernel_inference_count": len(kernel_steps),
        "public_kernel_domain_cited_inference": three,
        "public_root_four_inferred_parents": four,
        "public_root_six_cited_ancestors": provenance,
        "public_r35_original_candidates": len(original),
        "public_r35_source_bound_candidates": len(bound),
        "public_web_key": web.key,
        "public_web_partial_result": web.partial_result,
        "public_web_rendered_lines": len(web.rendered_lines),
        "public_web_model_route_checked": True,
        "public_http_checked": False,
        "public_root_complete": complete,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "full_pytest": False,
        "gate": (
            "PASS_R53_GENERIC_PUBLIC_ROOT_COMPLETE_HTTP_PENDING"
            if complete and web_complete else
            "PASS_R53_PUBLIC_ROOT_STILL_UNRESOLVED"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_checkout()
    observations = None if args.dry_run else inspect_public_root_completion()
    gate = ("PASS_R53_SOURCE_PREFLIGHT" if args.dry_run else observations["gate"])
    report = {
        "phase": "174-R3-R7-R53",
        "state": state,
        "observations": observations,
        "gate": gate,
    }
    directory = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir())) / (
        "EHPProofTracerAudit/phase174_r3_r7_r53"
    )
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / ("preflight.json" if args.dry_run else "public_source_bound_root.json")
    destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    prefix = "PHASE174_R3R7R53_"
    for name, value in state.items():
        print(prefix + name.upper() + "=" + str(value))
    if observations is not None:
        for name, value in observations.items():
            print(prefix + name.upper() + "=" + str(value))
    print(prefix + "REPORT=" + str(destination))
    print(prefix + "GATE=" + gate)
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## tests/test_static.py

```python
"""R53 prevents accidental scope creep in the public zero-branch wiring."""
from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]


def test_all_r53_python_files_parse_without_ellipsis() -> None:
    for file in ("provider.py", "source_guard.py", "install.py", "audit.py",
                 "CHANGED_FUNCTIONS_FULL.py", "tests/test_static.py",
                 "tests/test_guard.py", "tests/test_public.py"):
        tree = ast.parse((PACKAGE / file).read_text(encoding="utf-8"), feature_version=(3, 10))
        assert not any(isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant)
                       and node.value.value is Ellipsis for node in ast.walk(tree))


def test_only_zero_public_branch_receives_generic_source_bound_provider() -> None:
    tree = ast.parse((PACKAGE / "CHANGED_FUNCTIONS_FULL.py").read_text(encoding="utf-8"))
    functions = tuple(x for x in tree.body if isinstance(x, ast.FunctionDef))
    assert len(functions) == 1
    assert functions[0].name == "search_group_from_registered_goal"
    text = (PACKAGE / "CHANGED_FUNCTIONS_FULL.py").read_text(encoding="utf-8")
    assert text.count("build_public_source_bound_kernel_provider(provider, screened)") == 1
    assert "if isinstance(candidate, TodaPrimaryGroupZeroStatement):" in text
    assert "return search_registered_partial_proof(" in text
    assert "if proof_order_catalog is None:" in text
    assert "def registered_group_goal_candidates(" not in text


def test_provider_only_reuses_a_reviewed_general_mathematical_rule() -> None:
    text = (PACKAGE / "provider.py").read_text(encoding="utf-8")
    assert "find_inference_matches_for_rule" in text
    assert "SourceBoundGoal(conclusion=domain, source=source)" in text
    assert "return tuple(bound) + original" in text
    assert "ProofStep(" not in text
    assert "n == 7" not in text and "k == 5" not in text
    script = (PACKAGE / "run.ps1").read_text(encoding="utf-8")
    assert "param([switch]$DryRun)" in script and "--dry-run" in script
    assert "FULL_PYTEST=False" in script
    assert "--import-mode=importlib" in script
    assert "git reset" not in script and "git clean" not in script
```

## tests/test_guard.py

```python
"""R53 source guard and idempotent whole-function patch contracts."""
from __future__ import annotations

import ast

from phase174_r3_r7_r53_public_source_bound_kernel.install import (
    NEW_ANCHOR, OLD_ANCHOR, function_source, patched_source, prepare,
)
from phase174_r3_r7_r53_public_source_bound_kernel.source_guard import (
    REVIEWED_BLOBS, REVIEWED_HEAD, TARGET, TARGET_BLOB,
    verify_checkout,
)


def test_current_checked_develop_matches_reviewed_production_contract() -> None:
    state = verify_checkout()
    assert state["source_guard"] == "PASS"
    assert state["local_head"] == REVIEWED_HEAD
    assert state["remote_head"] == REVIEWED_HEAD
    assert state["reviewed_blob_count"] == len(REVIEWED_BLOBS) + 1
    assert len(TARGET_BLOB) == 40
    assert TARGET == "phase165_r55_nk_only_goal.py"


def test_replacement_is_idempotent_and_complete() -> None:
    working, old, updated = prepare()
    assert OLD_ANCHOR in old and NEW_ANCHOR not in old
    assert NEW_ANCHOR in updated and OLD_ANCHOR not in updated
    assert patched_source(old) == updated
    assert patched_source(updated) == updated
    actual = function_source(updated, "search_group_from_registered_goal")
    ast.parse(actual, feature_version=(3, 10))
    assert actual.count("build_public_source_bound_kernel_provider(provider, screened)") == 1
```

## tests/test_public.py

```python
"""R53 source-first generic kernel binding and real public Group query."""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r2_quotient_rules import KernelMultipleStatement
from phase165_r3_recursive_search import SourceBoundGoal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e2_unpositioned_citation.source_first import screen_independent_sources_for_derived_goal
from phase174_r3_r7_r3_ehp_zero_rule.rule import ehp_zero_inputs
from phase174_r3_r7_r37_upper_delta_surjectivity_isolated.rule import upper_delta_surjectivity_inputs
from phase174_r3_r7_r35_isolated_cyclic_delta_kernel.rule import RULE_NAME as KERNEL_RULE
from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
    build_public_source_bound_kernel_provider,
)
from phase174_r3_r7_r53_public_source_bound_kernel.audit import inspect_public_root_completion
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


def test_cited_generic_kernel_prefers_source_bound_but_retains_fallback() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    base = shared_expansion_provider(screened, proof_target=root)
    improved = build_public_source_bound_kernel_provider(base, screened)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    before = tuple(x for x in base(kernel) if x.rule.name == KERNEL_RULE)
    after = tuple(x for x in improved(kernel) if x.rule.name == KERNEL_RULE)
    assert len(before) == 1
    assert len(after) >= 2
    assert isinstance(after[0].subgoals[0], SourceBoundGoal)
    assert after[0].subgoals[0].conclusion == before[0].subgoals[0]
    assert after[-1].subgoals == before[0].subgoals
    assert improved(root)[0].subgoals == base(root)[0].subgoals


def test_missing_independent_cited_step_never_adds_bound_candidate() -> None:
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    screened = screen_independent_sources_for_derived_goal(build_shared_typed_bridge(), goal=root)
    base = shared_expansion_provider(screened, proof_target=root)
    empty = RegistryBridgeResult(screened.registry, screened.records, ())
    improved = build_public_source_bound_kernel_provider(base, empty)
    kernel = upper_delta_surjectivity_inputs(ehp_zero_inputs(root)[0])[2]
    before = tuple(x for x in base(kernel) if x.rule.name == KERNEL_RULE)
    after = tuple(x for x in improved(kernel) if x.rule.name == KERNEL_RULE)
    assert len(after) == len(before) == 1
    assert all(not isinstance(x.subgoals[0], SourceBoundGoal) for x in after)


def test_actual_public_zero_goal_is_completed_by_verified_proof_steps() -> None:
    result = search_group_from_registered_goal(n=7, k=5)
    goal = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(12, 7))
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == goal
    assert result.open_goals == ()
    roots = tuple(x for x in result.proven_steps
                  if x.rule is ProofRule.INFERENCE and x.conclusion == goal)
    assert len(roots) == 1
    assert len(roots[0].premises) == 4
    assert all(x.rule is ProofRule.INFERENCE for x in roots[0].premises)


def test_public_web_model_uses_common_verified_renderer() -> None:
    view = build_standard_web_group_proof_view(
        n=7, k=5, max_depth=2, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert view.partial_result is False
    assert view.rendered_lines
    assert view.n == 7 and view.k == 5


def test_public_audit_rechecks_citations_in_one_real_tree() -> None:
    report = inspect_public_root_completion()
    assert report["public_root_complete"] is True
    assert report["public_kernel_domain_cited_inference"] is True
    assert report["public_root_four_inferred_parents"] is True
    assert report["public_root_six_cited_ancestors"] is True
    assert report["public_web_key"] == "generic-complete-proof"
    assert report["public_http_checked"] is False
    assert report["new_given"] == 0
    assert report["new_mathematical_rules"] == 0
```

## run.ps1

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R53 source guard or planned patch failed' }
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.audit --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R53 audited context preflight failed' }
    if ($DryRun) {
        Write-Output 'PHASE174_R3R7R53_RUN=DRYRUN_PASS'
        Write-Output '(END)'
        exit 0
    }
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.install
    if ($LASTEXITCODE -ne 0) { throw 'R53 guarded public provider integration failed' }
    python -B -m phase174_r3_r7_r53_public_source_bound_kernel.audit
    if ($LASTEXITCODE -ne 0) { throw 'R53 actual public and Web-model proof audit failed' }
    $Groups = @(
        @{Name='R53_STATIC'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_static.py'},
        @{Name='R53_GUARD'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_guard.py'},
        @{Name='R53_PUBLIC'; Path='phase174_r3_r7_r53_public_source_bound_kernel/tests/test_public.py'},
        @{Name='R52_PROBE_REGRESSION'; Path='phase174_r3_r7_r52_public_kernel_source_bound_probe/tests/test_probe.py'},
        @{Name='R51_PUBLIC_REGRESSION'; Path='phase174_r3_r7_r51_public_route_gap_audit/tests/test_public.py'},
        @{Name='R50_SCOPED_PROOF_REGRESSION'; Path='phase174_r3_r7_r50_root_exactness_terminal_zero_frontier/tests/test_frontier.py'},
        @{Name='R36_CITED_KERNEL_REGRESSION'; Path='phase174_r3_r7_r36_cited_kernel_provider_wiring/tests/test_public.py'},
        @{Name='R35_KERNEL_MATH_REGRESSION'; Path='phase174_r3_r7_r35_isolated_cyclic_delta_kernel/tests/test_rule.py'}
    )
    foreach ($Group in $Groups) {
        Write-Output ('PHASE174_R3R7R53_TEST_GROUP=' + $Group.Name)
        python -B -m pytest -q --import-mode=importlib -p no:cacheprovider $Group.Path
        if ($LASTEXITCODE -ne 0) {
            throw ('R53 focused pytest failed: ' + $Group.Name)
        }
    }
    Write-Output 'PHASE174_R3R7R53_RUN=PASS'
    Write-Output 'PHASE174_R3R7R53_FULL_PYTEST=False'
    Write-Output '(END)'
} finally {
    Pop-Location
}
```
