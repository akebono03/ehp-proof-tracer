# Phase 174 R3-R7-R17R2：Windows Git パス監査修正

## 原因

R17R1 本実行で、R17 公開表示テスト2件 PASS、修正済み Phase 173 テスト7件 PASS となった後、Source Guard が `Unexpected tracked changes` を出した。`git diff --name-only` の相対パスは `/` 区切りだが、Windows の `str(Path)` は `\` 区切りとなるため、**同じ2ファイルを一致と判定できなかった**。

## 変更対象

- 既存パッケージ内（未追跡） `phase174_r3_r7_r17r1_historical_test_contract/audit.py`
  - `expected_tracked_paths`：新規関数。`verify_source_and_state` の直前に追加。
  - `verify_source_and_state`：期待変更パスの構築を上記関数に委譲。
- 新規 `phase174_r3_r7_r17r1r2_windows_git_path_guard_fix` 内 `patch.py`：厳密 SHA 検査と上記修正の適用・ロールバック。
- 新規 `run.ps1`：厳密な事前検査、限定テスト、既存 R17R1 スクリプトの再実行。
- 新規 `tests/test_patch.py`・`tests/test_live_guard.py`：パス比較と live 状態の限定テスト。

本番の数学的実装・ソース・Renderer・テストの内容は変更しない。古い R17R1 のテスト修正内容も変更しない。import 変更なし。

## 限定テストと完了条件

1. 新規の純粋なパス比較契約テスト 6件（パッケージ単体で PASS）。
2. `-DryRun` で旧 R17R1 の元コードと既存 Source Guard を再点検（変更なし）。
3. 本実行で監査コードだけ修正し、live パス比較テスト1件を実行。
4. 既存の R17R1 `run.ps1` をそのまま再実行。R17・Phase173 の限定 pytest、2ファイルの exact Source Guard が PASS すること。
5. 最終 Gate：`PASS_WINDOWS_GIT_PATH_GUARD_R17R1_FINAL`。

**全体 pytest は Phase 174 の最終段階のみ**。R17R2 は既存の証明探索に関与せず、`π_{12}^{7}=0` の完成を宣言しない。次の作業は `Δ` の全射性など数学的証明連鎖の監査である。
