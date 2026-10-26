# Phase 169 R3U1 — R3U 推論規則テストの修復

## 発生した問題

R3U は新規5テストが PASS したが、既存 R3I の `test_r3i_historical_inference_only_rules_remain_intact()` が FAIL した。歴史的 Hopf 推論規則の factory を個別に2回呼ぶため、生成された `guard` と `conclusion_builder` は別の Python 関数オブジェクトとなる。したがって `is` によるオブジェクト同一性比較は正しい検証ではない。

R3U1 では Hopf 側の比較を `.__code__ is` に変更する。元規則の数学的定義が同じ factory の同じ関数コードであることを確認するものであり、元規則、前提、guard や結論生成の実装は変更しない。Delta 側は意図した2前提の新規 guard を引き続き確認する。

## 変更対象

- `phase165_r14_r5_ehp_connection.py` の `expand_cited_ehp_terminal_goal()` 全体：R3U の変更を再適用。**R3U からの追加変更なし**。
- `phase169_r3i_cited_ehp_inference/tests/test_phase169_r3i_cited_ehp_inference.py`
- `phase169_r3i1_proof_closure_audit/tests/test_phase169_r3i_cited_ehp_inference.py`
- `phase169_r3i2_import_repair/tests/test_phase169_r3i_cited_ehp_inference.py`

以上の3テストファイルについて R3U と同じ4関数を置換。ただし R3U1 固有の修正は `test_r3i_historical_inference_only_rules_remain_intact()` の2つの比較式のみ。import 節、その他の本番ファイル、既存のクラス、Renderer、台帳、リポジトリ直下のドキュメントは変更しない。

## 実行（Windows PowerShell）

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3u1_rule_factory_identity_fix.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3u1_rule_factory_identity_fix\run.ps1"
```

以前の R3U は失敗時に自動復元済みなので、R3U ZIP の再実行は不要。

## 限定テストと完了条件

R3U 新規テスト5件、既存 R3I・R3I1・R3I2 の8件ずつ、1-stem 回帰テスト10件、計39件を **pytest プロセスを分けて** 実行する。加えて `audit.py` が実際の $\pi_5^3$ 証明木について (5.1) からの $\pi_5^5=\mathbb Z\{\iota_5\}$ を Delta 単射の前提として確認する。

エラー時は `output/` 内にバックアップした4ファイルを安全に復元する。完了の判断はユーザー環境の pytest と監査結果で行う。全体 pytest は Phase 169 終了時だけ実施。

## 次の工程との境界

$H:\pi_6^3\to\pi_6^5$ の全射性に利用する群構造の明示と $\pi_6^4$ 以降の2-stem導出は R3U1 の対象外とする。
