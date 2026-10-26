"""R4G: patch reviewed two functions/classes only; preserve user worktree on failure."""
from __future__ import annotations

import ast
import hashlib
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PACKAGE = Path(__file__).resolve().parent
OUT = PACKAGE / "output"
BLOBS = {
    "phase165_r52_r27_r5_literature.py": "b683533badcf80a6568bd22859efa6b7b8f1edd5",
    "phase168_r3_37c_reference_projection.py": "32b7d01545fe8b37afb0eb85a53caf615064d83f",
}

CLASS_OLD = '@dataclass(frozen=True)\nclass TodaProp44UniversalStatement:\n    """For n, alpha: H(alpha)=±iota_(2n-1) implies the sum map is an isomorphism."""\n    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"\n    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"\n    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"\n    target_group: str = "pi_i^n"\n    quantifiers: tuple[str, ...] = ("n", "i", "alpha")\n    includes_suspension_injectivity: bool = True\n'
CLASS_NEW = '@dataclass(frozen=True)\nclass TodaProp44UniversalStatement:\n    """Conditional proposition plus its explicitly checked preceding Hopf-fibration premise.\n\n    The fibration statement is printed before Proposition 4.4 in the adopted\n    Toda source, not in the proposition environment itself.\n    """\n    source_condition: str = "alpha in pi_(2n-1)^n; H(alpha)=+/-iota_(2n-1)"\n    isomorphism_map: str = "(beta,gamma)->E(beta)+alpha o gamma"\n    source_group: str = "pi_(i-1)^(n-1) + pi_i^(2n-1)"\n    target_group: str = "pi_i^n"\n    quantifiers: tuple[str, ...] = ("n", "i", "alpha")\n    includes_suspension_injectivity: bool = True\n    preceding_hopf_fibration_dimensions: tuple[int, ...] = (2, 4, 8)\n'
VERIFY_FUNCTION = 'def verify_prop44_hopf_fibration_source(source_path: Path | None = None) -> None:\n    """Verify the actual Chapter IV paragraph immediately before Proposition 4.4.\n\n    The frozen Git blob is an independently reviewed source identity; no\n    assertion can be introduced from a modified or incomplete passage.\n    """\n    if source_path is None:\n        source_path = Path(__file__).resolve().parent / "sources" / "toda" / "Toda_04_2.tex"\n    if not isinstance(source_path, Path):\n        raise TypeError("source_path must be a pathlib.Path")\n    original = source_path.read_bytes()\n    normalized = original.replace(b"\\r\\n", b"\\n")\n    candidates = (original, normalized, normalized.replace(b"\\n", b"\\r\\n"))\n    def actual_sha(content: bytes) -> str:\n        return sha1(b"blob " + str(len(content)).encode("ascii") + b"\\x00" + content).hexdigest()\n    if not any(actual_sha(candidate) == "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7"\n               for candidate in candidates):\n        raise ValueError("unverified Toda Chapter IV source file for Hopf fibration")\n    text = normalized.decode("utf-8")\n    start_marker = "$n=2,4,8$ のとき, Hopf fibration"\n    end_marker = r"\\begin{proposition}\\label{prop:4.4}"\n    start = text.find(start_marker)\n    end = text.find(end_marker)\n    if start < 0 or end <= start or text.count(start_marker) != 1 or text.count(end_marker) != 1:\n        raise ValueError("Proposition 4.4 Hopf-fibration source position is invalid")\n    passage = text[start:end]\n    required = (\n        r"S^{2n-1}\\xrightarrow{h} S^n",\n        "Hopf 不変量",\n        r"$\\pm1$",\n        r"\\cite{Steenrod1951}",\n    )\n    if any(fragment not in passage for fragment in required):\n        raise ValueError("the reviewed Hopf-fibration prelude is missing")\n'


def git_blob(text: str) -> str:
    value = text.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(value)).encode("ascii") + b"\x00" + value).hexdigest()


def source_matches_blob(source: str, expected: str) -> bool:
    normalized = source.replace("\r\n", "\n")
    candidates = (source, normalized, normalized.replace("\n", "\r\n"))
    return any(git_blob(candidate) == expected for candidate in candidates)


def replace_exact(source: str, original: str, replacement: str) -> str:
    if source.count(original) != 1:
        raise RuntimeError("required source anchor was missing or ambiguous")
    return source.replace(original, replacement, 1)


def patch_literature(source: str) -> str:
    source = replace_exact(source,
        "from dataclasses import dataclass\nfrom hashlib import sha256\n",
        "from dataclasses import dataclass\nfrom hashlib import sha1, sha256\nfrom pathlib import Path\n",
    )
    source = replace_exact(source, CLASS_OLD, CLASS_NEW)
    source = replace_exact(source, "_SOURCES = (\n", VERIFY_FUNCTION + "\n\n_SOURCES = (\n")
    source = replace_exact(source,
        "def build_typed_literature_bridge(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:\n"
        "    \"\"\"Produce two fixed, source-bound general claims; never promote other archive rows.\"\"\"\n"
        "    registry = UnifiedStatementRegistry()\n",
        "def build_typed_literature_bridge(source_bridge: RegistryBridgeResult) -> RegistryBridgeResult:\n"
        "    \"\"\"Produce two fixed, source-bound general claims; never promote other archive rows.\"\"\"\n"
        "    verify_prop44_hopf_fibration_source()\n"
        "    registry = UnifiedStatementRegistry()\n",
    )
    return source


def patch_projection(source: str) -> str:
    old = (
        "            elif (type(statement) is TodaProp44UniversalStatement\n"
        "                  and statement == TodaProp44UniversalStatement()):\n"
        "                sentence = (\n"
        "                    r\"$\\alpha\\in\\pi_{2n-1}^{n}$, \"\n"
        "                    r\"$H(\\alpha)=\\pm\\iota_{2n-1}$ とすると, \"\n"
        "                    r\"$E:\\pi_{i-1}^{n-1}\\to\\pi_i^{n}$ は単射.\"\n"
        "                )\n"
    )
    new = (
        "            elif (type(statement) is TodaProp44UniversalStatement\n"
        "                  and statement == TodaProp44UniversalStatement()\n"
        "                  and statement.preceding_hopf_fibration_dimensions == (2, 4, 8)):\n"
        "                sentence = (\n"
        "                    r\"Proposition 4.4 直前の記述（Steenrod1951 を引用）: \"\n"
        "                    r\"$n=2,4,8$ では Hopf fibration \"\n"
        "                    r\"$h:S^{2n-1}\\to S^n$ が存在する.\"\n"
        "                    + \"\\n\"\n"
        "                    r\"$\\alpha\\in\\pi_{2n-1}^{n}$, \"\n"
        "                    r\"$H(\\alpha)=\\pm\\iota_{2n-1}$ とすると, \"\n"
        "                    r\"$E:\\pi_{i-1}^{n-1}\\to\\pi_i^{n}$ は単射.\"\n"
        "                )\n"
    )
    return replace_exact(source, old, new)


def print_function(source: str, name: str) -> str:
    tree = ast.parse(source)
    node = next((item for item in tree.body
                 if isinstance(item, (ast.FunctionDef, ast.ClassDef)) and item.name == name), None)
    if node is None:
        raise RuntimeError("unable to extract full source: " + name)
    lines = source.splitlines(keepends=True)
    first = min([node.lineno] + [item.lineno for item in node.decorator_list])
    return "".join(lines[first - 1:node.end_lineno]) + "\n"


def prepare() -> None:
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          check=True, text=True, capture_output=True).stdout.strip()
    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT,
                            check=True, text=True, capture_output=True).stdout.strip()
    if branch != "develop":
        raise RuntimeError("R4G requires develop branch")
    # Fail before changing production code if the original pre-Proposition 4.4
    # TeX paragraph no longer has the reviewed Git blob identity.
    source_tex = (ROOT / "sources" / "toda" / "Toda_04_2.tex").read_text(encoding="utf-8")
    if not source_matches_blob(source_tex, "4d0c32b196f4bd51c04650dd26b0fd7133b6d4f7"):
        raise RuntimeError("R4G cannot verify Chapter IV Hopf-fibration source")
    OUT.mkdir(exist_ok=True)
    candidates = {}
    for name, blob in BLOBS.items():
        path = ROOT / name
        original = path.read_bytes()
        source = original.decode("utf-8").replace("\r\n", "\n")
        if not source_matches_blob(source, blob):
            raise RuntimeError("unrecognized worktree source: " + name)
        modified = patch_literature(source) if "literature" in name else patch_projection(source)
        ast.parse(modified)
        candidates[name] = (original, modified.encode("utf-8"), modified)
    for name, (original, replacement, modified) in candidates.items():
        (OUT / (name + ".before")).write_bytes(original)
        (OUT / (name + ".FULL")).write_bytes(replacement)
        if "literature" in name:
            (OUT / "TodaProp44UniversalStatement_FULL.py").write_text(
                print_function(modified, "TodaProp44UniversalStatement"), encoding="utf-8")
            (OUT / "verify_prop44_hopf_fibration_source_FULL.py").write_text(
                print_function(modified, "verify_prop44_hopf_fibration_source"), encoding="utf-8")
            (OUT / "build_typed_literature_bridge_FULL.py").write_text(
                print_function(modified, "build_typed_literature_bridge"), encoding="utf-8")
        else:
            (OUT / "project_reference_bodies_FULL.py").write_text(
                print_function(modified, "project_reference_bodies"), encoding="utf-8")
    written = []
    try:
        for name, (original, replacement, modified) in candidates.items():
            (ROOT / name).write_bytes(replacement)
            written.append(name)
            print("R4G_PATCHED=" + name)
    except BaseException:
        for name in reversed(written):
            (ROOT / name).write_bytes(candidates[name][0])
        raise
    print("R4G_GIT_HEAD=" + head)
    print("R4G_FULL_FUNCTIONS_DIR=" + str(OUT))

if __name__ == "__main__":
    prepare()
