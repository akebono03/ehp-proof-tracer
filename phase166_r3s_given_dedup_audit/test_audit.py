"""Small unit tests for R3-S duplicate link detection."""
from dataclasses import dataclass

from proof import ProofRule, ProofStep, Relation
from phase165_r14_r6_generic_iso import GeneratorImage
from audit import HOPF_RELATION_IDS, inspect_bridge


@dataclass(frozen=True)
class Link:
    assertion_id: str
    step: ProofStep


@dataclass(frozen=True)
class Registry:
    _assertions: dict


@dataclass(frozen=True)
class Bridge:
    registry: Registry
    proof_links: tuple[Link, ...]


def sample_bridge(include_duplicate: bool) -> Bridge:
    image = Link("image", ProofStep(GeneratorImage("H", "eta2", "iota3"), (), ProofRule.GIVEN))
    links = (image,)
    if include_duplicate:
        links += (Link(HOPF_RELATION_IDS[0], ProofStep(Relation("H(eta2)", "iota3"), (), ProofRule.GIVEN)),)
    return Bridge(Registry({HOPF_RELATION_IDS[0]: object()}), links)


def test_r3s_accepts_registered_statement_without_given_link():
    report = inspect_bridge(sample_bridge(False))
    assert report["no_duplicate_hopf_given"]
    assert report["registered_assertions_preserved"]
    assert report["generator_image_given_links"] == ["image"]


def test_r3s_detects_duplicate_independent_given():
    report = inspect_bridge(sample_bridge(True))
    assert not report["no_duplicate_hopf_given"]
    assert report["duplicate_hopf_relation_given_links"] == [HOPF_RELATION_IDS[0]]


def test_r3s_does_not_mutate_existing_links():
    bridge = sample_bridge(True)
    before = bridge.proof_links
    inspect_bridge(bridge)
    assert bridge.proof_links == before
