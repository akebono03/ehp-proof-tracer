# Phase 175 R4R11 — 変更・追加コード全文

## R4R11R1 — ProofStepLink テスト fixture 修正（2026-11-18）

- 変更対象は `tests/test_provider.py` 内の `cited_bridge()` **全体**のみ。`ProofStepLink(aid, step=ProofStep(...))` のキーワード引数 `step=` を明示する。
- テストファイルの import、その他のテスト関数、クラス、既存本番コードには変更なし。
- 下記 `tests/test_provider.py` の節には、修正後の **import および全関数全文**を収録している。
- 互換スタブでの修正版限定 pytest は **94 passed**。2026-11-18 のユーザー実環境では修正前に **4 failed, 124 passed**（本修正版のユーザー環境実行は未確認）。
- 数学規則・GIVEN・既存 API を変更しない。


既存 `phase165_r52_r9_shared_math.py` の変更対象は `shared_expansion_provider()` のみ。import の変更はありません。`installer.py` は変更後の関数全体を AST で生成し、**DryRun 時にも** `%LOCALAPPDATA%\EHPProofTracerAudit\phase175_r4r11_signed_eta_torsion_public\<実行ID>\shared_expansion_provider_FULL_AFTER.py` に全文出力します。同時に `phase165_r52_r9_shared_math_FULL_AFTER.py` に変更後モジュール全文を出力します。具体的な挿入位置は、既存 `build_cited_58_prop25_provider(bridge)` を `extra_providers` に追加した行の直後です。未知の HEAD・Git blob・変更は拒否します。

## 変更一覧

- 既存 `phase165_r52_r9_shared_math.py` / `shared_expansion_provider()`：一関数全体を置換（出力は上記）。
- 新規パッケージ `phase175_r4r11_signed_eta_torsion_public/`：下記の全ファイルを追加。
- 新規 `eta_two_torsion_normalization_inputs()`、`signed_eta_two_torsion_rule()`、`expand_signed_eta_two_torsion()`、`build_signed_eta_torsion_provider()` 等。
- テストは新規4ファイル。既存テスト関数は変更しない。

## `__init__.py` 全文

```python

```

## `rule.py` 全文

```python
"""Source-conditional normalization of a signed Delta image along a 2-torsion suspension.

Let beta = eta_n (n>=3), so beta is a suspension by the cited eta-family
notation.  If 2 beta = 0 and Delta(gamma)=+/-( (2k a - b) o beta ), then
Delta(gamma)=b o beta. The two signs agree because 2(b o beta)=0.

No source fact, order relation, or group result is manufactured here.
"""
from __future__ import annotations

from expression import (
    Composition,
    GeneratorSymbol,
    HomotopyElement,
    MapApplication,
    Multiple,
    Sum,
    Zero,
)
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase165_r3_recursive_search import GoalExpansion
from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaImageUpToSignStatement


RULE_NAME = "signed Delta image normalized by proved eta-family two-torsion"


def eta_two_torsion_normalization_inputs(
    goal: object,
    signed: object,
    two_beta_zero: object,
    definition: object,
) -> tuple[TodaDeltaImageUpToSignStatement, Relation, TodaEtaFamilyGeneralDefinition] | None:
    """Check all typed dimensions and the two independently proved obligations."""
    if (type(goal) is not Relation
            or goal.relation_type is not RelationType.EQUALITY
            or type(goal.lhs) is not MapApplication
            or goal.lhs.map != EHP_DELTA_MAP
            or type(goal.rhs) is not Composition
            or type(signed) is not TodaDeltaImageUpToSignStatement
            or type(signed.positive_value) is not Composition
            or type(signed.positive_value.left) is not Sum
            or type(two_beta_zero) is not Relation
            or two_beta_zero.relation_type is not RelationType.EQUALITY
            or type(two_beta_zero.lhs) is not Multiple
            or type(two_beta_zero.rhs) is not Zero
            or type(definition) is not TodaEtaFamilyGeneralDefinition
            or definition != TodaEtaFamilyGeneralDefinition()):
        return None

    linear = signed.positive_value.left
    beta = signed.positive_value.right
    if (type(linear.left) is not Multiple
            or type(linear.right) is not Multiple
            or type(linear.left.coefficient) is not int
            or linear.left.coefficient % 2 != 0
            or type(linear.right.coefficient) is not int
            or linear.right.coefficient != -1
            or type(beta) is not HomotopyElement
            or type(beta.dimension) is not int
            or type(beta.source) is not int
            or type(beta.target) is not int):
        return None
    n = beta.target
    if (n < 3 or beta.dimension != n or beta.source != n + 1
            or beta.generator != GeneratorSymbol("η", index=n)):
        return None
    # eta_n=E^(n-2) eta_2: n>=3 is a suspension; arbitrary
    # unsuspended two-torsion beta is NOT enough for left distributivity.
    a = linear.left.expression
    b = linear.right.expression
    a_span = typed_endpoints(a)
    b_span = typed_endpoints(b)
    beta_span = typed_endpoints(beta)
    gamma_span = typed_endpoints(signed.element)
    if (a_span is None or a_span != b_span
            or beta_span is None or beta_span[1] != a_span[0]
            or gamma_span is None
            or typed_endpoints(signed.positive_value) != (beta_span[0], a_span[1])
            or signed.map != TodaDeltaMap(
                TodaPrimaryGroup(*gamma_span),
                TodaPrimaryGroup(beta_span[0], a_span[1]),
            )):
        return None
    expected_zero = Relation(Multiple(2, beta), Zero(), RelationType.EQUALITY)
    expected_exact = Relation(
        MapApplication(EHP_DELTA_MAP, signed.element),
        Composition(b, beta),
        RelationType.EQUALITY,
    )
    if two_beta_zero != expected_zero or goal != expected_exact:
        return None
    return signed, two_beta_zero, definition


def signed_eta_two_torsion_rule(
    goal: Relation,
    signed: TodaDeltaImageUpToSignStatement,
    two_beta_zero: Relation,
    definition: TodaEtaFamilyGeneralDefinition,
) -> InferenceRule:
    """Require INFERENCE signed image, INFERENCE order-zero, GIVEN eta definition."""
    required = eta_two_torsion_normalization_inputs(
        goal, signed, two_beta_zero, definition,
    )
    if required is None:
        raise ValueError("not an admissible signed two-torsion Delta normalization")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.INFERENCE
            and premises[2].rule is ProofRule.GIVEN
            and not premises[2].premises
            and tuple(step.conclusion for step in premises) == required
            and eta_two_torsion_normalization_inputs(
                goal, signed, two_beta_zero, definition,
            ) == required
        )

    return InferenceRule(
        name=RULE_NAME,
        description=(
            "For a cited eta_n suspension (n>=3), a proved 2 eta_n=0, "
            "and independently proved signed Delta(gamma)=+/-( (2k a-b)o eta_n ), "
            "left distributivity gives -(b o eta_n) up to sign. "
            "Since 2(b o eta_n)=0, both signs equal +(b o eta_n). "
            "No group structure is inferred and no missing source is assumed."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaDeltaImageUpToSignStatement,
                statement_pattern=required[0],
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=required[1],
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=TodaEtaFamilyGeneralDefinition,
                statement_pattern=required[2],
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_signed_eta_two_torsion(
    goal: object,
    candidates: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose only against independently source-discovered signed candidates."""
    if not isinstance(candidates, tuple):
        raise TypeError("candidates must be a tuple")
    if not isinstance(goal, Relation):
        return ()
    definition = TodaEtaFamilyGeneralDefinition()
    if (not isinstance(goal.rhs, Composition)
            or not isinstance(goal.rhs.right, HomotopyElement)):
        return ()
    beta = goal.rhs.right
    order_zero = Relation(Multiple(2, beta), Zero(), RelationType.EQUALITY)
    options = []
    for signed in candidates:
        if not isinstance(signed, TodaDeltaImageUpToSignStatement):
            continue
        required = eta_two_torsion_normalization_inputs(
            goal, signed, order_zero, definition,
        )
        if required is None or required in (x.subgoals for x in options):
            continue
        options.append(GoalExpansion(
            signed_eta_two_torsion_rule(goal, signed, order_zero, definition),
            required,
        ))
    return tuple(options)
```

## `provider.py` 全文

```python
"""Source-first shared provider for the generic signed eta-torsion normalization.

A cited (5.8) source generates only a possible intermediate signed target.
Its R4R10 / Proposition 2.5 ProofStep, eta-family definition, and the actual
order-zero ProofStep remain mandatory search goals.
"""
from __future__ import annotations

from expression import Composition, HomotopyElement, MapApplication
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase175_r4r10_cited_58_prop25_public.provider import screened_cited_facts
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta, canonical_toda58,
)
from phase175_r4r11_signed_eta_torsion_public.rule import (
    expand_signed_eta_two_torsion,
)
from proof import Relation
from toda_rules import TodaDeltaImageUpToSignStatement


def build_signed_eta_torsion_provider(bridge: RegistryBridgeResult):
    """Build only legitimate backward proposals from an exact screened source."""
    available = screened_cited_facts(bridge)
    pinned = canonical_toda58()
    candidates = tuple(
        claim.statement for claim in available
        if type(claim) is CitedToda58SignedDelta
        and claim.locator == "(5.8)"
        and claim.statement == pinned
    )

    def expand(goal: object):
        if (not isinstance(goal, Relation)
                or not isinstance(goal.lhs, MapApplication)
                or not isinstance(goal.rhs, Composition)
                or not isinstance(goal.rhs.right, HomotopyElement)
                or not isinstance(goal.lhs.expression, HomotopyElement)):
            return ()
        beta = goal.rhs.right
        gamma = goal.lhs.expression
        proposals = []
        for source in candidates:
            source_value = source.positive_value
            if source_value is None:
                continue
            signed = TodaDeltaImageUpToSignStatement(
                map=TodaDeltaMap(
                    TodaPrimaryGroup(gamma.source, gamma.target),
                    TodaPrimaryGroup(beta.source, source_value.left.expression.target),
                ),
                element=gamma,
                positive_value=Composition(source_value, beta),
            )
            proposals.append(signed)
        return expand_signed_eta_two_torsion(goal, tuple(proposals))

    return expand
```

## `installer.py` 全文

```python
"""Pinned full-function installation of the R4R11 shared inference provider.

Only shared_expansion_provider() is modified. The full replacement is
always exported for review, even on DryRun. No module import changes.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path("phase165_r52_r9_shared_math.py")
BASE_WORKING_BLOB = "900d670dff839d484d14dccb37fb79471b39902e"
REVIEWED_COMMITTED_BLOBS = (
    "df4e0f834e9bc321f338ec10b363c79d82623457",
    BASE_WORKING_BLOB,
)
FUNCTION = "shared_expansion_provider"
ANCHOR = '''    extra_providers = (build_cited_58_prop25_provider(bridge),) + tuple(extra_providers)
'''
ADDITION = '''    # Phase 175 R4R11: signed two-torsion normalization is conditional.
    # It requires verified Prop 2.5, order-two and eta-family premises.
    from phase175_r4r11_signed_eta_torsion_public.provider import (
        build_signed_eta_torsion_provider,
    )
    extra_providers = (build_signed_eta_torsion_provider(bridge),) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        encoding="utf-8", errors="replace", text=True, check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R11_GIT_ERROR: " + " ".join(args) + ": " + result.stderr)
    return result.stdout.strip()


def git_blob_sha(value: bytes) -> str:
    return sha1(b"blob " + str(len(value)).encode("ascii") + b"\x00" + value).hexdigest()


def function_replacement(original: str) -> tuple[str, str, str]:
    """Return whole module and full function, refusing unreviewed text."""
    syntax = ast.parse(original)
    functions = [node for node in syntax.body if isinstance(node, ast.FunctionDef)
                 and node.name == FUNCTION]
    if len(functions) != 1:
        raise RuntimeError("R4R11_FUNCTION_NOT_UNIQUE")
    fn = functions[0]
    lines = original.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if before.count(ANCHOR) != 1:
        raise RuntimeError("R4R11_ANCHOR_CHANGED")
    if before.count(ADDITION) > 1:
        raise RuntimeError("R4R11_DUPLICATED_INSERTION")
    original_without_addition = original
    if ADDITION in before:
        original_without_addition = original.replace(ADDITION, "", 1)
    if git_blob_sha(original_without_addition.encode("utf-8")) != BASE_WORKING_BLOB:
        raise RuntimeError("R4R11_UNREVIEWED_BASE_SOURCE")
    after_function = before if ADDITION in before else before.replace(
        ANCHOR, ANCHOR + ADDITION, 1,
    )
    updated = "".join(lines[:fn.lineno - 1]) + after_function + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    return updated, after_function, original_without_addition


def plan(root: Path) -> tuple[Path, bytes, bytes, str]:
    """Work with both reviewed R4R10 HEADs and LF/CRLF checkouts."""
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R4R11_PRODUCTION_FILE_MISSING")
    committed = git(root, "rev-parse", "HEAD:" + TARGET.as_posix())
    if committed not in REVIEWED_COMMITTED_BLOBS:
        raise RuntimeError("R4R11_UNREVIEWED_COMMITTED_PRODUCTION")
    current = path.read_bytes()
    normalized = current.replace(b"\r\n", b"\n").decode("utf-8")
    new_content, whole_function, _ = function_replacement(normalized)
    eol = b"\r\n" if b"\r\n" in current else b"\n"
    new_data = new_content.encode("utf-8")
    if eol == b"\r\n":
        new_data = new_data.replace(b"\n", b"\r\n")
    return path, current, new_data, whole_function


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    path, before, after, full_function = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "shared_expansion_provider_FULL_AFTER.py").write_text(
        full_function, encoding="utf-8",
    )
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    if before != after and not dry_run:
        descriptor, temp = tempfile.mkstemp(prefix="r4r11_", suffix=".py", dir=path.parent)
        try:
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(after)
            os.replace(temp, path)
        finally:
            if os.path.exists(temp):
                os.unlink(temp)
    return {
        "production_path": TARGET.as_posix(),
        "patch_required": before != after,
        "patch_applied": before != after and not dry_run,
        "after_git_blob": git_blob_sha(after.replace(b"\r\n", b"\n")),
        "full_function_exported": True,
    }
```

## `audit.py` 全文

```python
"""Phase 175 R4R11: source-first signed Delta / proved eta order-two normalization.

The phase adds one general inference, not a new mathematical source/GIVEN.
A group query for pi_9^5 is not claimed complete by this phase.
"""
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

from phase175_r4r11_signed_eta_torsion_public import installer

PACKAGE = "phase175_r4r11_signed_eta_torsion_public"
PRIOR_PACKAGE = "phase175_r4r10_cited_58_prop25_public"
PRIOR_GATE = "PASS_R4R10_CITED_58_PROP25_SHARED_CONNECTED_PI95_PENDING"
DRY_GATE = "PASS_R4R11_SIGNED_ETA_TORSION_DRYRUN"
FINAL_GATE = "PASS_R4R11_SIGNED_ETA_TORSION_SHARED_CONNECTED_PI95_PENDING"
BASE_HEAD = "5c263cc69dc409842d3a13cb3fc65c2347df0bef"
REVIEWED_R4R10_HEAD = "abf619040d52aa9fd61c5bca60db81e28912e24d"
PINNED_WORKING_BLOBS = {
    "phase175_r4r10_cited_58_prop25_public/source.py": "b5162bdaac25e4578973816290207379734229f6",
    "phase175_r4r10_cited_58_prop25_public/provider.py": "be1d726fe98c0258685674ea41099aab1103f318",
    "phase175_r4r10_cited_58_prop25_public/audit.py": "4a60304020bfde1d28639eff9deb72c0e00d6b57",
    "phase175_r4r7_prop25_typed_composition/rule.py": "e957752baf93f75352d106e53205730af9a02b4d",
    "phase175_r4r5_eta7_annihilator_isolated/rule.py": "13fcf56001d2b03283acf2b921d639a01f4d89c3",
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(root: Path, *args: str, allow_failure: bool = False) -> tuple[int, str]:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        encoding="utf-8", errors="replace", text=True, check=False,
    )
    if result.returncode and not allow_failure:
        raise RuntimeError("R4R11_GIT_FAILED: " + " ".join(args) + ": " + result.stderr)
    return result.returncode, result.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R11_WRONG_REPO_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R11_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    if head not in (BASE_HEAD, REVIEWED_R4R10_HEAD):
        raise RuntimeError("R4R11_UNREVIEWED_HEAD: " + head)
    if head == REVIEWED_R4R10_HEAD:
        code, _ = git(root, "merge-base", "--is-ancestor", BASE_HEAD, head,
                      allow_failure=True)
        if code != 0:
            raise RuntimeError("R4R11_REVIEWED_LINEAGE_NOT_ANCESTOR")
        changed = git(root, "diff", "--name-only", BASE_HEAD, head)[1].splitlines()
        if any(not (name == installer.TARGET.as_posix()
                    or name.startswith(PRIOR_PACKAGE + "/")) for name in changed):
            raise RuntimeError("R4R11_UNREVIEWED_INTERVENING_COMMIT")
    dirty = sorted(set(
        git(root, "diff", "--name-only")[1].splitlines()
        + git(root, "diff", "--cached", "--name-only")[1].splitlines()
    ))
    if any(item not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for item in dirty):
        raise RuntimeError("R4R11_UNREVIEWED_TRACKED_CHANGE: " + repr(dirty))
    # plan() fail-closes against arbitrary edits to shared production source,
    # and verifies the whole-function, idempotent patch, not merely a marker.
    plan_path, before, after, _ = installer.plan(root)
    if plan_path != root / installer.TARGET:
        raise RuntimeError("R4R11_WRONG_TARGET_PATH")
    for path, expected in PINNED_WORKING_BLOBS.items():
        file = root / path
        if not file.is_file():
            raise RuntimeError("R4R11_SOURCE_MISSING: " + path)
        actual = installer.git_blob_sha(file.read_bytes().replace(b"\r\n", b"\n"))
        if actual != expected:
            raise RuntimeError("R4R11_SOURCE_DRIFT: " + path)
    return {
        "head": head,
        "reviewed_base_head": BASE_HEAD,
        "reviewed_successor_head": REVIEWED_R4R10_HEAD,
        "pinned_blobs": len(PINNED_WORKING_BLOBS),
        "production_patch_required": before != after,
        "production_after_blob": installer.git_blob_sha(after.replace(b"\r\n", b"\n")),
        "dirty_tracked_paths": dirty,
    }


def validate_prior(report: object) -> dict[str, object]:
    if not isinstance(report, dict):
        raise RuntimeError("R4R11_R4R10_REPORT_INVALID")
    expected = {
        "phase": "175-R4R10",
        "dry_run": False,
        "gate": PRIOR_GATE,
        "new_given": 2,
        "new_mathematical_rules": 0,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    if any(report.get(key) != value for key, value in expected.items()):
        raise RuntimeError("R4R11_R4R10_GATE_OR_SCOPE_CHANGED")
    pre = report.get("preflight")
    replay = report.get("delta_composition_replay")
    public = report.get("public")
    installed = report.get("install")
    if (not isinstance(pre, dict) or pre.get("head") != BASE_HEAD
            or not isinstance(replay, dict)
            or not isinstance(public, dict)
            or not isinstance(installed, dict)
            or any(replay.get(key) is not True for key in (
                "conclusion_is_signed", "proposition_2_5_citation_present",
                "equation_5_8_citation_present", "eta_family_citation_present",
                "signed_parent_inferred", "composition_identity_parent_inferred",
            ))
            or replay.get("root_group_conclusion_inferred") is not False
            or public.get("public_prop25_candidate_found") is not True
            or public.get("public_signed_parent_candidate_found") is not True
            or public.get("public_identity_parent_candidate_found") is not True
            or public.get("public_root_pi95_proof_complete") is not False
            or installed.get("production_path") != installer.TARGET.as_posix()
            or installed.get("two_full_functions_exported") is not True
            or not isinstance(installed.get("after_git_blob"), str)
            or len(installed["after_git_blob"]) != 40):
        raise RuntimeError("R4R11_R4R10_EVIDENCE_INVALID")
    return {
        "successful_prior": True,
        "prior_head": pre["head"],
        "source_5_8_and_prop25_shared": True,
        "pi95_not_yet_complete": True,
    }


def find_prior(explicit: Path | None) -> Path:
    if explicit is not None:
        result = explicit.expanduser().resolve()
        if not result.is_file():
            raise RuntimeError("R4R11_PRIOR_REPORT_MISSING: " + str(result))
        return result
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    rejected = []
    for path in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(path.read_text(encoding="utf-8")))
            return path
        except (OSError, ValueError, UnicodeError, RuntimeError) as exc:
            rejected.append(str(path) + ": " + str(exc))
    raise RuntimeError("R4R11_SUCCESSFUL_R4R10_REPORT_NOT_FOUND: " + str(folder)
                       + "; " + " | ".join(rejected[:3]))


def exact_delta_eta9_goal():
    from expression import Composition, MapApplication
    from map_facts import EHP_DELTA_MAP
    from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
    from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
    from proof import Relation
    signed = sample_delta_eta9()
    source = canonical_toda58()
    return Relation(
        MapApplication(EHP_DELTA_MAP, signed.element),
        Composition(source.positive_value.right.expression,
                    signed.positive_value.right),
    )


def replay_general_rule() -> dict[str, object]:
    """Replay the three mandatory premises; no theorem-specific proof leaf."""
    from expression import Multiple, Zero
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
    from phase175_r4r11_signed_eta_torsion_public.rule import signed_eta_two_torsion_rule
    from proof import (InferenceRule, ProofRule, ProofStep, Relation,
                       apply_inference_match, find_inference_matches_for_rule)
    goal = exact_delta_eta9_goal()
    signed = sample_delta_eta9()
    beta = signed.positive_value.right
    two_beta_zero = Relation(Multiple(2, beta), Zero())
    definition = TodaEtaFamilyGeneralDefinition()
    rule = signed_eta_two_torsion_rule(goal, signed, two_beta_zero, definition)
    parents = (
        ProofStep(signed, (), ProofRule.INFERENCE,
                  inference_rule=InferenceRule("synthetic signed premise")),
        ProofStep(two_beta_zero, (), ProofRule.INFERENCE,
                  inference_rule=InferenceRule("synthetic order-two premise")),
        ProofStep(definition, (), ProofRule.GIVEN,
                  inference_rule=InferenceRule("synthetic citation premise")),
    )
    # The synthetic fixtures are NOT substituted for real source certificates.
    matches = find_inference_matches_for_rule(rule, parents)
    if len(matches) != 1:
        raise RuntimeError("R4R11_ISOLATED_PROOF_REPLAY_FAILED")
    result = apply_inference_match(matches[0])
    if (result.rule is not ProofRule.INFERENCE
            or result.conclusion != goal
            or result.premises != parents):
        raise RuntimeError("R4R11_DERIVED_RESULT_INVALID")
    if find_inference_matches_for_rule(rule, parents[:2]):
        raise RuntimeError("R4R11_MISSING_CITATION_ACCEPTED")
    return {
        "synthetic_rule_contract_passed": True,
        "real_signed_parent_not_substituted": True,
        "real_order_zero_parent_not_substituted": True,
        "new_group_proof_created": False,
    }


def inspect_shared_connection() -> dict[str, object]:
    """Verify real DB-prior eta7 identity and all shared backward candidate routes.

    DB's generator may use a different Unicode name than a literature
    display label. Never silently equate HomotopyElement names: reconstruct
    the Prop 2.5 instance with the exact, admitted prior generator object.
    """
    from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
    from homotopy_groups import FiniteCyclicGroup, TodaDeltaMap, TodaPrimaryGroup
    from map_facts import EHP_DELTA_MAP
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
    from phase175_r4r10_cited_58_prop25_public.provider import CITED_PROP25_RULE
    from phase175_r4r11_signed_eta_torsion_public.rule import RULE_NAME
    from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
    from phase175_r4r5_eta7_annihilator_isolated.rule import RULE_NAME as ORDER_RULE_NAME
    from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from proof import Relation
    from toda_rules import TodaDeltaImageUpToSignStatement

    bridge = build_shared_typed_bridge()
    root = exact_prior_database_result(5, 4)
    eta_prior = exact_prior_database_result(7, 1)
    if (not isinstance(root, Relation)
            or not isinstance(eta_prior, Relation)
            or eta_prior.lhs != TodaPrimaryGroup(8, 7)
            or not isinstance(eta_prior.rhs, FiniteCyclicGroup)
            or eta_prior.rhs.order != 2):
        raise RuntimeError("R4R11_TYPED_ROOT_OR_ETA7_DB_CONTEXT_NOT_FOUND")
    beta = eta_prior.rhs.generator
    if (not isinstance(beta, HomotopyElement)
            or beta.source != 8 or beta.target != 7 or beta.dimension != 7
            or beta.generator != GeneratorSymbol("η", index=7)):
        raise RuntimeError("R4R11_UNREVIEWED_ETA7_PRIOR_GENERATOR")
    source = canonical_toda58()
    gamma = sample_delta_eta9().element
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(source.positive_value, beta),
    )
    exact = Relation(
        MapApplication(EHP_DELTA_MAP, gamma),
        Composition(source.positive_value.right.expression, beta),
    )
    provider = shared_expansion_provider(bridge, proof_target=root)
    delta_options = tuple(item for item in provider(signed)
                          if item.rule.name == CITED_PROP25_RULE)
    if len(delta_options) != 1:
        raise RuntimeError("R4R11_R4R10_SIGNED_ROUTE_NOT_FOUND")
    exact_options = tuple(item for item in provider(exact)
                          if item.rule.name == RULE_NAME)
    if len(exact_options) != 1 or len(exact_options[0].subgoals) != 3:
        raise RuntimeError("R4R11_SHARED_NORMALIZATION_NOT_FOUND")
    child_signed, order, definition = exact_options[0].subgoals
    if (child_signed != signed
            or definition != TodaEtaFamilyGeneralDefinition()
            or child_signed.positive_value != signed.positive_value
            or source.positive_value.right.coefficient != -1):
        raise RuntimeError("R4R11_PUBLIC_PREMISES_CHANGED")
    order_options = tuple(item for item in provider(order)
                          if item.rule.name == ORDER_RULE_NAME)
    if not order_options or any(option.subgoals != (eta_prior,) for option in order_options):
        raise RuntimeError("R4R11_PUBLIC_ORDER_TWO_ROUTE_NOT_FOUND")
    return {
        "r4r10_signed_delta_route_present": True,
        "r4r11_exact_delta_route_present": True,
        "prior_eta7_order_two_route_present": True,
        "exact_database_generator_identity_reused": True,
        "three_proof_obligations_preserved": True,
        "group_conclusion_completed": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run(root: Path, *, dry_run: bool, prior_file: Path | None) -> int:
    folder = report_folder()
    report: dict[str, object] = {
        "phase": "175-R4R11", "dry_run": dry_run,
        "gate": "FAIL_R4R11_SIGNED_ETA_TORSION",
        "new_given": 0, "new_mathematical_rules": 1,
        "pi95_proof_complete": False, "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        prior = find_prior(prior_file)
        report["prior_report"] = str(prior)
        report["prior"] = validate_prior(json.loads(prior.read_text(encoding="utf-8")))
        report["isolated_replay"] = replay_general_rule()
        report["install"] = installer.install(root, dry_run=dry_run, output=folder)
        report["public"] = None if dry_run else inspect_shared_connection()
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as exc:
        report["error"] = type(exc).__name__ + ": " + str(exc)
        report["traceback"] = traceback.format_exc()[-7000:]
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R11 — 2-torsion 符号正規化\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "(5.8) と Proposition 2.5 は R4R10 で出典登録済み。"
        + "一般規則は未証明の符号を勝手に選ばず、証明済み位数2の前提を必要とする。\n\n"
        + "π₉⁵ の完成証明は本段階で主張しない。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R11_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R11_NEW_GIVEN=0")
    print("PHASE175_R4R11_NEW_MATHEMATICAL_RULES=1")
    print("PHASE175_R4R11_SHARED_RULE=" + (
        "CONNECTED" if isinstance(report.get("public"), dict)
        and report["public"].get("r4r11_exact_delta_route_present") else "NOT_CHECKED"
    ))
    print("PHASE175_R4R11_PI95=NOT_COMPLETE")
    print("PHASE175_R4R11_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R11_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R11_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R11_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r10-report", type=Path)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r10_report)


if __name__ == "__main__":
    sys.exit(main())
```

## `run.ps1` 全文

```powershell
param(
    [switch] $DryRun,
    [string] $R4R10Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r11_signed_eta_torsion_public/tests/test_rule.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_provider.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_installer.py',
        'phase175_r4r11_signed_eta_torsion_public/tests/test_audit.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_source.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_installer.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_audit.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r5r3_public_order_zero/tests/test_real_integration.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R11 focused pytest failed' }
    Write-Output 'PHASE175_R4R11_FOCUSED_PYTEST=PASS'

    $arguments = @(
        '-B', '-m', 'phase175_r4r11_signed_eta_torsion_public.audit',
        '--root', $root
    )
    if ($DryRun) { $arguments += '--dry-run' }
    if ($R4R10Report -ne '') { $arguments += @('--r4r10-report', $R4R10Report) }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R11 signed torsion audit failed' }
    Write-Output 'PHASE175_R4R11_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R11_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R11_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
```

## `tests/test_rule.py` 全文

```python
"""Generic signed-to-exact normalization: strictly proved two-torsion and suspension."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import (
    Composition, GeneratorSymbol, HomotopyElement, MapApplication,
    Multiple, Sum, Zero,
)
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from map_facts import EHP_DELTA_MAP
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r10_cited_58_prop25_public.source import canonical_toda58
from phase175_r4r11_signed_eta_torsion_public.rule import (
    RULE_NAME, eta_two_torsion_normalization_inputs,
    signed_eta_two_torsion_rule, expand_signed_eta_two_torsion,
)
from proof import (
    InferenceRule, ProofRule, ProofStep, Relation, RelationType,
    apply_inference_match, find_inference_matches_for_rule,
)
from toda_rules import TodaDeltaImageUpToSignStatement


def fixture():
    source = canonical_toda58()
    beta = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", 7))
    gamma = HomotopyElement("η₉", 9, 10, 9, GeneratorSymbol("η", 9))
    signed = TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(source.positive_value, beta),
    )
    order = Relation(Multiple(2, beta), Zero(), RelationType.EQUALITY)
    goal = Relation(
        MapApplication(EHP_DELTA_MAP, gamma),
        Composition(source.positive_value.right.expression, beta),
        RelationType.EQUALITY,
    )
    return goal, signed, order, TodaEtaFamilyGeneralDefinition()


def synthetic(value: object, kind: ProofRule) -> ProofStep:
    return ProofStep(value, (), kind, inference_rule=InferenceRule("test fixture"))


def test_canonical_delta_eta9_normalizes_without_direct_given() -> None:
    goal, signed, order, definition = fixture()
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition) == (
        signed, order, definition,
    )
    rule = signed_eta_two_torsion_rule(goal, signed, order, definition)
    assert rule.name == RULE_NAME
    parents = (
        synthetic(signed, ProofRule.INFERENCE),
        synthetic(order, ProofRule.INFERENCE),
        synthetic(definition, ProofRule.GIVEN),
    )
    matches = find_inference_matches_for_rule(rule, parents)
    assert len(matches) == 1
    step = apply_inference_match(matches[0])
    assert step.rule is ProofRule.INFERENCE
    assert step.conclusion == goal
    assert step.premises == parents


def test_missing_sources_or_forged_given_not_accepted() -> None:
    goal, signed, order, definition = fixture()
    rule = signed_eta_two_torsion_rule(goal, signed, order, definition)
    parents = (
        synthetic(signed, ProofRule.INFERENCE),
        synthetic(order, ProofRule.INFERENCE),
        synthetic(definition, ProofRule.GIVEN),
    )
    for i in range(3):
        remaining = parents[:i] + parents[i + 1:]
        assert not find_inference_matches_for_rule(rule, remaining)
    assert not find_inference_matches_for_rule(rule, (
        synthetic(signed, ProofRule.GIVEN), parents[1], parents[2],
    ))
    assert not find_inference_matches_for_rule(rule, (
        parents[0], synthetic(order, ProofRule.GIVEN), parents[2],
    ))
    assert not find_inference_matches_for_rule(rule, (
        parents[0], parents[1], synthetic(definition, ProofRule.INFERENCE),
    ))


def test_general_even_coefficient_branch() -> None:
    goal, signed, order, definition = fixture()
    value = signed.positive_value
    changed = replace(value, left=replace(
        value.left, left=Multiple(8, value.left.left.expression),
    ))
    signed = replace(signed, positive_value=changed)
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition)


@pytest.mark.parametrize("coefficient", [1, 3, -3, True])
def test_odd_or_boolean_coefficient_rejected(coefficient: object) -> None:
    goal, signed, order, definition = fixture()
    value = signed.positive_value
    changed = replace(value, left=replace(
        value.left, left=Multiple(coefficient, value.left.left.expression),
    ))
    signed = replace(signed, positive_value=changed)
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition) is None


@pytest.mark.parametrize("change", [
    "wrong_order", "wrong_goal", "wrong_map", "wrong_beta", "wrong_sign", "not_suspension",
    "bad_definition", "changed_gamma", "invalid_type", "wrong_middle_group",
])
def test_unproved_or_malformed_rejected(change: str) -> None:
    goal, signed, order, definition = fixture()
    if change == "wrong_order":
        order = replace(order, lhs=Multiple(4, order.lhs.expression))
    elif change == "wrong_goal":
        goal = replace(goal, rhs=signed.positive_value)
    elif change == "wrong_map":
        goal = replace(goal, lhs=MapApplication(GeneratorSymbol("E"), signed.element))
    elif change == "wrong_beta":
        beta = replace(signed.positive_value.right, generator=GeneratorSymbol("ν", 7))
        signed = replace(signed, positive_value=replace(signed.positive_value, right=beta))
    elif change == "wrong_sign":
        linear = signed.positive_value.left
        signed = replace(signed, positive_value=replace(
            signed.positive_value,
            left=replace(linear, right=Multiple(1, linear.right.expression)),
        ))
    elif change == "not_suspension":
        beta = replace(signed.positive_value.right, dimension=2, source=3, target=2,
                       generator=GeneratorSymbol("η", 2))
        signed = replace(signed, positive_value=replace(signed.positive_value, right=beta))
    elif change == "bad_definition":
        definition = TodaEtaFamilyGeneralDefinition(lower_bound=4)
    elif change == "changed_gamma":
        signed = replace(signed, element=replace(signed.element, source=12))
    elif change == "invalid_type":
        signed = "signed Delta image text"
    elif change == "wrong_middle_group":
        signed = replace(signed, map=replace(signed.map,
                        target_group=TodaPrimaryGroup(9, 4)))
    assert eta_two_torsion_normalization_inputs(goal, signed, order, definition) is None


def test_source_discovered_expansion_not_a_proof_leaf() -> None:
    goal, signed, order, definition = fixture()
    options = expand_signed_eta_two_torsion(goal, (signed, signed))
    assert len(options) == 1
    assert options[0].subgoals == (signed, order, definition)
    assert not expand_signed_eta_two_torsion(goal, ())
    assert not expand_signed_eta_two_torsion(goal, ("source text",))
    assert all(not isinstance(x, ProofStep) for x in options[0].subgoals)


def test_non_group_statement_does_not_claim_pi95() -> None:
    goal, signed, order, definition = fixture()
    assert isinstance(goal, Relation)
    assert goal.lhs.map == EHP_DELTA_MAP
    assert not hasattr(goal.lhs, "group_dimension")
    assert not hasattr(goal.rhs, "summands")
    with pytest.raises(ValueError):
        signed_eta_two_torsion_rule(goal, signed, replace(order, rhs=goal.rhs), definition)
```

## `tests/test_provider.py` 全文

```python
"""Provider discovers the R4R10 signed source without creating a new GIVEN."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, MapApplication, Multiple, Zero
from map_facts import EHP_DELTA_MAP
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r10_cited_58_prop25_public.audit import sample_delta_eta9
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta, canonical_toda58,
)
from phase175_r4r11_signed_eta_torsion_public.provider import (
    build_signed_eta_torsion_provider,
)
from phase175_r4r11_signed_eta_torsion_public.rule import RULE_NAME
from proof import ProofRule, ProofStep, Relation
from unified_statement_registry import (
    AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry,
    ProofStepLink, ReferenceKind, UnifiedStatementRegistry,
)


def cited_bridge(include_source: bool = True, duplicate: bool = False) -> RegistryBridgeResult:
    registry = UnifiedStatementRegistry()
    refs = []
    if include_source:
        refs.append(CitedToda58SignedDelta(canonical_toda58()))
        if duplicate:
            refs.append(CitedToda58SignedDelta(canonical_toda58()))
    refs.append(TodaEtaFamilyGeneralDefinition())
    links = []
    for i, item in enumerate(refs):
        aid = "test:cited:" + str(i)
        rid = "test:source:" + str(i)
        registry.add_reference(LiteratureEntry(
            rid, ReferenceKind.EQUATION, "cited fixture" + str(i),
        ))
        registry.add_assertion(AssertionEntry(
            aid, rid, AssertionKind.STATEMENT, item, AssertionOrigin.FIXED_STATEMENT,
        ))
        links.append(ProofStepLink(aid, step=ProofStep(item, (), ProofRule.GIVEN)))
    return RegistryBridgeResult(registry, (), tuple(links))


def exact_target() -> Relation:
    signed = sample_delta_eta9()
    source = canonical_toda58()
    return Relation(
        MapApplication(EHP_DELTA_MAP, signed.element),
        Composition(source.positive_value.right.expression, signed.positive_value.right),
    )


def test_source_backed_provider_requires_actual_cited_witness() -> None:
    target = exact_target()
    good = build_signed_eta_torsion_provider(cited_bridge())(target)
    assert len(good) == 1
    assert good[0].rule.name == RULE_NAME
    signed, order, definition = good[0].subgoals
    assert signed == sample_delta_eta9()
    assert order == Relation(Multiple(2, signed.positive_value.right), Zero())
    assert definition == TodaEtaFamilyGeneralDefinition()
    assert not build_signed_eta_torsion_provider(cited_bridge(False))(target)


def test_duplicate_source_is_not_a_new_proof_or_extra_branch() -> None:
    options = build_signed_eta_torsion_provider(cited_bridge(duplicate=True))(exact_target())
    assert len(options) == 1
    assert all(not isinstance(goal, ProofStep) for goal in options[0].subgoals)


def test_wrong_goal_or_unrelated_expression_does_not_propose() -> None:
    expand = build_signed_eta_torsion_provider(cited_bridge())
    exact = exact_target()
    assert not expand(replace(exact, rhs=sample_delta_eta9().positive_value))
    assert not expand(replace(exact, lhs=MapApplication("wrong map", exact.lhs.expression)))
    assert not expand("untyped Delta identity text")
    assert not expand(Relation(Multiple(2, sample_delta_eta9().element), Zero()))


def test_provider_does_not_registered_pi95_group_proof() -> None:
    options = build_signed_eta_torsion_provider(cited_bridge())(exact_target())
    assert len(options) == 1
    assert all(not hasattr(item, "group_dimension") for item in options[0].subgoals)
```

## `tests/test_installer.py` 全文

```python
"""Whole-function installer guard, never partial unscoped text edits."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r11_signed_eta_torsion_public import installer


def sample_code() -> str:
    return (
        "def before():\n    return 1\n\n"
        "def shared_expansion_provider(bridge):\n"
        + installer.ANCHOR
        + "    return extra_providers\n\n"
        + "def after():\n    return 2\n"
    )


def test_one_complete_function_patched(monkeypatch: pytest.MonkeyPatch) -> None:
    content = sample_code()
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(content.encode()))
    updated, after, base = installer.function_replacement(content)
    assert installer.ADDITION in after
    assert base == content
    assert updated.count(installer.ADDITION) == 1
    assert "def before():\n    return 1" in updated
    assert "def after():\n    return 2" in updated
    ast.parse(updated)


def test_installer_idempotent_and_exact_base(monkeypatch: pytest.MonkeyPatch) -> None:
    content = sample_code()
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(content.encode()))
    once = installer.function_replacement(content)[0]
    twice = installer.function_replacement(once)[0]
    assert once == twice
    with pytest.raises(RuntimeError, match="UNREVIEWED_BASE_SOURCE"):
        installer.function_replacement(once.replace("return 1", "return 3"))


def test_anchor_or_function_change_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    content = sample_code()
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(content.encode()))
    with pytest.raises(RuntimeError, match="ANCHOR_CHANGED"):
        installer.function_replacement(content.replace("build_cited_58_prop25_provider", "other"))
    with pytest.raises(RuntimeError, match="FUNCTION_NOT_UNIQUE"):
        installer.function_replacement(content + content)


def test_dry_run_writes_complete_function_but_not_production(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    path = root / installer.TARGET
    initial = sample_code()
    path.write_text(initial, encoding="utf-8")
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(initial.encode()))
    monkeypatch.setattr(installer, "git", lambda root, *args: installer.REVIEWED_COMMITTED_BLOBS[0])
    result = installer.install(root, dry_run=True, output=tmp_path / "output")
    assert result["patch_required"] is True
    assert result["patch_applied"] is False
    assert path.read_text(encoding="utf-8") == initial
    assert "def shared_expansion_provider" in (
        tmp_path / "output" / "shared_expansion_provider_FULL_AFTER.py"
    ).read_text(encoding="utf-8")


def test_real_install_only_one_function(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    root = tmp_path / "repo"
    root.mkdir()
    path = root / installer.TARGET
    initial = sample_code()
    path.write_text(initial, encoding="utf-8")
    monkeypatch.setattr(installer, "BASE_WORKING_BLOB", installer.git_blob_sha(initial.encode()))
    monkeypatch.setattr(installer, "git", lambda root, *args: installer.REVIEWED_COMMITTED_BLOBS[0])
    result = installer.install(root, dry_run=False, output=tmp_path / "output")
    assert result["patch_applied"] is True
    installed = path.read_text(encoding="utf-8")
    assert installer.ADDITION in installed
    assert "def before():\n    return 1" in installed
    assert "def after():\n    return 2" in installed
    again = installer.install(root, dry_run=False, output=tmp_path / "output")
    assert again["patch_required"] is False
```

## `tests/test_audit.py` 全文

```python
"""R4R11 provenance, reviewed local history, and prior-report contracts."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase175_r4r11_signed_eta_torsion_public import audit, installer


def passed_r4r10_report() -> dict[str, object]:
    return {
        "phase": "175-R4R10", "dry_run": False, "gate": audit.PRIOR_GATE,
        "new_given": 2, "new_mathematical_rules": 0,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
        "preflight": {"head": audit.BASE_HEAD},
        "delta_composition_replay": {
            "conclusion_is_signed": True,
            "proposition_2_5_citation_present": True,
            "equation_5_8_citation_present": True,
            "eta_family_citation_present": True,
            "signed_parent_inferred": True,
            "composition_identity_parent_inferred": True,
            "root_group_conclusion_inferred": False,
        },
        "public": {
            "public_prop25_candidate_found": True,
            "public_signed_parent_candidate_found": True,
            "public_identity_parent_candidate_found": True,
            "public_root_pi95_proof_complete": False,
        },
        "install": {
            "production_path": installer.TARGET.as_posix(),
            "after_git_blob": installer.BASE_WORKING_BLOB,
            "two_full_functions_exported": True,
        },
    }


def test_valid_real_report_shape_is_accepted_not_promoted() -> None:
    result = audit.validate_prior(passed_r4r10_report())
    assert result["successful_prior"] is True
    assert result["pi95_not_yet_complete"] is True


@pytest.mark.parametrize("key,change", (
    ("dry_run", True), ("phase", "175-R4R8"),
    ("gate", audit.DRY_GATE), ("new_given", 0),
    ("new_mathematical_rules", 1), ("pi95_proof_complete", True),
    ("full_pytest_executed", True), ("prior_proof_search_executed", True),
))
def test_prior_scope_tamper_rejected(key: str, change: object) -> None:
    report = passed_r4r10_report()
    report[key] = change
    with pytest.raises(RuntimeError, match="GATE_OR_SCOPE_CHANGED"):
        audit.validate_prior(report)


@pytest.mark.parametrize("section,key,change", (
    ("preflight", "head", "0" * 40),
    ("delta_composition_replay", "conclusion_is_signed", False),
    ("delta_composition_replay", "signed_parent_inferred", False),
    ("delta_composition_replay", "eta_family_citation_present", False),
    ("delta_composition_replay", "root_group_conclusion_inferred", True),
    ("public", "public_prop25_candidate_found", False),
    ("public", "public_signed_parent_candidate_found", False),
    ("public", "public_identity_parent_candidate_found", False),
    ("public", "public_root_pi95_proof_complete", True),
    ("install", "production_path", "proof.py"),
    ("install", "two_full_functions_exported", False),
))
def test_prior_evidence_tamper_rejected(
    section: str, key: str, change: object,
) -> None:
    report = deepcopy(passed_r4r10_report())
    report[section][key] = change
    with pytest.raises(RuntimeError, match="EVIDENCE_INVALID"):
        audit.validate_prior(report)


def test_latest_successful_report_is_selected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    older = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE / "old" / "report.json"
    newer = tmp_path / "EHPProofTracerAudit" / audit.PRIOR_PACKAGE / "new" / "report.json"
    older.parent.mkdir(parents=True)
    newer.parent.mkdir(parents=True)
    older.write_text(json.dumps(passed_r4r10_report()), encoding="utf-8")
    tampered = passed_r4r10_report()
    tampered["gate"] = "FAIL"
    newer.write_text(json.dumps(tampered), encoding="utf-8")
    assert audit.find_prior(None) == older
    assert audit.find_prior(older) == older.resolve()


def fake_git_factory(root: Path, head: str, changed: str = ""):
    def fake_git(repository: Path, *args: str, allow_failure: bool = False):
        if args == ("rev-parse", "--show-toplevel"):
            return 0, str(root)
        if args == ("branch", "--show-current"):
            return 0, "develop"
        if args == ("rev-parse", "HEAD"):
            return 0, head
        if args == ("diff", "--name-only"):
            return 0, changed
        if args == ("diff", "--cached", "--name-only"):
            return 0, ""
        if args == ("merge-base", "--is-ancestor", audit.BASE_HEAD, head):
            return 0, ""
        if args == ("diff", "--name-only", audit.BASE_HEAD, head):
            return 0, audit.PRIOR_PACKAGE + "/source.py\n" + installer.TARGET.as_posix()
        raise AssertionError(args)
    return fake_git


def test_reviewed_heads_are_accepted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(audit, "PINNED_WORKING_BLOBS", {})
    monkeypatch.setattr(installer, "plan", lambda root: (
        root / installer.TARGET, b"old", b"new", "full function",
    ))
    for head in (audit.BASE_HEAD, audit.REVIEWED_R4R10_HEAD):
        monkeypatch.setattr(audit, "git", fake_git_factory(tmp_path, head))
        found = audit.preflight(tmp_path)
        assert found["head"] == head


def test_unknown_head_or_dirty_unrelated_change_rejected(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(audit, "PINNED_WORKING_BLOBS", {})
    monkeypatch.setattr(installer, "plan", lambda root: (
        root / installer.TARGET, b"old", b"new", "full function",
    ))
    monkeypatch.setattr(audit, "git", fake_git_factory(tmp_path, "0" * 40))
    with pytest.raises(RuntimeError, match="UNREVIEWED_HEAD"):
        audit.preflight(tmp_path)
    monkeypatch.setattr(audit, "git", fake_git_factory(tmp_path, audit.BASE_HEAD, "proof.py"))
    with pytest.raises(RuntimeError, match="UNREVIEWED_TRACKED_CHANGE"):
        audit.preflight(tmp_path)
```



---

# Phase 175 R4R11R2 — Git blob の CRLF/LF 照合修正（2026-11-18）

## 修正対象

- `phase175_r4r11_signed_eta_torsion_public/audit.py`：新規 `reviewed_eol_blob_matches()` を既存 `preflight()` の直前に追加。`preflight()` を全体置換。
- `phase175_r4r11_signed_eta_torsion_public/tests/test_audit.py`：新規 `test_reviewed_eol_blob_matches_crlf_and_lf_without_accepting_drift()` を `test_reviewed_heads_are_accepted()` の直前に追加。
- `README.md`, `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `TEST_RESULTS_JA.md`：全文更新。

import の変更なし。既存クラス・数学規則・本番コード・`run.ps1` の変更なし。R4R11R1 からの既存テスト修正を保持する。以下は追加関数・変更関数・追加テストの省略なしの全文。

## 変更後の `audit.py` import 全文

```python
"""Phase 175 R4R11: source-first signed Delta / proved eta order-two normalization.

The phase adds one general inference, not a new mathematical source/GIVEN.
A group query for pi_9^5 is not claimed complete by this phase.
"""
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

from phase175_r4r11_signed_eta_torsion_public import installer
```

## `reviewed_eol_blob_matches()` 全文（`preflight()` 直前に追加）

```python
def reviewed_eol_blob_matches(content: bytes, expected_blob: str) -> bool:
    """Match a pinned Git blob under LF or CRLF working-tree conventions.

    Git may store a text file with CRLF (notably expression.py and Toda TeX)
    while a checkout uses LF, or vice versa. Compare *complete bytes* of both
    line-ending encodings; never waive the pinned SHA-1 or change source text.
    """
    normalized = content.replace(b"\r\n", b"\n")
    candidates = (
        content,
        normalized,
        normalized.replace(b"\n", b"\r\n"),
    )
    return any(installer.git_blob_sha(data) == expected_blob for data in candidates)
```

## `preflight()` 全文

```python
def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R11_WRONG_REPO_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R11_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    if head not in (BASE_HEAD, REVIEWED_R4R10_HEAD):
        raise RuntimeError("R4R11_UNREVIEWED_HEAD: " + head)
    if head == REVIEWED_R4R10_HEAD:
        code, _ = git(root, "merge-base", "--is-ancestor", BASE_HEAD, head,
                      allow_failure=True)
        if code != 0:
            raise RuntimeError("R4R11_REVIEWED_LINEAGE_NOT_ANCESTOR")
        changed = git(root, "diff", "--name-only", BASE_HEAD, head)[1].splitlines()
        if any(not (name == installer.TARGET.as_posix()
                    or name.startswith(PRIOR_PACKAGE + "/")) for name in changed):
            raise RuntimeError("R4R11_UNREVIEWED_INTERVENING_COMMIT")
    dirty = sorted(set(
        git(root, "diff", "--name-only")[1].splitlines()
        + git(root, "diff", "--cached", "--name-only")[1].splitlines()
    ))
    if any(item not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for item in dirty):
        raise RuntimeError("R4R11_UNREVIEWED_TRACKED_CHANGE: " + repr(dirty))
    # plan() fail-closes against arbitrary edits to shared production source,
    # and verifies the whole-function, idempotent patch, not merely a marker.
    plan_path, before, after, _ = installer.plan(root)
    if plan_path != root / installer.TARGET:
        raise RuntimeError("R4R11_WRONG_TARGET_PATH")
    for path, expected in PINNED_WORKING_BLOBS.items():
        file = root / path
        if not file.is_file():
            raise RuntimeError("R4R11_SOURCE_MISSING: " + path)
        if not reviewed_eol_blob_matches(file.read_bytes(), expected):
            raise RuntimeError("R4R11_SOURCE_DRIFT: " + path)
    return {
        "head": head,
        "reviewed_base_head": BASE_HEAD,
        "reviewed_successor_head": REVIEWED_R4R10_HEAD,
        "pinned_blobs": len(PINNED_WORKING_BLOBS),
        "production_patch_required": before != after,
        "production_after_blob": installer.git_blob_sha(after.replace(b"\r\n", b"\n")),
        "dirty_tracked_paths": dirty,
    }
```

## `tests/test_audit.py` import 全文

```python
"""R4R11 provenance, reviewed local history, and prior-report contracts."""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from phase175_r4r11_signed_eta_torsion_public import audit, installer
```

## 新規テスト関数全文（`test_reviewed_heads_are_accepted()` 直前に追加）

```python
def test_reviewed_eol_blob_matches_crlf_and_lf_without_accepting_drift() -> None:
    """Regression: expression.py/Toda sources are committed with CRLF."""
    source_lf = b"alpha\nbeta\n"
    source_crlf = b"alpha\r\nbeta\r\n"
    expected_crlf = installer.git_blob_sha(source_crlf)
    expected_lf = installer.git_blob_sha(source_lf)

    assert audit.reviewed_eol_blob_matches(source_crlf, expected_crlf)
    assert audit.reviewed_eol_blob_matches(source_lf, expected_crlf)
    assert audit.reviewed_eol_blob_matches(source_lf, expected_lf)
    assert audit.reviewed_eol_blob_matches(source_crlf, expected_lf)
    assert not audit.reviewed_eol_blob_matches(b"alpha\nbetampered\n", expected_crlf)
    assert not audit.reviewed_eol_blob_matches(b"alpha\rbet a\n", expected_crlf)
    assert not audit.reviewed_eol_blob_matches(source_crlf, "0" * 40)
```
