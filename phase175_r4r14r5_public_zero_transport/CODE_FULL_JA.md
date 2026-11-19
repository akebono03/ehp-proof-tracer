# Phase 175 R4R14R5 コード全文

## `provider.py`

```python
"""Public backward proposals for proved composite-image-zero transport.

Only the cited general law that passed the existing R41 screening may select
an unproved composition-zero obligation. No root-group fact or proof leaf is
created by this provider; the shared DFS must prove both parent goals.
"""
from __future__ import annotations

from typing import Callable

from expression import Composition, Zero
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r3_recursive_search import GoalExpansion
from phase174_r3_r7_r12_toda59_annihilator_source.rule import (
    canonical_annihilator_instance,
)
from phase174_r3_r7_r38_source_bound_zero_image_public_wiring.provider import (
    lifted_stable_composition,
    valid_suspension,
)
from phase174_r3_r7_r41_adopted_db_zero_image_public_wiring.provider import (
    screened_general_law,
)
from phase175_r4r14r4_general_zero_transport.rule import (
    expand_proved_composite_zero_image,
)
from proof import Relation, RelationType

PROVIDER_ID = "phase175.r4r14r5.cited_composite_zero_transport"


def build_public_composite_zero_transport_provider(
    bridge: RegistryBridgeResult,
) -> Callable[[object], tuple[GoalExpansion, ...]]:
    """Offer the generic two-premise rule only for a screened cited zero law.

    This works for any typed stable composite whose *entire* lifted value
    matches a cited annihilator. Longer composites can also use this rule
    after independently proved reassociation; no factor-count restriction
    is introduced here.
    """
    laws = screened_general_law(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        if (len(laws) != 1
                or not isinstance(goal, GeneratorImage)
                or not valid_suspension(goal.map)
                or not isinstance(goal.target_generator, Zero)):
            return ()
        lifted = lifted_stable_composition(goal.source_generator)
        if not isinstance(lifted, Composition):
            return ()
        mapping = goal.map
        from phase169_r10eq_r1_universal_stable_definition.definition import (
            typed_element_span,
        )
        if typed_element_span(goal.source_generator) != (
            mapping.source_group.group_dimension,
            mapping.source_group.sphere_dimension,
        ):
            return ()
        if typed_element_span(lifted) != (
            mapping.target_group.group_dimension,
            mapping.target_group.sphere_dimension,
        ):
            return ()
        from phase174_r3_r7_r9_composition_associativity.rule import (
            typed_composition_factors,
        )
        factors = typed_composition_factors(lifted)
        if not factors:
            return ()
        cited_relation = canonical_annihilator_instance(laws[0], factors[0].dimension)
        if cited_relation != Relation(lifted, Zero(), RelationType.EQUALITY):
            return ()
        image = GeneratorImage(mapping, goal.source_generator, lifted)
        return expand_proved_composite_zero_image(goal, image)

    return expand

```

## `installer.py`

```python
"""Guarded minimal insertion of the shared provider; no full-file rewrites."""
from __future__ import annotations

import argparse
import ast
import subprocess
from pathlib import Path

TARGET = "phase165_r52_r9_shared_math.py"
EXPECTED_BLOB = "f5329594a8298af34cd05932bf4a7b6c59d6e4de"
ANCHOR = "    # R41: retain DB-prior provenance and the actual cited source boundary."
INSERTION = (
    "    # Phase 175 R4R14R5: source-screened composite-value zero transport.\n"
    "    # Each premise is still proved by the shared source-first DFS.\n"
    "    from phase175_r4r14r5_public_zero_transport.provider import (\n"
    "        build_public_composite_zero_transport_provider,\n"
    "    )\n"
    "    extra_providers = (\n"
    "        build_public_composite_zero_transport_provider(bridge),\n"
    "    ) + tuple(extra_providers)\n"
)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ("git", *args), cwd=root, text=True, encoding="utf-8",
        capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("GIT_FAILED " + " ".join(args) + " " + result.stderr.strip())
    return result.stdout.strip()


def expected_updated_source(data: str) -> str:
    if data.count(ANCHOR) != 1 or INSERTION in data:
        raise RuntimeError("SHARED_PROVIDER_ANCHOR_CHANGED")
    updated = data.replace(ANCHOR, INSERTION + ANCHOR)
    tree = ast.parse(updated)
    fun = [node for node in tree.body
           if isinstance(node, ast.FunctionDef)
           and node.name == "shared_expansion_provider"]
    if len(fun) != 1:
        raise RuntimeError("SHARED_PROVIDER_FUNCTION_CHANGED")
    return updated


def verify_and_apply(root: Path, *, dry_run: bool) -> str:
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("REPOSITORY_ROOT_REQUIRED")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("DEVELOP_BRANCH_REQUIRED")
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("STAGED_CHANGES_REQUIRE_REVIEW")
    if git(root, "rev-parse", "HEAD:" + TARGET) != EXPECTED_BLOB:
        raise RuntimeError("HEAD_SOURCE_BLOB_CHANGED")
    source = root / TARGET
    original = subprocess.run(
        ("git", "show", "HEAD:" + TARGET), cwd=root,
        capture_output=True, check=True,
    ).stdout.decode("utf-8")
    canonical = expected_updated_source(original)
    contents = source.read_bytes()
    if b"\r\n" in contents and b"\n" in contents.replace(b"\r\n", b""):
        raise RuntimeError("MIXED_EOL_REJECTED")
    newline = "\r\n" if b"\r\n" in contents else "\n"
    current = contents.decode("utf-8").replace("\r\n", "\n")
    if current not in (original.replace("\r\n", "\n"), canonical.replace("\r\n", "\n")):
        raise RuntimeError("UNEXPECTED_WORKTREE_SOURCE")
    baseline = original.replace("\r\n", "\n")
    modified = canonical.replace("\r\n", "\n")
    if current == baseline:
        status = "PATCH_REQUIRED"
        if not dry_run:
            source.write_bytes(modified.replace("\n", newline).encode("utf-8"))
    else:
        status = "ALREADY_APPLIED"
    # Provide the complete modified function for immediate inspection.
    tree = ast.parse(modified)
    fun = next(node for node in tree.body if isinstance(node, ast.FunctionDef)
               and node.name == "shared_expansion_provider")
    body = "\n".join(modified.splitlines()[fun.lineno - 1:fun.end_lineno])
    out = root / "phase175_r4r14r5_public_zero_transport" / "SHARED_PROVIDER_FULL_JA.md"
    if not dry_run:
        out.write_text(
            "# 変更後の共有関数全文\n\n"
            "変更対象：`phase165_r52_r9_shared_math.py` / "
            "`shared_expansion_provider`。\n\n```python\n"
            + body + "\n```\n", encoding="utf-8",
        )
    return status


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    state = verify_and_apply(args.root, dry_run=args.dry_run)
    print("PHASE175_R4R14R5_PATCH_STATUS=" + state)
    print("PHASE175_R4R14R5_GATE=" + (
        "PASS_DRYRUN_SOURCE_GUARD" if args.dry_run
        else "PASS_GUARDED_SHARED_PROVIDER_WIRING"
    ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```

## `tests/test_provider.py`

```python
"""Focused Phase 175 R4R14R5 public source and generic-proof contracts."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaPrimaryGroupZeroStatement, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase169_r10e2_unpositioned_citation.source_first import (
    screen_independent_sources_for_derived_goal,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase175_r4r14r4_general_zero_transport.rule import (
    RULE_NAME, composite_value_zero_inputs,
)
from phase175_r4r14r5_public_zero_transport.provider import (
    build_public_composite_zero_transport_provider,
)


def _inputs():
    root = TodaPrimaryGroupZeroStatement(TodaPrimaryGroup(10, 6))
    screened = screen_independent_sources_for_derived_goal(
        build_shared_typed_bridge(), goal=root,
    )
    previous = exact_prior_database_result(5, 4)
    assert previous is not None
    mapping = TodaSuspensionMap(
        TodaPrimaryGroup(9, 5), TodaPrimaryGroup(10, 6),
    )
    goal = GeneratorImage(mapping, previous.rhs.generator, Zero())
    return root, screened, goal


def test_source_screened_binary_composition_generates_two_real_goals():
    _, screened, goal = _inputs()
    options = build_public_composite_zero_transport_provider(screened)(goal)
    assert len(options) == 1
    assert options[0].rule.name == RULE_NAME
    parents = options[0].subgoals
    assert composite_value_zero_inputs(goal, parents[0]) == parents
    assert parents[0].source_generator == goal.source_generator
    assert parents[0].map == goal.map
    assert parents[1].rhs == Zero()
    assert options[0].rule.literature_reference is None


def test_shared_provider_offers_same_generic_rule():
    root, screened, goal = _inputs()
    options = shared_expansion_provider(screened, proof_target=root)(goal)
    matching = tuple(candidate for candidate in options if candidate.rule.name == RULE_NAME)
    assert len(matching) == 1
    assert matching[0].subgoals == build_public_composite_zero_transport_provider(screened)(goal)[0].subgoals


def test_no_cited_source_no_zero_proposal():
    _, screened, goal = _inputs()
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    empty = RegistryBridgeResult(registry=UnifiedStatementRegistry(), records=(), proof_links=())
    assert build_public_composite_zero_transport_provider(empty)(goal) == ()
    assert build_public_composite_zero_transport_provider(screened)(
        replace(goal, target_generator=goal.source_generator)
    ) == ()


def test_unproved_parents_cannot_close_any_step():
    _, screened, goal = _inputs()
    option = build_public_composite_zero_transport_provider(screened)(goal)[0]
    from proof import find_inference_matches_for_rule
    assert find_inference_matches_for_rule(option.rule, ()) == ()

```

## `tests/test_installer.py`

```python
"""Installer accepts one exact anchor, rejects ambiguous rewrites."""
from __future__ import annotations

import ast

import pytest

from phase175_r4r14r5_public_zero_transport.installer import (
    ANCHOR, INSERTION, expected_updated_source,
)


def test_guarded_insert_is_local_and_parseable():
    source = (
        "def shared_expansion_provider(bridge):\n"
        "    extra_providers = ()\n"
        + ANCHOR + "\n"
        "    return extra_providers\n"
    )
    revised = expected_updated_source(source)
    ast.parse(revised)
    assert revised.count(INSERTION) == 1
    assert revised.count(ANCHOR) == 1
    assert "return extra_providers" in revised


def test_repeated_or_ambiguous_insert_fails():
    source = (
        "def shared_expansion_provider(bridge):\n"
        "    extra_providers = ()\n" + ANCHOR + "\n"
        "    return extra_providers\n"
    )
    with pytest.raises(RuntimeError, match="ANCHOR_CHANGED"):
        expected_updated_source(expected_updated_source(source))
    with pytest.raises(RuntimeError, match="ANCHOR_CHANGED"):
        expected_updated_source(source.replace(ANCHOR, ""))

```

## `audit.py`

```python
"""Observe the real public search after the shared zero transport was connected."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus


def inspect_public_target() -> dict[str, object]:
    """Return the actual search state, never manufacture a completed proof."""
    contexts: list[object] = []
    result = search_group_from_registered_goal(n=6, k=4, context_sink=contexts.append)
    state = getattr(result.status, "value", str(result.status))
    complete = result.status is ProofSearchStatus.COMPLETE
    return {
        "target": "pi_10^6",
        "status": state,
        "complete": complete,
        "conclusion": str(result.conclusion) if result.conclusion is not None else None,
        "open_goals": [str(item) for item in result.open_goals],
        "proven_steps": len(result.proven_steps),
        "references": len(result.references),
        "new_given": 0,
        "full_pytest": False,
    }


def main() -> int:
    inspected = inspect_public_target()
    dest = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "EHP_Phase175_R4R14R5_public_search.json"
    dest.write_text(json.dumps(inspected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE175_R4R14R5_SEARCH_STATUS=" + str(inspected["status"]))
    print("PHASE175_R4R14R5_OPEN_GOALS=" + str(len(inspected["open_goals"])))
    print("PHASE175_R4R14R5_PROVEN_STEPS=" + str(inspected["proven_steps"]))
    print("PHASE175_R4R14R5_REPORT=" + str(dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

```
