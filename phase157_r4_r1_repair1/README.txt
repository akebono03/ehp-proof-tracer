Phase157-R4-R1 repair1

原因:
- audit script を package subdirectory の path で直接起動したため、
  Python の import search path に repository root が入らなかった。
- そのため toda_calculation_facade を import できなかった。

変更:
- phase157_r4_r1_representative_boundary_audit/audit_phase157_r4_r1.py
  の先頭で repository root を sys.path に追加する。
- production code は変更しない。
- audit logic 自体も変更しない。

実行:
- representative boundary audit
- Phase157 R2/R3 周辺 focused regression

全体 pytest は Phase157 closure まで実行しない。
