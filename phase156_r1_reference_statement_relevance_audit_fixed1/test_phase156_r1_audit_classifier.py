from phase156_r1_reference_statement_relevance_audit.audit_phase156_r1 import (
  CLASS_BODY_REQUIRED,
  CLASS_REFERENCE_OVERFULL,
  CLASS_UNNECESSARY,
  classify_duplicate,
)


def test_phase156_r1_classifies_standalone_duplicate_as_unnecessary():
  classification, _ = classify_duplicate(
    reference_number=2,
    statement_line="$E: A \\xrightarrow{\\cong} B$",
    reference_statement_count=1,
    body_occurrences=(
      {
        "line_number": 4,
        "line": "$E: A \\xrightarrow{\\cong} B$",
        "standalone": True,
      },
    ),
  )

  assert classification == CLASS_UNNECESSARY


def test_phase156_r1_classifies_derivation_context_as_body_required():
  classification, _ = classify_duplicate(
    reference_number=2,
    statement_line="$E: A \\xrightarrow{\\cong} B$",
    reference_statement_count=1,
    body_occurrences=(
      {
        "line_number": 4,
        "line": "これより, $E: A \\xrightarrow{\\cong} B$を得る。",
        "standalone": False,
      },
    ),
  )

  assert classification == CLASS_BODY_REQUIRED


def test_phase156_r1_classifies_multi_statement_reference_as_overfull():
  classification, _ = classify_duplicate(
    reference_number=2,
    statement_line="$E: A \\xrightarrow{\\cong} B$",
    reference_statement_count=2,
    body_occurrences=(
      {
        "line_number": 4,
        "line": "これより, $E: A \\xrightarrow{\\cong} B$を得る。",
        "standalone": False,
      },
    ),
  )

  assert classification == CLASS_REFERENCE_OVERFULL


def test_phase156_r1_classifies_reference_only_use_as_unnecessary():
  classification, _ = classify_duplicate(
    reference_number=3,
    statement_line="$x=0$",
    reference_statement_count=1,
    body_occurrences=(
      {
        "line_number": 7,
        "line": "[R3] により, $x=0$。",
        "standalone": False,
      },
    ),
  )

  assert classification == CLASS_UNNECESSARY
