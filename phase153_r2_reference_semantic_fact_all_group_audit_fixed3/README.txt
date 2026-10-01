Phase 153-R2 Follow-up
Reference / Semantic Fact All-Group Audit
=========================================

目的
----
current 112 groups に対して、literature reference を持つ leaf premise を
次の3分類へ分けて実測する。

1. reference_only
2. reference_plus_semantic_fact
3. unresolved_rendering

母集団
------
Phase 151 / Phase 152 と同じ。

- n = 2..15
- k = 0..7
- 112 groups
- proof depth = 2
- semantic closure 後の presentation

判定規則
--------
reference_only:
  provenance-only statement。

reference_plus_semantic_fact:
  provenance-only ではなく、generic renderer が rule-name / type-name /
  raw fallback を使わず意味表示できる。

unresolved_rendering:
  provenance-only ではないが、generic renderer が fallback に落ちる。
  public Narrative で rule-name を表示して埋め合わせる対象とはせず、
  semantic rendering defect として残す。

重要な境界
----------
- production code は変更しない。
- public route は変更しない。
- provenance-only catalog は変更しない。
- reference extraction / numbering は変更しない。
- statement renderer は追加しない。
- pytest 全体は実行しない。

出力
----
audit_output/reference_leaf_occurrences.csv
audit_output/reference_leaf_category_summary.csv
audit_output/reference_leaf_by_statement_type.csv
audit_output/exception_inventory.csv
audit_output/reference_leaf_summary.txt
audit_run_output.txt

この監査結果を見てから、reference marker と semantic fact の共存規則を
実装するかどうかを判断する。


Fixed1
------
最初の runner は PowerShell の $ErrorActionPreference = "Stop" により、
Python traceback の stderr 出力を NativeCommandError として途中で止めていた。

Fixed1 は production code と監査判定ロジックを変更しない。
以下だけを追加する。

- import/API preflight
- Python 実行中だけ ErrorActionPreference を Continue に変更
- stderr を stdout と合わせて全文表示・audit_run_output.txt に保存
- Python の exit code は維持して失敗を正しく返す


Fixed2
------
Fixed1 で原因を確認した結果、サブフォルダ内の audit script を直接 Python で
実行したため repository root が import path に入らず、
toda_calculation_facade を import できなかった。

Fixed2 は production code と audit 判定ロジックを変更しない。

runner のみ変更し、
- 現在の repository root を PYTHONPATH の先頭へ追加する
- preflight で toda_calculation_facade も確認する
- 実行終了時に元の PYTHONPATH を復元する

これにより repository root の production modules を参照して
同じ112群 audit を実行する。


Fixed3
------
Fixed2 で112群の監査処理自体は進行したが、最後の summary print で
Windows PowerShell の cp932 が Unicode em dash (U+2014) を出力できず
UnicodeEncodeError になった。

Fixed3 は production code と audit 判定ロジックを変更しない。

runner のみ変更し、
- PYTHONIOENCODING=utf-8
- PYTHONUTF8=1
を監査実行中だけ設定する。

終了時には元の環境変数を復元する。
