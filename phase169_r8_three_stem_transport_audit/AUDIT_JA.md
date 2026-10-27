# Phase 169 R8 — 3-stem の安定輸送に必要な依存関係の監査

## これまでに確認できたこと

R7 では、限定 pytest 41件 PASS。既存の $\pi_7^5$ と $\pi_8^6$ に加え、$\pi_9^7$、$\pi_{10}^8$ も complete と表示された（ユーザー実行ログ）。

$\pi_{10}^7=\mathbb Z/8\{\nu_7\}$ は 3-stem（$k=3$, $n=7$）なので、安定範囲 $n\ge k+2$ を満たす。

ただし R7 の本番 Provider は 2-stem に限定されている。R7 一般ルールは、元の中間表記を生成し、各段階の `GeneratorImage` を**別々の証明目標**にする。したがって、型付きで候補が作れることだけでは完成証明とはいえない。

現行文献台帳には Proposition 5.6 の `pi8_5_group_relation` と `higher_nu_group_relation` が存在するが、DB・台帳での登録は証明完了を意味しない。

## 今回の監査の対象

- `phase169_r8_three_stem_transport_audit/audit.py`：新規、監査専用。
- `phase169_r8_three_stem_transport_audit/run.ps1`：新規の PowerShell 実行ファイル。
- 本番コード、既存テスト、README 等の主要文書：変更なし。

## 確認事項

1. $\pi_8^5$、$\pi_9^6$、$\pi_{10}^7$ の目標と探索状態。
2. 文献順における $\pi_8^5$ 等の先行群候補の利用資格。
3. Toda (4.5) を使った `E^r` の同型候補。
4. `\nu_5,\nu_6,\nu_7` の型付き `GeneratorImage` サブゴールが生成できるか。
5. 現行 Provider と一般輸送関数における接続状況。
6. DB の Relation を自動的な GIVEN としないこと。

## 完了条件と境界

診断の結果を `output/audit.json` と `output/audit.md` に保存し、コードの変更なしを確認する。`complete` を表示する条件は既存の Backward Search・Proof Tree・文献順検証に従う。3-stem の一般化や新しい文献規則の実装は、今回の監査結果の後に限る。

全体 pytest は Phase 169 の最後にだけ行う。
