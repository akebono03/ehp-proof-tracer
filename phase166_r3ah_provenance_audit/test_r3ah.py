from phase166_r3ah_provenance_audit.audit import CASES, contained_relations
from proof import Relation
from homotopy_groups import TodaPrimaryGroup, FiniteCyclicGroup
from expression import HomotopyElement, GeneratorSymbol


def test_scope_preserves_three_stems_and_nine_targets():
    assert CASES == ((2, 4), (2, 5), (2, 6), (3, 5), (3, 6), (3, 7),
                     (7, 9), (7, 10), (7, 11))


def test_relation_extraction_does_not_create_new_claims():
    generator = HomotopyElement(name="η_4", dimension=4, source=6, target=4,
                                generator=GeneratorSymbol(family="η", index=4))
    relation = Relation(TodaPrimaryGroup(6, 4), FiniteCyclicGroup(2, generator))
    assert contained_relations((relation,)) == (relation,)
    assert contained_relations(()) == ()
