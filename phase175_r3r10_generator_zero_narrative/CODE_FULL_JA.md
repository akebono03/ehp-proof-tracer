# Phase 175 R3R10R1 — 変更コード全文

このファイルには R3R10 の既存関数置換、監査・テストコードの**全文**を収録する。R3R10R1 の唯一の実装修正は `tests/test_install.py::test_crlf_file_preserves_line_endings()`。差分の省略はしない。変更対象と配置先は `AUDIT_PLAN_JA.md` を参照。

## 変更する既存関数全文 — `phase168_r3_27_typed_statement_projection.py::typed_sentence`

```python
def typed_sentence(statement, step):
    from phase174_r3_r6_r3_common_narrative.projection import (
        project_verified_index_two_statement,
    )
    index_two = project_verified_index_two_statement(statement, step)
    if index_two is not None:
        return index_two
    map_sentence = map_property_sentence(statement, step)
    if map_sentence is not None:
        return map_sentence
    # Only project the mathematical content already present in a typed claim.
    # These are shared statement formatters, not a proof-tree-specific narrative.
    from expression import Zero
    from proof import Relation, RelationType
    from phase165_r12_r2_quotient_rules import KernelMultipleStatement
    from phase174_r3_r7_r25_prop27_isolated_inference.rule import (
        Prop27TypedHopfDeltaStatement, typed_specialization,
    )
    if type(statement) is Prop27TypedHopfDeltaStatement:
        if (type(statement.n) is int and statement.n >= 2
                and statement.n % 2 == 0
                and statement == typed_specialization(statement.n)):
            sign = r"\pm" if statement.sign_undetermined else ""
            return (
                rf"$H(\Delta(\iota_{{{statement.source_iota_dimension}}}))="
                rf"{sign}{statement.absolute_coefficient}"
                rf"\iota_{{{statement.target_iota_dimension}}}$."
            )
        return None
    from map_property_rules import ImageZeroStatement
    if type(statement) is ImageZeroStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        if source is not None and target is not None and symbol is not None:
            return rf"${symbol}:{source}\to {target}$ は零写像."
        return None
    if type(statement) is KernelMultipleStatement:
        mapping = statement.map
        source = group_tex(getattr(mapping, "source_group", None))
        target = group_tex(getattr(mapping, "target_group", None))
        symbol = map_symbol_tex(mapping)
        generator = element_tex(statement.source_generator)
        if (source is not None and target is not None
                and symbol is not None and generator is not None
                and type(statement.multiple) is int
                and statement.multiple >= 1
                and statement.domain == mapping.source_group):
            return (
                rf"$\ker({symbol}:{source}\to {target})="
                rf"\mathbb{{Z}}\{{{statement.multiple}{generator}\}}$."
            )
        return None
    if (type(statement) is Relation
            and statement.relation_type is RelationType.EQUALITY
            and isinstance(statement.rhs, Zero)):
        from toda_conclusion_latex_renderer import (
            render_repository_conclusion_latex,
        )
        try:
            latex = render_repository_conclusion_latex(statement)
        except (TypeError, ValueError):
            return None
        return "$" + latex + "$."
    from toda_rules import Toda45IsomorphismStatement
    from homotopy_groups import TodaIteratedSuspensionMap
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            source = group_tex(mapping.source_group)
            target = group_tex(mapping.target_group)
            if source is not None and target is not None and type(mapping.exponent) is int:
                symbol = 'E' if mapping.exponent == 1 else rf'E^{{{mapping.exponent}}}'
                evidence = toda45_specialization_evidence(step)
                if evidence is not None:
                    _, bindings = evidence
                    values = dict(bindings)
                    return (
                        rf'$(n,m,k)=({values["n"]},{values["m"]},{values["k"]})$ '
                        rf'に適用すると, ${symbol}: {source}\to {target}$ は同型である.'
                    )
                return rf'${symbol}: {source}\to {target}$ は同型である.'
    if isinstance(statement, GeneratorImage):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        symbol = map_symbol_tex(statement.map)
        if isinstance(statement.target_generator, Zero):
            y = "0"
            if x is None:
                from expression import Composition, HomotopyElement
                from toda_human_readable_renderer import render_toda_expression_latex
                if isinstance(statement.source_generator, (Composition, HomotopyElement)):
                    try:
                        if isinstance(statement.source_generator, Composition):
                            left = render_toda_expression_latex(statement.source_generator.left)
                            right = render_toda_expression_latex(statement.source_generator.right)
                            x = left + r"\circ " + right
                        else:
                            x = render_toda_expression_latex(statement.source_generator)
                    except (TypeError, ValueError):
                        x = None
        if x is not None and y is not None and symbol is not None:
            return rf"${symbol}({x})={y}$."
    if isinstance(statement, EHPImageEqualsKernelStatement):
        window = statement.window
        if prop42_exactness_indices(TodaProp42ExactnessStatement(window)) is None:
            return None
        if window.first_map == EHP_DELTA_MAP and window.second_map == EHP_E_MAP:
            return r"完全性より, $\operatorname{Im}\Delta=\ker E$ が成り立つ."
        if window.first_map == EHP_E_MAP and window.second_map == EHP_H_MAP:
            return r"完全性より, $\operatorname{Im}E=\ker H$ が成り立つ."
    if isinstance(statement, TodaDeltaImageFreeCyclicStatement):
        if not isinstance(statement.map, TodaDeltaMap) or not isinstance(statement.image_group, FreeCyclicGroup):
            return None
        generator = element_tex(statement.image_group.generator)
        if generator is not None:
            return rf"これより, $\operatorname{{Im}}\Delta=\mathbb{{Z}}\{{{generator}\}}$."
    if isinstance(statement, SuspensionKernelFreeCyclicStatement):
        if not isinstance(statement.map, TodaSuspensionMap) or not isinstance(statement.kernel_group, FreeCyclicGroup):
            return None
        generator = element_tex(statement.kernel_group.generator)
        if generator is not None:
            return rf"完全性より, $\ker E=\mathbb{{Z}}\{{{generator}\}}$."
    if isinstance(statement, QuotientIsomorphismStatement):
        if not isinstance(statement.map, TodaSuspensionMap):
            return None
        domain, codomain = group_tex(statement.domain), group_tex(statement.codomain)
        generator = element_tex(statement.source_generator)
        if domain is not None and codomain is not None and generator is not None and type(statement.multiple) is int:
            multiple = statement.multiple
            return rf"全射性と核の決定から, 準同型定理より ${codomain}\cong {domain}/\mathbb{{Z}}\{{{multiple}{generator}\}}$."
    if isinstance(statement, GeneratorSuspension) and isinstance(statement.map, TodaSuspensionMap):
        x, y = element_tex(statement.source_generator), element_tex(statement.target_generator)
        if x is not None and y is not None:
            return rf"$E({x})={y}$."
    return None
```

## 新規インストーラー — `install.py`

```python
"""Guarded function-level installation of the Phase 175 R3R10 display fix."""
from __future__ import annotations

import ast
from dataclasses import dataclass
import os
from pathlib import Path
import tempfile

PACKAGE = Path(__file__).resolve().parent
TARGET_RELATIVE = Path("phase168_r3_27_typed_statement_projection.py")
BASE_FILE = PACKAGE / "full_functions" / "typed_sentence_BASE.py"
REPLACEMENT_FILE = PACKAGE / "full_functions" / "typed_sentence_FULL.py"
PINNED_HEAD_BLOB = "9ce32b5db34a3981649b9b9f2c5ff897eb8de831"


@dataclass(frozen=True)
class PatchPlan:
    status: str
    old_bytes: bytes
    new_bytes: bytes
    expected_function: str
    replacement_function: str


def _function_span(content: str, function_name: str) -> tuple[int, int]:
    """Use Python syntax to identify an entire, top-level function safely."""
    tree = ast.parse(content)
    matches = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name == function_name
    ]
    if len(matches) != 1:
        raise RuntimeError("R3R10_TYPED_SENTENCE_FUNCTION_NOT_UNIQUE")
    node = matches[0]
    if node.decorator_list:
        raise RuntimeError("R3R10_UNEXPECTED_FUNCTION_DECORATOR")
    return node.lineno - 1, node.end_lineno


def _normalized_function(content: str) -> str:
    """Normalize line endings, not source code or import semantics."""
    normalized = content.replace("\r\n", "\n")
    first, last = _function_span(normalized, "typed_sentence")
    return "".join(normalized.splitlines(keepends=True)[first:last]).rstrip("\n") + "\n"


def plan_patch(root: Path) -> PatchPlan:
    target = Path(root) / TARGET_RELATIVE
    if not target.is_file():
        raise RuntimeError("R3R10_TARGET_FILE_MISSING")
    original = target.read_bytes()
    if original.startswith(b"\xef\xbb\xbf"):
        raise RuntimeError("R3R10_UNEXPECTED_UTF8_BOM")
    original_text = original.decode("utf-8")
    baseline = _normalized_function(BASE_FILE.read_text(encoding="utf-8"))
    replacement = _normalized_function(REPLACEMENT_FILE.read_text(encoding="utf-8"))
    observed = _normalized_function(original_text)
    if observed == replacement:
        return PatchPlan("ALREADY_APPLIED", original, original, baseline, replacement)
    if observed != baseline:
        raise RuntimeError("R3R10_CURRENT_TYPED_SENTENCE_DIFFERS_FROM_REVIEWED_BASELINE")
    lines = original_text.splitlines(keepends=True)
    first, last = _function_span(original_text, "typed_sentence")
    eol = "\r\n" if b"\r\n" in original else "\n"
    output = "".join(lines[:first]) + replacement.replace("\n", eol) + "".join(lines[last:])
    return PatchPlan("PATCH_REQUIRED", original, output.encode("utf-8"), baseline, replacement)


def apply_patch(root: Path, plan: PatchPlan) -> None:
    """Install one reviewed function while preserving all other source bytes."""
    target = Path(root) / TARGET_RELATIVE
    if target.read_bytes() != plan.old_bytes:
        raise RuntimeError("R3R10_TARGET_CHANGED_AFTER_PREFLIGHT")
    if plan.status == "ALREADY_APPLIED":
        return
    if plan.status != "PATCH_REQUIRED":
        raise RuntimeError("R3R10_UNSUPPORTED_PATCH_STATUS")
    with tempfile.NamedTemporaryFile(
        mode="wb", dir=target.parent, prefix=".r3r10_", delete=False,
    ) as stream:
        staged = Path(stream.name)
        stream.write(plan.new_bytes)
    try:
        os.replace(staged, target)
    finally:
        if staged.exists():
            staged.unlink()
    if _normalized_function(target.read_text(encoding="utf-8")) != plan.replacement_function:
        raise RuntimeError("R3R10_POST_INSTALL_FUNCTION_MISMATCH")
```

## 新規監査 — `audit.py`

```python
"""R3R10 read-only preflight and guarded, display-only integration gate."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import traceback

from phase175_r3r10_generator_zero_narrative import install

GATE = "PASS_R3R10_LEMMA57_ZERO_GENERATOR_NARRATIVE_VISIBLE"
TEST_PATHS = (
    "phase175_r3r10_generator_zero_narrative/tests/test_projection.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_install.py",
    "phase175_r3r10_generator_zero_narrative/tests/test_public.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_public_search.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_rule.py",
    "phase175_r3r9_lemma57_explicit_public/tests/test_route.py",
    "phase175_r3r8r1_verified_prior_public/tests/test_verified_prior.py",
)


def _command(root: Path, *argv: str, timeout: int = 300) -> subprocess.CompletedProcess:
    return subprocess.run(
        argv, cwd=root, capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=timeout, check=False,
    )


def _check_git(root: Path) -> dict[str, str]:
    if not (root / ".git").exists():
        raise RuntimeError("R3R10_REPOSITORY_ROOT_REQUIRED")
    commands = {
        "branch": ("git", "branch", "--show-current"),
        "head": ("git", "rev-parse", "HEAD"),
        "blob": ("git", "rev-parse", "HEAD:" + install.TARGET_RELATIVE.as_posix()),
        "target_status": ("git", "status", "--porcelain", "--", install.TARGET_RELATIVE.as_posix()),
    }
    values = {}
    for key, command in commands.items():
        result = _command(root, *command)
        if result.returncode:
            raise RuntimeError("R3R10_GIT_PREFLIGHT_FAILED: " + key)
        values[key] = result.stdout.strip()
    if values["branch"] != "develop":
        raise RuntimeError("R3R10_DEVELOP_BRANCH_REQUIRED")
    if values["blob"] != install.PINNED_HEAD_BLOB:
        raise RuntimeError("R3R10_REVIEWED_SOURCE_BLOB_CHANGED")
    if not (root / "phase175_r3r9_lemma57_explicit_public" / "route.py").is_file():
        raise RuntimeError("R3R10_R3R9_SOURCE_REQUIRED")
    return values


def _audit_public_result() -> dict[str, object]:
    from phase175_r1_k4_audit.audit import inspect_one_group
    from phase175_r3r9_lemma57_explicit_public.audit import verify_public_result

    data = inspect_one_group(3, 4)
    certificate = verify_public_result(data)
    source_numbers = {
        ref["number"] for ref in data["references"]
        if ref.get("locator") == "Lemma 5.7"
    }
    if len(source_numbers) != 1:
        raise RuntimeError("R3R10_LEMMA57_CITATION_NOT_UNIQUE")
    source_number = next(iter(source_numbers))
    markdown = data.get("markdown")
    if not isinstance(markdown, str):
        raise RuntimeError("R3R10_MODEL_NARRATIVE_MISSING")
    body = markdown.split("\n証明\n", 1)[-1]
    formula = re.compile(
        r"\[R" + str(source_number) + r"\]より,\s*"
        r"\$E\(\\eta_\{?2\}?[^$]*\\nu[^$]*\)=0\$\."
    )
    match = formula.search(body)
    if match is None:
        raise RuntimeError("R3R10_EXPLICIT_LEMMA57_SENTENCE_MISSING")
    zero_map = re.search(r"\$E:\\pi_\{6\}\^\{2\}\\to\s*\\pi_\{7\}\^\{3\}\$ は零写像", body)
    if zero_map is None:
        raise RuntimeError("R3R10_ZERO_MAP_NARRATIVE_MISSING")
    if match.end() >= zero_map.start():
        raise RuntimeError("R3R10_LEMMA57_SENTENCE_NOT_BEFORE_ZERO_MAP")
    web_lines = data.get("web_lines")
    if not isinstance(web_lines, list) or not any(
        "E(" in str(line.get("math")) and "=0" in str(line.get("math"))
        for line in web_lines
    ):
        raise RuntimeError("R3R10_WEB_GENERATOR_ZERO_LINE_MISSING")
    return {
        "search_status": certificate["search_status"],
        "web": certificate["web"],
        "trust": data.get("trust_verified"),
        "lemma57_reference": f"[R{source_number}]",
        "display_line": match.group(0),
        "reference_count": data.get("reference_count"),
        "lemma54_used": certificate["lemma54_used"],
    }


def run(root: Path, dry_run: bool, timeout_seconds: int) -> int:
    root = Path(root).resolve()
    values = _check_git(root)
    plan = install.plan_patch(root)
    target = root / install.TARGET_RELATIVE
    if plan.status == "PATCH_REQUIRED" and values["target_status"]:
        raise RuntimeError("R3R10_PREEXISTING_TARGET_MODIFICATION_REFUSED")
    print("PHASE175_R3R10_BRANCH=" + values["branch"])
    print("PHASE175_R3R10_HEAD=" + values["head"])
    print("PHASE175_R3R10_REVIEWED_BLOB=" + values["blob"])
    print("PHASE175_R3R10_PATCH_STATUS=" + plan.status)
    print("PHASE175_R3R10_NEW_GIVEN=0")
    print("PHASE175_R3R10_NEW_MATHEMATICAL_RULES=0")
    if dry_run:
        print("PHASE175_R3R10_GATE=PASS_R3R10_READ_ONLY_DRYRUN")
        return 0

    base = Path(os.environ.get("LOCALAPPDATA") or tempfile.gettempdir())
    folder = base / "EHPProofTracerAudit" / "phase175_r3r10_generator_zero_narrative"
    folder.mkdir(parents=True, exist_ok=True)
    backup = folder / "phase168_r3_27_before_r3r10.py"
    if plan.status == "PATCH_REQUIRED":
        backup.write_bytes(plan.old_bytes)
    try:
        install.apply_patch(root, plan)
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        command = (
            sys.executable, "-B", "-m", "pytest", "-q", "--disable-warnings",
            "-p", "no:cacheprovider", "-o", "addopts=", "--import-mode=importlib",
            *TEST_PATHS,
        )
        test_result = subprocess.run(
            command, cwd=root, capture_output=True, text=True,
            encoding="utf-8", errors="replace", env=env, timeout=timeout_seconds,
            check=False,
        )
        (folder / "focused_pytest.txt").write_text(
            test_result.stdout + "\n" + test_result.stderr, encoding="utf-8",
        )
        print(test_result.stdout[-3000:])
        if test_result.returncode:
            raise RuntimeError("R3R10_FOCUSED_PYTEST_FAILED")
        print("PHASE175_R3R10_FOCUSED_PYTEST=PASS")
        public = _audit_public_result()
        report = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "gate": GATE,
            "git_head": values["head"],
            "original_sha256": hashlib.sha256(plan.old_bytes).hexdigest(),
            "installed_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "public": public,
        }
        (folder / "report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8",
        )
        for key, value in public.items():
            print(f"PHASE175_R3R10_{key.upper()}={value}")
        print("PHASE175_R3R10_GATE=" + GATE)
        return 0
    except Exception:
        if plan.status == "PATCH_REQUIRED":
            if target.read_bytes() == plan.new_bytes:
                target.write_bytes(plan.old_bytes)
                print("PHASE175_R3R10_ROLLBACK=RESTORED")
            else:
                print("PHASE175_R3R10_ROLLBACK=MANUAL_INSPECTION_REQUIRED")
        raise


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    args = parser.parse_args()
    try:
        return run(args.root, args.dry_run, args.timeout_seconds)
    except Exception:
        traceback.print_exc()
        print("PHASE175_R3R10_GATE=FAIL")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規テスト — `tests/test_projection.py`

```python
"""R3R10 shared projection tests: only verified typed content is verbalized."""
from __future__ import annotations

from expression import Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase168_r3_27_typed_statement_projection import typed_sentence
from proof import ProofRule, ProofStep


def _registered_zero_image() -> GeneratorImage:
    prior = exact_prior_database_result(2, 4)
    assert prior is not None
    return GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(6, 2), TodaPrimaryGroup(7, 3)),
        prior.rhs.generator,
        Zero(),
    )


def test_registered_composite_generator_zero_is_visible() -> None:
    image = _registered_zero_image()
    step = ProofStep(image, (), ProofRule.INFERENCE)
    rendered = typed_sentence(image, step)
    assert rendered is not None
    assert rendered.startswith(r"$E(\eta_{2}")
    assert r"\nu'" in rendered
    assert r"\circ " in rendered
    assert rendered.endswith("=0$.")


def test_non_expression_zero_generator_does_not_get_invented_text() -> None:
    image = _registered_zero_image()
    malformed = GeneratorImage(image.map, "NOT_A_TYPED_EXPRESSION", Zero())
    step = ProofStep(malformed, (), ProofRule.INFERENCE)
    assert typed_sentence(malformed, step) is None


def test_nonzero_unsupported_generator_is_not_reinterpreted_as_zero() -> None:
    image = _registered_zero_image()
    changed = GeneratorImage(image.map, image.source_generator, "not-zero")
    step = ProofStep(changed, (), ProofRule.INFERENCE)
    assert typed_sentence(changed, step) is None
```

## R3R10R1 修正テスト — `tests/test_install.py`（必要な import と関数全文）

```python
"""Dry-run planning, complete function replacement, and fail-closed guards."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r3r10_generator_zero_narrative import install


def _fixture_root(tmp_path: Path) -> Path:
    path = tmp_path / install.TARGET_RELATIVE
    path.write_text(
        'from __future__ import annotations\n\n'
        + install.BASE_FILE.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    return tmp_path


def test_plan_dry_run_does_not_write_and_full_function_replaces(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    target = root / install.TARGET_RELATIVE
    initial = target.read_bytes()
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    assert target.read_bytes() == initial
    install.apply_patch(root, plan)
    assert target.read_bytes() != initial
    assert install.plan_patch(root).status == "ALREADY_APPLIED"
    assert install._normalized_function(target.read_text(encoding="utf-8")) == plan.replacement_function


def test_unknown_function_version_fails_closed(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    target = root / install.TARGET_RELATIVE
    target.write_text(target.read_text(encoding="utf-8").replace(
        '    return None\n', '    return "unreviewed"\n', 1,
    ), encoding="utf-8")
    with pytest.raises(RuntimeError, match="CURRENT_TYPED_SENTENCE_DIFFERS"):
        install.plan_patch(root)


def test_crlf_file_preserves_line_endings(tmp_path: Path) -> None:
    root = _fixture_root(tmp_path)
    target = root / install.TARGET_RELATIVE
    # Path.write_text() may already have produced CRLF on Windows.
    normalized = target.read_bytes().replace(b"\r\n", b"\n")
    target.write_bytes(normalized.replace(b"\n", b"\r\n"))
    assert b"\r\r\n" not in target.read_bytes()
    plan = install.plan_patch(root)
    assert plan.status == "PATCH_REQUIRED"
    install.apply_patch(root, plan)
    result = target.read_bytes()
    assert b"\r\n" in result
    assert b"\r\r\n" not in result
    assert result.count(b"\n") == result.count(b"\r\n")
```

## 新規テスト — `tests/test_public.py`

```python
"""Actual public Group query must show the cited generator image before zero map."""
from __future__ import annotations

from phase175_r3r10_generator_zero_narrative.audit import _audit_public_result


def test_pi73_public_narrative_explicit_lemma57_generator_zero() -> None:
    observed = _audit_public_result()
    assert observed["search_status"] == "complete"
    assert observed["web"] == "generic-complete-proof"
    assert observed["trust"] is True
    assert observed["lemma54_used"] is False
    assert "=0" in observed["display_line"]
```

## 新規実行 — `run.ps1`

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
    & python -B -m phase175_r3r10_generator_zero_narrative.audit --root $root --dry-run --timeout-seconds $TimeoutSeconds
} else {
    & python -B -m phase175_r3r10_generator_zero_narrative.audit --root $root --timeout-seconds $TimeoutSeconds
}
$code = $LASTEXITCODE
Write-Output "PHASE175_R3R10_EXIT_CODE=$code"
exit $code
```
