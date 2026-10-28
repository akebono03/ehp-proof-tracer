"""Isolated R10EN provenance and fail-closed policy tests."""
from __future__ import annotations

import importlib.util
import sys
from enum import Enum
from pathlib import Path
from types import ModuleType, SimpleNamespace


def make_module(monkeypatch):
    class Rule(Enum):
        GIVEN = "given"
        INFERENCE = "inference"

    class Image:
        pass

    proof = ModuleType("proof")
    proof.ProofRule = Rule
    images = ModuleType("phase165_r14_r6_generic_iso")
    images.GeneratorImage = Image
    monkeypatch.setitem(sys.modules, "proof", proof)
    monkeypatch.setitem(sys.modules, "phase165_r14_r6_generic_iso", images)
    filepath = Path(__file__).resolve().parents[1] / "core.py"
    spec = importlib.util.spec_from_file_location("r10en_isolated_core", filepath)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module, Rule, Image


def make_tree(rule, image_type):
    given = SimpleNamespace(rule=rule.GIVEN, premises=(), conclusion=object())
    first = SimpleNamespace(rule=rule.INFERENCE, premises=(given,), conclusion=image_type())
    other = SimpleNamespace(rule=rule.INFERENCE, premises=(), conclusion=image_type())
    root = SimpleNamespace(rule=rule.INFERENCE, premises=(first, other), conclusion=object())
    model = SimpleNamespace(
        steps=(given, first, other, root),
        step_citation_numbers=((4, 2), (), (), ()),
        citations=(SimpleNamespace(number=2), SimpleNamespace(number=4)),
    )
    return model, first, other


def test_r10en_cyclic_union_policy(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=False,
    ) == (2, 4)


def test_r10en_direct_sum_requires_each_image_cited(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=True,
    ) is None


def test_r10en_direct_sum_positive_for_each_image(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    other.premises = (model.steps[0],)
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=True,
    ) == (2, 4)


def test_r10en_unregistered_citation_fails_closed(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    model.step_citation_numbers = ((4, 99), (), (), ())
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=False,
    ) is None


def test_r10en_unindexed_ancestor_fails_closed(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    first.premises = (SimpleNamespace(rule=rule.GIVEN, premises=()),)
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=False,
    ) is None


def test_r10en_ancestor_missing_from_order_fails_closed(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    assert module.verified_generator_image_citation_numbers(
        model, (1, 2, 3), (first, other), require_each=False,
    ) is None


def test_r10en_duplicate_image_refuses(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, first), require_each=False,
    ) is None


def test_r10en_uncited_union_refuses(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    model.step_citation_numbers = ((), (), (), ())
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=False,
    ) is None


def test_r10en_never_modifies_steps_or_citations(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    before = (tuple(id(x) for x in model.steps), model.step_citation_numbers,
              tuple(id(x) for x in model.citations))
    assert module.verified_generator_image_citation_numbers(
        model, (0, 1, 2, 3), (first, other), require_each=False,
    ) is not None
    after = (tuple(id(x) for x in model.steps), model.step_citation_numbers,
             tuple(id(x) for x in model.citations))
    assert after == before


def test_r10en_invalid_or_malformed_input_refuses(monkeypatch):
    module, rule, image = make_module(monkeypatch)
    model, first, other = make_tree(rule, image)
    check = module.verified_generator_image_citation_numbers
    assert check(model, (0, 1, 1, 2, 3), (first,), require_each=False) is None
    assert check(model, (0, 1, 2, 3), (first,), require_each="false") is None
    assert check(model, (0, 1, 2, 3), (), require_each=False) is None
    model.citations = (SimpleNamespace(number=2), SimpleNamespace(number=2))
    assert check(model, (0, 1, 2, 3), (first,), require_each=False) is None
