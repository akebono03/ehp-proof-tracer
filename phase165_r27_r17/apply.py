from __future__ import annotations
import ast
from pathlib import Path
import shutil

ROOT = Path.cwd()
PATH = ROOT / 'repository_element_facade.py'
OLD_IMPORT = '''from standard_production_repository import (
  build_standard_production_proof_repository,
)
'''
NEW_IMPORT = '''from proof_repository import ProofRepository
'''
NEW_FUNCTION = '''def explore_standard_repository_generator_input(
  generator_input: str,
) -> RepositoryGeneratorExplorationReport:
  """Explore currently admissible occurrences without legacy bootstrap evidence.

  An empty report is not a mathematical nonexistence assertion.
  """
  generator = resolve_generator_input(generator_input)
  repository = ProofRepository()
  return explore_repository_generator(repository, generator)
'''

def main() -> None:
    if not PATH.is_file():
        raise SystemExit('Missing repository_element_facade.py')
    original = PATH.read_text(encoding='utf-8')
    if 'build_standard_production_proof_repository' not in original:
        if 'repository = ProofRepository()' in original:
            print('R27-R17 already installed')
            return
        raise SystemExit('Unexpected source: legacy function missing')
    if original.count(OLD_IMPORT) != 1:
        raise SystemExit('Preflight failed: legacy import not unique')
    tree = ast.parse(original)
    functions = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'explore_standard_repository_generator_input']
    if len(functions) != 1:
        raise SystemExit('Preflight failed: expected one public function')
    function = functions[0]
    old_body = '\n'.join(original.splitlines()[function.lineno-1:function.end_lineno])
    if 'build_standard_production_proof_repository()' not in old_body or 'explore_repository_generator(' not in old_body:
        raise SystemExit('Preflight failed: unexpected function body')
    revised = original.replace(OLD_IMPORT,'',1).replace(old_body,NEW_FUNCTION.rstrip(),1)
    if 'from proof_repository import ProofRepository' not in revised:
        raise SystemExit('Missing required ProofRepository import')
    ast.parse(revised)
    backup = ROOT / 'repository_element_facade.phase165_r27_r17_backup.py'
    if not backup.exists():
        shutil.copy2(PATH,backup)
    PATH.write_text(revised, encoding='utf-8')
    print('R27-R17 installed: legacy Generator bootstrap call removed')

if __name__ == '__main__':
    main()
