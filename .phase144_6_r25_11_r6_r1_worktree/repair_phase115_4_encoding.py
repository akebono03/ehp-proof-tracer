from pathlib import Path
import re
import shutil
import subprocess

project = Path(r"C:\Users\user\Dropbox\Python\fitz\ehp_proof")
package = Path(r"C:\Users\user\Downloads\phase115_4_sigma11_handoff")

phase114 = project / "tests" / "test_phase114_3_nu5_operation_query_handoff.py"
phase115 = project / "tests" / "test_phase115_sigma11_operation_query_handoff.py"

# Preserve the currently corrupted files for inspection.
for path in (phase114, phase115):
    if path.exists():
        backup = path.with_name(
            path.name + ".corrupted_before_phase115_4_repair"
        )
        shutil.copy2(path, backup)
        print(f"Backed up corrupted file: {backup}")

# Restore the Phase 114 test exactly from Git HEAD.
phase114_bytes = subprocess.check_output(
    [
        "git",
        "show",
        "HEAD:tests/test_phase114_3_nu5_operation_query_handoff.py",
    ],
    cwd=project,
)
phase114.write_bytes(phase114_bytes)
print(f"Restored from Git HEAD: {phase114}")

# Restore the Phase 115 test exactly from the downloaded package.
source_phase115 = (
    package / "test_phase115_sigma11_operation_query_handoff.py"
)

if not source_phase115.exists():
    raise FileNotFoundError(
        f"Phase 115 package test not found: {source_phase115}"
    )

shutil.copy2(
    source_phase115,
    phase115,
)
print(f"Restored from package: {phase115}")

# Patch Phase 114 using Python UTF-8 I/O.
text = phase114.read_text(encoding="utf-8")

import_block = """from repository_nu5_stable_bridge_specialization import (
  is_nu5_stable_bridge_operation_query,
)
"""

if (
    "from repository_nu5_stable_bridge_specialization import ("
    not in text
):
    anchor = """from repository_operation_query_presentation import (
  build_repository_operation_query_presentation,
)
"""

    if anchor not in text:
        raise RuntimeError(
            "Phase 114 import anchor not found"
        )

    text = text.replace(
        anchor,
        import_block + anchor,
        1,
    )

old_pattern = (
    r"(?ms)^def "
    r"test_phase114_3_handoff_does_not_expand_to_e_sigma11"
    r"\(\):.*?(?=^def |\Z)"
)

new_function = """def test_phase114_3_nu5_handoff_guard_does_not_accept_e_sigma11():
  query = parse_repository_operation_query(
    "E(sigma_11)"
  )

  assert not (
    is_nu5_stable_bridge_operation_query(
      query
    )
  )


"""

text, count = re.subn(
    old_pattern,
    new_function,
    text,
    count=1,
)

if count != 1:
    raise RuntimeError(
        "Phase 114 E(sigma_11) boundary test not found"
    )

phase114.write_text(
    text,
    encoding="utf-8",
    newline="\n",
)
print(f"Patched safely as UTF-8: {phase114}")

# Patch Phase 115 using Python UTF-8 I/O.
text = phase115.read_text(encoding="utf-8")

pattern = (
    r"(?ms)^def "
    r"test_phase115_4_existing_nu5_handoff_remains_available"
    r"\(\):.*?(?=^def |\Z)"
)

new_function = """def test_phase115_4_existing_nu5_handoff_remains_available():
  result = (
    query_standard_repository_operation_input(
      "E(nu_5)"
    )
  )

  assert result.found

  assert any(
    (
      isinstance(
        match.statement,
        Relation,
      )
      and isinstance(
        match.statement.lhs,
        Suspension,
      )
      and match.statement.lhs
      .expression
      .generator
      == GeneratorSymbol(
        family="\\u03bd",
        index=5,
      )
      and match.statement.rhs.generator
      == GeneratorSymbol(
        family="\\u03bd",
        index=6,
      )
    )
    for match in result.matches
  )


"""

text, count = re.subn(
    pattern,
    new_function,
    text,
    count=1,
)

if count != 1:
    raise RuntimeError(
        "Phase 115 nu5 regression test not found"
    )

phase115.write_text(
    text,
    encoding="utf-8",
    newline="\n",
)
print(f"Patched safely as UTF-8: {phase115}")

print()
print("Phase 115-4 encoding repair completed.")
