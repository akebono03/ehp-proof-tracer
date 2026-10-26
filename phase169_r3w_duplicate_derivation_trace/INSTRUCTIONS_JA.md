# 実行方法

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3w_duplicate_derivation_trace.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3w_duplicate_derivation_trace\run.ps1"
```

`R3W_CANDIDATE` と `R3W_PAIR_COMPARISON` の出力、または `output/r3w_duplicate_derivations.json` を確認する。
本番ファイルは更新しない。全体 pytest は Phase 169 終了時まで実行しない。
