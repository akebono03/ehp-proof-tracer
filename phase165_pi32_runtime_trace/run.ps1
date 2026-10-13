$ErrorActionPreference = 'Stop'
Set-Location (Split-Path -Parent $PSScriptRoot)
if (Get-Command python -ErrorAction SilentlyContinue) {
  & python (Join-Path $PSScriptRoot 'audit.py')
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
  & py -3 (Join-Path $PSScriptRoot 'audit.py')
} else {
  throw 'Python 3 is required.'
}
if ($LASTEXITCODE -ne 0) { throw 'Runtime trace returned a nonzero exit code. Review phase165_pi32_runtime_trace_output/audit.json.' }
