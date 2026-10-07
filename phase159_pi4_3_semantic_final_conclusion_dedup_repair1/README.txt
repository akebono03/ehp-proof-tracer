Phase 159 pi4_3 semantic final-conclusion dedup repair1

原因
----
前回パッケージの apply script では function anchor の改行を誤って
literal "\\n" として生成したため、production code は変更されなかった。

また PowerShell は外部 python process の non-zero exit code で自動停止しないため、
apply failure 後も後続 pytest が実行された。

今回の修正
----------
1. apply script の function replacement を start/end marker 方式に修正。
2. 各 python / pytest 実行後に $LASTEXITCODE を確認し、失敗時は即停止。
3. Phase 144 の既存 failure は今回の regression 判定から除外。
4. 最終 Markdown の文字列重複削除ではなく、
   structured contribution 挿入時に semantic identity で root conclusion の再挿入を止める。

semantic identity
-----------------
Relation:
- lhs
- rhs
- relation_type

除外:
- source
- note

root conclusion が argument conclusion として既に所有されている場合、
同じ semantic key を持つ contribution は挿入しない。

変更対象
--------
新規:
- toda_group_proof_narrative_statement_identity.py
- tests/test_phase159_pi4_3_semantic_final_conclusion_dedup.py

変更:
- toda_group_proof_narrative_contribution_renderer.py
  - import
  - _insert_toda_group_proof_narrative_argument_contributions()

全体テストは実行しない。
