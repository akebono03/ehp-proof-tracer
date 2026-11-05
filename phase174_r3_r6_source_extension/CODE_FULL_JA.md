# Phase 174 R3-R6 — コード全文（配布用）

このファイルには**新規追加するクラス・関数、テスト、監査、パッチ用コードの全文**を収録する。既存ファイルを更新する箇所については、この ZIP の `patch.py` に含まれる一意のコード置換を実行した後、変更後の `build_shared_typed_bridge`、`shared_expansion_provider`、3つのテスト・監査関数の全文を `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r6\*_FULL.py` に出力する。モジュール上部の既存 import 節は変更せず、新しい import は関数本体内に追加する。

R3-R6 の変更対象は `実装仕様.md` に記載した4ファイルであり、その他の既存ファイル・共通 Narrative・5つの中核文書は編集しない。

## `source.py`

```python
"""Phase 174 R3-R6: source-verified universal Toda (4.8) and (5.5).

The only new GIVENs are the two source-level universal formulae.  The
index-two injection and each doubled generator relation require INFERENCE
ProofSteps from the existing canonical backward-search engine.  Neither
this module nor its caller registers a special pi_8^5 result.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha1
from pathlib import Path

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import FiniteCyclicGroup
from phase163_r4_registry_bridge import (
    MigrationRecord,
    MigrationStatus,
    RegistryBridgeResult,
)
from phase165_r3_recursive_search import GoalExpansion
from phase166_r3b_publication_order_binding.phase166_r3b_publication_order_binding import (
    _load_manifest_reference_order,
)
from phase165_r5_manifest_bridge import DEFAULT_MANIFEST
from phase169_r10d2_general_family_definition.family_citation import (
    CitedStableFamilyDefinition,
    StableFamilyMemberDefinition,
    canonical_member,
)
from phase174_r3_r5_finite_cyclic_extension.rule import Toda48UniversalConditionalStatement
from proof import (
    InferenceRule,
    LiteratureReference,
    PremisePattern,
    ProofRule,
    ProofStep,
    Relation,
    RelationType,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ProofStepLink,
    ReferenceKind,
    UnifiedStatementRegistry,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = (
    ("(4.8)", "04", "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7"),
    ("(5.5)", "05", "579661138928499ba04a51327f686d9b971b5314"),
)


@dataclass(frozen=True)
class Toda55UniversalDoubleStatement:
    """The cited general equation 2 nu_n = E^(n-3) nu-prime for n>=5."""

    minimum_index: int = 5
    coefficient: int = 2
    exponent_shift: int = 3
    family: str = "ν"
    base_decoration: str = "′"


def _git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def verify_extension_texts(
    root: Path = ROOT,
    manifest: Path = DEFAULT_MANIFEST,
) -> tuple[tuple[str, int], ...]:
    """Fail closed on modified source bytes, missing hypotheses and source order.

    CRLF checkouts are accepted only when their normalized content is exactly
    the reviewed Git blob.  A TeX snippet alone is not enough evidence.
    """
    if not isinstance(root, Path) or not isinstance(manifest, Path):
        raise TypeError("root and manifest must be pathlib.Path")
    text_by_locator: dict[str, str] = {}
    for locator, chapter, expected in SOURCES:
        path = root / "sources" / "toda" / f"Toda_{chapter}_2.tex"
        data = path.read_bytes()
        normalized = data.replace(b"\r\n", b"\n")
        candidates = (data, normalized, normalized.replace(b"\n", b"\r\n"))
        if not any(_git_blob_sha(value) == expected for value in candidates):
            raise ValueError(f"Unreviewed Toda source blob for {locator}")
        text_by_locator[locator] = normalized.decode("utf-8-sig")
    chapter4 = text_by_locator["(4.8)"]
    chapter5 = text_by_locator["(5.5)"]
    start48 = r"\begin{equation}\label{4.8}"
    end = r"\end{equation}"
    if chapter4.count(start48) != 1:
        raise ValueError("Toda (4.8) source anchor is not unique")
    block48 = chapter4.split(start48, 1)[1].split(end, 1)[0]
    for fragment in (
        r"n \ \text{を偶数とする.",
        r"\Delta(\iota_{2n-1})=0",
        r"E^{2}:\pit{2n-2}{\,n-1}\to\pit{2n}{\,n+1}",
        r"\ \text{は単射で, }",
        r"\pit{2n}{\,n+1}/E^{2}\pit{2n-2}{\,n-1}\cong\mathbb{Z}_2",
    ):
        if fragment not in block48:
            raise ValueError("Toda (4.8) conditional clause missing: " + fragment)
    start55 = r"\begin{equation}\label{eq:5.5}"
    if chapter5.count(start55) != 1:
        raise ValueError("Toda (5.5) source anchor is not unique")
    position55 = chapter5.index(start55)
    block55 = chapter5.split(start55, 1)[1].split(end, 1)[0]
    if (
        r"n\ge5\ \text{に対して, } 2\nu_n=E^{\,n-3}\nu'" not in block55
        or r"\nu_n:=E^{\,n-4}\nu_{4}" not in chapter5[:position55]
        or r"\begin{proposition}\label{prop:5.6}" not in chapter5[position55:]
    ):
        raise ValueError("Toda (5.5) general-double relation or source order invalid")
    positions, _, _ = _load_manifest_reference_order(manifest)
    found = (
        positions.get("toda:(4.8)"),
        positions.get("toda:(5.5)"),
        positions.get("toda:Proposition 5.6"),
    )
    if found != (7500, 8600, 8800):
        raise ValueError("Reviewed Toda publication-order boundary changed")
    return (("(4.8)", found[0]), ("(5.5)", found[1]))


def build_cited_extension_sources(
    root: Path = ROOT,
    manifest: Path = DEFAULT_MANIFEST,
) -> RegistryBridgeResult:
    """Register two universal source statements; no special group or relation."""
    positions = dict(verify_extension_texts(root, manifest))
    registry = UnifiedStatementRegistry()
    links = []
    records = []
    for locator, chapter, _ in SOURCES:
        source = (
            Toda48UniversalConditionalStatement()
            if locator == "(4.8)" else Toda55UniversalDoubleStatement()
        )
        ref_id = "toda:" + locator
        assertion_id = "toda:174:r3r6:universal:" + locator
        registry.add_reference(LiteratureEntry(
            reference_id=ref_id,
            kind=ReferenceKind.EQUATION,
            locator=locator,
            source_id=(f"sources/toda/Toda_{chapter}_2.tex "
                       "(adopted transcription; original edition unverified)"),
            publication_position=positions[locator],
        ))
        registry.add_assertion(AssertionEntry(
            assertion_id=assertion_id,
            reference_id=ref_id,
            kind=AssertionKind.STATEMENT,
            content=source,
            origin=AssertionOrigin.FIXED_STATEMENT,
            scope=("universal formula only", "no direct group conclusion"),
        ))
        links.append(ProofStepLink(assertion_id, step=ProofStep(
            conclusion=source,
            premises=(),
            rule=ProofRule.GIVEN,
            inference_rule=InferenceRule(
                name="Cited universal Toda " + locator,
                literature_reference=LiteratureReference(
                    label="Toda " + locator, locator=locator,
                ),
            ),
        )))
        records.append(MigrationRecord(
            "phase174_r3_r6", locator, assertion_id, MigrationStatus.STRUCTURED,
            "Source-blob-verified universal formula; no concrete goal asserted",
        ))
    return RegistryBridgeResult(registry, tuple(records), tuple(links))


def _cited_nu_member(goal: object) -> StableFamilyMemberDefinition | None:
    """A requested doubled relation must carry the complete typed nu identity."""
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or not isinstance(goal.lhs, Multiple)
        or type(goal.lhs.coefficient) is not int
        or goal.lhs.coefficient != 2
        or not isinstance(goal.lhs.expression, HomotopyElement)
        or not isinstance(goal.rhs, IteratedSuspension)
        or type(goal.rhs.exponent) is not int
        or not isinstance(goal.rhs.expression, HomotopyElement)
    ):
        return None
    target = goal.lhs.expression
    earlier = goal.rhs.expression
    n = target.dimension
    if (
        type(n) is not int or n < 5
        or goal.rhs.exponent != n - 3
        or target.source != n + 3 or target.target != n
        or target.generator != GeneratorSymbol("ν", index=n)
        or earlier.dimension != 3 or earlier.source != 6 or earlier.target != 3
        or goal.rhs.source != target.source
        or goal.rhs.target != target.target
    ):
        return None
    # Convert the registered HyoujiGen spelling (\nu') to the cited ν′
    # source identity through the existing conservative, typed ID resolver.
    # This tests symbol identity only; it does not assert any element order.
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )
    nu_prime_cited = HomotopyElement(
        name="ν′", dimension=3, source=6, target=3,
        generator=GeneratorSymbol("ν", decoration="′"),
    )
    if not same_registered_group_presentation(
        FiniteCyclicGroup(4, earlier), FiniteCyclicGroup(4, nu_prime_cited),
    ):
        return None
    source = CitedStableFamilyDefinition(family_id=4, minimum_n=4, stem=3)
    member = canonical_member(source, n)
    if member is None or (
        member.element.dimension != n
        or member.element.source != target.source
        or member.element.target != target.target
        or member.element.generator != target.generator
    ):
        return None
    return member


def cited_toda55_double_inference_rule(
    goal: Relation,
) -> InferenceRule:
    """Conclude the concrete double only from cited (5.5) and a family member."""
    member = _cited_nu_member(goal)
    if member is None:
        raise ValueError("not a typed instance of the universal Toda (5.5)")
    theorem = Toda55UniversalDoubleStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and premises[0].conclusion == member
            and type(premises[1].conclusion) is Toda55UniversalDoubleStatement
            and premises[1].conclusion == theorem
            and _cited_nu_member(goal) == member
        )

    return InferenceRule(
        name="specialize cited Toda (5.5) doubled nu-family identity",
        description=(
            "The source equation for every n>=5 is specialized to the typed "
            "nu-family member from an independently cited Definition."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=StableFamilyMemberDefinition,
                statement_pattern=member,
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Toda55UniversalDoubleStatement,
                statement_pattern=theorem,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
        literature_reference=LiteratureReference(
            label="Toda (5.5)", locator="(5.5)",
        ),
    )


def expand_cited_toda55_double(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Backwards proposal only; screen the general equation and family source."""
    if not isinstance(available, tuple):
        raise TypeError("available must be a screened tuple")
    member = _cited_nu_member(goal)
    if (
        member is None
        or available.count(Toda55UniversalDoubleStatement()) != 1
        or available.count(member.source) != 1
    ):
        return ()
    return (GoalExpansion(
        cited_toda55_double_inference_rule(goal),
        (member, Toda55UniversalDoubleStatement()),
    ),)
```

## `verify.py`

```python
"""DryRun-compatible verifier of the unchanged cited Toda source and order."""
from __future__ import annotations

from phase174_r3_r6_source_extension.source import verify_extension_texts


def main() -> int:
    positions = dict(verify_extension_texts())
    print("PHASE174_R3R6_TODA48_SOURCE_POSITION=" + str(positions["(4.8)"]))
    print("PHASE174_R3R6_TODA55_SOURCE_POSITION=" + str(positions["(5.5)"]))
    print("PHASE174_R3R6_SOURCE_TEXT_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `patch.py`

```python
"""Guarded R3-R6 patch: exact reviewed R3-R5 code and focused test contracts.

Only whole-function or unique guarded insertions are installed.  Source bytes
are pinned to the actual 174-3-5 Git commit, including an older local HEAD
with the identical R3-R5 worktree implementation.  No reset or merge occurs.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
import os
from pathlib import Path
import subprocess
import tempfile

REVIEWED_HEAD = "7bd64d36e17246195525ecb0ec27a170abb73206"
PREVIOUS_HEAD = "45d97b2adc73c2347866de28b344fce1e6d2c095"
SHARED = "phase165_r52_r9_shared_math.py"
R3R4_TEST = "phase174_r3_r4_public_delta_connection/tests/test_connection.py"
R3R5_TEST = "phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py"
PREFLIGHT = "phase174_r3_r5_preflight/audit.py"
REVIEWED_BLOBS = {
    SHARED: "419e6fd2f5848777fec05f2048169bc2dc044f9d",
    R3R4_TEST: "e34c6c24a6a1de1a330c8a36d135e3bb87a8f633",
    R3R5_TEST: "f7351a47ce328603236f2dad71c8c8d886d79cd1",
    PREFLIGHT: "b309cdd38475e1c8643f757f93f0830903983b52",
}


def git(*args: str) -> bytes:
    return subprocess.run(("git",) + args, check=True, capture_output=True).stdout


def blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\x00" + data).hexdigest()


def reviewed_originals() -> dict[str, bytes]:
    """Check the reviewed production/test blobs, even before the local merge."""
    head = git("rev-parse", "HEAD").decode("ascii").strip()
    branch = git("branch", "--show-current").decode("utf-8").strip()
    remote = git("ls-remote", "origin", "refs/heads/develop").decode("ascii").split()
    if len(remote) != 2 or remote[1] != "refs/heads/develop":
        raise ValueError("Cannot confirm remote develop HEAD")
    if branch != "develop" or head not in (PREVIOUS_HEAD, REVIEWED_HEAD) or remote[0] != REVIEWED_HEAD:
        raise ValueError(
            "Reviewed R3-R6 HEAD mismatch: " + f"local={head} remote={remote[0]} expected={REVIEWED_HEAD}"
        )
    if git("diff", "--cached", "--name-only").strip():
        raise ValueError("Staged changes require review")
    changed = set(git("diff", "--name-only", "HEAD").decode("utf-8").splitlines())
    known_prior_worktree = set(REVIEWED_BLOBS)
    if changed - known_prior_worktree:
        raise ValueError("Unrelated user worktree changes: " + repr(sorted(changed - known_prior_worktree)))
    reviewed = {}
    for path, expected in REVIEWED_BLOBS.items():
        if head == REVIEWED_HEAD:
            data = git("show", "HEAD:" + path)
        elif path == SHARED:
            from phase174_r3_r5_finite_cyclic_extension.patch import insert_shared
            data = insert_shared(git("show", "HEAD:" + path))
        elif path == R3R4_TEST:
            from phase174_r3_r5_finite_cyclic_extension.patch import replace_r3r4_test
            data = replace_r3r4_test(git("show", "HEAD:" + path))
        elif path == PREFLIGHT:
            from phase174_r3_r5_finite_cyclic_extension.patch import replace_preflight_provider_guard
            data = replace_preflight_provider_guard(git("show", "HEAD:" + path))
        else:
            data = Path(path).read_bytes()
        if blob_sha(data) != expected:
            raise ValueError("Pinned reviewed Git blob differs: " + path)
        reviewed[path] = data
    return reviewed


def reviewed_shared_bytes() -> bytes:
    """Return the pinned full R3-R5 production file, not a guessed patch."""
    return reviewed_originals()[SHARED]


def _insert(original: bytes, old_text: str, new_text: str, description: str) -> bytes:
    ending = b"\r\n" if b"\r\n" in original else b"\n"
    old = old_text.encode("utf-8").replace(b"\n", ending)
    new = new_text.encode("utf-8").replace(b"\n", ending)
    if original.count(new) == 1 and original.count(old) == 0:
        return original
    if original.count(old) != 1 or original.count(new) != 0:
        raise ValueError("Reviewed insertion context changed: " + description)
    result = original.replace(old, new, 1)
    ast.parse(result.decode("utf-8-sig"))
    return result


def connect_shared(original: bytes) -> bytes:
    """Change just the two reviewed functions, never the root goal or renderer."""
    old_sources = (
        "        sources = sources + (build_cited_prop22_right_reference(production),)\n"
        "    registry = UnifiedStatementRegistry()\n"
    )
    new_sources = (
        "        sources = sources + (build_cited_prop22_right_reference(production),)\n"
        "        from phase174_r3_r6_source_extension.source import build_cited_extension_sources\n"
        "        sources = sources + (build_cited_extension_sources(),)\n"
        "    registry = UnifiedStatementRegistry()\n"
    )
    first = _insert(original, old_sources, new_sources, "source registration")
    old_expand = (
        "        options.extend(expand_toda48_index_two(goal))\n"
        "        options.extend(expand_finite_index_two_cyclic_structure(goal))\n"
        "        options.extend(expand_finite_cyclic_relation(goal))\n"
    )
    new_expand = (
        "        options.extend(expand_toda48_index_two(goal))\n"
        "        options.extend(expand_finite_index_two_cyclic_structure(goal))\n"
        "        from phase174_r3_r6_source_extension.source import expand_cited_toda55_double\n"
        "        options.extend(expand_cited_toda55_double(goal, tuple(available)))\n"
        "        options.extend(expand_finite_cyclic_relation(goal))\n"
    )
    return _insert(first, old_expand, new_expand, "universal doubled relation expansion")


def replace_r3r4_test(original: bytes) -> bytes:
    old = (
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    assert current in (r3r4, insert_shared(r3r4))\n"
    )
    new = (
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    from phase174_r3_r6_source_extension.patch import connect_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    r3r5 = insert_shared(r3r4)\n"
        "    assert current in (r3r4, r3r5, connect_shared(r3r5))\n"
    )
    return _insert(original, old, new, "R3-R4 source-guard test")


def replace_r3r5_test(original: bytes) -> bytes:
    old = (
        "    # The source theorem is deliberately NOT created as a verified GIVEN.\n"
        "    assert not any(link.step is not None and link.step.conclusion == index_options[0].subgoals[1]\n"
        "                   for link in screened.proof_links)\n"
    )
    new = (
        "    # In R3-R6 only the general source formulae are GIVEN; concrete\n"
        "    # index-two and doubled relations still require independent inference.\n"
        "    from phase174_r3_r6_source_extension.source import Toda55UniversalDoubleStatement\n"
        "    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN\n"
        "               and link.step.conclusion == index_options[0].subgoals[1]\n"
        "               for link in screened.proof_links)\n"
        "    assert any(link.step is not None and link.step.rule is ProofRule.GIVEN\n"
        "               and link.step.conclusion == Toda55UniversalDoubleStatement()\n"
        "               for link in screened.proof_links)\n"
        "    assert not any(link.step is not None and link.step.rule is ProofRule.GIVEN\n"
        "                   and link.step.conclusion in (goal, cyclic, index, double)\n"
        "                   for link in screened.proof_links)\n"
    )
    return _insert(original, old, new, "R3-R5 published source theorem test")


def _replace_function(original: bytes, function_name: str, replacement: str) -> bytes:
    normalized = original.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(normalized)
    found = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name == function_name]
    if len(found) != 1:
        raise ValueError("Expected exactly one function: " + function_name)
    node = found[0]
    lines = normalized.splitlines(keepends=True)
    expected_name = "def " + function_name + "("
    if not lines[node.lineno - 1].startswith(expected_name):
        raise ValueError("Unexpected function header")
    output = "".join(lines[:node.lineno - 1]) + replacement.rstrip("\n") + "\n" + "".join(lines[node.end_lineno:])
    ending = "\r\n" if b"\r\n" in original else "\n"
    data = output.replace("\n", ending).encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        data = b"\xef\xbb\xbf" + data
    ast.parse(data.decode("utf-8-sig"))
    return data


PREFLIGHT_FUNCTION = '''def inspect_source_provider(root: Path) -> dict[str, Any]:
    """Check the exact reviewed R3-R5 or R3-R6 provider, not a loose substring."""
    file = root / SOURCE_FILE
    source = file.read_bytes()
    parsed = ast.parse(source.decode("utf-8-sig"))
    functions = [
        node for node in parsed.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "shared_expansion_provider"
    ]
    if len(functions) != 1:
        raise ValueError("shared_expansion_provider must have one definition")
    if source.count(DELTA_HOOK.encode("utf-8")) != 1:
        raise ValueError("R3-R4 general Delta-zero hook is absent or duplicated")
    from phase174_r3_r6_source_extension.patch import reviewed_shared_bytes, connect_shared
    reviewed = reviewed_shared_bytes()
    if source not in (reviewed, connect_shared(reviewed)):
        raise ValueError("Unreviewed production source modifications")
    head = run_git("rev-parse", "HEAD")
    state = "COMMITTED" if head == "7bd64d36e17246195525ecb0ec27a170abb73206" and source == reviewed else "WORKTREE_PATCHED"
    return {
        "state": state,
        "delta_provider_hook_present": True,
        "full_function_line_count": functions[0].end_lineno - functions[0].lineno + 1,
        "production_source_changed_by_this_audit": False,
    }
'''


def replace_preflight_audit(original: bytes) -> bytes:
    return _replace_function(original, "inspect_source_provider", PREFLIGHT_FUNCTION)


def full_function(data: bytes, function_name: str) -> str:
    text = data.decode("utf-8-sig").replace("\r\n", "\n")
    lines = text.splitlines()
    hits = [n for n in ast.parse(text).body
            if isinstance(n, ast.FunctionDef) and n.name == function_name]
    if len(hits) != 1:
        raise ValueError("Cannot export complete replacement function: " + function_name)
    return "\n".join(lines[hits[0].lineno - 1:hits[0].end_lineno]) + "\n"


def install(*, dry_run: bool) -> dict[str, object]:
    reviewed = reviewed_originals()
    modified = {
        SHARED: connect_shared(reviewed[SHARED]),
        R3R4_TEST: replace_r3r4_test(reviewed[R3R4_TEST]),
        R3R5_TEST: replace_r3r5_test(reviewed[R3R5_TEST]),
        PREFLIGHT: replace_preflight_audit(reviewed[PREFLIGHT]),
    }
    states = {}
    for path, before in reviewed.items():
        current = Path(path).read_bytes()
        if current == before:
            states[path] = "REVIEWED_R3R5"
        elif current == modified[path]:
            states[path] = "ALREADY_R3R6"
        else:
            raise ValueError("Refusing unrelated user changes to " + path)
    if not dry_run:
        for path, after in modified.items():
            if states[path] == "REVIEWED_R3R5":
                Path(path).write_bytes(after)
        for path, after in modified.items():
            if Path(path).read_bytes() != after:
                raise ValueError("Installed file differs from reviewed replacement: " + path)
        folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        folder = folder / "EHPProofTracerAudit" / "phase174_r3_r6"
        folder.mkdir(parents=True, exist_ok=True)
        functions = (
            (SHARED, "build_shared_typed_bridge"),
            (SHARED, "shared_expansion_provider"),
            (R3R4_TEST, "test_r3r4_real_production_file_has_only_reviewed_wiring"),
            (R3R5_TEST, "test_public_pi85_cyclic_root_and_delta_proposals_reached"),
            (PREFLIGHT, "inspect_source_provider"),
        )
        for path, name in functions:
            output = folder / (name + "_FULL.py")
            output.write_text(full_function(modified[path], name), encoding="utf-8")
    return {
        "changed": tuple(modified),
        "states": states,
        "blobs": {path: blob_sha(data) for path, data in modified.items()},
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = install(dry_run=args.dry_run)
    print("PHASE174_R3R6_REVIEWED_HEAD=" + REVIEWED_HEAD)
    print("PHASE174_R3R6_EXISTING_FILES=" + str(len(result["changed"])))
    for path, sha in result["blobs"].items():
        print("PHASE174_R3R6_PATCH_BLOB " + path + " " + sha)
    print("PHASE174_R3R6_SOURCE_GUARD=PASS")
    print("PHASE174_R3R6_DRY_RUN=PASS" if args.dry_run else "PHASE174_R3R6_PATCH=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `audit.py`

```python
"""Verify live R3-R6 source-ancestry, independent inferences, root status."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import RegisteredGoalUnresolved, reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r2_search_adapter import search_registered_partial_proof
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase174_r3_r5_finite_cyclic_extension.rule import Toda48UniversalConditionalStatement
from phase174_r3_r6_source_extension.patch import (
    PREFLIGHT,
    R3R4_TEST,
    R3R5_TEST,
    SHARED,
    connect_shared,
    replace_preflight_audit,
    replace_r3r4_test,
    replace_r3r5_test,
    reviewed_originals,
)
from phase174_r3_r6_source_extension.source import (
    Toda55UniversalDoubleStatement,
    verify_extension_texts,
)
from proof import ProofRule


def _leaves(step) -> tuple[object, ...]:
    """Return all cited GIVEN conclusions under a proved inference step."""
    if step.rule is ProofRule.GIVEN:
        return (step.conclusion,)
    result = []
    for premise in step.premises:
        result.extend(_leaves(premise))
    return tuple(result)


def audit() -> dict[str, object]:
    reviewed = reviewed_originals()
    changes = {
        SHARED: connect_shared,
        R3R4_TEST: replace_r3r4_test,
        R3R5_TEST: replace_r3r5_test,
        PREFLIGHT: replace_preflight_audit,
    }
    if any(Path(path).read_bytes() != transform(reviewed[path])
           for path, transform in changes.items()):
        raise ValueError("Unexpected source patch or test content")
    positions = dict(verify_extension_texts())
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Public target is not uniquely registered")
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise ValueError("Target source order is missing")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    available = tuple(link.step.conclusion for link in screened.proof_links
                      if link.step is not None and link.step.rule is ProofRule.GIVEN)
    if available.count(Toda48UniversalConditionalStatement()) != 1:
        raise ValueError("Toda (4.8) general reference missing or duplicated")
    if available.count(Toda55UniversalDoubleStatement()) != 1:
        raise ValueError("Toda (5.5) general reference missing or duplicated")
    provider = shared_expansion_provider(screened, proof_target=target)
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    proposals = tuple(p for p in provider(cyclic) if p.rule.name ==
                      "finite cyclic extension by an index-two injective image")
    if len(proposals) != 1:
        raise ValueError("R3-R5 generic cyclic extension proposal changed")
    index, prior, doubled = proposals[0].subgoals
    if index in available or prior in available and prior == target or doubled in available or target in available:
        raise ValueError("A derived conclusion was promoted to a direct reference")
    index_step = reconstruct_registered_goal(
        index, screened, citing, provider, lookup_mode="typed_reference",
    )
    if index_step.rule is not ProofRule.INFERENCE or (
        Toda48UniversalConditionalStatement() not in _leaves(index_step)
    ):
        raise ValueError("Toda (4.8) index-two claim lacks certified source ancestry")
    doubled_step = reconstruct_registered_goal(
        doubled, screened, citing, provider, lookup_mode="typed_reference",
    )
    if doubled_step.rule is not ProofRule.INFERENCE or (
        Toda55UniversalDoubleStatement() not in _leaves(doubled_step)
    ):
        raise ValueError("Toda (5.5) double lacks independently certified source ancestry")
    try:
        prior_step = reconstruct_registered_goal(
            prior, screened, citing, provider, lookup_mode="typed_reference",
        )
    except RegisteredGoalUnresolved:
        prior_step = None
    partial = search_registered_partial_proof(
        n=5, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    certified = partial.status.value == "complete"
    if certified and not any(
        s.rule is ProofRule.INFERENCE and s.conclusion == target
        for s in partial.proven_steps
    ):
        raise ValueError("Complete status without a verified group root")
    if any(link.step is not None and link.step.rule is ProofRule.GIVEN
           and link.step.conclusion == target for link in screened.proof_links):
        raise ValueError("The target was incorrectly registered as GIVEN")
    return {
        "phase": "174-R3-R6",
        "reviewed_source_positions": positions,
        "registered_universal_source_given": 2,
        "registered_direct_group_given": 0,
        "toda48_index_two_step": "INFERENCE",
        "toda48_ancestry_cited": True,
        "toda55_double_step": "INFERENCE",
        "toda55_ancestry_cited": True,
        "prior_group_obligation_proved": prior_step is not None,
        "prior_group_proof_rule": prior_step.rule.value if prior_step is not None else None,
        "root_search_status": partial.status.value,
        "root_proven_step_count": len(partial.proven_steps),
        "root_open_goal_types": [type(g).__name__ for g in partial.open_goals],
        "root_complete_verified": certified,
        "web_narrative_complete_checked": False,
        "new_group_specific_rules": 0,
        "full_pytest_performed": False,
    }


def main() -> int:
    result = audit()
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = folder / "EHPProofTracerAudit" / "phase174_r3_r6"
    folder.mkdir(parents=True, exist_ok=True)
    destination = folder / "audit.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print("PHASE174_R3R6_CITED_UNIVERSAL_GIVENS=2")
    print("PHASE174_R3R6_NEW_GROUP_GIVEN=0")
    print("PHASE174_R3R6_TODA48_INDEX_INFERRED=True")
    print("PHASE174_R3R6_TODA55_DOUBLE_INFERRED=True")
    print("PHASE174_R3R6_PRIOR_PROVED=" + str(result["prior_group_obligation_proved"]))
    print("PHASE174_R3R6_ROOT_STATUS=" + result["root_search_status"])
    print("PHASE174_R3R6_ROOT_PROVEN_STEPS=" + str(result["root_proven_step_count"]))
    print("PHASE174_R3R6_ROOT_COMPLETE=" + str(result["root_complete_verified"]))
    print("PHASE174_R3R6_REPORT=" + str(destination))
    print("PHASE174_R3R6_SOURCE_ANCESTRY_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_source.py`

```python
"""Phase 174 R3-R6: source ancestry and generic backward specialization tests."""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48UniversalConditionalStatement,
    Toda48IndexTwoDoubleSuspensionStatement,
)
from phase174_r3_r6_source_extension.source import (
    Toda55UniversalDoubleStatement,
    build_cited_extension_sources,
    cited_toda55_double_inference_rule,
    expand_cited_toda55_double,
    verify_extension_texts,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _public_context():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    assert len(goals) == 1
    goal = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing is not None
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=goal, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    provider = shared_expansion_provider(screened, proof_target=goal)
    return goal, citing, screened, provider


def test_toda48_toda55_text_and_manifest_order() -> None:
    positions = dict(verify_extension_texts())
    assert positions == {"(4.8)": 7500, "(5.5)": 8600}


def test_toda48_injectivity_clause_preserves_printed_tex_spacing() -> None:
    """The adopted source has a space before the closing TeX brace."""
    source = Path(__file__).resolve().parents[2] / "sources/toda/Toda_04_2.tex"
    text = source.read_text(encoding="utf-8-sig")
    start = r"\begin{equation}\label{4.8}"
    assert text.count(start) == 1
    block = text.split(start, 1)[1].split(r"\end{equation}", 1)[0]
    assert r"E^{2}:\pit{2n-2}{\,n-1}\to\pit{2n}{\,n+1}" in block
    assert r"\ \text{は単射で, }" in block
    assert r"\pit{2n}{\,n+1}/E^{2}\pit{2n-2}{\,n-1}\cong\mathbb{Z}_2" in block
    assert dict(verify_extension_texts()) == {"(4.8)": 7500, "(5.5)": 8600}


def test_unverified_modified_toda_transcription_rejected(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[2]
    for ch in ("04", "05"):
        source = root / "sources" / "toda" / f"Toda_{ch}_2.tex"
        target = tmp_path / "sources" / "toda" / source.name
        target.parent.mkdir(parents=True, exist_ok=True)
        content = source.read_bytes()
        if ch == "04":
            content = content.replace(b"\\Delta(\\iota_{2n-1})=0", b"\\Delta(\\iota_{2n-1})=1")
        target.write_bytes(content)
    with pytest.raises(ValueError, match="Unreviewed Toda source blob"):
        verify_extension_texts(tmp_path)


def test_source_bridge_registers_universal_only() -> None:
    bridge = build_cited_extension_sources()
    assert len(bridge.proof_links) == 2
    claims = {link.step.conclusion for link in bridge.proof_links}
    assert claims == {
        Toda48UniversalConditionalStatement(), Toda55UniversalDoubleStatement(),
    }
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)
    assert all(not isinstance(link.step.conclusion, Relation) for link in bridge.proof_links)
    for assertion in bridge.registry._assertions.values():
        ref = bridge.registry.reference(assertion.reference_id)
        assert ref.publication_position in (7500, 8600)
        assert assertion.content in claims


def test_cited_toda55_inference_rejects_given_family_member_and_wrong_formula() -> None:
    n = 5
    nu = HomotopyElement("ν₅", n, n + 3, n, GeneratorSymbol("ν", index=n))
    prior = HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", decoration="′"))
    goal = Relation(Multiple(2, nu), IteratedSuspension(prior, n - 3), RelationType.EQUALITY)
    sources = (Toda55UniversalDoubleStatement(),)
    assert not expand_cited_toda55_double(goal, sources)
    from phase169_r10d2_general_family_definition.family_citation import (
        CitedStableFamilyDefinition,
        canonical_member,
    )
    definition = CitedStableFamilyDefinition(4, 4, 3)
    proposals = expand_cited_toda55_double(goal, sources + (definition,))
    assert len(proposals) == 1
    member, theorem = proposals[0].subgoals
    assert member == canonical_member(definition, n)
    assert theorem == Toda55UniversalDoubleStatement()
    rule = cited_toda55_double_inference_rule(goal)
    inferred = ProofStep(member, (), ProofRule.INFERENCE)
    cited = ProofStep(theorem, (), ProofRule.GIVEN)
    assert len(find_inference_matches_for_rule(rule, (inferred, cited))) == 1
    assert not find_inference_matches_for_rule(
        rule, (ProofStep(member, (), ProofRule.GIVEN), cited),
    )
    assert not find_inference_matches_for_rule(
        rule, (inferred, ProofStep(theorem, (), ProofRule.INFERENCE)),
    )
    assert not expand_cited_toda55_double(
        Relation(Multiple(2, nu), IteratedSuspension(prior, 3), RelationType.EQUALITY),
        sources + (definition,),
    )
    wrong = replace(nu, generator=GeneratorSymbol("μ", index=n))
    assert not expand_cited_toda55_double(
        Relation(Multiple(2, wrong), IteratedSuspension(prior, 2), RelationType.EQUALITY),
        sources + (definition,),
    )


def test_public_screen_exposes_two_source_only_leaves_before_target() -> None:
    goal, citing, screened, provider = _public_context()
    refs = {type(link.step.conclusion): link.step for link in screened.proof_links
            if link.step is not None and link.step.rule is ProofRule.GIVEN}
    assert Toda48UniversalConditionalStatement in refs
    assert Toda55UniversalDoubleStatement in refs
    assert refs[Toda48UniversalConditionalStatement].conclusion == Toda48UniversalConditionalStatement()
    assert refs[Toda55UniversalDoubleStatement].conclusion == Toda55UniversalDoubleStatement()
    assert goal not in tuple(step.conclusion for step in refs.values())
    options = provider(CyclicStructureStatement(goal.lhs, goal.rhs.generator, 8))
    candidates = tuple(x for x in options if x.rule.name ==
                       "finite cyclic extension by an index-two injective image")
    assert len(candidates) == 1
    index, prior, doubled = candidates[0].subgoals
    assert isinstance(index, Toda48IndexTwoDoubleSuspensionStatement)
    assert prior.lhs == TodaPrimaryGroup(6, 3)
    double_proposals = tuple(p for p in provider(doubled) if p.rule.name ==
                             "specialize cited Toda (5.5) doubled nu-family identity")
    assert len(double_proposals) == 1
    index_step = reconstruct_registered_goal(
        index, screened, citing, provider, lookup_mode="typed_reference",
    )
    double_step = reconstruct_registered_goal(
        doubled, screened, citing, provider, lookup_mode="typed_reference",
    )
    assert index_step.rule is ProofRule.INFERENCE
    assert double_step.rule is ProofRule.INFERENCE
    assert any(s.rule is ProofRule.GIVEN and
               s.conclusion == Toda55UniversalDoubleStatement()
               for s in double_step.premises)
```

## `tests/test_patch.py`

```python
"""Guarded local replacement contracts; no real repository mutation."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r6_source_extension.patch import (
    connect_shared,
    replace_r3r4_test,
    replace_preflight_audit,
)


SHARED_FIXTURE = b'''def build_shared_typed_bridge():
    if True:
        sources = sources + (build_cited_prop22_right_reference(production),)
    registry = UnifiedStatementRegistry()
    return registry

def shared_expansion_provider():
    def expand(goal):
        options.extend(expand_toda48_index_two(goal))
        options.extend(expand_finite_index_two_cyclic_structure(goal))
        options.extend(expand_finite_cyclic_relation(goal))
        return options
    return expand
'''


def test_shared_patch_only_two_full_function_targets_and_idempotent() -> None:
    revised = connect_shared(SHARED_FIXTURE)
    assert connect_shared(revised) == revised
    assert revised.count(b'build_cited_extension_sources()') == 1
    assert revised.count(b'expand_cited_toda55_double(goal, tuple(available))') == 1
    assert ast.parse(revised)


def test_shared_patch_rejects_changed_or_duplicated_anchor() -> None:
    with pytest.raises(ValueError, match='insertion context'):
        connect_shared(SHARED_FIXTURE.replace(b'expand_toda48_index_two', b'unreviewed_rule'))
    with pytest.raises(ValueError, match='insertion context'):
        connect_shared(SHARED_FIXTURE + SHARED_FIXTURE)


def test_crlf_checkout_preserves_line_endings_and_syntax() -> None:
    crlf = SHARED_FIXTURE.replace(b'\n', b'\r\n')
    transformed = connect_shared(crlf)
    assert b'\r\n' in transformed
    assert transformed.replace(b'\r\n', b'').count(b'\n') == 0
    assert ast.parse(transformed)


def test_prior_regression_test_patch_only_accepts_reviewed_chain() -> None:
    source = (
        "from pathlib import Path\n"
        "\n"
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    assert current in (r3r4, insert_shared(r3r4))\n"
    ).encode('utf-8')
    transformed = replace_r3r4_test(source)
    assert replace_r3r4_test(transformed) == transformed
    assert b'connect_shared(r3r5)' in transformed
    with pytest.raises(ValueError, match='insertion context'):
        replace_r3r4_test(source.replace(b'insert_shared(r3r4)', b'arbitrary(r3r4)'))


def test_preflight_complete_function_replacement_parses() -> None:
    source = (
        'from __future__ import annotations\n'
        'from pathlib import Path\n'
        'from typing import Any\n'
        '\n'
        'def inspect_source_provider(root: Path) -> dict[str, Any]:\n'
        '    return {"state": "COMMITTED"}\n'
        '\n'
        'def unaffected():\n'
        '    return 1\n'
    ).encode('utf-8')
    updated = replace_preflight_audit(source)
    assert b'def unaffected():' in updated
    assert updated.count(b'def inspect_source_provider') == 1
    assert ast.parse(updated)
```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $RepoRoot

if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) {
    throw 'Execute from the extracted package inside ehp_proof repository'
}

python -m phase174_r3_r6_source_extension.patch --dry-run
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 source/HEAD DryRun failed' }

python -m phase174_r3_r6_source_extension.verify
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 adopted Toda source verification failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R3R6_DRY_RUN_GATE=PASS'
    exit 0
}

python -m phase174_r3_r6_source_extension.patch
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 guarded patch failed' }

python -m phase174_r3_r6_source_extension.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 source ancestry audit failed' }

python -m pytest -q `
    phase174_r3_r6_source_extension/tests/test_source.py `
    phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
    phase174_r3_r5_preflight/tests/test_audit.py `
    phase174_r3_r4_public_delta_connection/tests/test_connection.py
if ($LASTEXITCODE -ne 0) { throw 'R3-R6 focused pytest failed' }

Write-Output 'PHASE174_R3R6_FOCUSED_PYTEST=PASS'
Write-Output 'PHASE174_R3R6_FULL_PYTEST_NOT_RUN=True'
Write-Output 'PHASE174_R3R6_GATE=PASS'
```

