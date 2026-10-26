# Phase 169 R3Y 実行手順

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3y_hopf_bound_codomain.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3y_hopf_bound_codomain\run.ps1"
```

変更は `phase165_r3_recursive_search.py` の新規 `SourceBoundGoal` と `reconstruct_registered_goal()`、`phase165_r14_r5_ehp_connection.py` の `expand_cited_ehp_terminal_goal()`、R3I 系の同型テスト3ファイルです。新規テスト・監査ファイルはパッケージ内部に限定します。

通常の証明探索では異なる出典に基づく正当な証明を統合しません。全体 pytest は Phase 169 終了時のみ実施します。
