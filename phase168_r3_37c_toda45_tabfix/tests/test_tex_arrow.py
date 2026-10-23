from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup
from toda_rules import Toda45IsomorphismStatement
from phase168_r3_27_typed_statement_projection import typed_sentence


def test_toda45_concrete_arrow_is_literal_latex():
    statement = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=1, source_group=TodaPrimaryGroup(4, 3),
        target_group=TodaPrimaryGroup(5, 4)))
    result = typed_sentence(statement, None)
    assert result == r"$E: \pi_{4}^{3}\to \pi_{5}^{4}$ は同型である."
    assert "\t" not in result
