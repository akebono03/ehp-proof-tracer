"""Standalone graph checks of the shared suppression helper."""
from __future__ import annotations

import importlib.util
import sys
from enum import Enum
from pathlib import Path
from types import ModuleType, SimpleNamespace


def _load_isolated_core(monkeypatch):
    class ProofRule(Enum):
        GIVEN = "given"
        INFERENCE = "inference"

    class GeneratorImage:
        pass

    class GeneratorSuspension:
        pass

    names = {
        "proof": {"ProofRule": ProofRule},
        "phase165_r14_r14_diagonal_and_prop42": {
            "GeneratorSuspension": GeneratorSuspension,
        },
        "phase165_r14_r6_generic_iso": {"GeneratorImage": GeneratorImage},
    }
    for name, attrs in names.items():
        stub = ModuleType(name)
        for field, value in attrs.items():
            setattr(stub, field, value)
        monkeypatch.setitem(sys.modules, name, stub)
    path = Path(__file__).resolve().parents[1] / "core.py"
    spec = importlib.util.spec_from_file_location("r10el_core_standalone", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, ProofRule, GeneratorImage, GeneratorSuspension


def _graph(rule, image_type, suspension_type):
    given = SimpleNamespace(conclusion=object(), rule=rule.GIVEN, premises=())
    suspension = SimpleNamespace(
        conclusion=suspension_type(), rule=rule.INFERENCE, premises=(given,),
    )
    image = SimpleNamespace(
        conclusion=image_type(), rule=rule.INFERENCE, premises=(suspension,),
    )
    root = SimpleNamespace(conclusion=object(), rule=rule.INFERENCE,
                           premises=(image,))
    steps = (given, suspension, image, root)
    model = SimpleNamespace(steps=steps, step_citation_numbers=((), (), (), ()))
    return model, image


def test_r10el_isolated_exclusive_ancestry(monkeypatch):
    module, rule, image_type, suspension_type = _load_isolated_core(monkeypatch)
    model, image = _graph(rule, image_type, suspension_type)
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 3), [image], 3, require_all=True,
    ) == (1, 2)
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 3), [image], 3, require_all=False,
    ) == (1, 2)


def test_r10el_isolated_external_consumer_fails_closed(monkeypatch):
    module, rule, image_type, suspension_type = _load_isolated_core(monkeypatch)
    model, image = _graph(rule, image_type, suspension_type)
    external = SimpleNamespace(
        conclusion=object(), rule=rule.INFERENCE, premises=(model.steps[1],),
    )
    model.steps += (external,)
    model.step_citation_numbers += ((),)
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 3, 4), [image], 3, require_all=True,
    ) is None
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 3, 4), [image], 3, require_all=False,
    ) == (2,)


def test_r10el_isolated_individual_citation_preserved(monkeypatch):
    module, rule, image_type, suspension_type = _load_isolated_core(monkeypatch)
    model, image = _graph(rule, image_type, suspension_type)
    model.step_citation_numbers = ((), (1,), (), ())
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 3), [image], 3, require_all=True,
    ) == (2,)
    model.step_citation_numbers = ((), (), (2,), ())
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 3), [image], 3, require_all=True,
    ) is None


def test_r10el_isolated_duplicate_indices_and_missing_node(monkeypatch):
    module, rule, image_type, suspension_type = _load_isolated_core(monkeypatch)
    model, image = _graph(rule, image_type, suspension_type)
    assert module.exclusive_generator_inference_indices(
        model, (0, 1, 2, 2, 3), [image], 3, require_all=True,
    ) is None
    assert module.exclusive_generator_inference_indices(
        model, (0, 2, 3), [image], 3, require_all=True,
    ) is None
