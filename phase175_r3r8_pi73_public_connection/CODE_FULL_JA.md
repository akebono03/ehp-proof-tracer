# Phase 175 R3R8 — 変更コード全文

## 変更対象（最初に列挙）

- 既存ファイル `phase165_r52_r9_shared_math.py`：`search_shared_group_goal()` のみ。
- 新規 `phase175_r3r8_pi73_public_connection/route.py`：`public_cited_ehp_extensions()`、`prepare_pi73_public_connection()`。
- 新規 `install.py`、`audit.py`、`run.ps1`、`__init__.py`、`tests/test_install.py`、`tests/test_route.py`、`tests/__init__.py`。
- 既存クラス・関数・テストへの他の変更はなし。既存ファイルのトップレベル import は変更なし。
- 新規関数の追加位置：それぞれ新規ファイルの import 群の直後。既存関数の全文置換は `search_shared_group_goal_FULL.py.txt` と同一。

## 既存ファイル import（変更なし）

当該ファイルの import は一切変更しません。既存関数内のローカル import だけ追加します。

## 既存関数 `search_shared_group_goal()` — 変更後全文

```python
def search_shared_group_goal(*, n: int, k: int, group_structure: object,
                              bridge: RegistryBridgeResult | None = None,
                              expansion_provider=None,
                              citing_assertion_id: str | None = None,
                              verified_assertion_ids: tuple[str, ...] = (), completed_internal_proofs: tuple = (), proof_use_order=None,
                              ordered_completed_proofs: tuple = (), target_order: int | None = None,
                              proof_order_catalog=None, recursive_proof_order_catalog=None, context_sink=None):
    """Run canonical search under a screened Reference context.

    Older calls retain their signature. R15 ordering is applied to sources
    outside the explicitly adopted-Tex policy; no IDs are auto-verified.
    """
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r57_r12_ordered_proofs import validate_prior_internal_proofs

    goal = Relation(TodaPrimaryGroup(n + k, n), group_structure)
    if proof_order_catalog is not None and recursive_proof_order_catalog is None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot mix with caller-supplied proofs")
        if any(record.completed is not None for record in proof_order_catalog._records):
            raise ValueError("on-demand mode forbids registered completed proofs")
        recursive_proof_order_catalog = proof_order_catalog
        proof_order_catalog = None
    if recursive_proof_order_catalog is not None:
        from phase165_r57_r14_recursive_search import search_recursively_in_proof_order
        if (proof_order_catalog is not None or ordered_completed_proofs
                or completed_internal_proofs or target_order is not None):
            raise ValueError("recursive proof order cannot mix with saved or caller-supplied proofs")

        def search_one(statement, earlier, order):
            if (not isinstance(statement, Relation)
                    or not isinstance(statement.lhs, TodaPrimaryGroup)
                    or statement.relation_type is not RelationType.EQUALITY):
                raise TypeError("recursive catalog targets must be typed group relations")
            target = statement.lhs
            if (not isinstance(target.group_dimension, int)
                    or not isinstance(target.sphere_dimension, int)
                    or target.sphere_dimension < 2
                    or target.group_dimension < target.sphere_dimension):
                raise ValueError("recursive target must have concrete dimensions")
            return search_shared_group_goal(
                n=target.sphere_dimension,
                k=target.group_dimension - target.sphere_dimension,
                group_structure=statement.rhs,
                bridge=bridge,
                expansion_provider=expansion_provider,
                citing_assertion_id=citing_assertion_id,
                verified_assertion_ids=verified_assertion_ids,
                completed_internal_proofs=(),
                proof_use_order=proof_use_order,
                ordered_completed_proofs=earlier,
                target_order=order,
                context_sink=context_sink if statement == goal else None,
            )

        return search_recursively_in_proof_order(
            recursive_proof_order_catalog, goal, search_one,
        )
    if proof_order_catalog is not None:
        from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog
        if not isinstance(proof_order_catalog, ProofOrderCatalog):
            raise TypeError("proof_order_catalog must be ProofOrderCatalog")
        if ordered_completed_proofs or completed_internal_proofs or target_order is not None:
            raise ValueError("catalog proof order cannot be mixed with caller order")
        prior, target_order = proof_order_catalog.select_prior(goal)
    else:
        prior = validate_prior_internal_proofs(
            ordered_completed_proofs, target_order, completed_internal_proofs
        )
    if bridge is None:
        bridge = build_shared_typed_bridge()
    if n == 4 and k == 3 and expansion_provider is None:
        from phase173_r4_r1_public_connection.route import (
            prepare_pi74_public_connection,
        )
        pi74_connection = prepare_pi74_public_connection(
            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi74_connection is not None:
            bridge, citing_assertion_id, expansion_provider = pi74_connection
    # R3R8: connect the R3R7 cited general EHP proof chain, not a saved result.
    if n == 3 and k == 4 and expansion_provider is None:
        from phase175_r3r8_pi73_public_connection.route import (
            prepare_pi73_public_connection,
        )
        pi73_connection = prepare_pi73_public_connection(
            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi73_connection is not None:
            bridge, citing_assertion_id, expansion_provider = pi73_connection
    if citing_assertion_id is not None and expansion_provider is None:
        from phase174_r3_r6_r2_prop44_lemma54.source import (
            attach_earlier_verified_lemma54,
        )
        bridge = attach_earlier_verified_lemma54(bridge, citing_assertion_id)
    assertions = tuple(bridge.registry._assertions.values())
    if not assertions:
        raise ValueError("shared typed registry is empty")
    context_id = citing_assertion_id or assertions[0].assertion_id
    if citing_assertion_id is None:
        from phase169_r10e2_unpositioned_citation.source_first import (
            screen_independent_sources_for_derived_goal,
        )
        proof_context = screen_independent_sources_for_derived_goal(
            bridge, goal=goal,
        )
    else:
        proof_context = screen_shared_proof_context(
            bridge, goal=goal, citing_assertion_id=context_id,
            verified_assertion_ids=verified_assertion_ids,
            explicit_publication_target=True,
        )
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    proof_context = prefer_universal_prop42_derivation(proof_context)
    # Phase 173 R4-R8: reuse only the three isolated, source-verified Toda (5.6) roots.
    if n == 4 and k in (4, 5, 6) and expansion_provider is None and citing_assertion_id is None:
        from phase173_r4_r8_public_connection.route import (
            prepare_pi4_higher_public_connection,
        )
        pi4_higher_connection = prepare_pi4_higher_public_connection(
            bridge=bridge, goal=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        if pi4_higher_connection is not None:
            proof_context, expansion_provider = pi4_higher_connection
    if context_sink is not None:
        context_sink(proof_context)
    if expansion_provider is None:
        expansion_provider = shared_expansion_provider(
            proof_context, proof_target=goal,
            prior_conclusions=tuple(item.root.conclusion for item in prior),
        )
        # Every ordinary (nonzero) group search needs the same cited R53
        # source-bound kernel candidate already used by the zero-group route.
        # This is a candidate ordering wrapper, not a new premise or GIVEN.
        from phase174_r3_r7_r53_public_source_bound_kernel.provider import (
            build_public_source_bound_kernel_provider,
        )
        expansion_provider = build_public_source_bound_kernel_provider(
            expansion_provider, proof_context,
        )
    return search_registered_partial_proof(
        n=n, k=k, goal=goal, bridge=proof_context,
        citing_assertion_id=context_id,
        expansion_provider=expansion_provider,
        lookup_mode="typed_reference_publication" if citing_assertion_id is not None else "typed_reference",
        structure_status=GroupStructureStatus.UNKNOWN,
        completed_internal_proofs=prior,
    )
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/__init__.py` — 全文

```python
"""Phase 175 R3R8: publish source-first EHP inference without a special proof."""
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/route.py` — 全文

```python
"""Attach the R3R7 source-backed general rules to ordinary Group query search.

Only the already registered (3,4) group selects this route. The inference
rules themselves are reusable, and all six premises remain independent
backward goals. No target conclusion or saved ProofStep is imported.
"""
from __future__ import annotations

from pathlib import Path

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    TodaLemma54TypedSource,
)
from phase174_r3_r6_r2_prop44_lemma54.source import attach_earlier_verified_lemma54
from phase174_r3_r7_r5_zero_image_hopf_injective.rule import (
    expand_hopf_injective_from_zero_image,
    hopf_injectivity_from_zero_image_inputs,
)
from phase174_r3_r7_r6_cyclic_generator_zero_image.rule import (
    expand_zero_image_from_cyclic_generator,
)
from phase175_r3_pi73_hopf_lift.rule import expand_cited_hopf_lift
from phase175_r3r6_lemma57_general.rule import (
    expand_cited_lemma57_zero_generator,
    lemma57_criterion_inputs,
)
from phase175_r3r6_lemma57_general.source import (
    GENERAL_ASSERTION_ID,
    TodaLemma57GeneralCriterion,
    build_isolated_lemma57_source,
    merge_isolated_cited_source,
)
from phase175_r3r7_lemma54_membership.rule import (
    cited_lemma54_double_relation,
    expand_cited_lemma54_double,
    expand_even_factor_membership,
)
from phase175_r3r7_lemma54_membership.source import verify_lemma54_before_lemma57
from proof import ProofRule, Relation, RelationType
from unified_statement_registry import AssertionOrigin


def public_cited_ehp_extensions(available: tuple[object, ...]):
    """Return reusable proposals using only the screened source conclusions.

    This closure does not carry a completed proof. Existing R3R7 algebraic
    inference rules are called unmodified. A lower group is only a candidate
    goal; the canonical resolver independently establishes its provenance.
    """
    if (available.count(TodaLemma54TypedSource()) != 1
            or available.count(TodaLemma57GeneralCriterion()) != 1):
        raise ValueError("R3R8 requires exactly one screened Lemma 5.4 and 5.7")
    equation = cited_lemma54_double_relation()

    def expand(statement: object):
        options = []
        options.extend(expand_cited_lemma54_double(statement, available))
        options.extend(expand_even_factor_membership(statement, (equation,)))
        options.extend(expand_cited_lemma57_zero_generator(statement, available))
        if isinstance(statement, ImageZeroStatement):
            suspension = statement.map
            if isinstance(suspension, TodaSuspensionMap):
                domain, codomain = suspension.source_group, suspension.target_group
                if (isinstance(domain, TodaPrimaryGroup)
                        and isinstance(codomain, TodaPrimaryGroup)
                        and type(domain.group_dimension) is int
                        and type(domain.sphere_dimension) is int
                        and codomain == TodaPrimaryGroup(
                            domain.group_dimension + 1,
                            domain.sphere_dimension + 1,
                        )):
                    n = domain.sphere_dimension
                    k = domain.group_dimension - n
                    prior = exact_prior_database_result(n, k)
                    if isinstance(prior, Relation) and prior.relation_type is RelationType.EQUALITY:
                        options.extend(expand_zero_image_from_cyclic_generator(
                            statement, prior,
                        ))
        options.extend(expand_hopf_injective_from_zero_image(statement))
        options.extend(expand_cited_hopf_lift(statement, available))
        return tuple(options)

    return expand


def prepare_pi73_public_connection(*, bridge, goal, citing_assertion_id,
                                   prior_conclusions: tuple):
    """Return (augmented bridge, real target citation ID, public provider).

    This mirrors the existing pi_7^4 public connection: the target alone
    chooses the *routing*, never the mathematical facts. Returning None is a
    safe refusal; the existing ordinary search is left untouched.
    """
    if not isinstance(prior_conclusions, tuple):
        raise TypeError("prior_conclusions must be tuple")
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or goal.lhs != TodaPrimaryGroup(7, 3)):
        return None
    candidates = registered_group_goal_candidates(bridge, n=3, k=4)
    if len(candidates) != 1 or candidates[0] != goal:
        return None
    exact_id = resolve_specialized_goal_citing_id(bridge, goal)
    if not isinstance(exact_id, str) or not exact_id:
        return None
    if citing_assertion_id is not None and citing_assertion_id != exact_id:
        return None
    if (ADOPTED_ASSERTION_ID in bridge.registry._assertions
            or GENERAL_ASSERTION_ID in bridge.registry._assertions):
        return None
    root = Path(__file__).resolve().parents[1]
    verify_lemma54_before_lemma57(root)
    earlier = attach_earlier_verified_lemma54(bridge, exact_id)
    extra = build_isolated_lemma57_source(root)
    augmented = merge_isolated_cited_source(earlier, extra)
    for assertion_id in (ADOPTED_ASSERTION_ID, GENERAL_ASSERTION_ID):
        if assertion_id not in augmented.registry._assertions:
            return None
        if not precedes_citing_assertion(augmented, assertion_id, exact_id):
            return None
    screened = prefer_universal_prop42_derivation(
        screen_shared_proof_context(
            augmented, goal=goal, citing_assertion_id=exact_id,
            explicit_publication_target=True,
        )
    )
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None
        and link.step.rule is ProofRule.GIVEN
        and screened.registry.assertion(link.assertion_id).origin
        is AssertionOrigin.FIXED_STATEMENT
    )
    if (available.count(TodaLemma54TypedSource()) != 1
            or available.count(TodaLemma57GeneralCriterion()) != 1
            or goal in available):
        return None

    # Check the same independent, typed chain as R3R7 before making it public.
    prior = exact_prior_database_result(2, 4)
    if (not isinstance(prior, Relation)
            or prior.lhs != TodaPrimaryGroup(6, 2)):
        return None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    generator_image = GeneratorImage(e, prior.rhs.generator, Zero())
    inputs = lemma57_criterion_inputs(generator_image)
    if inputs is None:
        return None
    structure = CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order)
    lifts = expand_cited_hopf_lift(structure, available)
    if len(lifts) != 1 or lifts[0].subgoals[0] is None:
        return None
    hopf_inputs = hopf_injectivity_from_zero_image_inputs(lifts[0].subgoals[0])
    if hopf_inputs is None or hopf_inputs[0] != ImageZeroStatement(e):
        return None
    if len(expand_zero_image_from_cyclic_generator(hopf_inputs[0], prior)) != 1:
        return None

    from phase165_r52_r9_shared_math import shared_expansion_provider

    ordinary = shared_expansion_provider(
        screened, proof_target=goal, prior_conclusions=prior_conclusions,
    )
    extensions = public_cited_ehp_extensions(available)

    def provider(statement: object):
        # Keep R3R7's first-successful proposal ordering. No step is injected.
        return extensions(statement) + ordinary(statement)

    return augmented, exact_id, provider
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/install.py` — 全文

```python
"""Guarded single-function installer for the R3R8 public proof-search route.

Only a fixed insertion into search_shared_group_goal is permitted. DryRun
never writes to the worktree, and a failed normal audit can restore its exact
original bytes; no Git staging, reset or commit is performed.
"""
from __future__ import annotations

import ast
from hashlib import sha256
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
TARGET = Path("phase165_r52_r9_shared_math.py")
PINNED_GIT_BLOB = "9fa11b383812570fae1a26868c98992a5934a327"
ANCHOR = "    if citing_assertion_id is not None and expansion_provider is None:\n"
PUBLIC_INSERTION = (
    "    # R3R8: connect the R3R7 cited general EHP proof chain, not a saved result.\n"
    "    if n == 3 and k == 4 and expansion_provider is None:\n"
    "        from phase175_r3r8_pi73_public_connection.route import (\n"
    "            prepare_pi73_public_connection,\n"
    "        )\n"
    "        pi73_connection = prepare_pi73_public_connection(\n"
    "            bridge=bridge, goal=goal, citing_assertion_id=citing_assertion_id,\n"
    "            prior_conclusions=tuple(item.root.conclusion for item in prior),\n"
    "        )\n"
    "        if pi73_connection is not None:\n"
    "            bridge, citing_assertion_id, expansion_provider = pi73_connection\n"
)


def git(root: Path, *args: str) -> str:
    """Only execute nonmutating Git commands."""
    if not args or args[0] not in {"rev-parse", "branch", "diff", "status"}:
        raise ValueError("R3R8 read-only Git operation required")
    process = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode:
        raise RuntimeError("R3R8_GIT_QUERY_FAILED: " + " ".join(args))
    return process.stdout.rstrip("\r\n")


def find_function(text: str) -> tuple[int, int]:
    """Find exactly one complete top-level function using Python's AST."""
    parsed = ast.parse(text)
    matches = [node for node in parsed.body
               if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
               and node.name == "search_shared_group_goal"]
    if len(matches) != 1 or not isinstance(matches[0], ast.FunctionDef):
        raise RuntimeError("R3R8_SEARCH_FUNCTION_NOT_UNIQUE")
    node = matches[0]
    lines = text.splitlines(keepends=True)
    return (sum(len(line) for line in lines[:node.lineno - 1]),
            sum(len(line) for line in lines[:node.end_lineno]))


def preflight(root: Path = ROOT) -> dict[str, object]:
    """Verify exact tracked original, reviewed function contract and clean index."""
    root = Path(root).resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("R3R8_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("R3R8_WRONG_BRANCH")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != PINNED_GIT_BLOB:
        raise RuntimeError("R3R8_UNREVIEWED_PRODUCTION_BLOB")
    # The prior R3R7 handoff explicitly recorded a clean tracked worktree.
    tracked = git(root, "status", "--porcelain=v1", "--untracked-files=no")
    if tracked:
        raise RuntimeError("R3R8_UNREVIEWED_TRACKED_CHANGES: " + tracked[:300])
    content = (root / TARGET).read_bytes()
    if content.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R8_UNEXPECTED_BOM")
    original = content.decode("utf-8").replace("\r\n", "\n")
    start, end = find_function(original)
    original_function = original[start:end]
    if original_function.count(ANCHOR) != 1 or PUBLIC_INSERTION in original:
        raise RuntimeError("R3R8_UNREVIEWED_ROUTING_ANCHOR")
    template = (PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(encoding="utf-8")
    if template.count(PUBLIC_INSERTION) != 1:
        raise RuntimeError("R3R8_FULL_FUNCTION_TEMPLATE_INVALID")
    old_ast = ast.dump(ast.parse(original_function), include_attributes=False)
    source_ast = ast.dump(ast.parse(template.replace(PUBLIC_INSERTION, "")), include_attributes=False)
    if old_ast != source_ast:
        raise RuntimeError("R3R8_EXISTING_FUNCTION_CHANGED_SINCE_REVIEW")
    compiled = original[:start] + original_function.replace(
        ANCHOR, PUBLIC_INSERTION + ANCHOR, 1,
    ) + original[end:]
    compile(compiled, str(root / TARGET), "exec")
    worktree_text = content.decode("utf-8")
    newline = "\r\n" if "\r\n" in worktree_text else "\n"
    actual_anchor = ANCHOR.replace("\n", newline)
    actual_insertion = PUBLIC_INSERTION.replace("\n", newline)
    if worktree_text.count(actual_anchor) != 1:
        raise RuntimeError("R3R8_WORKTREE_EOL_ANCHOR_CHANGED")
    candidate_bytes = worktree_text.replace(
        actual_anchor, actual_insertion + actual_anchor, 1,
    ).encode("utf-8")
    return {
        "head": git(root, "rev-parse", "HEAD"),
        "original_git_blob": PINNED_GIT_BLOB,
        "original_sha256": sha256(content).hexdigest(),
        "candidate_sha256": sha256(candidate_bytes).hexdigest(),
        "function_name": "search_shared_group_goal",
        "modified_tracked_files": [TARGET.as_posix()],
        "new_specific_given": 0,
        "new_proof_replay": 0,
        "whole_pytest_executed": False,
    }


def apply(root: Path, backup_folder: Path) -> dict[str, object]:
    """Replace one function only; preserve the input bytes for rollback."""
    evidence = preflight(root)
    root = Path(root).resolve()
    path = root / TARGET
    before = path.read_bytes()
    original = before.decode("utf-8")
    newline = "\r\n" if "\r\n" in original else "\n"
    anchor = ANCHOR.replace("\n", newline)
    insertion = PUBLIC_INSERTION.replace("\n", newline)
    if original.count(anchor) != 1:
        raise RuntimeError("R3R8_SOURCE_ANCHOR_DRIFT")
    final = original.replace(anchor, insertion + anchor, 1).encode("utf-8")
    if sha256(final).hexdigest() != evidence["candidate_sha256"]:
        raise RuntimeError("R3R8_CANDIDATE_HASH_CHANGED")
    backup_folder.mkdir(parents=True, exist_ok=True)
    (backup_folder / "phase165_r52_r9_shared_math.py.before").write_bytes(before)
    path.write_bytes(final)
    actual = path.read_bytes()
    if actual != final:
        raise RuntimeError("R3R8_WRITE_VERIFICATION_FAILED")
    return {**evidence, "installed_sha256": sha256(actual).hexdigest()}


def verify_postflight(root: Path, evidence: dict[str, object]) -> None:
    """After success, only the one reviewed public function may be dirty."""
    actual = (Path(root) / TARGET).read_bytes()
    if sha256(actual).hexdigest() != evidence["installed_sha256"]:
        raise RuntimeError("R3R8_PATCH_MUTATED_AFTER_INSTALL")
    records = git(root, "status", "--porcelain=v1", "--untracked-files=no")
    if records != " M " + TARGET.as_posix():
        raise RuntimeError("R3R8_UNEXPECTED_TRACKED_POSTFLIGHT: " + records)


def rollback(root: Path, backup_folder: Path) -> None:
    """Restore byte-identical clean original on failed installation or audit."""
    original = (backup_folder / "phase165_r52_r9_shared_math.py.before").read_bytes()
    (Path(root) / TARGET).write_bytes(original)
    if (Path(root) / TARGET).read_bytes() != original:
        raise RuntimeError("R3R8_ROLLBACK_VERIFICATION_FAILED")
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/audit.py` — 全文

```python
"""Phase 175 R3R8: guarded public wiring and real Group query verification."""
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

from phase175_r3r7_lemma54_membership import audit as previous
from phase175_r3r8_pi73_public_connection import install

PACKAGE = "phase175_r3r8_pi73_public_connection"
MARKER = "__PHASE175_R3R8_WORKER__="
FOCUSED_TESTS = (
    "phase175_r3r8_pi73_public_connection/tests",
    "phase175_r3r7_lemma54_membership/tests/test_rule.py",
    "phase175_r3r6_lemma57_general/tests/test_rule.py",
    "phase175_r3_pi73_hopf_lift/tests/test_rule.py",
    "phase173_r4_r1_public_connection/tests",
)
EXPECTED_R3R7 = frozenset({
    "lemma54_double_relation",
    "double_suspension_membership",
    "lemma57_zero_generator_image",
    "zero_suspension_image",
    "hopf_injectivity",
    "pi73_cyclic_lift",
})


def latest_successful_r3r7() -> Path:
    """Use actual user-executed normal R3R7 evidence, never a claimed result."""
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    directory = base / "EHPProofTracerAudit" / "phase175_r3r7_lemma54_membership"
    for path in sorted(directory.glob("*/report.json"), reverse=True):
        try:
            report = json.loads(path.read_text(encoding="utf-8"))
            worker = report.get("worker")
            data = worker.get("data") if isinstance(worker, dict) else None
            if not isinstance(data, dict):
                continue
            rows = data.get("observations", ())
            actual = {row["name"]: row["status"] for row in rows}
            if (report.get("phase") == "175-R3R7"
                    and report.get("dry_run") is False
                    and report.get("result") == "PASS_R3R7_ISOLATED_PI73_CYCLIC_INFERRED"
                    and report.get("tracked_unchanged") is True
                    and data.get("new_specific_given") == 0
                    and data.get("new_production_rules") == 0
                    and data.get("public_provider_modified") is False
                    and set(actual) == EXPECTED_R3R7
                    and all(value == "INFERRED" for value in actual.values())):
                return path
        except (OSError, UnicodeError, KeyError, ValueError, TypeError):
            continue
    raise RuntimeError("R3R8_NO_VALID_COMPLETED_R3R7_NORMAL_AUDIT")


def worker() -> int:
    """Reuse the real R1 auditor: typed search + trust check + common Web renderer."""
    try:
        from phase175_r1_k4_audit.audit import inspect_one_group
        result = {"status": "INSPECTED", "data": inspect_one_group(3, 4)}
    except Exception as exc:
        result = {"status": "ERROR", "error": type(exc).__name__ + ": " + str(exc),
                  "traceback": traceback.format_exc()[-7000:]}
    print(MARKER + json.dumps(result, ensure_ascii=False), flush=True)
    return 0


def run_worker(root: Path, folder: Path, seconds: int) -> dict:
    """Constrain full public path inspection in a child process."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    try:
        completed = subprocess.run(
            [sys.executable, "-B", "-m", PACKAGE + ".audit", "--worker"],
            cwd=root, env=env, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=seconds, check=False,
        )
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "seconds": seconds}
    (folder / "worker.log").write_text(
        completed.stdout + "\nSTDERR:\n" + completed.stderr, encoding="utf-8",
    )
    rows = [line[len(MARKER):] for line in completed.stdout.splitlines()
            if line.startswith(MARKER)]
    if completed.returncode or len(rows) != 1:
        return {"status": "INVALID_WORKER", "code": completed.returncode,
                "marker_count": len(rows)}
    try:
        value = json.loads(rows[0])
    except json.JSONDecodeError:
        return {"status": "INVALID_WORKER_JSON"}
    return value if isinstance(value, dict) else {"status": "INVALID_WORKER_PAYLOAD"}


def focused_pytest(root: Path, folder: Path, seconds: int) -> None:
    """Run targeted tests only; record errors without a full-suite run."""
    env = dict(os.environ)
    env.update(PYTHONUTF8="1", PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    env["PYTHONPATH"] = str(root) + os.pathsep + env.get("PYTHONPATH", "")
    args = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider",
            *FOCUSED_TESTS]
    try:
        completed = subprocess.run(
            args, cwd=root, capture_output=True, text=True, encoding="utf-8",
            errors="replace", timeout=seconds, env=env, check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("R3R8_FOCUSED_PYTEST_TIMEOUT") from exc
    output = completed.stdout + "\nSTDERR:\n" + completed.stderr
    (folder / "focused_pytest.log").write_text(output, encoding="utf-8")
    tail = completed.stdout.strip().splitlines()
    for line in tail[-3:]:
        print("PHASE175_R3R8_PYTEST_OUTPUT=" + line[:500], flush=True)
    if completed.returncode:
        raise RuntimeError("R3R8_FOCUSED_PYTEST_FAILED: " + output[-1600:])
    print("PHASE175_R3R8_FOCUSED_PYTEST=PASS", flush=True)


def write_report(folder: Path, report: dict[str, object]) -> None:
    """All evidence and backup files remain outside the Git checkout."""
    (folder / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R3R8 — 通常 Group query 公開接続", "",
        "- Gate: `" + str(report.get("result")) + "`",
        "- 対象: $\\pi_7^3=\\mathbb Z/2\\{\\nu'\\eta_6\\}$",
        "- 新規結論 GIVEN: 0、保存済み証明再利用: 0",
        "- 全体 pytest: 未実施", "",
    ]
    worker_result = report.get("worker", {})
    if isinstance(worker_result, dict):
        data = worker_result.get("data", {})
        if isinstance(data, dict):
            lines += [
                "## 実測結果", "",
                "- Search: `" + str(data.get("search_status")) + "`",
                "- 完成証明: `" + str(data.get("audit_result")) + "`",
                "- 未解決 Goal: " + str(data.get("search_open_count")),
                "- 証明ステップ数: " + str(data.get("search_proven_count")),
                "- Trust boundary: " + str(data.get("trust_verified")),
                "- Web key: `" + str(data.get("web_key")) + "`",
                "- Reference 件数: " + str(data.get("reference_count")), "",
            ]
            if data.get("exception"):
                lines.append("- 例外: `" + str(data["exception"]) + "`")
            if data.get("web_error"):
                lines.append("- Web 例外: `" + str(data["web_error"]) + "`")
    if report.get("error"):
        lines += ["## 失敗", "", "`" + str(report["error"]) + "`"]
    (folder / "report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(root: Path, dry_run: bool, seconds: int) -> int:
    """Preflight and real verification, rolling back a failed public install."""
    root = Path(root).resolve()
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S_%fZ"
    )
    folder.mkdir(parents=True, exist_ok=False)
    report: dict[str, object] = {
        "phase": "175-R3R8", "dry_run": dry_run, "result": "NOT_STARTED",
        "new_specific_given": 0, "new_mathematical_rules": 0,
        "full_pytest": False, "modified_file": str(install.TARGET),
    }
    installed = False
    result_code = 2
    print("PHASE175_R3R8_OUTPUT=" + str(folder), flush=True)
    try:
        report["preflight_source_guard"] = previous.scoped_preflight(root)
        report["r3r7_report"] = str(latest_successful_r3r7())
        report["patch_preflight"] = install.preflight(root)
        print("PHASE175_R3R8_SOURCE_GUARD=PASS", flush=True)
        print("PHASE175_R3R8_R3R7_SIX_INFERENCES=PASS", flush=True)
        if dry_run:
            # Check all source and patch contracts but do not modify any file.
            report["result"] = "PASS_R3R8_READ_ONLY_DRYRUN"
            result_code = 0
        else:
            report["installation"] = install.apply(root, folder)
            installed = True
            print("PHASE175_R3R8_PATCH_APPLIED=ONE_FUNCTION", flush=True)
            focused_pytest(root, folder, seconds)
            inspected = run_worker(root, folder, seconds)
            report["worker"] = inspected
            if inspected.get("status") != "INSPECTED":
                raise RuntimeError("R3R8_PUBLIC_WORKER_FAILED: " + str(inspected))
            data = inspected.get("data", {})
            print("PHASE175_R3R8_SEARCH=" + str(data.get("search_status")), flush=True)
            print("PHASE175_R3R8_TRUST_VERIFIED=" + str(data.get("trust_verified")), flush=True)
            print("PHASE175_R3R8_WEB_KEY=" + str(data.get("web_key")), flush=True)
            print("PHASE175_R3R8_WEB_REFERENCES=" + str(data.get("reference_count")), flush=True)
            if not (
                data.get("audit_result") == "COMPLETE_AND_WEB_VERIFIED"
                and data.get("search_status") == "complete"
                and data.get("search_open_count") == 0
                and data.get("search_conclusion_matches_db") is True
                and data.get("trust_verified") is True
                and data.get("model_root_verified") is True
                and data.get("web_key") == "generic-complete-proof"
                and data.get("web_partial") is False
                and isinstance(data.get("reference_count"), int)
                and data["reference_count"] >= 2
            ):
                raise RuntimeError("R3R8_PUBLIC_VERIFICATION_INCOMPLETE: " + str({
                    key: data.get(key) for key in (
                        "audit_result", "search_status", "search_open_count",
                        "search_proven_count", "trust_verified", "model_error",
                        "web_key", "web_error", "exception",
                    )
                }))
            install.verify_postflight(root, report["installation"])
            report["result"] = "PASS_R3R8_PUBLIC_PI73_COMPLETE_AND_WEB_VERIFIED"
            result_code = 0
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-6000:]
        report["result"] = "R3R8_REFUSED_OR_PUBLIC_VERIFICATION_FAILED"
        print("PHASE175_R3R8_ERROR=" + report["error"], flush=True)
    finally:
        if installed and result_code != 0:
            try:
                install.rollback(root, folder)
                report["rolled_back"] = True
                print("PHASE175_R3R8_ROLLBACK=PASS", flush=True)
            except Exception as exc:
                report["rolled_back"] = False
                report["rollback_error"] = str(exc)
                report["result"] = "R3R8_ROLLBACK_FAILED"
        report["tracked_unchanged"] = bool(dry_run or (result_code != 0 and report.get("rolled_back")))
        write_report(folder, report)
        print("PHASE175_R3R8_REPORT=" + str(folder / "report.json"), flush=True)
        print("PHASE175_R3R8_GATE=" + str(report["result"]), flush=True)
        print("(END)", flush=True)
    return result_code


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=install.ROOT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--worker", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    if args.timeout_seconds < 1:
        parser.error("timeout must be positive")
    if args.worker:
        return worker()
    return run(args.root, args.dry_run, args.timeout_seconds)


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/tests/__init__.py` — 全文

```python
"""Focused Phase 175 R3R8 regression tests."""
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/tests/test_install.py` — 全文

```python
"""Installer must not alter other functions, APIs or unexpected Git states."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r3r8_pi73_public_connection import install


def test_complete_function_template_compiles_without_elision() -> None:
    full = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    assert full.count(install.PUBLIC_INSERTION) == 1
    compile(full, "search_shared_group_goal_FULL.py.txt", "exec")
    original = full.replace(install.PUBLIC_INSERTION, "")
    assert install.ANCHOR in original
    assert original.replace(
        install.ANCHOR, install.PUBLIC_INSERTION + install.ANCHOR, 1,
    ) == full
    parsed = ast.parse(full)
    assert len(parsed.body) == 1
    assert isinstance(parsed.body[0], ast.FunctionDef)
    assert parsed.body[0].name == "search_shared_group_goal"


def test_full_function_preserves_existing_public_api() -> None:
    full = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    node = ast.parse(full).body[0]
    expected = {
        "n", "k", "group_structure", "bridge", "expansion_provider",
        "citing_assertion_id", "verified_assertion_ids",
        "completed_internal_proofs", "proof_use_order",
        "ordered_completed_proofs", "target_order", "proof_order_catalog",
        "recursive_proof_order_catalog", "context_sink",
    }
    assert set(arg.arg for arg in node.args.kwonlyargs) == expected
    assert len(node.args.posonlyargs) == 0


def test_find_function_requires_exactly_one_top_level_definition() -> None:
    source = "def search_shared_group_goal():\n    return 1\n"
    assert install.find_function(source) == (0, len(source))
    with pytest.raises(RuntimeError, match="FUNCTION_NOT_UNIQUE"):
        install.find_function(source + "\n" + source)
    with pytest.raises(RuntimeError, match="FUNCTION_NOT_UNIQUE"):
        install.find_function("def other():\n    pass\n")


def test_git_command_whitelist_is_read_only(tmp_path: Path) -> None:
    for denied in ("add", "reset", "checkout", "commit", "clean", "push"):
        with pytest.raises(ValueError, match="read-only"):
            install.git(tmp_path, denied, "something")


def test_patch_has_no_import_change_or_other_api_change() -> None:
    template = (install.PACKAGE / "search_shared_group_goal_FULL.py.txt").read_text(
        encoding="utf-8",
    )
    before = ast.parse(template.replace(install.PUBLIC_INSERTION, "")).body[0]
    after = ast.parse(template).body[0]
    assert ast.dump(before.args) == ast.dump(after.args)
    assert len(after.body) == len(before.body) + 1
    assert not any(isinstance(node, (ast.Global, ast.Nonlocal)) for node in after.body)
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/tests/test_route.py` — 全文

```python
"""Actual typed proof-connection tests; no synthetic completed ProofSteps."""
from __future__ import annotations

from dataclasses import replace

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageZeroStatement
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r14_r6_generic_iso import GeneratorImage
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r1_lemma54_source_bridge.source import TodaLemma54TypedSource
from phase175_r3r6_lemma57_general.rule import lemma57_criterion_inputs
from phase175_r3r6_lemma57_general.source import TodaLemma57GeneralCriterion
from phase175_r3r7_lemma54_membership.rule import cited_lemma54_double_relation
from phase175_r3r8_pi73_public_connection.route import (
    prepare_pi73_public_connection,
    public_cited_ehp_extensions,
)
from proof import ProofRule


def test_pi73_prepared_provider_exposes_six_independent_goals() -> None:
    bridge = build_shared_typed_bridge()
    candidates = registered_group_goal_candidates(bridge, n=3, k=4)
    assert len(candidates) == 1
    goal = candidates[0]
    prepared = prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id=None,
        prior_conclusions=(),
    )
    assert prepared is not None
    augmented, citing_id, provider = prepared
    assert citing_id == resolve_specialized_goal_citing_id(bridge, goal)
    assert len(provider(cited_lemma54_double_relation())) >= 1
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    e = TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3))
    zero = GeneratorImage(e, prior.rhs.generator, Zero())
    general, membership = lemma57_criterion_inputs(zero)
    for target in (
        membership, zero, ImageZeroStatement(e),
        CyclicStructureStatement(goal.lhs, goal.rhs.generator, goal.rhs.order),
    ):
        assert len(provider(target)) >= 1
    assert general == TodaLemma57GeneralCriterion()
    assert not any(link.step is not None and link.step.conclusion == goal
                   for link in augmented.proof_links)
    assert ADOPTED_ID not in bridge.registry._assertions


ADOPTED_ID = "phase173:r4r1:lemma54:typed_hopf_source"


def test_wrong_or_unregistered_goal_cannot_enable_connection() -> None:
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=4)
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=replace(goal, lhs=TodaPrimaryGroup(9, 3)),
        citing_assertion_id=None, prior_conclusions=(),
    ) is None
    assert prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id="invented-id",
        prior_conclusions=(),
    ) is None


def test_public_proposals_never_directly_prove_a_goal() -> None:
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=4)
    result = prepare_pi73_public_connection(
        bridge=bridge, goal=goal, citing_assertion_id=None, prior_conclusions=(),
    )
    assert result is not None
    augmented, citing, provider = result
    screened = screen_shared_proof_context(
        augmented, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    )
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    assert available.count(TodaLemma54TypedSource()) == 1
    assert available.count(TodaLemma57GeneralCriterion()) == 1
    assert goal not in available
    extension = public_cited_ehp_extensions(available)
    for offered in extension(cited_lemma54_double_relation()):
        assert hasattr(offered, "subgoals")
        assert not hasattr(offered, "conclusion")
    assert provider(goal) is not None
```

## 新規ファイル `phase175_r3r8_pi73_public_connection/run.ps1` — 全文

```powershell
param(
    [switch]$DryRun,
    [int]$TimeoutSeconds = 300
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

if ($DryRun) {
    Write-Output 'PHASE175_R3R8_DRYRUN_START'
    & python -B -m phase175_r3r8_pi73_public_connection.audit `
        --root $root --dry-run --timeout-seconds $TimeoutSeconds
    $code = $LASTEXITCODE
    Write-Output "PHASE175_R3R8_EXIT_CODE=$code"
    exit $code
}

Write-Output 'PHASE175_R3R8_PUBLIC_INTEGRATION_START'
& python -B -m phase175_r3r8_pi73_public_connection.audit `
    --root $root --timeout-seconds $TimeoutSeconds
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R8_EXIT_CODE=$code"
exit $code
```

## 実行する限定テスト

Windows本リポジトリで `run.ps1` の本実行時に以下を実施します。

```powershell
python -B -m pytest -q -p no:cacheprovider phase175_r3r8_pi73_public_connection/tests phase175_r3r7_lemma54_membership/tests/test_rule.py phase175_r3r6_lemma57_general/tests/test_rule.py phase175_r3_pi73_hopf_lift/tests/test_rule.py phase173_r4_r1_public_connection/tests
```

## 完了条件と次Phaseとの境界

通常検索の証明木が完成し、共通Webが `generic-complete-proof` を返す場合のみGate PASS。その他の群、Renderer、全体pytestはR3R8で変更・実施しません。
