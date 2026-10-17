from homotopy_groups import TodaPrimaryGroup, TodaSuspensionMap
from map_property_rules import ImageWholeStatement, SurjectiveMapStatement, whole_image_implies_surjective_inference_rule
from phase165_r12_r12_ehp_consequences import expand_ehp_exactness_consequences
from phase165_r12_r30_ehp_surjectivity import expand_ehp_whole_image
from phase165_r14_r6_generic_iso import MapSurjective
from phase165_r8_rule_provider import create_rule_expansion_provider


def test_r30_ehp_whole_image_builds_proof_subgoal():
    e = TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3))
    goal = ImageWholeStatement(e)
    found = expand_ehp_whole_image(goal)
    assert len(found) == 1
    assert found[0].subgoals == (MapSurjective(e),)
    assert len(expand_ehp_exactness_consequences(found[0].subgoals[0])) == 1


def test_r30_surjectivity_rule_already_expands_to_whole_image():
    e = TodaSuspensionMap(TodaPrimaryGroup(3, 2), TodaPrimaryGroup(4, 3))
    goal = SurjectiveMapStatement(e)
    options = create_rule_expansion_provider((whole_image_implies_surjective_inference_rule(),))(goal)
    assert len(options) == 1
    assert options[0].subgoals == (ImageWholeStatement(e),)


def test_r30_non_suspension_map_not_accepted():
    from expression import MapSymbol
    assert expand_ehp_whole_image(ImageWholeStatement(MapSymbol("f"))) == ()
    assert expand_ehp_whole_image(SurjectiveMapStatement(MapSymbol("f"))) == ()


def test_r30_invalid_ehp_indices_do_not_create_exactness():
    e = TodaSuspensionMap(TodaPrimaryGroup(5, 2), TodaPrimaryGroup(6, 4))
    assert len(expand_ehp_whole_image(ImageWholeStatement(e))) == 1
    assert expand_ehp_exactness_consequences(MapSurjective(e)) == ()
