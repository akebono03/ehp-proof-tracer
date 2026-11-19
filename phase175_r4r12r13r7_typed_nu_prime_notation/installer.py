"""Minimal anchored replacement of the R13R2 coordinate matcher only."""
from __future__ import annotations

from pathlib import Path

TARGET = Path("phase175_r4r12r13r2_delta_injective_e_surjective/rule.py")
OLD_IMPORT = "from expression import Multiple, Sum\n"
NEW_IMPORT = (
    "from expression import Multiple, Sum\n"
    "from phase175_r4r12r13r7_typed_nu_prime_notation.notation import (\n"
    "    same_typed_generator_notation,\n"
    ")\n"
)
OLD_BODY = "    if value == free:\n        return 1, 0\n    if value == torsion:\n        return 0, 1\n"
NEW_BODY = (
    "    if same_typed_generator_notation(value, free):\n"
    "        return 1, 0\n"
    "    if same_typed_generator_notation(value, torsion):\n"
    "        return 0, 1\n"
)


def render(source: str) -> tuple[str, bool]:
    """Fail closed on source drift and partial application."""
    if source.count(NEW_IMPORT) == 1 and source.count(NEW_BODY) == 1:
        return source, False
    if NEW_IMPORT in source or NEW_BODY in source:
        raise RuntimeError("R13R7_PARTIAL_PATCH")
    if source.count(OLD_IMPORT) != 1 or source.count(OLD_BODY) != 1:
        raise RuntimeError("R13R7_SOURCE_DRIFT")
    result = source.replace(OLD_IMPORT, NEW_IMPORT, 1).replace(OLD_BODY, NEW_BODY, 1)
    return result, True


def plan(root: Path) -> tuple[Path, str, str, bool]:
    path = root / TARGET
    before = path.read_text(encoding="utf-8-sig")
    after, needed = render(before)
    return path, before, after, needed


def install(root: Path, *, dry_run: bool, output: Path) -> dict[str, object]:
    import ast
    path, before, after, required = plan(root)
    ast.parse(after)
    output.mkdir(parents=True, exist_ok=True)
    (output / "rule_FULL.py").write_text(after, encoding="utf-8")
    if required and not dry_run:
        raw = path.read_bytes()
        if b"\r\n" in raw:
            path.write_bytes(after.replace("\n", "\r\n").encode("utf-8"))
        else:
            path.write_text(after, encoding="utf-8")
    return {"change_required": required, "installed": required and not dry_run,
            "target": str(TARGET), "full_replacement_file": str(output / "rule_FULL.py")}
