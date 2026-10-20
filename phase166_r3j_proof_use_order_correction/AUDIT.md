# Phase 166 R3-J 監査

- 変更: `phase165_r52_r13_reference_registration.py::build_adopted_prop51_reference`、`phase165_r55_nk_only_goal.py::search_group_from_registered_goal`、`phase165_prop51_claim_order.py::proof_ordered_prop51_items`。
- 命題内の証明使用順序: `H(η₂)=ι₃` → `π₃²` → `Δ(ι₅)` → `π₄³` → 高次 η 群。
- 複合命題の既存 API は保持し、個々の主張をリンク無しで登録する。
- 既存の `publication_position` と文献間順序判定は現時点で残る。全台帳の唯一の証明使用順序への移行は未完成。今回のパッケージを「完全統一」と呼ばない。
- 既存の R3-I ZIP は適用しない。R3-H 5 PASS の状態から使用する。
- 全体 pytest は実行しない。
