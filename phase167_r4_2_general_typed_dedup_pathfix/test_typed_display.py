from types import SimpleNamespace
from expression import HomotopyElement, IteratedSuspension
from homotopy_groups import TodaPrimaryGroup,TodaSuspensionMap
from toda_group_proof_narrative_argument_body_renderer import _phase167_r4_2_typed_display_equality_key as key
from phase165_r14_r14_diagonal_and_prop42 import GeneratorSuspension

def test_typed_display_dedup_any_generator_family():
    from expression import GeneratorSymbol
    for family in ('eta_test','nu_test','sigma_test'):
        s=HomotopyElement(name='a',dimension=4,source=5,target=4,generator=GeneratorSymbol(family=family,index=4))
        t=HomotopyElement(name='b',dimension=5,source=6,target=5,generator=GeneratorSymbol(family=family,index=5))
        mp=TodaSuspensionMap(TodaPrimaryGroup(5,4),TodaPrimaryGroup(6,5))
        assert key(GeneratorSuspension(mp,s,t))==key(SimpleNamespace(element=t,iterated_suspension=IteratedSuspension(s,1)))
        assert key(SimpleNamespace(element=t,iterated_suspension=IteratedSuspension(s,0))) is None

def test_typed_display_keys_distinguish_different_generators():
    from expression import GeneratorSymbol
    s=HomotopyElement(name='a',dimension=4,source=5,target=4,generator=GeneratorSymbol(family='x',index=4))
    t=HomotopyElement(name='b',dimension=5,source=6,target=5,generator=GeneratorSymbol(family='x',index=5))
    u=HomotopyElement(name='c',dimension=5,source=6,target=5,generator=GeneratorSymbol(family='y',index=5))
    mp=TodaSuspensionMap(TodaPrimaryGroup(5,4),TodaPrimaryGroup(6,5))
    assert key(GeneratorSuspension(mp,s,t))!=key(GeneratorSuspension(mp,s,u))
