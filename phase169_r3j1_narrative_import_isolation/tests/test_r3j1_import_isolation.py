"""Focused import-route regression after split legacy-adapter pytest collection."""
from __future__ import annotations

import importlib
from pathlib import Path


def test_r3j1_canonical_ehp_module_origin():
    repo = Path(__file__).resolve().parents[2]
    module = importlib.import_module("phase165_r14_r5_ehp_connection")
    assert Path(module.__file__).resolve() == (repo / "phase165_r14_r5_ehp_connection.py").resolve()


def test_r3j1_both_terminal_adapters_resolve_from_canonical_module():
    module = importlib.import_module("phase165_r14_r5_ehp_connection")
    assert callable(module.expand_registered_ehp_terminal_goal)
    assert callable(module.expand_cited_ehp_terminal_goal)
