# R20R9R4 変更コード全文

## 変更対象と挿入位置

- 本番: `phase171_r2j_r4_r3_double_image_bridge/source.py` の末尾にある既存関数 `expand_public_cited_double_image_equality()` を、次の全文で置き換える。モジュール先頭の import は変更なし。関数内 import は全文掲載。
- 修正用: `phase171_r20r9_public_cited_double_image/install.py`（全ファイル）。
- テスト: `phase171_r20r9_public_cited_double_image/tests/test_install.py` の既存テストを変更、`tests/test_source.py` の末尾に回帰テスト追加。必要 import も全文掲載。
- `run.ps1` は R20R9R3 の分離 pytest 実行を維持。全文掲載。
- `phase165_r52_r9_shared_math.py` は変更なし。

## 本番関数全文

```python
def expand_public_cited_double_image_equality(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose a typed E-image substitution from screened source relations.

    The earlier database presentation supplies only a typed generator-image
    *goal*, never a proof step.  The cited relation and the suspension-image
    premise must be reconstructed by the ordinary proof search.  Existing
    inference rules enforce a GIVEN cited relation and an INFERENCE image.
    """
    from phase165_r3_recursive_search import GoalExpansion
    from expression import MapApplication, Multiple
    from homotopy_groups import FiniteCyclicGroup
    from map_facts import EHP_E_MAP
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase166_r3aj_structured_generator import (
        database_structured_group_goal_candidates,
    )
    from phase168_r2_8_3_generator_identity.identity import (
        same_registered_group_presentation,
    )
    from phase169_r10e5_composite_generator_image.rule import _endpoints

    if not isinstance(available, tuple):
        raise TypeError("available must contain screened fixed statements")
    if (
        not isinstance(goal, Relation)
        or goal.relation_type is not RelationType.EQUALITY
        or not isinstance(goal.lhs, Multiple)
        or type(goal.lhs.coefficient) is not int
        or goal.lhs.coefficient <= 0
        or not isinstance(goal.rhs, MapApplication)
        or goal.rhs.map != EHP_E_MAP
    ):
        return ()
    qn = _endpoints(goal.lhs.expression)
    if qn is None or _endpoints(goal.rhs.expression) != (qn[0] - 1, qn[1] - 1):
        return ()
    q, n = qn
    if type(q) is not int or type(n) is not int or n < 3 or q <= n:
        return ()
    earlier_group = TodaPrimaryGroup(q - 1, n - 1)
    middle_group = TodaPrimaryGroup(q, n)
    prior_sources = tuple(
        claim for claim in available
        if isinstance(claim, Relation)
        and claim.relation_type is RelationType.EQUALITY
        and claim.lhs == earlier_group
        and isinstance(claim.rhs, FiniteCyclicGroup)
        and type(claim.rhs.order) is int
        and claim.rhs.order > 1
    )
    if not prior_sources:
        return ()
    typed_candidates = database_structured_group_goal_candidates(
        n=n - 1, k=q - n,
    )
    cited_doubles = tuple(
        claim for claim in available
        if isinstance(claim, Relation)
        and claim.relation_type is RelationType.EQUALITY
        and claim.lhs == goal.lhs
        and _endpoints(claim.rhs) == qn
    )
    proposals: list[GoalExpansion] = []
    for typed in typed_candidates:
        if (
            not isinstance(typed, Relation)
            or typed.relation_type is not RelationType.EQUALITY
            or typed.lhs != earlier_group
            or not isinstance(typed.rhs, FiniteCyclicGroup)
            or type(typed.rhs.order) is not int
        ):
            continue
        if not any(
            typed.rhs.order == prior.rhs.order
            and same_registered_group_presentation(typed.rhs, prior.rhs)
            for prior in prior_sources
        ):
            continue
        for cited_double in cited_doubles:
            image = GeneratorImage(
                map=TodaSuspensionMap(earlier_group, middle_group),
                source_generator=typed.rhs.generator,
                target_generator=cited_double.rhs,
            )
            if typed_double_image_conclusion(cited_double, image) != goal:
                continue
            option = GoalExpansion(
                typed_double_image_rule(cited_double, image),
                (cited_double, image),
            )
            if not any(
                previous.subgoals == option.subgoals
                and previous.rule.name == option.rule.name
                for previous in proposals
            ):
                proposals.append(option)
    # Competing sound candidate routes are acceptable; the recursive search
    # selects its first certified completion.  Direct citation checks remain.
    return tuple(proposals)

```

## installer 全文

```python
"""Guarded R20R9 installer; only public typed double-image proposal wiring."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
REVIEWED_HEAD = "9c4e903c512941b9c2003105d1867cf7b694b363"
R7_SOURCE = Path("phase171_r2j_r4_r7_nonzero_nu_order/source.py")
DOUBLE_SOURCE = Path("phase171_r2j_r4_r3_double_image_bridge/source.py")
PROVIDER = Path("phase165_r52_r9_shared_math.py")
REVIEWED_BLOBS = {
    R7_SOURCE: "d395784df802a279ac03fd8a6beb443c961d5538",
    DOUBLE_SOURCE: "52d5aced7e698e508d87a35d3237ec496cc9c262",
    PROVIDER: "8d4197f5939bb344321d98d5df06373e9acbf86d",
}
R8_ADDITION = (PACKAGE / "r20r8_source_addition.py.txt").read_text(encoding="utf-8")
R9_ADDITION = (PACKAGE / "source_addition.py.txt").read_text(encoding="utf-8")
# Keep the first R20R9 source in the guard as an upgradeable, exact baseline.
LEGACY_SOURCE_DIMENSION_GUARD = "if qn is None or _endpoints(goal.rhs.expression) != qn:"
CORRECT_SOURCE_DIMENSION_GUARD = (
    "if qn is None or _endpoints(goal.rhs.expression) != (qn[0] - 1, qn[1] - 1):"
)
# R20R9R2 incorrectly compared an E-image target with the E-image input.
# The cited (5.3) equality is 2*x=y, while the goal is 2*x=E(z).
R20R9R2_CITED_TARGET_GUARD = "and claim.rhs == goal.rhs.expression"
R20R9R4_CITED_TARGET_GUARD = "and _endpoints(claim.rhs) == qn"
if R9_ADDITION.count(CORRECT_SOURCE_DIMENSION_GUARD) != 1:
    raise RuntimeError("R20R9R2 corrected source dimension guard absent or duplicated")
if R9_ADDITION.count(R20R9R4_CITED_TARGET_GUARD) != 1:
    raise RuntimeError("R20R9R4 corrected citation target guard absent or duplicated")
# The earlier R20R9R2 also set image.target_generator to the E input.
# Recover its exact pre-fix function text for full-content guard matching.
R20R9R2_GENERATOR_IMAGE_BLOCK = (
    "        image = GeneratorImage(\n"
    "            map=TodaSuspensionMap(earlier_group, middle_group),\n"
    "            source_generator=typed.rhs.generator,\n"
    "            target_generator=goal.rhs.expression,\n"
    "        )\n"
    "        for cited_double in cited_doubles:\n"
)
R20R9R4_GENERATOR_IMAGE_BLOCK = (
    "        for cited_double in cited_doubles:\n"
    "            image = GeneratorImage(\n"
    "                map=TodaSuspensionMap(earlier_group, middle_group),\n"
    "                source_generator=typed.rhs.generator,\n"
    "                target_generator=cited_double.rhs,\n"
    "            )\n"
)
if R9_ADDITION.count(R20R9R4_GENERATOR_IMAGE_BLOCK) != 1:
    raise RuntimeError("R20R9R4 corrected E-target generator block absent or duplicated")
R20R9R2_ADDITION = R9_ADDITION.replace(
    R20R9R4_GENERATOR_IMAGE_BLOCK, R20R9R2_GENERATOR_IMAGE_BLOCK, 1,
).replace(
    R20R9R4_CITED_TARGET_GUARD, R20R9R2_CITED_TARGET_GUARD, 1,
)
LEGACY_R9_ADDITION = R20R9R2_ADDITION.replace(
    CORRECT_SOURCE_DIMENSION_GUARD, LEGACY_SOURCE_DIMENSION_GUARD, 1,
)
R8_ANCHOR = "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))\n"
R8_LINE = "        options.extend(expand_public_nonzero_double_from_cited_source(goal, tuple(available)))\n"
R8_INSERTION = (
    R8_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_nonzero_double_from_cited_source,\n"
    + "        )\n"
    + R8_LINE
)
R9_INSERTION = (
    R8_LINE
    + "        from phase171_r2j_r4_r3_double_image_bridge.source import (\n"
    + "            expand_public_cited_double_image_equality,\n"
    + "        )\n"
    + "        options.extend(expand_public_cited_double_image_equality(goal, tuple(available)))\n"
)
R9_SOURCE_FLAG = "def expand_public_cited_double_image_equality("
R9_PROVIDER_FLAG = "        options.extend(expand_public_cited_double_image_equality(goal, tuple(available)))"


def normalize(data: bytes) -> str:
    """Compare complete text without changing the original newline format."""
    return data.decode("utf-8").replace("\r\n", "\n")


def adapt(text: str, original: bytes) -> bytes:
    """Preserve the original file's newline convention on replacement."""
    return (text.replace("\n", "\r\n") if b"\r\n" in original else text).encode("utf-8")


def git(*args: str) -> bytes:
    """Allow only the fixed, read-only Git queries required for preflight."""
    if args in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        pass
    elif len(args) == 2 and args[0] in {"show", "rev-parse"}:
        if args[1] not in {REVIEWED_HEAD + ":" + path.as_posix() for path in REVIEWED_BLOBS}:
            raise ValueError("unreviewed Git reference")
    else:
        raise ValueError("unapproved Git command")
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return result.stdout if args[0] == "show" else result.stdout.strip()


def expected_r20r8(reviewed: dict[Path, str]) -> dict[Path, str]:
    """Reconstruct exact R20R8 content from the verified R20R7 commit."""
    source = reviewed[R7_SOURCE]
    provider = reviewed[PROVIDER]
    if source.count("def expand_public_injected_generator_nonzero(") != 1:
        raise RuntimeError("R20R7 source is absent in reviewed commit")
    if source.count("def expand_public_nonzero_double_from_cited_source(") != 0:
        raise RuntimeError("R20R8 source already present in reviewed commit")
    if provider.count(R8_ANCHOR) != 1:
        raise RuntimeError("R20R7 provider anchor is missing or duplicated")
    return {
        R7_SOURCE: source.rstrip("\n") + "\n\n" + R8_ADDITION.lstrip("\n"),
        PROVIDER: provider.replace(R8_ANCHOR, R8_INSERTION, 1),
        DOUBLE_SOURCE: reviewed[DOUBLE_SOURCE],
    }


def patched_text(before: dict[Path, str]) -> dict[Path, str]:
    """Generate full replacements for the two R20R9 target source files."""
    source, provider = before[DOUBLE_SOURCE], before[PROVIDER]
    if source.count(R9_SOURCE_FLAG) != 0:
        raise RuntimeError("R20R9 already appears in reviewed R20R8 source")
    if provider.count(R8_LINE) != 1 or provider.count(R9_PROVIDER_FLAG) != 0:
        raise RuntimeError("R20R8 provider anchor absent or duplicated")
    return {
        R7_SOURCE: before[R7_SOURCE],
        DOUBLE_SOURCE: source.rstrip("\n") + "\n\n" + R9_ADDITION.lstrip("\n"),
        PROVIDER: provider.replace(R8_LINE, R9_INSERTION, 1),
    }


def legacy_r20r9_text(before: dict[Path, str]) -> dict[Path, str]:
    """Reconstruct the already-installed R20R9 source with its wrong E-input guard.

    The provider is unchanged. Only this exact, reviewed previous source may
    be migrated; arbitrary local edits must still fail closed.
    """
    after = patched_text(before)
    legacy = dict(after)
    old_source = before[DOUBLE_SOURCE].rstrip("\n") + "\n\n" + LEGACY_R9_ADDITION.lstrip("\n")
    if old_source.count(LEGACY_SOURCE_DIMENSION_GUARD) != 1:
        raise RuntimeError("R20R9R1 old guard absent or duplicated")
    legacy[DOUBLE_SOURCE] = old_source
    return legacy


def r20r9r2_text(before: dict[Path, str]) -> dict[Path, str]:
    """Reconstruct the complete, exact R20R9R2 source installed previously."""
    after = patched_text(before)
    previous = dict(after)
    previous[DOUBLE_SOURCE] = (
        before[DOUBLE_SOURCE].rstrip("\n") + "\n\n" + R20R9R2_ADDITION.lstrip("\n")
    )
    if previous[DOUBLE_SOURCE].count(R20R9R2_CITED_TARGET_GUARD) != 1:
        raise RuntimeError("R20R9R2 previous citation guard absent or duplicated")
    return previous


def checked_worktree() -> tuple[str, dict[Path, bytes], dict[Path, str], dict[Path, str]]:
    """Accept exact R20R8, R20R9R1, R20R9R2, or R20R9R4 content.

    The full reviewed R20R7 snapshot and deterministic transformations
    are used. Do not permit unrelated local edits or partial source states.
    """
    if git("branch", "--show-current").decode("utf-8") != "develop":
        raise RuntimeError("develop branch required")
    head = git("rev-parse", "HEAD").decode("ascii")
    reviewed: dict[Path, str] = {}
    original: dict[Path, bytes] = {}
    for path, reviewed_sha in REVIEWED_BLOBS.items():
        ref = REVIEWED_HEAD + ":" + path.as_posix()
        if git("rev-parse", ref).decode("ascii") != reviewed_sha:
            raise RuntimeError("reviewed commit baseline drift: " + path.as_posix())
        reviewed[path] = normalize(git("show", ref))
        original[path] = (ROOT / path).read_bytes()
    before = expected_r20r8(reviewed)
    after = patched_text(before)
    legacy = legacy_r20r9_text(before)
    previous = r20r9r2_text(before)
    edited = (DOUBLE_SOURCE, PROVIDER)
    if normalize(original[R7_SOURCE]) != before[R7_SOURCE]:
        raise RuntimeError("unexpected R20R8 dependency edit: " + R7_SOURCE.as_posix())
    if all(normalize(original[path]) == before[path] for path in edited):
        return head, original, before, after
    if all(normalize(original[path]) == legacy[path] for path in edited):
        return head, original, before, after
    if all(normalize(original[path]) == previous[path] for path in edited):
        return head, original, before, after
    if all(normalize(original[path]) == after[path] for path in edited):
        return head, original, before, after
    raise RuntimeError("partial R20R9 state or unexpected local edits")


def run_install(*, dry_run: bool) -> None:
    """Back up and replace only files that differ from corrected R20R9R2."""
    head, original, before, after = checked_worktree()
    edited = (DOUBLE_SOURCE, PROVIDER)
    changed = tuple(path for path in edited if normalize(original[path]) != after[path])
    already = not changed
    print("PHASE171_R20R9_HEAD=" + head, flush=True)
    print("PHASE171_R20R9_SOURCE_CONTENT_GUARD=PASS", flush=True)
    if dry_run:
        print("PHASE171_R20R9_DRY_RUN=PASS", flush=True)
        print("PHASE171_R20R9_ALREADY_INSTALLED=" + str(already), flush=True)
        print("PHASE171_R20R9R2_CORRECTION_NEEDED=" + str(bool(changed)), flush=True)
        return
    if changed:
        backup = PACKAGE / "output" / ("backup_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        backup.mkdir(parents=True, exist_ok=False)
        for path in changed:
            (backup / path.name).write_bytes(original[path])
        try:
            for path in changed:
                (ROOT / path).write_bytes(adapt(after[path], original[path]))
        except BaseException:
            for path in changed:
                (ROOT / path).write_bytes(original[path])
            raise
        print("PHASE171_R20R9_BACKUP=" + str(backup), flush=True)
    checked_worktree()
    out = PACKAGE / "output"
    out.mkdir(parents=True, exist_ok=True)
    for path in edited:
        full_text = normalize((ROOT / path).read_bytes())
        (out / (path.stem.upper() + "_" + path.parent.name.upper() + "_FULL_AFTER.py")).write_text(full_text, encoding="utf-8")
    shared = normalize((ROOT / PROVIDER).read_bytes())
    start = shared.index("def shared_expansion_provider(")
    end = shared.index("\ndef search_shared_group_goal(", start)
    (out / "SHARED_EXPANSION_PROVIDER_FUNCTION_FULL_AFTER.py").write_text(
        shared[start:end].rstrip("\n") + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R9_SOURCE_CHANGES=" + str(len(changed)), flush=True)
    print("PHASE171_R20R9R2_SOURCE_DIMENSION_GUARD=CORRECTED", flush=True)
    print("PHASE171_R20R9R4_CITED_IMAGE_TARGET_GUARD=CORRECTED", flush=True)
    print("PHASE171_R20R9_RESULT=PASS_INSTALLED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()

```

## installer テスト全文

```python
"""Installer guards, content reconstruction, line endings and idempotence."""
from __future__ import annotations

from pathlib import Path

import pytest

import phase171_r20r9_public_cited_double_image.install as installer


def _fixture():
    reviewed = {
        installer.R7_SOURCE: (
            "def expand_public_injected_generator_nonzero(goal):\n    return ()\n"
        ),
        installer.DOUBLE_SOURCE: "def typed_double_image_rule(goal):\n    return ()\n",
        installer.PROVIDER: "def shared_expansion_provider():\n" + installer.R8_ANCHOR,
    }
    return reviewed


def test_expected_content_only_adds_r20r8_then_r20r9() -> None:
    before = installer.expected_r20r8(_fixture())
    after = installer.patched_text(before)
    assert before[installer.R7_SOURCE] != _fixture()[installer.R7_SOURCE]
    assert after[installer.R7_SOURCE] == before[installer.R7_SOURCE]
    assert after[installer.DOUBLE_SOURCE].count(installer.R9_SOURCE_FLAG) == 1
    assert after[installer.PROVIDER].count(installer.R9_PROVIDER_FLAG) == 1
    assert installer.R9_PROVIDER_FLAG not in before[installer.PROVIDER]


def test_duplicate_or_missing_provider_anchor_rejected() -> None:
    before = installer.expected_r20r8(_fixture())
    changed = dict(before)
    changed[installer.PROVIDER] = "def shared_expansion_provider():\n"
    with pytest.raises(RuntimeError, match="anchor"):
        installer.patched_text(changed)
    changed[installer.PROVIDER] = before[installer.PROVIDER] + installer.R8_LINE
    with pytest.raises(RuntimeError, match="anchor"):
        installer.patched_text(changed)


def test_crlf_preserved() -> None:
    before = installer.expected_r20r8(_fixture())
    after = installer.patched_text(before)
    data = installer.adapt(after[installer.PROVIDER], before[installer.PROVIDER].replace("\n", "\r\n").encode("utf-8"))
    assert b"\r\n" in data
    assert installer.normalize(data) == after[installer.PROVIDER]


def test_checked_worktree_accepts_commit_transition_and_rejects_partial(monkeypatch, tmp_path: Path) -> None:
    reviewed = _fixture()
    before = installer.expected_r20r8(reviewed)
    after = installer.patched_text(before)
    for path in reviewed:
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(installer.adapt(before[path], b"\r\n"))

    def fake_git(*args):
        if args == ("branch", "--show-current"):
            return b"develop"
        if args == ("rev-parse", "HEAD"):
            return b"new-committed-head"
        if args[0] == "rev-parse":
            return installer.REVIEWED_BLOBS[Path(args[1].split(":", 1)[1])].encode("ascii")
        if args[0] == "show":
            return reviewed[Path(args[1].split(":", 1)[1])].encode("utf-8")
        raise AssertionError(args)

    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "git", fake_git)
    head, _, old, new = installer.checked_worktree()
    assert head == "new-committed-head"
    assert old == before and new == after
    # Upgrade exactly the R20R9R1 version that is present in the user worktree.
    legacy = installer.legacy_r20r9_text(before)
    assert legacy[installer.DOUBLE_SOURCE] != after[installer.DOUBLE_SOURCE]
    assert legacy[installer.PROVIDER] == after[installer.PROVIDER]
    for path in (installer.DOUBLE_SOURCE, installer.PROVIDER):
        (tmp_path / path).write_bytes(installer.adapt(legacy[path], b"\r\n"))
    installer.checked_worktree()
    previous = installer.r20r9r2_text(before)
    assert previous[installer.DOUBLE_SOURCE] != after[installer.DOUBLE_SOURCE]
    assert previous[installer.PROVIDER] == after[installer.PROVIDER]
    for path in (installer.DOUBLE_SOURCE, installer.PROVIDER):
        (tmp_path / path).write_bytes(installer.adapt(previous[path], b"\r\n"))
    installer.checked_worktree()
    for path in (installer.DOUBLE_SOURCE, installer.PROVIDER):
        (tmp_path / path).write_bytes(installer.adapt(after[path], b"\r\n"))
    installer.checked_worktree()
    (tmp_path / installer.PROVIDER).write_text(before[installer.PROVIDER], encoding="utf-8")
    with pytest.raises(RuntimeError, match="partial"):
        installer.checked_worktree()


def test_correct_dimension_guard_and_exact_legacy_upgrade() -> None:
    before = installer.expected_r20r8(_fixture())
    corrected = installer.patched_text(before)
    previous = installer.r20r9r2_text(before)
    legacy = installer.legacy_r20r9_text(before)
    assert corrected[installer.DOUBLE_SOURCE].count(installer.CORRECT_SOURCE_DIMENSION_GUARD) == 1
    assert corrected[installer.DOUBLE_SOURCE].count(installer.LEGACY_SOURCE_DIMENSION_GUARD) == 0
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R4_CITED_TARGET_GUARD) == 1
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R2_CITED_TARGET_GUARD) == 0
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R4_GENERATOR_IMAGE_BLOCK) == 1
    assert corrected[installer.DOUBLE_SOURCE].count(installer.R20R9R2_GENERATOR_IMAGE_BLOCK) == 0
    assert previous[installer.DOUBLE_SOURCE].count(installer.CORRECT_SOURCE_DIMENSION_GUARD) == 1
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R2_CITED_TARGET_GUARD) == 1
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R4_CITED_TARGET_GUARD) == 0
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R2_GENERATOR_IMAGE_BLOCK) == 1
    assert previous[installer.DOUBLE_SOURCE].count(installer.R20R9R4_GENERATOR_IMAGE_BLOCK) == 0
    assert legacy[installer.DOUBLE_SOURCE].count(installer.LEGACY_SOURCE_DIMENSION_GUARD) == 1
    assert legacy[installer.DOUBLE_SOURCE].count(installer.R20R9R2_CITED_TARGET_GUARD) == 1
    assert legacy[installer.DOUBLE_SOURCE].count(installer.CORRECT_SOURCE_DIMENSION_GUARD) == 0
    assert legacy[installer.PROVIDER] == corrected[installer.PROVIDER]
    assert previous[installer.PROVIDER] == corrected[installer.PROVIDER]

```

## public source テスト全文

```python
"""Focused public double-image proposal tests using independently established proof."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_r9_shared_math import shared_expansion_provider
from phase169_r10e5_composite_generator_image.rule import _endpoints
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r3_double_image_bridge.audit import build_double_image_proof
from phase171_r2j_r4_r3_double_image_bridge.source import (
    expand_public_cited_double_image_equality,
)
from proof import ProofRule


def _fixture():
    screened, target, _ = _screened_context()
    root, _, report = build_double_image_proof()
    assert root.rule is ProofRule.INFERENCE
    assert report["new_given_added"] == 0
    available = tuple(
        link.step.conclusion for link in screened.proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    )
    return target, root, available, screened


def test_public_cited_double_image_matches_existing_inference() -> None:
    target, root, available, screened = _fixture()
    candidates = expand_public_cited_double_image_equality(root.conclusion, available)
    expected = tuple(parent.conclusion for parent in root.premises)
    assert any(item.subgoals == expected and item.rule.name == root.inference_rule.name for item in candidates)
    shared = shared_expansion_provider(screened, proof_target=target)(root.conclusion)
    assert any(item.subgoals == expected and item.rule.name == root.inference_rule.name for item in shared)


def test_public_cited_double_image_missing_sources_fail_closed() -> None:
    _, root, available, _ = _fixture()
    assert expand_public_cited_double_image_equality(root.conclusion, ()) == ()
    without_double = tuple(item for item in available if getattr(item, "lhs", None) != root.conclusion.lhs)
    assert expand_public_cited_double_image_equality(root.conclusion, without_double) == ()
    with pytest.raises(TypeError, match="screened"):
        expand_public_cited_double_image_equality(root.conclusion, [])


def test_public_cited_double_image_rejects_wrong_goal() -> None:
    _, root, available, _ = _fixture()
    assert expand_public_cited_double_image_equality(root.conclusion.lhs, available) == ()
    assert expand_public_cited_double_image_equality(
        replace(root.conclusion, lhs=root.conclusion.rhs), available,
    ) == ()


def test_public_cited_double_image_checks_suspension_domain() -> None:
    _, root, available, _ = _fixture()
    lhs_endpoint = _endpoints(root.conclusion.lhs.expression)
    source_endpoint = _endpoints(root.conclusion.rhs.expression)
    assert lhs_endpoint == (6, 3)
    assert source_endpoint == (5, 2)
    assert source_endpoint == (lhs_endpoint[0] - 1, lhs_endpoint[1] - 1)
    proposals = expand_public_cited_double_image_equality(root.conclusion, available)
    assert any(
        proposal.subgoals == tuple(p.conclusion for p in root.premises)
        for proposal in proposals
    )

def test_public_cited_double_uses_target_generator_not_suspension_input() -> None:
    _, root, available, _ = _fixture()
    source_double = root.premises[0].conclusion
    inferred_image = root.premises[1].conclusion
    # Toda (5.3) identifies 2*nu' with the suspended *target* generator.
    # The E argument is a different element, in the source group.
    assert source_double.rhs == inferred_image.target_generator
    assert source_double.rhs != root.conclusion.rhs.expression
    assert _endpoints(source_double.rhs) == _endpoints(root.conclusion.lhs.expression)
    assert _endpoints(inferred_image.source_generator) == _endpoints(root.conclusion.rhs.expression)
    proposals = expand_public_cited_double_image_equality(root.conclusion, available)
    assert any(
        proposal.subgoals == (source_double, inferred_image)
        and proposal.rule.name == root.inference_rule.name
        for proposal in proposals
    )

```

## run.ps1 全文

```powershell
param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($DryRun) {
    python -m phase171_r20r9_public_cited_double_image.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R9 preflight failed' }
    exit 0
}
python -m phase171_r20r9_public_cited_double_image.install
if ($LASTEXITCODE -ne 0) { throw 'R20R9 install failed' }
if (-not $SkipTests) {
    # R20R8 and R20R9 both have tests/test_source.py. Collect them in
    # separate pytest processes so Python cannot conflate the modules.
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r9_public_cited_double_image/tests/test_install.py' `
        'phase171_r20r9_public_cited_double_image/tests/test_source.py' `
        'phase171_r2j_r4_r3_double_image_bridge/tests/test_audit.py::test_rule_does_not_accept_noninferred_image_or_uncited_relation_fixture'
    if ($LASTEXITCODE -ne 0) { throw 'R20R9 focused pytest: new tests and old source guard failed' }
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST_R9_AND_ORIGINAL=PASS'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r8_public_double_nonzero/tests/test_source.py'
    if ($LASTEXITCODE -ne 0) { throw 'R20R9 focused pytest: R20R8 regression failed' }
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST_R8=PASS'
    Write-Host 'PHASE171_R20R9_FOCUSED_PYTEST=PASS'
}
python -m phase171_r20r9_public_cited_double_image.audit
if ($LASTEXITCODE -ne 0) { throw 'R20R9 public route audit failed' }
git status -sb
git diff --stat

```
