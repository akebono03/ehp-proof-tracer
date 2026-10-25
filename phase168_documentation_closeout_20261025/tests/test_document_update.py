"""Documentation-only safety checks; tested on temporary fixtures, not real repo."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from phase168_documentation_closeout_20261025 import update_docs as docs


def create_fixture(root: Path) -> dict[str, bytes]:
    source: dict[str, bytes] = {}
    titles = {
        "README.md": (docs.PACKAGE / "payload" / "README.before.md").read_text(encoding="utf-8"),
        "docs/design.md": "# EHP Proof Tracer 設計\n",
        "docs/development_log.md": "# EHP Proof Tracer 開発記録\n",
        "docs/roadmap.md": "# EHP Proof Tracer ロードマップ\n",
        "docs/proof_records.md": "# EHP Proof Tracer — 証明記録\n",
    }
    for name in docs.DOCS:
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if name == "README.md":
            content = titles[name]
        else:
            anchors = "\n".join(
                anchor for anchor in docs.REQUIRED_HISTORICAL_ANCHORS[name]
                if anchor != docs.ROADMAP_OLD_HEADING
            )
            content = titles[name] + anchors + "\n" + ("日本語の歴史的開発記録を保持する。\n" * 600)
            if name == "docs/roadmap.md":
                content += docs.ROADMAP_OLD_HEADING + "\n\n" + docs.ROADMAP_LAST_LINE + "\n"
        source[name] = content.encode("utf-8")
        target.write_bytes(source[name])
    return source


def bind_temp_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(docs, "ROOT", tmp_path)
    monkeypatch.setattr(docs, "OUTPUT", tmp_path / "phase168_documentation_closeout_20261025" / "output")
    monkeypatch.setattr(docs, "BACKUPS", docs.OUTPUT / "backups")
    monkeypatch.setattr(docs, "FULL", docs.OUTPUT / "full_files")
    monkeypatch.setattr(docs, "MANIFEST", docs.OUTPUT / "manifest.json")


def test_all_five_complete_docs_generated_and_reusable(tmp_path, monkeypatch):
    bind_temp_root(tmp_path, monkeypatch)
    original = create_fixture(tmp_path)
    docs.apply()
    docs.verify()
    manifest = json.loads(docs.MANIFEST.read_text(encoding="utf-8"))
    assert set(manifest["files"]) == set(docs.DOCS)
    for name in docs.DOCS:
        updated = (docs.ROOT / name).read_bytes()
        assert updated == (docs.FULL / name).read_bytes()
        assert original[name] == (docs.BACKUPS / name).read_bytes()
        assert docs.sha(updated) == manifest["files"][name]["after_sha256"]
        if name != "README.md":
            assert "歴史的開発記録" in updated.decode("utf-8")
    docs.apply()
    docs.verify()
    assert (docs.OUTPUT / "phase168_documentation_full_files_review.zip").is_file()
    docs.restore()
    for name in docs.DOCS:
        assert (docs.ROOT / name).read_bytes() == original[name]
    docs.apply()
    docs.verify()


def test_edited_original_is_not_silently_overwritten(tmp_path, monkeypatch):
    bind_temp_root(tmp_path, monkeypatch)
    original = create_fixture(tmp_path)
    path = tmp_path / "docs" / "design.md"
    path.write_text("# EHP Proof Tracer 設計\nmanual rewrite", encoding="utf-8")
    with pytest.raises(RuntimeError, match="missing prerequisite historical anchor"):
        docs.apply()
    for name in docs.DOCS:
        if name != "docs/design.md":
            assert (docs.ROOT / name).read_bytes() == original[name]
    assert not docs.MANIFEST.exists()


def test_tampering_prohibits_restoration(tmp_path, monkeypatch):
    bind_temp_root(tmp_path, monkeypatch)
    create_fixture(tmp_path)
    docs.apply()
    target = tmp_path / "docs" / "design.md"
    target.write_bytes(target.read_bytes() + b"\nMANUAL EDIT")
    with pytest.raises(RuntimeError, match="refusing restore"):
        docs.restore()
    assert docs.MANIFEST.is_file()


def test_wrong_historical_roadmap_tail_is_rejected(tmp_path, monkeypatch):
    bind_temp_root(tmp_path, monkeypatch)
    original = create_fixture(tmp_path)
    target = tmp_path / "docs" / "roadmap.md"
    target.write_bytes(original["docs/roadmap.md"] + b"\nmore work in progress\n")
    with pytest.raises(RuntimeError, match="final planned Phase 168 section has changed"):
        docs.apply()
    assert not docs.MANIFEST.exists()
