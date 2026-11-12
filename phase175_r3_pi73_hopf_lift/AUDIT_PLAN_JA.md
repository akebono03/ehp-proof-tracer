# Phase 175 R3R4 — R2→R3 Git 監査履歴の限定修正

## 1. 実測と問題の範囲

Windows R3R3 DryRun は限定 pytest **112 PASS**、作業ツリーの監査変更監視は PASS。
一方 `verify_lineage()` が `R3_R2_LINEAGE_NOT_AUDIT_ONLY` を返して中断した。
したがって R3R2 の独立証明探索 Worker は未実行であり、群の証明は未判定。

R2 の正常監査 report は R3 ディレクトリの Git 登録より前の HEAD を記録している。
従来の R3 `verify_lineage()` は「R2 ディレクトリ内の追加ファイル `A` のみ許容」としていたため、
R3 の監査パッケージの正常な追加まで拒否していた。

## 2. 変更対象（ファイル・関数・追加位置）

- `phase175_r3_pi73_hopf_lift/audit.py`
  - 新規定数 `R3_LINEAGE_ALLOWED_ADDITIONS`：`select_r2_report()` の後、`verify_lineage()` の直前に追加。
  - 既存関数 `verify_lineage()`：関数全文を置換。
  - import 変更なし（現行 import 全文を `CODE_FULL_JA.md` に収録）。
  - `preflight()`、`run()`、数学規則・GIVEN・Web 接続は変更しない。
- `phase175_r3_pi73_hopf_lift/tests/test_audit.py`
  - ファイル末尾に独立した実 Git DAG の4テスト関数を追加。
  - import 変更なし（全文を `CODE_FULL_JA.md` に収録）。
- `phase175_r3_pi73_hopf_lift/README.md`：英語で全文更新。
- `phase175_r3_pi73_hopf_lift/AUDIT_PLAN_JA.md`：本仕様の全文。
- `phase175_r3_pi73_hopf_lift/CODE_FULL_JA.md`：新旧コード・テストの全文。

## 3. 修正した Git 監査仕様

1. 正常な R2 本実行 report の `preflight.head` を検証する。
2. `merge-base --is-ancestor` で過去 HEAD と現 HEAD の祖先関係を確認する。
3. `git diff --name-status --no-renames` の全エントリが **追加 `A`** であることを要求する。
4. 追加場所を既存ルールどおりの `phase175_r2_k4_frontier_audit/`、または12件の名前を列挙した R3 パッケージ内のファイルに限定する。
5. R3 内の未知の追加ファイル、R3 既存ファイルのコミット変更 `M`、削除 `D`、Rename、数学コード等は従来どおり拒否する。
6. 許可したパス一覧と R3 パス一覧を `lineage` に記録する。モードは既存の `AUDIT_ONLY_DESCENDANT` を維持する。
7. 作業ツリー変更の例外は R3R3 の6監査ファイルの ` M` に限定し、ステージ済み変更・本番ファイル変更を許可しない。SHA-256 による前後検査も変更しない。
8. R1/R2/R3 の Git Blob pin と引用根拠、原則 `First Successful Proof Search` は変更しない。

Git 履歴の新規 R3 ファイルは監査・独立推論パッケージの範囲だけ。ルールが一般であることと
その ProofStep が導出されたことは別々に扱い、Proof Tree が完成したとは報告しない。

## 4. 限定テストと完了条件

ローカルの隔離された R1/R2/R3 パッケージでは `test_audit.py`、`test_rule.py`、
`test_frontier.py`、R1/R2 の監査テストについて **90 PASS、2 SKIP**。
SKIP は独立環境に本体の型付き数学モジュールがないためで、Windows では `run.ps1` が
既存の全限定テストを実行する。Python の import および構文検査は別途実施。

DryRun 完了条件：`PHASE175_R3_SOURCE_GUARD=PASS`、
`PHASE175_R3_R2_EVIDENCE=PASS`、`PHASE175_R3_R2_LINEAGE=AUDIT_ONLY_DESCENDANT`、
`PHASE175_R3_GATE=PASS_R3_READ_ONLY_DRYRUN`、実行前後の監査対象一致。

本実行では `H` の単射性、`π_7^5` の群構造、`H(ν′η_6)=η_5^2` の3前提の
独立探索を継続し、前提が欠ければ `PASS_R3_PI73_HOPF_FRONTIER_RECORDED` にとどめる。

## 5. 次工程との境界

R3R4 は Git 監査履歴の修正のみ。`rule.py`、`frontier.py`、`run.ps1`、
共有 Provider、Web Renderer、R1/R2、ルートの README・4文書は無変更。

$\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ の証明を優先し、
未完成なら各前提の未解決原因だけを次に扱う。
$\pi_9^5$ と $\pi_{10}^6$ はこの工程では扱わない。
全体 pytest は Phase 175 の終了時のみ実行する。
