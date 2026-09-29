from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def replace_once(path, old, new):
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected 1 occurrence, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")

p = ROOT / "tests/test_phase143_34_argument_header_method.py"
replace_once(p,
'    "次に、$\\\\nu\'$ の位数を決定する."\n    "そのために、次の完全列を考える."\n',
'    "次に、$\\\\nu\'$ の位数を決定するために、"\n    "次の完全列を考える."\n')
replace_once(p,
'    "最後に、$\\\\pi_{6}^{3}$ の群構造を決定する."\n    "そのために、次の完全列を考える."\n',
'    "最後に、$\\\\pi_{6}^{3}$ の群構造を決定するために、"\n    "次の完全列を考える."\n')
replace_once(p,
'    "$\\\\nu\'$ の位数を決定する."\n',
'    "$\\\\nu\'$ の位数を決定するために、"\n    "次の完全列を考える."\n')
replace_once(p,
'    "そのために、次の完全列を考える."\n    in rendered\n',
'    "位数を決定するために、次の完全列を考える."\n    in rendered\n')

p = ROOT / "tests/test_phase143_44_single_argument_narrative_renderer.py"
replace_once(p,
'    "次に、$\\\\nu\'$ の位数を決定する. "\n    "そのために、次の完全列を考える."\n',
'    "次に、$\\\\nu\'$ の位数を決定するために、"\n    "次の完全列を考える."\n')
replace_once(p,
'    "$\\\\nu\'$ の位数を決定する."\n',
'    "$\\\\nu\'$ の位数を決定するために、"\n    "次の完全列を考える."\n')

p = ROOT / "tests/test_phase143_46_multi_argument_narrative_assembler.py"
replace_once(p,
'    "次に、$\\\\nu\'$ の位数を決定する."\n',
'    "次に、$\\\\nu\'$ の位数を決定するために、"\n    "次の完全列を考える."\n')
replace_once(p,
'    "$\\\\nu\'$ の位数を決定する. "\n    "そのために、次の完全列を考える."\n',
'    "$\\\\nu\'$ の位数を決定するために、"\n    "次の完全列を考える."\n')

p = ROOT / "tests/test_phase144_5_generic_definition_order_equations.py"
replace_once(p,
'  assert r"$\\nu\'$ の位数を決定する." in rendered\n',
'  assert (\n    r"$\\nu\'$ の位数を決定するために、"\n    r"次の完全列を考える."\n    in rendered\n  )\n')

p = ROOT / "tests/test_phase144_6_pi6_generic_production_route.py"
replace_once(p,
'  assert r"$\\nu\'$ の位数を決定する." in actual\n',
'  assert (\n    r"$\\nu\'$ の位数を決定するために、"\n    r"次の完全列を考える."\n    in actual\n  )\n')

print("Phase 146 expectation-only repair applied.")
print("Production code changes: none")
