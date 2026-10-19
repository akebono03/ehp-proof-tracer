# Phase 166 R3 — 証明資格境界の監査

## 変更対象

新規 `phase166_r3_permission_audit/audit.py`：`inspect_lookup_modes()`、`inspect()`、`main()` を追加。新規 `test_audit.py`：限定監査テスト4件を追加。`run.ps1` は実行専用。

本番の `repository.py`、`proof.py`、命題台帳、共通探索、Renderer は変更しない。

## 着眼点

- R2 の `TodaFixedStatementComponent` は文献の構成要素を指すメタデータであり、型付き数学的命題の認定ではない。
- `assess_phase164_r2_citation()` は METADATA_ONLY を拒否し、独立確認、文献順、循環依存などを検査する。
- 共通探索の `lookup_mode="typed_reference"` は直接の型付き参照取得を使う。すべての経路で同じ資格条件が適用されているかは別途確認が必要。
- この監査は許可を与えない。監査で問題が見つかった場合、R3 の追加改修の対象とする。

## 完了条件

既存の対象4主張がメタデータとして扱われること、ID の承認を模した引数だけでは使用可能にならないこと、共通探索の参照取得モードの違いが可視化されること。限定テストは4件と既存の関連テストのみ。全体 pytest は R10 に残す。

## 次との境界

R3 では取得資格の安全性を検証する。関係式の逆向き展開や実際の3群の証明生成（R4〜R8）は追加しない。
