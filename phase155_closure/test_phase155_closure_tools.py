from __future__ import annotations

import phase155_update_documents as updater


def test_replace_or_append_appends_when_marker_absent():
  updated = updater._replace_or_append(
    "before\n",
    "<!-- PHASE155_CLOSURE_START -->\nsection\n<!-- PHASE155_CLOSURE_END -->",
    updater.DOC_MARKER_START,
    updater.DOC_MARKER_END,
  )

  assert updated.count(
    updater.DOC_MARKER_START
  ) == 1


def test_replace_or_append_replaces_existing_section():
  original = (
    "before\n"
    "<!-- PHASE155_CLOSURE_START -->\n"
    "old\n"
    "<!-- PHASE155_CLOSURE_END -->\n"
    "after\n"
  )

  replacement = (
    "<!-- PHASE155_CLOSURE_START -->\n"
    "new\n"
    "<!-- PHASE155_CLOSURE_END -->"
  )

  updated = updater._replace_or_append(
    original,
    replacement,
    updater.DOC_MARKER_START,
    updater.DOC_MARKER_END,
  )

  assert "old" not in updated
  assert "new" in updated
  assert updated.count(
    updater.DOC_MARKER_START
  ) == 1


def test_readme_section_is_english():
  assert (
    "Phase 155 test-suite consolidation"
    in updater.README_SECTION
  )

  assert (
    "new tests should be lightweight by default"
    in updater.README_SECTION
  )


def test_roadmap_names_phase156_reference_boundary():
  assert (
    "Phase 156"
    in updater.ROADMAP_SECTION
  )

  assert (
    "Reference statement relevance / minimal display"
    in updater.ROADMAP_SECTION
  )


def test_phase155_does_not_claim_phase156_implementation():
  assert (
    "Phase 155 は Reference の表示内容を新たに最小化しない"
    in updater.DESIGN_SECTION
  )
