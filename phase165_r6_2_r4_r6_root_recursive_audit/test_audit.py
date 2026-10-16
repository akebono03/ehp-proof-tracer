from dataclasses import dataclass
from audit import audit, inspect, same

@dataclass(frozen=True)
class Claim:
    value:int

class FakeBridge:
    proof_links=()
    class Registry:
        _assertions={}
    registry=Registry()

def test_type_sensitive_equality():
    assert same(Claim(1),Claim(1))
    assert not same(Claim(1),1)

def test_depth_limit():
    node,step=inspect(Claim(1),FakeBridge(),lambda x:(),0,(),{'remaining':4})
    assert node['state']=='DEPTH_LIMIT' and step is None

def test_cycle():
    node,step=inspect(Claim(1),FakeBridge(),lambda x:(),3,(Claim(1),),{'remaining':4})
    assert node['state']=='CYCLE' and step is None

def test_no_proposals():
    node,step=inspect(Claim(1),FakeBridge(),lambda x:(),2,(),{'remaining':4})
    assert node['state']=='NO_VERIFIED_DERIVATION' and node['candidate_count']==0

def test_node_budget():
    node,step=inspect(Claim(1),FakeBridge(),lambda x:(),2,(),{'remaining':0})
    assert node['state']=='NODE_BUDGET_EXCEEDED'
