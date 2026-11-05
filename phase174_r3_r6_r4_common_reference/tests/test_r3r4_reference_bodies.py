"""Focused source-bound Reference projections, not a new proof-search rule."""
from __future__ import annotations

from dataclasses import replace

from phase168_r3_37c_reference_projection import project_reference_bodies
from phase174_r3_r5_finite_cyclic_extension.rule import (
    Toda48UniversalConditionalStatement,
)
from phase174_r3_r6_source_extension.source import (
    Toda55UniversalDoubleStatement,
    build_cited_extension_sources,
)
from phase174_r3_r6_r4_common_reference.projection import (
    project_cited_universal_toda_reference_body,
)
from unified_statement_registry import (
    AssertionEntry,
    AssertionKind,
    AssertionOrigin,
    LiteratureEntry,
    ReferenceKind,
    UnifiedStatementRegistry,
)


def test_reviewed_toda48_keeps_condition_and_generic_formula() -> None:
    bridge = build_cited_extension_sources()
    assertion_id = "toda:174:r3r6:universal:(4.8)"
    entry = bridge.registry.assertion(assertion_id)
    body = project_reference_bodies(bridge.registry, (assertion_id,))
    assert len(body) == 1
    assert r"$\Delta(\iota_{2n-1})=0$ と仮定する" in body[0]
    assert r"E^2:\pi_{2n-2}^{n-1}\hookrightarrow\pi_{2n}^{n+1}" in body[0]
    assert r"\pi_{2n}^{n+1}/E^2(\pi_{2n-2}^{n-1})\cong\mathbb{Z}/2" in body[0]
    assert r"\pi_{8}^{5}" not in body[0]
    assert entry.content == Toda48UniversalConditionalStatement()


def test_reviewed_toda55_is_general_and_distinct_from_group_result() -> None:
    bridge = build_cited_extension_sources()
    assertion_id = "toda:174:r3r6:universal:(5.5)"
    body = project_reference_bodies(bridge.registry, (assertion_id,))
    assert body == (r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$.",)
    assert "\\pi_{8}^{5}" not in body[0]
    assert bridge.registry.assertion(assertion_id).content == Toda55UniversalDoubleStatement()


def test_unowned_mismatched_or_modified_source_is_not_rendered() -> None:
    bridge = build_cited_extension_sources()
    assertion_id = "toda:174:r3r6:universal:(5.5)"
    assertion = bridge.registry.assertion(assertion_id)
    expected = assertion.content
    projector = project_cited_universal_toda_reference_body
    assert projector(replace(assertion), bridge.registry, expected) is None
    assert projector(replace(assertion, reference_id="toda:(4.8)"), bridge.registry, expected) is None
    assert projector(replace(assertion, scope=("other",)), bridge.registry, expected) is None
    assert projector(replace(assertion, origin=AssertionOrigin.PROOF_INTERNAL), bridge.registry, expected) is None
    assert projector(assertion, bridge.registry, replace(expected, coefficient=3)) is None
    assert projector(assertion, bridge.registry, Toda48UniversalConditionalStatement()) is None
    fake = UnifiedStatementRegistry()
    fake.add_reference(LiteratureEntry(
        reference_id="toda:(5.5)", kind=ReferenceKind.EQUATION,
        locator="(5.5)", source_id="unverified", publication_position=8600,
    ))
    fake.add_assertion(assertion)
    assert project_reference_bodies(fake, (assertion_id,)) == ()


def test_unrelated_reference_is_unchanged_and_no_group_given_added() -> None:
    bridge = build_cited_extension_sources()
    ids = ("toda:174:r3r6:universal:(4.8)", "toda:174:r3r6:universal:(5.5)")
    body = project_reference_bodies(bridge.registry, ids)
    assert len(body) == 2
    assert project_reference_bodies(bridge.registry, ()) == ()
    assert project_reference_bodies(None, ids) == ()
    assert len(bridge.proof_links) == 2
    from proof import ProofRule, Relation
    assert all(link.step is not None and link.step.rule is ProofRule.GIVEN
               and not isinstance(link.step.conclusion, Relation)
               for link in bridge.proof_links)


def test_public_pi85_uses_registered_reference_without_duplicate_conclusion() -> None:
    from phase174_r3_r6_r2_prop44_lemma54.audit import inspect

    result = inspect()
    assert result["root_status"] == "complete"
    assert result["root_proven_steps"] == 16
    assert result["new_group_given"] == 0
    narrative = result["narrative"]
    assert "[R4] (4.8)." in narrative
    assert "[R7] (5.5)." in narrative
    assert r"$\Delta(\iota_{2n-1})=0$ と仮定する" in narrative
    assert r"$n\ge5$ に対し, $2\nu_n=E^{n-3}\nu'$." in narrative
    assert r"E^{2}:\pi_{6}^{3}\hookrightarrow \pi_{8}^{5}" in narrative
    assert r"|\pi_{8}^{5}|=2\cdot 4=8" in narrative
    root_lines = tuple(
        line for line in narrative.splitlines()
        if r"\pi_{8}^{5}" in line and r"\mathbb{Z}/8" in line and "=" in line
    )
    assert len(root_lines) == 1, root_lines
