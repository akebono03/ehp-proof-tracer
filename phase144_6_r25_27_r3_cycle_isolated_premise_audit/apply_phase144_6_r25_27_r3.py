from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "phase144_6_r25_27_proof_edge_ownership_boundary_audit" / "audit_phase144_6_r25_27.py"
TEST = ROOT / "phase144_6_r25_27_proof_edge_ownership_boundary_audit" / "test_phase144_6_r25_27.py"


def main() -> int:
  source = AUDIT.read_text(encoding="utf-8")

  old_sig = """def _closure_from_block(
  dependencies,
  start_index,
  boundary_indices,
):
"""
  new_sig = """def _closure_from_block(
  dependencies,
  start_index,
  boundary_indices,
  excluded_indices=(),
):
"""
  if old_sig in source:
    source = source.replace(old_sig, new_sig, 1)

  old_guard = """  def visit(
    block_index,
  ):
    if block_index in boundary_indices:
      return
"""
  new_guard = """  excluded_indices = frozenset(
    excluded_indices
  )

  def visit(
    block_index,
  ):
    if block_index in boundary_indices:
      return

    if block_index in excluded_indices:
      return
"""
  if old_guard in source:
    source = source.replace(old_guard, new_guard, 1)

  old_start = """  if start_index not in boundary_indices:
    visit(
      start_index
    )
"""
  new_start = """  if (
    start_index not in boundary_indices
    and start_index not in excluded_indices
  ):
    visit(
      start_index
    )
"""
  if old_start in source:
    source = source.replace(old_start, new_start, 1)

  old_call = """        _closure_from_block(
          dependencies,
          premise_index,
          boundary,
        )
"""
  new_call = """        _closure_from_block(
          dependencies,
          premise_index,
          boundary,
          excluded_indices=(
            conclusion_index,
          ),
        )
"""
  if old_call in source:
    source = source.replace(old_call, new_call)

  AUDIT.write_text(source, encoding="utf-8")

  test_source = TEST.read_text(encoding="utf-8")
  old_test_call = """        _closure_from_block(
          dependencies,
          premise_index,
          boundary,
        )
"""
  new_test_call = """        _closure_from_block(
          dependencies,
          premise_index,
          boundary,
          excluded_indices=(
            conclusion_index,
          ),
        )
"""
  if old_test_call in test_source:
    test_source = test_source.replace(
      old_test_call,
      new_test_call,
    )
  TEST.write_text(test_source, encoding="utf-8")

  print("R25-27-R3 isolated-premise audit repair applied.")
  print("Production code changes: none.")
  print("Only R25-27 audit/test harness changed.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
