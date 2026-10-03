from phase156_r5_cross_group_reference_minimal_display_audit.audit_phase156_r5 import (
  classify_public_reference_structure,
)


def test_phase156_r5_structure_accepts_contiguous_used_headers():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
        2,
      ),
      body_markers=(
        2,
        1,
        2,
      ),
    )
  )

  assert missing == ()
  assert unused == ()
  assert contiguous is True


def test_phase156_r5_structure_detects_missing_header():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
      ),
      body_markers=(
        1,
        2,
      ),
    )
  )

  assert missing == (
    2,
  )
  assert unused == ()
  assert contiguous is True


def test_phase156_r5_structure_detects_unused_header():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
        2,
      ),
      body_markers=(
        1,
      ),
    )
  )

  assert missing == ()
  assert unused == (
    2,
  )
  assert contiguous is True


def test_phase156_r5_structure_detects_non_contiguous_headers():
  missing, unused, contiguous = (
    classify_public_reference_structure(
      header_numbers=(
        1,
        3,
      ),
      body_markers=(
        1,
        3,
      ),
    )
  )

  assert missing == ()
  assert unused == ()
  assert contiguous is False
