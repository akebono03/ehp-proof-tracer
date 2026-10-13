from pathlib import Path
import ast
import shutil

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / 'toda_group_proof_narrative_references.py'
BACKUP = Path(__file__).resolve().parent / 'backup_before_apply'
NAME = 'filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary'


def main():
    src = TARGET.read_text(encoding='utf-8')
    module = ast.parse(src)
    matching = [node for node in module.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == NAME]
    if len(matching) != 1:
        raise RuntimeError('expected exactly one reference boundary filter')
    node = matching[0]
    lines = src.splitlines(keepends=True)
    section = ''.join(lines[node.lineno - 1:node.end_lineno])
    marker = '''      if (\n        boundary is None\n        or boundary.classification\n        != TodaLiteratureStatementClassification.FIXED_STATEMENT\n      ):\n        continue\n'''
    replacement = '''      # An explicitly cited, premise-free GIVEN is an adopted source\n      # assertion, not a proof-internal derived statement. Phase 165\n      # registers these leaves without legacy fixed-rule aliases.\n      from proof import ProofRule\n      explicitly_cited_source = (\n        proof_step is not root_step\n        and proof_step.rule is ProofRule.GIVEN\n        and not proof_step.premises\n        and proof_step.inference_rule is not None\n        and proof_step.inference_rule.literature_reference is not None\n        and proof_step.inference_rule.literature_reference.locator\n        == entry.reference.locator\n      )\n      if explicitly_cited_source:\n        retained_steps.append(proof_step)\n        continue\n\n''' + marker
    if 'explicitly_cited_source = (' in section:
        print('R50 boundary fix already installed; no changes made')
        return
    if section.count(marker) != 1:
        raise RuntimeError('R50 anchor mismatch; source unchanged')
    revised = section.replace(marker, replacement)
    result = ''.join(lines[:node.lineno - 1]) + revised + ''.join(lines[node.end_lineno:])
    ast.parse(result)
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(TARGET, BACKUP / TARGET.name)
    TARGET.write_text(result, encoding='utf-8')
    print('R50 explicit GIVEN source boundary bridge installed; original backed up')


if __name__ == '__main__':
    main()
