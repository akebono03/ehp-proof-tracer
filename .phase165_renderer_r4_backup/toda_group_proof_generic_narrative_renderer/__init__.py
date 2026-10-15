"""Compatibility imports only. This package contains no Narrative renderer."""
from __future__ import annotations
from importlib import import_module

_PUBLIC = {
    "render_toda_partial_proof_narrative_markdown": "render_toda_partial_proof_narrative_markdown",
    "render_toda_group_proof_generic_narrative_markdown": "render_toda_group_proof_narrative_markdown",
}


def __getattr__(name: str):
    if name in _PUBLIC:
        return getattr(import_module("toda_group_proof_narrative_renderer"), _PUBLIC[name])
    return getattr(import_module("toda_group_proof_narrative_shared_components"), name)


def __dir__():
    helpers = import_module("toda_group_proof_narrative_shared_components")
    return sorted(set(globals()) | set(dir(helpers)) | set(_PUBLIC))
