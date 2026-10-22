# Phase 168 R2-6 — 命題台帳 / 共通 Bridge 全体監査

## 目的

production の命題台帳と `build_shared_typed_bridge()` の実出力を比較し、
Proposition / Lemma / Equation の typed statement（型付き主張）について次を監査する。

- typed content の有無
- 共通 Bridge への接続
- reference（出典メタデータ）の有無
- publication/component position（掲載位置）の有無
- `ProofStepLink` の有無
- `GIVEN` link の有無
- 同一 snapshot 内の重複

R2-6 では production code を変更しない。

## 実行

リポジトリ root で:

```powershell
Expand-Archive `
  -Path "$HOME\Downloads\phase168_r2_6_registry_bridge_audit.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase168_r2_6_registry_bridge_audit\run.ps1"
```

## 出力

- `output/registry_bridge_audit.json`
- `output/registry_bridge_audit.csv`

この出力を R2-7 の最小変更対象決定に使用する。
