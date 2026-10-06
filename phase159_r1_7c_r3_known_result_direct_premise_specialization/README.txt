Phase 159 R1-7c R3
====================

目的
----
pi_11^4 を代表例として、既知結果を直接前提として再利用する際に、
その既知結果の内部証明を public Narrative へ再展開しない一般規則を追加する。

同時に、root の decomposition isomorphism が必要とする direct-sum source の各成分を、
root の直接前提から必要な形へ特殊化して表示する。

期待する public proof body
--------------------------
- pi_10^3 = 0
- pi_11^7 = 0
- pi_10^3 \oplus pi_11^7 \xrightarrow{\cong} pi_11^4
- pi_11^4 = 0
- QED

表示しないもの
--------------
pi_10^3 を既知結果として使用する pi_11^4 の本文では、
pi_10^3 の内部証明である H / Delta / exactness の ancestry を再展開しない。

設計境界
--------
- pi_11^4 の group name による分岐は追加しない。
- Proposition 5.8 / Proposition 4.4 の文字列一致では発火させない。
- Proposition 4.4 の symbolic parameter i は root target の group dimension で特殊化する。
- core inference rule と bootstrap は変更しない。
- R2 で導入した equality-chain 処理は変更しない。
- 文末表現、identity equality、ord 重複、pi6_3 の短完全列冗長性は R3 の対象外。
- repository-wide pytest は実行しない。Phase 159 の最後にのみ実行する。

変更対象
--------
Production:
- toda_group_proof_narrative_contribution_renderer.py
  - homotopy_groups import
  - 新規 helper 群
  - render_toda_group_proof_narrative_multi_argument_with_contributions_markdown()
    に R3 postprocessor を1回接続

Test:
- tests/test_phase159_r1_7c_r3_known_result_direct_premise_specialization.py
  - 新規追加のみ

実行
----
PowerShell:

cd C:\Users\user\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_r1_7c_r3_known_result_direct_premise_specialization" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_r1_7c_r3_known_result_direct_premise_specialization.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_r1_7c_r3_known_result_direct_premise_specialization\run_phase159_r1_7c_r3.ps1"

完了条件
--------
1. 新規 R3 focused tests が全 PASS。
2. pi_11^4 本文に pi_10^3=0 と pi_11^7=0 が出る。
3. pi_11^4 本文に pi_10^3 \oplus pi_11^7 -> pi_11^4 の同型特殊化が出る。
4. pi_11^4 本文から pi_10^3 の H / Delta / exactness ancestry が消える。
5. pi_10^3 自身の証明では exactness が維持される。
6. pi_11^4 の core inference の3直接前提契約が壊れない。
7. full pytest は実行しない。

GitHub baseline
---------------
実装前監査は akebono03/ehp-proof-tracer の default branch を確認した。
検索結果で参照された current commit:
abed4cf3998f3f461c7fb6d93119f53d06d5fa5a
