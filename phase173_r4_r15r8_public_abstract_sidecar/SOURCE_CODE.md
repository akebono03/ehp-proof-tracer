# Phase 173 R4-R15R8 — コード変更・テスト全文

GitHub `akebono03/ehp-proof-tracer` の develop HEAD `9d5b57205ebf001c7eb6981de71a626fb5aeafa2` から現行コードと関連テストを確認。既存ファイルは2つだけ変更し、Source Guard で元の内容を保護する。

## 変更対象・追加位置

- `phase165_r52_partial_proof.py`: import 全文、追加クラス `CertifiedAbstractStructure`（`PartialProofResult` の直前）、変更クラス `PartialProofResult` 全文。
- `phase165_r55_nk_only_goal.py`: import 全文、変更関数 `search_group_from_registered_goal` 全文。
- 新規 `phase173_r4_r15r8_public_abstract_sidecar`: `attach.py`、`patch_source.py`、`install.py`、`audit.py`、`run.ps1`、限定テスト（以下で各ファイル全文）。

# R15R8 — 変更後のクラス・関数全文

以下のコードは実装対象のクラス2個、関数1個の全体です。GitHub の現行内容を検査したうえで差し替えます。実行時には `install.py` がチェックアウトされた実ソースから同じ単位を `FULL_CHANGED_UNITS.md` に再生成します。

## `phase165_r52_partial_proof.py` — import 全文

```python
"""Phase 165 R52: range-independent, fail-closed partial proof presentation.

This module records *observed* proof progress. It does not certify a step or
infer a proof from a goal. Callers must supply their already validated steps.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any

from homotopy_groups import TodaPrimaryGroup
from proof import ProofRule, ProofStep
```

## `phase165_r52_partial_proof.py` — 新規クラス `CertifiedAbstractStructure`（`PartialProofResult` の直前）

```python
@dataclass(frozen=True)
class CertifiedAbstractStructure:
    """Verified abstract invariants, separate from a named group conclusion."""
    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]
    proof_step: ProofStep

    def __post_init__(self) -> None:
        from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
            TodaProp44AbstractGroupResult,
        )
        if not isinstance(self.group, TodaPrimaryGroup):
            raise TypeError("abstract certificate must have a typed target group")
        expected = TodaProp44AbstractGroupResult(
            self.group, self.invariant_summands,
        )
        if (not isinstance(self.proof_step, ProofStep)
                or self.proof_step.rule is not ProofRule.INFERENCE
                or self.proof_step.conclusion != expected
                or self.proof_step.inference_rule is None
                or not callable(self.proof_step.inference_rule.match_guard)
                or not self.proof_step.inference_rule.match_guard(
                    self.proof_step.premises, (),
                )):
            raise ValueError("abstract certificate has no verified inference root")
```

## `phase165_r52_partial_proof.py` — 変更クラス `PartialProofResult` 全文

```python
@dataclass(frozen=True)
class PartialProofResult:
    target: TodaPrimaryGroup
    status: ProofSearchStatus
    structure_status: GroupStructureStatus = GroupStructureStatus.UNKNOWN
    references: tuple[str, ...] = ()
    proven_steps: tuple[ProofStep, ...] = ()
    open_goals: tuple[Any, ...] = ()
    diagnostics: tuple[str, ...] = ()
    conclusion: Any | None = None
    abstract_structure: CertifiedAbstractStructure | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.target, TodaPrimaryGroup):
            raise TypeError("target must be TodaPrimaryGroup")
        if not isinstance(self.status, ProofSearchStatus):
            raise TypeError("status must be ProofSearchStatus")
        if not isinstance(self.structure_status, GroupStructureStatus):
            raise TypeError("structure_status must be GroupStructureStatus")
        for name in ("references", "proven_steps", "open_goals", "diagnostics"):
            if not isinstance(getattr(self, name), tuple):
                raise TypeError(f"{name} must be a tuple")
        if not all(isinstance(s, ProofStep) for s in self.proven_steps):
            raise TypeError("proven_steps must contain only ProofStep")
        if not all(isinstance(s, str) and s for s in self.references + self.diagnostics):
            raise ValueError("references and diagnostics must contain nonempty strings")
        if self.status is ProofSearchStatus.COMPLETE:
            if self.conclusion is None or self.open_goals:
                raise ValueError("complete proof requires conclusion and no open goals")
            if not any(step.conclusion == self.conclusion for step in self.proven_steps):
                raise ValueError("completed conclusion requires a matching proven step")
        elif self.conclusion is not None:
            raise ValueError("incomplete result must not claim a final conclusion")
        if self.abstract_structure is not None:
            if (not isinstance(self.abstract_structure, CertifiedAbstractStructure)
                    or self.abstract_structure.group != self.target
                    or self.status not in (
                        ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
                    )
                    or self.conclusion is not None
                    or self.structure_status is GroupStructureStatus.KNOWN):
                raise ValueError(
                    "abstract-only evidence cannot certify a named group"
                )
        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:
            raise ValueError("not-searched result cannot contain derived steps")
        if self.status is ProofSearchStatus.SEARCH_FAILED and not self.diagnostics:
            raise ValueError("failed search requires a diagnostic")
```

## `phase165_r55_nk_only_goal.py` — import 全文（変更なし）

```python
"""Select typed group proof goals from registered fixed claims, never from legacy results."""
from __future__ import annotations

from dataclasses import fields, is_dataclass, replace

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus, make_partial_proof_result
from phase165_r52_r9_shared_math import build_shared_typed_bridge, search_shared_group_goal
from proof import Relation, RelationType
from unified_statement_registry import AssertionOrigin
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
```

## `phase165_r55_nk_only_goal.py` — 変更関数 `search_group_from_registered_goal` 全文

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

## 新規ファイル全文

### `__init__.py`

```python
"""Attach independently certified abstract Toda 4.4 evidence to public partial results."""
```

### `attach.py`

```python
"""Attach a cited abstract certificate without promoting named group completion."""
from __future__ import annotations

from dataclasses import replace

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    GroupStructureStatus,
    PartialProofResult,
    ProofSearchStatus,
)
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r10_general_toda56_core.core import checked_abstract_inputs
from proof import ProofRule


def attach_certified_abstract_structure(
    result: PartialProofResult, *, n: int, k: int,
    goal: object, bridge: RegistryBridgeResult,
) -> PartialProofResult:
    """Attach *only* a separately replayed abstract proof to a named partial.

    No result status, named conclusion, open goal, named structure status, or
    registered source context is modified. The certificate's source context is
    internal to its proof construction. Missing evidence always returns the
    original result without granting any new proof claim.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("Expected a canonical partial proof result")
    if (type(n) is not int or type(k) is not int or n != 4 or k < 3
            or result.status not in (
                ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
            )
            or result.abstract_structure is not None
            or result.target.group_dimension != n + k
            or result.target.sphere_dimension != n
            or result.structure_status is GroupStructureStatus.KNOWN
            or not isinstance(bridge, RegistryBridgeResult)):
        return result
    target = exact_prior_database_result(n, k)
    if (target is None or type(target) is not type(goal) or target != goal
            or checked_abstract_inputs(target) is None):
        return result
    try:
        certificate = search_source_first_abstract(k=k, bridge=bridge)
    except (ValueError, LookupError):
        # An optional abstract sidecar must not break existing named queries
        # when an independently screened source is absent from a caller bridge.
        return result
    if certificate is None or certificate.proof_target != target:
        return result
    root = certificate.root_step
    if (certificate.public_group_complete is not False
            or root.rule is not ProofRule.INFERENCE
            or root.conclusion != certificate.conclusion
            or root.inference_rule is None
            or not root.inference_rule.match_guard(root.premises, ())):
        return result
    structural = CertifiedAbstractStructure(
        group=certificate.conclusion.group,
        invariant_summands=certificate.conclusion.invariant_summands,
        proof_step=root,
    )
    return replace(result, abstract_structure=structural)
```

### `patch_source.py`

```python
"""Small, source-guarded changes to the canonical public result model and selector."""
from __future__ import annotations

import ast


ABSTRACT_CLASS = '''@dataclass(frozen=True)
class CertifiedAbstractStructure:
    """Verified abstract invariants, separate from a named group conclusion."""
    group: TodaPrimaryGroup
    invariant_summands: tuple[tuple[str, int], ...]
    proof_step: ProofStep

    def __post_init__(self) -> None:
        from phase173_r4_r15r6_abstract_toda44_rule.abstract_rule import (
            TodaProp44AbstractGroupResult,
        )
        if not isinstance(self.group, TodaPrimaryGroup):
            raise TypeError("abstract certificate must have a typed target group")
        expected = TodaProp44AbstractGroupResult(
            self.group, self.invariant_summands,
        )
        if (not isinstance(self.proof_step, ProofStep)
                or self.proof_step.rule is not ProofRule.INFERENCE
                or self.proof_step.conclusion != expected
                or self.proof_step.inference_rule is None
                or not callable(self.proof_step.inference_rule.match_guard)
                or not self.proof_step.inference_rule.match_guard(
                    self.proof_step.premises, (),
                )):
            raise ValueError("abstract certificate has no verified inference root")


'''

MODEL_FIELD = '    abstract_structure: CertifiedAbstractStructure | None = None\n'
MODEL_GUARD = '''        if self.abstract_structure is not None:
            if (not isinstance(self.abstract_structure, CertifiedAbstractStructure)
                    or self.abstract_structure.group != self.target
                    or self.status not in (
                        ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED,
                    )
                    or self.conclusion is not None
                    or self.structure_status is GroupStructureStatus.KNOWN):
                raise ValueError(
                    "abstract-only evidence cannot certify a named group"
                )
'''

ORDER_BRANCH = '''        if order_diagnostic is not None:
            return make_partial_proof_result(
                n=n, k=k, status=ProofSearchStatus.SEARCH_FAILED,
                open_goals=(candidate,), diagnostics=(order_diagnostic,),
            )
'''
ORDER_REPLACEMENT = '''        if order_diagnostic is not None:
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
'''
END_BRANCH = '''    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    return result
'''
END_REPLACEMENT = '''    if result.status is ProofSearchStatus.COMPLETE and result.conclusion == candidate:
        return replace(result, structure_status=GroupStructureStatus.KNOWN)
    if n == 4 and k >= 3:
        from phase173_r4_r15r8_public_abstract_sidecar.attach import (
            attach_certified_abstract_structure,
        )
        return attach_certified_abstract_structure(
            result, n=n, k=k, goal=candidate, bridge=bridge,
        )
    return result
'''


def _eol(source: bytes) -> str:
    text = source.decode("utf-8-sig")
    if "\r\n" in text and text.count("\r\n") == text.count("\n"):
        return "\r\n"
    if "\r\n" in text:
        raise RuntimeError("Mixed source line endings require review")
    return "\n"


def _replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise RuntimeError("Reviewed production anchor absent or ambiguous: " + repr(old[:80]))
    return source.replace(old, new, 1)


def transform_model(source: bytes) -> bytes:
    eol = _eol(source)
    text = source.decode("utf-8-sig").replace("\r\n", "\n")
    if text.count("@dataclass(frozen=True)\nclass PartialProofResult:") != 1:
        raise RuntimeError("Reviewed result class not found")
    if "class CertifiedAbstractStructure:" in text or "abstract_structure:" in text:
        raise RuntimeError("Result model already contains an abstract sidecar")
    text = _replace_once(text, "from proof import ProofStep\n",
                         "from proof import ProofRule, ProofStep\n")
    text = _replace_once(text, "@dataclass(frozen=True)\nclass PartialProofResult:",
                         ABSTRACT_CLASS + "@dataclass(frozen=True)\nclass PartialProofResult:")
    text = _replace_once(text, "    conclusion: Any | None = None\n",
                         "    conclusion: Any | None = None\n" + MODEL_FIELD)
    anchor = '        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:\n'
    text = _replace_once(text, anchor, MODEL_GUARD + anchor)
    ast.parse(text)
    return text.replace("\n", eol).encode("utf-8")


def transform_selector(source: bytes) -> bytes:
    eol = _eol(source)
    text = source.decode("utf-8-sig").replace("\r\n", "\n")
    if "attach_certified_abstract_structure" in text:
        raise RuntimeError("Selector already has abstract attachment logic")
    text = _replace_once(text, ORDER_BRANCH, ORDER_REPLACEMENT)
    text = _replace_once(text, END_BRANCH, END_REPLACEMENT)
    ast.parse(text)
    return text.replace("\n", eol).encode("utf-8")


def full_replacement_units(original_model: bytes, original_selector: bytes) -> str:
    """Emit complete reviewed classes and complete changed selector function."""
    model = ast.parse(transform_model(original_model).decode("utf-8-sig"))
    selector = ast.parse(transform_selector(original_selector).decode("utf-8-sig"))
    model_text = transform_model(original_model).decode("utf-8-sig").replace("\r\n", "\n")
    selector_text = transform_selector(original_selector).decode("utf-8-sig").replace("\r\n", "\n")
    chunks = []
    for node in model.body:
        if isinstance(node, ast.ClassDef) and node.name in ("CertifiedAbstractStructure", "PartialProofResult"):
            # Include the entire decorated class, including class-level import annotations.
            lines = model_text.splitlines(keepends=True)
            start = min((d.lineno for d in node.decorator_list), default=node.lineno)
            chunks.append((node.name, "".join(lines[start-1:node.end_lineno])))
    for node in selector.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "search_group_from_registered_goal":
            lines = selector_text.splitlines(keepends=True)
            chunks.append((node.name, "".join(lines[node.lineno-1:node.end_lineno])))
    if len(chunks) != 3:
        raise RuntimeError("Could not extract all three complete replacement units")
    return "".join("### `" + name + "`\n\n```python\n" + body + "```\n\n" for name,body in chunks)
```

### `install.py`

```python
"""Guarded, reversible two-file installation for the public abstract sidecar."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

from phase173_r4_r15r8_public_abstract_sidecar.patch_source import (
    transform_model,
    transform_selector,
    full_replacement_units,
)

REVIEWED_HEAD = "9d5b57205ebf001c7eb6981de71a626fb5aeafa2"
REVIEWED_BLOBS = {
    "phase165_r52_partial_proof.py": "669fb947f1f9b4670d10723f8a562e60c015b249",
    "phase165_r55_nk_only_goal.py": "8afedad058c040a4d618af04485b83e93aacf5a4",
    "phase165_r52_r9_shared_math.py": "f49b0b7699e29ec1b78d73578dc66a0e33d6e336",
    "phase173_r4_r10_general_toda56_core/core.py": "d35600804ecbbc5f8566d52e45a2f6ecf8816347",
    "phase169_r10e4_ordered_db_prior/db_prior.py": "ed8c6a1f0f6f130005d42a2edba4ab40991e879b",
    "phase165_r52_r27_r5_literature.py": "c9bfe2788f4cf043db6dada98a437afea6accf75",
    "phase173_r4_r1_lemma54_source_bridge/source.py": "a37bf7447194d72526522366944778c386c8966c",
    "phase165_r3_recursive_search.py": "06009bfcf57f99cac58c229d99c53f16324692d0",
    "phase173_r4_r10_general_toda56_core/tests/test_core.py": "68205bf2840688a7b5d7277875c513323be7a5fc",
}
REVIEWED_PREVIOUS_FILES = {
    "phase173_r4_r15r7_source_first_abstract_certificate/search.py": "e7026a26302816a4d06eb5d99b35d46f9e16ceeb4f9477c6fa2435e0f3776fe1",
    "phase173_r4_r15r7_source_first_abstract_certificate/source.py": "4d4f64fe2470dcf32da38463edc21dc4e4f05a406b36e34d0f15810d4821aadd",
    "phase173_r4_r15r6_abstract_toda44_rule/abstract_rule.py": "fceab3505977b741e0756221b8c7c7abb70339ca75527e55f1924f23f7b54444",
}
TARGETS = {
    "phase165_r52_partial_proof.py": transform_model,
    "phase165_r55_nk_only_goal.py": transform_selector,
}
PACKAGE = "phase173_r4_r15r8_public_abstract_sidecar"
REPORT_FILE = "installed_state.json"


def git(root: Path, *args: str, binary: bool = False):
    result = subprocess.run(("git", *args), cwd=root, capture_output=True,
                            text=not binary, encoding=None if binary else "utf-8",
                            errors=None if binary else "replace", check=False)
    if result.returncode:
        raise RuntimeError("git " + " ".join(args) + " failed: " + str(result.stderr)[:500])
    return result.stdout if binary else result.stdout.strip()


def normalized(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n")


def sha(data: bytes) -> str:
    return hashlib.sha256(normalized(data)).hexdigest()


def reviewed_patch(root: Path) -> tuple[dict[str, bytes], dict[str, bytes], dict[str, str]]:
    originals: dict[str, bytes] = {}
    patched: dict[str, bytes] = {}
    states: dict[str, str] = {}
    for name, transform in TARGETS.items():
        if git(root, "rev-parse", "HEAD:" + name) != REVIEWED_BLOBS[name]:
            raise RuntimeError("Unreviewed Git blob: " + name)
        baseline = git(root, "show", "HEAD:" + name, binary=True)
        existing = (root / name).read_bytes()
        next_bytes = transform(baseline)
        originals[name] = baseline
        patched[name] = next_bytes
        if normalized(existing) == normalized(baseline):
            states[name] = "BASELINE"
        elif normalized(existing) == normalized(next_bytes):
            states[name] = "PATCHED"
        else:
            raise RuntimeError("Unreviewed worktree content: " + name)
    return originals, patched, states


def preflight(root: Path):
    root = root.resolve()
    if Path(git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise RuntimeError("Wrong repository root")
    if git(root, "branch", "--show-current") != "develop":
        raise RuntimeError("Expected develop branch")
    head = git(root, "rev-parse", "HEAD")
    if git(root, "rev-parse", "origin/develop") != head:
        raise RuntimeError("Local and remote develop do not agree")
    ancestor = subprocess.run(("git", "merge-base", "--is-ancestor", REVIEWED_HEAD, head),
                              cwd=root, check=False)
    if ancestor.returncode != 0:
        raise RuntimeError("Unreviewed HEAD lineage")
    changed = tuple(filter(None, git(root, "diff", "--name-only", REVIEWED_HEAD, head).splitlines()))
    if any(not (path == ".pytest_cache/v/cache/nodeids"
                or path.startswith("phase173_r4_r15r7_source_first_abstract_certificate/"))
           for path in changed):
        raise RuntimeError("Unreviewed committed change: " + repr(changed))
    if git(root, "diff", "--cached", "--name-only"):
        raise RuntimeError("Staged changes require review")
    dirty = tuple(filter(None, git(root, "diff", "--name-only").splitlines()))
    if any(name not in TARGETS and name != ".pytest_cache/v/cache/nodeids" for name in dirty):
        raise RuntimeError("Other tracked modifications require review: " + repr(dirty))
    for name, blob in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + name) != blob:
            raise RuntimeError("Dependency source blob mismatch: " + name)
        if name not in TARGETS and git(root, "hash-object", "--", name) != blob:
            raise RuntimeError("Dependency worktree changed: " + name)
    for name, expected in REVIEWED_PREVIOUS_FILES.items():
        file = root / name
        if not file.is_file() or sha(file.read_bytes()) != expected:
            raise RuntimeError("Unreviewed preceding phase file: " + name)
    originals, patched, states = reviewed_patch(root)
    if len(set(states.values())) > 1:
        raise RuntimeError("Mixed baseline/installed state requires review")
    print("PHASE173_R4_R15R8_HEAD=" + head, flush=True)
    print("PHASE173_R4_R15R8_HEAD_LINEAGE=PASS", flush=True)
    print("PHASE173_R4_R15R8_SOURCE_GUARD=PASS", flush=True)
    print("PHASE173_R4_R15R8_INSTALL_STATE=" + next(iter(states.values())), flush=True)
    return originals, patched, states


def install(root: Path, package: Path, *, dry_run: bool) -> None:
    originals, patched, states = preflight(root)
    preview = full_replacement_units(originals["phase165_r52_partial_proof.py"],
                                     originals["phase165_r55_nk_only_goal.py"])
    (package / "FULL_CHANGED_UNITS.md").write_text(
        "# Complete revised production classes and function\n\n" + preview,
        encoding="utf-8",
    )
    if dry_run:
        print("PHASE173_R4_R15R8_DRY_RUN=PASS", flush=True)
        print("PHASE173_R4_R15R8_PRODUCTION_EDIT=NONE", flush=True)
        return
    if next(iter(states.values())) == "PATCHED":
        print("PHASE173_R4_R15R8_ALREADY_INSTALLED=True", flush=True)
        return
    backup = package / "reviewed_originals"
    backup.mkdir(parents=True, exist_ok=True)
    for name, content in originals.items():
        (backup / (Path(name).name + ".bak")).write_bytes(content)
    try:
        for name, content in patched.items():
            destination = root / name
            tmp = destination.with_suffix(destination.suffix + ".r15r8_tmp")
            tmp.write_bytes(content)
            tmp.replace(destination)
    except Exception:
        for name, content in originals.items():
            (root / name).write_bytes(content)
        raise
    (package / REPORT_FILE).write_text(json.dumps({
        "phase": "173-R4-R15R8", "before": {k: sha(v) for k,v in originals.items()},
        "after": {k: sha(v) for k,v in patched.items()},
        "completed_named_proof_promoted": False,
    }, indent=2) + "\n", encoding="utf-8")
    print("PHASE173_R4_R15R8_PATCHED=" + ",".join(TARGETS), flush=True)


def restore(root: Path, package: Path):
    originals, patched, states = preflight(root)
    backup = package / "reviewed_originals"
    if next(iter(states.values())) != "PATCHED":
        print("PHASE173_R4_R15R8_RESTORE=SKIPPED_BASELINE", flush=True)
        return
    for name, original in originals.items():
        saved = backup / (Path(name).name + ".bak")
        if not saved.is_file() or sha(saved.read_bytes()) != sha(original):
            raise RuntimeError("Reviewed rollback backup missing: " + name)
    for name in TARGETS:
        (root / name).write_bytes((backup / (Path(name).name + ".bak")).read_bytes())
    print("PHASE173_R4_R15R8_ROLLBACK=PASS", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    package = Path(__file__).resolve().parent
    if args.restore:
        restore(root, package)
    else:
        install(root, package, dry_run=args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

### `audit.py`

```python
"""Source-first abstract evidence in public result model, without named completion."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from phase165_r52_partial_proof import (
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r8_public_abstract_sidecar.attach import (
    attach_certified_abstract_structure,
)
from phase173_r4_r15r8_public_abstract_sidecar.install import preflight


def inspect_k(k: int, bridge: object) -> dict[str, object]:
    """Check the canonical result type carries evidence without named promotion.

    This is a result-model audit; it does not claim the unrelated group search
    has successfully generated any named generator equality or Web display.
    """
    target = exact_prior_database_result(4, k)
    named = make_partial_proof_result(
        n=4, k=k, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(target,), diagnostics=("記名生成元の証明は未解決",),
    )
    enriched = attach_certified_abstract_structure(
        named, n=4, k=k, goal=target, bridge=bridge,
    )
    evidence = enriched.abstract_structure
    passed = bool(
        evidence is not None
        and evidence.group == enriched.target
        and enriched.status is ProofSearchStatus.SEARCH_FAILED
        and enriched.structure_status is GroupStructureStatus.UNKNOWN
        and enriched.conclusion is None
        and enriched.open_goals == (target,)
        and enriched.diagnostics == named.diagnostics
        and evidence.proof_step.inference_rule.match_guard(
            evidence.proof_step.premises, (),
        )
    )
    return {
        "k": k,
        "abstract_certified": passed,
        "invariant_summands": (
            [list(term) for term in evidence.invariant_summands]
            if evidence is not None else []
        ),
        "named_status_unchanged": enriched.status == named.status,
        "open_goals_unchanged": enriched.open_goals == named.open_goals,
        "named_conclusion_promoted": enriched.conclusion is not None,
        "named_generator_proved": False,
        "web_complete": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    preflight(root)
    shared = build_shared_typed_bridge()
    rows = [inspect_k(k, shared) for k in (4, 7, 8, 31)]
    # Run the real registered public selector once, not just a fabricated
    # presentation object. A name-labelled target remains incomplete.
    registered_target = exact_prior_database_result(4, 31)
    real_public = search_group_from_registered_goal(
        n=4, k=31, goal=registered_target, bridge=shared,
    )
    public_path_passed = bool(
        real_public.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
        and real_public.abstract_structure is not None
        and real_public.conclusion is None
        and real_public.open_goals
        and real_public.structure_status is GroupStructureStatus.UNKNOWN
        and real_public.abstract_structure.invariant_summands == (("finite", 2),) * 8
    )
    passed = bool(
        public_path_passed
        and all(row["abstract_certified"] for row in rows)
        and rows[-1]["invariant_summands"] == [["finite", 2]] * 8
        and all(row["named_status_unchanged"] and row["open_goals_unchanged"]
                and row["named_conclusion_promoted"] is False for row in rows)
    )
    report = {
        "phase": "173-R4-R15R8",
        "mode": "CANONICAL_PUBLIC_PARTIAL_RESULT_ABSTRACT_SIDECAR",
        "rows": rows,
        "public_selector_checked": True,
        "public_selector_abstract_attached": public_path_passed,
        "public_selector_named_status": real_public.status.value,
        "public_selector_open_goals": len(real_public.open_goals),
        "public_web_renderer_changed": False,
        "named_group_public_complete": False,
        "full_pytest_performed": False,
        "passed": passed,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    for row in rows:
        print("PHASE173_R4_R15R8_K=" + str(row["k"])
              + " ABSTRACT_ATTACHED=" + str(row["abstract_certified"])
              + " NAMED_STATUS_UNCHANGED=" + str(row["named_status_unchanged"]),
              flush=True)
    print("PHASE173_R4_R15R8_K31_REAL_PUBLIC_SELECTOR="
          + ("PASS" if public_path_passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R8_K31_PUBLIC_RESULT_ABSTRACT="
          + ("PASS" if passed else "FAIL"), flush=True)
    print("PHASE173_R4_R15R8_WEB_COMPLETE=False", flush=True)
    print("PHASE173_R4_R15R8_REPORT=" + str(args.output), flush=True)
    print("PHASE173_R4_R15R8_AUDIT=" + ("PASS" if passed else "FAIL"), flush=True)
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
```

### `tests/__init__.py`

```python
"""Tests for canonical partial results carrying separately certified abstract structure."""
```

### `tests/test_static.py`

```python
"""Offline source-patch regression tests. Never monkeypatch mathematical evidence."""
from __future__ import annotations

import ast

import pytest

from phase173_r4_r15r8_public_abstract_sidecar.patch_source import (
    END_BRANCH, END_REPLACEMENT, MODEL_FIELD, ORDER_BRANCH, ORDER_REPLACEMENT,
    transform_model, transform_selector,
)


def source_model() -> bytes:
    return (
        "from dataclasses import dataclass\nfrom typing import Any\n"
        "from proof import ProofStep\n"
        "@dataclass(frozen=True)\nclass PartialProofResult:\n"
        "    conclusion: Any | None = None\n"
        "    def __post_init__(self) -> None:\n"
        "        if self.status is ProofSearchStatus.NOT_SEARCHED and self.proven_steps:\n"
        "            pass\n"
    ).encode()


def source_selector() -> bytes:
    return (
        "def search_group_from_registered_goal():\n"
        "    if proof_order_catalog is None:\n"
        "        proof_order_catalog, order_diagnostic = query()\n"
        + ORDER_BRANCH + END_BRANCH
    ).encode()


@pytest.mark.parametrize("eol", ("\n", "\r\n"))
def test_model_transform_preserves_eol_and_adds_entire_class(eol: str) -> None:
    changed = transform_model(source_model().replace(b"\n", eol.encode()))
    text = changed.decode()
    assert "class CertifiedAbstractStructure:" in text
    assert MODEL_FIELD.strip() in text
    assert "from proof import ProofRule, ProofStep" in text
    assert (b"\r\n" in changed) == (eol == "\r\n")
    ast.parse(text)


@pytest.mark.parametrize("eol", ("\n", "\r\n"))
def test_selector_transform_preserves_eol_and_existing_goal_selection(eol: str) -> None:
    changed = transform_selector(source_selector().replace(b"\n", eol.encode()))
    text = changed.decode()
    assert "attach_certified_abstract_structure" in text
    assert "if n == 4 and k >= 3:" in text
    assert "result.status is ProofSearchStatus.COMPLETE" in text
    assert "return result" in text
    assert (b"\r\n" in changed) == (eol == "\r\n")
    ast.parse(text)


def test_missing_model_guard_refuses_unreviewed_source() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform_model(source_model().replace(b"from proof import ProofStep", b"from proof import Other"))


def test_duplicate_model_refuses_install() -> None:
    with pytest.raises(RuntimeError, match="already"):
        transform_model(source_model().replace(
            b"@dataclass(frozen=True)\nclass PartialProofResult:",
            b"@dataclass(frozen=True)\nclass CertifiedAbstractStructure:\n"
            b"    pass\n@dataclass(frozen=True)\nclass PartialProofResult:",
        ))


def test_selector_rejects_a_rewritten_end_branch() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform_selector(source_selector().replace(END_BRANCH.encode(), b"    return None\n"))


def test_selector_rejects_a_rewritten_order_branch() -> None:
    with pytest.raises(RuntimeError, match="anchor"):
        transform_selector(source_selector().replace(ORDER_BRANCH.encode(), b"    return None\n"))


def test_gating_retains_original_complete_condition() -> None:
    assert END_REPLACEMENT.startswith("    if result.status is ProofSearchStatus.COMPLETE")
    assert ORDER_REPLACEMENT.count("if n == 4 and k >= 3:") == 1


def test_transforms_are_not_double_applied() -> None:
    with pytest.raises(RuntimeError):
        transform_model(transform_model(source_model()))
    with pytest.raises(RuntimeError):
        transform_selector(transform_selector(source_selector()))
```

### `tests/test_integration.py`

```python
"""Repository-backed tests for the public result sidecar; not Web completion."""
from __future__ import annotations

from dataclasses import replace

import pytest

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import (
    CertifiedAbstractStructure,
    GroupStructureStatus,
    ProofSearchStatus,
    make_partial_proof_result,
)
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r7_source_first_abstract_certificate.search import (
    search_source_first_abstract,
)
from phase173_r4_r15r8_public_abstract_sidecar.attach import (
    attach_certified_abstract_structure,
)
from proof import ProofRule, ProofStep


@pytest.fixture(scope="module")
def verified_k31():
    """Use a real source-first certificate and the real registry once."""
    bridge = build_shared_typed_bridge()
    goal = exact_prior_database_result(4, 31)
    certificate = search_source_first_abstract(k=31, bridge=bridge)
    assert certificate is not None
    assert certificate.root_step.inference_rule.match_guard(
        certificate.root_step.premises, (),
    )
    return bridge, goal, certificate


def _pending(goal):
    return make_partial_proof_result(
        n=4, k=31, status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=(goal,), diagnostics=("named goal unresolved",),
    )


def test_genuine_abstract_proof_attached_without_named_promotion(verified_k31) -> None:
    bridge, goal, certificate = verified_k31
    base = _pending(goal)
    result = attach_certified_abstract_structure(
        base, n=4, k=31, goal=goal, bridge=bridge,
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert result.open_goals == base.open_goals
    assert result.structure_status is GroupStructureStatus.UNKNOWN
    assert result.diagnostics == base.diagnostics
    assert result.abstract_structure is not None
    assert result.abstract_structure.invariant_summands == (("finite", 2),) * 8
    assert result.abstract_structure.proof_step.rule is ProofRule.INFERENCE
    assert result.abstract_structure.proof_step.conclusion == certificate.conclusion


def test_forged_named_complete_or_mismatched_group_is_rejected(verified_k31) -> None:
    bridge, goal, _ = verified_k31
    result = attach_certified_abstract_structure(
        _pending(goal), n=4, k=31, goal=goal, bridge=bridge,
    )
    assert result.abstract_structure is not None
    with pytest.raises(ValueError, match="verified inference root"):
        replace(result.abstract_structure, group=TodaPrimaryGroup(36, 4))
    with pytest.raises(ValueError, match="abstract-only"):
        replace(result, target=TodaPrimaryGroup(36, 4))
    with pytest.raises(ValueError, match="abstract-only"):
        replace(result, structure_status=GroupStructureStatus.KNOWN)
    fake = ProofStep(result.abstract_structure.proof_step.conclusion, (), ProofRule.GIVEN)
    with pytest.raises(ValueError, match="verified inference root"):
        replace(result.abstract_structure, proof_step=fake)


def test_nonmatching_target_and_other_sphere_preserve_old_status(verified_k31) -> None:
    bridge, goal, _ = verified_k31
    base = _pending(goal)
    assert attach_certified_abstract_structure(base, n=4, k=31,
                                               goal=exact_prior_database_result(4, 4),
                                               bridge=bridge) is base
    assert attach_certified_abstract_structure(base, n=5, k=31,
                                               goal=goal, bridge=bridge) is base


def test_canonical_public_selector_preserves_named_partial(verified_k31, monkeypatch) -> None:
    """Only mock the unrelated named search; abstract evidence is authentic."""
    import phase165_r55_nk_only_goal as public
    import phase173_r4_r15r8_public_abstract_sidecar.attach as attachment

    bridge, goal, certificate = verified_k31
    pending = _pending(goal)
    monkeypatch.setattr(public, "search_shared_group_goal", lambda **kwargs: pending)
    monkeypatch.setattr(public, "resolve_specialized_goal_citing_id", lambda *args: None)
    monkeypatch.setattr(attachment, "search_source_first_abstract",
                        lambda **kwargs: certificate)
    result = public.search_group_from_registered_goal(
        n=4, k=31, bridge=bridge, goal=goal, proof_order_catalog=object(),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.conclusion is None
    assert result.open_goals == (goal,)
    assert result.abstract_structure is not None
    assert result.abstract_structure.invariant_summands == (("finite", 2),) * 8
```

### `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'R15R8 git fetch failed' }

    python -m phase173_r4_r15r8_public_abstract_sidecar.install --root "$Root" --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R8 source guard / preview failed' }

    python -m pytest -q phase173_r4_r15r8_public_abstract_sidecar/tests/test_static.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R8 static tests failed' }

    if ($DryRun) {
        Write-Output 'PHASE173_R4_R15R8_DRY_RUN=PASS'
        Write-Output 'PHASE173_R4_R15R8_PRODUCTION_EDIT=NONE'
    } else {
        python -m phase173_r4_r15r8_public_abstract_sidecar.install --root "$Root"
        if ($LASTEXITCODE -ne 0) { throw 'R15R8 installation failed' }
        try {
            python -m pytest -q `
                phase173_r4_r15r8_public_abstract_sidecar/tests/test_integration.py `
                phase173_r4_r15r7_source_first_abstract_certificate/tests/test_integration.py `
                phase173_r4_r15r6_abstract_toda44_rule/tests/test_integration.py `
                phase173_r4_r10_general_toda56_core/tests/test_core.py `
                phase173_r4_r11_zero_public_connection/tests/test_route.py
            if ($LASTEXITCODE -ne 0) { throw 'R15R8 focused pytest failed' }
            Write-Output 'PHASE173_R4_R15R8_FOCUSED_PYTEST=PASS'

            python -m phase173_r4_r15r8_public_abstract_sidecar.audit --root "$Root" `
                --output (Join-Path $PSScriptRoot 'public_abstract_sidecar_report.json')
            if ($LASTEXITCODE -ne 0) { throw 'R15R8 audit failed' }
            Write-Output 'PHASE173_R4_R15R8_PHASE_COMPLETED=False'
        } catch {
            python -m phase173_r4_r15r8_public_abstract_sidecar.install --root "$Root" --restore
            throw
        }
    }
} finally {
    Pop-Location
}
```

## 限定 pytest と完了条件

DryRun は `tests/test_static.py` を実行。通常実行は R15R8 integration、R15R7、R15R6、既存一般 Core、R4-R11 公開 Web の限定テストを実行する。`k=31` の実公開群検索で `abstract_structure` が添付されても、記名群の未解決 Goal と status が保持されることを監査する。全体 pytest は Phase 最後に実施する。
