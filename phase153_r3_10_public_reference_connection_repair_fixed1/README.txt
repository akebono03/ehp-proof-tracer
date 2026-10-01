Phase153-R3-10 Fixed1
Exact Public Reference Section Boundary

原因
====
初版では "## 証明" を substring として検索したため、
legacy/custom Narrative の "## 証明対象" に先に一致した。

その結果:
- custom route の Reference section 境界を誤認した
- テストも同じ誤認をした
- Reference entry のない群にも "## 証明" を必須とした

Fixed1
======
- section heading は splitlines() + lines.index("## 証明") で完全一致
- production helper も "## 証明対象" と "## 証明" を区別
- Reference entry が空の群は public Reference connection テスト対象外
- 初版の standard generic wrapper 修正は維持
- proof body / ownership / duplicate suppression は変更しない

変更対象
========
production:
- toda_group_proof_narrative_renderer.py
  - _phase153_r3_10_connect_public_reference_section 全体

tests:
- tests/test_phase153_r3_10_public_reference_connection_repair.py
  - 全文更新

完了条件
========
- structured Reference entry がある112-group scopeの全群で、
  selected statement が public Reference section に存在
- structured Reference marker missing = 0
- targeted regression tests PASS
- full pytest は実行しない
