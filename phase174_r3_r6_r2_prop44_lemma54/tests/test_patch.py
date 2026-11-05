"""Off-repository guarded-patch tests; no production paths are mutated."""
from __future__ import annotations

import ast

import pytest

from phase174_r3_r6_r2_prop44_lemma54.patch import (
    PROP44_CLASS,
    RULES,
    patch_injectivity,
    patch_literature,
    patch_projection,
    patch_renderer,
    patch_shared,
    replace_one,
)


def test_prop44_has_no_implicit_hopf_fibration_dimensions() -> None:
    ast.parse("from dataclasses import dataclass\n" + PROP44_CLASS)
    assert "preceding_hopf_fibration_dimensions" not in PROP44_CLASS
    assert "source_condition" in PROP44_CLASS
    assert "Lemma 5.4" in RULES
    assert "premises[1].premises[0].rule is ProofRule.GIVEN" in RULES


def test_exact_replacement_is_single_and_fail_closed() -> None:
    assert replace_one("a x b", "x", "Y", label="fixture") == "a Y b"
    with pytest.raises(ValueError):
        replace_one("x x", "x", "Y", label="duplicate")
    with pytest.raises(ValueError):
        replace_one("missing", "x", "Y", label="absent")


def test_old_provider_and_new_lemma_route_are_replaced_together() -> None:
    source = "\n".join((
        "def build_shared_typed_bridge():",
        "    if True:",
        "        sources = sources + (build_cited_extension_sources(),)",
        "def shared_expansion_provider():",
        "    def expand(goal):",
        "        from phase169_r4b_prop44_injectivity.rule import expand_cited_prop44_injectivity",
        "        options.extend(expand_cited_prop44_injectivity(goal, tuple(available)))",
        "def search_shared_group_goal():",
        "    if True:",
        "        if pi74_connection is not None:",
        "            bridge, citing_assertion_id, expansion_provider = pi74_connection",
        "    assertions = tuple(bridge.registry._assertions.values())",
        "",
    ))
    updated = patch_shared(source)
    ast.parse(updated)
    assert updated.count("build_cited_preprop44_splitting()") == 1
    assert updated.count("attach_earlier_verified_lemma54") == 2
    assert updated.count("expand_cited_lemma54_hopf(goal, tuple(available))") == 1
    assert updated.count("conditional_prop44 = expand_cited_prop44_injectivity") == 1
    with pytest.raises(ValueError):
        patch_shared(updated)


def test_conditional_rule_full_units_are_parseable() -> None:
    original = """from __future__ import annotations

def _is_hopf_four_suspension(goal):
    return True

def prop44_hopf_four_injectivity_rule(goal):
    return None

def expand_cited_prop44_injectivity(goal, available):
    return ()
"""
    revised = patch_injectivity(original)
    ast.parse(revised)
    assert revised.count("def prop44_hopf_four_injectivity_rule") == 1
    assert revised.count("def expand_cited_prop44_injectivity") == 1
    assert revised.count("premises[1].premises[0].rule is ProofRule.GIVEN") == 1


def test_reference_projection_does_not_mix_proposition_with_prelude() -> None:
    source = "\n".join((
        "def project_reference_bodies():",
        "    from phase165_r52_r27_r5_literature import Toda52UniversalStatement, TodaProp44UniversalStatement",
        "    if True:",
        "            elif (type(statement) is TodaProp44UniversalStatement",
        "                  and statement == TodaProp44UniversalStatement()",
        "                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):",
        "                sentence = 'condition'",
        "            elif isinstance(statement, TodaProp42GeneralExactnessStatement):",
        "                sentence = 'exact'",
        "",
    ))
    updated = patch_projection(source)
    assert "statement.preceding_hopf_fibration_dimensions" not in updated
    assert "TodoPreProp44" not in updated
    assert "TodaPreProp44SplittingStatement" in updated
    # This string fixture is not a complete if/elif chain; check unit separately.
    assert updated.count("Chapter IV") == 0


def test_renderer_removes_only_manufactured_hopf_invariant_of_h() -> None:
    source = "\n".join((
        "def render_model_backed_narrative_markdown():",
        "    if True:",
        "                    # R4F: the source paragraph immediately BEFORE Prop. 4.4",
        "                    application = 'unverified Hopf invariant'",
        '                        lines.extend((application, ""))',
        "    return lines",
        "",
    ))
    updated = patch_renderer(source)
    assert "unverified Hopf invariant" not in updated
    assert "return lines" in updated
