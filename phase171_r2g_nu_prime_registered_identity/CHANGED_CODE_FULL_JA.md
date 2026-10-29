# Phase 171 R2G — 変更コード全文

## 変更対象

- 既存ファイル `phase168_r2_8_3_generator_identity/identity.py` の `_factor_identity()` 関数全体を置換する。
- `import` は変更しない。その他の既存関数・クラス・テストは変更しない。
- 新規追加ファイルは `phase171_r2g_nu_prime_registered_identity/` 以下。追加位置はリポジトリ直下の新規ディレクトリである。
- GitHub `develop`（確認時 HEAD `f6f765cf1828ad10a451cd557d85413e2911ba08`）のコード・関連テスト・`HyoujiGen.csv` を確認。対象ファイル Git blob SHA は `b6e097848ff5dd93ab23eeb724250a21423222bb`。

## 既存 `identity.py` import 全文（変更なし）

```python
from __future__ import annotations

import csv
from pathlib import Path

from expression import Composition, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
```

## `_factor_identity()` 置換後の関数全文

```python
def _factor_identity(expression, records):
    suspensions = 0
    while isinstance(expression, (Suspension, IteratedSuspension)):
        if isinstance(expression, Suspension):
            suspensions += 1
        elif type(expression.exponent) is int and expression.exponent >= 0:
            suspensions += expression.exponent
        else:
            return None
        expression = expression.expression
    if not isinstance(expression, HomotopyElement):
        return None
    if type(expression.dimension) is not int or expression.generator is None:
        return None
    symbol = expression.generator
    family = symbol.family
    index = symbol.index
    decoration = symbol.decoration
    actual_dimension = expression.dimension + suspensions
    matches = []
    for identifier, record in records.items():
        if identifier not in (2, 3, 4):
            continue
        base_n, stem = int(record["n"]), int(record["k"])
        if identifier == 2:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        elif identifier == 4:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        else:
            is_symbol = (
                (family == record["latex"] and index is None and decoration is None)
                or (family == "ν" and index == base_n and decoration in ("′", "'"))
                or (
                    family == "ν"
                    and index is None
                    and decoration in ("′", "'")
                    and identifier == 3
                    and base_n == 3
                    and stem == 3
                    and record.get("kinds") == "1"
                    and record["latex"] == r"\nu'"
                    and record["display"] in ("ν'", "ν′")
                )
            )
            if expression.dimension != base_n:
                continue
        if not is_symbol:
            continue
        if expression.source is not None and expression.source != expression.dimension + stem:
            continue
        if expression.target is not None and expression.target != expression.dimension:
            continue
        matches.append((identifier, actual_dimension, actual_dimension + stem, actual_dimension))
    return matches[0] if len(matches) == 1 else None
```

## 新規 `__init__.py` 全文

```python
"""Phase 171 R2G: source-registered nu-prime generator identity only."""
```

## 新規 `install.py` 全文

```python
"""Safely patch only the reviewed nu-prime branch of _factor_identity."""
from __future__ import annotations

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parent
RELATIVE = "phase168_r2_8_3_generator_identity/identity.py"
TARGET = ROOT / RELATIVE
EXPECTED_HEAD_BLOB = "b6e097848ff5dd93ab23eeb724250a21423222bb"

ORIGINAL_FUNCTION = '''def _factor_identity(expression, records):
    suspensions = 0
    while isinstance(expression, (Suspension, IteratedSuspension)):
        if isinstance(expression, Suspension):
            suspensions += 1
        elif type(expression.exponent) is int and expression.exponent >= 0:
            suspensions += expression.exponent
        else:
            return None
        expression = expression.expression
    if not isinstance(expression, HomotopyElement):
        return None
    if type(expression.dimension) is not int or expression.generator is None:
        return None
    symbol = expression.generator
    family = symbol.family
    index = symbol.index
    decoration = symbol.decoration
    actual_dimension = expression.dimension + suspensions
    matches = []
    for identifier, record in records.items():
        if identifier not in (2, 3, 4):
            continue
        base_n, stem = int(record["n"]), int(record["k"])
        if identifier == 2:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        elif identifier == 4:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        else:
            is_symbol = ((family == record["latex"] and index is None and decoration is None)
                         or (family == "ν" and index == base_n and decoration in ("′", "'")))
            if expression.dimension != base_n:
                continue
        if not is_symbol:
            continue
        if expression.source is not None and expression.source != expression.dimension + stem:
            continue
        if expression.target is not None and expression.target != expression.dimension:
            continue
        matches.append((identifier, actual_dimension, actual_dimension + stem, actual_dimension))
    return matches[0] if len(matches) == 1 else None'''

REPLACEMENT_FUNCTION = r'''def _factor_identity(expression, records):
    suspensions = 0
    while isinstance(expression, (Suspension, IteratedSuspension)):
        if isinstance(expression, Suspension):
            suspensions += 1
        elif type(expression.exponent) is int and expression.exponent >= 0:
            suspensions += expression.exponent
        else:
            return None
        expression = expression.expression
    if not isinstance(expression, HomotopyElement):
        return None
    if type(expression.dimension) is not int or expression.generator is None:
        return None
    symbol = expression.generator
    family = symbol.family
    index = symbol.index
    decoration = symbol.decoration
    actual_dimension = expression.dimension + suspensions
    matches = []
    for identifier, record in records.items():
        if identifier not in (2, 3, 4):
            continue
        base_n, stem = int(record["n"]), int(record["k"])
        if identifier == 2:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        elif identifier == 4:
            is_symbol = family == record["display"] and index == expression.dimension and decoration is None
            if expression.dimension < base_n:
                continue
        else:
            is_symbol = (
                (family == record["latex"] and index is None and decoration is None)
                or (family == "ν" and index == base_n and decoration in ("′", "'"))
                or (
                    family == "ν"
                    and index is None
                    and decoration in ("′", "'")
                    and identifier == 3
                    and base_n == 3
                    and stem == 3
                    and record.get("kinds") == "1"
                    and record["latex"] == r"\nu'"
                    and record["display"] in ("ν'", "ν′")
                )
            )
            if expression.dimension != base_n:
                continue
        if not is_symbol:
            continue
        if expression.source is not None and expression.source != expression.dimension + stem:
            continue
        if expression.target is not None and expression.target != expression.dimension:
            continue
        matches.append((identifier, actual_dimension, actual_dimension + stem, actual_dimension))
    return matches[0] if len(matches) == 1 else None'''


def _git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ("git",) + arguments, cwd=ROOT, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=check,
    )


def _source_function(text: str) -> str:
    tree = ast.parse(text)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                 and node.name == "_factor_identity"]
    if len(functions) != 1:
        raise RuntimeError("_factor_identity must exist exactly once")
    node = functions[0]
    lines = text.splitlines(keepends=True)
    return "".join(lines[node.lineno - 1:node.end_lineno]).rstrip("\r\n")


def proposed_bytes(source: bytes) -> tuple[str, bytes]:
    if source.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("unexpected UTF-8 BOM: refusing replacement")
    text = source.decode("utf-8")
    if "\r\n" in text and "\n" in text.replace("\r\n", ""):
        raise RuntimeError("mixed newlines: refusing replacement")
    existing = _source_function(text.replace("\r\n", "\n"))
    if existing == REPLACEMENT_FUNCTION:
        return "ALREADY_PATCHED", source
    if existing != ORIGINAL_FUNCTION:
        raise RuntimeError("_factor_identity differs from reviewed source")
    normalized = text.replace("\r\n", "\n")
    if normalized.count(ORIGINAL_FUNCTION) != 1:
        raise RuntimeError("reviewed function is not unique")
    new_text = normalized.replace(ORIGINAL_FUNCTION, REPLACEMENT_FUNCTION, 1)
    if "\r\n" in text:
        new_text = new_text.replace("\n", "\r\n")
    ast.parse(new_text)
    return "NEEDS_PATCH", new_text.encode("utf-8")


def preflight() -> tuple[str, bytes, bytes]:
    branch = _git("branch", "--show-current").stdout.decode("utf-8").strip()
    if branch != "develop":
        raise RuntimeError("expected develop branch, got " + branch)
    original = TARGET.read_bytes()
    state, updated = proposed_bytes(original)
    if state == "NEEDS_PATCH":
        baseline = _git("rev-parse", "HEAD:" + RELATIVE).stdout.decode("ascii").strip()
        if baseline != EXPECTED_HEAD_BLOB:
            raise RuntimeError("unreviewed committed identity.py: " + baseline)
        if _git("diff", "--quiet", "HEAD", "--", RELATIVE, check=False).returncode != 0:
            raise RuntimeError("identity.py has local tracked changes; refusing overwrite")
    return state, original, updated


def _atomic_write(destination: Path, payload: bytes) -> None:
    fd, temporary = tempfile.mkstemp(prefix=".r2g_", dir=str(destination.parent))
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, destination)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "apply"))
    args = parser.parse_args()
    try:
        state, original, updated = preflight()
        print("PHASE171_R2G_PREFLIGHT=" + state, flush=True)
        if args.action == "check":
            print("PHASE171_R2G_RESULT=PASS_CHECK", flush=True)
            return 0
        if state == "ALREADY_PATCHED":
            print("PHASE171_R2G_RESULT=PASS_ALREADY_PATCHED", flush=True)
            return 0
        base = Path(os.environ.get("LOCALAPPDATA") or str(Path.home())) / "EHPProofTracerRecovery"
        directory = base / ("phase171_r2g_" + datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f"))
        directory.mkdir(parents=True, exist_ok=False)
        backup = directory / "identity.py.before"
        backup.write_bytes(original)
        (directory / "state.json").write_text(json.dumps({
            "target": RELATIVE,
            "original_sha256": hashlib.sha256(original).hexdigest(),
            "patched_sha256": hashlib.sha256(updated).hexdigest(),
            "reviewed_git_blob": EXPECTED_HEAD_BLOB,
        }, ensure_ascii=False, indent=2), encoding="utf-8")
        _atomic_write(TARGET, updated)
        print("PHASE171_R2G_BACKUP=" + str(directory), flush=True)
        print("PHASE171_R2G_PATCHED=" + RELATIVE, flush=True)
        print("PHASE171_R2G_RESULT=PASS_APPLY", flush=True)
        return 0
    except Exception as exc:
        print("PHASE171_R2G_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 `audit.py` 全文

```python
"""Verify only the registered nu-prime presentation identity, not a group proof."""
from __future__ import annotations

import json
import sys

from expression import Multiple
from homotopy_groups import FiniteCyclicGroup
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3c_publication_order import precedes_citing_assertion
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r2_8_3_generator_identity.identity import same_registered_group_presentation
from phase171_r2e_toda53_double_reference import ASSERTION_ID
from proof import ProofRule


def audit() -> int:
    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=3)
    if len(targets) != 1:
        raise RuntimeError("expected exactly one typed pi_6^3 DB goal")
    target = targets[0]
    if not isinstance(target.rhs, FiniteCyclicGroup) or target.rhs.order != 4:
        raise RuntimeError("unexpected pi_6^3 target structure")
    source_id = "shared:12:" + ASSERTION_ID
    source = bridge.registry.assertion(source_id).content
    if not isinstance(source.lhs, Multiple) or source.lhs.coefficient != 2:
        raise RuntimeError("unexpected R2E double relation")
    cited = source.lhs.expression
    db = target.rhs.generator
    if db == cited:
        raise RuntimeError("this audit expects structurally distinct generator presentations")
    if not same_registered_group_presentation(target.rhs, FiniteCyclicGroup(4, cited)):
        raise RuntimeError("R2G HyoujiGen identity mismatch")
    citing_id = resolve_specialized_goal_citing_id(bridge, target)
    if not citing_id or not precedes_citing_assertion(bridge, source_id, citing_id):
        raise RuntimeError("R2E source is not strictly prior to pi_6^3 goal")
    screened = screen_shared_proof_context(
        bridge, goal=target, citing_assertion_id=citing_id,
        explicit_publication_target=True,
    )
    matches = tuple(link for link in screened.proof_links
                    if link.assertion_id == source_id
                    and link.step is not None
                    and link.step.rule is ProofRule.GIVEN
                    and not link.step.premises
                    and link.step.conclusion == source)
    if len(matches) != 1:
        raise RuntimeError("R2E source is not exactly one screened GIVEN")
    if any(link.step is not None and link.step.conclusion == target
           for link in screened.proof_links):
        raise RuntimeError("DB goal must never become a direct proof leaf")
    result = {
        "coordinate": "pi_6^3",
        "master_id": 3,
        "raw_generator_dataclass_equal": False,
        "registered_presentation_identity": True,
        "screened_r2e_given_count": len(matches),
        "root_proof_created": False,
    }
    print("PHASE171_R2G_IDENTITY=" + json.dumps(result, ensure_ascii=False), flush=True)
    print("PHASE171_R2G_RESULT=PASS_SOURCE_IDENTITY_ONLY", flush=True)
    return 0


def main() -> int:
    try:
        return audit()
    except Exception as exc:
        print("PHASE171_R2G_AUDIT_ERROR=" + f"{type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規 `run.ps1` 全文

```powershell
param(
    [switch] $DryRun
)
$ErrorActionPreference = 'Stop'
$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
Push-Location $RepoRoot
try {
    & python -B -m phase171_r2g_nu_prime_registered_identity.install check
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_PREFLIGHT_FAILED' }
    if ($DryRun.IsPresent) {
        Write-Host 'PHASE171_R2G_RESULT=PASS_DRY_RUN'
        return
    }
    & python -B -m phase171_r2g_nu_prime_registered_identity.install apply
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_PATCH_FAILED' }
    $Tests = @(
        'phase171_r2g_nu_prime_registered_identity/tests/test_install_unit.py',
        'phase171_r2g_nu_prime_registered_identity/tests/test_identity.py',
        'phase168_r2_8_3_generator_identity/tests/test_r2_8_3_generator_identity.py',
        'phase171_r2e_toda53_double_source/tests/test_source.py'
    )
    & python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider @Tests
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_FOCUSED_PYTEST_FAILED' }
    Write-Host 'PHASE171_R2G_FOCUSED_PYTEST=PASS'
    & python -B -m phase171_r2g_nu_prime_registered_identity.audit
    if ($LASTEXITCODE -ne 0) { throw 'PHASE171_R2G_AUDIT_FAILED' }
    Write-Host 'PHASE171_R2G_RESULT=PASS'
}
finally {
    Pop-Location
}
```

## 新規 `tests/__init__.py` 全文

```python
"""Focused R2G package regressions."""
```

## 新規 `tests/test_install_unit.py` 全文

```python
"""Source-independent preflight and mathematical identity contract tests."""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import subprocess

import pytest

from phase171_r2g_nu_prime_registered_identity import install


def source_fixture(*, newline: str = "\n") -> bytes:
    source = (
        "from __future__ import annotations\n"
        "from collections import namedtuple\n\n"
        + install.ORIGINAL_FUNCTION + "\n\n"
        + "def unrelated():\n    return 42\n"
    )
    return source.replace("\n", newline).encode("utf-8")


def test_installer_changes_one_full_function_only() -> None:
    before = source_fixture()
    state, after = install.proposed_bytes(before)
    assert state == "NEEDS_PATCH"
    assert install.REPLACEMENT_FUNCTION in after.decode("utf-8")
    assert after.decode("utf-8").replace(install.REPLACEMENT_FUNCTION, install.ORIGINAL_FUNCTION) == before.decode("utf-8")
    assert after.decode("utf-8").endswith("def unrelated():\n    return 42\n")
    ast.parse(after)
    assert install.proposed_bytes(after) == ("ALREADY_PATCHED", after)


def test_installer_preserves_crlf() -> None:
    state, after = install.proposed_bytes(source_fixture(newline="\r\n"))
    assert state == "NEEDS_PATCH"
    assert b"\r\n" in after
    assert b"\n" not in after.replace(b"\r\n", b"")


def test_installer_rejects_unknown_function() -> None:
    changed = source_fixture().replace(b"if identifier == 2:", b"if identifier == 99:")
    with pytest.raises(RuntimeError, match="differs"):
        install.proposed_bytes(changed)


def test_installer_rejects_missing_and_duplicate_function() -> None:
    with pytest.raises(RuntimeError, match="exactly once"):
        install.proposed_bytes(b"def unrelated():\n    return 1\n")
    duplicate = source_fixture() + b"\n" + install.ORIGINAL_FUNCTION.encode("utf-8") + b"\n"
    with pytest.raises(RuntimeError, match="exactly once"):
        install.proposed_bytes(duplicate)


def test_installer_rejects_mixed_newlines() -> None:
    with pytest.raises(RuntimeError, match="mixed newlines"):
        install.proposed_bytes(source_fixture(newline="\r\n") + b"\n")


def test_new_alias_has_complete_source_and_can_run_with_typed_mock() -> None:
    @dataclass(frozen=True)
    class Symbol:
        family: str
        index: int | None = None
        decoration: str | None = None

    @dataclass(frozen=True)
    class HomotopyElement:
        name: str
        dimension: int
        source: int
        target: int
        generator: Symbol

    @dataclass(frozen=True)
    class Suspension:
        expression: object

    @dataclass(frozen=True)
    class IteratedSuspension:
        expression: object
        exponent: int

    namespace = {
        "HomotopyElement": HomotopyElement,
        "Suspension": Suspension,
        "IteratedSuspension": IteratedSuspension,
    }
    exec(compile(install.REPLACEMENT_FUNCTION, "<reviewed R2G function>", "exec"), namespace)
    recognized = namespace["_factor_identity"]
    records = {3: {"n": "3", "k": "3", "kinds": "1",
                   "latex": r"\nu'", "display": "ν'"}}
    r2e = HomotopyElement("ν′", 3, 6, 3, Symbol("ν", decoration="′"))
    assert recognized(r2e, records) == (3, 3, 6, 3)
    assert recognized(HomotopyElement("ν′", 3, 7, 3, r2e.generator), records) is None
    assert recognized(HomotopyElement("ν′", 3, 6, 3, Symbol("ν")), records) is None
    assert recognized(Suspension(r2e), records) == (3, 4, 7, 4)
    records[3]["latex"] = r"\nu"
    assert recognized(r2e, records) is None


def test_preflight_preserves_unrelated_local_changes_and_rejects_target_edit(monkeypatch, tmp_path: Path) -> None:
    def git(*arguments: str) -> str:
        process = subprocess.run(
            ("git",) + arguments, cwd=tmp_path, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return process.stdout.strip()

    git("init", "-q")
    git("config", "user.email", "r2g@example.invalid")
    git("config", "user.name", "R2G Test")
    git("branch", "-M", "develop")
    target = tmp_path / install.RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source_fixture())
    unrelated = tmp_path / "other_tracked.py"
    unrelated.write_text("x = 1\n", encoding="utf-8")
    git("add", "--", ".")
    git("commit", "-qm", "unit baseline")
    blob = git("rev-parse", "HEAD:" + install.RELATIVE)
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "EXPECTED_HEAD_BLOB", blob)
    unrelated.write_text("x = 2\n", encoding="utf-8")
    (tmp_path / "phase171_r2f_untracked").mkdir()
    state, original, proposed = install.preflight()
    assert state == "NEEDS_PATCH"
    assert proposed != original
    assert unrelated.read_text(encoding="utf-8") == "x = 2\n"
    target.write_bytes(original + b"\n# local edit\n")
    with pytest.raises(RuntimeError, match="local tracked changes"):
        install.preflight()


def test_preflight_rejects_unknown_committed_blob(monkeypatch, tmp_path: Path) -> None:
    def git(*arguments: str) -> str:
        process = subprocess.run(
            ("git",) + arguments, cwd=tmp_path, check=True,
            capture_output=True, text=True, encoding="utf-8",
        )
        return process.stdout.strip()

    git("init", "-q")
    git("config", "user.email", "r2g@example.invalid")
    git("config", "user.name", "R2G Test")
    git("branch", "-M", "develop")
    target = tmp_path / install.RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(source_fixture())
    git("add", "--", ".")
    git("commit", "-qm", "unit baseline")
    monkeypatch.setattr(install, "ROOT", tmp_path)
    monkeypatch.setattr(install, "TARGET", target)
    monkeypatch.setattr(install, "EXPECTED_HEAD_BLOB", "0" * 40)
    with pytest.raises(RuntimeError, match="unreviewed committed"):
        install.preflight()
```

## 新規 `tests/test_identity.py` 全文

```python
"""Focused R2G tests for registered, typed nu-prime identity."""
from __future__ import annotations

import pytest

from expression import GeneratorSymbol, HomotopyElement, IteratedSuspension, Suspension
from homotopy_groups import FiniteCyclicGroup, FreeCyclicGroup
from phase168_r2_8_3_generator_identity.identity import (
    _factor_identity,
    _master_records,
    same_registered_group_presentation,
)


def db_nu_prime() -> HomotopyElement:
    return HomotopyElement(
        "ν'", 3, 6, 3, GeneratorSymbol(r"\nu'"),
    )


def r2e_nu_prime(*, decoration: str = "′") -> HomotopyElement:
    return HomotopyElement(
        "ν′", 3, 6, 3, GeneratorSymbol("ν", decoration=decoration),
    )


def test_master_row_three_matches_reviewed_metadata() -> None:
    record = _master_records()[3]
    assert (record["n"], record["k"], record["kinds"]) == ("3", "3", "1")
    assert (record["display"], record["latex"]) == ("ν'", r"\nu'")


def test_unindexed_r2e_nu_prime_is_same_registered_id_as_db() -> None:
    db = db_nu_prime()
    r2e = r2e_nu_prime()
    assert db != r2e
    assert _factor_identity(db, _master_records()) == (3, 3, 6, 3)
    assert _factor_identity(r2e, _master_records()) == (3, 3, 6, 3)
    assert same_registered_group_presentation(FiniteCyclicGroup(4, db), FiniteCyclicGroup(4, r2e))


def test_ascii_prime_and_suspension_are_registered_equivalences() -> None:
    db = db_nu_prime()
    r2e = r2e_nu_prime(decoration="'")
    assert same_registered_group_presentation(FiniteCyclicGroup(4, db), FiniteCyclicGroup(4, r2e))
    assert same_registered_group_presentation(
        FiniteCyclicGroup(4, IteratedSuspension(db, 1)),
        FiniteCyclicGroup(4, Suspension(r2e)),
    )


@pytest.mark.parametrize("invalid", [
    HomotopyElement("ν′", 4, 7, 4, GeneratorSymbol("ν", decoration="′")),
    HomotopyElement("ν′", 3, 7, 3, GeneratorSymbol("ν", decoration="′")),
    HomotopyElement("ν′", 3, 6, 4, GeneratorSymbol("ν", decoration="′")),
    HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν")),
    HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("ν", index=5, decoration="′")),
    HomotopyElement("ν′", 3, 6, 3, GeneratorSymbol("η", decoration="′")),
])
def test_unindexed_alias_rejects_wrong_type(invalid: HomotopyElement) -> None:
    assert not same_registered_group_presentation(
        FiniteCyclicGroup(4, db_nu_prime()), FiniteCyclicGroup(4, invalid),
    )


def test_wrong_order_and_group_kind_do_not_match() -> None:
    assert not same_registered_group_presentation(
        FiniteCyclicGroup(4, db_nu_prime()),
        FiniteCyclicGroup(8, r2e_nu_prime()),
    )
    assert not same_registered_group_presentation(
        FreeCyclicGroup(db_nu_prime()),
        FiniteCyclicGroup(4, r2e_nu_prime()),
    )


def test_new_alias_rejects_changed_master_record() -> None:
    base = _master_records()
    for key, value in (("latex", r"\nu"), ("display", "ν"),
                       ("kinds", "0"), ("k", "4"), ("n", "4")):
        records = {i: record.copy() for i, record in base.items()}
        records[3][key] = value
        assert _factor_identity(r2e_nu_prime(), records) is None


def test_real_r2e_relation_matches_db_goal_without_becoming_proof() -> None:
    from phase165_r52_r9_shared_math import build_shared_typed_bridge
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    from phase171_r2e_toda53_double_reference import ASSERTION_ID
    from expression import Multiple

    bridge = build_shared_typed_bridge()
    targets = registered_group_goal_candidates(bridge, n=3, k=3)
    assert len(targets) == 1
    target = targets[0]
    source = bridge.registry.assertion("shared:12:" + ASSERTION_ID).content
    assert isinstance(source.lhs, Multiple) and source.lhs.coefficient == 2
    assert target.rhs.generator != source.lhs.expression
    assert same_registered_group_presentation(
        target.rhs, FiniteCyclicGroup(4, source.lhs.expression),
    )
    assert not any(link.step is not None and link.step.conclusion == target
                   for link in bridge.proof_links)
```

## 新規 `README.md` 全文

```markdown
# Phase 171 R2G — Registered nu-prime generator identity

This package extends the existing `HyoujiGen.csv`-backed presentation identity to recognize an unindexed, decorated `GeneratorSymbol(family="ν", index=None, decoration="′")` at the registered nu-prime ID 3. The database spelling `GeneratorSymbol(family="\\nu'")` and the earlier indexed spelling remain supported.

It modifies only the complete `_factor_identity()` function in `phase168_r2_8_3_generator_identity/identity.py`. The existing imports, API, theorem registry, proof inference rules, database, citation screening and renderer remain untouched. It does not prove a group order, cyclic structure, or a Proposition 5.6 conclusion.

The installation first verifies the `develop` branch, the known committed file blob, the exact reviewed function and the absence of local edits to the target file. It preserves unrelated uncommitted or untracked files. Before applying the patch, it writes an exact backup and metadata under `%LOCALAPPDATA%\EHPProofTracerRecovery` (or the home directory if `LOCALAPPDATA` is unset). Re-execution is safe when the reviewed patch is already present. Conflicting content is rejected rather than overwritten.

## Windows PowerShell

Extract the ZIP into the repository root, keeping all existing R2E/R2F files. Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2g_nu_prime_registered_identity\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase171_r2g_nu_prime_registered_identity\run.ps1"
```

The normal run executes only selected existing and new pytest files, then checks the real screened (5.3) source against the database's π₆³ generator ID. A raw dataclass inequality is expected; only registered presentation identity becomes true. Full pytest is deferred to the Phase 171 closeout.
```

## 新規 `監査仕様.md` 全文

```markdown
# Phase 171 R2G — 監査仕様

## 対象と目的

π₆³ の DB Goal の生成元と Toda (5.3) の ν′ の型付き表現を、`data/HyoujiGen.csv` の ID 3 に基づいて照合する。`GeneratorSymbol(family="ν", index=None, decoration="′")` という R2E で採用した表現だけが、従来の ID 3 判定から漏れていた。

## 変更対象

既存ファイル `phase168_r2_8_3_generator_identity/identity.py` の `_factor_identity()` 関数全体のみを置換する。既存 import と他の関数は変更しない。新規ディレクトリ `phase171_r2g_nu_prime_registered_identity/` に安全なインストーラー、監査、限定テスト、PowerShell 実行ファイルを追加する。

## 正当性と制限

追加の判定は ID 3、基礎次数 n=3、stem k=3、kinds=1、登録 latex `\nu'`、登録 display `ν'` と実際の元の source/target を照合する。既存の DB latex 表現、添字付き文献表現、懸垂表現の認識は保持する。異なる次数、元の型、群の位数、巡回群／自由群の種別は同一としない。

DB の群構造を GIVEN として取り込まず、Proposition 5.6 の目標を証拠としない。`ProofRule.INFERENCE` を生成・変更しない。`publication precedence` と citation screening（出典選別）も既存処理に委ねる。

## 確認する検証

新規インストーラーテストと型付き同一性テスト、既存 `phase168_r2_8_3_generator_identity/tests/test_r2_8_3_generator_identity.py`、R2E の `(5.3)` テストを限定実行する。監査では DB の生の dataclass 等価性は False のまま、登録済み同一性は True、目標を結論とする出典付き GIVEN の新規登録はないことを検証する。

## 次との境界

R2G は生成元の Presentation（表示構造）の同一性のみを解決する。π₆³ の位数 4 と生成性、Proposition 2.2 の Hopf 合成公式、EHP 短完全列の証明と `CyclicStructureStatement` の導出は R2H 以降の仕事とする。Phase 171 全体 pytest は Phase 終了時にのみ実行する。
```

## 変更一覧・限定 pytest・完了条件・次 Phase との境界

R2G では既存 ID 3 の Presentation 同一性判定のみ拡張する。数学的な出典 GIVEN、Proposition 5.6、ProofRule、DB、publication precedence の変更はない。

`run.ps1` は新規のインストーラー・型付き同一性テスト、既存 Phase 168 ID 照合テスト、R2E 出典テストの4ファイルに限定して pytest を実行する。全体 pytest は実行しない。

完了条件は (5.3) の `2ν′` の元と π₆³ DB Goal の生成元が HyoujiGen の同一 ID 3 に対応し、異なる次数や位数を混同せず、出典付き `GIVEN` から目標群構造を直接生成しないこと。次 R2H は Proposition 2.2 の型付き引用・推論。短完全列からの位数4・生成性・完成 Proof Tree は本 R2G では行わない。
