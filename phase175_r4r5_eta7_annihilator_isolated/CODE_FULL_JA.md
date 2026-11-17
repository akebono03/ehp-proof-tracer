# Phase 175 R4R5R2 — 実行コード・テスト全文

## 変更対象の一覧

今回の変更は既存の監査パッケージ `phase175_r4r5_eta7_annihilator_isolated/` 内に限定する。GitHub 本番の証明探索・データベース・共通 Renderer、ルートの5文書は変更しない。

### ファイル・関数

- `rule.py`（import 全文を変更）：既存 `typed_endpoints()`、`order_zero_premise()`、`finite_cyclic_order_zero_rule()`、`expand_finite_cyclic_order_zero()` の関数全文を更新。`typed_endpoints()` の直後に新規 `_finite_cyclic_components()` を追加。従来の単独巡回群 API は維持。
- `audit.py`（import 全文・定数を更新）：`eta7_prior_and_isolated_zero()` の直後に新規 `direct_sum_prior_and_isolated_zero()` を追加。既存 `run()` 全体を更新。既存 R4R5R1 の関数・検証境界は維持。
- `tests/test_rule.py`（末尾に新規テスト関数）：直和・入れ子・別成分・一般次数・懸垂式・型不一致・未証明の拒否・`ZERO` 型を確認。既存テストは維持。
- `tests/test_audit.py`（末尾にテスト関数・fixture）：実際の π₈⁴ の2成分に相当する型付き構造と、既存 DB prior 認証 API の失敗経路を模擬。既存テストは維持。
- `run.ps1`：限定 pytest・監査の標準出力に R4R5R2 の表示を追加。
- `README.md`、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、本書：全文更新。README は英語、それ以外は日本語。

クラスの変更・追加なし。テスト以外の本番モジュールの変更なし。以下に、import を含む全ファイルを**省略なし**で掲載する。テストコードはテスト関数全文と import 全文を含む。

## `rule.py` — 全文

```python
"""A proved finite-cyclic direct summand annihilates its typed generator.

Works for a single FiniteCyclicGroup and for each finite cyclic summand of a
DirectSumGroup, including nested sums. No group presentation is asserted here.
A source-first caller supplies concrete candidate presentations to the
backward provider; the ordinary engine must prove the chosen premise.
"""
from __future__ import annotations

from expression import (
    Composition, HomotopyElement, IteratedSuspension, Multiple,
    Sum, Suspension, Zero,
)
from homotopy_groups import (
    DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import (
    InferenceRule, PremisePattern, ProofRule, Relation, RelationType,
)

RULE_NAME = "proved finite cyclic summand order annihilates its generator"


def typed_endpoints(element: object) -> tuple[int, int] | None:
    """Return (source dimension, sphere dimension) when endpoints are typed."""
    if isinstance(element, HomotopyElement):
        if not all(type(value) is int for value in (
            element.dimension, element.source, element.target,
        )):
            return None
        if (element.dimension != element.target or element.target < 2
                or element.source <= element.target):
            return None
        return element.source, element.target
    if isinstance(element, Composition):
        left = typed_endpoints(element.left)
        right = typed_endpoints(element.right)
        if left is None or right is None or left[0] != right[1]:
            return None
        return right[0], left[1]
    if isinstance(element, Suspension):
        pair = typed_endpoints(element.expression)
        if pair is None:
            return None
        return pair[0] + 1, pair[1] + 1
    if isinstance(element, IteratedSuspension):
        if type(element.exponent) is not int or element.exponent < 0:
            return None
        pair = typed_endpoints(element.expression)
        if pair is None:
            return None
        return pair[0] + element.exponent, pair[1] + element.exponent
    if isinstance(element, Multiple):
        if type(element.coefficient) is not int:
            return None
        return typed_endpoints(element.expression)
    if isinstance(element, Sum):
        left = typed_endpoints(element.left)
        right = typed_endpoints(element.right)
        if left is None or left != right:
            return None
        return left
    return None


def _finite_cyclic_components(structure: object) -> tuple[FiniteCyclicGroup, ...]:
    """Traverse only actual finite cyclic components of a typed presentation."""
    if isinstance(structure, FiniteCyclicGroup):
        if type(structure.order) is int and structure.order >= 2:
            return (structure,)
        return ()
    if not isinstance(structure, DirectSumGroup):
        return ()
    components: list[FiniteCyclicGroup] = []
    for summand in structure.summands:
        components.extend(_finite_cyclic_components(summand))
    return tuple(components)


def order_zero_premise(
    goal: object, presentation: Relation | None = None,
) -> Relation | None:
    """Validate one candidate source, never infer an arbitrary complement.

    No presentation: preserve the R4R5R1 single-cyclic backward obligation.
    Supplied presentation: require the exact target generator as a finite
    cyclic summand with the specified order, and matching sphere endpoints.
    """
    if (not isinstance(goal, Relation)
            or goal.relation_type not in (RelationType.EQUALITY, RelationType.ZERO)
            or type(goal.lhs) is not Multiple
            or type(goal.lhs.coefficient) is not int
            or goal.lhs.coefficient < 2
            or type(goal.rhs) is not Zero
            or goal.source is not None
            or goal.note is not None):
        return None
    endpoints = typed_endpoints(goal.lhs.expression)
    if endpoints is None:
        return None
    source, target = endpoints
    group = TodaPrimaryGroup(source, target)
    if presentation is None:
        return Relation(
            lhs=group,
            rhs=FiniteCyclicGroup(goal.lhs.coefficient, goal.lhs.expression),
            relation_type=RelationType.EQUALITY,
        )
    if (not isinstance(presentation, Relation)
            or presentation.relation_type is not RelationType.EQUALITY
            or presentation.lhs != group):
        return None
    for summand in _finite_cyclic_components(presentation.rhs):
        if (summand.order == goal.lhs.coefficient
                and summand.generator == goal.lhs.expression):
            return presentation
    return None


def finite_cyclic_order_zero_rule(
    goal: Relation, presentation: Relation | None = None,
) -> InferenceRule:
    """One-premise ordinary rule, binding the *entire* group presentation."""
    expected = order_zero_premise(goal, presentation)
    if expected is None:
        raise ValueError("goal must be a typed finite-order generator zero equality with a proved finite-cyclic summand presentation")

    def guard(premises, bindings) -> bool:
        return (
            len(premises) == 1
            and premises[0].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[0].conclusion == expected
            and order_zero_premise(goal, expected) == expected
        )

    def conclusion_builder(premises) -> Relation:
        if (len(premises) != 1
                or premises[0].conclusion != expected
                or order_zero_premise(goal, expected) != expected):
            raise ValueError("the proved finite-cyclic summand is required")
        return goal

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "In a proved group presentation, every finite-cyclic summand "
            "Z/m{g} satisfies m*g=0. The presentation must be proved first."
        ),
        premise_patterns=(
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=expected,
            ),
        ),
        conclusion_builder=conclusion_builder,
        match_guard=guard,
    )


def expand_finite_cyclic_order_zero(
    goal: object, presentations: tuple[Relation, ...] = (),
) -> tuple[GoalExpansion, ...]:
    """Provide source-first backward proposals for any verified component.

    With no source candidates retain the previous single-cyclic proposal.
    With source candidates, use only matching concrete presentations; do not
    fabricate complement groups or treat candidates as verified evidence.
    """
    if not isinstance(presentations, tuple):
        raise TypeError("presentations must be a tuple")
    if not presentations:
        premise = order_zero_premise(goal)
        if premise is None:
            return ()
        return (GoalExpansion(finite_cyclic_order_zero_rule(goal), (premise,)),)
    results: list[GoalExpansion] = []
    seen: list[Relation] = []
    for candidate in presentations:
        premise = order_zero_premise(goal, candidate)
        if premise is None or premise in seen:
            continue
        seen.append(premise)
        results.append(GoalExpansion(
            finite_cyclic_order_zero_rule(goal, premise), (premise,),
        ))
    return tuple(results)
```

## `audit.py` — 全文

```python
"""Phase 175 R4R5R2: derive m*g=0 from finite-cyclic summands.

Reuse explicit ordered DB priors for both pi_8^7 and pi_8^4; never replay
prior proofs. Direct-sum and single-summand inferences remain isolated;
production and source registries are not modified.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback

from phase175_r4_pi95_audit.audit import git, preflight
from phase175_r4r4_pi95_premise_frontier.audit import verify_code_and_source_pins
from phase175_r4r5_eta7_annihilator_isolated.rule import (
    expand_finite_cyclic_order_zero,
    order_zero_premise, typed_endpoints,
)

PACKAGE = "phase175_r4r5_eta7_annihilator_isolated"
PRIOR_PACKAGE = "phase175_r4r4_pi95_premise_frontier"
PRIOR_GATE = "PASS_R4R4_PREMISE_FRONTIER_RECORDED_NOT_PUBLIC"
EXPECTED_PRIOR_HEAD = "43140c00d311e4bbcc20688eb9e50a5d0050a787"
PINNED_R4R4_BLOB = "0a9fbbd1c3262dfc46ec8f6e8a819eb5876742fc"
DRY_GATE = "PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_DRYRUN"
FINAL_GATE = "PASS_R4R5R2_DIRECT_SUM_ORDER_ZERO_ISOLATED_NOT_PUBLIC"
EXTRA_SOURCE_PINS = {
    # Existing ordered DB prior API and the concrete parsers it calls.
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase169_r3m_prior_result_catalog/prior_results.py": "c522cbaf924b3a9aa500d453b8eb6a1a66c42611",
    "phase166_r3af_goal_adapter.py": "d85f595c9c8be18a2db760b8a20868b40eb15300",
    "phase166_r3aj_structured_generator.py": "c6ecbc4bb95631a58de38b412879d22c1e1c2c61",
    "repository.py": "b648a360e98e3c3143d8f3c7489d8ade46b9ecb0",
    "data/sphere.csv": "b7e98a4469e0dcf2c5ea16691a7225951fd36395",
    "data/HyoujiGen.csv": "26f33db0c83ba7f151433583fe861598399cbe6a",
    # Structural types and ordinary inference replay.
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "phase175_r4r4_pi95_premise_frontier/audit.py": PINNED_R4R4_BLOB,
}


def latest_prior_report(explicit: Path | None = None) -> Path:
    """Use only a successful non-DryRun R4R4 report, never invented evidence."""
    if explicit is not None:
        found = explicit.resolve()
        if not found.is_file():
            raise RuntimeError("R4R5_R4R4_REPORT_MISSING: " + str(found))
        return found
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    for found in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            record = json.loads(found.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, TypeError):
            continue
        if isinstance(record, dict) and record.get("gate") == PRIOR_GATE:
            return found
    raise RuntimeError("R4R5_SUCCESSFUL_R4R4_REPORT_NOT_FOUND")


def validate_prior_report(record: object) -> dict[str, object]:
    """Check provenance and scope; a prior audit is never a proof certificate."""
    if not isinstance(record, dict):
        raise RuntimeError("R4R5_PRIOR_NOT_OBJECT")
    expected = {
        "phase": "175-R4R4",
        "mode": "SOURCE_FIRST_PREMISE_FRONTIER_AUDIT",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "public_proof_complete": False,
        "full_pytest_executed": False,
        "premise_count": 6,
        "verified_parent_steps_replayed_here": 0,
    }
    if any(record.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R5_PRIOR_GATE_OR_SCOPE_INVALID")
    preflight_data = record.get("preflight")
    if (not isinstance(preflight_data, dict)
            or preflight_data.get("head") != EXPECTED_PRIOR_HEAD
            or preflight_data.get("pinned_source_count") != 18):
        raise RuntimeError("R4R5_PRIOR_HEAD_OR_SOURCE_INVALID")
    rows = record.get("premises")
    if (not isinstance(rows, list) or len(rows) != 6
            or [row.get("index") for row in rows if isinstance(row, dict)]
            != [1, 2, 3, 4, 5, 6]
            or any(row.get("verified_parent_step_in_r4r4") is not False
                   for row in rows if isinstance(row, dict))):
        raise RuntimeError("R4R5_PRIOR_PREMISE_FRONTIER_INVALID")
    return {"prior_head": preflight_data["head"], "premises": len(rows),
            "prior_audit_is_not_a_proof": True}


def validate_prior_lineage(root: Path, old_head: str, current_head: str) -> list[str]:
    """Allow the verified R4R4 package commit, no unrelated tracked changes."""
    if old_head != EXPECTED_PRIOR_HEAD:
        raise RuntimeError("R4R5_UNREVIEWED_PRIOR_HEAD")
    _, observed_head = git(root, "rev-parse", "HEAD")
    if observed_head != current_head:
        raise RuntimeError("R4R5_HEAD_CHANGED")
    status, _ = git(root, "merge-base", "--is-ancestor", old_head, current_head,
                    allow_failure=True)
    if status != 0:
        raise RuntimeError("R4R5_PRIOR_HEAD_NOT_ANCESTOR")
    _, names = git(root, "diff", "--name-only", old_head, current_head)
    changed = sorted(set(name.strip() for name in names.splitlines() if name.strip()))
    extra = [name for name in changed if not name.startswith(PRIOR_PACKAGE + "/")]
    if extra:
        raise RuntimeError("R4R5_UNREVIEWED_LINEAGE_CHANGES: " + repr(extra))
    return changed


def verify_source_pins(root: Path) -> dict[str, str]:
    """Pin committed DB-prior implementation, source data and inference code."""
    for name, expected in EXTRA_SOURCE_PINS.items():
        if not (root / name).is_file():
            raise RuntimeError("R4R5_SOURCE_MISSING: " + name)
        _, actual = git(root, "rev-parse", "HEAD:" + name)
        if actual != expected:
            raise RuntimeError("R4R5_SOURCE_PIN_DRIFT: " + name)
    verify_code_and_source_pins(root)
    return dict(EXTRA_SOURCE_PINS)


def eta7_prior_and_isolated_zero() -> dict[str, object]:
    """Reuse the verified, ordered DB prior; DO NOT reconstruct its proof tree.

    The target group is read only as a typed goal for the existing prior-order
    gate. Neither group row is asserted as a new literature statement. The
    ordinary m*g=0 inference is replayed against a checked DB-prior ProofStep.
    """
    from expression import GeneratorSymbol, HomotopyElement, Multiple, Zero
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, precedes_db_goal,
        verified_db_step,
    )
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match,
        find_inference_matches_for_rule,
    )

    source_relation = exact_prior_database_result(7, 1)
    if (not isinstance(source_relation, Relation)
            or source_relation.relation_type is not RelationType.EQUALITY
            or source_relation.lhs != TodaPrimaryGroup(8, 7)
            or not isinstance(source_relation.rhs, FiniteCyclicGroup)
            or type(source_relation.rhs.order) is not int
            or source_relation.rhs.order != 2):
        raise RuntimeError("R4R5_PI87_DB_PRIOR_UNAVAILABLE_OR_INVALID")
    generator = source_relation.rhs.generator
    if (not isinstance(generator, HomotopyElement)
            or generator.source != 8
            or generator.target != 7
            or generator.dimension != 7
            or not isinstance(generator.generator, GeneratorSymbol)
            or generator.generator.family != "η"
            or generator.generator.index != 7):
        raise RuntimeError("R4R5_PI87_DB_GENERATOR_UNVERIFIED")

    # The target is a GOAL only, not an assumed/proved result.
    target_relation = exact_prior_database_result(5, 4)
    if (not isinstance(target_relation, Relation)
            or target_relation.relation_type is not RelationType.EQUALITY
            or target_relation.lhs != TodaPrimaryGroup(9, 5)):
        raise RuntimeError("R4R5_PI95_DB_TARGET_GOAL_MISSING")
    if not precedes_db_goal(7, 1, 5, 4):
        raise RuntimeError("R4R5_PRIOR_ORDER_DISALLOWED")

    adopted_step = admitted_db_step(
        source_relation, proof_target=target_relation,
    )
    if (adopted_step is None
            or adopted_step.rule is not ProofRule.GIVEN
            or adopted_step.premises
            or adopted_step.conclusion != source_relation
            or not verified_db_step(adopted_step, proof_target=target_relation)):
        raise RuntimeError("R4R5_PI87_DB_PRIOR_AUTHENTICATION_FAILED")

    goal = Relation(Multiple(2, generator), Zero(), RelationType.EQUALITY)
    if order_zero_premise(goal) != source_relation:
        raise RuntimeError("R4R5_ORDER_ZERO_SOURCE_GOAL_NOT_IDENTICAL")
    options = expand_finite_cyclic_order_zero(goal)
    if len(options) != 1 or options[0].subgoals != (source_relation,):
        raise RuntimeError("R4R5_ORDER_ZERO_RULE_EXPANSION_FAILED")
    matches = find_inference_matches_for_rule(options[0].rule, (adopted_step,))
    if len(matches) != 1:
        raise RuntimeError("R4R5_ORDER_ZERO_RULE_MATCH_FAILED")
    step = apply_inference_match(matches[0])
    if (step.rule is not ProofRule.INFERENCE or step.conclusion != goal
            or step.premises != (adopted_step,)):
        raise RuntimeError("R4R5_ORDER_ZERO_PROOF_STEP_INVALID")

    return {
        "prior_group": "pi_8^7",
        "prior_status": "ADOPTED_DATABASE_PRIOR",
        "prior_rechecked_against_explicit_csv": True,
        "prior_order_checked_against_pi95": True,
        "prior_proof_search_executed": False,
        "prior_proof_tree_reconstructed": False,
        "source_goal": repr(source_relation),
        "target_is_unproved_goal": True,
        "derived_statement": repr(goal),
        "derived_rule": step.inference_rule.name,
        "derived_rule_proof_step": True,
        "derived_step_has_authenticated_db_premise": step.premises[0] is adopted_step,
        "adopted_db_prior_step_count": 1,
        "new_literature_given": 0,
        "registered_in_public": False,
    }


def direct_sum_prior_and_isolated_zero() -> dict[str, object]:
    """Use the earlier pi_8^4 *direct sum* without replaying its proof.

    Each component generator is independently tested against the same rule.
    Its DB prior is authenticated once using the existing strict order gate.
    This is an isolated rule application, NOT a public proof-tree insertion.
    """
    from expression import Multiple, Zero
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
    from phase169_r10e4_ordered_db_prior.db_prior import (
        admitted_db_step, exact_prior_database_result, precedes_db_goal,
        verified_db_step,
    )
    from proof import (
        ProofRule, Relation, RelationType, apply_inference_match,
        find_inference_matches_for_rule,
    )

    source_relation = exact_prior_database_result(4, 4)
    target_relation = exact_prior_database_result(5, 4)
    if (not isinstance(source_relation, Relation)
            or source_relation.relation_type is not RelationType.EQUALITY
            or source_relation.lhs != TodaPrimaryGroup(8, 4)
            or not isinstance(source_relation.rhs, DirectSumGroup)
            or len(source_relation.rhs.summands) != 2
            or not all(isinstance(s, FiniteCyclicGroup)
                       and type(s.order) is int and s.order == 2
                       for s in source_relation.rhs.summands)):
        raise RuntimeError("R4R5_PI84_DIRECT_SUM_DB_PRIOR_MISSING")
    if (not isinstance(target_relation, Relation)
            or target_relation.relation_type is not RelationType.EQUALITY
            or target_relation.lhs != TodaPrimaryGroup(9, 5)
            or not precedes_db_goal(4, 4, 5, 4)):
        raise RuntimeError("R4R5_PI84_PRIOR_ORDER_OR_TARGET_INVALID")

    prior_step = admitted_db_step(source_relation, proof_target=target_relation)
    if (prior_step is None or prior_step.rule is not ProofRule.GIVEN
            or prior_step.premises
            or prior_step.conclusion != source_relation
            or not verified_db_step(prior_step, proof_target=target_relation)):
        raise RuntimeError("R4R5_PI84_DB_PRIOR_AUTHENTICATION_FAILED")

    derivations: list[dict[str, object]] = []
    for summand in source_relation.rhs.summands:
        if typed_endpoints(summand.generator) != (8, 4):
            raise RuntimeError("R4R5_PI84_GENERATOR_ENDPOINTS_INVALID")
        goal = Relation(
            Multiple(summand.order, summand.generator), Zero(),
            RelationType.EQUALITY,
        )
        if order_zero_premise(goal, source_relation) != source_relation:
            raise RuntimeError("R4R5_DIRECT_SUM_MEMBERSHIP_NOT_VERIFIED")
        proposals = expand_finite_cyclic_order_zero(goal, (source_relation,))
        if len(proposals) != 1 or proposals[0].subgoals != (source_relation,):
            raise RuntimeError("R4R5_DIRECT_SUM_RULE_EXPANSION_FAILED")
        matches = find_inference_matches_for_rule(proposals[0].rule, (prior_step,))
        if len(matches) != 1:
            raise RuntimeError("R4R5_DIRECT_SUM_RULE_MATCH_FAILED")
        result = apply_inference_match(matches[0])
        if (result.rule is not ProofRule.INFERENCE
                or result.conclusion != goal
                or result.premises != (prior_step,)):
            raise RuntimeError("R4R5_DIRECT_SUM_PROOF_STEP_INVALID")
        derivations.append({
            "generator": repr(summand.generator),
            "order": summand.order,
            "zero_relation": repr(result.conclusion),
            "inference_rule": result.inference_rule.name,
            "authenticated_prior_parent": result.premises[0] is prior_step,
        })

    if len(derivations) != 2 or len({item["generator"] for item in derivations}) != 2:
        raise RuntimeError("R4R5_PI84_TWO_DISTINCT_SUMMANDS_NOT_ESTABLISHED")
    return {
        "prior_group": "pi_8^4",
        "prior_status": "ADOPTED_DATABASE_PRIOR",
        "prior_rechecked_against_explicit_csv": True,
        "prior_order_checked_against_pi95": True,
        "prior_proof_search_executed": False,
        "prior_proof_tree_reconstructed": False,
        "summands_verified_in_isolation": 2,
        "inferred_zero_steps": len(derivations),
        "summand_derivations": derivations,
        "new_literature_given": 0,
        "registered_in_public": False,
    }


def output_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    dest = base / "EHPProofTracerAudit" / PACKAGE / stamp
    dest.mkdir(parents=True, exist_ok=False)
    return dest


def run(root: Path, dry_run: bool, prior_path: Path | None = None) -> int:
    output = output_folder()
    data: dict[str, object] = {
        "phase": "175-R4R5R2", "revision": "R2",
        "mode": "ISOLATED_ORDERED_DB_PRIOR_FINITE_DIRECT_SUM_ORDER_TO_ZERO",
        "dry_run": dry_run, "gate": "FAIL_R4R5_ETA7_ORDER_ZERO",
        "production_changes": [], "new_given": 0, "new_mathematical_rules": 1,
        "rule_connected_to_public": False, "pi95_proof_complete": False,
        "full_pytest_executed": False,
    }
    try:
        pre = preflight(root)
        data["preflight"] = pre
        prior_file = latest_prior_report(prior_path)
        data["prior_report_path"] = str(prior_file)
        old = validate_prior_report(json.loads(prior_file.read_text(encoding="utf-8")))
        data["prior_report_evidence"] = old
        data["lineage_paths"] = validate_prior_lineage(root, old["prior_head"], pre["head"])
        data["extra_source_pins"] = verify_source_pins(root)
        data["proposition25_status"] = "CITED_BUT_NOT_CONNECTED_BY_R4R5"
        data["toda58_status"] = "CITED_BUT_NOT_CONNECTED_BY_R4R5"
        if not dry_run:
            data["eta7"] = eta7_prior_and_isolated_zero()
            data["direct_sum"] = direct_sum_prior_and_isolated_zero()
        else:
            data["eta7"] = {"status": "NOT_READ_IN_DRYRUN", "prior_proof_search_executed": False}
            data["direct_sum"] = {"status": "NOT_READ_IN_DRYRUN", "prior_proof_search_executed": False}
        data["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        data["error"] = f"{type(exc).__name__}: {exc}"
        data["traceback"] = traceback.format_exc()[-6000:]
    (output / "report.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    lines = [
        "# Phase 175 R4R5R2 — 巡回直和成分の位数から零関係の推論監査", "",
        "Gate: `" + str(data["gate"]) + "`", "",
        "π₈⁷・π₈⁴ の認証済み先行 DB 結果から、各有限巡回成分の位数倍が0となる規則を隔離適用。",
        "先行群の完成証明の再探索は行わない。",
        "Proposition 2.5 と (5.8) の接続は次段階、π₉⁵ の公開証明は未完成。", "",
        "η₇ の実証: `" + str(data.get("eta7", {})) + "`", "",
        "直和成分の実証: `" + str(data.get("direct_sum", {})) + "`", "",
    ]
    (output / "report.md").write_text("\n".join(lines), encoding="utf-8")
    print("PHASE175_R4R5_HEAD=" + str(data.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R5_PINNED_R4_SOURCES=" + str(data.get("preflight", {}).get("pinned_source_count", 0)))
    print("PHASE175_R4R5_ADDITIONAL_SOURCE_PINS=" + str(len(data.get("extra_source_pins", {}))))
    print("PHASE175_R4R5_NEW_GIVEN=0")
    print("PHASE175_R4R5_NEW_GENERAL_RULES=1")
    print("PHASE175_R4R5_PUBLIC_PROOF=NOT_COMPLETE")
    print("PHASE175_R4R5_FULL_PYTEST=NOT_RUN")
    eta = data.get("eta7", {})
    print("PHASE175_R4R5_PI87_PRIOR=" + str(eta.get("prior_status", eta.get("status", "UNVERIFIED"))))
    print("PHASE175_R4R5_PI87_PROOF_SEARCH_EXECUTED=" + str(eta.get("prior_proof_search_executed", False)))
    print("PHASE175_R4R5_2ETA7_ZERO_STEP=" + str(eta.get("derived_rule_proof_step", False)))
    direct_sum = data.get("direct_sum", {})
    print("PHASE175_R4R5_DIRECT_SUM_ZERO_STEPS=" + str(direct_sum.get("inferred_zero_steps", 0)))
    print("PHASE175_R4R5R2_DIRECT_SUM_ZERO_STEPS=" + str(direct_sum.get("inferred_zero_steps", 0)))
    print("PHASE175_R4R5_PI84_PROOF_SEARCH_EXECUTED=" + str(direct_sum.get("prior_proof_search_executed", False)))
    print("PHASE175_R4R5_REPORT=" + str(output / "report.json"))
    print("PHASE175_R4R5_GATE=" + str(data["gate"]))
    print("PHASE175_R4R5R2_GATE=" + str(data["gate"]))
    if "error" in data:
        print("PHASE175_R4R5_ERROR=" + data["error"])
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r4-report", type=Path, default=None)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), args.dry_run, args.r4r4_report)


if __name__ == "__main__":
    sys.exit(main())
```

## `tests/test_rule.py` — 全文

```python
"""Synthetic-premise contracts for the isolated *general* order-to-zero rule.

Test-created ProofSteps are NOT real published or independently verified proofs.
The audit authenticates the earlier pi_8^7 DB row without a proof replay.
"""
from __future__ import annotations

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, Multiple, Zero
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase175_r4r5_eta7_annihilator_isolated.rule import (
    RULE_NAME, expand_finite_cyclic_order_zero, finite_cyclic_order_zero_rule,
    order_zero_premise, typed_endpoints,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)


def eta(n: int) -> HomotopyElement:
    return HomotopyElement(
        name="η_" + str(n), dimension=n, source=n + 1, target=n,
        generator=GeneratorSymbol("η", index=n),
    )


def zero_goal(n: int, m: int = 2) -> Relation:
    return Relation(Multiple(m, eta(n)), Zero(), RelationType.EQUALITY)


def fake_proved_step(relation: Relation) -> ProofStep:
    """A shape-only test fixture: trust is separately checked by the audit."""
    return ProofStep(
        conclusion=relation, premises=(), rule=ProofRule.INFERENCE,
        inference_rule=InferenceRule(name="synthetic test-only prior"),
    )


def test_eta7_typed_order_two_premise() -> None:
    target = zero_goal(7)
    assert typed_endpoints(eta(7)) == (8, 7)
    assert order_zero_premise(target) == Relation(
        TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, eta(7)), RelationType.EQUALITY,
    )
    proposals = expand_finite_cyclic_order_zero(target)
    assert len(proposals) == 1
    assert proposals[0].subgoals == (order_zero_premise(target),)
    assert proposals[0].rule.name == RULE_NAME


@pytest.mark.parametrize("n,m", [(3, 2), (4, 3), (7, 2), (8, 4), (15, 8)])
def test_general_rule_works_outside_eta7(n: int, m: int) -> None:
    target = zero_goal(n, m)
    premise = order_zero_premise(target)
    assert premise is not None
    options = expand_finite_cyclic_order_zero(target)
    assert len(options) == 1
    matches = find_inference_matches_for_rule(
        options[0].rule, (fake_proved_step(premise),),
    )
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == target
    assert step.premises[0].conclusion == premise


def test_rule_rejects_unverified_relation_step_kind() -> None:
    goal = zero_goal(7)
    premise = order_zero_premise(goal)
    assert premise is not None
    fake_relation = ProofStep(premise, (), ProofRule.RELATION)
    rule = finite_cyclic_order_zero_rule(goal)
    assert find_inference_matches_for_rule(rule, (fake_relation,)) == ()
    assert find_inference_matches_for_rule(rule, ()) == ()
    assert find_inference_matches_for_rule(rule, (fake_proved_step(
        Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(4, eta(7))),
    ),)) == ()


@pytest.mark.parametrize("bad", [
    Relation(Multiple(1, eta(7)), Zero()),
    Relation(Multiple(0, eta(7)), Zero()),
    Relation(Multiple(-2, eta(7)), Zero()),
    Relation(Multiple(2, eta(7)), eta(7)),
    Relation(Multiple(2, eta(7)), Zero(), RelationType.ORDER),
    Relation(eta(7), Zero()),
    Relation(Multiple(2, eta(7)), Zero(), source="fabricated citation"),
    Relation(Multiple(2, eta(7)), Zero(), note="unreviewed"),
    Relation(Multiple(True, eta(7)), Zero()),
])
def test_invalid_goal_never_generates_rule(bad: Relation) -> None:
    assert expand_finite_cyclic_order_zero(bad) == ()
    assert order_zero_premise(bad) is None
    with pytest.raises(ValueError, match="typed finite-order"):
        finite_cyclic_order_zero_rule(bad)


def test_sphere_dimension_mismatch_fails_closed() -> None:
    bogus = HomotopyElement(
        "η_7", dimension=8, source=8, target=7,
        generator=GeneratorSymbol("η", index=7),
    )
    assert typed_endpoints(bogus) is None
    assert expand_finite_cyclic_order_zero(Relation(Multiple(2, bogus), Zero())) == ()
    incomplete = HomotopyElement("g", dimension=7, source=None, target=7)
    assert typed_endpoints(incomplete) is None


def test_composition_endpoint_guard() -> None:
    first = HomotopyElement("f", dimension=4, source=7, target=4)
    second = HomotopyElement("g", dimension=7, source=8, target=7)
    comp = Composition(first, second)
    assert typed_endpoints(comp) == (8, 4)
    assert order_zero_premise(Relation(Multiple(2, comp), Zero())) == Relation(
        TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, comp),
    )
    malformed = Composition(second, first)
    assert typed_endpoints(malformed) is None


def test_source_only_is_never_sufficient_for_verified_parent() -> None:
    goal = zero_goal(7)
    options = expand_finite_cyclic_order_zero(goal)
    assert options[0].subgoals == (order_zero_premise(goal),)
    assert len(options) == 1
    assert options[0].rule.premise_patterns[0].proof_rule is None


def test_each_direct_sum_generator_independently_annihilated() -> None:
    from homotopy_groups import DirectSumGroup, FreeCyclicGroup

    a = HomotopyElement("a", 4, source=8, target=4)
    b = HomotopyElement("b", 4, source=8, target=4)
    c = HomotopyElement("c", 4, source=8, target=4)
    group = TodaPrimaryGroup(8, 4)
    presentation = Relation(
        group,
        DirectSumGroup((FreeCyclicGroup(c), FiniteCyclicGroup(2, a),
                        FiniteCyclicGroup(4, b))),
    )
    for m, gen in ((2, a), (4, b)):
        goal = Relation(Multiple(m, gen), Zero())
        assert order_zero_premise(goal, presentation) == presentation
        proposals = expand_finite_cyclic_order_zero(goal, (presentation,))
        assert len(proposals) == 1
        assert proposals[0].subgoals == (presentation,)
        matches = find_inference_matches_for_rule(
            proposals[0].rule, (fake_proved_step(presentation),),
        )
        assert len(matches) == 1
        step = apply_inference_match(matches[0])
        assert step.conclusion == goal
        assert step.premises[0].conclusion == presentation
    assert order_zero_premise(Relation(Multiple(2, c), Zero()), presentation) is None
    assert expand_finite_cyclic_order_zero(
        Relation(Multiple(2, c), Zero()), (presentation,),
    ) == ()


def test_nested_direct_sum_and_duplicate_candidates() -> None:
    from homotopy_groups import DirectSumGroup, FreeCyclicGroup
    a = HomotopyElement("a", 5, source=9, target=5)
    b = HomotopyElement("b", 5, source=9, target=5)
    presentation = Relation(TodaPrimaryGroup(9, 5), DirectSumGroup((
        FreeCyclicGroup(a), DirectSumGroup((FiniteCyclicGroup(8, b),)),
    )))
    goal = Relation(Multiple(8, b), Zero())
    assert order_zero_premise(goal, presentation) == presentation
    options = expand_finite_cyclic_order_zero(goal, (presentation, presentation))
    assert len(options) == 1
    assert options[0].subgoals == (presentation,)


@pytest.mark.parametrize("invalid", [
    "wrong_order", "wrong_generator", "wrong_group", "not_in_direct_sum",
    "wrong_relation", "zero_order", "trivial_order",
])
def test_direct_sum_source_fail_closed(invalid: str) -> None:
    from homotopy_groups import DirectSumGroup, FreeCyclicGroup
    a = HomotopyElement("a", 4, source=8, target=4)
    b = HomotopyElement("b", 4, source=8, target=4)
    goal = Relation(Multiple(2, a), Zero())
    if invalid == "wrong_order":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(4, a),)))
    elif invalid == "wrong_generator":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, b),)))
    elif invalid == "wrong_group":
        source = Relation(TodaPrimaryGroup(9, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)))
    elif invalid == "not_in_direct_sum":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FreeCyclicGroup(a),)))
    elif invalid == "wrong_relation":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)), RelationType.ORDER)
    elif invalid == "zero_order":
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(0, a),)))
    else:
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(1, a),)))
    assert order_zero_premise(goal, source) is None
    assert expand_finite_cyclic_order_zero(goal, (source,)) == ()
    with pytest.raises(ValueError, match="finite-cyclic summand"):
        finite_cyclic_order_zero_rule(goal, source)


def test_source_first_candidates_are_not_self_certifying() -> None:
    from homotopy_groups import DirectSumGroup
    a = HomotopyElement("a", 4, source=8, target=4)
    presentation = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)))
    goal = Relation(Multiple(2, a), Zero())
    proposals = expand_finite_cyclic_order_zero(goal, (presentation,))
    assert len(proposals) == 1
    assert proposals[0].subgoals == (presentation,)
    assert find_inference_matches_for_rule(proposals[0].rule, ()) == ()
    unproved_relation = ProofStep(presentation, (), ProofRule.RELATION)
    assert find_inference_matches_for_rule(proposals[0].rule, (unproved_relation,)) == ()
    incorrect_step = fake_proved_step(Relation(
        TodaPrimaryGroup(8, 4), FiniteCyclicGroup(2, a),
    ))
    assert find_inference_matches_for_rule(proposals[0].rule, (incorrect_step,)) == ()
    with pytest.raises(TypeError, match="tuple"):
        expand_finite_cyclic_order_zero(goal, [presentation])


def test_iterated_suspension_and_composition_endpoints_for_real_shape() -> None:
    from expression import IteratedSuspension, Suspension, Sum
    nu_prime = HomotopyElement("nu-prime", 3, source=6, target=3)
    eta7 = HomotopyElement("eta7", 7, source=8, target=7)
    first = IteratedSuspension(nu_prime, 1)
    assert typed_endpoints(first) == (7, 4)
    assert typed_endpoints(Suspension(nu_prime)) == (7, 4)
    assert typed_endpoints(Composition(first, eta7)) == (8, 4)
    assert typed_endpoints(IteratedSuspension(nu_prime, -1)) is None
    assert typed_endpoints(IteratedSuspension(nu_prime, True)) is None
    assert typed_endpoints(Sum(first, first)) == (7, 4)
    assert typed_endpoints(Sum(first, eta7)) is None
    assert typed_endpoints(Multiple(2, first)) == (7, 4)


def test_direct_sum_candidate_requires_exact_ambient_endpoints() -> None:
    from homotopy_groups import DirectSumGroup
    gen = HomotopyElement("g", 4, source=8, target=4)
    another = HomotopyElement("g", 5, source=9, target=5)
    source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, gen),)))
    assert order_zero_premise(Relation(Multiple(2, another), Zero()), source) is None
    assert order_zero_premise(Relation(Multiple(4, gen), Zero()), source) is None
    assert order_zero_premise(Relation(Multiple(2, gen), Zero()), source) == source


def test_zero_relation_type_is_supported_as_a_general_zero_goal() -> None:
    from homotopy_groups import DirectSumGroup
    a = HomotopyElement("a", 4, source=8, target=4)
    presentation = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, a),)))
    goal = Relation(Multiple(2, a), Zero(), RelationType.ZERO)
    proposals = expand_finite_cyclic_order_zero(goal, (presentation,))
    assert len(proposals) == 1
    matches = find_inference_matches_for_rule(
        proposals[0].rule, (fake_proved_step(presentation),),
    )
    assert len(matches) == 1
    assert apply_inference_match(matches[0]).conclusion == goal
```

## `tests/test_audit.py` — 全文

```python
"""Focused fail-closed R4R5 lineage, prior-evidence and source guard tests."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import sys
from types import ModuleType

import pytest

from phase175_r4r5_eta7_annihilator_isolated import audit


def prior_fixture() -> dict[str, object]:
    return {
        "phase": "175-R4R4",
        "mode": "SOURCE_FIRST_PREMISE_FRONTIER_AUDIT",
        "gate": audit.PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "public_proof_complete": False,
        "full_pytest_executed": False,
        "preflight": {"head": audit.EXPECTED_PRIOR_HEAD, "pinned_source_count": 18},
        "premise_count": 6,
        "verified_parent_steps_replayed_here": 0,
        "premises": [
            {"index": n, "verified_parent_step_in_r4r4": False}
            for n in range(1, 7)
        ],
    }


def test_prior_real_gate_is_not_a_proof_certificate() -> None:
    found = audit.validate_prior_report(prior_fixture())
    assert found["prior_head"] == audit.EXPECTED_PRIOR_HEAD
    assert found["premises"] == 6
    assert found["prior_audit_is_not_a_proof"] is True


@pytest.mark.parametrize("key,value", [
    ("phase", "175-R4R3"),
    ("gate", audit.DRY_GATE),
    ("dry_run", True),
    ("new_given", 1),
    ("new_mathematical_rules", 1),
    ("production_changes", ["proof.py"]),
    ("rule_connected_to_public", True),
    ("public_proof_complete", True),
    ("full_pytest_executed", True),
    ("premise_count", 5),
])
def test_prior_scope_rejects_changed_fields(key: str, value: object) -> None:
    record = prior_fixture()
    record[key] = value
    with pytest.raises(RuntimeError, match="PRIOR_GATE_OR_SCOPE_INVALID"):
        audit.validate_prior_report(record)


@pytest.mark.parametrize("target,value", [
    ("head", "f" * 40),
    ("pinned_source_count", 17),
])
def test_prior_head_and_pins_rejected(target: str, value: object) -> None:
    record = prior_fixture()
    record["preflight"][target] = value
    with pytest.raises(RuntimeError, match="PRIOR_HEAD_OR_SOURCE_INVALID"):
        audit.validate_prior_report(record)


def test_prior_premises_must_not_be_marked_proved() -> None:
    record = prior_fixture()
    record["premises"][2]["verified_parent_step_in_r4r4"] = True
    with pytest.raises(RuntimeError, match="PRIOR_PREMISE_FRONTIER_INVALID"):
        audit.validate_prior_report(record)


def test_prior_missing_or_malformed_rows_rejected() -> None:
    record = prior_fixture()
    record["premises"].pop()
    with pytest.raises(RuntimeError, match="PRIOR_PREMISE_FRONTIER_INVALID"):
        audit.validate_prior_report(record)
    record = prior_fixture()
    record["premises"][1] = "bad row"
    with pytest.raises(RuntimeError, match="PRIOR_PREMISE_FRONTIER_INVALID"):
        audit.validate_prior_report(record)


def test_latest_successful_report_only(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    folder = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE
    a, b = folder / "20261117T055000Z", folder / "20261117T055100Z"
    a.mkdir(parents=True)
    b.mkdir(parents=True)
    (a / "report.json").write_text(json.dumps(prior_fixture()), encoding="utf-8")
    rejected = prior_fixture()
    rejected["gate"] = "FAIL_R4R4"
    (b / "report.json").write_text(json.dumps(rejected), encoding="utf-8")
    assert audit.latest_prior_report() == a / "report.json"
    assert audit.latest_prior_report(a / "report.json") == (a / "report.json").resolve()
    with pytest.raises(RuntimeError, match="R4R4_REPORT_MISSING"):
        audit.latest_prior_report(folder / "missing.json")


def test_source_pins_require_exact_committed_blobs(monkeypatch, tmp_path: Path) -> None:
    for name in audit.EXTRA_SOURCE_PINS:
        file = tmp_path / name
        file.parent.mkdir(exist_ok=True, parents=True)
        file.write_text("fixture", encoding="utf-8")

    def good_git(root, *args, allow_failure=False):
        name = args[-1].removeprefix("HEAD:")
        return 0, audit.EXTRA_SOURCE_PINS[name]

    monkeypatch.setattr(audit, "git", good_git)
    monkeypatch.setattr(audit, "verify_code_and_source_pins", lambda root: {})
    assert audit.verify_source_pins(tmp_path) == audit.EXTRA_SOURCE_PINS

    def bad_git(root, *args, allow_failure=False):
        return 0, "f" * 40

    monkeypatch.setattr(audit, "git", bad_git)
    with pytest.raises(RuntimeError, match="SOURCE_PIN_DRIFT"):
        audit.verify_source_pins(tmp_path)


def test_lineage_allow_only_reviewed_r4r4_package(monkeypatch, tmp_path: Path) -> None:
    new = "a" * 40

    def good_git(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, new
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase175_r4r4_pi95_premise_frontier/audit.py"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", good_git)
    assert audit.validate_prior_lineage(tmp_path, audit.EXPECTED_PRIOR_HEAD, new) == [
        "phase175_r4r4_pi95_premise_frontier/audit.py",
    ]


def test_lineage_reject_unrelated_code_change(monkeypatch, tmp_path: Path) -> None:
    new = "a" * 40

    def bad_git(root, *args, allow_failure=False):
        if args == ("rev-parse", "HEAD"):
            return 0, new
        if args[:2] == ("merge-base", "--is-ancestor"):
            return 0, ""
        if args[:2] == ("diff", "--name-only"):
            return 0, "phase165_r52_r9_shared_math.py\nphase175_r4r4_pi95_premise_frontier/audit.py"
        raise AssertionError(args)

    monkeypatch.setattr(audit, "git", bad_git)
    with pytest.raises(RuntimeError, match="UNREVIEWED_LINEAGE_CHANGES"):
        audit.validate_prior_lineage(tmp_path, audit.EXPECTED_PRIOR_HEAD, new)


def test_lineage_rejects_wrong_prior_and_wrong_current(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setattr(audit, "git", lambda root, *args, allow_failure=False: (0, "a" * 40))
    with pytest.raises(RuntimeError, match="UNREVIEWED_PRIOR_HEAD"):
        audit.validate_prior_lineage(tmp_path, "b" * 40, "a" * 40)
    with pytest.raises(RuntimeError, match="HEAD_CHANGED"):
        audit.validate_prior_lineage(tmp_path, audit.EXPECTED_PRIOR_HEAD, "b" * 40)


def test_scope_cannot_silently_claim_pi95_complete() -> None:
    assert audit.FINAL_GATE.endswith("NOT_PUBLIC")
    assert audit.DRY_GATE.endswith("DRYRUN")
    assert audit.PACKAGE == "phase175_r4r5_eta7_annihilator_isolated"
    assert "proof.py" in audit.EXTRA_SOURCE_PINS
    assert len(audit.EXTRA_SOURCE_PINS) == 11


def _install_checked_prior_fixture(monkeypatch, *, source=None, target=None,
                                   order_allowed=True, admitted=True, verified=True):
    """Mock existing ordered DB API only; no actual source proof is fabricated."""
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType

    eta7 = HomotopyElement("η_7", 7, source=8, target=7,
                           generator=GeneratorSymbol("η", index=7))
    nu5eta8 = HomotopyElement("ν5η8", 5, source=9, target=5)
    if source is None:
        source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2, eta7), RelationType.EQUALITY)
    if target is None:
        target = Relation(TodaPrimaryGroup(9, 5), FiniteCyclicGroup(2, nu5eta8), RelationType.EQUALITY)

    calls = []
    parent_name = "phase169_r10e4_ordered_db_prior"
    child_name = parent_name + ".db_prior"
    parent = ModuleType(parent_name)
    parent.__path__ = []
    child = ModuleType(child_name)

    def get_result(n, k):
        calls.append(("read", n, k))
        return {(7, 1): source, (5, 4): target}.get((n, k))

    def precedes(n, k, tn, tk):
        calls.append(("order", n, k, tn, tk))
        return order_allowed

    def admit(statement, *, proof_target):
        calls.append(("admit", statement, proof_target))
        if not admitted:
            return None
        return ProofStep(statement, (), ProofRule.GIVEN,
                         note="ADOPTED_DATABASE_PRIOR; independent reference not asserted",
                         inference_rule=InferenceRule(name="test-only adoption"))

    def check(step, *, proof_target):
        calls.append(("verify", step.conclusion, proof_target))
        return verified

    child.exact_prior_database_result = get_result
    child.precedes_db_goal = precedes
    child.admitted_db_step = admit
    child.verified_db_step = check
    monkeypatch.setitem(sys.modules, parent_name, parent)
    monkeypatch.setitem(sys.modules, child_name, child)
    return calls


def test_reuse_ordered_prior_does_not_replay_proof(monkeypatch) -> None:
    calls = _install_checked_prior_fixture(monkeypatch)
    result = audit.eta7_prior_and_isolated_zero()
    assert result["prior_status"] == "ADOPTED_DATABASE_PRIOR"
    assert result["prior_proof_search_executed"] is False
    assert result["prior_proof_tree_reconstructed"] is False
    assert result["prior_rechecked_against_explicit_csv"] is True
    assert result["derived_rule_proof_step"] is True
    assert result["derived_step_has_authenticated_db_premise"] is True
    assert result["adopted_db_prior_step_count"] == 1
    assert result["new_literature_given"] == 0
    assert result["registered_in_public"] is False
    assert [c[0] for c in calls] == ["read", "read", "order", "admit", "verify"]
    assert calls[0] == ("read", 7, 1)
    assert calls[1] == ("read", 5, 4)


@pytest.mark.parametrize("wrong", ["wrong_order", "wrong_generator", "wrong_group"])
def test_wrong_prior_group_rejected(monkeypatch, wrong: str) -> None:
    from expression import GeneratorSymbol, HomotopyElement
    from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
    from proof import Relation
    eta = HomotopyElement("η_7", 7, source=8, target=7,
                          generator=GeneratorSymbol("η", index=7))
    if wrong == "wrong_order":
        source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(4, eta))
    elif wrong == "wrong_generator":
        source = Relation(TodaPrimaryGroup(8, 7), FiniteCyclicGroup(2,
                          HomotopyElement("η_7", 7, source=8, target=7,
                                          generator=GeneratorSymbol("ν", index=7))))
    else:
        source = Relation(TodaPrimaryGroup(9, 7), FiniteCyclicGroup(2, eta))
    _install_checked_prior_fixture(monkeypatch, source=source)
    with pytest.raises(RuntimeError, match="PI87_DB_PRIOR_UNAVAILABLE_OR_INVALID|PI87_DB_GENERATOR_UNVERIFIED"):
        audit.eta7_prior_and_isolated_zero()


def test_prior_order_rejects_unapproved_reuse(monkeypatch) -> None:
    _install_checked_prior_fixture(monkeypatch, order_allowed=False)
    with pytest.raises(RuntimeError, match="PRIOR_ORDER_DISALLOWED"):
        audit.eta7_prior_and_isolated_zero()


@pytest.mark.parametrize("admitted,verified", [(False, True), (True, False)])
def test_db_prior_requires_existing_authentication(monkeypatch, admitted: bool, verified: bool) -> None:
    _install_checked_prior_fixture(monkeypatch, admitted=admitted, verified=verified)
    with pytest.raises(RuntimeError, match="DB_PRIOR_AUTHENTICATION_FAILED"):
        audit.eta7_prior_and_isolated_zero()


def test_target_is_not_marked_as_proved(monkeypatch) -> None:
    from homotopy_groups import TodaPrimaryGroup
    from proof import Relation
    from expression import Zero
    target = Relation(TodaPrimaryGroup(10, 5), Zero())
    _install_checked_prior_fixture(monkeypatch, target=target)
    with pytest.raises(RuntimeError, match="PI95_DB_TARGET_GOAL_MISSING"):
        audit.eta7_prior_and_isolated_zero()


def test_missing_group_prior_rejected(monkeypatch) -> None:
    _install_checked_prior_fixture(monkeypatch, source=False)
    with pytest.raises(RuntimeError, match="PI87_DB_PRIOR_UNAVAILABLE_OR_INVALID"):
        audit.eta7_prior_and_isolated_zero()


def _install_checked_direct_sum_prior_fixture(
    monkeypatch, *, source=None, target=None, order_allowed=True,
    admitted=True, verified=True,
):
    """Supply test-only ordered DB responses; no real proof is claimed."""
    from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
    from proof import InferenceRule, ProofRule, ProofStep, Relation

    eta7 = HomotopyElement("η_7", 7, source=8, target=7,
                           generator=GeneratorSymbol("η", index=7))
    nu4 = HomotopyElement("ν_4", 4, source=7, target=4,
                          generator=GeneratorSymbol("ν", index=4))
    nuprime = HomotopyElement("ν'", 3, source=6, target=3,
                             generator=GeneratorSymbol("ν'", index=3))
    x = Composition(nu4, eta7)
    y = Composition(IteratedSuspension(nuprime, 1), eta7)
    if source is None:
        source = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((
            FiniteCyclicGroup(2, x), FiniteCyclicGroup(2, y),
        )))
    if target is None:
        target = Relation(TodaPrimaryGroup(9, 5), FiniteCyclicGroup(
            2, HomotopyElement("target", 5, source=9, target=5),
        ))
    calls = []
    parent_name = "phase169_r10e4_ordered_db_prior"
    child_name = parent_name + ".db_prior"
    parent = ModuleType(parent_name)
    parent.__path__ = []
    child = ModuleType(child_name)

    def get_result(n, k):
        calls.append(("read", n, k))
        return {(4, 4): source, (5, 4): target}.get((n, k))

    def precedes(n, k, tn, tk):
        calls.append(("order", n, k, tn, tk))
        return order_allowed

    def admit(statement, *, proof_target):
        calls.append(("admit", statement, proof_target))
        if not admitted:
            return None
        return ProofStep(statement, (), ProofRule.GIVEN,
                         note="ADOPTED_DATABASE_PRIOR; independent reference not asserted",
                         inference_rule=InferenceRule(name="test-only DB adoption"))

    def check(step, *, proof_target):
        calls.append(("verify", step.conclusion, proof_target))
        return verified

    child.exact_prior_database_result = get_result
    child.precedes_db_goal = precedes
    child.admitted_db_step = admit
    child.verified_db_step = check
    monkeypatch.setitem(sys.modules, parent_name, parent)
    monkeypatch.setitem(sys.modules, child_name, child)
    return calls


def test_real_shape_direct_sum_prior_is_reused_without_replay(monkeypatch) -> None:
    calls = _install_checked_direct_sum_prior_fixture(monkeypatch)
    data = audit.direct_sum_prior_and_isolated_zero()
    assert data["prior_group"] == "pi_8^4"
    assert data["prior_status"] == "ADOPTED_DATABASE_PRIOR"
    assert data["prior_proof_search_executed"] is False
    assert data["prior_proof_tree_reconstructed"] is False
    assert data["summands_verified_in_isolation"] == 2
    assert data["inferred_zero_steps"] == 2
    assert all(row["authenticated_prior_parent"] for row in data["summand_derivations"])
    assert all(row["order"] == 2 for row in data["summand_derivations"])
    from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME
    assert all(row["inference_rule"] == RULE_NAME
               for row in data["summand_derivations"])
    assert [item[0] for item in calls] == ["read", "read", "order", "admit", "verify"]
    assert calls[0] == ("read", 4, 4)
    assert calls[1] == ("read", 5, 4)


@pytest.mark.parametrize("order_allowed,admitted,verified", [
    (False, True, True),
    (True, False, True),
    (True, True, False),
])
def test_direct_sum_prior_authentication_fail_closed(monkeypatch, order_allowed, admitted, verified) -> None:
    _install_checked_direct_sum_prior_fixture(
        monkeypatch, order_allowed=order_allowed, admitted=admitted, verified=verified,
    )
    with pytest.raises(RuntimeError, match="PRIOR_ORDER_OR_TARGET_INVALID|DB_PRIOR_AUTHENTICATION_FAILED"):
        audit.direct_sum_prior_and_isolated_zero()


def test_direct_sum_prior_bad_shape_rejected(monkeypatch) -> None:
    from expression import HomotopyElement
    from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, TodaPrimaryGroup
    from proof import Relation
    g = HomotopyElement("g", 4, source=8, target=4)
    wrong = Relation(TodaPrimaryGroup(8, 4), DirectSumGroup((FiniteCyclicGroup(2, g),)))
    _install_checked_direct_sum_prior_fixture(monkeypatch, source=wrong)
    with pytest.raises(RuntimeError, match="PI84_DIRECT_SUM_DB_PRIOR_MISSING"):
        audit.direct_sum_prior_and_isolated_zero()
```

## `run.ps1` — 全文

```powershell
param(
    [switch] $DryRun,
    [string] $R4R4Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'

$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
        phase175_r4r5_eta7_annihilator_isolated/tests/test_rule.py `
        phase175_r4r5_eta7_annihilator_isolated/tests/test_audit.py `
        phase175_r4r4_pi95_premise_frontier/tests/test_audit.py `
        phase175_r4r3_two_summand_quotient/tests/test_rule.py `
        phase175_r4r3_two_summand_quotient/tests/test_audit.py `
        phase175_r4_pi95_audit/tests/test_audit.py

    if ($LASTEXITCODE -ne 0) { throw 'R4R5 focused pytest failed' }
    Write-Output 'PHASE175_R4R5_FOCUSED_PYTEST=PASS'
    Write-Output 'PHASE175_R4R5R2_FOCUSED_PYTEST=PASS'

    $cmd = @('-B', '-m', 'phase175_r4r5_eta7_annihilator_isolated.audit', '--root', $root)
    if ($DryRun) { $cmd += '--dry-run' }
    if ($R4R4Report -ne '') { $cmd += @('--r4r4-report', $R4R4Report) }
    & python @cmd
    $auditExitCode = $LASTEXITCODE
    Write-Output "PHASE175_R4R5_EXIT_CODE=$auditExitCode"
    Write-Output "PHASE175_R4R5R2_EXIT_CODE=$auditExitCode"
    if ($auditExitCode -ne 0) { exit $auditExitCode }
    exit 0
} finally {
    Pop-Location
}
```

## `__init__.py` — 全文

```python
"""Phase 175 R4R5: isolated generic finite-cyclic generator annihilation."""
```
