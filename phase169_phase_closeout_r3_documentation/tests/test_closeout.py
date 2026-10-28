"""Focused contract checks; never invokes the repository-wide suite."""
import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "run.py"
SPEC = importlib.util.spec_from_file_location("phase169_doc_closeout", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def examples():
    return {
        "README.md": "# EHP Proof Tracer\n\n## Current status — Phase 169 R10ET complete; Phase 169 remains open (2026-10-28)\n\nold content\n\n## Current status — Phase 168 closed (2026-10-25)\n\n## Tests\npython -m pytest tests -q --tb=short\n",
        "docs/design.md": "# 設計\n\n## Phase 169 R10ET\n\nold\n",
        "docs/development_log.md": "# 開発ログ\n\nold\n",
        "docs/roadmap.md": "# Roadmap\n\n**現状：Phase 169 進行中。**\n\n### 次の実施順序\n\nold\n",
        "docs/proof_records.md": "# 証明記録\n\nold\n",
    }


def test_five_document_sources_match_contract():
    assert len(MODULE.DOC_BLOBS) == 5
    assert len(MODULE.SOURCE_BLOBS) == 8


def test_report_requires_precise_documented_test_counts():
    assert MODULE.REPORT_DIR_PREFIX == "phase169_closeout_r1_"
    assert MODULE.REVIEWED_REMOTE_HEAD != MODULE.BASELINE_HEAD


def test_full_files_are_generated():
    old = examples()
    new = MODULE.edit_documents(old)
    assert new.keys() == old.keys()
    assert all(len(new[k]) > len(old[k]) for k in old)


def test_closeout_markers_once():
    new = MODULE.edit_documents(examples())
    assert all(text.count(MODULE.DOC_MARKER) == 1 for text in new.values())


def test_readme_is_current():
    new = MODULE.edit_documents(examples())
    assert "Phase 169 closed" in new["README.md"]
    assert "3,546 active" in new["README.md"]
    assert "Phase 169 remains open" not in new["README.md"]


def test_roadmap_retains_prior_history():
    new = MODULE.edit_documents(examples())["docs/roadmap.md"]
    assert "R10ET 時点の状況" in new
    assert "Phase 169 — 正式終了" in new


def test_prior_logs_are_appended_not_replaced():
    old = examples()
    new = MODULE.edit_documents(old)
    assert new["docs/development_log.md"].startswith(old["docs/development_log.md"].rstrip("\n"))
    assert new["docs/proof_records.md"].startswith(old["docs/proof_records.md"].rstrip("\n"))


def test_double_run_refused():
    texts = MODULE.edit_documents(examples())
    with pytest.raises(RuntimeError, match="already exists"):
        MODULE.edit_documents(texts)


def test_changed_readme_layout_refused():
    old = examples()
    old["README.md"] = "# missing expected section"
    with pytest.raises(RuntimeError, match="README phase boundary"):
        MODULE.edit_documents(old)


def test_git_blob_matches_standard_object_encoding():
    assert MODULE.git_blob(b"hello world\n") == "3b18e512dba79e4c8300dd08aeb37f8e728b8dad"
