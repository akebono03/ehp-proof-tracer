Phase 158-R5-5a repair3 — ordering ownership diagnosis

目的
----
R5-5a repair1 / repair2 の focused test failure を受け、
pi_7^4 と pi_15^8 の derivation ordering 問題がどの層で生じているかを
推測せずに確定する。

repair1:
direct visible ProofStep edge の順序だけを監査した。
pi_7^4 は ORDERED_VISIBLE_DERIVATION となり、pi_15^8 は derivation 0 件だった。

repair2:
depth=2 proof graph 内の downstream consumer まで辿った。
それでも両群の public Narrative 上の逆転を ProofStep-to-ProofStep ordering として
検出できなかった。

したがって、問題の表示行が generic ProofStep rendering と1対1ではなく、
semantic block / narrative argument / contribution insertion / final public wrapping
のいずれかで生成・配置されている可能性を診断する。

変更対象
--------
追加のみ:

- phase158_r5_5a_repair3_ordering_ownership_diagnosis/audit_phase158_r5_5a_repair3.py
- phase158_r5_5a_repair3_ordering_ownership_diagnosis/test_phase158_r5_5a_repair3.py
- phase158_r5_5a_repair3_ordering_ownership_diagnosis/run_phase158_r5_5a_repair3.ps1
- phase158_r5_5a_repair3_ordering_ownership_diagnosis/README.txt

Production code changes
-----------------------
なし。

既存 test code changes
----------------------
なし。

診断対象
--------
- pi_7^4
- pi_15^8

出力する層
----------
1. actual public Web depth=2 Narrative body
2. depth=2 replay steps と generic rendering
3. semantic blocks
4. block dependency indices
5. generic block proof order
6. narrative arguments
7. presentation edges と premise/parent の block ownership

判断基準
--------
この repair3 では defect の自動分類をしない。

出力を見て、

A. proof graph 自体に依存関係がない
B. semantic dependency がない
C. block proof order が逆
D. block order は正しいが contribution insertion が後置される
E. generic body は正しいが final public wrapper が順序を変える

のどれかを確定する。

Phase boundary
--------------
audit/diagnosis のみ。

production renderer、presentation、proof data、semantic model は変更しない。
R5-5b の実装修正を先取りしない。

pytest
------
focused diagnosis test のみ。

repository-wide pytest は Phase 158 の最後にのみ実行する。

完了条件
--------
1. pi_7^4 と pi_15^8 の actual public body を取得できる。
2. replay / block / argument / edge の各層を同一出力で照合できる。
3. focused diagnosis test が PASS する。
4. production code を変更しない。
5. 次の repair の所有層を決めるための情報が得られる。
