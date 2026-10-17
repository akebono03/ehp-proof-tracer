from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import TodaPrimaryGroup
from phase165_r12_r2_quotient_rules import CyclicStructureStatement
from phase165_r12_r26_map_candidates import expand_cited_eta_quotient
from toda_rules import toda_eta_family_definition_statement


def test_r27_tex_eta_name_expands_with_exact_target_generator():
    canonical = toda_eta_family_definition_statement(3).element
    tex = HomotopyElement(
        name="η_3", dimension=canonical.dimension, source=canonical.source,
        target=canonical.target, generator=canonical.generator,
    )
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), tex, 2)
    options = expand_cited_eta_quotient(goal, 1)
    assert len(options) == 1
    quotient, source = options[0].subgoals
    assert quotient.target_generator == tex
    assert source.generator == toda_eta_family_definition_statement(2).element


def test_r27_unicode_eta_name_still_works():
    canonical = toda_eta_family_definition_statement(3).element
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), canonical, 2)
    options = expand_cited_eta_quotient(goal, 1)
    assert len(options) == 1
    assert options[0].subgoals[0].target_generator == canonical


def test_r27_invalid_names_and_identity_fields_fail_closed():
    canonical = toda_eta_family_definition_statement(3).element
    group = TodaPrimaryGroup(4, 3)
    for name in ("eta_3", "η_4", "η₄", "other"):
        wrong = HomotopyElement(
            name=name, dimension=canonical.dimension, source=canonical.source,
            target=canonical.target, generator=canonical.generator,
        )
        assert expand_cited_eta_quotient(CyclicStructureStatement(group, wrong, 2), 1) == ()
    wrong_symbol = HomotopyElement(
        name="η_3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="ν", index=3),
    )
    assert expand_cited_eta_quotient(CyclicStructureStatement(group, wrong_symbol, 2), 1) == ()


def test_r27_uncited_source_and_unrelated_goal_still_fail():
    canonical = toda_eta_family_definition_statement(3).element
    tex = HomotopyElement(name="η_3", dimension=3, source=4, target=3, generator=canonical.generator)
    goal = CyclicStructureStatement(TodaPrimaryGroup(4, 3), tex, 2)
    assert expand_cited_eta_quotient(goal, 0) == ()
    assert expand_cited_eta_quotient(goal, 2) == ()
    assert expand_cited_eta_quotient(CyclicStructureStatement(TodaPrimaryGroup(5, 3), tex, 2), 1) == ()
