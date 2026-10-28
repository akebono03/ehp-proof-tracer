"""AUDIT_ONLY: exact proved Definition support and cited-image fallback tests."""
from __future__ import annotations

from enum import Enum
from types import SimpleNamespace as Node

from phase169_r10et_r3_cyclic_definition_projection_audit.policy import (
    proposed_cyclic_image_citations,
)


class Rule(Enum):
    GIVEN = "given"
    INFERENCE = "inference"


def tree(*, mixed: bool):
    prior = Node(rule=Rule.GIVEN, premises=())
    iso_given = Node(rule=Rule.GIVEN, premises=())
    iso = Node(rule=Rule.INFERENCE, premises=(iso_given,))
    definition = Node(rule=Rule.INFERENCE, premises=(), kind="definition")
    others = [prior, iso_given, iso, definition]
    links = [(1,), (2,), (), ()]
    citations = [Node(number=1), Node(number=2)]
    images = [definition]
    if mixed:
        source_given = Node(rule=Rule.GIVEN, premises=())
        cited_image = Node(rule=Rule.INFERENCE, premises=(source_given,), kind="cited")
        others.extend((source_given, cited_image))
        links.extend(((3,), ()))
        citations.append(Node(number=3))
        images.append(cited_image)
    else:
        another = Node(rule=Rule.INFERENCE, premises=(), kind="definition")
        others.append(another)
        links.append(())
        images.append(another)
    root = Node(rule=Rule.INFERENCE, premises=(prior, iso, *images))
    others.append(root)
    links.append(())
    model = Node(steps=tuple(others),
                 step_citation_numbers=tuple(links),
                 citations=tuple(citations), root_index=len(others) - 1)
    return model, tuple(images)


def candidate(model, images, *, cited=(3,), canonical=None):
    checker = (canonical if canonical is not None
               else lambda x: getattr(x, "kind", None) == "definition")
    return proposed_cyclic_image_citations(
        model, tuple(range(len(model.steps))), images,
        legacy_checker=lambda m, o, s, require_each: cited,
        canonical_definition_checker=checker,
        given_rule=Rule.GIVEN, inference_rule=Rule.INFERENCE,
    )


def test_r10et_r3_only_certified_definition_images_need_no_family_citation():
    model, images = tree(mixed=False)
    assert candidate(model, images, cited=None) == ()
    assert candidate(model, images, cited=None, canonical=lambda _: False) is None


def test_r10et_r3_mixed_paths_keep_actual_given_provenance():
    model, images = tree(mixed=True)
    assert candidate(model, images) == (3,)
    assert candidate(model, images, cited=None) is None
    assert candidate(model, images, cited=()) is None


def test_r10et_r3_refuses_missing_root_source_or_iso_citation():
    model, images = tree(mixed=False)
    damaged = list(model.step_citation_numbers)
    damaged[0] = ()
    assert candidate(replace_dummy(model, tuple(damaged)), images) is None
    damaged = list(model.step_citation_numbers)
    damaged[1] = ()
    assert candidate(replace_dummy(model, tuple(damaged)), images) is None


def test_r10et_r3_refuses_unregistered_and_forged_citation_or_duplicate():
    model, images = tree(mixed=False)
    damaged = list(model.step_citation_numbers)
    damaged[0] = (99,)
    assert candidate(replace_dummy(model, tuple(damaged)), images) is None
    assert candidate(model, (images[0], images[0])) is None
    assert candidate(model, images, canonical=lambda _: True) == ()
    bad = Node(rule=Rule.INFERENCE, premises=(), kind="definition")
    assert candidate(model, (bad,)) is None


def replace_dummy(model, links):
    return Node(steps=model.steps, step_citation_numbers=links,
                citations=model.citations, root_index=model.root_index)
