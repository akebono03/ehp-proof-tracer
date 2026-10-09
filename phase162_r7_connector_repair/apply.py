from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
BACKUP = TARGET.with_name(TARGET.name + '.phase162_r7_before.bak')
NEW_FUNCTION = '''def normalize_toda_group_proof_narrative_connectors(
  markdown: str,
) -> str:
  if not isinstance(
    markdown,
    str,
  ):
    raise TypeError(
      "markdown must be a str"
    )

  paragraphs = markdown.split(
    "\\n\\n"
  )
  retained = []

  for index, paragraph in enumerate(
    paragraphs
  ):
    stripped = paragraph.strip()

    if (
      stripped == "以上より,"
      and index + 1 < len(
        paragraphs
      )
      and paragraphs[
        index + 1
      ].strip().startswith(
        "以上で得た群構造, 生成元, および写像に関する結果を合わせると,"
      )
    ):
      continue

    retained.append(
      paragraph
    )

  normalized_paragraphs = retained
  standalone_connectors = {
    "以上より,",
    "したがって,",
    "これより,",
  }
  exactness_reason_prefixes = (
    "この完全性と ",
    "完全性より,",
  )
  index = 0

  while index < len(
    normalized_paragraphs
  ) - 1:
    stripped = normalized_paragraphs[
      index
    ].strip()

    if stripped not in standalone_connectors:
      index += 1
      continue

    next_paragraph = normalized_paragraphs[
      index + 1
    ]
    next_stripped = next_paragraph.lstrip()

    if (
      stripped == "これより,"
      and next_stripped.startswith(
        exactness_reason_prefixes
      )
    ):
      normalized_paragraphs.pop(
        index
      )
      continue

    separator = (
      "\\n"
      if next_stripped.startswith(
        r"\\["
      )
      else " "
    )

    normalized_paragraphs[
      index:
      index + 2
    ] = [
      stripped
      + separator
      + next_paragraph,
    ]

  for index, paragraph in enumerate(
    normalized_paragraphs
  ):
    stripped = paragraph.strip()

    if not stripped:
      continue

    if stripped.startswith(
      "次に, "
    ):
      normalized_paragraphs[
        index
      ] = paragraph.replace(
        "次に, ",
        "まず, ",
        1,
      )

    break

  # Repeated identical discourse prefixes convey no additional proof step.
  # Preserve all following mathematical statements and reference markers.
  for index, paragraph in enumerate(normalized_paragraphs):
    leading = paragraph[:len(paragraph) - len(paragraph.lstrip())]
    content = paragraph.lstrip()
    for connector in ("これより,", "したがって,", "以上より,"):
      prefix = connector + " "
      while content.startswith(prefix + prefix):
        content = content[len(prefix):]
    normalized_paragraphs[index] = leading + content

  return "\\n\\n".join(
    normalized_paragraphs
  )
'''

def main():
    source = TARGET.read_text(encoding='utf-8-sig')
    tree = ast.parse(source)
    matches = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'normalize_toda_group_proof_narrative_connectors']
    if len(matches) != 1:
        raise RuntimeError(f'Expected one normalization function, found {len(matches)}')
    lines = source.splitlines(keepends=True)
    node = matches[0]
    existing = ''.join(lines[node.lineno - 1:node.end_lineno])
    if 'standalone_connectors' not in existing or 'exactness_reason_prefixes' not in existing:
        raise RuntimeError('Unexpected version of existing function; refusing to patch')
    changed = ''.join(lines[:node.lineno - 1]) + NEW_FUNCTION + ''.join(lines[node.end_lineno:])
    ast.parse(changed)
    if source == changed:
        print('Already up to date')
        return
    BACKUP.write_text(source, encoding='utf-8')
    TARGET.write_text(changed, encoding='utf-8')
    print('Updated:', TARGET)
    print('Backup:', BACKUP)

if __name__ == '__main__':
    main()
