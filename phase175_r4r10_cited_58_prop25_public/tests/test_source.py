"""Toda source anchors/metadata are checked, not guessed from output labels."""
from __future__ import annotations

from pathlib import Path

import pytest

from phase175_r4r10_cited_58_prop25_public import source


def cited_blocks() -> dict[str, str]:
    return {
        source.CHAPTER_2: (
            r'\begin{proposition}\label{prop:2.5}' + '\n'
            + r'\alpha\in\pi_{i+1}(S^{2m+1}), \ \beta\in \pi_{j-1}(S^{i-1})'
            + '\n' + r'\Delta\alpha\ \circ\ \beta\ \subset\ \Delta(\alpha\circ E^2\beta)'
            + '\n' + r'j<3m-1, \(2\)-primary では等号'
            + '\n' + r'\end{proposition}'
        ),
        source.CHAPTER_5: (
            r'\begin{equation}\label{eq:5.8}' + '\n'
            + r"\Delta(\iota_9)=\pm(2\nu_4-E\nu')"
            + '\n' + r'\end{equation}'
            + '\n' + r'\begin{proposition}\label{prop:5.8}'
        ),
    }


def prepare_source(monkeypatch: pytest.MonkeyPatch) -> dict[str, str]:
    blocks = cited_blocks()
    monkeypatch.setattr(source, 'vetted_source',
                        lambda path, expected: blocks[path.relative_to(source.ROOT).as_posix()])
    monkeypatch.setattr(source, '_load_manifest_reference_order',
                        lambda manifest: ({
                            source.PROPOSITION_REFERENCE_ID: 2500,
                            source.EQUATION_REFERENCE_ID: 8500,
                            'toda:Proposition 5.8': 9000,
                        }, {}, {}))
    return blocks


def test_full_toda_source_conditions_and_manifest_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prepare_source(monkeypatch)
    assert source.source_positions() == {
        source.PROPOSITION_REFERENCE_ID: 2500,
        source.EQUATION_REFERENCE_ID: 8500,
    }


def test_removed_prop25_inequality_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocks = prepare_source(monkeypatch)
    blocks[source.CHAPTER_2] = blocks[source.CHAPTER_2].replace('j<3m-1', 'j>3m-1')
    with pytest.raises(ValueError, match='PROP25_SOURCE_CHANGED'):
        source.source_positions()


def test_modified_toda58_sign_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocks = prepare_source(monkeypatch)
    blocks[source.CHAPTER_5] = blocks[source.CHAPTER_5].replace(r'\pm', '+')
    with pytest.raises(ValueError, match='EQ58_SOURCE_CHANGED'):
        source.source_positions()


def test_missing_recorded_publication_order_is_rejected(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prepare_source(monkeypatch)
    monkeypatch.setattr(source, '_load_manifest_reference_order',
                        lambda manifest: ({source.EQUATION_REFERENCE_ID: 8500}, {}, {}))
    with pytest.raises(ValueError, match='SOURCE_POSITION_INVALID'):
        source.source_positions()


def test_signed_source_registration_has_exactly_two_cited_given_leaves(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    prepare_source(monkeypatch)
    from proof import ProofRule
    bridge = source.build_cited_58_prop25_sources()
    assert len(bridge.proof_links) == 2
    assert all(link.step.rule is ProofRule.GIVEN for link in bridge.proof_links)
    assert all(link.step.inference_rule.literature_reference is not None
               for link in bridge.proof_links)
    assert {bridge.registry.reference(x.reference_id).locator
            for x in bridge.registry._assertions.values()} == {
                '(5.8)', 'Proposition 2.5',
            }
