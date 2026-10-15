"""Install a single additional R2 module without editing production sources."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def install(project: Path, package: Path) -> str:
    target = project / "phase165_renderer_narrative_model.py"
    source = package / "phase165_renderer_narrative_model.py"
    content = source.read_text(encoding="utf-8")
    ast.parse(content)
    if target.exists():
        old = target.read_text(encoding="utf-8")
        if old == content:
            return "ALREADY_INSTALLED"
        raise RuntimeError("R2 model already exists with different content; not overwriting")
    shutil.copy2(source, target)
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("Phase165 Renderer R2:", install(package.parent, package))
    print("No existing renderer or proof search code changed; full pytest NOT run")
