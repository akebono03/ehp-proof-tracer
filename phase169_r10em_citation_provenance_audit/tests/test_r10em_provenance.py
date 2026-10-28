"""Focused independent tests; no live repository or production edits."""
from __future__ import annotations

import importlib.util
import sys
from enum import Enum
from pathlib import Path
from types import ModuleType, SimpleNamespace


def _module(monkeypatch):
    class Rule(Enum):
        GIVEN = "given"
        INFERENCE = "inference"

    stub = ModuleType("proof")
    stub.ProofRule = Rule
    monkeypatch.setitem(sys.modules, "proof", stub)
    path = Path(__file__).resolve().parents[1] / "provenance.py"
    spec = importlib.util.spec_from_file_location("r10em_provenance_isolated", path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module, Rule


def _fixture(rule):
    given = SimpleNamespace(rule=rule.GIVEN, premises=())
    image1 = SimpleNamespace(rule=rule.INFERENCE, premises=(given,))
    image2 = SimpleNamespace(rule=rule.INFERENCE, premises=(given,))
    root = SimpleNamespace(rule=rule.INFERENCE, premises=(image1, image2))
    model = SimpleNamespace(
        steps=(given, image1, image2, root),
        step_citation_numbers=((2,), (), (), ()),
        citations=(SimpleNamespace(number=2),),
    )
    return model, image1, image2


def test_r10em_traces_both_images_to_same_real_given(monkeypatch):
    module, rule = _module(monkeypatch)
    model, image1, image2 = _fixture(rule)
    found = module.trace_generator_image_citations(
        model, (0, 1, 2, 3), (image1, image2),
    )
    assert found is not None
    assert [r.image_step_index for r in found] == [1, 2]
    assert all(row.given_step_indices == (0,) for row in found)
    assert all(row.registered_citation_numbers == (2,) for row in found)
    summary = module.summarize_image_provenance(found, (2,))
    assert summary["every_image_has_cited_given"]
    assert summary["projection_matches_union"]


def test_r10em_rejects_unindexed_ancestor_as_provenance(monkeypatch):
    module, rule = _module(monkeypatch)
    model, image1, image2 = _fixture(rule)
    found = module.trace_generator_image_citations(
        model, (1, 2, 3), (image1, image2),
    )
    assert found is not None
    assert all(row.missing_ancestor_indices for row in found)
    assert not module.summarize_image_provenance(found, (2,))["every_image_has_cited_given"]


def test_r10em_unregistered_citation_is_not_accepted(monkeypatch):
    module, rule = _module(monkeypatch)
    model, image1, image2 = _fixture(rule)
    model.step_citation_numbers = ((9,), (), (), ())
    found = module.trace_generator_image_citations(
        model, (0, 1, 2, 3), (image1, image2),
    )
    assert found is not None
    summary = module.summarize_image_provenance(found, (2,))
    assert summary["unregistered_citations"] == [9]
    assert not summary["every_image_has_cited_given"]
    assert not summary["projection_matches_union"]


def test_r10em_distinguishes_group_union_from_individual_coverage(monkeypatch):
    module, rule = _module(monkeypatch)
    model, image1, image2 = _fixture(rule)
    ungrounded = SimpleNamespace(rule=rule.INFERENCE, premises=())
    model.steps = (model.steps[0], image1, ungrounded, model.steps[3])
    found = module.trace_generator_image_citations(
        model, (0, 1, 2, 3), (image1, ungrounded),
    )
    assert found is not None
    summary = module.summarize_image_provenance(found, (2,))
    assert summary["projection_matches_union"]
    assert not summary["every_image_has_cited_given"]
    assert summary["images_with_cited_given"] == 1


def test_r10em_rejects_missing_image_or_duplicate_order(monkeypatch):
    module, rule = _module(monkeypatch)
    model, image1, image2 = _fixture(rule)
    assert module.trace_generator_image_citations(
        model, (0, 1, 2, 2, 3), (image1, image2),
    ) is None
    assert module.trace_generator_image_citations(
        model, (0, 1, 2, 3), (image1, image1),
    ) is None
    assert module.trace_generator_image_citations(
        model, (0, 1, 2, 3), (object(),),
    ) is None


def test_r10em_never_mutates_the_supplied_proof(monkeypatch):
    module, rule = _module(monkeypatch)
    model, image1, image2 = _fixture(rule)
    before = (tuple(id(x) for x in model.steps), model.step_citation_numbers)
    assert module.trace_generator_image_citations(
        model, (0, 1, 2, 3), (image1, image2),
    ) is not None
    assert (tuple(id(x) for x in model.steps), model.step_citation_numbers) == before
