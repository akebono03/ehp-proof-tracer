"""Isolated verification of the pure renderer without repository imports."""
from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
import types


def test_r10eb_typed_rendering_uses_series_stem_and_identity(monkeypatch):
    expression = types.ModuleType("expression")

    @dataclass(frozen=True)
    class Symbol:
        family: str
        index: int
        decoration: str | None = None

    @dataclass(frozen=True)
    class HomotopyElement:
        name: str
        dimension: int
        source: int
        target: int
        generator: Symbol

    @dataclass(frozen=True)
    class Composition:
        left: object
        right: object

    expression.HomotopyElement = HomotopyElement
    expression.Composition = Composition
    monkeypatch.setitem(sys.modules, "expression", expression)

    registry = types.ModuleType("phase169_r10b_registered_stable_family_binding.family_registry")

    @dataclass(frozen=True)
    class Family:
        family_id: int
        symbol_family: str
        display: str
        stem: int
        minimum_n: int
        latex: str

    families = [
        Family(4, "ν", "ν", 3, 4, r"\nu"),
        Family(9, "σ", "σ", 7, 8, r"\sigma"),
    ]

    def registered_family_of(item):
        if not isinstance(item, HomotopyElement):
            return None
        for f in families:
            expected_name = f.display + str(item.target).translate(
                str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
            )
            if (item.name == expected_name
                    and item.dimension == item.target
                    and item.source == item.target + f.stem
                    and item.target >= f.minimum_n
                    and item.generator == Symbol(f.symbol_family, item.target)):
                return f
        return None

    registry.registered_family_of = registered_family_of
    monkeypatch.setitem(sys.modules, registry.__name__, registry)
    source_path = Path(__file__).resolve().parents[1] / "display.py"
    spec = importlib.util.spec_from_file_location("r10eb_isolated_display", source_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    def element(f, n):
        return HomotopyElement(
            f.display + str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")),
            n, n + f.stem, n, Symbol(f.symbol_family, n),
        )

    nu = families[0]
    nu_cube = Composition(element(nu, 30),
                          Composition(element(nu, 33), element(nu, 36)))
    assert module.typed_stable_composition_power_latex(nu_cube) == r"\nu_{30}^{3}"
    bad = Composition(element(nu, 30), element(nu, 36))
    assert module.typed_stable_composition_power_latex(bad) is None
    sigma = families[1]
    sigma_cube = Composition(element(sigma, 11),
                             Composition(element(sigma, 18), element(sigma, 25)))
    assert module.typed_stable_composition_power_latex(sigma_cube) == r"\sigma_{11}^{3}"
