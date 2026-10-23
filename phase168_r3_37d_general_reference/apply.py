"""Only add a typed general-statement branch to existing Reference Projection."""
from __future__ import annotations
import ast
import difflib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "phase168_r3_37c_reference_projection.py"
OUT = Path(__file__).resolve().parent / "output"
BLOCK = r'''
    from phase165_r12_r20_eta_definition import TodaEtaFamilyGeneralDefinition
    from phase165_r12_r11_prop42_unified import TodaProp42GeneralExactnessStatement
    from toda_rules import Toda45IsomorphismStatement
    from expression import ScalarSymbol, ScalarSum, ScalarProduct
    from homotopy_groups import TodaIteratedSuspensionMap

    if isinstance(statement, TodaEtaFamilyGeneralDefinition):
        if type(statement.lower_bound) is int and statement.lower_bound == 2:
            return r"$n\ge 2$ に対し, $\eta_n=E^{n-2}\eta_2$ と定義する."
    if isinstance(statement, TodaProp42GeneralExactnessStatement):
        return (r"Proposition 4.2 により, EHP sequence "
                r"$\pi_{q+2}^{2p+1}\xrightarrow{\Delta}\pi_{q}^{p}"
                r"\xrightarrow{E}\pi_{q+1}^{p+1}"
                r"\xrightarrow{H}\pi_{q+1}^{2p+1}"
                r"\xrightarrow{\Delta}\cdots$ は完全である.")
    if isinstance(statement, Toda45IsomorphismStatement):
        mapping = statement.map
        if isinstance(mapping, TodaIteratedSuspensionMap):
            n = ScalarSymbol("n")
            m = ScalarSymbol("m")
            k = ScalarSymbol("k")
            if (
                mapping.exponent == ScalarSum(left=m, right=ScalarProduct(left=-1, right=n))
                and mapping.source_group.sphere_dimension == n
                and mapping.target_group.sphere_dimension == m
                and mapping.source_group.group_dimension == ScalarSum(left=n, right=k)
                and mapping.target_group.group_dimension == ScalarSum(left=m, right=k)
            ):
                return (r"$n\ge k+2$, $m\ge n$, $k\ge0$ に対して, "
                        r"$E^{m-n}:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{m+k}^{m}$ "
                        r"が成り立つ.")
'''

def main():
    raw=TARGET.read_bytes()
    old=raw.decode("utf-8").replace("\r\n","\n")
    if "TodaProp42GeneralExactnessStatement" in old and "EHP sequence" in old:
        raise RuntimeError("R3-37D general projection already installed")
    if old.count("def reference_statement_prose(")!=1:
        raise RuntimeError("Existing R3-37C Reference Projection function not found")
    tree=ast.parse(old)
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=="reference_statement_prose")
    lines=old.splitlines(keepends=True)
    original="".join(lines[node.lineno-1:node.end_lineno])
    sig_end=original.find("\n")
    if sig_end<0: raise RuntimeError("Unexpected function format")
    updated=original[:sig_end+1]+BLOCK+original[sig_end+1:]
    new=old.replace(original,updated,1)
    ast.parse(new)
    OUT.mkdir(exist_ok=True)
    (OUT/"reference_statement_prose_FULL.py").write_text(updated,encoding="utf-8")
    (OUT/"reference_statement_prose_BEFORE.py").write_text(original,encoding="utf-8")
    (OUT/"changes.diff").write_text("".join(difflib.unified_diff(
        old.splitlines(True),new.splitlines(True),fromfile="old",tofile="new"
    )),encoding="utf-8")
    TARGET.write_bytes(new.replace("\n","\r\n").encode("utf-8") if b"\r\n" in raw else new.encode("utf-8"))
    print("PATCHED:",TARGET)
    print("FULL_FUNCTION:",OUT/"reference_statement_prose_FULL.py")

if __name__=="__main__":
    main()
