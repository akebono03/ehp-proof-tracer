"""Generic formatter and observational contracts; no fabricated proof leaves."""
from types import SimpleNamespace

import pytest

from homotopy_groups import (TodaPrimaryGroup, TodaSuspensionMap, TodaDeltaMap,
                             TodaHopfInvariantMap, FiniteCyclicGroup)
from expression import HomotopyElement
from map_property_rules import ImageZeroStatement
from phase176_r3r45_direct_premise_audit.apply import TARGET, updated_source
from phase176_r3r45_direct_premise_audit.audit import candidate_records, nonzero_presentation
from proof import Relation
from web_group_proof_common import _group_proof_statement_latex


@pytest.mark.parametrize('mapping,symbol',[
    (TodaSuspensionMap(TodaPrimaryGroup(7,2),TodaPrimaryGroup(8,3)), 'E'),
    (TodaSuspensionMap(TodaPrimaryGroup(9,5),TodaPrimaryGroup(10,6)), 'E'),
    (TodaHopfInvariantMap(TodaPrimaryGroup(9,4),TodaPrimaryGroup(9,7)), 'H'),
    (TodaDeltaMap(TodaPrimaryGroup(9,7),TodaPrimaryGroup(7,3)), r'\Delta'),
])
def test_zero_map_latex(mapping,symbol):
    latex, fallback = _group_proof_statement_latex(ImageZeroStatement(mapping))
    assert fallback is None
    assert latex.startswith(symbol+':')
    assert r'\xrightarrow{0}' in latex
    for group in (mapping.source_group,mapping.target_group):
        assert rf'\pi_{{{group.group_dimension}}}^{{{group.sphere_dimension}}}' in latex


def test_display_patch_idempotent_and_rejects_unreviewed_source():
    raw = TARGET.read_bytes()
    assert updated_source(raw)==raw
    with pytest.raises(ValueError):
        updated_source(raw+b'\n# unreviewed modification\n')


def test_candidate_records_keep_all_siblings_in_order():
    item=SimpleNamespace(rule=SimpleNamespace(name='candidate'),subgoals=('first','last'))
    assert candidate_records((item,))==[{'rule':'candidate','premises':["'first'","'last'"]}]


def test_nonzero_presentation_is_shape_check_only():
    group = TodaPrimaryGroup(8,5)
    generator = HomotopyElement('a',5,8,5)
    assert nonzero_presentation(Relation(group,FiniteCyclicGroup(8,generator)),group)
    assert not nonzero_presentation(Relation(group,FiniteCyclicGroup(1,generator)),group)
    assert not nonzero_presentation(Relation(group,FiniteCyclicGroup(8,generator)),TodaPrimaryGroup(9,5))
