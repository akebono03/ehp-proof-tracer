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

def rep(rel, old, new):
    p = ROOT / rel
    data = p.read_bytes()
    old_b, new_b = old.encode("utf-8"), new.encode("utf-8")
    count = data.count(old_b)
    if count != 1:
        raise SystemExit(f"{rel}: expected 1 occurrence, found {count}")
    p.write_bytes(data.replace(old_b, new_b, 1))
    print("updated:", rel)

rep(FILES[0],
    "    \"次に、$\\\\nu'$ の位数を決定する.\"\n    \"そのために、次の完全列を考える.\"\n",
    "    \"次に、$\\\\nu'$ の位数を決定するために、\"\n    \"次の完全列を考える.\"\n")
rep(FILES[0],
    "    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定する.\"\n    \"そのために、次の完全列を考える.\"\n",
    "    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定するために、\"\n    \"次の完全列を考える.\"\n")
rep(FILES[0],
    "    \"$\\\\nu'$ の位数を決定する.\"\n",
    "    \"$\\\\nu'$ の位数を決定するために、\"\n    \"次の完全列を考える.\"\n")
rep(FILES[0],
    "    \"そのために、次の完全列を考える.\"\n    in rendered\n",
    "    \"位数を決定するために、次の完全列を考える.\"\n    in rendered\n")

rep(FILES[1],
    "    \"次に、$\\\\nu'$ の位数を決定する. \"\n    \"そのために、次の完全列を考える.\"\n",
    "    \"次に、$\\\\nu'$ の位数を決定するために、\"\n    \"次の完全列を考える.\"\n")
rep(FILES[1],
    "    \"$\\\\nu'$ の位数を決定する.\"\n",
    "    \"$\\\\nu'$ の位数を決定するために、\"\n    \"次の完全列を考える.\"\n")

rep(FILES[2],
    "    \"次に、$\\\\nu'$ の位数を決定する.\"\n",
    "    \"次に、$\\\\nu'$ の位数を決定するために、\"\n    \"次の完全列を考える.\"\n")
rep(FILES[2],
    "    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定する.\"\n",
    "    \"最後に、$\\\\pi_{6}^{3}$ の群構造を決定するために、\"\n    \"次の完全列を考える.\"\n")
rep(FILES[2],
    "    \"$\\\\nu'$ の位数を決定する. \"\n    \"そのために、次の完全列を考える.\"\n",
    "    \"$\\\\nu'$ の位数を決定するために、\"\n    \"次の完全列を考える.\"\n")

rep(FILES[3],
    "  assert r\"$\\nu'$ の位数を決定する.\" in rendered\n",
    "  assert (\n    r\"$\\nu'$ の位数を決定するために、\"\n    r\"次の完全列を考える.\"\n    in rendered\n  )\n")
rep(FILES[4],
    "  assert r\"$\\nu'$ の位数を決定する.\" in actual\n",
    "  assert (\n    r\"$\\nu'$ の位数を決定するために、\"\n    r\"次の完全列を考える.\"\n    in actual\n  )\n")

print("Phase 146 R3 clean minimal expectation repair applied.")
print("Production code changes: none")
