# Phase 169 R3S — 実行方法

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase169_r3s_composite_reference_projection.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase169_r3s_composite_reference_projection\run.ps1"
```

変更対象は `phase168_r3_37c_reference_projection.py` の `project_reference_bodies()` 全体のみです。import 部分は変更しません。変更前のバックアップは `output/phase168_r3_37c_reference_projection.py.before` に保存します。

Proposition 5.1 に登録された4つの構成要素を Reference に投影します。$(5.1)$ の新しい引用や $\pi_5^5$ の前提は追加しません。

pytest は R3S の限定4件、既存 Reference 3件、既存1-stem 10件に限定します。失敗時は保存済みのファイルに復旧します。
