# Phase 169 R3N 利用手順

実行場所はリポジトリの `develop` ブランチ。展開先はリポジトリ直下。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3n_prior_result_search.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3n_prior_result_search\run.ps1"
```

本 Phase の変更範囲：`phase165_r3_recursive_search.py` の `reconstruct_registered_goal` 全体、新規 `phase169_r3n_prior_result_alias.py` の2関数、新規の R3N テスト。`run.ps1` が変更後の関数全文と新規モジュール全文を `output` に保存する。import 節の変更はない。

先行証明の完成状態は一切問い合わせず、文献順を満たした既存固定命題と DB の生成元 ID のみを使う。新しい `GIVEN` を作成しない。未対応の安定 2-stem 証明は次工程に残す。全体 pytest は Phase 169 最終時に実行する。
