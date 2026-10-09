"""Apply the minimal R7-B public-output boundary fix, preserving backups."""
import ast
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_renderer.py'
REPLACEMENT = Path(__file__).with_name('modified_final_renderer.py').read_text(encoding='utf-8').lstrip('\n')
OLD_IMPORT = '''from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,
  link_toda_group_proof_narrative_reference_body_consumers,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_body_restatements,
)'''
NEW_IMPORT = '''from toda_group_proof_narrative_contribution_renderer import (
  _toda_group_proof_narrative_reference_statement_lines_by_number,
  build_toda_group_proof_narrative_reference_reuse_marker_by_step_id,
  link_toda_group_proof_narrative_reference_body_consumers,
  render_toda_group_proof_narrative_multi_argument_with_contributions_markdown,
  suppress_toda_group_proof_narrative_dangling_connectors,
  suppress_toda_group_proof_narrative_irrelevant_aggregate_ancestry,
  suppress_toda_group_proof_narrative_reference_body_duplicates,
  suppress_toda_group_proof_narrative_reference_body_restatements,
)'''

def main():
    source = TARGET.read_text(encoding='utf-8')
    if source.count(OLD_IMPORT) != 1:
        raise RuntimeError('Current contribution-renderer import block differs; no changes made')
    source = source.replace(OLD_IMPORT, NEW_IMPORT, 1)
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'render_toda_group_proof_narrative_markdown']
    if not candidates:
        raise RuntimeError('No public renderer found')
    node = candidates[-1]
    lines = source.splitlines(keepends=True)
    original = ''.join(lines[node.lineno-1:node.end_lineno])
    if '_phase160_r7_previous_public_narrative_renderer' not in original or 'stable_transport_narrative' not in original:
        raise RuntimeError('Latest public renderer differs from audited version; no changes made')
    updated = ''.join(lines[:node.lineno-1]) + REPLACEMENT + ''.join(lines[node.end_lineno:])
    ast.parse(updated)
    if updated.count('def render_toda_group_proof_narrative_markdown(') != source.count('def render_toda_group_proof_narrative_markdown('):
        raise RuntimeError('Renderer definition count changed unexpectedly')
    backup = TARGET.with_suffix(TARGET.suffix + '.phase162_r7b_final_boundary.bak')
    shutil.copy2(TARGET, backup)
    TARGET.write_text(updated, encoding='utf-8')
    print('Updated:', TARGET)
    print('Backup:', backup)

if __name__ == '__main__':
    main()
