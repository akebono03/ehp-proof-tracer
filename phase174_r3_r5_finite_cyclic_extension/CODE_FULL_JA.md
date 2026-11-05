# Phase 174 R3-R5 — コード全文（Git日本語ファイル名修正版）

変更対象（既存）: `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()`、`phase174_r3_r4_public_delta_connection/tests/test_connection.py` の `test_r3r4_real_production_file_has_only_reviewed_wiring()`、`phase174_r3_r5_preflight/audit.py` の `inspect_source_provider()`。その3関数は本実行時に `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r5_impl\` に全文出力。既存トップレベル import は変更しない。

今回の修正は `patch.py` の `verify_originals()` および `tests/test_head_lineage.py` 内の Git 出力モックと1件の新規テスト。以下に変更ファイルの import を含む**全文**と ZIP 内実装関数・テストを掲載する。

`tests/test_head_lineage.py` の新しいテスト `test_unicode_path_from_real_git_is_not_octal_quoted` はファイル末尾に追加。既存の保護条件は残す。

## `patch.py`

```python
"""Guarded R3-R5 patch; adapt only directly affected previous tests.

All three modified functions are exported in their entirety after application.
Original bytes and line endings are preserved around the reviewed insertions.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

SHARED = "phase165_r52_r9_shared_math.py"
TEST = "phase174_r3_r4_public_delta_connection/tests/test_connection.py"
PREFLIGHT = "phase174_r3_r5_preflight/audit.py"
PREFLIGHT_COMMITTED_BLOB = "989d14731e88053554b491324475f319b8be2660"
REVIEWED_HEAD = "45d97b2adc73c2347866de28b344fce1e6d2c095"
BASE_COMMIT = "7ad6ae86714251a88f7002981c0aa20fb51e7069"
SHARED_BLOB = "b8e8bf820e470a9cad9bad2092cd4ed1a7fc55ac"
TEST_FUNCTION = "test_r3r4_real_production_file_has_only_reviewed_wiring"
OLD_SHARED = (
    "        options.extend(expand_delta_zero_from_injection(goal))\n"
    "        options.extend(expand_finite_cyclic_relation(goal))\n"
)
NEW_SHARED = (
    "        options.extend(expand_delta_zero_from_injection(goal))\n"
    "        from phase174_r3_r5_finite_cyclic_extension.rule import (\n"
    "            expand_finite_index_two_cyclic_structure, expand_toda48_index_two,\n"
    "        )\n"
    "        options.extend(expand_toda48_index_two(goal))\n"
    "        options.extend(expand_finite_index_two_cyclic_structure(goal))\n"
    "        options.extend(expand_finite_cyclic_relation(goal))\n"
)


def git(*args: str) -> bytes:
    return subprocess.run(
        ("git",) + args, check=True, capture_output=True,
    ).stdout


def blob_sha(contents: bytes) -> str:
    return hashlib.sha1(
        b"blob " + str(len(contents)).encode("ascii") + b"\x00" + contents
    ).hexdigest()


def insert_shared(original: bytes) -> bytes:
    ending = b"\r\n" if b"\r\n" in original else b"\n"
    old = OLD_SHARED.encode("utf-8").replace(b"\n", ending)
    new = NEW_SHARED.encode("utf-8").replace(b"\n", ending)
    if original.count(new) == 1 and original.count(old) == 0:
        return original
    if original.count(old) != 1 or original.count(new) != 0:
        raise ValueError("R3-R4 provider insertion context is not unique")
    changed = original.replace(old, new)
    ast.parse(changed.decode("utf-8-sig"))
    return changed


def extract_function(contents: bytes, name: str) -> str:
    string = contents.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(string)
    definitions = [
        item for item in tree.body
        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef))
        and item.name == name
    ]
    if len(definitions) != 1:
        raise ValueError("Expected exactly one complete function: " + name)
    node = definitions[0]
    return "\n".join(string.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"


def replace_r3r4_test(original: bytes) -> bytes:
    """Keep the earlier R3-R4 invariant, allowing only the reviewed R3-R5 tail."""
    ending = b"\r\n" if b"\r\n" in original else b"\n"
    string = original.decode("utf-8-sig").replace("\r\n", "\n")
    tree = ast.parse(string)
    definitions = [
        node for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == TEST_FUNCTION
    ]
    if len(definitions) != 1:
        raise ValueError("R3-R4 guarded test function not found exactly once")
    node = definitions[0]
    old = "\n".join(string.splitlines()[node.lineno - 1:node.end_lineno]) + "\n"
    expected = (
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r4_public_delta_connection.patch import reviewed_head_bytes\n"
        "    old = reviewed_head_bytes()\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    assert current == replace_provider_call(old)\n"
        "    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'\n"
        "    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1\n"
    )
    replacement = (
        "def test_r3r4_real_production_file_has_only_reviewed_wiring():\n"
        "    from phase174_r3_r5_finite_cyclic_extension.patch import git, insert_shared\n"
        "    old = git('show', 'b5f5208a7e23397834e4a38ad307c660a4f26b59:phase165_r52_r9_shared_math.py')\n"
        "    current = Path('phase165_r52_r9_shared_math.py').read_bytes()\n"
        "    r3r4 = replace_provider_call(old)\n"
        "    assert current in (r3r4, insert_shared(r3r4))\n"
        "    assert git_blob_sha(old) == 'f49b0b7699e29ec1b78d73578dc66a0e33d6e336'\n"
        "    assert current.count(b'options.extend(expand_delta_zero_from_injection(goal))') == 1\n"
    )
    if old == replacement:
        return original
    if old != expected:
        raise ValueError("R3-R4 original regression test diverged from reviewed body")
    changed = string.replace(old, replacement, 1).replace("\n", ending.decode("ascii"))
    result = changed.encode("utf-8")
    if original.startswith(b"\xef\xbb\xbf"):
        result = b"\xef\xbb\xbf" + result
    ast.parse(result.decode("utf-8-sig"))
    return result



def replace_preflight_provider_guard(original: bytes) -> bytes:
    """Accept only the reviewed committed preflight file or its exact patch.

    The preflight package was committed after the previous implementation ZIP
    had been prepared. It is now a tracked file, guarded by its Git blob.
    """
    committed = git("show", "HEAD:" + PREFLIGHT)
    if blob_sha(committed) != PREFLIGHT_COMMITTED_BLOB:
        raise ValueError("Reviewed preflight Git blob changed")
    old = (
        '        from phase174_r3_r4_public_delta_connection.patch import replace_provider_call\n'
        '        if source.encode("utf-8") != replace_provider_call(committed.encode("utf-8")):\n'
        '            raise ValueError("Unreviewed production source modifications")'
    )
    new = (
        '        from phase174_r3_r4_public_delta_connection.patch import replace_provider_call\n'
        '        from phase174_r3_r5_finite_cyclic_extension.patch import insert_shared\n'
        '        reviewed_r3r4 = replace_provider_call(committed.encode("utf-8"))\n'
        '        if source.encode("utf-8") not in (reviewed_r3r4, insert_shared(reviewed_r3r4)):\n'
        '            raise ValueError("Unreviewed production source modifications")'
    )
    old_bytes = old.encode("utf-8")
    if committed.count(old_bytes) != 1:
        raise ValueError("Reviewed preflight insertion context changed")
    modified = committed.replace(old_bytes, new.encode("utf-8"), 1)
    ast.parse(modified.decode("utf-8-sig"))
    if original == committed or original == modified:
        return modified
    raise ValueError("Refusing unrelated edit to committed preflight audit")


def verify_originals() -> tuple[bytes, bytes]:
    head = git("rev-parse", "HEAD").decode().strip()
    branch = git("branch", "--show-current").decode().strip()
    remote_result = git("ls-remote", "origin", "refs/heads/develop").decode().split()
    if len(remote_result) != 2:
        raise ValueError("Cannot uniquely read remote develop HEAD")
    remote = remote_result[0]
    if branch != "develop" or head != REVIEWED_HEAD or remote != REVIEWED_HEAD:
        raise ValueError(
            "Reviewed develop HEAD mismatch: local=" + head
            + " remote=" + remote + " expected=" + REVIEWED_HEAD
        )
    git("merge-base", "--is-ancestor", BASE_COMMIT, head)
    # Keep the entire reviewed-path check, but request literal UTF-8 paths.
    # By default Git quotes non-ASCII filenames as C-style octal escapes,
    # e.g. the reviewed Japanese .md pathname would never equal its literal.
    changed = set(git(
        "-c", "core.quotePath=false", "diff", "--name-only",
        BASE_COMMIT + ".." + head,
    ).decode("utf-8").splitlines())
    reviewed_changes = {
        "phase174_r3_r5_preflight/README.md",
        "phase174_r3_r5_preflight/__init__.py",
        "phase174_r3_r5_preflight/audit.py",
        "phase174_r3_r5_preflight/run.ps1",
        "phase174_r3_r5_preflight/tests/__init__.py",
        "phase174_r3_r5_preflight/tests/test_audit.py",
        "phase174_r3_r5_preflight/実装前監査.md",
    }
    if changed != reviewed_changes:
        unexpected = sorted(changed - reviewed_changes)
        missing = sorted(reviewed_changes - changed)
        raise ValueError(
            "Unexpected files changed since the reviewed R3-R4 base: "
            + f"unexpected={unexpected!r} missing={missing!r}"
        )
    original_shared = git("show", "HEAD:" + SHARED)
    original_test = git("show", "HEAD:" + TEST)
    original_preflight = git("show", "HEAD:" + PREFLIGHT)
    if blob_sha(original_shared) != SHARED_BLOB:
        raise ValueError("Shared provider no longer has the reviewed Git blob")
    if blob_sha(original_preflight) != PREFLIGHT_COMMITTED_BLOB:
        raise ValueError("Committed preflight audit differs from the reviewed Git blob")
    if git("diff", "--cached", "--name-only").strip():
        raise ValueError("Staged changes need manual review")
    return original_shared, original_test

def apply(*, dry_run: bool) -> dict[str, object]:
    original_shared, original_test = verify_originals()
    modified_shared = insert_shared(original_shared)
    modified_test = replace_r3r4_test(original_test)
    original_preflight = git("show", "HEAD:" + PREFLIGHT)
    modified_preflight = replace_preflight_provider_guard(original_preflight)
    targets = ((SHARED, original_shared, modified_shared),
               (TEST, original_test, modified_test),
               (PREFLIGHT, original_preflight, modified_preflight))
    states: dict[str, str] = {}
    for name, before, after in targets:
        current = Path(name).read_bytes()
        if current == before:
            states[name] = "REVIEWED_ORIGINAL"
        elif current == after:
            states[name] = "ALREADY_APPLIED"
        else:
            raise ValueError("Refusing to overwrite unrelated user edit: " + name)
    if not dry_run:
        for name, before, after in targets:
            if states[name] == "REVIEWED_ORIGINAL":
                Path(name).write_bytes(after)
        for name, before, after in targets:
            if Path(name).read_bytes() != after:
                raise ValueError("Production or test replacement differs: " + name)
        folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
        folder = folder / "EHPProofTracerAudit" / "phase174_r3_r5_impl"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "shared_expansion_provider_FULL.py").write_text(
            extract_function(modified_shared, "shared_expansion_provider"),
            encoding="utf-8",
        )
        (folder / "test_r3r4_source_guard_FULL.py").write_text(
            extract_function(modified_test, TEST_FUNCTION), encoding="utf-8",
        )
        (folder / "preflight_inspect_source_provider_FULL.py").write_text(
            extract_function(modified_preflight, "inspect_source_provider"),
            encoding="utf-8",
        )
    return {
        "states": states,
        "new_shared_blob": blob_sha(modified_shared),
        "new_test_blob": blob_sha(modified_test),
        "only_three_reviewed_existing_files": True,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = apply(dry_run=args.dry_run)
    print("PHASE174_R3R5_IMPL_SOURCE_GUARD=PASS")
    print("PHASE174_R3R5_IMPL_SHARED_BLOB=" + result["new_shared_blob"])
    print("PHASE174_R3R5_IMPL_TEST_BLOB=" + result["new_test_blob"])
    print("PHASE174_R3R5_IMPL_REVIEWED_CHANGES=3")
    if args.dry_run:
        print("PHASE174_R3R5_IMPL_DRY_RUN=PASS")
    else:
        print("PHASE174_R3R5_IMPL_SOURCE_PATCH=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_head_lineage.py`

```python
"""Focused regression tests for the reviewed post-R3-R4 HEAD transition."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase174_r3_r5_finite_cyclic_extension import patch


REVIEWED_CHANGED_PATHS = (
    "phase174_r3_r5_preflight/README.md",
    "phase174_r3_r5_preflight/__init__.py",
    "phase174_r3_r5_preflight/audit.py",
    "phase174_r3_r5_preflight/run.ps1",
    "phase174_r3_r5_preflight/tests/__init__.py",
    "phase174_r3_r5_preflight/tests/test_audit.py",
    "phase174_r3_r5_preflight/実装前監査.md",
)


def reviewed_git_output(*, remote: str | None = None, changed: tuple[str, ...] = REVIEWED_CHANGED_PATHS):
    """Return a controlled git responder; do not alter the real repository."""
    shared = b"reviewed synthetic shared provider"
    preflight = b"reviewed synthetic committed preflight"
    test = b"reviewed synthetic test"
    remote_head = patch.REVIEWED_HEAD if remote is None else remote
    responses = {
        ("rev-parse", "HEAD"): patch.REVIEWED_HEAD.encode(),
        ("branch", "--show-current"): b"develop\n",
        ("ls-remote", "origin", "refs/heads/develop"):
            (remote_head + "\trefs/heads/develop\n").encode(),
        ("merge-base", "--is-ancestor", patch.BASE_COMMIT, patch.REVIEWED_HEAD): b"",
        ("-c", "core.quotePath=false", "diff", "--name-only",
         patch.BASE_COMMIT + ".." + patch.REVIEWED_HEAD):
            ("\n".join(changed) + "\n").encode("utf-8"),
        ("show", "HEAD:" + patch.SHARED): shared,
        ("show", "HEAD:" + patch.TEST): test,
        ("show", "HEAD:" + patch.PREFLIGHT): preflight,
        ("diff", "--cached", "--name-only"): b"",
    }

    def fake_git(*args: str) -> bytes:
        return responses[args]

    return fake_git, shared, preflight, test


def test_reviewed_head_accepts_only_preflight_commit(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_git, shared, preflight, test = reviewed_git_output()
    monkeypatch.setattr(patch, "git", fake_git)
    monkeypatch.setattr(patch, "SHARED_BLOB", patch.blob_sha(shared))
    monkeypatch.setattr(patch, "PREFLIGHT_COMMITTED_BLOB", patch.blob_sha(preflight))
    assert patch.verify_originals() == (shared, test)


def test_changed_remote_head_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_git, shared, preflight, test = reviewed_git_output(remote="0" * 40)
    monkeypatch.setattr(patch, "git", fake_git)
    with pytest.raises(ValueError, match="Reviewed develop HEAD mismatch"):
        patch.verify_originals()


def test_unreviewed_commit_path_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_git, shared, preflight, test = reviewed_git_output(
        changed=REVIEWED_CHANGED_PATHS + ("unrelated.py",)
    )
    monkeypatch.setattr(patch, "git", fake_git)
    with pytest.raises(ValueError, match="Unexpected files changed"):
        patch.verify_originals()


def test_preflight_replacement_is_exact_idempotent_and_rejects_edits(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    base = Path(__file__).resolve().parents[2] / patch.PREFLIGHT
    # The committed original is loaded from git instead of trusting the current
    # working tree, which may already contain the narrowly reviewed update.
    from subprocess import run
    committed = run(
        ("git", "show", "HEAD:" + patch.PREFLIGHT),
        check=True, capture_output=True,
    ).stdout
    if patch.blob_sha(committed) != patch.PREFLIGHT_COMMITTED_BLOB:
        pytest.fail("Reviewed preflight original changed at HEAD")
    updated = patch.replace_preflight_provider_guard(committed)
    assert updated != committed
    assert patch.replace_preflight_provider_guard(updated) == updated
    with pytest.raises(ValueError, match="Refusing unrelated edit"):
        patch.replace_preflight_provider_guard(committed + b"# unrelated edit\n")


def test_unicode_path_from_real_git_is_not_octal_quoted(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Guard compares literal UTF-8 paths, never Git's C-quoted names.

    Exercise a real temporary Git repository, not just a mocked Git reply.
    No files in the user's EHP repository are written by this test.
    """
    import subprocess

    def run(*args: str) -> bytes:
        return subprocess.run(
            ("git",) + args,
            check=True, cwd=tmp_path, capture_output=True,
        ).stdout

    run("init", "-q")
    run("-c", "user.name=EHP Test", "-c", "user.email=ehp@example.invalid",
        "commit", "-q", "--allow-empty", "-m", "initial")
    base = run("rev-parse", "HEAD").decode("ascii").strip()
    path = "phase174_r3_r5_preflight/実装前監査.md"
    file = tmp_path / path
    file.parent.mkdir(parents=True)
    file.write_text("source verified\n", encoding="utf-8")
    run("add", "--", path)
    run("-c", "user.name=EHP Test", "-c", "user.email=ehp@example.invalid",
        "commit", "-q", "-m", "add Japanese audit file")

    monkeypatch.chdir(tmp_path)
    reviewed_paths = patch.git(
        "-c", "core.quotePath=false", "diff", "--name-only",
        base + "..HEAD",
    ).decode("utf-8").splitlines()
    assert reviewed_paths == [path]
```

## `rule.py`

```python
"""Phase 174 R3-R5: typed backward obligations for a cyclic index-two extension.

This module supplies two generic mathematical inferences, NOT new axioms.
Toda (4.8) remains a separate cited subgoal. The ordinary proof engine must
establish it and the Delta-zero, prior cyclic relation, and doubled relation.
No sphere dimension, generator name or bibliography ID is hard-coded.
"""
from __future__ import annotations

from dataclasses import dataclass

from expression import HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import (
    FiniteCyclicGroup,
    TodaDeltaMap,
    TodaIteratedSuspensionMap,
    TodaPrimaryGroup,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import GoalExpansion
from phase169_r10e5_composite_generator_image.rule import _endpoints
from proof import InferenceRule, PremisePattern, ProofRule, Relation, RelationType
from toda_rules import TodaDeltaZeroStatement


@dataclass(frozen=True)
class Toda48UniversalConditionalStatement:
    """Citable source *obligation* for Toda (4.8), not an assumed citation.

    This phase does NOT register a GIVEN for this statement. Any future
    source bridge must independently verify text and publication precedence.
    """


@dataclass(frozen=True)
class Toda48IndexTwoDoubleSuspensionStatement:
    """E^2:A -> B is injective and B/E^2(A) has order two."""

    map: TodaIteratedSuspensionMap
    quotient_order: int = 2


def toda48_delta_goal(index_goal: object) -> TodaDeltaZeroStatement | None:
    """Check the entire even-n (4.8) geometry before proposing its Delta goal."""
    if not isinstance(index_goal, Toda48IndexTwoDoubleSuspensionStatement):
        return None
    mapping = index_goal.map
    if not isinstance(mapping, TodaIteratedSuspensionMap):
        return None
    if type(mapping.exponent) is not int or mapping.exponent != 2:
        return None
    if type(index_goal.quotient_order) is not int or index_goal.quotient_order != 2:
        return None
    a, b = mapping.source_group, mapping.target_group
    if not isinstance(a, TodaPrimaryGroup) or not isinstance(b, TodaPrimaryGroup):
        return None
    if any(type(x) is not int for x in (
        a.group_dimension, a.sphere_dimension,
        b.group_dimension, b.sphere_dimension,
    )):
        return None
    n = a.sphere_dimension + 1
    if n < 4 or n % 2 != 0:
        return None
    if a != TodaPrimaryGroup(2 * n - 2, n - 1):
        return None
    if b != TodaPrimaryGroup(2 * n, n + 1):
        return None
    return TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(2 * n - 1, 2 * n - 1),
        TodaPrimaryGroup(2 * n - 3, n - 1),
    ))


def toda48_index_two_inference_rule(
    goal: Toda48IndexTwoDoubleSuspensionStatement,
) -> InferenceRule:
    """Derive the conditional quotient and injection from cited (4.8) + Delta=0."""
    delta = toda48_delta_goal(goal)
    if delta is None:
        raise ValueError("invalid even-dimensional Toda (4.8) application")
    source = Toda48UniversalConditionalStatement()

    def guard(premises, bindings):
        return (
            len(premises) == 2
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule is ProofRule.GIVEN
            and premises[0].conclusion == delta
            and type(premises[1].conclusion) is Toda48UniversalConditionalStatement
            and premises[1].conclusion == source
            and toda48_delta_goal(goal) == delta
        )

    return InferenceRule(
        name="Toda (4.8) conditional index-two double suspension",
        description=(
            "The even-dimensional zero-Delta branch of Toda (4.8) makes E^2 "
            "injective and its image of index two. The stated condition and "
            "the source theorem must both be verified."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=TodaDeltaZeroStatement,
                statement_pattern=delta,
            ),
            PremisePattern(
                proof_rule=ProofRule.GIVEN,
                statement_type=Toda48UniversalConditionalStatement,
                statement_pattern=source,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_toda48_index_two(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Put the verifiable Delta-zero subgoal before the cited-source obligation."""
    delta = toda48_delta_goal(goal)
    if delta is None:
        return ()
    return (GoalExpansion(
        toda48_index_two_inference_rule(goal),
        (delta, Toda48UniversalConditionalStatement()),
    ),)


def finite_index_two_cyclic_conclusion(
    index: object,
    prior: object,
    double: object,
) -> CyclicStructureStatement | None:
    """Group theorem: |A|=m even, [B:f(A)]=2, 2b=f(a) => B=<b>, |B|=2m.

    Because f is injective, 2b has order m. For even m the only possible
    order of b is 2m; the index-two formula gives |B|=2m, so b generates B.
    Both injectivity and the index-two quotient belong to the typed index
    statement; a merely presented map is insufficient proof evidence.
    """
    if (
        not isinstance(index, Toda48IndexTwoDoubleSuspensionStatement)
        or toda48_delta_goal(index) is None
        or not isinstance(prior, Relation)
        or prior.relation_type is not RelationType.EQUALITY
        or not isinstance(prior.lhs, TodaPrimaryGroup)
        or not isinstance(prior.rhs, FiniteCyclicGroup)
        or type(prior.rhs.order) is not int
        or prior.rhs.order < 2
        or prior.rhs.order % 2 != 0
        or not isinstance(double, Relation)
        or double.relation_type is not RelationType.EQUALITY
        or not isinstance(double.lhs, Multiple)
        or type(double.lhs.coefficient) is not int
        or double.lhs.coefficient != 2
        or not isinstance(double.rhs, IteratedSuspension)
        or type(double.rhs.exponent) is not int
        or double.rhs.exponent != 2
        or not isinstance(double.lhs.expression, HomotopyElement)
    ):
        return None
    mapping = index.map
    a, b = mapping.source_group, mapping.target_group
    source_generator = prior.rhs.generator
    target_generator = double.lhs.expression
    if (
        prior.lhs != a
        or not isinstance(source_generator, HomotopyElement)
        or double.rhs.expression != source_generator
        or _endpoints(source_generator) != (a.group_dimension, a.sphere_dimension)
        or _endpoints(target_generator) != (b.group_dimension, b.sphere_dimension)
        or (double.rhs.source, double.rhs.target) != (
            b.group_dimension, b.sphere_dimension,
        )
    ):
        return None
    return CyclicStructureStatement(b, target_generator, 2 * prior.rhs.order)


def finite_index_two_cyclic_rule(
    goal: CyclicStructureStatement,
    index: Toda48IndexTwoDoubleSuspensionStatement,
    prior: Relation,
    double: Relation,
) -> InferenceRule:
    """All substantive premises must be recovered through the proof search."""
    if finite_index_two_cyclic_conclusion(index, prior, double) != goal:
        raise ValueError("invalid typed finite cyclic extension premise configuration")

    def guard(premises, bindings):
        return (
            len(premises) == 3
            and premises[0].rule is ProofRule.INFERENCE
            and premises[1].rule in (ProofRule.GIVEN, ProofRule.INFERENCE)
            and premises[2].rule is ProofRule.INFERENCE
            and premises[0].conclusion == index
            and premises[1].conclusion == prior
            and premises[2].conclusion == double
            and finite_index_two_cyclic_conclusion(
                premises[0].conclusion,
                premises[1].conclusion,
                premises[2].conclusion,
            ) == goal
        )

    return InferenceRule(
        name="finite cyclic extension by an index-two injective image",
        description=(
            "An even-order cyclic subgroup embedded with index two is the "
            "double of an element precisely when the typed double relation "
            "identifies its generator; that element generates the extension."
        ),
        premise_patterns=(
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Toda48IndexTwoDoubleSuspensionStatement,
                statement_pattern=index,
            ),
            PremisePattern(
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=prior,
            ),
            PremisePattern(
                proof_rule=ProofRule.INFERENCE,
                statement_type=Relation,
                relation_type=RelationType.EQUALITY,
                statement_pattern=double,
            ),
        ),
        match_guard=guard,
        conclusion_pattern=goal,
    )


def expand_finite_index_two_cyclic_structure(
    goal: object,
) -> tuple[GoalExpansion, ...]:
    """Use earlier database presentations as candidate GOALS, never as proofs.

    The checked dimensions are derived from Toda (4.8), not from a named
    group, hard-coded dimension, or generator. No directly GIVEN group or
    doubled relation is manufactured.
    """
    if (
        not isinstance(goal, CyclicStructureStatement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or not isinstance(goal.generator, HomotopyElement)
        or type(goal.order) is not int
        or goal.order < 4
        or goal.order % 4 != 0
    ):
        return ()
    b = goal.group
    if (
        type(b.group_dimension) is not int
        or type(b.sphere_dimension) is not int
        or b.sphere_dimension < 5
        or _endpoints(goal.generator) != (
            b.group_dimension, b.sphere_dimension,
        )
    ):
        return ()
    n = b.sphere_dimension - 1
    a = TodaPrimaryGroup(b.group_dimension - 2, b.sphere_dimension - 2)
    mapping = TodaIteratedSuspensionMap(2, a, b)
    index = Toda48IndexTwoDoubleSuspensionStatement(mapping)
    if toda48_delta_goal(index) is None:
        return ()
    from phase166_r3aj_structured_generator import (
        database_structured_group_goal_candidates,
    )
    candidates = database_structured_group_goal_candidates(
        n=a.sphere_dimension, k=a.group_dimension - a.sphere_dimension,
    )
    options: list[GoalExpansion] = []
    for prior in candidates:
        if (
            not isinstance(prior, Relation)
            or prior.relation_type is not RelationType.EQUALITY
            or prior.lhs != a
            or not isinstance(prior.rhs, FiniteCyclicGroup)
            or prior.rhs.order * 2 != goal.order
        ):
            continue
        double = Relation(
            Multiple(2, goal.generator),
            IteratedSuspension(prior.rhs.generator, 2),
            RelationType.EQUALITY,
        )
        if finite_index_two_cyclic_conclusion(index, prior, double) != goal:
            continue
        options.append(GoalExpansion(
            finite_index_two_cyclic_rule(goal, index, prior, double),
            (index, prior, double),
        ))
    # Avoid silently selecting between conflicting lower presentations.
    return tuple(options) if len(options) == 1 else ()
```

## `audit.py`

```python
"""Read-only post-patch gate: real screened proposals, not invented evidence."""
from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile

from homotopy_groups import TodaDeltaMap, TodaPrimaryGroup
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase174_r3_r5_finite_cyclic_extension.patch import (
    SHARED, TEST, PREFLIGHT, insert_shared, replace_r3r4_test,
    replace_preflight_provider_guard, git,
)
from proof import ProofRule
from toda_rules import TodaDeltaZeroStatement


def audit() -> dict[str, object]:
    """A proposal route is not a completed proof; preserve this distinction."""
    if (Path(SHARED).read_bytes() != insert_shared(git("show", "HEAD:" + SHARED))
            or Path(TEST).read_bytes() != replace_r3r4_test(git("show", "HEAD:" + TEST))
            or Path(PREFLIGHT).read_bytes() != replace_preflight_provider_guard(Path(PREFLIGHT).read_bytes())):
        raise ValueError("Production source or regression test is not reviewed")
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=5, k=3)
    if len(goals) != 1:
        raise ValueError("Unexpected public target count")
    target = goals[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    if citing is None:
        raise ValueError("Publication position is missing")
    screened = prefer_universal_prop42_derivation(screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing,
        explicit_publication_target=True,
    ))
    provider = shared_expansion_provider(screened, proof_target=target)
    cyclic = CyclicStructureStatement(target.lhs, target.rhs.generator, target.rhs.order)
    cyclic_options = tuple(
        x for x in provider(cyclic)
        if x.rule.name == "finite cyclic extension by an index-two injective image"
    )
    if len(cyclic_options) != 1:
        raise ValueError("Typed cyclic root is not uniquely expanded")
    index, prior, doubled = cyclic_options[0].subgoals
    index_options = tuple(
        x for x in provider(index)
        if x.rule.name == "Toda (4.8) conditional index-two double suspension"
    )
    if len(index_options) != 1:
        raise ValueError("Conditional Toda (4.8) expansion is missing")
    delta, theorem = index_options[0].subgoals
    expected = TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    if delta != expected:
        raise ValueError("Root branch is not the reviewed Delta-zero condition")
    if any(
        link.step is not None and link.step.rule is ProofRule.GIVEN
        and link.step.conclusion == theorem
        for link in screened.proof_links
    ):
        raise ValueError("The unaudited general theorem was directly GIVEN")
    # Prove Delta by the ordinary citation-screened provider, independently
    # of whether all sibling obligations can be proved in this R3-R5 stage.
    inferred_delta = reconstruct_registered_goal(
        delta, screened, citing, provider, lookup_mode="typed_reference",
    )
    if inferred_delta.rule is not ProofRule.INFERENCE or inferred_delta.conclusion != delta:
        raise ValueError("An inferred Delta-zero ProofStep was not reconstructed")
    from phase165_r52_r2_search_adapter import search_registered_partial_proof
    partial = search_registered_partial_proof(
        n=5, k=3, goal=target, bridge=screened,
        citing_assertion_id=citing, expansion_provider=provider,
        lookup_mode="typed_reference",
    )
    rooted_delta = any(s.conclusion == delta and s.rule is ProofRule.INFERENCE
                       for s in partial.proven_steps)
    return {
        "phase": "174-R3-R5-IMPL",
        "mode": "SOURCE_CONDITIONAL_CYCLIC_BACKWARD_EXPANSION",
        "root_goal_type": type(target).__name__,
        "cyclic_goal_type": type(cyclic).__name__,
        "root_to_cyclic_proposals": len(cyclic_options),
        "cyclic_to_toda48_proposals": len(index_options),
        "delta_proposal_count": len(provider(delta)),
        "public_delta_independently_proved": True,
        "root_search_status": partial.status.value,
        "root_proven_steps": len(partial.proven_steps),
        "rooted_delta_in_partial_steps": rooted_delta,
        "new_source_theorem_registered": False,
        "root_group_completed_by_this_stage": partial.status.value == "complete",
        "source_citation_registration_missing": True,
        "double_relation_inference_still_required": True,
        "new_given": 0,
        "full_pytest_performed": False,
        "existing_files_modified": [SHARED, TEST, PREFLIGHT],
    }


def main() -> int:
    result = audit()
    if result["root_group_completed_by_this_stage"]:
        raise ValueError("Unexpected conclusion: unregistered source theorem supplied")
    folder = Path(os.environ.get("LOCALAPPDATA", tempfile.gettempdir()))
    folder = folder / "EHPProofTracerAudit" / "phase174_r3_r5_impl"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "audit.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE174_R3R5_IMPL_CYCLIC_PROPOSALS=" + str(result["root_to_cyclic_proposals"]))
    print("PHASE174_R3R5_IMPL_TODA48_PROPOSALS=" + str(result["cyclic_to_toda48_proposals"]))
    print("PHASE174_R3R5_IMPL_DELTA_INFERRED=" + str(result["public_delta_independently_proved"]))
    print("PHASE174_R3R5_IMPL_ROOT_STATUS=" + result["root_search_status"])
    print("PHASE174_R3R5_IMPL_ROOT_PROVEN_STEPS=" + str(result["root_proven_steps"]))
    print("PHASE174_R3R5_IMPL_ROOTED_DELTA=" + str(result["rooted_delta_in_partial_steps"]))
    print("PHASE174_R3R5_IMPL_NEW_GIVEN=0")
    print("PHASE174_R3R5_IMPL_GROUP_COMPLETE=False")
    print("PHASE174_R3R5_IMPL_REPORT=" + str(path))
    print("PHASE174_R3R5_IMPL_MATH_GATE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## `tests/test_rule.py`

```python
"""Focused type-safety, proof-rule, and public-backward-branch tests for R3-R5."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import HomotopyElement, IteratedSuspension, Multiple
from homotopy_groups import (
    FiniteCyclicGroup, TodaDeltaMap, TodaIteratedSuspensionMap, TodaPrimaryGroup,
)
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48IndexTwoDoubleSuspensionStatement,
    Toda48UniversalConditionalStatement,
    expand_finite_index_two_cyclic_structure,
    expand_toda48_index_two,
    finite_index_two_cyclic_conclusion,
    finite_index_two_cyclic_rule,
    toda48_delta_goal,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule
from toda_rules import TodaDeltaZeroStatement


def configuration(n: int = 4, m: int = 4):
    """Synthetic group-theory fixtures: no external claim is certified."""
    a = TodaPrimaryGroup(2 * n - 2, n - 1)
    b = TodaPrimaryGroup(2 * n, n + 1)
    generator_a = HomotopyElement("a", n - 1, 2 * n - 2, n - 1)
    generator_b = HomotopyElement("b", n + 1, 2 * n, n + 1)
    index = Toda48IndexTwoDoubleSuspensionStatement(TodaIteratedSuspensionMap(2, a, b))
    prior = Relation(a, FiniteCyclicGroup(m, generator_a), RelationType.EQUALITY)
    double = Relation(
        Multiple(2, generator_b), IteratedSuspension(generator_a, 2),
        RelationType.EQUALITY,
    )
    goal = CyclicStructureStatement(b, generator_b, 2 * m)
    return index, prior, double, goal


def test_toda48_even_dimension_checks_and_delta_endpoints() -> None:
    index, _, _, _ = configuration(4)
    delta = toda48_delta_goal(index)
    assert delta == TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    assert len(expand_toda48_index_two(index)) == 1
    assert expand_toda48_index_two(index)[0].subgoals == (
        delta, Toda48UniversalConditionalStatement(),
    )
    assert toda48_delta_goal(configuration(5)[0]) is None
    assert toda48_delta_goal(replace(index, quotient_order=3)) is None
    assert toda48_delta_goal(Toda48IndexTwoDoubleSuspensionStatement(
        TodaIteratedSuspensionMap(1, index.map.source_group, index.map.target_group)
    )) is None
    assert toda48_delta_goal(Toda48IndexTwoDoubleSuspensionStatement(
        TodaIteratedSuspensionMap(2, index.map.source_group, TodaPrimaryGroup(9, 5))
    )) is None


def test_toda48_index_inference_rejects_given_delta_and_missing_source() -> None:
    index, _, _, _ = configuration()
    proposal = expand_toda48_index_two(index)[0]
    delta, source = proposal.subgoals
    inferred = ProofStep(delta, (), ProofRule.INFERENCE)
    cited = ProofStep(source, (), ProofRule.GIVEN)
    matches = find_inference_matches_for_rule(proposal.rule, (inferred, cited))
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == index
    assert not find_inference_matches_for_rule(
        proposal.rule, (ProofStep(delta, (), ProofRule.GIVEN), cited)
    )
    assert not find_inference_matches_for_rule(
        proposal.rule, (inferred, ProofStep(source, (), ProofRule.INFERENCE))
    )
    assert not find_inference_matches_for_rule(
        proposal.rule,
        (ProofStep(toda48_delta_goal(configuration(6)[0]), (), ProofRule.INFERENCE), cited),
    )


def test_even_order_cyclic_extension_valid_and_odd_order_rejected() -> None:
    index, prior, double, goal = configuration()
    assert finite_index_two_cyclic_conclusion(index, prior, double) == goal
    assert finite_index_two_cyclic_conclusion(*configuration(m=3)[:3]) is None
    rule = finite_index_two_cyclic_rule(goal, index, prior, double)
    inputs = (
        ProofStep(index, (), ProofRule.INFERENCE),
        ProofStep(prior, (), ProofRule.INFERENCE),
        ProofStep(double, (), ProofRule.INFERENCE),
    )
    matches = find_inference_matches_for_rule(rule, inputs)
    assert len(matches) == 1
    assert derive_inference_proof_step(matches[0]).conclusion == goal
    assert not find_inference_matches_for_rule(rule, (
        inputs[0], inputs[1], ProofStep(double, (), ProofRule.GIVEN),
    ))
    assert not find_inference_matches_for_rule(rule, (
        ProofStep(index, (), ProofRule.GIVEN), inputs[1], inputs[2],
    ))


def test_wrong_generator_wrong_map_wrong_relation_all_rejected() -> None:
    index, prior, double, goal = configuration()
    bad_prior = Relation(
        prior.lhs,
        FiniteCyclicGroup(4, HomotopyElement("c", 3, 6, 3)),
        RelationType.EQUALITY,
    )
    bad_double = Relation(
        Multiple(2, HomotopyElement("c", 5, 8, 5)),
        double.rhs,
        RelationType.EQUALITY,
    )
    assert finite_index_two_cyclic_conclusion(index, bad_prior, double) is None
    assert finite_index_two_cyclic_conclusion(index, prior, bad_double) is not None
    assert finite_index_two_cyclic_conclusion(index, prior, bad_double) != goal
    reversed_double = Relation(double.rhs, double.lhs, RelationType.EQUALITY)
    assert finite_index_two_cyclic_conclusion(index, prior, reversed_double) is None
    wrong_index = Toda48IndexTwoDoubleSuspensionStatement(TodaIteratedSuspensionMap(
        2, index.map.source_group, TodaPrimaryGroup(10, 6),
    ))
    assert finite_index_two_cyclic_conclusion(wrong_index, prior, double) is None
    with pytest.raises(ValueError):
        finite_index_two_cyclic_rule(goal, wrong_index, prior, double)


def test_public_pi85_cyclic_root_and_delta_proposals_reached() -> None:
    """Use the real source-screened public provider, not a synthetic proposal."""
    from phase165_r52_r9_shared_math import (
        build_shared_typed_bridge, shared_expansion_provider,
    )
    from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
    from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id

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
    cyclic = CyclicStructureStatement(goal.lhs, goal.rhs.generator, 8)
    options = tuple(x for x in provider(cyclic)
                    if x.rule.name == "finite cyclic extension by an index-two injective image")
    assert len(options) == 1
    index, prior, double = options[0].subgoals
    assert prior.lhs == TodaPrimaryGroup(6, 3)
    assert prior.rhs.order == 4
    assert index.map.source_group == prior.lhs
    assert index.map.target_group == goal.lhs
    assert double.lhs == Multiple(2, goal.rhs.generator)
    index_options = tuple(x for x in provider(index)
                          if x.rule.name == "Toda (4.8) conditional index-two double suspension")
    assert len(index_options) == 1
    delta = index_options[0].subgoals[0]
    assert delta == TodaDeltaZeroStatement(TodaDeltaMap(
        TodaPrimaryGroup(7, 7), TodaPrimaryGroup(5, 3),
    ))
    assert any(x.rule.name == "EHP injective suspension and Delta-E exactness imply zero Delta"
               for x in provider(delta))
    # The source theorem is deliberately NOT created as a verified GIVEN.
    assert not any(link.step is not None and link.step.conclusion == index_options[0].subgoals[1]
                   for link in screened.proof_links)
```

## `run.ps1`

```powershell
param([switch]$DryRun)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
$OldBytecode = $env:PYTHONDONTWRITEBYTECODE
$OldEncoding = $env:PYTHONIOENCODING
try {
    $env:PYTHONDONTWRITEBYTECODE = '1'
    $env:PYTHONIOENCODING = 'utf-8'

    $IndexBefore = @(git ls-files --stage) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the Git index' }
    $StatusBefore = @(git status --porcelain=v1 --untracked-files=all) -join "`n"
    if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the working tree' }

    if ($DryRun) {
        & python -B -m phase174_r3_r5_finite_cyclic_extension.patch --dry-run
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 patch DryRun failed' }
        $IndexAfter = @(git ls-files --stage) -join "`n"
        $StatusAfter = @(git status --porcelain=v1 --untracked-files=all) -join "`n"
        if ($IndexAfter -cne $IndexBefore -or $StatusAfter -cne $StatusBefore) {
            throw 'DryRun unexpectedly changed the index or working tree'
        }
        Write-Output 'PHASE174_R3R5_IMPL_DRY_RUN_GATE=PASS'
    } else {
        & python -B -m phase174_r3_r5_finite_cyclic_extension.patch
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 patch failed' }
        & python -B -m phase174_r3_r5_finite_cyclic_extension.audit
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 public backward-expansion audit failed' }
        & python -B -m pytest -q -p no:cacheprovider `
            phase174_r3_r5_finite_cyclic_extension/tests/test_rule.py `
            phase174_r3_r5_finite_cyclic_extension/tests/test_head_lineage.py `
            phase174_r3_r4_public_delta_connection/tests/test_connection.py `
            phase174_r3_r5_preflight/tests/test_audit.py `
            phase174_r3_r3_injective_delta_zero/tests/test_rule.py
        if ($LASTEXITCODE -ne 0) { throw 'R3-R5 focused tests failed' }
        Write-Output 'PHASE174_R3R5_IMPL_FOCUSED_PYTEST=PASS'

        $IndexAfter = @(git ls-files --stage) -join "`n"
        if ($IndexAfter -cne $IndexBefore) { throw 'Git index was changed' }
        $ChangedTracked = @(git diff --name-only)
        $ExpectedTracked = @(
            'phase165_r52_r9_shared_math.py',
            'phase174_r3_r4_public_delta_connection/tests/test_connection.py',
            'phase174_r3_r5_preflight/audit.py'
        )
        foreach ($Entry in $ChangedTracked) {
            if ($ExpectedTracked -notcontains $Entry) {
                throw ('Unreviewed tracked change: ' + $Entry)
            }
        }
        Write-Output 'PHASE174_R3R5_IMPL_PREFLIGHT_COMPATIBILITY=PASS'
        Write-Output 'PHASE174_R3R5_IMPL_GIT_GUARD=PASS'
        Write-Output 'PHASE174_R3R5_IMPL_GATE=PASS'
    }
}
finally {
    $env:PYTHONDONTWRITEBYTECODE = $OldBytecode
    $env:PYTHONIOENCODING = $OldEncoding
    Pop-Location
}
```
