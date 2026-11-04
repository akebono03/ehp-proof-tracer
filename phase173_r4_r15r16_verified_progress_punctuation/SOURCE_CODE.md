# R15R16 新規ファイル・テストの全文

変更済みの既存関数については `FULL_CHANGED_UNITS.md` を参照してください. 新規・変更コードは省略していません.

## `projection_patch.py`

```python
"""Literal, fail-closed function replacements for reviewed source files."""
from __future__ import annotations

PROJECTION_OLD = 'def _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:\n    """Format only an already certified abstract structure, never identify generators."""\n    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:\n        raise ValueError("abstract result has nonconcrete group dimensions")\n    invariant_latex = abstract_invariants_latex(structure.invariant_summands)\n    target_latex = rf"\\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"\n    return (\n        "## 証明済みの抽象群構造\\n\\n"\n        + rf"${target_latex} \\cong {invariant_latex}$."\n        + "\\n\\n"\n        + "これは出典検査済みの抽象群 ProofStep による結論であり、"\n        + "登録済みの先行 DB 群を前提とする。"\n        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"\n    )\n'
PROJECTION_NEW = 'def _verified_abstract_progress_lines(\n    structure: CertifiedAbstractStructure,\n) -> tuple[str, ...]:\n    """Present actual certified premises, without adopting named-generator goals.\n\n    The certificate\'s original typed inference guard has already checked its\n    four premises. Their registered source metadata is used only for display.\n    No new proof step, citation identity, or mathematical conclusion is made.\n    """\n    from web_group_proof_common import _group_proof_statement_latex\n\n    root = structure.proof_step\n    if len(root.premises) != 4:\n        raise ValueError("verified abstract inference requires four premises")\n    theorem_step, first_prior, second_prior, hopf_step = root.premises\n\n    def source_label(step: object) -> str | None:\n        rule = getattr(step, "inference_rule", None)\n        reference = getattr(rule, "literature_reference", None)\n        if reference is None:\n            return None\n        label = reference.locator or reference.label\n        return label if isinstance(label, str) and label.strip() else None\n\n    def verified_math(step: object) -> str | None:\n        try:\n            latex, fallback = _group_proof_statement_latex(step.conclusion)\n        except (TypeError, ValueError):\n            return None\n        return f"${latex}$" if latex is not None and fallback is None else None\n\n    theorem_label = source_label(root)\n    theorem_description = (\n        f"{theorem_label} の適用前提となる定理を検証した."\n        if theorem_label is not None else "一般定理の前提を検証した."\n    )\n    lines = [theorem_description]\n    for prior in (first_prior, second_prior):\n        formula = verified_math(prior)\n        locator = source_label(prior)\n        if formula is not None and locator is not None:\n            lines.append(f"先行データベースの {formula} を {locator} により確認した.")\n        elif formula is not None:\n            lines.append(f"先行データベースの検証済み結果 {formula} を確認した.")\n        else:\n            lines.append("先行データベースの型付き結果を検証した.")\n\n    hopf_formula = verified_math(hopf_step)\n    hopf_locator = source_label(hopf_step)\n    if hopf_formula is not None and hopf_locator is not None:\n        lines.append(f"{hopf_locator} から {hopf_formula} を導いた.")\n    elif hopf_formula is not None:\n        lines.append(f"検証済みの Hopf 関係 {hopf_formula} を導いた.")\n    else:\n        lines.append("検証済みの Hopf 関係を前提として確認した.")\n\n    theorem_reference = theorem_label or "検証済みの一般定理"\n    lines.append(\n        f"これらの検証済み前提を使い, {theorem_reference} により"\n        "抽象群構造を導いた."\n    )\n    return tuple(lines)\n\n\ndef _render_abstract_claim(target: object, structure: CertifiedAbstractStructure) -> str:\n    """Show certified progress and the abstract claim, never named generators."""\n    if type(target.group_dimension) is not int or type(target.sphere_dimension) is not int:\n        raise ValueError("abstract result has nonconcrete group dimensions")\n    invariant_latex = abstract_invariants_latex(structure.invariant_summands)\n    target_latex = rf"\\pi_{{{target.group_dimension}}}^{{{target.sphere_dimension}}}"\n    progress = "\\n\\n".join(_verified_abstract_progress_lines(structure))\n    return (\n        "## 検証済みの途中経過\\n\\n"\n        + progress\n        + "\\n\\n"\n        + "## 証明済みの抽象群構造\\n\\n"\n        + rf"${target_latex} \\cong {invariant_latex}$."\n        + "\\n\\n"\n        + "これは出典検査済みの抽象群 ProofStep による結論であり、"\n        + "登録済みの先行 DB 群を前提とする。"\n        + "記名生成元の対応は未証明であり、上記の未解決 Goal と探索状態は変わらない。"\n    )\n'
LAYOUT_OLD = '    result = "\\n".join(normalized)\n    return result.rstrip("\\n") + ("\\n" if markdown.endswith("\\n") else "")\n'
LAYOUT_NEW = '    normalized = _normalize_narrative_punctuation(normalized)\n    result = "\\n".join(normalized)\n    return result.rstrip("\\n") + ("\\n" if markdown.endswith("\\n") else "")\n'
LAYOUT_APPEND = '\n\ndef _normalize_narrative_punctuation(lines: list[str]) -> list[str]:\n    """Apply uniform prose punctuation to the common Web narrative layout.\n\n    Math and inline-code spans remain untouched. Numbered source locators,\n    decimal points, headings, and display math remain intact. Sentence-final\n    periods create physical line breaks, not new proof steps.\n    """\n    result: list[str] = []\n    in_display_math = False\n    in_code_fence = False\n    for line in lines:\n        stripped = line.strip()\n        if stripped.startswith("```"):\n            in_code_fence = not in_code_fence\n            result.append(line)\n            continue\n        if stripped == r"\\[":\n            in_display_math = True\n            result.append(line)\n            continue\n        if stripped == r"\\]":\n            in_display_math = False\n            result.append(line)\n            continue\n        if (in_code_fence or in_display_math\n                or stripped.startswith(("# ", "## ", "### "))):\n            result.append(line)\n            continue\n\n        chunks: list[str] = []\n        current: list[str] = []\n        in_inline_math = False\n        in_inline_code = False\n        for index, raw in enumerate(line):\n            if raw == "$" and not in_inline_code and (index == 0 or line[index - 1] != "\\\\"):\n                in_inline_math = not in_inline_math\n            elif raw == "`" and not in_inline_math and (index == 0 or line[index - 1] != "\\\\"):\n                in_inline_code = not in_inline_code\n\n            protected = in_inline_math or in_inline_code or raw in ("$", "`")\n            character = raw\n            if not protected and raw in ("、", "，"):\n                character = "," if (index + 1 < len(line) and line[index + 1].isspace()) else ", "\n            elif not protected and raw == "。":\n                character = "."\n            current.append(character)\n\n            if protected or character != ".":\n                continue\n            remaining = line[index + 1:]\n            next_word = remaining.lstrip()\n            if not next_word:\n                continue\n            # The dot in 4.4, 0.5, or an enumerated item is not a full stop.\n            if raw == "." and remaining[0].isdigit():\n                continue\n            if raw == "." and "".join(current[:-1]).strip().isdigit():\n                continue\n            next_char = next_word[0]\n            is_japanese = (\n                "\\u3040" <= next_char <= "\\u30ff"\n                or "\\u3400" <= next_char <= "\\u9fff"\n            )\n            sentence_boundary = raw == "。" or is_japanese or (\n                remaining[0].isspace()\n                and (next_char.isupper() or next_char in "（[「")\n            )\n            if sentence_boundary:\n                chunks.append("".join(current).rstrip())\n                current = []\n        final = "".join(current).strip()\n        if final:\n            chunks.append(final)\n        if chunks:\n            result.extend(chunks)\n        else:\n            result.append("")\n    return result\n'


def replace_verified(text: str, old: str, new: str, *, label: str) -> str:
    if text.count(old) != 1:
        raise RuntimeError("reviewed function boundary mismatch: " + label)
    return text.replace(old, new, 1)


def patch_projection(text: str) -> str:
    return replace_verified(text, PROJECTION_OLD, PROJECTION_NEW, label="abstract projection")


def patch_layout(text: str) -> str:
    result = replace_verified(text, LAYOUT_OLD, LAYOUT_NEW, label="shared layout")
    if "def _normalize_narrative_punctuation" in result:
        raise RuntimeError("duplicate common punctuation helper")
    return result.rstrip("\n") + LAYOUT_APPEND


TRANSFORMERS = {
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py": patch_projection,
    "phase173_r4_r15r13_unified_presentation/layout.py": patch_layout,
}
```

## `install.py`

```python
"""Source-guarded installation of the Phase 173 R15R16 presentation patch."""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess

from .projection_patch import TRANSFORMERS

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = Path(__file__).resolve().parent
BACKUP = PACKAGE / "backups"
STATE = PACKAGE / "installed_state.json"
REVIEWED_HEAD = "92f967c079f4a66e19a598e0acc54b742f11df9c"
REVIEWED_BLOBS = {
    "phase173_r4_r15r9_shared_abstract_renderer/projection.py":
        "55eadbd3deb6a7ca54f78d1fe3c470053196840d",
    "phase173_r4_r15r13_unified_presentation/layout.py":
        "05d2b3a0353c0ff1251f65dcd53d902c9ffbb140",
}


def _command(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], cwd=ROOT, capture_output=True,
        text=True, encoding="utf-8", errors="replace", check=False,
    )


def _git(*arguments: str) -> str:
    completed = _command(*arguments)
    if completed.returncode != 0:
        raise RuntimeError("git command failed: " + " ".join(arguments)
                           + ": " + completed.stderr.strip()[:400])
    return completed.stdout.strip()


def _guard() -> str:
    branch = _git("branch", "--show-current")
    head = _git("rev-parse", "HEAD")
    remote = _git("rev-parse", "origin/develop")
    if branch != "develop" or head != remote:
        raise RuntimeError("develop local/remote HEAD mismatch")
    ancestry = _command("merge-base", "--is-ancestor", REVIEWED_HEAD, "HEAD")
    if ancestry.returncode != 0:
        raise RuntimeError("current HEAD is not descended from reviewed R15R15")
    if _git("diff", "--cached", "--name-only"):
        raise RuntimeError("staged changes require inspection")
    for name, expected in REVIEWED_BLOBS.items():
        if _git("rev-parse", "HEAD:" + name) != expected:
            raise RuntimeError("reviewed GitHub source blob changed: " + name)
        if not (ROOT / name).is_file():
            raise RuntimeError("reviewed source file missing: " + name)
    local_changes = set(filter(None, _git("diff", "--name-only").splitlines()))
    unexpected = local_changes.difference(TRANSFORMERS)
    if unexpected:
        raise RuntimeError("unreviewed tracked changes: " + ", ".join(sorted(unexpected)))
    print("R15R16_BRANCH=" + branch, flush=True)
    print("R15R16_LOCAL_HEAD=" + head, flush=True)
    print("R15R16_REMOTE_HEAD=" + remote, flush=True)
    print("R15R16_REVIEWED_ANCESTOR=" + REVIEWED_HEAD, flush=True)
    print("R15R16_SOURCE_GUARD=PASS", flush=True)
    return head


def _target_bytes(original: bytes, name: str) -> bytes:
    normalized = original.decode("utf-8").replace("\r\n", "\n")
    transformed = TRANSFORMERS[name](normalized)
    compile(transformed, name, "exec")
    if b"\r\n" in original:
        transformed = transformed.replace("\n", "\r\n")
    return transformed.encode("utf-8")


def _read_previous(state: dict, name: str) -> bytes:
    entry = state["files"][name]
    previous = (BACKUP / entry["backup"]).read_bytes()
    if sha256(previous).hexdigest() != entry["original_sha256"]:
        raise RuntimeError("backup checksum mismatch: " + name)
    return previous


def _preflight() -> tuple[dict[str, bytes], dict[str, bytes], str]:
    head = _guard()
    installed = STATE.is_file()
    if BACKUP.exists() and not installed:
        raise RuntimeError("orphan R15R16 backups require inspection")
    state = json.loads(STATE.read_text(encoding="utf-8")) if installed else None
    if state is not None and state["head"] != head:
        raise RuntimeError("HEAD changed after installation: inspect before proceeding")
    original: dict[str, bytes] = {}
    expected: dict[str, bytes] = {}
    for name in TRANSFORMERS:
        current = (ROOT / name).read_bytes()
        previous = _read_previous(state, name) if state is not None else current
        result = _target_bytes(previous, name)
        if state is not None:
            if sha256(result).hexdigest() != state["files"][name]["target_sha256"]:
                raise RuntimeError("patched content changed: " + name)
            if current != result:
                raise RuntimeError("installed file locally altered: " + name)
        else:
            changed = _git("diff", "--", name)
            if changed:
                raise RuntimeError("file locally altered: " + name)
        original[name] = previous
        expected[name] = result
    return original, expected, head


def dry_run() -> None:
    _preflight()
    print("R15R16_DRY_RUN=PASS", flush=True)
    print("R15R16_PRODUCTION_EDIT=NONE", flush=True)


def install() -> None:
    original, target, head = _preflight()
    if STATE.exists():
        print("R15R16_ALREADY_INSTALLED=True", flush=True)
        return
    BACKUP.mkdir(exist_ok=False)
    state = {"head": head, "files": {}}
    try:
        for index, (name, data) in enumerate(original.items()):
            filename = f"source_{index}.backup"
            (BACKUP / filename).write_bytes(data)
            state["files"][name] = {
                "backup": filename,
                "original_sha256": sha256(data).hexdigest(),
                "target_sha256": sha256(target[name]).hexdigest(),
            }
        STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        for name, data in target.items():
            location = ROOT / name
            temporary = location.with_name(location.name + ".r15r16.tmp")
            temporary.write_bytes(data)
            os.replace(temporary, location)
    except BaseException:
        if STATE.exists():
            restore()
        else:
            for path in BACKUP.iterdir():
                path.unlink()
            BACKUP.rmdir()
        raise
    print("R15R16_INSTALLED=True", flush=True)
    print("R15R16_FULL_PYTEST_RUN=False", flush=True)


def restore() -> None:
    if not STATE.is_file():
        raise RuntimeError("installation state missing")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    if _git("rev-parse", "HEAD") != state["head"]:
        raise RuntimeError("HEAD changed after installation; restore refused")
    original = {}
    for name, entry in state["files"].items():
        previous = _read_previous(state, name)
        current_hash = sha256((ROOT / name).read_bytes()).hexdigest()
        if current_hash not in (entry["original_sha256"], entry["target_sha256"]):
            raise RuntimeError("unexpected post-install local change: " + name)
        original[name] = previous
    for name, data in original.items():
        (ROOT / name).write_bytes(data)
    STATE.unlink()
    for entry in state["files"].values():
        (BACKUP / entry["backup"]).unlink()
    BACKUP.rmdir()
    print("R15R16_RESTORED=True", flush=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--install", action="store_true")
    group.add_argument("--restore", action="store_true")
    args = parser.parse_args()
    try:
        if args.restore:
            restore()
        elif args.install:
            install()
        else:
            dry_run()
        return 0
    except (RuntimeError, TypeError, ValueError, OSError, UnicodeError,
            KeyError, SyntaxError) as exc:
        print("R15R16_ERROR=" + type(exc).__name__ + ": " + str(exc), flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

## `run.ps1`

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $Root
try {
    git fetch origin develop
    if ($LASTEXITCODE -ne 0) { throw 'GitHub fetch failed' }

    python -m phase173_r4_r15r16_verified_progress_punctuation.install --dry-run
    if ($LASTEXITCODE -ne 0) { throw 'R15R16 source guard failed' }

    python -m pytest -q -p no:cacheprovider `
        phase173_r4_r15r16_verified_progress_punctuation/tests/test_preview.py
    if ($LASTEXITCODE -ne 0) { throw 'R15R16 pure preview tests failed' }

    if ($DryRun) {
        Write-Output 'R15R16_DRY_RUN=PASS'
        Write-Output 'R15R16_PHASE_COMPLETED=False'
        exit 0
    }

    python -m phase173_r4_r15r16_verified_progress_punctuation.install --install
    if ($LASTEXITCODE -ne 0) { throw 'R15R16 installation failed' }
    try {
        python -m pytest -q -p no:cacheprovider `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_preview.py `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_contract.py `
            phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py `
            phase173_r4_r15r15_abstract_result_banner/tests/test_integration.py `
            phase173_r4_r15r14_common_partial_presentation/tests/test_integration.py `
            phase173_r4_r15r13_unified_presentation/tests/test_integration.py `
            phase173_r4_r15r11_model_abstract_integration/tests/test_integration.py `
            phase173_r4_r15r12_reference_correction/tests/test_integration.py
        if ($LASTEXITCODE -ne 0) { throw 'Focused pytest failed' }
        Write-Output 'R15R16_FOCUSED_PYTEST=PASS'
        Write-Output 'R15R16_FULL_PYTEST_RUN=False'
        Write-Output 'R15R16_PHASE_COMPLETED=False'
    } catch {
        python -m phase173_r4_r15r16_verified_progress_punctuation.install --restore
        if ($LASTEXITCODE -ne 0) { throw 'R15R16 rollback requires manual inspection' }
        throw
    }
} finally {
    Pop-Location
}
```

## `tests/test_preview.py`

```python
"""Pure DryRun previews of reviewed presentation changes, no repository edits."""
from __future__ import annotations

import pytest

from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    LAYOUT_APPEND,
    LAYOUT_OLD,
    PROJECTION_NEW,
    PROJECTION_OLD,
    patch_layout,
    patch_projection,
)


def test_projection_patch_is_single_replacement() -> None:
    proposed = patch_projection(PROJECTION_OLD)
    assert proposed.count("def _verified_abstract_progress_lines(") == 1
    assert proposed.count("def _render_abstract_claim(") == 1
    assert "## 検証済みの途中経過" in proposed
    assert "## 証明済みの抽象群構造" in proposed
    compile(proposed, "reviewed-projection.py", "exec")


def test_layout_patch_has_one_shared_formatter() -> None:
    proposed = patch_layout(LAYOUT_OLD)
    assert proposed.count("def _normalize_narrative_punctuation(") == 1
    assert proposed.count("_normalize_narrative_punctuation(normalized)") == 1
    compile("def example(markdown, normalized):\n" + LAYOUT_OLD, "preview.py", "exec")


def test_prose_punctuation_preview_and_math_protection() -> None:
    namespace: dict[str, object] = {}
    exec(compile(LAYOUT_APPEND, "reviewed-punctuation.py", "exec"), namespace)
    normalize = namespace["_normalize_narrative_punctuation"]
    result = normalize([
        "確認した。次に、証明する。",
        "**[R1] Proposition 4.4.**",
        r"$H(\nu_4)=\iota_7$ と $\pi_{12}^{4}$ を使う。",
    ])
    assert result[0] == "確認した."
    assert result[1] == "次に, 証明する."
    assert result[2] == "**[R1] Proposition 4.4.**"
    assert r"$H(\nu_4)=\iota_7$" in result[3]


def test_conflicting_source_is_rejected() -> None:
    with pytest.raises(RuntimeError):
        patch_layout("unrelated text")
    with pytest.raises(RuntimeError):
        patch_projection("unrelated text")
    assert "No new proof step" in PROJECTION_NEW
```

## `tests/test_contract.py`

```python
"""Tests of R15R16 shared prose layout and pure patch invariants."""
from __future__ import annotations

import pytest

from phase173_r4_r15r13_unified_presentation.layout import (
    _normalize_narrative_punctuation,
    canonicalize_proof_layout,
)
from phase173_r4_r15r16_verified_progress_punctuation.projection_patch import (
    patch_layout,
    patch_projection,
    PROJECTION_OLD,
    LAYOUT_OLD,
)


def test_actual_prose_periods_are_line_breaks() -> None:
    markdown = (
        "使用する結果\n\n**[R1] Proposition 4.4.**\n\n"
        "証明\n\nこれは確認済みである。続いて、定理を使う.次の結論を得た.\n"
    )
    converted = canonicalize_proof_layout(markdown)
    assert "## 使用する結果" in converted
    assert "Proposition 4.4." in converted
    assert "これは確認済みである.\n続いて, 定理を使う.\n次の結論を得た." in converted
    assert converted.count("\n---\n") == 1


def test_math_code_and_numbered_source_are_not_changed() -> None:
    converted = _normalize_narrative_punctuation([
        r"$H(\nu_4)=\iota_7$ と $\pi_{12}^4$ を示す。次へ進む.",
        "**[R1] Proposition 4.4.**",
        r"\[",
        r"\pi_{12}^{4}=\mathbb{Z}/2",
        r"\]",
        "`x.3` を用い、0.5 の関係を確認した。",
    ])
    assert converted[0] == r"$H(\nu_4)=\iota_7$ と $\pi_{12}^4$ を示す."
    assert converted[1] == "次へ進む."
    assert "**[R1] Proposition 4.4.**" in converted
    assert r"\pi_{12}^{4}=\mathbb{Z}/2" in converted
    assert "`x.3` を用い, 0.5 の関係を確認した." in converted


def test_no_status_or_group_names_required_for_punctuation() -> None:
    first = canonicalize_proof_layout("使用する結果\n\n証明\n\n結果である。結論を示す。\n")
    second = canonicalize_proof_layout("使用する結果\n\n証明\n\n検証した。未解決である。\n")
    assert "結果である.\n結論を示す." in first
    assert "検証した.\n未解決である." in second


def test_source_mismatch_is_rejected() -> None:
    with pytest.raises(RuntimeError, match="reviewed function boundary mismatch"):
        patch_projection("unrelated source")
    with pytest.raises(RuntimeError, match="reviewed function boundary mismatch"):
        patch_layout("unrelated source")
    assert patch_projection(PROJECTION_OLD).count("## 検証済みの途中経過") == 1
    assert "_normalize_narrative_punctuation(normalized)" in patch_layout(LAYOUT_OLD)
```

## `tests/test_integration.py`

```python
"""Real certified partial proofs display their checked intermediate premises."""
from __future__ import annotations

import pytest

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r15r9_shared_abstract_renderer.projection import (
    render_certified_abstract_model_section,
    render_certified_abstract_section,
)
from web_group_proof import build_standard_web_group_proof_view


@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_abstract_certificate_displays_actual_verified_milestones(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert result.abstract_structure.proof_step not in result.proven_steps
    assert len(result.abstract_structure.proof_step.premises) == 4

    model = build_proof_narrative_model(result)
    progress = render_certified_abstract_model_section(model)
    assert progress == render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in progress
    assert "Proposition 4.4" in progress
    assert "Lemma 5.4" in progress
    assert progress.count("先行データベースの ") == 2
    assert "sphere.csv" in progress
    assert "## 証明済みの抽象群構造" in progress
    assert "記名生成元の対応は未証明" in progress
    assert progress in render_model_backed_narrative_markdown(result, model)

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    assert view.key == "generic-partial-proof"
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("検証済みの途中経過") == 1
    assert headings.count("証明済みの抽象群構造") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(
        seg.value for line in view.rendered_lines for seg in line.segments
    )
    assert "sphere.csv" in shown and "Lemma 5.4" in shown
    assert "Relation(lhs=" not in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals


def test_completed_view_has_no_abstract_progress_sidecar() -> None:
    view = build_standard_web_group_proof_view(
        n=4, k=4, mode="narrative", citation_source="model",
    )
    assert view.key == "generic-complete-proof"
    assert not view.partial_result
    assert not view.abstract_structure_certified
    assert not any(
        line.kind == "heading" and line.prefix == "検証済みの途中経過"
        for line in view.rendered_lines
    )
    assert not any(
        "、" in seg.value or "。" in seg.value
        for line in view.rendered_lines for seg in line.segments
    )


def test_legacy_and_model_paths_share_abstract_progress() -> None:
    goal = exact_prior_database_result(4, 8)
    assert goal is not None
    views = (
        build_standard_web_group_proof_view(
            n=4, k=8, goal=goal, mode="narrative", citation_source=source,
        )
        for source in ("model", "legacy")
    )
    for view in views:
        assert view.key == "generic-partial-proof"
        assert any(
            line.kind == "heading" and line.prefix == "検証済みの途中経過"
            for line in view.rendered_lines
        )
```

## `__init__.py`

```python
"""Phase 173 R15R16 presentation patch."""
```

## `tests/__init__.py`

```python
"""Focused R15R16 tests."""
```
