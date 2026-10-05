Phase 158-R5-5a — Public depth=2 audit parity repair

目的
----
R5-5 の derivation completeness audit を、実際の Web の depth=2 public Narrative
と同じ scope に合わせる。

今回の変更対象
--------------
追加のみ:

- phase158_r5_5a_public_depth2_audit_parity_repair/audit_phase158_r5_5a.py
- phase158_r5_5a_public_depth2_audit_parity_repair/test_phase158_r5_5a.py
- phase158_r5_5a_public_depth2_audit_parity_repair/run_phase158_r5_5a.ps1
- phase158_r5_5a_public_depth2_audit_parity_repair/README.txt

Production code changes
-----------------------
なし。

既存 test code changes
----------------------
なし。

監査対象
--------
R5-5 と同じ代表 9 群:

- pi_6^3
- pi_8^5
- pi_15^8
- pi_7^4
- pi_10^4
- pi_11^4
- pi_12^5
- pi_16^9
- pi_4^3

Public scope
------------
監査の表示ソースは必ず次を使う。

build_standard_web_group_proof_view(
  n,
  k,
  max_depth=2,
  mode="narrative",
)

complete replay は public output source として使わない。

proof graph の照合側も、

build_toda_group_result_proof_replay(
  group_result,
  max_depth=2,
)

に限定する。

監査契約
--------
表示される direct dependency について、

premise position < consumer position

を満たすこと。

両方が表示されていても、

consumer position < premise position

なら、

OUT_OF_ORDER_DERIVATION

として報告する。

Reference prose mapping
-----------------------
次の prefix を除去してから元 step と照合する。

- [R#]より,
- [R#]を用いて,
- [R#]を用いる.

これにより Reference marker を付けた public prose も depth=2 replay step に対応付ける。

期待する代表 defect
-------------------
少なくとも現行表示で次を検出対象とする。

pi_15^8:
  isomorphism / decomposition premise が最終群構造の consumer より後に出る derivation ordering。

pi_7^4:
  「nu_4 の分解を用いる」が
  pi_7^4 = Z{nu_4} + Z/4{E nu'} の後に出る derivation ordering。

pi_12^5:
  complete replay 由来の stale [R3] use を public depth=2 問題として誤検出しないこと。

pi_16^9:
  complete replay 由来の stale [R2] / [R5] use を public depth=2 問題として誤検出しないこと。

pytest
------
この Phase では focused test のみ。

python -m pytest ^
  phase158_r5_5a_public_depth2_audit_parity_repair/test_phase158_r5_5a.py ^
  -q

全体 pytest は実行しない。
全体テストは Phase 158 の最後にのみ行う。

完了条件
--------
1. actual Web depth=2 Narrative と audit scope が一致する。
2. complete replay にしか存在しない prose を finding にしない。
3. Reference prefix 付き prose を replay step に対応付けられる。
4. visible premise / consumer の表示順を検査できる。
5. pi_15^8 と pi_7^4 の ordering defect を検出できる。
6. production code を変更しない。
7. R5-5b の repair を先取りしない。

次 Phase との境界
-----------------
R5-5a は audit parity repair のみ。

R5-5b では、R5-5a が確認した一般的な OUT_OF_ORDER_DERIVATION だけを対象に、
renderer / presentation ordering の最小修正を検討する。

R5-5a では production renderer、proof data、semantic model を変更しない。
