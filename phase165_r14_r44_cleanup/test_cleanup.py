from pathlib import Path
import ast

from cleanup import remove_r43_hook


def test_remove_only_r43_code():
    source = Path("toda_group_proof_narrative_renderer.py").read_text(encoding="utf-8")
    cleaned = remove_r43_hook(source)
    assert "phase165_r43_shared_narrative_enrichment" not in cleaned
    assert "enrich_common_narrative" not in cleaned
    ast.parse(cleaned)


def test_idempotent_removal():
    source = Path("toda_group_proof_narrative_renderer.py").read_text(encoding="utf-8")
    cleaned = remove_r43_hook(source)
    assert remove_r43_hook(cleaned) == cleaned


def test_r42_registry_provenance_preserved():
    source = Path("phase165_r14_r38_direct_registry.py").read_text(encoding="utf-8")
    assert "phase165_r42_source_inference" in source


def test_r42_typed_renderer_preserved():
    source = Path("toda_group_proof_generic_narrative_renderer.py").read_text(encoding="utf-8")
    assert "phase165_r42_generic_typed_prose" in source


def test_shared_renderer_imports():
    import toda_group_proof_narrative_renderer
    assert callable(toda_group_proof_narrative_renderer.render_toda_group_proof_narrative_markdown)
