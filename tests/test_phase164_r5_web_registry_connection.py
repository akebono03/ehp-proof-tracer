"""Focused Web integration for the Phase 164 R5 registry-backed pi_5^3 proof."""
from pathlib import Path

import pytest

from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof
from proof import ProofRule
from web_group_proof import build_standard_web_group_proof_view


@pytest.fixture(scope="module")
def registry_web_proof():
    return build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_registry_web_proof_has_inferred_group_root(registry_web_proof):
    replay, narrative = registry_web_proof
    root = replay.root_step
    assert root.rule is ProofRule.INFERENCE
    assert len(root.premises) == 3
    assert all(step.rule is ProofRule.INFERENCE for step in root.premises)
    assert replay.source_entry.phase == "164 R5"
    assert "## 証明" in narrative
    assert "### 群構造" in narrative
    assert narrative.count("□") == 1


def test_registry_isomorphism_is_an_actual_group_premise(registry_web_proof):
    replay, _ = registry_web_proof
    root = replay.root_step
    isomorphism = root.premises[1]
    assert isomorphism.rule is ProofRule.INFERENCE
    assert len(isomorphism.premises) == 2
    assert isomorphism.premises[0].rule is ProofRule.INFERENCE
    assert isomorphism.premises[1].rule is ProofRule.INFERENCE


def test_proof_markdown_cites_toda_and_ends_in_group_relation(registry_web_proof):
    _, markdown = registry_web_proof
    assert "Proposition 5.1" in markdown
    assert "(5.3)" in markdown
    assert "(5.2)" in markdown
    assert "同型" in markdown
    assert "pi_{5}^{3}" in markdown or "pi_{5}^3" in markdown


def test_group_query_web_narrative_is_phase164():
    view = build_standard_web_group_proof_view(3, 2, max_depth=2, mode="narrative")
    assert view.phase == "164 R5"
    assert view.key == "phase164-r5-registry-backed-pi5-3-web"
    assert view.mode == "narrative"
    assert view.rendered_lines
    content = "\n".join(segment.value for line in view.rendered_lines for segment in line.segments)
    assert "Proposition 5.1" in content
    assert "(5.3)" in content
    assert "群構造" in content or any(line.kind == "heading" and line.prefix == "群構造" for line in view.rendered_lines)


def test_invalid_depth_rejected():
    for invalid in (-1, True, "2"):
        with pytest.raises((ValueError, TypeError)):
            build_phase164_r5_web_pi5_3_proof(max_depth=invalid)


def test_manifest_must_exist(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError, match="manifest missing"):
        build_phase164_r5_web_pi5_3_proof(max_depth=2)


def test_non_target_web_path_does_not_load_r5(monkeypatch):
    import phase164_r5_web_registry_connection as r5
    def forbidden(**kwargs):
        raise AssertionError("R5 must not run outside pi5_3 narrative")
    monkeypatch.setattr(r5, "build_phase164_r5_web_pi5_3_proof", forbidden)
    # The trace view for pi5_3 remains the existing Web code path.
    view = build_standard_web_group_proof_view(3, 2, max_depth=0, mode="trace")
    assert view.mode == "trace"
    assert view.phase != "164 R5"
