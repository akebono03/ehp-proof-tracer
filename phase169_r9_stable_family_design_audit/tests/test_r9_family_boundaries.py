"""Focused audit tests, independent of EHP application imports."""
from __future__ import annotations

from pathlib import Path

from phase169_r9_stable_family_design_audit.audit import (
    family_name, family_transport_shape, read_family_rows,
    stable_group_transport_allowed,
)


ROOT = Path(__file__).resolve().parents[2]


def _rows():
    return {row["id"]: row for row in read_family_rows(ROOT / "data" / "HyoujiGen.csv")}


def test_eta_family_minimum_is_not_freudenthal_stable_range():
    eta = _rows()[2]
    assert eta["kinds"] == 0 and eta["n_min"] == 2 and eta["k"] == 1
    assert family_transport_shape(eta, 2, 1)
    assert not stable_group_transport_allowed(eta, 2, 1)
    assert stable_group_transport_allowed(eta, 3, 4)


def test_nu_and_sigma_have_separate_family_minimum_and_stability_start():
    rows = _rows()
    assert family_transport_shape(rows[4], 4, 3)
    assert not stable_group_transport_allowed(rows[4], 4, 3)
    assert stable_group_transport_allowed(rows[4], 5, 3)
    assert not stable_group_transport_allowed(rows[9], 8, 1)
    assert stable_group_transport_allowed(rows[9], 9, 1)


def test_nonfamily_rows_are_not_accepted_as_stable_series():
    nu_prime = _rows()[3]
    assert nu_prime["kinds"] == 1
    assert family_name(nu_prime, 5) is None
    assert not family_transport_shape(nu_prime, 5, 2)


def test_negative_r_and_dimensions_below_minimum_are_rejected():
    eta = _rows()[2]
    assert not family_transport_shape(eta, 3, -1)
    assert family_name(eta, 1) is None
    assert not family_transport_shape(eta, 1, 5)
