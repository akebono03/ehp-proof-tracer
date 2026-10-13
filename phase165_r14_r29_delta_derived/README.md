# Phase 165 R14-R29

## 変更対象（全文同梱）
- 新規 `phase165_r14_r29_delta_derived.py`: `Prop42ApplicationPolicy`, `derive_adopted_tex_delta_zero`, `audit_r29`
- 新規 `test_phase165_r14_r29_delta_derived.py`: 対象6テスト
- 新規 `audit.py`, `run.ps1`, `toda_51_complete.tex`
- 既存コード、Registry、推論規則は変更しない。

## 実装
ユーザーと合意した解釈「Proposition 4.2 の一般形に明示的除外がなければ n=1 に特殊化」を `Prop42ApplicationPolicy` に明示する。章全体で n=1 が除外される証拠が判明した場合は拒否する。R23 から本当の推論による懸垂同型、R26 から型付き EHP 完全性の ProofStep を得て、R24 の既存規則 `derive_delta_zero_from_steps` から `Delta=0` の ProofStep を構成する。テストの `GIVEN` は文献固定命題を示すので、旧証明木の再生ではない。

## 完了条件
6件の対象テスト合格、Delta の結論と二つの根拠 ProofStep の保持。原典版の未照合・章前提の未独立検証・厳密な引用資格の未承認を表示する。π₃² の証明は未完成。

## 次工程
Δ=0 から H の全射や他の EHP 完全性へ向かう。共通 Backward Search の引用資格は引き続き別の完了条件。全体 pytest は Phase 165 の最後のみ。
