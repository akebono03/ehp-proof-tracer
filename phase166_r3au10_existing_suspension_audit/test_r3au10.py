from pathlib import Path
from phase166_r3au10_existing_suspension_audit.audit import inspect_code
from expression import Composition, HomotopyElement, IteratedSuspension
from phase166_r3aj_structured_generator import _base_element, structured_generator_from_ids
import pandas as pd

def test_r3au10_base_suspension():
    row={"display":"ξ","n":5,"k":2,"kinds":1,"latex":r"\\xi"}
    expr=_base_element(row,7)
    assert isinstance(expr,IteratedSuspension)
    assert expr.exponent==2
    assert expr.target==7 and expr.source==9

def test_r3au10_composition_dimensions(tmp_path):
    master=tmp_path/"HyoujiGen.csv"
    pd.DataFrame([
        {"id":2,"display":"η","n":2,"k":1,"kinds":0,"latex":r"\\eta"},
        {"id":3,"display":"η","n":2,"k":1,"kinds":0,"latex":r"\\eta"}
    ]).to_csv(master,index=False)
    expr=structured_generator_from_ids(ids=[2,3],start_dimension=3,generator_csv=master)
    assert isinstance(expr,Composition)
    assert expr.is_type_compatible()

def test_r3au10_current_code_detected():
    result=inspect_code(Path.cwd())
    assert result["structured_generator_from_ids_present"]
    assert result["goal_uses_gen_coe"]
    assert result["goal_constructs_sum"]
