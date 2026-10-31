# Phase 171 R20R13R3 — HEAD 固定ガード修正

## 原因

R20R13R2 の installer は Git HEAD が `4d2682036...` と一致することを要求した。
しかし、監査済みのファイルを後続コミットで採用しても、内容は変わらない。
そのため、ソースを一切変更せずに実行が拒否された。

## 変更対象

- `phase171_r20r13r2_multiple_blank_eta_merge/install.py`
  - 新規 `committed_projection()`：HEAD の追跡ファイルのみを読み取る。
  - `preflight()`：コミット一致の代わりに HEAD と作業ツリーの両方の内容を検査する。
- `phase171_r20r13r2_multiple_blank_eta_merge/README.md`：最新ガード方針を反映（英語）。
- `phase171_r20r13r3_content_guard_fix/`：実行スクリプト、監査、回帰テスト。

数学的規則、証明木、Reference、Web Renderer と既存の η 統合処理は変更しない。

## テスト・完了条件

- 新しい HEAD かつ既知内容：許可。
- HEAD 内の未知内容：拒否。
- 作業ツリーの未知内容：拒否。
- 修正済み状態の再実行：無変更で成功。
- Renderer hook 不在：拒否。
- 限定 pytest PASS、公開探索 COMPLETE、3式統合 TRUE、Reference 8件。

全体 pytest は Phase 171 の終了段階でだけ実行する。
