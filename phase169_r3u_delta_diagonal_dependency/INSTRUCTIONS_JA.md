# Phase 169 R3U — 実行説明

## 目的

R3T で確認された (5.1) の対角群構造の特殊化を、$\Delta:\pi_5^5\to\pi_3^2$ の単射性の Proof Tree に接続する。

現在の Proposition 5.1 の複合命題のみでは単射性の説明が不足している。$\pi_5^5=\mathbb Z\{\iota_5\}$ の導出済み `ProofStep` を2番目の前提として要求する。新規の GIVEN は作らない。

## 実行

PowerShell でリポジトリ直下へ移動して実行する。

```powershell
cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof

Expand-Archive `
  -Path "$HOME\Downloads\phase169_r3u_delta_diagonal_dependency.zip" `
  -DestinationPath "." `
  -Force

powershell `
  -ExecutionPolicy Bypass `
  -File ".\phase169_r3u_delta_diagonal_dependency\run.ps1"
```

インストール対象は `phase165_r14_r5_ehp_connection.py` 内の `expand_cited_ehp_terminal_goal()` 全体と、R3I・R3I1・R3I2 で旧仕様を検査していた既存テスト各4関数だけである。その他の本番ファイル・Renderer・命題台帳・ルートドキュメントは変更しない。

## テストと自動復元

新規限定テスト5件、更新した既存 R3I・R3I1・R3I2 の限定テスト各7件、1-stem 回帰テスト10件を**別々の pytest プロセス**で実行する。その後、実際の $\pi_5^3$ の Web Narrative と Proof Tree の出典を検査する。失敗時は `output` に保存した更新前ファイルへ復元する。全体 pytest は Phase 169 終了時だけ行う。

## 完了条件

$\Delta$ 単射の直接前提が2件であり、2件目は (5.1) を GIVEN に持つ導出済み $\pi_5^5$ の群構造であること。Web Reference に (5.1) と Proposition 5.1 が存在し、完成済み $\pi_5^3$・既存1-stem群が回帰しないこと。

## 次 Phase との境界

$H:\pi_6^3\to\pi_6^5$ の全射性を説明する $\pi_6^5$ の特殊化の本文への明示や、$\pi_6^4$ 以降の 2-stem 展開はこの ZIP に含まれない。
