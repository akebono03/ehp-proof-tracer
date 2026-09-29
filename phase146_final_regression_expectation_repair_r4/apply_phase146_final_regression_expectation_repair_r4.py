from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    "tests/test_phase143_34_argument_header_method.py",
    "tests/test_phase143_44_single_argument_narrative_renderer.py",
    "tests/test_phase143_46_multi_argument_narrative_assembler.py",
    "tests/test_phase144_5_generic_definition_order_equations.py",
    "tests/test_phase144_6_pi6_generic_production_route.py",
)

subprocess.run(["git", "checkout", "--", *FILES], cwd=ROOT, check=True)
print("Restored five test files from HEAD.")

def newline_for(data: bytes) -> bytes:
    return b"\r\n" if b"\r\n" in data else b"\n"

def rep(rel, old_lines, new_lines):
    path = ROOT / rel
    data = path.read_bytes()
    nl = newline_for(data)
    old = nl.join(line.encode("utf-8") for line in old_lines) + nl
    new = nl.join(line.encode("utf-8") for line in new_lines) + nl
    count = data.count(old)
    if count != 1:
        raise SystemExit(
            f"{rel}: expected 1 occurrence, found {count}; "
            f"newline={'CRLF' if nl == bytes([13,10]) else 'LF'}"
        )
    path.write_bytes(data.replace(old, new, 1))
    print(
        f"updated: {rel} "
        f"({'CRLF' if nl == bytes([13,10]) else 'LF'} preserved)"
    )

rep(FILES[0],
    ["    \"次に、$\\\\nu'$ の位数を決定する.\"",
     "    \"そのために、次の完全列を考える.\""],
    ["    \"次に、$\\\\nu'$ の位数を決定するために、\"",
     "    \"次の完全列を考える.\""])
rep(FILES[0],
    ["    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定する.\"",
     "    \"そのために、次の完全列を考える.\""],
    ["    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定するために、\"",
     "    \"次の完全列を考える.\""])
rep(FILES[0],
    ["    \"$\\\\nu'$ の位数を決定する.\""],
    ["    \"$\\\\nu'$ の位数を決定するために、\"",
     "    \"次の完全列を考える.\""])
rep(FILES[0],
    ["    \"そのために、次の完全列を考える.\"",
     "    in rendered"],
    ["    \"位数を決定するために、次の完全列を考える.\"",
     "    in rendered"])

rep(FILES[1],
    ["    \"次に、$\\\\nu'$ の位数を決定する. \"",
     "    \"そのために、次の完全列を考える.\""],
    ["    \"次に、$\\\\nu'$ の位数を決定するために、\"",
     "    \"次の完全列を考える.\""])
rep(FILES[1],
    ["    \"$\\\\nu'$ の位数を決定する.\""],
    ["    \"$\\\\nu'$ の位数を決定するために、\"",
     "    \"次の完全列を考える.\""])

rep(FILES[2],
    ["    \"次に、$\\\\nu'$ の位数を決定する.\""],
    ["    \"次に、$\\\\nu'$ の位数を決定するために、\"",
     "    \"次の完全列を考える.\""])
rep(FILES[2],
    ["    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定する.\""],
    ["    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定するために、\"",
     "    \"次の完全列を考える.\""])
rep(FILES[2],
    ["    \"$\\\\nu'$ の位数を決定する. \"",
     "    \"そのために、次の完全列を考える.\""],
    ["    \"$\\\\nu'$ の位数を決定するために、\"",
     "    \"次の完全列を考える.\""])

rep(FILES[3],
    ["  assert r\"$\\nu'$ の位数を決定する.\" in rendered"],
    ["  assert (",
     "    r\"$\\nu'$ の位数を決定するために、\"",
     "    r\"次の完全列を考える.\"",
     "    in rendered",
     "  )"])

rep(FILES[4],
    ["  assert r\"$\\nu'$ の位数を決定する.\" in actual"],
    ["  assert (",
     "    r\"$\\nu'$ の位数を決定するために、\"",
     "    r\"次の完全列を考える.\"",
     "    in actual",
     "  )"])

print("Phase 146 R4 newline-aware minimal expectation repair applied.")
print("Production code changes: none")
