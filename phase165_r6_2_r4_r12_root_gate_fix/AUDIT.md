# Phase 165 R6-2 R4-R12 変更内容

- 対象: `phase165_r57_r11_proof_order_gate.py`
- 追加: `_is_symbolic_cited_root_specialization`（`is_unordered_root_structure_specialization` の直前）
- 置換: `is_unordered_root_structure_specialization` 全体
- import 変更: なし（関数内で必要な特殊化検証を遅延 import）
- 変更対象外: `retain_ordered_root_expansions`、正規探索本体、Web Renderer、文献台帳
- 完了条件: 対象2規則の型付き特殊化を候補として保持し、自己参照・非一致規則の拒否を維持。証明の完成は実環境で別途検証する。
- 次の境界: 正規探索と公開 Web Narrative の再検証。全体 pytest は Phase 165 終了時のみ。
