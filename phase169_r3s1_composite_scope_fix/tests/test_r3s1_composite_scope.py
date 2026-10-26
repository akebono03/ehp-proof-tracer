"""Scope inheritance must not turn atomic, cited components into invalid composites."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r12_component_bridge import expand_cited_given_components
from phase168_r3_37c_reference_projection import project_reference_bodies


@pytest.fixture(scope="module")
def expanded_reference():
    return expand_cited_given_components(build_adopted_prop51_reference())


def test_atomic_children_with_inherited_scope_render_one_cited_fact(expanded_reference):
    registry = expanded_reference.registry
    parent_id = "toda:adopted:prop5.1:finite_dimensional"
    parent = registry.assertion(parent_id)
    for field_name in (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ):
        child = registry.assertion(parent_id + ":component:" + field_name)
        assert child.scope == parent.scope
        assert child.dependencies == (parent_id,)
        assert child.content == getattr(parent.content, field_name)
        lines = project_reference_bodies(registry, (child.assertion_id,))
        assert len(lines) == 1
        assert lines[0].startswith("$")


def test_atomic_child_reference_matches_parent_component_and_deduplicates(expanded_reference):
    registry = expanded_reference.registry
    parent_id = "toda:adopted:prop5.1:finite_dimensional"
    parent_lines = project_reference_bodies(registry, (parent_id,))
    assert len(parent_lines) == 4
    child_ids = tuple(parent_id + ":component:" + name for name in (
        "pi3_2_group_relation", "eta2_hopf_relation",
        "delta_iota5_relation", "higher_eta_group_relation",
    ))
    child_lines = project_reference_bodies(registry, child_ids)
    assert set(child_lines) == set(parent_lines)
    assert len(child_lines) == 4
    mixed = project_reference_bodies(registry, (parent_id,) + child_ids)
    assert mixed == parent_lines


def test_child_scope_rejects_content_without_matching_parent_field(expanded_reference):
    registry = expanded_reference.registry
    parent_id = "toda:adopted:prop5.1:finite_dimensional"
    child_id = parent_id + ":component:pi3_2_group_relation"
    wrong = replace(registry.assertion(child_id), content="not a source component")

    class InvalidRegistry:
        def assertion(self, identifier):
            if identifier == child_id:
                return wrong
            return registry.assertion(identifier)

    with pytest.raises(ValueError, match="scope is inconsistent"):
        project_reference_bodies(InvalidRegistry(), (child_id,))


def test_child_scope_rejects_incorrect_parent_dependency(expanded_reference):
    registry = expanded_reference.registry
    parent_id = "toda:adopted:prop5.1:finite_dimensional"
    child_id = parent_id + ":component:delta_iota5_relation"
    wrong = replace(registry.assertion(child_id), dependencies=("unrelated:assertion",))

    class InvalidRegistry:
        def assertion(self, identifier):
            if identifier == child_id:
                return wrong
            if identifier == "unrelated:assertion":
                return registry.assertion("toda:adopted:prop5.1:delta_iota5_relation")
            return registry.assertion(identifier)

    with pytest.raises(ValueError, match="scope is inconsistent"):
        project_reference_bodies(InvalidRegistry(), (child_id,))
