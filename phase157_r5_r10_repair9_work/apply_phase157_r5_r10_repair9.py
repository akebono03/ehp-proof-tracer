from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path(__file__).resolve().parent / "backup_before_apply"
BACKUP.mkdir(exist_ok=True)


def backup(path: Path) -> None:
    destination = BACKUP / path.name
    if not destination.exists():
        shutil.copy2(path, destination)


def replace_once(
    path: Path,
    old: str,
    new: str,
    label: str,
) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        print(f"Already applied: {label}")
        return
    count = text.count(old)
    if count != 1:
        raise RuntimeError(
            f"expected exactly one match for {label} in {path}, found {count}"
        )
    path.write_text(
        text.replace(old, new, 1),
        encoding="utf-8",
    )
    print(f"Applied: {label}")


phase144 = ROOT / "tests" / "test_phase144_6_r3_production_references.py"
repair12 = ROOT / "tests" / "test_phase156_r5_repair12_reference_frontier.py"
repair13 = ROOT / "tests" / "test_phase156_r5_repair13_root_reference_frontier.py"

for path in (phase144, repair12, repair13):
    if not path.exists():
        raise RuntimeError(f"missing expected file: {path}")
    backup(path)


replace_once(
    phase144,
    '''  assert "Proposition 5.3" in reference_part
  assert "Lemma 5.4" in reference_part
  assert "Proposition 5.6" in reference_part
  assert "Proposition 5.1" not in reference_part
''',
    '''  assert "Proposition 5.3" in reference_part
  assert "Lemma 5.4" not in reference_part
  assert "Proposition 5.6" in reference_part
  assert "Proposition 5.1" not in reference_part
''',
    "Phase144 public references follow Phase157 relevance pruning",
)

replace_once(
    repair12,
    '''  assert headers == [
    "(5.3)",
    "Proposition 5.3",
    "Lemma 5.4",
    "(5.2)",
  ]
''',
    '''  assert headers == [
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.6",
  ]
''',
    "Phase156 repair12 depth2 public headers follow Phase157 relevance",
)

replace_once(
    repair12,
    '''  assert "Proposition 5.1" not in headers
  assert "(5.3)" in headers
  assert "Proposition 5.3" in headers
  assert "Lemma 5.4" in headers
  assert "(5.2)" in headers
''',
    '''  assert "Proposition 5.1" not in headers
  assert "(5.3)" in headers
  assert "Proposition 5.3" in headers
  assert "Proposition 5.6" in headers
  assert "Lemma 5.4" not in headers
  assert "(5.2)" not in headers
''',
    "Phase156 repair12 depth3 public headers follow Phase157 relevance",
)

replace_once(
    repair13,
    '''  assert headers == [
    "(5.3)",
    "Proposition 5.3",
    "Lemma 5.4",
    "(5.2)",
  ]
''',
    '''  assert headers == [
    "(5.3)",
    "Proposition 5.3",
    "Proposition 5.6",
  ]
''',
    "Phase156 repair13 depth2 public headers follow Phase157 relevance",
)

replace_once(
    repair13,
    '''  assert "Proposition 5.1" not in headers
  assert "(5.3)" in headers
  assert "Proposition 5.3" in headers
  assert "Lemma 5.4" in headers
  assert "(5.2)" in headers
''',
    '''  assert "Proposition 5.1" not in headers
  assert "(5.3)" in headers
  assert "Proposition 5.3" in headers
  assert "Proposition 5.6" in headers
  assert "Lemma 5.4" not in headers
  assert "(5.2)" not in headers
''',
    "Phase156 repair13 depth3 public headers follow Phase157 relevance",
)

print("")
print("Phase157 R5-R10 repair9 patch applied successfully.")
print("Production code changes: none")
print(f"Changed: {phase144.relative_to(ROOT)}")
print(f"Changed: {repair12.relative_to(ROOT)}")
print(f"Changed: {repair13.relative_to(ROOT)}")
