Phase 144-6 Public Route Cutover R2
===================================

目的
----
初回 Public Route Cutover ZIP の新規テストで発生した

ModuleNotFoundError:
No module named 'tests.test_phase143_19_method_evidence'

を修復する。

原因
----
production code の失敗ではない。
新規テストが tests ディレクトリを Python package として import したため、
実行環境の module resolution と衝突した。

変更対象
--------
tests/test_phase144_6_public_route_cutover.py

変更内容
--------
tests ディレクトリを sys.path に明示的に追加し、

from test_phase143_19_method_evidence import _method_evidence_data

として既存 helper を読み込む。

Production code changes
-----------------------
none

初回 ZIP で適用済みの
toda_group_proof_narrative_renderer.py
は変更しない。

実行
----
repository root で:

Expand-Archive `
  -Path "$HOME\Downloads\phase144_6_public_route_cutover_r2.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_public_route_cutover_r2\run_phase144_6_public_route_cutover_r2.ps1"

この R2 でも full suite は実行しない。
