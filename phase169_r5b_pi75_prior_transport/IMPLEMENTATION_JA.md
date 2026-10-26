# Phase 169 R5B — 実装・監査の範囲

## 変更対象

- `phase165_r52_r9_shared_math.py` — `shared_expansion_provider()` の内部 `expand()` に、R5B の既存規則接続を追加。import は関数内の2行を追加するだけで、モジュール先頭の import は変更しない。
- 新規 `phase169_r5b_pi75_prior_transport/rule.py` — `expand_prior_cited_toda45_composite_transport()` を追加。数学的推論規則は新設せず、既存の `toda45_composite_transport_rule` を使用する。
- 新規 `phase169_r5b_pi75_prior_transport/patch.py` — `build_patched_provider()`, `full_function()`, `main()` など。
- 新規 `phase169_r5b_pi75_prior_transport/audit.py` — `ancestors()`, `main()`。
- 新規 `phase169_r5b_pi75_prior_transport/tests/test_r5b_pi75_transport.py` — 関連6テスト。
- 新規 `phase169_r5b_pi75_prior_transport/tests/test_r5b_patch_guard.py` — 安全性3テスト。
- 新規 `phase169_r5b_pi75_prior_transport/run.ps1` — 展開後の実行用。

## 不変条件

1. $\pi_6^4$ の DB 行は証明目標であって GIVEN ではない。文献順は `resolve_prior_group_result()` で審査する。
2. 輸送元の群構造、Toda (4.5) の具体的同型、複合生成元の懸垂写像は、すべて独立した INFERENCE で証明させる。
3. 本番コードへの変更は上記1ファイルだけに限定する。既存の R3O 数学的規則、既存テスト、Renderer、文献台帳は変更しない。
4. R5B は $\pi_7^5$ に限定し、次の群を先取りしない。
5. 例外や限定テスト失敗時は変更前ファイルを復元する。全体 pytest は Phase 169 の最後だけ。

## 実行・確認

```powershell
cd C:\Users\user\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r5b_pi75_prior_transport.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r5b_pi75_prior_transport\run.ps1"
```

初回の Windows での数学的検索結果は未確認。新規純粋パッチ検査3件は開発環境でテストする。新規6件および R5A、R5、R3O、R4C の限定テストは `run.ps1` が実行する。

## 全文コード

- `output/shared_expansion_provider_FULL.py`：変更後の関数全文。
- `output/phase165_r52_r9_shared_math.py.FULL`：変更後の本番ファイル全文（import も含む）。
- `rule.py`：新規関数全文。
- `tests/*.py`：追加テスト関数と import 全文。
- `output/phase165_r52_r9_shared_math.py.before`：変更前の完全なバックアップ。

## 完了条件

$\pi_7^5=\mathbb Z/2\{\eta_5^2\}$ の公開探索が complete、未解決 Goal 0、Proof Tree と出典が検証され、Web でも `generic-complete-proof` で表示できること。証明本文の品質は必要に応じて次工程に分離する。
