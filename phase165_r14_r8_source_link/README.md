# Phase 165 R14-R8 — Toda (5.1) と Prop.5.1 の出典接続

変更対象（新規のみ）:
- `phase165_r14_r8_source_link.py` — `UnverifiedSourceCandidate`, `find_pi33_source_candidate()`, `find_eta2_hopf_source_candidate()`, `expand_source_mapped_group_goal()`, `audit_source_link()` 全文
- `test_phase165_r14_r8_source_link.py` — テスト5関数全文
- `audit.py`, `run.ps1`, `README.md`

既存 API、Registry、ProofStep、Web は変更しません。

## 出典
- `π₃³ = ℤ{ι₃}`: Toda (5.1) の直後の非番号数式（ユーザー提供 TeX、原本未認証）。
- `H(η₂) = ι₃`: 既存 `hopf_facts.py` が Toda Proposition 5.1 と表記。原本から意味認証したという主張ではありません。

## 実装境界
上記の出典を混同せず、既存 R14-R7 の `expand_discovered_group_goal()` に型付き候補を渡します。共通逆向き探索が求める3前提は同型・対角群・生成元の像です。証明登録や GIVEN ProofStep 作成は行いません。未認証候補は Backward Search の *目標* であり、証明ではありません。

## 完了条件
関連テスト5件と監査が成功し、root expansion=1、ProofStep=0、認証済み前提=0を示すこと。

## 次段階
EHP exactness から Hopf 同型の根拠を展開できる一般規則、及び固定文献命題の個別意味検証と引用資格の付与。全体 pytest は Phase 終了時だけ実行。
