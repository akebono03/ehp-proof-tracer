"""R3S tests: typed composite Reference projection without proof/search changes."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_4_link_bridge import build_linked_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from phase168_r3_37c_reference_projection import project_reference_bodies


def test_composite_prop51_reference_projects_registered_atomic_fields():
    bridge = build_adopted_prop51_reference()
    assertion_id = "toda:adopted:prop5.1:finite_dimensional"
    bodies = project_reference_bodies(bridge.registry, (assertion_id,))
    assert len(bodies) == 4
    assert any(r"\pi_{3}^{2}" in line and r"\eta_{2}" in line for line in bodies)
    assert any(r"H" in line and r"\eta_{2}" in line and r"\iota_{3}" in line for line in bodies)
    assert any(r"\Delta" in line and r"\iota_{5}" in line for line in bodies)
    assert any(r"\pi_{n+1}^{n}" in line and r"\eta_{n}" in line and r"n\ge4" in line
               for line in bodies)


def test_compound_reference_projection_is_deduplicated_and_citation_scoped():
    bridge = build_adopted_prop51_reference()
    assertion_id = "toda:adopted:prop5.1:finite_dimensional"
    result = project_reference_bodies(bridge.registry, (assertion_id, assertion_id))
    assert len(result) == len(set(result)) == 4
    assert project_reference_bodies(bridge.registry, ()) == ()


def test_composite_assertion_scope_mismatch_rejected():
    bridge = build_adopted_prop51_reference()
    identifier = "toda:adopted:prop5.1:finite_dimensional"
    original = bridge.registry.assertion(identifier)

    @dataclass(frozen=True)
    class InvalidAssertion:
        content: object
        scope: tuple

    class FakeRegistry:
        def assertion(self, key):
            assert key == identifier
            return InvalidAssertion(original.content,
                                    ("typed_composite_fields", ("no_such_field", "other")))

    with pytest.raises(ValueError, match="scope is inconsistent"):
        project_reference_bodies(FakeRegistry(), (identifier,))


def test_real_pi53_reference_contains_composite_source_without_new_citation():
    bridge = build_shared_typed_bridge()
    contexts = []
    result = search_group_from_registered_goal(n=3, k=2, bridge=bridge,
                                               context_sink=contexts.append)
    assert result.status is ProofSearchStatus.COMPLETE
    assert contexts
    model = build_linked_proof_narrative_model(result, contexts[-1])
    citations = tuple(citation for citation in model.citations
                      if (citation.reference.locator or citation.reference.label)
                      == "Proposition 5.1")
    assert len(citations) == 1
    citation = citations[0]
    assert len(citation.statement_bodies) == 4
    markdown = render_model_backed_narrative_markdown(result, model)
    assert f"[R{citation.number}] Proposition 5.1" in markdown
    for body in citation.statement_bodies:
        assert body in markdown
    assert not any((c.reference.locator or c.reference.label) == "(5.1)"
                   for c in model.citations)
