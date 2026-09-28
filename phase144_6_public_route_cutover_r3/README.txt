Phase 144-6 Public Route Cutover R3
===================================

監査結果
--------
R2 focused regression:
44 passed, 2 failed.

失敗した2件はいずれも
tests/test_phase135_1_web_narrative_display_math.py
に残っていた pi_6^3 legacy Narrative 固定契約だった。

旧固定契約:
- \nu'\in\pi_{6}^{3}.\tag{3}
- 「の位数を決定するために,」

R5-43 contribution-aware generic Narrative では、
式番号と文章構成は一般規則から生成されるため、
これらを固定することは public cutover と矛盾する。

一方で Phase135-2 / Phase135-3 の一般的な
inline math / display math / KaTeX 契約は PASS している。

変更対象
--------
tests/test_phase135_1_web_narrative_display_math.py

変更内容
--------
1. display math contract:
   legacy の固定 membership 式番号ではなく、
   generic Narrative に存在する EHP exact sequence が
   structured LaTeX として Web adapter に渡ることを確認する。

2. inline math contract:
   legacy 文言
   「の位数を決定するために,」
   ではなく、
   generic Narrative の
   「の位数を決定する.」
   を確認する。

Production code changes
-----------------------
none

Phase 境界
----------
Narrative の新機能追加は行わない。
Web adapter の production code も変更しない。
既存 Phase135 test を現在の generic public Narrative 契約へ合わせるだけ。

実行
----
repository root で:

Expand-Archive `
  -Path "$HOME\Downloads\phase144_6_public_route_cutover_r3.zip" `
  -DestinationPath "." `
  -Force

powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_public_route_cutover_r3\run_phase144_6_public_route_cutover_r3.ps1"

full suite はまだ実行しない。
focused regression PASS 後に Phase144-6 最終 full suite へ進む。
