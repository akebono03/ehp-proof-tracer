Phase 158-R5-5a repair3a — runner output-directory fix

目的
----
repair3 の diagnosis code と focused tests は正常だったが、
PowerShell runner が Python 実行前に

audit_output/console.txt

へリダイレクトしようとしたため、audit_output ディレクトリが存在せず失敗した。

今回の修正
----------
run_phase158_r5_5a_repair3.ps1 の実行前に、

New-Item -ItemType Directory -Path $OutputDir -Force

を追加し、audit_output ディレクトリを作成する。

変更対象
--------
- run_phase158_r5_5a_repair3.ps1 のみ

Production code changes
-----------------------
なし。

Diagnosis code changes
----------------------
なし。

Test code changes
-----------------
なし。

実行内容
--------
1. audit_output ディレクトリ作成
2. focused diagnosis tests
3. ordering ownership diagnosis
4. pi7_4 / pi15_8 の診断結果表示

pytest
------
focused diagnosis tests のみ。

repository-wide pytest は実行しない。
全体 pytest は Phase 158 の最後にのみ行う。

完了条件
--------
1. audit_output ディレクトリ作成エラーが発生しない。
2. focused diagnosis tests が PASS する。
3. diagnosis が最後まで実行される。
4. pi7_4.txt と pi15_8.txt が表示される。
5. production code を変更しない。
