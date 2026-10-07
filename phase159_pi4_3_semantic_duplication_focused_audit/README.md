# Phase 159 pi4_3 semantic duplication focused audit

この監査は production code を変更しません。

目的は、public Narrative の末尾に

`pi_4^3 = Z/2{eta_3}`

と

`以上より, pi_4^3 = Z/2{eta_3}`

が両方出る原因を、文字列比較ではなく semantic statement（意味上の主張）単位で切り分けることです。

## 確認内容

1. raw presentation と semantic closure presentation の node 数
2. root statement と同じ semantic key を持つ ProofStep の数
3. 同じ主張を持つ ProofStep が同一 object か別 object か
4. `Relation.__eq__` では異なるが、`source` / `note` を除けば同じ主張になるケースがあるか
5. 同じ主張を含む block
6. その block を conclusion / local body として使う argument
7. その block を target とする transition
8. 現在の public Narrative

## semantic key の方針

Relation では次だけを意味内容として扱います。

- lhs
- rhs
- relation_type

次は provenance metadata（出典メタデータ）なので key から除きます。

- source
- note

Relation 以外の frozen dataclass は型と field の構造を再帰的に key 化します。

これは今回は診断用です。production 実装への導入は監査結果を見てから行います。

## 実行

PowerShell:

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Remove-Item `
  ".\phase159_pi4_3_semantic_duplication_focused_audit" `
  -Recurse `
  -Force `
  -ErrorAction SilentlyContinue

Expand-Archive `
  -Path "$HOME\Downloads\phase159_pi4_3_semantic_duplication_focused_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase159_pi4_3_semantic_duplication_focused_audit\run_phase159_pi4_3_semantic_duplication_audit.ps1"
```

全体 pytest は実行しません。
