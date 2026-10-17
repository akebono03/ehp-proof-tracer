"""Ensure the actual R12-R14 source is importable rather than a namespace directory."""
from __future__ import annotations

from pathlib import Path

from phase165_r12_r14_kernel_closure import summarize_proof_ancestry


def test_r12_r14_ancestry_summary_is_imported_from_real_module() -> None:
    import phase165_r12_r14_kernel_closure as module

    assert callable(summarize_proof_ancestry)
    assert module.__file__ is not None
    assert Path(module.__file__).resolve() == (Path.cwd() / "phase165_r12_r14_kernel_closure.py").resolve()
