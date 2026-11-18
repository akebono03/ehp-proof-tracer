# Phase 175 R4R10 — 完全コードと置換位置

本番変更対象：`phase165_r52_r9_shared_math.py` の `build_shared_typed_bridge()` と `shared_expansion_provider()` の2関数のみ。既存 import を変更しない。関数は数行の差分ではなく AST で検証した関数全文で置き換える。DryRun と本実行の出力先に `build_shared_typed_bridge_FULL_AFTER.py`、`shared_expansion_provider_FULL_AFTER.py`、`phase165_r52_r9_shared_math_FULL_AFTER.py` の3ファイルとして全文を書き出す。これらは現行 Git HEAD のコードから生成するため、将来の未確認変更を混ぜない。

新規追加位置：`phase175_r4r10_cited_58_prop25_public` 直下の4つの Python モジュールと `tests/` 内の4テストモジュール。以下はそれぞれの import、クラス、関数、テスト関数を省略せず全文掲載したもの。

## `__init__.py`

```python
"""Cited Toda (5.8) and Proposition 2.5 source-first proof search bridge."""
```

## `source.py`

```python
"""Two independently pinned Toda source statements, never a pi_9^5 leaf.

(5.8) is cited as a signed Delta image. Proposition 2.5 is cited as a
universal conditional composition law. Both are adopted Japanese TeX
transcriptions; the original publication has not been independently checked.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, Multiple, Sum, Suspension
from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)

PACKAGE = "phase175_r4r10_cited_58_prop25_public"
ROOT = Path(__file__).resolve().parents[1]
CHAPTER_2 = "sources/toda/Toda_02_2.tex"
CHAPTER_5 = "sources/toda/Toda_05_2.tex"
CHAPTER_2_BLOB = "ed3667788805a429140dedf5d183736e43e0f2c3"
CHAPTER_5_BLOB = "579661138928499ba04a51327f686d9b971b5314"
EQUATION_REFERENCE_ID = "toda:(5.8)"
PROPOSITION_REFERENCE_ID = "toda:Proposition 2.5"
EQUATION_ASSERTION_ID = "toda:175:r4r10:equation58"
PROPOSITION_ASSERTION_ID = "toda:175:r4r10:proposition25"


@dataclass(frozen=True)
class CitedToda58SignedDelta:
    """The typed, signed *published premise*, not an inferred group result."""

    statement: TodaDeltaImageUpToSignStatement
    locator: str = "(5.8)"


@dataclass(frozen=True)
class CitedTodaProp25:
    """Source identity of the universal conditional Delta composition law."""

    locator: str = "Proposition 2.5"


def git_blob_sha(value: bytes) -> str:
    return sha1(b"blob " + str(len(value)).encode("ascii") + b"\x00" + value).hexdigest()


def vetted_source(path: Path, expected_blob: str) -> str:
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n")
    choices = (data, normalized, normalized.replace(b"\n", b"\r\n"))
    if not any(git_blob_sha(value) == expected_blob for value in choices):
        raise ValueError("R4R10_SOURCE_BLOB_DRIFT: " + str(path))
    return normalized.decode("utf-8-sig")


def source_positions(root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST) -> dict[str, int]:
    """Verify both complete source blocks and the recorded source order."""
    if not isinstance(root, Path) or not isinstance(manifest, Path):
        raise TypeError("root and manifest must be pathlib.Path")
    ch2 = vetted_source(root / CHAPTER_2, CHAPTER_2_BLOB)
    ch5 = vetted_source(root / CHAPTER_5, CHAPTER_5_BLOB)
    label25 = r"\begin{proposition}\label{prop:2.5}"
    label58 = r"\begin{equation}\label{eq:5.8}"
    if ch2.count(label25) != 1 or ch5.count(label58) != 1:
        raise ValueError("R4R10_TODA_ANCHOR_NOT_UNIQUE")
    prop25 = ch2.split(label25, 1)[1].split(r"\end{proposition}", 1)[0]
    eq58 = ch5.split(label58, 1)[1].split(r"\end{equation}", 1)[0]
    if not all(part in prop25 for part in (
        r"\alpha\in\pi_{i+1}(S^{2m+1})",
        r"\beta\in \pi_{j-1}(S^{i-1})",
        r"\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)",
        r"j<3m-1", r"2\)-primary", "等号",
    )):
        raise ValueError("R4R10_PROP25_SOURCE_CHANGED")
    if r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')" not in eq58:
        raise ValueError("R4R10_EQ58_SOURCE_CHANGED")
    if ch5.index(label58) >= ch5.index(r"\begin{proposition}\label{prop:5.8}"):
        raise ValueError("R4R10_EQ58_SOURCE_ORDER_CHANGED")
    positions, _, _ = _load_manifest_reference_order(manifest)
    expected = (
        positions.get(PROPOSITION_REFERENCE_ID),
        positions.get(EQUATION_REFERENCE_ID),
        positions.get("toda:Proposition 5.8"),
    )
    if (not all(type(v) is int and v > 0 for v in expected)
            or not (expected[0] < expected[1] < expected[2])):
        raise ValueError("R4R10_SOURCE_POSITION_INVALID")
    return {PROPOSITION_REFERENCE_ID: expected[0], EQUATION_REFERENCE_ID: expected[1]}


def canonical_toda58() -> TodaDeltaImageUpToSignStatement:
    """Literal typed interpretation of (5.8), retaining the unresolved ±."""
    iota9 = HomotopyElement("ι₉", 9, 9, 9, GeneratorSymbol("ι", index=9))
    nu4 = HomotopyElement("ν₄", 4, 7, 4, GeneratorSymbol("ν", index=4))
    nu_prime = HomotopyElement(
        "ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"),
    )
    return TodaDeltaImageUpToSignStatement(
        map=TodaDeltaMap(TodaPrimaryGroup(9, 9), TodaPrimaryGroup(7, 4)),
        element=iota9,
        positive_value=Sum(Multiple(2, nu4), Multiple(-1, Suspension(nu_prime))),
    )


def build_cited_58_prop25_sources(
    root: Path = ROOT, manifest: Path = DEFAULT_MANIFEST,
) -> RegistryBridgeResult:
    positions = source_positions(root, manifest)
    eq = CitedToda58SignedDelta(canonical_toda58())
    prop = CitedTodaProp25()
    registry = UnifiedStatementRegistry()
    links = []
    for ref_id, assertion_id, kind, statement in (
        (EQUATION_REFERENCE_ID, EQUATION_ASSERTION_ID, ReferenceKind.EQUATION, eq),
        (PROPOSITION_REFERENCE_ID, PROPOSITION_ASSERTION_ID, ReferenceKind.PROPOSITION, prop),
    ):
        locator = statement.locator
        registry.add_reference(LiteratureEntry(
            reference_id=ref_id,
            kind=kind,
            locator=locator,
            source_id=(CHAPTER_5 if kind is ReferenceKind.EQUATION else CHAPTER_2)
            + " (adopted Japanese TeX; original edition unverified)",
            publication_position=positions[ref_id],
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=ref_id,
            kind=AssertionKind.STATEMENT,
            content=statement,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope="source formula only; not pi_9^5 group result",
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=statement,
            premises=(),
            rule=ProofRule.GIVEN,
            inference_rule=InferenceRule(
                name="Cited Toda " + locator,
                literature_reference=LiteratureReference(
                    label="Toda " + locator, locator=locator,
                ),
            ),
        )))
    return RegistryBridgeResult(registry, (), tuple(links))
```

## `provider.py`

```python
"""Citation-backed backward proposals for Toda (5.8) and Proposition 2.5.

No group result, source, or ProofStep is created here. The common recursive
search must independently obtain the two cited GIVEN parents and the inferred
signed Delta and identity-composition parents before completing any result.
"""
from __future__ import annotations

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r3_recursive_search import GoalExpansion
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r7_prop25_typed_composition.rule import (
    prop25_inputs,
    prop25_signed_composition_rule,
)
from phase175_r4r10_cited_58_prop25_public.source import (
    CitedToda58SignedDelta,
    CitedTodaProp25,
    canonical_toda58,
)
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    Relation,
    RelationType,
)
from toda_rules import TodaDeltaImageUpToSignStatement
from unified_statement_registry import AssertionOrigin


SOURCE58_RULE = "read cited Toda (5.8) signed Delta image"
ETA_IDENTITY_RULE = "identity composition and cited eta suspension definition"
CITED_PROP25_RULE = "cited Toda Proposition 2.5 conditional composition"


def screened_cited_facts(bridge: RegistryBridgeResult) -> tuple[object, ...]:
    """Read only exact fixed-statement GIVEN links of the screened bridge."""
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
    selected = []
    for link in bridge.proof_links:
        if link.step is None or link.step.rule is not ProofRule.GIVEN:
            continue
        assertion = bridge.registry.assertion(link.assertion_id)
        if (assertion.origin is not AssertionOrigin.FIXED_STATEMENT
                or link.step.premises or assertion.content != link.step.conclusion):
            continue
        if link.step.conclusion not in selected:
            selected.append(link.step.conclusion)
    return tuple(selected)


def expand_cited_toda58(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """A signed typed reading of one already-cited source claim."""
    if not isinstance(goal, TodaDeltaImageUpToSignStatement):
        return ()
    sources = tuple(
        claim for claim in available
        if type(claim) is CitedToda58SignedDelta
        and claim.locator == "(5.8)"
        and claim.statement == canonical_toda58()
        and claim.statement == goal
    )
    if len(sources) != 1:
        return ()
    source = sources[0]

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[0].conclusion == source
            and goal == canonical_toda58()
        )

    return (GoalExpansion(InferenceRule(
        name=SOURCE58_RULE,
        description="Translate the precisely cited (5.8) into its typed signed image; do not choose ±.",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=CitedToda58SignedDelta,
            statement_pattern=source,
        ),),
        match_guard=guard,
        conclusion_pattern=goal,
    ), (source,)),)


def eta_identity_indices(goal: object) -> int | None:
    """Recognize iota_(n+2) o E^2(eta_n) = eta_(n+2) for n >= 2."""
    if (not isinstance(goal, Relation)
            or goal.relation_type is not RelationType.EQUALITY
            or not isinstance(goal.lhs, Composition)
            or not isinstance(goal.lhs.left, HomotopyElement)
            or not isinstance(goal.lhs.right, IteratedSuspension)
            or type(goal.lhs.right.exponent) is not int
            or goal.lhs.right.exponent != 2
            or not isinstance(goal.lhs.right.expression, HomotopyElement)
            or not isinstance(goal.rhs, HomotopyElement)):
        return None
    alpha, beta, gamma = goal.lhs.left, goal.lhs.right.expression, goal.rhs
    n = beta.target
    if type(n) is not int or n < 2:
        return None
    if (alpha.source != n + 2 or alpha.target != n + 2
            or alpha.dimension != n + 2
            or alpha.generator != GeneratorSymbol("ι", index=n + 2)
            or beta.dimension != n or beta.source != n + 1 or beta.target != n
            or beta.generator != GeneratorSymbol("η", index=n)
            or gamma.dimension != n + 2
            or gamma.source != n + 3 or gamma.target != n + 2
            or gamma.generator != GeneratorSymbol("η", index=n + 2)):
        return None
    return n


def expand_eta_identity(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Derive the definitional identity from the cited universal eta notation."""
    if (eta_identity_indices(goal) is None
            or available.count(TodaEtaFamilyGeneralDefinition()) != 1):
        return ()
    definition = TodaEtaFamilyGeneralDefinition()

    def guard(premises, bindings):
        return (
            len(premises) == 1
            and premises[0].rule is ProofRule.GIVEN
            and premises[0].conclusion == definition
            and not premises[0].premises
            and eta_identity_indices(goal) is not None
        )

    return (GoalExpansion(InferenceRule(
        name=ETA_IDENTITY_RULE,
        description="Use cited eta_n=E^(n-2) eta_2 and the identity map, not a new theorem.",
        premise_patterns=(PremisePattern(
            proof_rule=ProofRule.GIVEN,
            statement_type=TodaEtaFamilyGeneralDefinition,
            statement_pattern=definition,
        ),),
        conclusion_pattern=goal,
        match_guard=guard,
    ), (definition,)),)


def expand_cited_prop25(
    goal: object, available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Use the *general* R4R7 rule with an independent Prop 2.5 citation."""
    if (not isinstance(goal, TodaDeltaImageUpToSignStatement)
            or not isinstance(goal.positive_value, Composition)):
        return ()
    props = tuple(x for x in available if type(x) is CitedTodaProp25
                  and x.locator == "Proposition 2.5")
    signed_sources = tuple(x for x in available if type(x) is CitedToda58SignedDelta
                           and x.locator == "(5.8)"
                           and x.statement == canonical_toda58())
    if len(props) != 1 or len(signed_sources) != 1:
        return ()
    source = signed_sources[0].statement
    beta = goal.positive_value.right
    identity = Relation(
        lhs=Composition(source.element, IteratedSuspension(beta, 2)),
        rhs=goal.element,
        relation_type=RelationType.EQUALITY,
    )
    if (prop25_inputs(goal, source, identity) != (source, identity)
            or eta_identity_indices(identity) is None):
        return ()
    # Preserve the existing R4R7 condition/guard and require a source citation.
    base = prop25_signed_composition_rule(goal, source, identity)
    prop = props[0]

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.GIVEN
            and not premises[0].premises
            and premises[0].conclusion == prop
            and base.match_guard(premises[1:], ())
        )

    return (GoalExpansion(InferenceRule(
        name=CITED_PROP25_RULE,
        description="Cited Proposition 2.5, with R4R7 exact arithmetic guard and both proved inputs.",
        literature_reference=LiteratureReference(
            label="Toda Proposition 2.5", locator="Proposition 2.5",
        ),
        premise_patterns=(
            PremisePattern(proof_rule=ProofRule.GIVEN,
                           statement_type=CitedTodaProp25, statement_pattern=prop),
        ) + base.premise_patterns,
        match_guard=guard,
        conclusion_pattern=goal,
    ), (prop, source, identity)),)


def build_cited_58_prop25_provider(bridge: RegistryBridgeResult):
    """Only expose candidate expansions; all premises use ordinary proof search."""
    available = screened_cited_facts(bridge)

    def expand(goal: object) -> tuple[GoalExpansion, ...]:
        return (
            expand_cited_toda58(goal, available)
            + expand_eta_identity(goal, available)
            + expand_cited_prop25(goal, available)
        )

    return expand
```

## `installer.py`

```python
"""Pinned two-complete-function installation in the shared production path.

Never edits imports or unrelated functions. Writes a complete full-function
replacement to the report folder, allowing independent human inspection.
"""
from __future__ import annotations

import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

TARGET = Path("phase165_r52_r9_shared_math.py")
EXPECTED_COMMITTED_BLOB = "df4e0f834e9bc321f338ec10b363c79d82623457"
BRIDGE_FUNCTION = "build_shared_typed_bridge"
PROVIDER_FUNCTION = "shared_expansion_provider"

BRIDGE_ANCHOR = '''        sources = sources + (
            build_cited_lower_delta_sources(Path(__file__).resolve().parent),
        )
'''
BRIDGE_ADDITION = '''        # Phase 175 R4R10: source-only (5.8) and universal Proposition 2.5.
        from phase175_r4r10_cited_58_prop25_public.source import (
            build_cited_58_prop25_sources,
        )
        sources = sources + (build_cited_58_prop25_sources(),)
'''
PROVIDER_ANCHOR = '''    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("bridge must be RegistryBridgeResult")
'''
PROVIDER_ADDITION = '''    # Phase 175 R4R10: screened literature claims produce only open subgoals.
    from phase175_r4r10_cited_58_prop25_public.provider import (
        build_cited_58_prop25_provider,
    )
    extra_providers = (build_cited_58_prop25_provider(bridge),) + tuple(extra_providers)
'''


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )
    if result.returncode:
        raise RuntimeError("R4R10_GIT_FAILED: " + " ".join(args) + " " + result.stderr)
    return result.stdout.strip()


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def replace_full_function(
    original: str, function_name: str, anchor: str, addition: str,
) -> tuple[str, str]:
    """Replace one entire AST function; refuse moved anchors or duplicates."""
    tree = ast.parse(original)
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if len(found) != 1:
        raise RuntimeError("R4R10_FUNCTION_NOT_UNIQUE: " + function_name)
    fn = found[0]
    lines = original.splitlines(keepends=True)
    before = "".join(lines[fn.lineno - 1:fn.end_lineno])
    if addition in before:
        if before.count(addition) != 1:
            raise RuntimeError("R4R10_INSERTION_DUPLICATE: " + function_name)
        return original, before
    if before.count(anchor) != 1:
        raise RuntimeError("R4R10_ANCHOR_CHANGED: " + function_name)
    after = before.replace(anchor, anchor + addition, 1)
    updated = "".join(lines[:fn.lineno - 1]) + after + "".join(lines[fn.end_lineno:])
    ast.parse(updated)
    return updated, after


def plan(root: Path) -> tuple[Path, bytes, bytes, dict[str, str]]:
    """Compute the two full functions with Git pin and EOL preservation."""
    path = root / TARGET
    if not path.is_file():
        raise RuntimeError("R4R10_PRODUCTION_FILE_MISSING")
    if git(root, "rev-parse", "HEAD:" + TARGET.as_posix()) != EXPECTED_COMMITTED_BLOB:
        raise RuntimeError("R4R10_UNREVIEWED_PRODUCTION_COMMIT")
    current_bytes = path.read_bytes()
    normalized = current_bytes.replace(b"\r\n", b"\n")
    original = normalized.decode("utf-8")
    after_bridge, whole_bridge = replace_full_function(
        original, BRIDGE_FUNCTION, BRIDGE_ANCHOR, BRIDGE_ADDITION,
    )
    after_both, whole_provider = replace_full_function(
        after_bridge, PROVIDER_FUNCTION, PROVIDER_ANCHOR, PROVIDER_ADDITION,
    )
    eol = b"\r\n" if b"\r\n" in current_bytes else b"\n"
    result = after_both.encode("utf-8")
    if eol == b"\r\n":
        result = result.replace(b"\n", b"\r\n")
    # Only unchanged committed source or an exactly identical completed patch.
    if (git_blob_sha(normalized) != EXPECTED_COMMITTED_BLOB
            and current_bytes != result):
        raise RuntimeError("R4R10_UNREVIEWED_LOCAL_PRODUCTION_CHANGE")
    return path, current_bytes, result, {
        BRIDGE_FUNCTION: whole_bridge,
        PROVIDER_FUNCTION: whole_provider,
    }


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    if not isinstance(root, Path) or not isinstance(output, Path):
        raise TypeError("root and output must be pathlib.Path")
    path, before, after, functions = plan(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "build_shared_typed_bridge_FULL_AFTER.py").write_text(
        functions[BRIDGE_FUNCTION], encoding="utf-8",
    )
    (output / "shared_expansion_provider_FULL_AFTER.py").write_text(
        functions[PROVIDER_FUNCTION], encoding="utf-8",
    )
    (output / "phase165_r52_r9_shared_math_FULL_AFTER.py").write_bytes(after)
    changed = before != after
    if not dry_run and changed:
        fd, temp_name = tempfile.mkstemp(prefix="r4r10_", suffix=".py", dir=path.parent)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(after)
            os.replace(temp_name, path)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
    return {
        "production_path": TARGET.as_posix(),
        "patch_required": changed,
        "patch_applied": changed and not dry_run,
        "after_git_blob": git_blob_sha(after),
        "two_full_functions_exported": True,
    }
```

## `audit.py`

```python
"""Phase 175 R4R10: source-first cited (5.8) + Prop 2.5 public wiring.

Only the full shared bridge/provider functions are changed. No direct pi_9^5
conclusion is registered. A real proof replay is limited to the source-backed
Delta-composition statement, not the target homotopy group.
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

from phase175_r4r10_cited_58_prop25_public import installer
from phase175_r4r10_cited_58_prop25_public.source import (
    EQUATION_REFERENCE_ID,
    PROPOSITION_REFERENCE_ID,
    build_cited_58_prop25_sources,
    canonical_toda58,
    source_positions,
)

PACKAGE = "phase175_r4r10_cited_58_prop25_public"
PRIOR_PACKAGE = "phase175_r4r8_signed_delta_kernel_frontier"
PRIOR_GATE = "PASS_R4R8_SIGNED_DELTA_KERNEL_FRONTIER_RECORDED_NOT_PUBLIC"
DRY_GATE = "PASS_R4R10_CITED_58_PROP25_DRYRUN"
FINAL_GATE = "PASS_R4R10_CITED_58_PROP25_SHARED_CONNECTED_PI95_PENDING"
BASE_HEAD = "51f9907ac3116c78778d75864775d30d095efa5c"
R4R8_HEAD = "5c263cc69dc409842d3a13cb3fc65c2347df0bef"
REVIEWED_BLOBS = {
    "proof.py": "2eb683053eaf7146bd89afbc581a386af08b8060",
    "expression.py": "7f7cd97468cd753643369f54774ee9892968c345",
    "homotopy_groups.py": "883faf1b4a067485c9127f14dbb575aaa195960e",
    "toda_rules.py": "77f4159644f10eff65a79f6e528cf7b471c6ddc9",
    "phase175_r4r7_prop25_typed_composition/rule.py": "e957752baf93f75352d106e53205730af9a02b4d",
    "phase165_r12_r20_eta_definition.py": "9d7058607c102c47265a192735180cac36321910",
    "sources/toda/Toda_02_2.tex": "ed3667788805a429140dedf5d183736e43e0f2c3",
    "sources/toda/Toda_05_2.tex": "579661138928499ba04a51327f686d9b971b5314",
}


def git(root: Path, *args: str, allowed_failure: bool = False) -> tuple[int, str]:
    process = subprocess.run(
        ["git", *args], cwd=root, text=True, capture_output=True,
        encoding="utf-8", errors="replace", check=False,
    )
    if process.returncode and not allowed_failure:
        raise RuntimeError("R4R10_GIT_FAILED: " + " ".join(args) + " " + process.stderr.strip())
    return process.returncode, process.stdout.strip()


def preflight(root: Path) -> dict[str, object]:
    if Path(git(root, "rev-parse", "--show-toplevel")[1]).resolve() != root.resolve():
        raise RuntimeError("R4R10_NOT_REPOSITORY_ROOT")
    if git(root, "branch", "--show-current")[1] != "develop":
        raise RuntimeError("R4R10_WRONG_BRANCH")
    head = git(root, "rev-parse", "HEAD")[1]
    if git(root, "merge-base", "--is-ancestor", BASE_HEAD, head, allowed_failure=True)[0]:
        raise RuntimeError("R4R10_UNREVIEWED_HEAD_ANCESTRY")
    paths = git(root, "diff", "--name-only", BASE_HEAD, head)[1].splitlines()
    if any(not (path.startswith("phase175_r4r8_signed_delta_kernel_frontier/")
                or path.startswith("phase175_r4r9_general_cyclic_kernel_isolated/")
                or path == ".pytest_cache/v/cache/nodeids") for path in paths):
        raise RuntimeError("R4R10_UNREVIEWED_COMMITTED_PATHS: " + repr(paths))
    for path, expected in REVIEWED_BLOBS.items():
        if git(root, "rev-parse", "HEAD:" + path)[1] != expected:
            raise RuntimeError("R4R10_SOURCE_BLOB_DRIFT: " + path)
    target, before, after, _ = installer.plan(root)
    tracked = set(git(root, "diff", "--name-only")[1].splitlines())
    tracked.update(git(root, "diff", "--cached", "--name-only")[1].splitlines())
    if any(path not in (installer.TARGET.as_posix(), ".pytest_cache/v/cache/nodeids")
           for path in tracked):
        raise RuntimeError("R4R10_UNREVIEWED_TRACKED_CHANGES: " + repr(sorted(tracked)))
    if installer.TARGET.as_posix() in tracked and before != after:
        raise RuntimeError("R4R10_PRODUCTION_DIRTY_NOT_INSTALLED")
    return {
        "head": head,
        "reviewed_base_head": BASE_HEAD,
        "reviewed_r4r8_head": R4R8_HEAD,
        "intervening_paths": sorted(paths),
        "source_blob_pins_checked": len(REVIEWED_BLOBS),
        "production_patch_already_applied": before == after,
    }


def validate_prior(report: object) -> dict[str, object]:
    if not isinstance(report, dict):
        raise RuntimeError("R4R10_R4R8_REPORT_INVALID")
    expected = {
        "phase": "175-R4R8",
        "gate": PRIOR_GATE,
        "dry_run": False,
        "new_given": 0,
        "new_mathematical_rules": 0,
        "production_changes": [],
        "rule_connected_to_public": False,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    if any(report.get(k) != v for k, v in expected.items()):
        raise RuntimeError("R4R10_R4R8_REPORT_SCOPE_INVALID")
    groups = report.get("groups")
    obligations = report.get("unresolved_obligations")
    if (not isinstance(groups, dict)
            or groups.get("prior_presentations_identified") != 2
            or groups.get("group_presentations_do_not_certify_E_actions") is not True
            or not isinstance(obligations, list)
            or len(obligations) != 6):
        raise RuntimeError("R4R10_R4R8_REPORT_EVIDENCE_INVALID")
    return {
        "prior_gate": PRIOR_GATE,
        "prior_unresolved_obligations": len(obligations),
        "prior_math_proofs_not_adopted": True,
    }


def find_prior(explicit: Path | None) -> Path:
    if explicit is not None:
        found = explicit.expanduser().resolve()
        if not found.is_file():
            raise RuntimeError("R4R10_R4R8_REPORT_NOT_FOUND: " + str(found))
        return found
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PRIOR_PACKAGE
    failed = []
    for candidate in sorted(folder.glob("*/report.json"), reverse=True):
        try:
            validate_prior(json.loads(candidate.read_text(encoding="utf-8")))
            return candidate
        except (OSError, UnicodeError, ValueError, RuntimeError) as exc:
            failed.append(str(candidate) + " => " + str(exc))
    raise RuntimeError(
        "R4R10_SUCCESSFUL_R4R8_REPORT_MISSING: " + str(folder)
        + ("; " + " | ".join(failed[:3]) if failed else "")
    )


def sample_delta_eta9():
    """Construct only a typed *query*, not a verified result or proof."""
    from expression import Composition, GeneratorSymbol, HomotopyElement
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from toda_rules import TodaDeltaImageUpToSignStatement
    signed = canonical_toda58()
    beta = HomotopyElement("η₇", 7, 8, 7, GeneratorSymbol("η", index=7))
    gamma = HomotopyElement("η₉", 9, 10, 9, GeneratorSymbol("η", index=9))
    return TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(signed.positive_value, beta),
    )


def replay_cited_prop25() -> dict[str, object]:
    """Replay only the separately cited source route with typed ProofSteps."""
    from proof import ProofRule, apply_inference_match, find_inference_matches_for_rule
    from phase165_r12_r20_eta_definition import build_cited_eta_family_definition
    from phase175_r4r10_cited_58_prop25_public.provider import (
        build_cited_58_prop25_provider,
    )
    from phase163_r4_registry_bridge import RegistryBridgeResult
    from unified_statement_registry import UnifiedStatementRegistry
    source = build_cited_58_prop25_sources()
    eta = build_cited_eta_family_definition(
        Path(__file__).resolve().parents[1] / "sources" / "toda" / "Toda_05_2.tex",
    )
    registry = UnifiedStatementRegistry()
    for bridge in (source, eta):
        for ref in bridge.registry._references.values():
            registry.add_reference(ref)
        for assertion in bridge.registry._assertions.values():
            registry.add_assertion(assertion)
    combined = RegistryBridgeResult(
        registry, (), source.proof_links + eta.proof_links,
    )
    expand = build_cited_58_prop25_provider(combined)
    goal = sample_delta_eta9()
    proposals = expand(goal)
    if len(proposals) != 1 or len(proposals[0].subgoals) != 3:
        raise RuntimeError("R4R10_CITED_PROP25_NOT_EXPOSED")
    prop, signed, identity = proposals[0].subgoals
    source_givens = {type(link.step.conclusion): link.step
                     for link in combined.proof_links if link.step is not None}
    from phase175_r4r10_cited_58_prop25_public.source import CitedToda58SignedDelta, CitedTodaProp25
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    def inferred(subgoal: object, premise):
        opts = expand(subgoal)
        if len(opts) != 1:
            raise RuntimeError("R4R10_PARENTS_NOT_EXPOSED: " + repr(subgoal))
        matches = find_inference_matches_for_rule(opts[0].rule, (premise,))
        if len(matches) != 1:
            raise RuntimeError("R4R10_PARENTS_NOT_MATCHED")
        return apply_inference_match(matches[0])
    signed_step = inferred(signed, source_givens[CitedToda58SignedDelta])
    identity_step = inferred(identity, source_givens[TodaEtaFamilyGeneralDefinition])
    matches = find_inference_matches_for_rule(
        proposals[0].rule,
        (source_givens[CitedTodaProp25], signed_step, identity_step),
    )
    if len(matches) != 1:
        raise RuntimeError("R4R10_PROP25_NOT_MATCHED")
    final = apply_inference_match(matches[0])
    if (final.rule is not ProofRule.INFERENCE or final.conclusion != goal
            or len(final.premises) != 3
            or signed_step.rule is not ProofRule.INFERENCE
            or identity_step.rule is not ProofRule.INFERENCE):
        raise RuntimeError("R4R10_REPLAY_NOT_VERIFIED")
    return {
        "conclusion_is_signed": True,
        "proposition_2_5_citation_present": True,
        "equation_5_8_citation_present": True,
        "eta_family_citation_present": True,
        "signed_parent_inferred": True,
        "composition_identity_parent_inferred": True,
        "root_group_conclusion_inferred": False,
        "full_search_performed": False,
    }


def inspect_public_connection() -> dict[str, object]:
    """Verify all three real backward routes in the default shared registry."""
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase175_r4r10_cited_58_prop25_public.provider import (
        CITED_PROP25_RULE, ETA_IDENTITY_RULE, SOURCE58_RULE,
        screened_cited_facts,
    )
    from phase175_r4r10_cited_58_prop25_public.source import (
        CitedToda58SignedDelta, CitedTodaProp25,
    )
    bridge = build_shared_typed_bridge()
    facts = screened_cited_facts(bridge)
    if (sum(type(x) is CitedToda58SignedDelta for x in facts) != 1
            or sum(type(x) is CitedTodaProp25 for x in facts) != 1
            or facts.count(TodaEtaFamilyGeneralDefinition()) != 1):
        raise RuntimeError("R4R10_PUBLIC_CITED_SOURCES_NOT_SCREENED")
    expand = shared_expansion_provider(bridge)
    proposals = expand(sample_delta_eta9())
    selected = tuple(option for option in proposals
                     if option.rule.name == CITED_PROP25_RULE
                     and len(option.subgoals) == 3)
    if len(selected) != 1:
        raise RuntimeError("R4R10_PUBLIC_PROP25_EXPANSION_NOT_CONNECTED")
    _, signed, identity = selected[0].subgoals
    if (not any(item.rule.name == SOURCE58_RULE for item in expand(signed))
            or not any(item.rule.name == ETA_IDENTITY_RULE for item in expand(identity))):
        raise RuntimeError("R4R10_PUBLIC_PARENT_EXPANSIONS_NOT_CONNECTED")
    return {
        "source_5_8_screened": True,
        "proposition_2_5_screened": True,
        "eta_definition_screened": True,
        "public_prop25_candidate_found": True,
        "public_signed_parent_candidate_found": True,
        "public_identity_parent_candidate_found": True,
        "public_root_pi95_proof_complete": False,
    }


def report_folder() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / PACKAGE / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S_%fZ")
    folder.mkdir(parents=True, exist_ok=False)
    return folder


def run(root: Path, *, dry_run: bool, prior_file: Path | None) -> int:
    folder = report_folder()
    report: dict[str, object] = {
        "phase": "175-R4R10",
        "dry_run": dry_run,
        "gate": "FAIL_R4R10_CITED_58_PROP25_SHARED",
        "new_given": 2,
        "new_mathematical_rules": 0,
        "pi95_proof_complete": False,
        "full_pytest_executed": False,
        "prior_proof_search_executed": False,
    }
    try:
        report["preflight"] = preflight(root)
        prior = find_prior(prior_file)
        report["prior_report"] = str(prior)
        report["prior"] = validate_prior(json.loads(prior.read_text(encoding="utf-8")))
        report["source_positions"] = source_positions(root)
        cited = build_cited_58_prop25_sources(root)
        if len(cited.proof_links) != 2:
            raise RuntimeError("R4R10_SOURCE_REGISTRY_COUNT_CHANGED")
        report["source_refs"] = [EQUATION_REFERENCE_ID, PROPOSITION_REFERENCE_ID]
        report["delta_composition_replay"] = replay_cited_prop25()
        report["install"] = installer.install(root, dry_run=dry_run, output=folder)
        report["public"] = (None if dry_run else inspect_public_connection())
        report["gate"] = DRY_GATE if dry_run else FINAL_GATE
    except Exception as error:
        report["error"] = type(error).__name__ + ": " + str(error)
        report["traceback"] = traceback.format_exc()[-6000:]
    (folder / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8",
    )
    (folder / "report.md").write_text(
        "# Phase 175 R4R10 — Toda (5.8) / Prop 2.5 を共有探索へ接続\n\n"
        + "Gate: `" + str(report["gate"]) + "`\n\n"
        + "Toda (5.8) は出典付きの符号付き前提として利用します。\n\n"
        + "Prop 2.5 は R4R7 の型付き一般条件を使用します。\n\n"
        + "π₉⁵ の完成証明や符号の確定は本 Phase に含みません。\n",
        encoding="utf-8",
    )
    print("PHASE175_R4R10_HEAD=" + str(report.get("preflight", {}).get("head", "UNVERIFIED")))
    print("PHASE175_R4R10_NEW_CITED_GIVEN=2")
    print("PHASE175_R4R10_NEW_MATHEMATICAL_RULES=0")
    print("PHASE175_R4R10_SIGN_PRESERVED=YES")
    print("PHASE175_R4R10_PUBLIC_PROPOSITION25=" + (
        "CONNECTED" if report.get("public", {}).get("public_prop25_candidate_found") else "NOT_CHECKED"
    ) if isinstance(report.get("public"), dict) else "PHASE175_R4R10_PUBLIC_PROPOSITION25=NOT_CHECKED")
    print("PHASE175_R4R10_PI95=NOT_COMPLETE")
    print("PHASE175_R4R10_FULL_PYTEST=NOT_RUN")
    print("PHASE175_R4R10_REPORT=" + str(folder / "report.json"))
    print("PHASE175_R4R10_GATE=" + str(report["gate"]))
    if "error" in report:
        print("PHASE175_R4R10_ERROR=" + str(report["error"]))
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--r4r8-report", type=Path)
    args = parser.parse_args(argv)
    return run(args.root.resolve(), dry_run=args.dry_run, prior_file=args.r4r8_report)


if __name__ == "__main__":
    sys.exit(main())
```

## `run.ps1`

```powershell
param(
    [switch] $DryRun,
    [string] $R4R8Report = ""
)

$ErrorActionPreference = 'Stop'
$env:PYTHONUTF8 = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

Push-Location $root
try {
    $tests = @(
        'phase175_r4r10_cited_58_prop25_public/tests/test_installer.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_source.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_provider.py',
        'phase175_r4r10_cited_58_prop25_public/tests/test_audit.py',
        'phase175_r4r7_prop25_typed_composition/tests/test_rule.py',
        'phase175_r4r8_signed_delta_kernel_frontier/tests/test_audit.py'
    )
    & python -B -m pytest -q -p no:cacheprovider --import-mode=importlib @tests
    if ($LASTEXITCODE -ne 0) { throw 'R4R10 focused pytest failed' }
    Write-Output 'PHASE175_R4R10_FOCUSED_PYTEST=PASS'

    $arguments = @(
        '-B', '-m', 'phase175_r4r10_cited_58_prop25_public.audit',
        '--root', $root
    )
    if ($DryRun) { $arguments += '--dry-run' }
    if ($R4R8Report -ne '') { $arguments += @('--r4r8-report', $R4R8Report) }
    & python @arguments
    if ($LASTEXITCODE -ne 0) { throw 'R4R10 source-first audit failed' }
    Write-Output 'PHASE175_R4R10_EXIT_CODE=0'
    exit 0
} catch {
    Write-Output ('PHASE175_R4R10_ERROR=' + $_.Exception.Message)
    Write-Output 'PHASE175_R4R10_EXIT_CODE=1'
    exit 1
} finally {
    Pop-Location
}
```

## `tests/test_installer.py`

```python
"""AST / EOL / drift contracts for minimal full-function installation."""
from __future__ import annotations

import ast
from pathlib import Path

import pytest

from phase175_r4r10_cited_58_prop25_public import installer


def fixture_source() -> str:
    return (
        'def build_shared_typed_bridge():\n'
        '    if True:\n'
        + installer.BRIDGE_ANCHOR
        + '    return 1\n\n'
        'def shared_expansion_provider(bridge):\n'
        + installer.PROVIDER_ANCHOR
        + '    return bridge\n\n'
        'def unrelated():\n    return "unchanged"\n'
    )


def test_complete_bridge_replacement_keeps_other_functions() -> None:
    original = fixture_source()
    result, complete = installer.replace_full_function(
        original, installer.BRIDGE_FUNCTION,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
    )
    ast.parse(result)
    assert complete.startswith('def build_shared_typed_bridge():')
    assert complete.count('build_cited_58_prop25_sources()') == 1
    assert 'def unrelated():\n    return "unchanged"' in result


def test_complete_provider_replacement_keeps_other_functions() -> None:
    original = fixture_source()
    result, complete = installer.replace_full_function(
        original, installer.PROVIDER_FUNCTION,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_ADDITION,
    )
    ast.parse(result)
    assert complete.startswith('def shared_expansion_provider(bridge):')
    assert complete.count('build_cited_58_prop25_provider(bridge)') == 1
    assert installer.BRIDGE_ADDITION not in result


def test_two_function_install_is_idempotent() -> None:
    first, _ = installer.replace_full_function(
        fixture_source(), installer.BRIDGE_FUNCTION,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
    )
    first, _ = installer.replace_full_function(
        first, installer.PROVIDER_FUNCTION,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_ADDITION,
    )
    second, _ = installer.replace_full_function(
        first, installer.BRIDGE_FUNCTION,
        installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
    )
    second, _ = installer.replace_full_function(
        second, installer.PROVIDER_FUNCTION,
        installer.PROVIDER_ANCHOR, installer.PROVIDER_ADDITION,
    )
    assert first == second
    assert second.count('build_cited_58_prop25_sources()') == 1
    assert second.count('build_cited_58_prop25_provider(bridge)') == 1


@pytest.mark.parametrize('change', ('deleted', 'twice', 'invalid'))
def test_unreviewed_function_rejected(change: str) -> None:
    source = fixture_source()
    if change == 'deleted':
        source = source.replace(installer.BRIDGE_ANCHOR, '        pass\n')
    elif change == 'twice':
        source = source.replace(installer.BRIDGE_ANCHOR, installer.BRIDGE_ANCHOR * 2)
    else:
        source = source.replace('def build_shared_typed_bridge():', 'def build_shared_typed_bridge(')
    with pytest.raises((RuntimeError, SyntaxError)):
        installer.replace_full_function(
            source, installer.BRIDGE_FUNCTION,
            installer.BRIDGE_ANCHOR, installer.BRIDGE_ADDITION,
        )


def test_plan_rejects_unreviewed_committed_blob(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / installer.TARGET).write_text(fixture_source(), encoding='utf-8')
    monkeypatch.setattr(installer, 'git', lambda root, *args: '0' * 40)
    with pytest.raises(RuntimeError, match='UNREVIEWED_PRODUCTION_COMMIT'):
        installer.plan(tmp_path)


def test_plan_requires_exactly_reviewed_source(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    (tmp_path / installer.TARGET).write_text(fixture_source(), encoding='utf-8')
    monkeypatch.setattr(installer, 'git', lambda root, *args: installer.EXPECTED_COMMITTED_BLOB)
    with pytest.raises(RuntimeError, match='UNREVIEWED_LOCAL_PRODUCTION_CHANGE'):
        installer.plan(tmp_path)


def test_plan_accepts_windows_crlf_checkout_of_reviewed_blob(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_lf = fixture_source().encode('utf-8')
    reviewed_blob = installer.git_blob_sha(original_lf)
    monkeypatch.setattr(installer, 'EXPECTED_COMMITTED_BLOB', reviewed_blob)
    monkeypatch.setattr(installer, 'git', lambda root, *args: reviewed_blob)
    (tmp_path / installer.TARGET).write_bytes(original_lf.replace(b'\n', b'\r\n'))
    path, before, after, functions = installer.plan(tmp_path)
    assert path == tmp_path / installer.TARGET
    assert b'\r\n' in before and b'\r\n' in after
    assert b'\n' not in after.replace(b'\r\n', b'')
    assert after != before
    assert len(functions) == 2


def test_dry_run_exports_whole_functions_without_mutating_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = fixture_source().encode('utf-8')
    reviewed_blob = installer.git_blob_sha(original)
    monkeypatch.setattr(installer, 'EXPECTED_COMMITTED_BLOB', reviewed_blob)
    monkeypatch.setattr(installer, 'git', lambda root, *args: reviewed_blob)
    target = tmp_path / installer.TARGET
    target.write_bytes(original)
    report = installer.install(tmp_path, dry_run=True, output=tmp_path / 'output')
    assert target.read_bytes() == original
    assert report['patch_required'] is True
    assert report['patch_applied'] is False
    assert (tmp_path / 'output' / 'build_shared_typed_bridge_FULL_AFTER.py').is_file()
    assert (tmp_path / 'output' / 'shared_expansion_provider_FULL_AFTER.py').is_file()
    assert (tmp_path / 'output' / 'phase165_r52_r9_shared_math_FULL_AFTER.py').is_file()
```

## `tests/test_source.py`

```python
"""Toda source anchors/metadata are checked, not guessed from output labels."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r4r10_cited_58_prop25_public import source


def cited_blocks() -> dict[str, str]:
    return {
        source.CHAPTER_2: (
            r'\begin{proposition}\label{prop:2.5}' + '\n'
            + r'\alpha\in\pi_{i+1}(S^{2m+1}), \ \beta\in \pi_{j-1}(S^{i-1})'
            + '\n' + r'\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)'
            + '\n' + r'j<3m-1, \(2\)-primary では等号'
            + '\n' + r'\end{proposition}'
        ),
        source.CHAPTER_5: (
            r'\begin{equation}\label{eq:5.8}' + '\n'
            + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')"
            + '\n' + r'\end{equation}'
            + '\n' + r'\begin{proposition}\label{prop:5.8}'
        ),
    }


def prepare_source(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    blocks = cited_blocks()
    monkeypatch.setattr(source, 'vetted_source',
                        lambda path, expected: blocks[path.relative_to(source.ROOT).as_posix()])
    monkeypatch.setattr(source, '_load_manifest_reference_order',
                        lambda manifest: ({
                            source.PROPOSITION_REFERENCE_ID: 2500,
                            source.EQUATION_REFERENCE_ID: 8500,
                            'toda:Proposition 5.8': 9000,
                        }, {}, {}))
    return blocks


def test_full_toda_source_conditions_and_manifest_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prepare_source(monkeypatch)
    assert source.source_positions() == {
        source.PROPOSITION_REFERENCE_ID: 2500,
        source.EQUATION_REFERENCE_ID: 8500,
    }


def test_removed_prop25_inequality_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocks = prepare_source(monkeypatch)
    blocks[source.CHAPTER_2] = blocks[source.CHAPTER_2].replace('j<3m-1', 'j>3m-1')
    with pytest.raises(ValueError, match='PROP25_SOURCE_CHANGED'):
        source.source_positions()


def test_modified_toda58_sign_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocks = prepare_source(monkeypatch)
    blocks[source.CHAPTER_5] = blocks[source.CHAPTER_5].replace(r'\pm', '+')
    with pytest.raises(ValueError, match='EQ58_SOURCE_CHANGED'):
        source.source_positions()


def test_missing_recorded_publication_order_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prepare_source(monkeypatch)
    monkeypatch.setattr(source, '_load_manifest_reference_order',
                        lambda manifest: ({source.EQUATION_REFERENCE_ID: 8500}, {}, {}))
    with pytest.raises(ValueError, match='SOURCE_POSITION_INVALID'):
        source.source_positions()


def test_signed_source_registration_has_exactly_two_cited_given_leaves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prepare_source(monkeypatch)
    from proof import ProofRule
    bridge = source.build_cited_58_prop25_sources()
    assert len(bridge.proof_links) == 2
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)
    assert all(link.step.inference_rule.literature_reference is not None
               for link in bridge.proof_links)
    assert {bridge.registry.reference(x.reference_id).locator
            for x in bridge.registry._assertions.values()} == {
                '(5.8)', 'Proposition 2.5',
            }
```

## `tests/test_provider.py`

```python
"""Only the quoted sources and typed η definition may close the Prop 2.5 chain."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, IteratedSuspension
from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
from phase175_r4r10_cited_58_prop25_public import provider, source
from proof import InferenceRule, ProofRule, ProofStep, Relation, RelationType


def eta_goal():
    signed = source.canonical_toda58()
    beta = HomotopyElement('η₇', 7, 8, 7, GeneratorSymbol('η', index=7))
    gamma = HomotopyElement('η₉', 9, 10, 9, GeneratorSymbol('η', index=9))
    from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
    from toda_rules import TodaDeltaImageUpToSignStatement
    return TodaDeltaImageUpToSignStatement(
        TodaDeltaMap(TodaPrimaryGroup(10, 9), TodaPrimaryGroup(8, 4)),
        gamma, Composition(signed.positive_value, beta),
    )


def three_sources():
    return (
        source.CitedToda58SignedDelta(source.canonical_toda58()),
        source.CitedTodaProp25(),
        TodaEtaFamilyGeneralDefinition(),
    )


def test_toda58_formula_is_signed_and_typed() -> None:
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    signed = source.canonical_toda58()
    assert typed_endpoints(signed.element) == (9, 9)
    assert typed_endpoints(signed.positive_value) == (7, 4)
    assert signed.positive_value.right.coefficient == -1
    assert source.CitedToda58SignedDelta(signed).locator == '(5.8)'


def test_cited_source58_requires_independent_given() -> None:
    signed = source.canonical_toda58()
    options = provider.expand_cited_toda58(signed, three_sources())
    assert len(options) == 1
    assert options[0].subgoals == (three_sources()[0],)
    assert not provider.expand_cited_toda58(signed, ())
    assert not provider.expand_cited_toda58(signed, (source.CitedTodaProp25(),))


def test_identity_requires_cited_eta_definition() -> None:
    goal = eta_goal()
    identity = Relation(
        Composition(source.canonical_toda58().element,
                    IteratedSuspension(goal.positive_value.right, 2)),
        goal.element, RelationType.EQUALITY,
    )
    assert provider.eta_identity_indices(identity) == 7
    assert len(provider.expand_eta_identity(identity, three_sources())) == 1
    assert not provider.expand_eta_identity(identity, three_sources()[:2])
    assert provider.eta_identity_indices(replace(identity, rhs=source.canonical_toda58().element)) is None


def test_prop25_uses_exact_r4r7_typed_guard_and_citation() -> None:
    goal = eta_goal()
    result = provider.expand_cited_prop25(goal, three_sources())
    assert len(result) == 1
    proposal = result[0]
    assert proposal.rule.name == provider.CITED_PROP25_RULE
    assert proposal.rule.literature_reference.locator == 'Proposition 2.5'
    assert len(proposal.subgoals) == 3
    assert proposal.subgoals[0] == source.CitedTodaProp25()
    assert proposal.subgoals[1] == source.canonical_toda58()
    assert provider.eta_identity_indices(proposal.subgoals[2]) == 7


def test_missing_cited_prop25_or_58_rejected() -> None:
    goal = eta_goal()
    assert not provider.expand_cited_prop25(goal, three_sources()[0:1])
    assert not provider.expand_cited_prop25(goal, three_sources()[1:])


def test_fake_target_with_wrong_delta_map_rejected() -> None:
    goal = eta_goal()
    forged = replace(goal, map=source.canonical_toda58().map)
    assert not provider.expand_cited_prop25(forged, three_sources())


def test_wrong_dimension_or_unsigned_expression_rejected() -> None:
    goal = eta_goal()
    bad = replace(goal, positive_value=source.canonical_toda58().positive_value)
    assert not provider.expand_cited_prop25(bad, three_sources())
    wrong = replace(goal, element=source.canonical_toda58().element)
    assert not provider.expand_cited_prop25(wrong, three_sources())


def test_proof_requires_all_three_parents() -> None:
    from proof import find_inference_matches_for_rule, apply_inference_match
    goal = eta_goal()
    expansion = provider.expand_cited_prop25(goal, three_sources())[0]
    prop, signed, identity = expansion.subgoals
    fake_inferred = lambda x: ProofStep(x, (), ProofRule.INFERENCE, inference_rule=InferenceRule('test'))
    given = ProofStep(prop, (), ProofRule.GIVEN)
    parents = (given, fake_inferred(signed), fake_inferred(identity))
    match = find_inference_matches_for_rule(expansion.rule, parents)
    assert len(match) == 1
    step = apply_inference_match(match[0])
    assert step.conclusion == goal
    assert step.rule is ProofRule.INFERENCE
    assert not find_inference_matches_for_rule(expansion.rule, parents[:2])
    assert not find_inference_matches_for_rule(
        expansion.rule, (fake_inferred(prop),) + parents[1:],
    )


def test_prop25_sign_is_never_chosen() -> None:
    goal = eta_goal()
    assert goal.positive_value.left.right.coefficient == -1
    assert provider.expand_cited_prop25(goal, three_sources())


def test_no_pi95_group_result_is_registered_by_two_source_types() -> None:
    assert all(not hasattr(x, 'group') for x in three_sources()[:2])
```

## `tests/test_audit.py`

```python
"""Prior-report and source-first audit boundary checks."""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import pytest

from phase175_r4r10_cited_58_prop25_public import audit, source


def passed_report() -> dict[str, object]:
    return {
        'phase': '175-R4R8', 'gate': audit.PRIOR_GATE, 'dry_run': False,
        'new_given': 0, 'new_mathematical_rules': 0,
        'production_changes': [], 'rule_connected_to_public': False,
        'pi95_proof_complete': False, 'full_pytest_executed': False,
        'prior_proof_search_executed': False,
        'groups': {
            'prior_presentations_identified': 2,
            'group_presentations_do_not_certify_E_actions': True,
        },
        'unresolved_obligations': [{'index': k} for k in range(1, 7)],
    }


def test_prior_report_is_audit_not_proof() -> None:
    result = audit.validate_prior(passed_report())
    assert result['prior_unresolved_obligations'] == 6
    assert result['prior_math_proofs_not_adopted'] is True


@pytest.mark.parametrize('key,value', (
    ('phase', '175-R4R7'), ('gate', audit.DRY_GATE), ('dry_run', True),
    ('new_given', 1), ('new_mathematical_rules', 1),
    ('production_changes', ['proof.py']), ('rule_connected_to_public', True),
    ('pi95_proof_complete', True), ('full_pytest_executed', True),
    ('prior_proof_search_executed', True),
))
def test_bad_prior_report_rejected(key: str, value: object) -> None:
    bad = passed_report()
    bad[key] = value
    with pytest.raises(RuntimeError, match='REPORT_SCOPE_INVALID'):
        audit.validate_prior(bad)


@pytest.mark.parametrize('change', ('groups', 'obligations', 'missing_groups'))
def test_missing_prior_math_boundary_rejected(change: str) -> None:
    data = passed_report()
    if change == 'groups':
        data['groups']['group_presentations_do_not_certify_E_actions'] = False
    elif change == 'obligations':
        data['unresolved_obligations'] = []
    else:
        data.pop('groups')
    with pytest.raises(RuntimeError, match='REPORT_EVIDENCE_INVALID'):
        audit.validate_prior(data)


def test_sample_is_only_a_typed_goal() -> None:
    from toda_rules import TodaDeltaImageUpToSignStatement
    from phase175_r4r7_prop25_typed_composition.rule import typed_endpoints
    goal = audit.sample_delta_eta9()
    assert isinstance(goal, TodaDeltaImageUpToSignStatement)
    assert typed_endpoints(goal.element) == (10, 9)
    assert typed_endpoints(goal.positive_value) == (8, 4)


def test_source_integrity_rejects_unknown_file(tmp_path: Path) -> None:
    candidate = tmp_path / 'Toda.tex'
    candidate.write_text('fabricated source\n', encoding='utf-8')
    with pytest.raises(ValueError, match='SOURCE_BLOB_DRIFT'):
        source.vetted_source(candidate, source.CHAPTER_5_BLOB)


def test_source_identity_has_no_direct_group_claim() -> None:
    eq = source.CitedToda58SignedDelta(source.canonical_toda58())
    prop = source.CitedTodaProp25()
    assert eq.locator == '(5.8)'
    assert prop.locator == 'Proposition 2.5'
    assert eq.statement.element.dimension == 9


def test_source_bound_chain_replays_without_group_conclusion(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Independent source GIVEN parents must produce a signed INFERENCE chain."""
    monkeypatch.setattr(source, 'source_positions', lambda root=source.ROOT,
                        manifest=source.DEFAULT_MANIFEST: {
                            source.EQUATION_REFERENCE_ID: 8500,
                            source.PROPOSITION_REFERENCE_ID: 2500,
                        })
    result = audit.replay_cited_prop25()
    assert result['conclusion_is_signed'] is True
    assert result['equation_5_8_citation_present'] is True
    assert result['proposition_2_5_citation_present'] is True
    assert result['eta_family_citation_present'] is True
    assert result['root_group_conclusion_inferred'] is False
    assert result['full_search_performed'] is False
```

