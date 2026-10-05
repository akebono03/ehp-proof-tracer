Phase 158-R5-5a repair2 — downstream ordering audit

目的
----
最初の R5-5a では actual Web depth=2 scope への parity は確認できたが、
ordering 判定を direct proof edge のみに限定したため、次の実問題を検出できなかった。

- pi_7^4:
  visible premise には direct consumer があり、その direct edge 自体は順序正常だった。
  しかし群構造という downstream consumer は premise より前に表示されていた。

- pi_15^8:
  問題となる premise と群構造の関係が direct edge ではなく、
  direct-edge 監査では derivation 0 件となった。

repair2 では production code を変更せず、audit の graph traversal だけを修正する。

変更対象
--------
追加のみ:

- phase158_r5_5a_repair2_downstream_ordering/audit_phase158_r5_5a_repair2.py
- phase158_r5_5a_repair2_downstream_ordering/test_phase158_r5_5a_repair2.py
- phase158_r5_5a_repair2_downstream_ordering/run_phase158_r5_5a_repair2.ps1
- phase158_r5_5a_repair2_downstream_ordering/README.txt

Production code changes
-----------------------
なし。

既存 test code changes
----------------------
なし。

Public output source
--------------------
actual Web と同じ:

build_standard_web_group_proof_view(
  n,
  k,
  max_depth=2,
  mode="narrative",
)

proof graph scope
-----------------
depth=2 replay に含まれる step identity のみに限定する。

build_toda_group_result_proof_replay(
  group_result,
  max_depth=2,
)

そのうえで、

extract_toda_recursive_proof_provenance(group_result)

の edge を使用し、depth=2 selected step 内だけで

premise -> parent -> ... -> downstream consumer

を辿る。

ordering contract
-----------------
表示される premise と、depth=2 graph 内で到達可能な表示される downstream consumer
について、

premise position < consumer position

を要求する。

consumer が先なら、

OUT_OF_ORDER_DERIVATION

とする。

direct edge に限らない。

Reference prose mapping
-----------------------
次の prefix を除去して step と対応付ける。

- [R#]より,
- [R#]を用いて,
- [R#]を用いる.

Phase boundary
--------------
これは audit repair のみ。

production renderer、presentation ordering、proof data、semantic model は変更しない。

R5-5b では、この監査で確認された一般的な ordering defect だけを修正対象とする。

pytest
------
focused test のみ。

python -m pytest ^
  phase158_r5_5a_repair2_downstream_ordering/test_phase158_r5_5a_repair2.py ^
  -q

repository-wide pytest は Phase 158 の最後にのみ実行する。

完了条件
--------
1. actual Web depth=2 scope を維持する。
2. direct edge だけでなく downstream consumer まで監査する。
3. pi_7^4 の ordering defect を検出する。
4. pi_15^8 の ordering defect を検出する。
5. production code を変更しない。
6. R5-5b の repair を先取りしない。
