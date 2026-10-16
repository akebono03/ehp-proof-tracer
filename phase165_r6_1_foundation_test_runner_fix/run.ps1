$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $root

$source = Join-Path $root 'phase165_r14_r36_adopted_backward.py'
if (-not (Test-Path $source)) { throw 'Source module not found' }
$check = @'
from pathlib import Path
import ast
p = Path('phase165_r14_r36_adopted_backward.py')
s = p.read_text(encoding='utf-8-sig')
t = ast.parse(s)
fn = [x for x in t.body if isinstance(x, ast.FunctionDef) and x.name == 'adopted_leaf_steps']
assert len(fn) == 1, 'adopted_leaf_steps is missing or duplicated'
segment = '\n'.join(s.splitlines()[fn[0].lineno - 1: fn[0].end_lineno])
assert 'instantiate_foundational_identity_suspension(1).statement' in segment, 'foundation index fix is not installed'
assert 'goals = backward_leaf_goals(pi32_goal())' not in segment, 'old fixed-goal dependency still present'
print('Source checks passed')
'@
$check | python -
if ($LASTEXITCODE -ne 0) { throw 'Source checks failed' }

# Separate invocations avoid pytest's duplicate test-module import mismatch.
python -m pytest -q '.\phase165_r6_1_foundation_index_fix\test_independent_source.py'
if ($LASTEXITCODE -ne 0) { throw 'Foundation index focused tests failed' }
python -m pytest -q '.\phase165_r6_1_adopted_leaves_independent\test_independent_source.py'
if ($LASTEXITCODE -ne 0) { throw 'Adopted leaf focused tests failed' }
Write-Host 'R6-1 targeted checks completed. Full pytest NOT run.'
