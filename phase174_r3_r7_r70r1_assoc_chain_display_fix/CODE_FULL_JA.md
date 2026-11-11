# Phase 174 R70R1 — 変更コード・テスト全文

## 変更対象

| 種別 | ファイル | クラス・関数 |
|---|---|---|
| 対象の既存ファイル | `phase174_r3_r7_r70_verified_narrative_projection/projection.py` | `_project_composite_images（関数全体を置換）` |
| 新規Installer | `phase174_r3_r7_r70r1_assoc_chain_display_fix/install.py` | `replacement / source_guard / main` |
| 追加テスト | `phase174_r3_r7_r70r1_assoc_chain_display_fix/tests/test_install.py` | `既存テストを変更せず、新規9件` |

## 変更関数の全文（元の `_project_composite_images()` と置換）

```python
def _project_composite_images(lines: list[str], model, scope: frozenset[int]) -> list[str]:
    """Condense three displayed premises only for a verified composite-zero step."""
    from expression import Zero
    from phase165_r14_r6_generic_iso import GeneratorImage
    from phase168_r3_27_typed_statement_projection import typed_sentence
    from phase169_r10e5_composite_generator_image.rule import (
        component_image_obligations,
    )
    from phase174_r3_r7_r9_composition_associativity.rule import (
        RULE_NAME as ASSOCIATIVITY_RULE_NAME,
        generator_image_associativity_inputs,
    )
    from phase174_r3_r7_r7_composite_zero_audit.rule import (
        RULE_NAME, composite_zero_generator_inputs,
    )
    from proof import ProofRule
    from toda_proof_narrative_renderer import render_toda_expression_latex

    output = list(lines)
    for index in sorted(scope):
        zero_step = model.steps[index]
        zero_goal = zero_step.conclusion
        if (zero_step.rule is not ProofRule.INFERENCE
                or getattr(zero_step.inference_rule, "name", None) != RULE_NAME
                or not isinstance(zero_goal, GeneratorImage)
                or not isinstance(zero_goal.target_generator, Zero)
                or len(zero_step.premises) != 2):
            continue
        image_step, annihilator_step = zero_step.premises
        if (image_step.rule is not ProofRule.INFERENCE
                or annihilator_step.rule is not ProofRule.INFERENCE
                or _step_index(model, image_step, scope) is None
                or _step_index(model, annihilator_step, scope) is None
                or composite_zero_generator_inputs(
                    zero_goal, image_step.conclusion
                ) != (image_step.conclusion, annihilator_step.conclusion)):
            continue
        # A verified image may first be rebracketed by the generic
        # associativity rule. Trace that one certified INFERENCE edge before
        # checking the existing two-component suspension rule. R9 changes
        # parentheses, not the image, generator, or source citations.
        component_image_step = image_step
        if len(image_step.premises) == 1:
            right_step = image_step.premises[0]
            expected_right = generator_image_associativity_inputs(
                image_step.conclusion,
            )
            if (image_step.inference_rule is None
                    or image_step.inference_rule.name != ASSOCIATIVITY_RULE_NAME
                    or right_step.rule is not ProofRule.INFERENCE
                    or _step_index(model, right_step, scope) is None
                    or expected_right != (right_step.conclusion,)):
                continue
            component_image_step = right_step
        requirements = component_image_obligations(
            component_image_step.conclusion,
        )
        if (requirements is None
                or len(component_image_step.premises) != 2):
            continue
        component_steps = component_image_step.premises
        if (any(parent.rule is not ProofRule.INFERENCE
                or _step_index(model, parent, scope) is None
                for parent in component_steps)
                or tuple(parent.conclusion for parent in component_steps) != requirements):
            continue
        tags = _given_ancestor_tags(model, annihilator_step, scope)
        if len(tags) != 1:
            continue
        component_sentences = tuple(typed_sentence(parent.conclusion, parent)
                                    for parent in component_steps)
        annihilator_sentence = typed_sentence(annihilator_step.conclusion, annihilator_step)
        if (any(not isinstance(item, str) for item in component_sentences)
                or not isinstance(annihilator_sentence, str)):
            continue
        indices = tuple(_body_index(output, item) for item in component_sentences)
        related = _body_index(output, annihilator_sentence,
                              prefix=f"[R{tags[0]}]より, ")
        if (related is None or any(i is None for i in indices)
                or len(set(indices + (related,))) != 3):
            continue
        positions = sorted(indices + (related,))
        if (positions[0] != indices[0] or positions[1] != indices[1]
                or positions[2] != related
                or any(output[i] for i in range(positions[0], positions[2] + 1)
                       if i not in positions)):
            continue
        try:
            generator = render_toda_expression_latex(zero_goal.source_generator)
            composite = render_toda_expression_latex(image_step.conclusion.target_generator)
        except (TypeError, ValueError):
            continue
        if not generator or not composite or "\\" not in generator or "\\" not in composite:
            continue
        combined = (f"懸垂と合成の関係および [R{tags[0]}]より, "
                    f"$E({generator})={composite}=0$.")
        suffix = output[positions[2] + 1:]
        while suffix and suffix[0] == "":
            suffix.pop(0)
        output = output[:positions[0]] + [combined, ""] + suffix
    return output
```

## 新規 `install.py` の全文（新規ディレクトリ直下）

```python
"""R70R1: replace only the reviewed existing complete composite-display function.

The source guard accepts full-file LF or CRLF, not mixed or CR-only data.
No mathematical rule, existing text formatter or reference mapping is changed.
"""
from __future__ import annotations

import argparse
import ast
from hashlib import sha1
from pathlib import Path
import subprocess


PACKAGE = "phase174_r3_r7_r70r1_assoc_chain_display_fix"
TARGET = "phase174_r3_r7_r70_verified_narrative_projection/projection.py"
OLD_SOURCE_BLOB = "e77875a3d03bcb189c4053aa178f3c59375fbfce"
REVIEWED_DEPENDENCIES = {
    "phase174_r3_r7_r9_composition_associativity/rule.py": "2c44c68be90cb761d7bdd35e29f23977b5f93a2e",
    "phase169_r10e5_composite_generator_image/rule.py": "01acace3eb273d47091421a61291ee54b51c369f",
    "phase174_r3_r7_r7_composite_zero_audit/rule.py": "d98a7b45e08cd3b07c16e3f38e0a558ccebfc9b6",
    "phase174_r3_r7_r38_source_bound_zero_image_public_wiring/provider.py": "6aa48096b41714fbdf588c3ba423d264a4a13bb9",
}


def git_blob_sha(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def normalize(data: bytes) -> tuple[str, bytes, str]:
    bom = b"\xef\xbb\xbf" if data.startswith(b"\xef\xbb\xbf") else b""
    body = data[len(bom):]
    if b"\r" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70R1_UNEXPECTED_CR_ONLY")
    if b"\r\n" in body and b"\n" in body.replace(b"\r\n", b""):
        raise RuntimeError("R70R1_MIXED_LINE_ENDINGS")
    eol = "\r\n" if b"\r\n" in body else "\n"
    return body.decode("utf-8").replace("\r\n", "\n"), bom, eol


def acceptable_blob(data: bytes, expected_sha: str) -> bool:
    text, bom, _ = normalize(data)
    lf = bom + text.encode("utf-8")
    crlf = bom + text.replace("\n", "\r\n").encode("utf-8")
    return expected_sha in {
        git_blob_sha(data), git_blob_sha(lf), git_blob_sha(crlf)
    }


def function_text(source: str, name: str) -> str:
    tree = ast.parse(source)
    named = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name]
    if len(named) != 1:
        raise RuntimeError("R70R1_TARGET_FUNCTION_MISSING_OR_AMBIGUOUS")
    fragment = ast.get_source_segment(source, named[0])
    if fragment is None:
        raise RuntimeError("R70R1_NO_FUNCTION_SEGMENT")
    return fragment.rstrip("\n") + "\n"


def replacement(root: Path, original: bytes) -> tuple[str, bytes]:
    text, bom, eol = normalize(original)
    revised = (root / PACKAGE / "output/_project_composite_images_FULL_AFTER.py").read_text(encoding="utf-8")
    old_function = function_text(text, "_project_composite_images")
    if not revised.startswith("def _project_composite_images("):
        raise RuntimeError("R70R1_INVALID_REVIEWED_REPLACEMENT")
    ast.parse(revised)
    if old_function == revised:
        # Recover the prior fully reviewed function from the package's exact R70 source.
        prior = (root / PACKAGE / "output/_project_composite_images_FULL_BEFORE.py").read_text(encoding="utf-8")
        restored = text.replace(old_function, prior, 1)
        baseline = bom + restored.replace("\n", eol).encode("utf-8")
        if not acceptable_blob(baseline, OLD_SOURCE_BLOB):
            raise RuntimeError("R70R1_PATCHED_SOURCE_NOT_REVIEWED")
        return "ALREADY_APPLIED", original
    if not acceptable_blob(original, OLD_SOURCE_BLOB):
        raise RuntimeError("R70R1_SOURCE_GUARD_FAILED")
    changed = text.replace(old_function, revised, 1)
    if changed == text or changed.count(revised) != 1:
        raise RuntimeError("R70R1_PATCH_IS_NOT_SINGLE_FUNCTION")
    ast.parse(changed)
    return "PATCH_REQUIRED", bom + changed.replace("\n", eol).encode("utf-8")


def source_guard(root: Path) -> tuple[str, ...]:
    checked = []
    for name, expected in REVIEWED_DEPENDENCIES.items():
        if not acceptable_blob((root / name).read_bytes(), expected):
            raise RuntimeError("R70R1_DEPENDENCY_MISMATCH: " + name)
        checked.append(name)
    return tuple(checked)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    options = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=root,
                            capture_output=True, text=True, check=False)
    if branch.returncode or branch.stdout.strip() != "develop":
        raise RuntimeError("R70R1_DEVELOP_REQUIRED")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                          capture_output=True, text=True, check=True).stdout.strip()
    pins = source_guard(root)
    # R70 must already have installed its one-function shared formatter.
    # Do not proceed on an unrelated or unpatched narrative path.
    from phase174_r3_r7_r70_verified_narrative_projection.install import (
        TARGET as FORMATTER_TARGET,
        replace_formatter,
    )
    formatter_state, _ = replace_formatter((root / FORMATTER_TARGET).read_bytes())
    if formatter_state != "ALREADY_APPLIED":
        raise RuntimeError("R70R1_PRECEDING_R70_FORMATTER_MISSING")
    target = root / TARGET
    status, patched = replacement(root, target.read_bytes())
    print("PHASE174_R70R1_SOURCE_GUARD=PASS")
    print("PHASE174_R70R1_SOURCE_PINS=" + str(len(pins) + 1))
    print("PHASE174_R70R1_LOCAL_HEAD=" + head)
    print("PHASE174_R70R1_PATCH_STATUS=" + status)
    print("PHASE174_R70R1_NEW_GIVEN=0")
    print("PHASE174_R70R1_NEW_MATHEMATICAL_RULES=0")
    if options.dry_run:
        print("PHASE174_R70R1_GATE=PASS_R70R1_READ_ONLY_DRYRUN")
        print("(END)")
        return 0
    if status == "PATCH_REQUIRED":
        target.write_bytes(patched)
    print("PHASE174_R70R1_GATE=PASS_R70R1_ASSOCIATIVITY_PATCH_APPLIED_OR_PRESENT")
    print("(END)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

## 新規限定テスト全文（新規 `tests/test_install.py`）

```python
"""R70R1 whole-function installer and associative zero-image display regressions."""
from __future__ import annotations

from enum import Enum
from pathlib import Path
from types import ModuleType, SimpleNamespace
import sys

import pytest

from phase174_r3_r7_r70r1_assoc_chain_display_fix.install import (
    PACKAGE, TARGET, OLD_SOURCE_BLOB, git_blob_sha,
    function_text, normalize, replacement,
)
from phase174_r3_r7_r70_verified_narrative_projection.projection import (
    _project_composite_images,
)


def test_existing_r70_source_pinned_and_replaced_once(tmp_path: Path) -> None:
    actual = Path(__file__).resolve().parents[2]
    original = (actual / PACKAGE / "output/projection.py.FULL_BEFORE").read_bytes()
    assert git_blob_sha(original) == OLD_SOURCE_BLOB
    package_output = tmp_path / PACKAGE / "output"
    package_output.mkdir(parents=True, exist_ok=True)
    output = actual / PACKAGE / "output"
    for name in (
        "_project_composite_images_FULL_AFTER.py",
        "_project_composite_images_FULL_BEFORE.py",
    ):
        (package_output / name).write_bytes((output / name).read_bytes())
    status, changed = replacement(tmp_path, original)
    assert status == "PATCH_REQUIRED"
    assert changed != original
    assert "generator_image_associativity_inputs" in changed.decode()
    assert replacement(tmp_path, changed) == ("ALREADY_APPLIED", changed)
    assert function_text(changed.decode(), "_project_composite_images").count(
        "component_image_step = right_step"
    ) == 1


def test_replacement_preserves_crlf(tmp_path: Path) -> None:
    actual = Path(__file__).resolve().parents[2]
    normalized_text, _, _ = normalize((actual / PACKAGE / "output/projection.py.FULL_BEFORE").read_bytes())
    raw = normalized_text.replace("\n", "\r\n").encode()
    package_output = tmp_path / PACKAGE / "output"
    package_output.mkdir(parents=True, exist_ok=True)
    output = actual / PACKAGE / "output"
    for name in (
        "_project_composite_images_FULL_AFTER.py",
        "_project_composite_images_FULL_BEFORE.py",
    ):
        (package_output / name).write_bytes((output / name).read_bytes())
    state, result = replacement(tmp_path, raw)
    assert state == "PATCH_REQUIRED"
    assert b"\r\r\n" not in result
    assert b"\r\n" in result
    assert replacement(tmp_path, result) == ("ALREADY_APPLIED", result)


def test_replacement_rejects_unreviewed_content(tmp_path: Path) -> None:
    actual = Path(__file__).resolve().parents[2]
    source = (actual / PACKAGE / "output/projection.py.FULL_BEFORE").read_bytes() + b"# unreviewed change\n"
    with pytest.raises(RuntimeError, match="R70R1_SOURCE_GUARD_FAILED"):
        replacement(actual, source)


def test_normalize_rejects_mixed_and_cr_only() -> None:
    with pytest.raises(RuntimeError, match="R70R1_UNEXPECTED_CR_ONLY"):
        normalize(b"a\rb\n")
    with pytest.raises(RuntimeError, match="R70R1_MIXED_LINE_ENDINGS"):
        normalize(b"a\r\nb\n")


class ProofRule(Enum):
    GIVEN = "given"
    INFERENCE = "inference"


class Zero:
    pass


class GeneratorImage:
    def __init__(self, mapping, source_generator, target_generator):
        self.map = mapping
        self.source_generator = source_generator
        self.target_generator = target_generator


class Step:
    def __init__(self, conclusion, premises=(), rule=ProofRule.INFERENCE, name=""):
        self.conclusion = conclusion
        self.premises = tuple(premises)
        self.rule = rule
        self.inference_rule = SimpleNamespace(name=name)


@pytest.fixture
def chain(monkeypatch: pytest.MonkeyPatch):
    """Model exactly the production R7 <- R9 associativity <- composition route."""
    def install(name: str, **members) -> None:
        module = ModuleType(name)
        module.__dict__.update(members)
        monkeypatch.setitem(sys.modules, name, module)

    install("proof", ProofRule=ProofRule)
    install("expression", Zero=Zero)
    install("phase165_r14_r6_generic_iso", GeneratorImage=GeneratorImage)
    install("phase168_r3_27_typed_statement_projection",
            typed_sentence=lambda conclusion, step: getattr(conclusion, "sentence", None))
    install("toda_proof_narrative_renderer", render_toda_expression_latex=lambda obj: obj)

    generator = r"\nu_{5}\eta_{8}^{2}"
    lifted = r"\nu_{6}\eta_{9}^{2}"
    mapping = object()
    source = Step("Toda 5.9", rule=ProofRule.GIVEN)
    first = Step(SimpleNamespace(sentence=r"$E(\nu_{5})=\nu_{6}$."))
    second = Step(SimpleNamespace(sentence=r"$E(\eta_{8}^{2})=\eta_{9}^{2}$."))
    right_goal = GeneratorImage(mapping, generator, lifted)
    right_step = Step(right_goal, (first, second), name="suspension preserves composition")
    left_goal = GeneratorImage(mapping, generator, lifted)
    left_step = Step(left_goal, (right_step,), name="composition associativity")
    annihilator = Step(SimpleNamespace(sentence=r"$\nu_{6}\eta_{9}=0$."), (source,))
    zero_goal = GeneratorImage(mapping, generator, Zero())
    zero_step = Step(zero_goal, (left_step, annihilator), name="composite zero")
    model = SimpleNamespace(
        steps=(source, first, second, right_step, left_step, annihilator, zero_step),
        step_citation_numbers=((2,), (), (), (), (), (), ()),
        root_index=6,
    )
    install("phase169_r10e5_composite_generator_image.rule",
            component_image_obligations=lambda goal:
            (first.conclusion, second.conclusion) if goal is right_goal else None)
    install("phase174_r3_r7_r9_composition_associativity.rule",
            RULE_NAME="composition associativity",
            generator_image_associativity_inputs=lambda goal:
            (right_goal,) if goal is left_goal else None)
    install("phase174_r3_r7_r7_composite_zero_audit.rule",
            RULE_NAME="composite zero",
            composite_zero_generator_inputs=lambda goal, candidate:
            (left_goal, annihilator.conclusion) if goal is zero_goal else None)
    lines = [
        "使用する結果", "", "証明", "",
        r"$E(\nu_{5})=\nu_{6}$.", "",
        r"$E(\eta_{8}^{2})=\eta_{9}^{2}$.", "",
        r"[R2]より, $\nu_{6}\eta_{9}=0$.", "", "□",
    ]
    return model, lines, left_step


def test_verified_associativity_bridge_is_condensed(chain):
    model, lines, _ = chain
    condensed = _project_composite_images(lines, model, frozenset(range(7)))
    assert r"$E(\nu_{5})=\nu_{6}$." not in condensed
    assert r"$E(\eta_{8}^{2})=\eta_{9}^{2}$." not in condensed
    assert r"[R2]より, $\nu_{6}\eta_{9}=0$." not in condensed
    assert "懸垂と合成の関係および [R2]より, " + (
        r"$E(\nu_{5}\eta_{8}^{2})=\nu_{6}\eta_{9}^{2}=0$."
    ) in condensed
    assert condensed[0:3] == lines[0:3]
    assert condensed[-1] == "□"


def test_no_rewrite_if_associativity_rule_unverified(chain):
    model, lines, left = chain
    left.inference_rule.name = "other rule"
    assert _project_composite_images(lines, model, frozenset(range(7))) == lines


def test_no_rewrite_without_cited_given_ancestor(chain):
    model, lines, _ = chain
    model.step_citation_numbers = ((), (), (), (), (), (), ())
    assert _project_composite_images(lines, model, frozenset(range(7))) == lines


def test_no_rewrite_if_intervening_nonempty_sentence(chain):
    model, lines, _ = chain
    different = lines.copy()
    different.insert(5, "別の独立した証明行.")
    assert _project_composite_images(different, model, frozenset(range(7))) == different


def test_no_rewrite_if_component_outside_root_scope(chain):
    model, lines, _ = chain
    assert _project_composite_images(lines, model, frozenset({0, 2, 3, 4, 5, 6})) == lines
```

## 新規 `run.ps1` 全文

```powershell
param([switch]$DryRun)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $root
$package = 'phase174_r3_r7_r70r1_assoc_chain_display_fix'

python -m "$package.install" $(if ($DryRun) { '--dry-run' })
if ($LASTEXITCODE -ne 0) { throw 'R70R1 source guard or installer failed' }

if ($DryRun) {
    Write-Output 'PHASE174_R70R1_GATE=PASS_R70R1_DRYRUN'
    Write-Output '(END)'
    exit 0
}

python -m pytest -q -p no:cacheprovider -o addopts= --import-mode=importlib `
    "$package/tests/test_install.py" `
    'phase174_r3_r7_r70_verified_narrative_projection/tests/test_projection.py' `
    'phase171_r20r13_eta_sentence_layout/tests/test_projection.py' `
    'phase171_r20r13r2_multiple_blank_eta_merge/tests/test_correction.py' `
    'phase174_r3_r7_r69_general_narrative_gap_audit/tests/test_audit.py' `
    'phase174_r3_r7_r68_ehp_premise_semantics_audit/tests/test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R70R1 focused pytest failed' }

python -m phase174_r3_r7_r70_verified_narrative_projection.audit
if ($LASTEXITCODE -ne 0) { throw 'R70R1 R70 public narrative regression failed' }

Write-Output 'PHASE174_R70R1_GATE=PASS_R70R1_FOCUSED_AND_PUBLIC_ASSOCIATIVITY'
Write-Output '(END)'
```
