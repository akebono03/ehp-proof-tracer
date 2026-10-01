Phase153-R3-4 Fixed1
Reference Statement Rendering Connection

初版の失敗原因
==============
R3-4 初版では Reference statement connection を
toda_group_proof_narrative_contribution_renderer.py の経路に接続した。

しかし pi_10^6 は
render_toda_group_proof_narrative_markdown() の fallback route を通るため、
public Narrative の Reference section では旧 renderer 呼び出しのままだった。

そのため:
- statement candidate helper test: PASS
- R3-3 selection rule: PASS
- public pi_10^6 statement placement: FAIL

Fixed1 の変更
=============
production:
- toda_group_proof_narrative_renderer.py のみ

変更内容:
1. 既に R3-4 初版で追加済みの
   _toda_group_proof_narrative_reference_statement_lines_by_number()
   を import する。
2. fallback route の Reference section 生成でも同 helper を使う。
3. render_toda_group_proof_narrative_reference_entries_markdown()
   に statement_lines_by_reference_number を渡す。

変更しないもの
==============
- R3-3 selection rule
- candidate 判定
- contribution route
- 本文重複 suppress
- unresolved renderer
- theorem/group specific branch
- tests

実行前提
========
R3-4 初版を実行済みであること。
今回ユーザー環境は初版の apply が完了して test だけ1件失敗した状態なので、
そのまま Fixed1 を適用する。

完了条件
========
Phase153-R3-4 targeted tests が全件 PASS。

次 Phase との境界
================
R3-4 完了後、本文との重複 suppress を別 subphase で扱う。
