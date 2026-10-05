# Phase 158-R2 repair1

## 原因

R2 の focused test 失敗は2種類。

1. Phase 158 新規テストが `str.index("## 証明")` を使用していたため、
   `## 証明対象` に部分一致した。
2. pi15_8 dedicated renderer の詳細な Proposition 4.4 statement が、
   public Reference connector 後に失われた。

## Production code 変更

`toda_group_proof_narrative_renderer.py`

### 新規関数

`_phase158_preserve_dedicated_reference_detail()`

追加位置:
`_phase158_normalize_public_narrative_contract()` の直前。

### 変更関数

`render_toda_group_proof_narrative_markdown()`

変更箇所:
pi15_8 dedicated branch のみ。
canonical Reference connector の結果へ、元の dedicated Reference statement detail を保存してから
Phase 158 public shell normalization を行う。

import の変更なし。

## Test 修正

Phase 158 の section 順序テストを `splitlines().index()` に変更し、
header を完全一致で判定する。

## 実行制御

PowerShell で `$LASTEXITCODE` を検査し、
focused test が失敗した場合は audit へ進まない。

## Phase 境界

Reference attribution や数学的内容を新しく変更しない。
R2 が失わせた既存 dedicated detail の保存だけを行う。
全体 pytest は Phase 158 最終段階まで実行しない。
