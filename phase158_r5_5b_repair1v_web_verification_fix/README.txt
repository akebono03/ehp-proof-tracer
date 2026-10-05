Phase 158-R5-5b repair1v — Web verification fix

状態
====
repair1v production patch applied successfully.

Focused tests:
- Phase 143 generic dependency order: 10 passed
- Phase 144 equation numbering: 3 passed
- Phase 149 local-body ordering: 8 passed
- Phase 156 relation-side normalization: 4 passed
- Phase 156 connector/local-order: 6 passed
- Phase 157 cleanup regressions: 7 passed
- Phase 158-R5-5b public ordering: 5 passed

合計 43 passed.

最後の Web 表示確認だけ、
ZIP サブディレクトリ内の Python script から実行したため、
repository root が sys.path に入らず:

ModuleNotFoundError: No module named 'web_group_proof'

で停止した。

修正
====
確認スクリプト先頭で:

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

を sys.path に追加する。

Production code:
変更なし。

Existing repository tests:
変更なし。

今回実行する内容:
1. lightweight Web verification 1件
2. pi6^3 / pi7^4 / pi15^8 public Web proof body 表示

repository-wide pytest:
実行しない。
