"""Package author helper: assemble the complete replacement and new files."""
from pathlib import Path
from phase169_r10b_registered_stable_family_binding.patch import NEW_FUNCTION

PACKAGE = Path(__file__).resolve().parent
SECTIONS = (
    ("既存関数の置換全文（既存 import は変更しない）", "python", NEW_FUNCTION),
    ("新規モジュール全文: family_registry.py", "python", (PACKAGE / "family_registry.py").read_text(encoding="utf-8")),
    ("新規テスト関数と import の全文: tests/test_r10b_registered_family.py", "python", (PACKAGE / "tests" / "test_r10b_registered_family.py").read_text(encoding="utf-8")),
    ("パッチ全体: patch.py", "python", (PACKAGE / "patch.py").read_text(encoding="utf-8")),
    ("監査全体: audit.py", "python", (PACKAGE / "audit.py").read_text(encoding="utf-8")),
    ("Windows PowerShell 実行スクリプト全文: run.ps1", "powershell", (PACKAGE / "run.ps1").read_text(encoding="utf-8")),
)
content = "# Phase 169 R10B — 変更・追加コード全文\n\n" + "\n".join(
    "## " + title + "\n\n```" + lang + "\n" + body.rstrip() + "\n```\n"
    for title, lang, body in SECTIONS
)
(PACKAGE / "CHANGED_CODE_JA.md").write_text(content, encoding="utf-8")
