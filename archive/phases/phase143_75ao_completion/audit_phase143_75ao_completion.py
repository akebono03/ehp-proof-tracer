import runpy

print("=" * 78)
print("Phase 143-75AO bulk completion inventory")
print("=" * 78)

runpy.run_path(
  "phase143_75u/"
  "audit_phase143_75u_remaining_fallbacks.py",
  run_name="__main__",
)

print("")
print("Expected after the 75AO nine-type bulk batch:")
print("  baseline before batch: 53")
print("  removed occurrences: 37")
print("  expected fallback occurrences: 16")
print("  expected statement types: 6")
print("  expected distinct fallback rule names: 6")
print("  expected render errors: 0")
