from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
BASE = Path(__file__).resolve().parent
TARGET = ROOT / 'toda_group_proof_narrative_references.py'
BACKUP = BASE / 'backup_before_apply' / TARGET.name

OLD = '''      component_keys = {
        boundary.component_key
        for proof_step in entry.proof_steps
        for boundary in (
          classify_toda_literature_statement_step(
            proof_step
          ),
        )
        if (
          boundary is not None
          and boundary.classification
          == TodaLiteratureStatementClassification.FIXED_STATEMENT
          and boundary.reference_locator
          == "(5.1)"
          and boundary.component_key is not None
        )
      }
'''
NEW = '''      component_keys = {
        boundary.component_key
        for proof_step in entry.proof_steps
        for boundary in (
          classify_toda_literature_statement_step(
            proof_step
          ),
        )
        if (
          boundary is not None
          and boundary.classification
          == TodaLiteratureStatementClassification.FIXED_STATEMENT
          and boundary.reference_locator
          == "(5.1)"
          and boundary.component_key is not None
        )
      }

      # Adopted typed GIVEN leaves carry the citation locator but not
      # the legacy fixed-rule component key. Recognize only the two
      # structurally identifiable (5.1) components, without hardcoded n.
      for proof_step in entry.proof_steps:
        inference = proof_step.inference_rule
        if (
          proof_step.premises
          or inference is None
          or inference.literature_reference is None
          or inference.literature_reference.locator != "(5.1)"
          or getattr(proof_step.rule, "name", None) != "GIVEN"
        ):
          continue
        conclusion = proof_step.conclusion
        if type(conclusion).__name__ == "TodaPrimaryGroupZeroStatement":
          group = getattr(conclusion, "group", None)
          if group is None:
            group = getattr(conclusion, "target_group", None)
          if (
            getattr(group, "sphere_dimension", None) == 1
            and isinstance(getattr(group, "group_dimension", None), int)
            and group.group_dimension > 1
          ):
            component_keys.add("circle_higher_homotopy_zero")
        elif type(conclusion).__name__ == "Relation":
          lhs = getattr(conclusion, "lhs", None)
          rhs = getattr(conclusion, "rhs", None)
          if (
            isinstance(getattr(lhs, "group_dimension", None), int)
            and lhs.group_dimension >= 1
            and lhs.group_dimension == getattr(lhs, "sphere_dimension", None)
            and type(rhs).__name__ == "FreeCyclicGroup"
          ):
            component_keys.add("diagonal_identity_group")
'''
# Proposition 4.2 is a general exactness assertion; avoid presenting three
# specialized windows as if they were three literature statements.
INSERT_ANCHOR = '''      continue

    statement_lines = (
'''
INSERT_NEW = '''      continue

    if entry.reference.locator == "Proposition 4.2":
      lines.append(
        r"$\\cdots \\to \\pi_{i-1}^{n} \\xrightarrow{E} "
        r"\\pi_{i}^{n+1} \\xrightarrow{H} "
        r"\\pi_{i}^{2n+1} \\xrightarrow{\\Delta} "
        r"\\pi_{i-2}^{n} \\xrightarrow{E} "
        r"\\pi_{i-1}^{n+1} \\to \\cdots$ は完全である."
      )
      continue

    statement_lines = (
'''

def main():
    source = TARGET.read_text(encoding='utf-8')
    tree = ast.parse(source)
    candidates = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'render_toda_group_proof_narrative_reference_entries_markdown']
    if len(candidates) != 1:
        raise RuntimeError('Renderer function not unique; no files changed')
    node = candidates[0]
    lines = source.splitlines(keepends=True)
    segment = ''.join(lines[node.lineno - 1:node.end_lineno])
    if NEW in segment and INSERT_NEW in segment:
        print('Common Reference Renderer adapter already installed')
        return
    if segment.count(OLD) != 1 or segment.count(INSERT_ANCHOR) != 1:
        raise RuntimeError('Unexpected Renderer version; no files changed')
    segment = segment.replace(OLD, NEW, 1).replace(INSERT_ANCHOR, INSERT_NEW, 1)
    updated = ''.join(lines[:node.lineno - 1]) + segment + ''.join(lines[node.end_lineno:])
    ast.parse(updated)
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP)
    TARGET.write_text(updated, encoding='utf-8')
    print('R50 existing Reference Renderer typed-source adapter installed; backup saved')

if __name__ == '__main__':
    main()
