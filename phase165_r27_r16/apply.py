from pathlib import Path
import ast
import shutil

ROOT = Path.cwd()
TARGET = ROOT / 'repository_operation_query_facade.py'
OLD = '''from proof_repository import ProofRepository
from phase164_r7_repository_root_resolution import (
  validate_repository_internal_proof_roots,
)
'''
NEW = '''from proof_repository import ProofRepository
'''
OLD_IMPORT = '''from standard_production_repository import (
  build_standard_production_proof_repository,
)
'''
OLD_FUNCTION = '''def query_standard_repository_operation_input(
  query_input: str,
) -> RepositoryOperationQueryResult:
  repository = (
    build_standard_production_proof_repository()
  )

  validate_repository_internal_proof_roots(
    repository
  )

  return query_repository_operation_input(
    repository,
    query_input,
  )
'''
NEW_FUNCTION = '''def query_standard_repository_operation_input(
  query_input: str,
) -> RepositoryOperationQueryResult:
  """Parse the query, without treating legacy bootstrap steps as proof.

  Until a certified typed-operation result is available from the common
  proof pipeline, the public operation query reports no proven matches.
  The repository-accepting API remains available for explicit callers.
  """
  query = parse_repository_operation_query(query_input)
  return RepositoryOperationQueryResult(query=query, matches=())
'''

def main():
    if not TARGET.is_file():
        raise SystemExit('Missing repository_operation_query_facade.py')
    original = TARGET.read_text(encoding='utf-8-sig')
    if NEW_FUNCTION in original and OLD_IMPORT not in original:
        print('R27-R16 already installed')
        return
    for required in (OLD, OLD_IMPORT, OLD_FUNCTION):
        if original.count(required) != 1:
            raise SystemExit('Preflight failed: unexpected local file layout; no modifications')
    changed = original.replace(OLD, NEW).replace(OLD_IMPORT,'').replace(OLD_FUNCTION,NEW_FUNCTION)
    ast.parse(changed)
    backup = TARGET.with_name('repository_operation_query_facade.phase165_r27_r16_backup.py')
    if not backup.exists():
        shutil.copy2(TARGET, backup)
    TARGET.write_text(changed,encoding='utf-8',newline='\n')
    print('R27-R16 installed: removed legacy builder from standard Operation entry')
if __name__ == '__main__': main()
