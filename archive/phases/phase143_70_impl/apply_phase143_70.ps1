$ErrorActionPreference = "Stop"

$repo = (Get-Location).Path
$catalog = Join-Path $repo "toda_group_proof_narrative_provenance_catalog.py"
$testTarget = Join-Path $repo "tests\test_phase143_70_provenance_only_residual.py"

if (-not (Test-Path $catalog)) {
    throw "Run this script from the ehp-proof-tracer repository root."
}

$source = Get-Content -Raw -Encoding UTF8 $catalog

$oldImports = @'
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp58FiniteDimensionalStatement,
)
'@

$newImports = @'
from toda_rules import (
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
)
'@

$oldTuple = @'
TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES = (
  *REFERENCE_STATEMENT_TYPES,
  TodaProp44DecompositionMap,
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp58FiniteDimensionalStatement,
)
'@

$newTuple = @'
TODA_GROUP_PROOF_NARRATIVE_PROVENANCE_ONLY_STATEMENT_TYPES = (
  *REFERENCE_STATEMENT_TYPES,
  TodaProp44DecompositionMap,
  Toda36Lemma514SigmaDoublePrimeBridgeStatement,
  Toda515Sigma8Prop44SpecializationStatement,
  Toda56Nu4DecompositionIsomorphismStatement,
  TodaLemma513Statement,
  TodaLemma514Sigma8Statement,
  TodaLemma514SigmaDoublePrimeStatement,
  TodaLemma514SigmaPrimeStatement,
  TodaLemma54Statement,
  TodaProp51FiniteDimensionalStatement,
  TodaProp511FiniteDimensionalStatement,
  TodaProp515Pi12_5HopfIsomorphismStatement,
  TodaProp53FiniteDimensionalStatement,
  TodaProp56FiniteDimensionalStatement,
  TodaProp58FiniteDimensionalStatement,
  TodaProp59FiniteDimensionalStatement,
)
'@

if (-not $source.Contains($oldImports)) {
    throw "Expected import block not found. Your local catalog differs from the audited version."
}
if (-not $source.Contains($oldTuple)) {
    throw "Expected provenance tuple not found. Your local catalog differs from the audited version."
}

$source = $source.Replace($oldImports, $newImports)
$source = $source.Replace($oldTuple, $newTuple)
Set-Content -Path $catalog -Value $source -Encoding UTF8

Copy-Item `
  (Join-Path $PSScriptRoot "tests\test_phase143_70_provenance_only_residual.py") `
  $testTarget `
  -Force

Write-Host "Phase 143-70 files applied."
