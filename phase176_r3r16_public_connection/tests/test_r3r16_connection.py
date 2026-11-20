"""Focused tests of the R3R16 public source and generic right-zero connection."""
from __future__ import annotations

from dataclasses import replace

from expression import Composition, HomotopyElement, Zero
from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from phase165_r14_r6_generic_iso import GeneratorImage
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase175_r3r9_lemma57_explicit_public.source import (
    TodaLemma57ExplicitNuPrimeZero,
    build_explicit_lemma57_source,
)
from phase176_r3r16_public_connection.provider import build_public_lemma57_right_provider
from proof import ProofRule, ProofStep
from unified_statement_registry import UnifiedStatementRegistry
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_no_screened_source_means_no_proposals():
    empty = RegistryBridgeResult(UnifiedStatementRegistry(), (), ())
    provider = build_public_lemma57_right_provider(empty)
    assert provider(object()) == ()


def test_real_source_only_is_not_direct_image_given():
    source = build_explicit_lemma57_source(ROOT)
    provider = build_public_lemma57_right_provider(source)
    assert all(link.step.rule is ProofRule.GIVEN for link in source.proof_links)
    assert all(type(link.step.conclusion) is TodaLemma57ExplicitNuPrimeZero for link in source.proof_links)
    assert provider(object()) == ()


def test_wrong_source_content_is_rejected():
    source = build_explicit_lemma57_source(ROOT)
    bad_link = replace(source.proof_links[0], step=ProofStep("fake", (), ProofRule.GIVEN))
    bad = RegistryBridgeResult(source.registry, source.records, (bad_link,))
    assert build_public_lemma57_right_provider(bad)(object()) == ()


def test_typed_generic_right_zero_requires_three_factors():
    from phase176_r3r14_isolated_two_stage_provider.provider import preceding_zero_image
    a = HomotopyElement("a", dimension=2, source=3, target=2)
    b = HomotopyElement("b", dimension=3, source=6, target=3)
    c = HomotopyElement("c", dimension=6, source=7, target=6)
    goal = GeneratorImage(
        TodaSuspensionMap(TodaPrimaryGroup(7, 2), TodaPrimaryGroup(8, 3)),
        Composition(a, Composition(b, c)), Zero(),
    )
    assert preceding_zero_image(goal) is not None
    assert preceding_zero_image(replace(goal, source_generator=Composition(a, b))) is None
