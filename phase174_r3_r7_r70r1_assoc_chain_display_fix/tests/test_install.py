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
