"""R10E5-R2: reviewed provider call keeps its available source context."""
from __future__ import annotations

from pathlib import Path

from phase169_r10e5_composite_generator_image.patch import OLD, NEW, transform


def test_r10e5r2_anchor_matches_reviewed_provider_and_retains_available():
    expected = "        options.extend(expand_cited_stable_family(goal, tuple(available)))"
    assert expected in OLD
    assert expected in NEW
    fixture = (
        "def shared_expansion_provider(bridge):\n"
        "    def expand(goal):\n"
        + OLD + "\n"
        "        return ()\n"
        "    return expand\n"
    ).encode("utf-8")
    updated, function = transform(fixture)
    assert NEW in updated.decode("utf-8")
    assert expected in function
    assert "options.extend(expand_composite_generator_image(goal))" in function


def test_r10e5r2_live_provider_uses_preserved_available_context():
    root = Path(__file__).resolve().parents[2]
    provider = (root / "phase165_r52_r9_shared_math.py").read_text(
        encoding="utf-8-sig",
    )
    assert NEW in provider.replace("\r\n", "\n")
    assert "options.extend(expand_cited_stable_family(goal, tuple(available)))" in provider
