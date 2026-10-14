"""Focused source-transformation tests for R57-R4 safe retirement."""
import ast
from pathlib import Path

from install import clean_shadowed_public_renderer


def _sample():
    return (
        "def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(x):\n"
        "    return 'legacy ' + str(x)\n\n"
        "def render_toda_group_proof_narrative_markdown(x):\n"
        "    return _phase159_render_pi_n_plus_1_n_stable_transport_narrative(x)\n\n"
        "def render_toda_group_proof_narrative_markdown(x):\n"
        "    return 'common ' + str(x)\n\n"
        "_phase160_r7_previous_public_narrative_renderer = "
        "render_toda_group_proof_narrative_markdown\n\n"
        "def render_toda_group_proof_narrative_markdown(x):\n"
        "    return _phase160_r7_previous_public_narrative_renderer(x)\n"
    )


def test_r57_r4_removes_only_shadowed_definition_and_unreferenced_helper():
    changed, removed = clean_shadowed_public_renderer(_sample())
    assert len(removed) == 2
    assert changed.count("def render_toda_group_proof_narrative_markdown(") == 2
    assert "def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(" not in changed
    namespace = {}
    exec(compile(changed, "<test>", "exec"), namespace)
    assert namespace["render_toda_group_proof_narrative_markdown"](3) == "common 3"


def test_r57_r4_keeps_dedicated_helper_if_external_reference_exists():
    changed, removed = clean_shadowed_public_renderer(
        _sample(), external_helper_references=("consumer.py",),
    )
    assert len(removed) == 1
    assert "def _phase159_render_pi_n_plus_1_n_stable_transport_narrative(" in changed


def test_r57_r4_fails_closed_if_earlier_renderer_is_captured():
    import pytest
    source = _sample().replace(
        "def render_toda_group_proof_narrative_markdown(x):\n"
        "    return 'common ' + str(x)",
        "captured_old = render_toda_group_proof_narrative_markdown\n\n"
        "def render_toda_group_proof_narrative_markdown(x):\n"
        "    return 'common ' + str(x)",
    )
    with pytest.raises(RuntimeError, match="captured"):
        clean_shadowed_public_renderer(source)


def test_r57_r4_idempotent_cleanup():
    once, _ = clean_shadowed_public_renderer(_sample())
    twice, removed = clean_shadowed_public_renderer(once)
    # second historical definition may be captured into a live alias: fail-closed
    assert twice == once
    assert removed == ()
