# Phase 169 R3O：実行手順

## 変更対象

- `phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` のみ。トップレベル import は変更しない。
- 新規 `phase169_r3o_stable_composite_rule.py` をリポジトリ直下に追加。モジュール冒頭の import を含む全文を同梱。
- 追加位置：`shared_expansion_provider()` 内の `expand()` が `expand_finite_cyclic_relation(goal)` を呼んだ直後。
- 新規 `toda45_composite_transport_rule()` と `expand_cited_toda45_composite_transport()` の全文は `new_files/` のモジュールに収録。
- 追加限定テスト7件は `tests/test_r3o_toda45_composite_transport.py` 全文として収録。

## PowerShell

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3o_toda45_composite_transport.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3o_toda45_composite_transport\run.ps1"
```

## 検証

実行前に `develop` ブランチ、挿入位置の一意性、Python 構文を検証する。既存ファイルのバックアップを `output/` に残す。実行後、変更後の `shared_expansion_provider()` 全文と新規モジュール全文を `output/` に出力する。

限定 pytest は新規7件、R3N/R3Mの計13件、1-stem関連10件をそれぞれ独立したプロセスで実行。最後に通常の Web 経路で $\pi_5^3,\pi_6^4,\pi_7^5,\pi_8^6$ の探索結果と (4.5) の引用・実際の根の祖先を記録する。

## 完了条件

限定テストと Web 監査が成功し、$\pi_7^5$ の完成が実測で確認されること。証明木が未完成なら次の未解決 Goal を優先して調査する。先行群の `complete` 判定、先行証明再探索、文献順の変更は行わない。

## 次工程との境界

R3O は (4.5) の1回の安定輸送と合成生成元に限定する。$\pi_6^4$ のEHP証明、$\pi_8^6$ の一般反復輸送、全文 Renderer 整理、全体 pytest は行わない。
