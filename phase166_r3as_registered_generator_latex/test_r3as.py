"""Only generator presentation, never proof search."""
from pathlib import Path
import pandas as pd
from phase166_r3aj_structured_generator import structured_generator_from_ids
from toda_human_readable_renderer import render_toda_public_group_generator_latex

DATA = Path(__file__).resolve().parent.parent / "data" / "HyoujiGen.csv"

def test_mu_3_11_closes_single_subscript():
    expr = structured_generator_from_ids(ids=[103], start_dimension=11, generator_csv=DATA)
    assert render_toda_public_group_generator_latex(expr) == r"\mu_{3,11}"

def test_k_one_uses_registered_tex():
    expr = structured_generator_from_ids(ids=[111], start_dimension=11, generator_csv=DATA)
    assert render_toda_public_group_generator_latex(expr) == r"K_{1}"

def test_exceptional_registered_delta_and_beta_bars():
    delta = structured_generator_from_ids(ids=[64], start_dimension=20, generator_csv=DATA)
    beta = structured_generator_from_ids(ids=[65], start_dimension=20, generator_csv=DATA)
    assert render_toda_public_group_generator_latex(delta) == r"\Delta(\eta_{41})"
    assert render_toda_public_group_generator_latex(beta) == r"\bar{\bar{\beta}}"

def test_stable_8stem_and_exceptional_one_suspension():
    nu_bar = structured_generator_from_ids(ids=[11], start_dimension=12, generator_csv=DATA)
    epsilon = structured_generator_from_ids(ids=[10], start_dimension=12, generator_csv=DATA)
    nu_prime = structured_generator_from_ids(ids=[3], start_dimension=4, generator_csv=DATA)
    assert render_toda_public_group_generator_latex(nu_bar) == r"\bar{\nu}_{12}"
    assert render_toda_public_group_generator_latex(epsilon) == r"\varepsilon_{12}"
    assert render_toda_public_group_generator_latex(nu_prime) == r"E\nu'"
