from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup
from toda_rules import Toda45IsomorphismStatement
from phase168_r3_27_typed_statement_projection import typed_sentence


def test_concrete_toda45_iso_is_rendered():
    statement = Toda45IsomorphismStatement(
        map=TodaIteratedSuspensionMap(
            exponent=1,
            source_group=TodaPrimaryGroup(4, 3),
            target_group=TodaPrimaryGroup(5, 4),
        )
    )
    sentence = typed_sentence(statement, None)
    assert sentence == r"$E: \pi_{4}^{3}\to \pi_{5}^{4}$ は同型である."


def test_non_concrete_toda45_statement_is_not_guessed():
    from expression import ScalarSymbol
    statement = Toda45IsomorphismStatement(
        map=TodaIteratedSuspensionMap(
            exponent=ScalarSymbol("r"),
            source_group=TodaPrimaryGroup(4, 3),
            target_group=TodaPrimaryGroup(5, 4),
        )
    )
    assert typed_sentence(statement, None) is None
