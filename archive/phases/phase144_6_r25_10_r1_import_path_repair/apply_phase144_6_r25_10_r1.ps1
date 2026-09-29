$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$Target = Join-Path $ProjectRoot "phase144_6_r25_10_final_regression_ownership_audit\audit_phase144_6_r25_10.py"

if (-not (Test-Path $Target)) {
  throw "R25-10 audit script not found: $Target"
}

$Text = Get-Content -Raw -Encoding UTF8 $Target

$OldImport = @'
from dataclasses import fields,is_dataclass
import importlib,inspect
'@

$NewImport = @'
from dataclasses import fields,is_dataclass
import importlib
import importlib.util
import inspect
from pathlib import Path
import sys
'@

if (-not $Text.Contains($OldImport)) {
  throw "Expected R25-10 import block was not found."
}

$Text = $Text.Replace(
  $OldImport,
  $NewImport
)

$OldCall = @'
def call(mod,fn):
  return getattr(importlib.import_module(mod),fn)()
'@

$NewCall = @'
def load_test_module(module_name):
  prefix = "tests."

  if not module_name.startswith(prefix):
    return importlib.import_module(module_name)

  short_name = module_name[len(prefix):]
  path = (
    Path(__file__).resolve().parent.parent
    / "tests"
    / f"{short_name}.py"
  )

  if not path.is_file():
    raise ModuleNotFoundError(
      f"test module file not found: {path}"
    )

  cache_name = (
    "_phase144_6_r25_10_"
    + short_name
  )

  if cache_name in sys.modules:
    return sys.modules[cache_name]

  spec = importlib.util.spec_from_file_location(
    cache_name,
    path,
  )

  if (
    spec is None
    or spec.loader is None
  ):
    raise ImportError(
      f"cannot create module spec for {path}"
    )

  module = importlib.util.module_from_spec(
    spec
  )
  sys.modules[cache_name] = module
  spec.loader.exec_module(
    module
  )
  return module


def call(mod,fn):
  return getattr(
    load_test_module(mod),
    fn,
  )()
'@

if (-not $Text.Contains($OldCall)) {
  throw "Expected R25-10 call() block was not found."
}

$Text = $Text.Replace(
  $OldCall,
  $NewCall
)

$Text = $Text.Replace(
  'm=importlib.import_module("tests.test_phase144_6_r5_43_r2_recursive_repr_repair")',
  'm=load_test_module("tests.test_phase144_6_r5_43_r2_recursive_repr_repair")'
)

$Text = $Text.Replace(
  'm=importlib.import_module("tests.test_phase144_6_r5_43_11d_final_completion_audit")',
  'm=load_test_module("tests.test_phase144_6_r5_43_11d_final_completion_audit")'
)

$Text = $Text.Replace(
  'm=importlib.import_module("tests.test_phase144_6_r5_43_11c_r2_argument_participation_guard")',
  'm=load_test_module("tests.test_phase144_6_r5_43_11c_r2_argument_participation_guard")'
)

$Text = $Text.Replace(
  'm=importlib.import_module("tests.test_phase144_6_r5_43_3")',
  'm=load_test_module("tests.test_phase144_6_r5_43_3")'
)

Set-Content `
  -Path $Target `
  -Value $Text `
  -Encoding UTF8

Write-Host "R25-10-R1 audit import-path repair applied."
Write-Host "Production changes: none."
Write-Host "Existing tests changed: none."
