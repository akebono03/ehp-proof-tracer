import pandas as pd

from expression import GeneratorSymbol, HomotopyElement
from models import GroupComponent
from phase166_r3ap_simple_identity_audit.audit import compare_simple_component


def _gen_rows():
    return pd.DataFrame([
        {"id": 1, "display": "ι", "kinds": 0, "k": 0, "n": 1},
        {"id": 2, "display": "η", "kinds": 0, "k": 1, "n": 2},
        {"id": 4, "display": "ν", "kinds": 0, "k": 3, "n": 4},
    ]).set_index("id")


def test_eta_simple_identity_confirmed():
    component = GroupComponent(id=0, order=2, generator="η2", element=[2], gen_coe=[1])
    typed = HomotopyElement("η₂", 2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    assert compare_simple_component(n=2, k=1, component=component, generator_rows=_gen_rows(), typed_generator=typed)["status"] == "confirmed"


def test_inconsistent_id_cannot_confirm():
    component = GroupComponent(id=0, order=2, generator="η2", element=[4], gen_coe=[1])
    typed = HomotopyElement("η₂", 2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    assert compare_simple_component(n=2, k=1, component=component, generator_rows=_gen_rows(), typed_generator=typed)["status"] == "mismatch"


def test_missing_ids_are_unverifiable():
    component = GroupComponent(id=0, order=2, generator="η2", element=[], gen_coe=[1])
    typed = HomotopyElement("η₂", 2, source=3, target=2, generator=GeneratorSymbol("η", 2))
    assert compare_simple_component(n=2, k=1, component=component, generator_rows=_gen_rows(), typed_generator=typed)["status"] == "unverifiable"
