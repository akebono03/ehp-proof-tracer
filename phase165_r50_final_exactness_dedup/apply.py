from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_contribution_renderer.py'
BACKUP = Path(__file__).resolve().parent / 'backup_before_apply' / TARGET.name
START = 'def link_toda_group_proof_narrative_reference_body_consumers('
END = 'def suppress_toda_group_proof_narrative_reference_body_restatements('
OLD = '''  return "\\n".join(
    compacted_lines
  ).strip()
'''
NEW = '''  # A cited exactness subwindow is redundant after the longer EHP
  # sequence has already been displayed in the same proof body.
  # Keep the reference marker by attaching it to the original
  # introduction rather than treating exactness as a new conclusion.
  for index in range(len(compacted_lines) - 1, -1, -1):
    line = compacted_lines[index].strip()
    match = re.match(
      r"^\\[R([0-9]+)\\]より,\\s*\\$(.+?)\\$\\s*は完全である[.。]?$",
      line,
    )
    if match is None:
      continue

    reference_number, subwindow = match.groups()
    normalized_subwindow = re.sub(
      r"\\s+", "", subwindow.replace(r"\\Delta", "Δ")
    )
    earlier_sequence_indices = []
    for earlier_index, earlier_line in enumerate(compacted_lines[:index]):
      if earlier_line.strip().startswith("[R"):
        continue
      earlier_math = re.search(r"\\$(.+?)\\$", earlier_line)
      if earlier_math is None:
        continue
      earlier_core = re.sub(
        r"\\s+", "",
        earlier_math.group(1).replace(r"\\Delta", "Δ"),
      )
      if (
        normalized_subwindow in earlier_core
        and normalized_subwindow != earlier_core
        and earlier_core.count(r"\\xrightarrow{")
        > normalized_subwindow.count(r"\\xrightarrow{")
      ):
        earlier_sequence_indices.append(earlier_index)

    if len(earlier_sequence_indices) != 1:
      continue

    introduction_indices = [
      previous_index
      for previous_index in range(earlier_sequence_indices[0])
      if "次の完全列を考える" in compacted_lines[previous_index]
    ]
    if len(introduction_indices) != 1:
      continue

    intro_index = introduction_indices[0]
    marker = "[R" + reference_number + "]"
    if marker not in compacted_lines[intro_index]:
      compacted_lines[intro_index] = (
        marker + "を用いて, " + compacted_lines[intro_index]
      )
    del compacted_lines[index]

  return "\\n".join(
    compacted_lines
  ).strip()
'''

def main():
    source = TARGET.read_text(encoding='utf-8')
    start = source.index(START)
    end = source.index(END, start)
    block = source[start:end]
    if NEW in block:
        print('R50 final dedup already installed')
        return
    if block.count(OLD) != 1:
        raise RuntimeError('unexpected current link function; no changes')
    if 'if lines[consumer_index].strip() != consumer_line.strip():' not in block:
        raise RuntimeError('R50 consumer-link guard missing; no changes')
    updated = source[:start] + block.replace(OLD, NEW, 1) + source[end:]
    ast.parse(updated, filename=str(TARGET))
    BACKUP.parent.mkdir(exist_ok=True, parents=True)
    shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(updated, encoding='utf-8')
    print('R50 final exactness-subwindow dedup installed; original backed up')

if __name__ == '__main__':
    main()
