# Phase 166 R3-Q 変更内容

## 変更対象

- `phase165_r55_nk_only_goal.py`
  - `search_group_from_registered_goal()` 関数全体を置換する。
- 新規 `phase166_r3q_web_publication_order/tests/test_phase166_r3q_web_publication_order.py`
  - R3-Q 限定テスト3件を追加する。
- 新規 `phase166_r3q_web_publication_order/apply.py`
  - 対象関数をバックアップ後に置換する導入器。
- 新規 `phase166_r3q_web_publication_order/run.ps1`
  - 導入と限定 pytest を実行する。
- 新規 `phase166_r3q_web_publication_order/README.md`
  - 実行方法を記載する。

## 実装内容

通常の `search_group_from_registered_goal()` が選択した型付き群構造目標について、その目標を供給した `FIXED_STATEMENT` の assertion ID を特定し、既存 `search_shared_group_goal()` の `citing_assertion_id` に渡す。

これにより既存の `lookup_mode="typed_reference_publication"` と `phase166_r3c_publication_order.precedes_citing_assertion()` が通常 Web 探索でも使用される。

$\pi_5^4$ は既存の Proposition 5.1 一般主張の specialization（特殊化）なので、既存 `specialize_eta_group_relation()` によって元の一般主張 assertion を掲載順境界として解決する。完成済み Proof の再利用や $\pi_5^4$ 専用の証明規則は追加しない。

## 限定 pytest

```powershell
python -m pytest -q `
  .\phase166_r3q_web_publication_order\tests\test_phase166_r3q_web_publication_order.py `
  .\phase166_r3d_pi32_regression\tests\test_phase166_r3d_pi32_regression.py
```

## 完了条件

- $\pi_3^2$ の通常 Web 完全証明が維持される。
- $\pi_4^3$ の目標境界が Proposition 5.1 の `component_position=500` になる。
- $\pi_5^4$ の目標境界が Proposition 5.1 の一般主張 `component_position=600` になる。
- 既存の共通 `precedes_citing_assertion()` が前後判定を行う。
- renderer、完成済み Proof 再利用、$\pi_5^4$ 専用証明経路を追加しない。
- 全体 pytest は実行しない。

## 次 Phase との境界

R3-Q は通常 Web 探索を統一掲載順へ接続するところまでとする。$\pi_4^3$ または $\pi_5^4$ が未完成の場合、その不足している一般規則・型付き前提・specialization 接続の修正は R3-Q の結果を確認してから次の作業として扱う。R3-Q 自体で将来の証明規則を先取りしない。
