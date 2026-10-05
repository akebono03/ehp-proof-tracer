Phase157-R5-R5 repair1 — audit import path correction

原因:
`python path\to\audit.py` で実行したため、Python の project import search path に
repository root が入らず、

  ModuleNotFoundError: No module named 'toda_calculation_facade'

で停止した。

変更対象:
- phase157_r5_r5_112_group_cross_audit/audit_phase157_r5_r5.py

production code:
- 変更なし

existing tests:
- 変更なし

audit logic:
- 変更なし

import 部分の変更:
`import sys` を追加し、project imports より前に:

  REPOSITORY_ROOT = Path.cwd()
  if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

を追加する。

その後、同じ Phase157-R5-R5 audit を再実行する。

pytest:
- 実行しない

full Narrative:
- 実行しない
