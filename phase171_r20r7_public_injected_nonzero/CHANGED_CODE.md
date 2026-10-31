# Phase 171 R20R7R1 — 修正版のコード全文

## 最初に変更対象を列挙

R20R7R1 自体は既存の本番ファイルを変更しない。修正済み配布パッケージ内で、以下を変更する。

1. `phase171_r20r7_public_injected_nonzero/install.py`：定数 `REVIEWED_R20R6_COMMITTED_BLOBS` を追加（既存の `REVIEWED_HEAD_BLOBS` の直後）。既存関数 `checked_worktree()` 全体を置換。既存 import は変更なし（以下に全文収録）。
2. `phase171_r20r7_public_injected_nonzero/tests/test_install.py`：`Path` とモジュール import を追加し、模擬 Git ワークツリーの検証用関数と4つのテストを末尾に追加。import・全テスト関数の全文を以下に収録。

R20R7 本実行時に変更される本番ファイルは、従来と同じ2つだけ。

- `phase171_r2j_r4_r7_nonzero_nu_order/source.py`：新関数 `expand_public_injected_generator_nonzero()` をファイル末尾、R20R6 追加関数の後に追加。既存 import 変更なし。既存クラス・関数変更なし。
- `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` 内で R20R6 の呼出し直後に新関数の import と呼出しを追加。既存ファイル import 変更なし。既存クラス変更なし。

本修正では数学的な推論規則、Citation（引用資格）、Web 出力には触れない。

## インストーラ `install.py` 全文（import・関数を省略せず収録）

```python
"""Guarded R20R7 installer: connect only the prior-cyclic/E-injective nonzero rule."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
SOURCE = Path("phase171_r2j_r4_r7_nonzero_nu_order/source.py")
PROVIDER = Path("phase165_r52_r9_shared_math.py")
REVIEWED_HEAD_BLOBS = {
    SOURCE: "5b95010681f6257dc46a4236c099445281635e53",
    PROVIDER: "10d3303e6b3a52246f1cfb8a8998f3a67be0b0ac",
}
# The exact R20R6 worktree was subsequently committed to develop.
# Both pairs are reviewed. Never accept a mixed pair of these versions.
REVIEWED_R20R6_COMMITTED_BLOBS = {
    SOURCE: "340b66a90118a0760cd94eadaf192ad69f3c48b7",
    PROVIDER: "c3a25c075f1dfa4573ce3feb1c07f653b0aa649a",
}
R20R6_SOURCE_ADDITION = (PACKAGE / "r20r6_reviewed_source_addition.py.txt").read_text(encoding="utf-8")
SOURCE_ADDITION = (PACKAGE / "source_addition.py.txt").read_text(encoding="utf-8")
R20R6_ANCHOR = "        options.extend(expand_cited_full_order_cyclic_structure(goal, tuple(available)))\n"
R20R6_REPLACEMENT = (
    R20R6_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_order_four_from_nonzero_double,\n"
    + "        )\n"
    + "        options.extend(expand_public_order_four_from_nonzero_double(goal))\n"
)
R20R7_ANCHOR = "        options.extend(expand_public_order_four_from_nonzero_double(goal))\n"
R20R7_REPLACEMENT = (
    R20R7_ANCHOR
    + "        from phase171_r2j_r4_r7_nonzero_nu_order.source import (\n"
    + "            expand_public_injected_generator_nonzero,\n"
    + "        )\n"
    + "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))\n"
)
SOURCE_FLAG = "def expand_public_injected_generator_nonzero("
PROVIDER_FLAG = "        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))"


def git_read(*arguments: str) -> bytes:
    """Allow only branch, HEAD, and reviewed committed-file reads."""
    if arguments in {("branch", "--show-current"), ("rev-parse", "HEAD")}:
        pass
    elif len(arguments) == 2 and arguments[0] == "rev-parse" and arguments[1].startswith("HEAD:"):
        if arguments[1][5:] not in {SOURCE.as_posix(), PROVIDER.as_posix()}:
            raise ValueError("unreviewed committed file")
    elif len(arguments) == 2 and arguments[0] == "show" and arguments[1].startswith("HEAD:"):
        if arguments[1][5:] not in {SOURCE.as_posix(), PROVIDER.as_posix()}:
            raise ValueError("unreviewed committed file")
    else:
        raise ValueError("unapproved Git command")
    result = subprocess.run(
        ["git", *arguments], cwd=ROOT, check=True, capture_output=True,
    )
    return result.stdout if arguments[0] == "show" else result.stdout.strip()


def normalize(data: bytes) -> str:
    """Use LF in memory while retaining each working file's line endings."""
    return data.decode("utf-8").replace("\r\n", "\n")


def adapt(text: str, original: bytes) -> bytes:
    """Restore the original newline convention when writing full files."""
    return text.replace("\n", "\r\n").encode("utf-8") if b"\r\n" in original else text.encode("utf-8")


def expected_r20r6(source: str, provider: str) -> tuple[str, str]:
    """Reconstruct the reviewed R20R6-only working state from Git HEAD."""
    if source.count("def inferred_order_four_rule(") != 1:
        raise RuntimeError("reviewed mathematical order-four rule was changed")
    if provider.count(R20R6_ANCHOR) != 1:
        raise RuntimeError("reviewed R20R6 provider insertion anchor absent")
    return (
        source.rstrip("\n") + "\n\n" + R20R6_SOURCE_ADDITION.lstrip("\n"),
        provider.replace(R20R6_ANCHOR, R20R6_REPLACEMENT, 1),
    )


def patched_text(source: str, provider: str) -> tuple[str, str]:
    """Append only R20R7, with no modification to existing inference rules."""
    if source.count("def expand_public_order_four_from_nonzero_double(") != 1:
        raise RuntimeError("R20R6 order-four source function is absent or duplicated")
    if provider.count(R20R7_ANCHOR) != 1:
        raise RuntimeError("R20R6 order-four provider call is absent or duplicated")
    source_exists = SOURCE_FLAG in source
    provider_exists = PROVIDER_FLAG in provider
    if source_exists != provider_exists:
        raise RuntimeError("partial R20R7 installation; no files changed")
    if source_exists:
        if source.count(SOURCE_FLAG) != 1 or provider.count(PROVIDER_FLAG) != 1:
            raise RuntimeError("duplicate R20R7 definitions")
        return source, provider
    return (
        source.rstrip("\n") + "\n\n" + SOURCE_ADDITION.lstrip("\n"),
        provider.replace(R20R7_ANCHOR, R20R7_REPLACEMENT, 1),
    )


def checked_worktree() -> tuple[str, dict[Path, bytes], dict[Path, str], dict[Path, str]]:
    """Accept either reviewed R20R6 baseline, rejecting mixed versions or edits.

    The earlier R20R6 patch was originally uncommitted, then committed as
    exactly the Git blobs listed in REVIEWED_R20R6_COMMITTED_BLOBS. The
    mathematical source is identical; only the HEAD file identities differ.
    """
    branch = git_read("branch", "--show-current").decode("utf-8")
    if branch != "develop":
        raise RuntimeError("develop branch required")
    head = git_read("rev-parse", "HEAD").decode("utf-8")
    committed: dict[Path, str] = {}
    original: dict[Path, bytes] = {}
    blobs: dict[Path, str] = {}
    for path, earlier_blob in REVIEWED_HEAD_BLOBS.items():
        blob = git_read("rev-parse", "HEAD:" + path.as_posix()).decode("ascii")
        if blob not in (earlier_blob, REVIEWED_R20R6_COMMITTED_BLOBS[path]):
            raise RuntimeError("reviewed committed source drift: " + str(path) + " actual=" + blob)
        blobs[path] = blob
        committed[path] = normalize(git_read("show", "HEAD:" + path.as_posix()))
        original[path] = (ROOT / path).read_bytes()
    if all(blobs[path] == REVIEWED_HEAD_BLOBS[path] for path in (SOURCE, PROVIDER)):
        r20r6_source, r20r6_provider = expected_r20r6(
            committed[SOURCE], committed[PROVIDER],
        )
    elif all(
        blobs[path] == REVIEWED_R20R6_COMMITTED_BLOBS[path]
        for path in (SOURCE, PROVIDER)
    ):
        r20r6_source, r20r6_provider = committed[SOURCE], committed[PROVIDER]
    else:
        raise RuntimeError("mixed R20R6 committed versions; no files changed")
    r20r7_source, r20r7_provider = patched_text(r20r6_source, r20r6_provider)
    valid_states = {
        SOURCE: {r20r6_source, r20r7_source},
        PROVIDER: {r20r6_provider, r20r7_provider},
    }
    for path in (SOURCE, PROVIDER):
        if normalize(original[path]) not in valid_states[path]:
            raise RuntimeError("unexpected local edits in " + str(path))
    source_done = normalize(original[SOURCE]) == r20r7_source
    provider_done = normalize(original[PROVIDER]) == r20r7_provider
    if source_done != provider_done:
        raise RuntimeError("partial R20R7 installation")
    return head, original, {SOURCE: r20r6_source, PROVIDER: r20r6_provider}, {SOURCE: r20r7_source, PROVIDER: r20r7_provider}


def run_install(*, dry_run: bool) -> None:
    """Install safely, back up full originals and emit full modified functions."""
    head, original, before, after = checked_worktree()
    print("PHASE171_R20R7_HEAD=" + head, flush=True)
    print("PHASE171_R20R7_SOURCE_CONTENT_GUARD=PASS", flush=True)
    already = all(normalize(original[path]) == after[path] for path in (SOURCE, PROVIDER))
    if dry_run:
        print("PHASE171_R20R7_DRY_RUN=PASS", flush=True)
        print("PHASE171_R20R7_ALREADY_INSTALLED=" + str(already), flush=True)
        return
    if not already:
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
        backup = PACKAGE / "output" / ("backup_" + stamp)
        backup.mkdir(parents=True, exist_ok=False)
        for path in (SOURCE, PROVIDER):
            (backup / path.name).write_bytes(original[path])
        try:
            for path in (SOURCE, PROVIDER):
                (ROOT / path).write_bytes(adapt(after[path], original[path]))
        except Exception:
            for path in (SOURCE, PROVIDER):
                (ROOT / path).write_bytes(original[path])
            raise
        print("PHASE171_R20R7_BACKUP=" + str(backup), flush=True)
    checked_worktree()
    out = PACKAGE / "output"
    out.mkdir(exist_ok=True)
    complete_source = normalize((ROOT / SOURCE).read_bytes())
    complete_provider = normalize((ROOT / PROVIDER).read_bytes())
    begin = complete_provider.index("def shared_expansion_provider(")
    end = complete_provider.index("\ndef search_shared_group_goal(", begin)
    (out / "SOURCE_FULL_AFTER.py").write_text(complete_source, encoding="utf-8")
    (out / "SHARED_PROVIDER_FUNCTION_FULL_AFTER.py").write_text(
        complete_provider[begin:end].rstrip("\n") + "\n", encoding="utf-8",
    )
    print("PHASE171_R20R7_SOURCE_CHANGES=" + ("0" if already else "2"), flush=True)
    print("PHASE171_R20R7_RESULT=PASS_INSTALLED", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_install(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
```

## インストーラ関連テスト `tests/test_install.py` 全文

```python
"""Deterministic patch and CRLF regression tests, without changing root sources."""
from __future__ import annotations

from pathlib import Path

import pytest

import phase171_r20r7_public_injected_nonzero.install as installer
from phase171_r20r7_public_injected_nonzero.install import (
    PROVIDER_FLAG,
    R20R6_ANCHOR,
    R20R7_ANCHOR,
    SOURCE_FLAG,
    adapt,
    expected_r20r6,
    normalize,
    patched_text,
)


def _reviewed_mock():
    source = "from __future__ import annotations\n\ndef inferred_order_four_rule(goal):\n    return goal\n"
    provider = (
        "def shared_expansion_provider():\n"
        + R20R6_ANCHOR
        + "    return ()\n"
    )
    return expected_r20r6(source, provider)


def test_install_follows_exact_reviewed_r20r6_patch() -> None:
    earlier_source, earlier_provider = _reviewed_mock()
    new_source, new_provider = patched_text(earlier_source, earlier_provider)
    assert new_source.count(SOURCE_FLAG) == 1
    assert new_provider.count(PROVIDER_FLAG) == 1
    assert new_provider.count(R20R7_ANCHOR) == 1
    assert patched_text(new_source, new_provider) == (new_source, new_provider)


def test_install_rejects_half_patch_and_drift() -> None:
    earlier_source, earlier_provider = _reviewed_mock()
    new_source, new_provider = patched_text(earlier_source, earlier_provider)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(new_source, earlier_provider)
    with pytest.raises(RuntimeError, match="partial"):
        patched_text(earlier_source, new_provider)
    with pytest.raises(RuntimeError, match="provider call"):
        patched_text(earlier_source, "def shared_expansion_provider():\n    return ()\n")


def test_install_keeps_original_crlf_or_lf() -> None:
    earlier_source, earlier_provider = _reviewed_mock()
    new_source, new_provider = patched_text(earlier_source, earlier_provider)
    crlf = adapt(new_source, earlier_source.replace("\n", "\r\n").encode("utf-8"))
    assert b"\r\n" in crlf
    assert normalize(crlf) == new_source
    assert adapt(new_provider, earlier_provider.encode("utf-8")).decode("utf-8") == new_provider


def _check_mock_worktree(monkeypatch, tmp_path: Path, *, committed: bool, mixed: bool = False):
    """Simulate reviewed Git contents without touching the actual repository."""
    r20r6_source, r20r6_provider = _reviewed_mock()
    legacy_source = "from __future__ import annotations\n\ndef inferred_order_four_rule(goal):\n    return goal\n"
    legacy_provider = "def shared_expansion_provider():\n" + R20R6_ANCHOR + "    return ()\n"
    # Pre-commit HEAD contains the older sources; its worktree already has R20R6.
    files = {
        installer.SOURCE: r20r6_source if committed else legacy_source,
        installer.PROVIDER: r20r6_provider if committed else legacy_provider,
    }
    worktree = {installer.SOURCE: r20r6_source, installer.PROVIDER: r20r6_provider}
    early_ids = {installer.SOURCE: "early-source", installer.PROVIDER: "early-provider"}
    committed_ids = {installer.SOURCE: "r20r6-source", installer.PROVIDER: "r20r6-provider"}
    ids = dict(committed_ids if committed else early_ids)
    if mixed:
        ids[installer.PROVIDER] = early_ids[installer.PROVIDER] if committed else committed_ids[installer.PROVIDER]
    for path, content in files.items():
        dest = tmp_path / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        # Exact bytes that a clean worktree would contain, CRLF included.
        dest.write_bytes(worktree[path].replace("\n", "\r\n").encode("utf-8"))
    def fake_git_read(*arguments: str) -> bytes:
        if arguments == ("branch", "--show-current"):
            return b"develop"
        if arguments == ("rev-parse", "HEAD"):
            return b"test-head"
        if len(arguments) == 2 and arguments[1].startswith("HEAD:"):
            path = Path(arguments[1][5:])
            if arguments[0] == "rev-parse":
                return ids[path].encode("ascii")
            if arguments[0] == "show":
                return files[path].encode("utf-8")
        raise AssertionError("unexpected Git command: " + repr(arguments))
    monkeypatch.setattr(installer, "ROOT", tmp_path)
    monkeypatch.setattr(installer, "git_read", fake_git_read)
    monkeypatch.setattr(installer, "REVIEWED_HEAD_BLOBS", early_ids)
    monkeypatch.setattr(installer, "REVIEWED_R20R6_COMMITTED_BLOBS", committed_ids)
    return r20r6_source, r20r6_provider


def test_checked_worktree_accepts_committed_r20r6_pair(monkeypatch, tmp_path: Path) -> None:
    original_source, original_provider = _check_mock_worktree(
        monkeypatch, tmp_path, committed=True,
    )
    head, originals, before, after = installer.checked_worktree()
    assert head == "test-head"
    assert before == {
        installer.SOURCE: original_source,
        installer.PROVIDER: original_provider,
    }
    assert all(b"\r\n" in originals[path] for path in (installer.SOURCE, installer.PROVIDER))
    assert after[installer.SOURCE].count(SOURCE_FLAG) == 1
    assert after[installer.PROVIDER].count(PROVIDER_FLAG) == 1


def test_checked_worktree_accepts_precommit_r20r6_pair(monkeypatch, tmp_path: Path) -> None:
    original_source, original_provider = _check_mock_worktree(
        monkeypatch, tmp_path, committed=False,
    )
    _, _, before, after = installer.checked_worktree()
    assert before[installer.SOURCE] == original_source
    assert before[installer.PROVIDER] == original_provider
    assert after[installer.SOURCE].count(SOURCE_FLAG) == 1
    assert after[installer.PROVIDER].count(PROVIDER_FLAG) == 1


def test_checked_worktree_rejects_mixed_git_baselines(monkeypatch, tmp_path: Path) -> None:
    _check_mock_worktree(monkeypatch, tmp_path, committed=True, mixed=True)
    with pytest.raises(RuntimeError, match="mixed R20R6"):
        installer.checked_worktree()


def test_checked_worktree_rejects_unreviewed_local_edits(monkeypatch, tmp_path: Path) -> None:
    _check_mock_worktree(monkeypatch, tmp_path, committed=True)
    target = tmp_path / installer.SOURCE
    target.write_bytes(target.read_bytes() + b"\r\n# extra edit\r\n")
    with pytest.raises(RuntimeError, match="unexpected local edits"):
        installer.checked_worktree()
```

## R20R7 の新規本番関数全文（追加位置：`source.py` 末尾）

```python
def expand_public_injected_generator_nonzero(
    goal: object,
    available: tuple[object, ...],
) -> tuple[GoalExpansion, ...]:
    """Propose E(generator) != 0 from one earlier finite-cyclic source and injective E.

    The source relation is an eligible, cited GIVEN candidate, not a DB group
    target.  The E-injectivity subgoal must be independently proved as an
    INFERENCE.  No statement or ProofStep is manufactured by this proposer.
    """
    from phase165_r3_recursive_search import GoalExpansion

    if not isinstance(available, tuple):
        raise TypeError("available must be a tuple of screened source statements")
    if (
        not isinstance(goal, NonZeroGroupElement)
        or not isinstance(goal.group, TodaPrimaryGroup)
        or not isinstance(goal.element, MapApplication)
        or goal.element.map != EHP_E_MAP
    ):
        return ()
    q = goal.group.group_dimension
    n = goal.group.sphere_dimension
    if (
        type(q) is not int
        or type(n) is not int
        or n < 3
        or q <= n
    ):
        return ()
    source_group = TodaPrimaryGroup(q - 1, n - 1)
    injective = MapInjective(TodaSuspensionMap(source_group, goal.group))
    matched: list[Relation] = []
    for claim in available:
        if (
            not isinstance(claim, Relation)
            or claim.relation_type is not RelationType.EQUALITY
            or claim.lhs != source_group
            or not isinstance(claim.rhs, FiniteCyclicGroup)
            or nonzero_cyclic_generator_image(claim, injective, goal.element) != goal
        ):
            continue
        if claim not in matched:
            matched.append(claim)
    if len(matched) != 1:
        return ()
    source = matched[0]
    return (
        GoalExpansion(
            injected_generator_nonzero_rule(goal, source, injective),
            (source, injective),
        ),
    )
```

## R20R7 の `shared_expansion_provider()` 追加位置・import 部分全文

```python
        from phase171_r2j_r4_r7_nonzero_nu_order.source import (
            expand_public_order_four_from_nonzero_double,
        )
        options.extend(expand_public_order_four_from_nonzero_double(goal))
        from phase171_r2j_r4_r7_nonzero_nu_order.source import (
            expand_public_injected_generator_nonzero,
        )
        options.extend(expand_public_injected_generator_nonzero(goal, tuple(available)))
```

変更後の `shared_expansion_provider()` 関数全文は本実行時に `output/SHARED_PROVIDER_FUNCTION_FULL_AFTER.py` に必ず出力する。変更後の `source.py` 全文は `output/SOURCE_FULL_AFTER.py` に出力する。R20R6 で実装済みの全行を保持する。

## R20R7 の公開接続監査 `audit.py` 全文

```python
"""Read-only confirmation of the public E-injectivity/nonzero-generator route."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r20r7_public_injected_nonzero.install import checked_worktree
from proof import ProofRule, find_inference_matches_for_rule

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent


def audit() -> dict:
    """Compare only verified proposal semantics, not an injected completed proof."""
    head, _, _, _ = checked_worktree()
    before = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    screened, target, _ = _screened_context()
    doubled, order_four, nodes, old_report = build_nonzero_nu_order_proof()
    if (
        doubled.rule is not ProofRule.INFERENCE
        or order_four.rule is not ProofRule.INFERENCE
        or old_report["new_given_added"] != 0
        or old_report["nu_prime_order_four_proven"] is not True
        or not nodes
    ):
        raise RuntimeError("independent R4-R7 inference ancestry is invalid")
    nonzero = doubled.premises[1]
    if nonzero.rule is not ProofRule.INFERENCE or len(nonzero.premises) != 2:
        raise RuntimeError("the independently proved E-image nonzero node is missing")
    provider = shared_expansion_provider(screened, proof_target=target)
    proposed = provider(nonzero.conclusion)
    if not isinstance(proposed, tuple):
        raise RuntimeError("shared provider returned invalid options")
    matched = tuple(
        option for option in proposed
        if option.rule.name == nonzero.inference_rule.name
        and option.subgoals == tuple(parent.conclusion for parent in nonzero.premises)
    )
    certified = 0
    for option in matched:
        matches = find_inference_matches_for_rule(option.rule, nonzero.premises)
        if any(
            tuple(match.premises) == nonzero.premises
            and derive_inference_proof_step(match).conclusion == nonzero.conclusion
            for match in matches
        ):
            certified += 1
    if certified != 1:
        raise RuntimeError("a unique certified injected nonzero public proposal was not found")
    after = subprocess.run(
        ["git", "status", "--porcelain", "--untracked-files=no"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout
    if before != after:
        raise RuntimeError("tracked worktree changed during read-only audit")
    return {
        "phase": "171-R20R7",
        "mode": "READ_ONLY_PUBLIC_INJECTED_NONZERO_CONNECTION",
        "git_head": head,
        "nonzero_goal": repr(nonzero.conclusion),
        "source_and_injectivity_subgoals": [repr(x.conclusion) for x in nonzero.premises],
        "provider_options": len(proposed),
        "matching_options": len(matched),
        "certified_options": certified,
        "injected_eta_image_nonzero": "CERTIFIED_PUBLIC_PROPOSAL_PRESENT",
        "nu_order_four_rule_connected": True,
        "not_yet_connected": ["double_nonzero", "typed_double_equality"],
        "new_given_added": 0,
        "completed_proofs_imported": False,
        "public_complete_asserted": False,
        "web_verified": False,
        "tracked_worktree_unchanged": True,
        "full_pytest": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    head, _, _, _ = checked_worktree()
    print("PHASE171_R20R7_HEAD=" + head, flush=True)
    if args.dry_run:
        print("PHASE171_R20R7_DRY_RUN=PASS", flush=True)
        return
    report = audit()
    directory = PACKAGE / "output" / datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    directory.mkdir(parents=True, exist_ok=False)
    dest = directory / "audit.json"
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("PHASE171_R20R7_INJECTED_ETA_IMAGE_NONZERO=" + report["injected_eta_image_nonzero"], flush=True)
    print("PHASE171_R20R7_NU_ORDER_FOUR=RULE_CONNECTED", flush=True)
    print("PHASE171_R20R7_NOT_YET_CONNECTED=" + ",".join(report["not_yet_connected"]), flush=True)
    print("PHASE171_R20R7_NEW_GIVEN=0", flush=True)
    print("PHASE171_R20R7_PUBLIC_COMPLETE_ASSERTED=False", flush=True)
    print("PHASE171_R20R7_REPORT=" + str(dest), flush=True)
    print("PHASE171_R20R7_RESULT=PASS_IMAGE_NONZERO_CONNECTED", flush=True)


if __name__ == "__main__":
    main()
```

## R20R7 の回帰テスト `tests/test_public_injected_nonzero.py` 全文

```python
"""Only source-screened prior cyclic facts and proven injectivity may imply nonzero E."""
from __future__ import annotations

from dataclasses import replace

import pytest

from expression import Composition, GeneratorSymbol, HomotopyElement, MapApplication
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionMap
from map_facts import EHP_E_MAP
from phase164_r8_proofstep_factory import derive_inference_proof_step
from phase165_r14_r6_generic_iso import MapInjective
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase171_r2i_eta_hopf_bridge.audit import _screened_context
from phase171_r2j_r4_r7_nonzero_nu_order.audit import build_nonzero_nu_order_proof
from phase171_r2j_r4_r7_nonzero_nu_order.source import (
    NonZeroGroupElement,
    expand_public_injected_generator_nonzero,
)
from proof import ProofRule, ProofStep, Relation, RelationType, find_inference_matches_for_rule


def _eta(n: int, typed: bool) -> HomotopyElement:
    return HomotopyElement(
        name="η_" + str(n), dimension=n,
        source=n + 1 if typed else None,
        target=n if typed else None,
        generator=GeneratorSymbol(family="η", index=n),
    )


def _triple(typed: bool) -> Composition:
    return Composition(
        _eta(2, typed), Composition(_eta(3, typed), _eta(4, typed)),
    )


def _case():
    source = TodaPrimaryGroup(5, 2)
    target = TodaPrimaryGroup(6, 3)
    earlier = Relation(
        source, FiniteCyclicGroup(2, _triple(False)), RelationType.EQUALITY,
    )
    goal = NonZeroGroupElement(target, MapApplication(EHP_E_MAP, _triple(True)))
    injection = MapInjective(TodaSuspensionMap(source, target))
    return earlier, goal, injection


def test_public_nonzero_image_from_cited_group_and_injective_e() -> None:
    earlier, goal, injection = _case()
    routes = expand_public_injected_generator_nonzero(goal, (earlier,))
    assert len(routes) == 1
    assert routes[0].subgoals == (earlier, injection)
    assert routes[0].rule.name == "injective map preserves nonzero finite-cyclic generator"
    assert not any(isinstance(item, ProofStep) for item in routes[0].subgoals)
    parents = (
        ProofStep(earlier, (), ProofRule.GIVEN),
        ProofStep(injection, (), ProofRule.INFERENCE),
    )
    matching = find_inference_matches_for_rule(routes[0].rule, parents)
    assert len(matching) == 1
    assert derive_inference_proof_step(matching[0]).conclusion == goal


def test_public_nonzero_requires_cited_group_and_valid_goal() -> None:
    earlier, goal, _ = _case()
    assert expand_public_injected_generator_nonzero(goal, ()) == ()
    assert expand_public_injected_generator_nonzero("unrelated", (earlier,)) == ()
    with pytest.raises(TypeError):
        expand_public_injected_generator_nonzero(goal, [earlier])
    wrong_generator = replace(earlier, rhs=FiniteCyclicGroup(2, _eta(3, False)))
    assert expand_public_injected_generator_nonzero(goal, (wrong_generator,)) == ()
    wrong_order = replace(earlier, rhs=FiniteCyclicGroup(1, earlier.rhs.generator))
    assert expand_public_injected_generator_nonzero(goal, (wrong_order,)) == ()
    wrong_target = replace(goal, group=TodaPrimaryGroup(7, 3))
    assert expand_public_injected_generator_nonzero(wrong_target, (earlier,)) == ()
    wrong_e = replace(goal, element="not a suspension image")
    assert expand_public_injected_generator_nonzero(wrong_e, (earlier,)) == ()


def test_public_nonzero_fails_closed_on_competing_prior_presentations() -> None:
    earlier, goal, _ = _case()
    assert len(expand_public_injected_generator_nonzero(goal, (earlier, earlier))) == 1
    rival = replace(earlier, rhs=FiniteCyclicGroup(4, earlier.rhs.generator))
    assert expand_public_injected_generator_nonzero(goal, (earlier, rival)) == ()


def test_shared_provider_matches_real_r4r7_proved_parents() -> None:
    screened, target, _ = _screened_context()
    doubled, order_four, _, prior = build_nonzero_nu_order_proof()
    assert prior["new_given_added"] == 0
    assert order_four.rule is ProofRule.INFERENCE
    real = doubled.premises[1]
    assert real.rule is ProofRule.INFERENCE
    proposals = shared_expansion_provider(screened, proof_target=target)(real.conclusion)
    matches = tuple(
        candidate for candidate in proposals
        if candidate.rule.name == real.inference_rule.name
        and candidate.subgoals == tuple(item.conclusion for item in real.premises)
    )
    assert len(matches) == 1
    admissible = find_inference_matches_for_rule(matches[0].rule, real.premises)
    assert any(
        derive_inference_proof_step(item).conclusion == real.conclusion
        and item.premises == real.premises
        for item in admissible
    )
```

## 実行スクリプト `run.ps1` 全文

```powershell
param(
    [switch]$DryRun,
    [switch]$SkipTests
)
$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if ($DryRun) {
    python -m phase171_r20r7_public_injected_nonzero.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R20R7 preflight failed' }
    exit 0
}
python -m phase171_r20r7_public_injected_nonzero.install
if ($LASTEXITCODE -ne 0) { throw 'R20R7 install failed' }
if (-not $SkipTests) {
    Write-Host 'PHASE171_R20R7_FOCUSED_PYTEST_START'
    python -m pytest -q -p no:cacheprovider `
        'phase171_r20r7_public_injected_nonzero/tests/test_public_injected_nonzero.py' `
        'phase171_r20r7_public_injected_nonzero/tests/test_install.py' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_injective_nonzero_from_a_real_finite_cyclic_generator' `
        'phase171_r2j_r4_r7_nonzero_nu_order/tests/test_audit.py::test_prior_untyped_eta_composition_is_matched_by_registered_identity'
    if ($LASTEXITCODE -ne 0) { throw 'R20R7 focused pytest failed' }
    Write-Host 'PHASE171_R20R7_FOCUSED_PYTEST=PASS'
}
python -m phase171_r20r7_public_injected_nonzero.audit
if ($LASTEXITCODE -ne 0) { throw 'R20R7 public proof-route audit failed' }
git status -sb
git diff --stat
```
