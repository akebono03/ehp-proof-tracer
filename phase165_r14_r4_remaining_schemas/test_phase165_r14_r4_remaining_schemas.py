import pytest
from phase165_r14_r4_remaining_schemas import (
    StableStem, StableIdentity, Toda51TypedClaim,
    instantiate_remaining_toda51_clause,
)

def test_all_four_remaining_source_keys_have_typed_instances():
    values = (
        instantiate_remaining_toda51_clause("pi_i_n_zero", i=2, n=3),
        instantiate_remaining_toda51_clause("negative_stem_zero", k=-1),
        instantiate_remaining_toda51_clause("stable_zero_stem_cyclic"),
        instantiate_remaining_toda51_clause("stable_identity", n=3),
    )
    assert len({v.key for v in values}) == 4
    assert all(isinstance(v, Toda51TypedClaim) for v in values)
    assert all(v.source_locator == "(5.1)" and v.proof_eligible is False for v in values)

@pytest.mark.parametrize("i,n", [(3,3), (4,3), (-1,3), (0,0), (2,True)])
def test_vanishing_range_rejected(i,n):
    with pytest.raises((ValueError,TypeError)):
        instantiate_remaining_toda51_clause("pi_i_n_zero", i=i, n=n)

@pytest.mark.parametrize("k", [0,1,True,1.5])
def test_negative_stem_bounds_rejected(k):
    with pytest.raises((ValueError,TypeError)):
        instantiate_remaining_toda51_clause("negative_stem_zero", k=k)

def test_stable_zero_stem_has_no_free_indices():
    with pytest.raises(ValueError):
        instantiate_remaining_toda51_clause("stable_zero_stem_cyclic", n=2)

def test_stable_suspension_is_symbolic_and_has_range():
    claim=instantiate_remaining_toda51_clause("stable_identity", n=3)
    assert isinstance(claim.assertion, StableIdentity)
    assert claim.assertion.source_dimension == 3
    with pytest.raises(ValueError):
        instantiate_remaining_toda51_clause("stable_identity", n=0)

def test_negative_stem_preserves_both_components():
    claim=instantiate_remaining_toda51_clause("negative_stem_zero", k=-1)
    assert len(claim.assertion)==2
    assert claim.assertion[0].lhs==StableStem(-1)
    assert claim.assertion[1].lhs==StableStem(-1,2)

def test_proof_promotion_is_rejected():
    valid=instantiate_remaining_toda51_clause("stable_zero_stem_cyclic")
    with pytest.raises(ValueError):
        Toda51TypedClaim(valid.key, valid.assertion, (), proof_eligible=True)
