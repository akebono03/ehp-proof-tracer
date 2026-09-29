from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = (
    Path("tests/test_phase143_34_argument_header_method.py"),
    Path("tests/test_phase143_44_single_argument_narrative_renderer.py"),
    Path("tests/test_phase143_46_multi_argument_narrative_assembler.py"),
    Path("tests/test_phase144_5_generic_definition_order_equations.py"),
    Path("tests/test_phase144_6_pi6_generic_production_route.py"),
)

# R1 wrote these files with LF. Restore the repository's Windows CRLF working-tree
# representation without changing their already-correct expectation updates.
for rel in FILES:
    path = ROOT / rel
    data = path.read_bytes()
    normalized = data.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    path.write_bytes(normalized)
    print(f"CRLF restored: {rel}")

# The only remaining stale expectation found by the R1 focused run:
# group-structure purpose is fused with its exactness-method transition too.
path = ROOT / "tests/test_phase143_46_multi_argument_narrative_assembler.py"
data = path.read_bytes()
old = (
    '    "最後に、$\\\\pi_{6}^{3}$ の群構造を決定する."\r\n'
).encode("utf-8")
new = (
    '    "最後に、$\\\\pi_{6}^{3}$ の群構造を決定するために、"\r\n'
    '    "次の完全列を考える."\r\n'
).encode("utf-8")

count = data.count(old)
if count != 1:
    raise SystemExit(
        "expected exactly one remaining pi6 group-purpose occurrence; "
        f"found {count}"
    )
path.write_bytes(data.replace(old, new, 1))

print("Phase 146 R2 remaining expectation repair applied.")
print("Production code changes: none")
