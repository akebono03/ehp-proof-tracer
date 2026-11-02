"""Focused tests for source-gated Toda Lemma 5.4 and inferred Hopf claim."""
from __future__ import annotations

from hashlib import sha256
from types import SimpleNamespace

import pytest

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase173_r4_r1_lemma54_source_bridge.source import (
    ADOPTED_ASSERTION_ID,
    SOURCE_ID,
    TodaLemma54TypedSource,
    add_verified_lemma54_source,
    canonical_hopf_relation,
    expand_cited_lemma54_hopf,
    lemma54_hopf_inference_rule,
    validate_lemma54_text,
)
from proof import ProofRule
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def source_text() -> str:
    return (
        "chapter prefix\n"
        "\\begin{lemma}[]\n\\label{lem:5.4}\n"
        "\\nu_{4}\\in \\pi^{4}_{7}\n"
        "H(\\nu_{4})=\\iota_7,\\qquad 2E \\nu_{4}=E^{2}\\nu' .\n"
        "\\end{lemma}\nchapter suffix\n"
    )


def archive_bridge(*, modified_text: str | None = None,
                   wrong_hash: bool = False,
                   source_position: int | None = 3,
                   goal_position: int | None = 5) -> RegistryBridgeResult:
    text = source_text() if modified_text is None else modified_text
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="archive:lemma54", kind=ReferenceKind.LEMMA,
        locator="Lemma 5.4", source_id=SOURCE_ID,
        publication_position=source_position,
    ))
    registry.add_reference(LiteratureEntry(
        reference_id="goal:prop56", kind=ReferenceKind.PROPOSITION,
        locator="Proposition 5.6", publication_position=goal_position,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="source:archive", reference_id="archive:lemma54",
        kind=AssertionKind.STATEMENT,
        content={
            "source_statement_id": SOURCE_ID,
            "source_text": text,
            "source_sha256": "bad" if wrong_hash else sha256(text.encode("utf-8")).hexdigest(),
        },
        origin=AssertionOrigin.SOURCE_ARCHIVE,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="target:goal", reference_id="goal:prop56",
        kind=AssertionKind.STATEMENT, content="independent proof goal",
        origin=AssertionOrigin.FIXED_STATEMENT,
    ))
    return RegistryBridgeResult(registry, (), ())


def test_verified_toda_lemma54_text() -> None:
    validate_lemma54_text(source_text())


@pytest.mark.parametrize("missing", [
    r"\label{lem:5.4}", r"\nu_{4}\in \pi^{4}_{7}",
    r"H(\nu_{4})=\iota_7", r"2E \nu_{4}=E^{2}\nu'",
])
def test_missing_source_fragment_is_rejected(missing: str) -> None:
    with pytest.raises(ValueError):
        validate_lemma54_text(source_text().replace(missing, "REMOVED"))


def test_register_source_only_after_exact_hash_and_position() -> None:
    bridge = archive_bridge()
    updated = add_verified_lemma54_source(
        bridge, citing_assertion_id="target:goal", chapter=source_text(),
    )
    assert ADOPTED_ASSERTION_ID not in bridge.registry._assertions
    registered = updated.registry.assertion(ADOPTED_ASSERTION_ID)
    assert registered.origin is AssertionOrigin.FIXED_STATEMENT
    assert registered.content == TodaLemma54TypedSource()
    assert registered.reference_id == "archive:lemma54"
    assert updated.proof_links == ()


def test_modified_archive_hash_is_rejected() -> None:
    with pytest.raises(ValueError, match="SHA-256"):
        add_verified_lemma54_source(
            archive_bridge(wrong_hash=True),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_archive_must_be_literal_chapter_passage() -> None:
    text = source_text().replace("chapter prefix", "different prefix")
    with pytest.raises(ValueError, match="literal source passage"):
        add_verified_lemma54_source(
            archive_bridge(modified_text=text),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_citation_after_target_is_rejected() -> None:
    with pytest.raises(ValueError, match="earlier publication"):
        add_verified_lemma54_source(
            archive_bridge(source_position=9),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_missing_position_is_rejected() -> None:
    with pytest.raises(ValueError, match="earlier publication"):
        add_verified_lemma54_source(
            archive_bridge(source_position=None),
            citing_assertion_id="target:goal", chapter=source_text(),
        )


def test_derived_hopf_requires_one_screened_typed_source() -> None:
    goal = canonical_hopf_relation()
    assert expand_cited_lemma54_hopf(goal, ()) == ()
    source = TodaLemma54TypedSource()
    result = expand_cited_lemma54_hopf(goal, (source,))
    assert len(result) == 1
    assert result[0].subgoals == (source,)
    assert result[0].rule.conclusion_pattern == goal
    assert expand_cited_lemma54_hopf(goal, (source, source)) == ()


def test_inference_refuses_given_hopf_as_inference_source() -> None:
    goal = canonical_hopf_relation()
    rule = lemma54_hopf_inference_rule(goal)
    source = TodaLemma54TypedSource()
    good = SimpleNamespace(conclusion=source, rule=ProofRule.GIVEN)
    wrong = SimpleNamespace(conclusion=source, rule=ProofRule.INFERENCE)
    assert rule.match_guard((good,), {}) is True
    assert rule.match_guard((wrong,), {}) is False


def test_wrong_goal_is_not_inferred() -> None:
    with pytest.raises(ValueError):
        lemma54_hopf_inference_rule(object())
    assert expand_cited_lemma54_hopf(object(), (TodaLemma54TypedSource(),)) == ()
