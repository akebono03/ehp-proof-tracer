"""R52-R3: make empty steps legal only for explicitly typed partial views.

Changes precisely one existing dataclass, WebGroupProofView, by adding a
backward-compatible keyword and retaining the legacy completed-proof check.
Also replaces the complete R52-R3 adapter function module.
"""
from __future__ import annotations

import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
BUNDLE = Path(__file__).resolve().parent
VIEW_PATH = ROOT / "web_group_proof.py"
ADAPTER_PATH = ROOT / "phase165_r52_r3_web_adapter.py"
CLASS_NAME = "WebGroupProofView"
FIELD_LINE = "  partial_result: bool = False\n"
OLD_CHECK = """    if not self.steps:
      raise ValueError(
        "steps must not be empty"
      )"""
NEW_CHECK = """    if not isinstance(self.partial_result, bool):
      raise TypeError("partial_result must be a bool")

    if not self.steps and not self.partial_result:
      raise ValueError(
        "steps must not be empty"
      )"""


def replace_class(source: str) -> tuple[str, str]:
    tree = ast.parse(source)
    classes = [node for node in tree.body if isinstance(node, ast.ClassDef)
               and node.name == CLASS_NAME]
    if len(classes) != 1:
        raise RuntimeError("Expected exactly one WebGroupProofView class")
    node = classes[0]
    lines = source.splitlines(keepends=True)
    segment = "".join(lines[node.lineno - 1:node.end_lineno])
    if "partial_result: bool = False" in segment:
        if "if not self.steps and not self.partial_result:" not in segment:
            raise RuntimeError("Partial Web view change is incomplete")
        return source, segment
    anchor = "  ] = ()\n\n  def __post_init__("
    if segment.count(anchor) != 1:
        raise RuntimeError("WebGroupProofView field layout changed")
    if segment.count(OLD_CHECK) != 1:
        raise RuntimeError("WebGroupProofView steps guard changed")
    segment = segment.replace(anchor, "  ] = ()\n" + FIELD_LINE + "\n  def __post_init__(", 1)
    segment = segment.replace(OLD_CHECK, NEW_CHECK, 1)
    changed = "".join(lines[:node.lineno-1]) + segment + "".join(lines[node.end_lineno:])
    ast.parse(changed)
    return changed, segment


def main() -> None:
    if not VIEW_PATH.is_file() or not ADAPTER_PATH.is_file():
        raise FileNotFoundError("Run from repository root after R52-R3 installation")
    current = VIEW_PATH.read_text(encoding="utf-8-sig")
    new_source, complete_class = replace_class(current)
    adapter_content = (BUNDLE / ADAPTER_PATH.name).read_text(encoding="utf-8")
    ast.parse(adapter_content)
    if "partial_result=True" not in adapter_content:
        raise RuntimeError("Partial adapter does not opt into the empty-step contract")
    installed_adapter = ADAPTER_PATH.read_text(encoding="utf-8-sig")
    if "def build_partial_web_group_proof_view(" not in installed_adapter:
        raise RuntimeError("Installed adapter is not R52-R3")
    # Write complete replacement class for inspection, never a fragment.
    (BUNDLE / "WebGroupProofView_REPLACEMENT.py.txt").write_text(
        complete_class.rstrip() + "\n", encoding="utf-8"
    )
    if new_source != current:
        backup = ROOT / "web_group_proof.phase165_r52_r3_empty_steps_backup.py"
        if backup.exists():
            raise RuntimeError("Backup already exists; refusing to overwrite")
        shutil.copy2(VIEW_PATH, backup)
        VIEW_PATH.write_text(new_source, encoding="utf-8")
        print("Updated complete WebGroupProofView class; preserved legacy steps validation")
    else:
        print("WebGroupProofView is already updated")
    if installed_adapter != adapter_content:
        adapter_backup = ROOT / "phase165_r52_r3_web_adapter.empty_steps_backup.py"
        if adapter_backup.exists():
            raise RuntimeError("Adapter backup already exists; refusing to overwrite")
        shutil.copy2(ADAPTER_PATH, adapter_backup)
        ADAPTER_PATH.write_text(adapter_content, encoding="utf-8")
        print("Updated complete partial Web adapter")
    else:
        print("Partial Web adapter is already updated")


if __name__ == "__main__":
    main()
