from phase177_r15_finite_cyclic_delta_injective_public.installer import ANCHOR, PATCH, proposed_source

import pytest


def test_only_intended_hook():
    source = 'def shared_expansion_provider(bridge, proof_target=None):\n    extra_providers = ()\n' + ANCHOR + '    return extra_providers\n'
    assert proposed_source(source) == source.replace(ANCHOR,PATCH+ANCHOR)
    with pytest.raises(ValueError):
        proposed_source(source.replace(ANCHOR,PATCH+ANCHOR))
    with pytest.raises(ValueError):
        proposed_source(source.replace('shared_expansion_provider','another_function'))
