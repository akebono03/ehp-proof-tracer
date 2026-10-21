# Phase 166-3AI: 112群の証明対象変換監査

現行の DB Goal アダプターに対して、$n=2,\dots,15$、$k=0,\dots,7$ の112群を監査します。

## 変更対象

- 新規 `phase166_r3ai_112_goal_audit/audit.py`：監査関数 `audit()`、`_candidate_result()`、`main()`。
- 新規 `phase166_r3ai_112_goal_audit/tests/test_goal_audit.py`：3件の限定テスト。
- 新規 `phase166_r3ai_112_goal_audit/run.ps1`：実行スクリプト。

既存のソース、命題台帳、Renderer、証明探索は変更しません。監査では既存の `SphereRepository` と `database_group_goal_candidates()` をそのまま呼び出します。未変換の理由は候補の診断分類であり、数学的な正否判定ではありません。

## 実行

```powershell
Expand-Archive -Path "$HOME\Downloads\phase166_r3ai_112_goal_audit.zip" -DestinationPath . -Force
powershell -ExecutionPolicy Bypass -File '.\phase166_r3ai_112_goal_audit\run.ps1'
```

`phase166_r3ai_112_goal_audit/results/report.json` に112群の診断を出力します。限定 pytest だけを実行します。

## 完了条件と次段階

112件について取得元と型付き Goal 変換結果を出力し、限定テスト3件が通過すること。続く変更では、`zero_unhandled` と `unsupported` の実例を既存型と突き合わせ、安全なものだけ変換します。現在の作業で将来 Phase の推論規則や Renderer は追加しません。
