# Phase 175 R4R3R2 — R4 監査コミットの HEAD 系譜検証修正

## R4R3R2 変更対象と事前確認（2026-11-17）

### 変更対象・追加位置

- `phase175_r4r3_two_summand_quotient/audit.py`：`from phase175_r4_pi95_audit.audit import git, preflight` に import 全文の当該1行を変更。`FINAL_GATE` 直後に `REVIEWED_R4_REPORT_HEAD`、`REVIEWED_R4_COMMIT`、`REVIEWED_R4_COMMIT_CHANGES` の定数を追加。`validate_r4_report()` の直前に **新規** `validate_r4_lineage()` を挿入。`run()` を関数全文置換。既存クラス・既存数学規則・既存 `validate_r4_report()` を変更しない。
- `phase175_r4r3_two_summand_quotient/tests/test_audit.py`：ファイル末尾に `test_r4_same_head_lineage_needs_no_exception()`、`reviewed_git_result()`（テスト用 helper）、`test_r4_reviewed_one_commit_is_accepted()`、拒否テスト5群を追加。既存テスト関数・import は変更しない。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`TEST_RESULTS_JA.md`、`CODE_FULL_JA.md`（日本語）の全文を更新。
- `rule.py`、`tests/test_rule.py`、`run.ps1`、`__init__.py`、既存本番 Proof Search、共有 Renderer、ルート主要5文書は変更しない。

### GitHub 現行コードと関連テストの確認

GitHub `akebono03/ehp-proof-tracer`、`develop` の比較 `c77a26fd...20622a30` を取得。差分は **1コミット**：R4監査パッケージ8ファイルの追加（`A`）と、追跡済み `.pytest_cache/v/cache/nodeids` の変更（`M`）のみ。`phase165_r52_r9_shared_math.py`、採用文献、既存の証明 API の変更はゼロ。R4R3 の `audit.py`・`tests/test_audit.py`・`run.ps1` を直前の ZIP 実体で読み、関連する既存 R4 `audit.py` およびその `tests/test_audit.py` は GitHub 上のコミット済み内容と比較した。

### 実測失敗と修正理由

ユーザーの R4R3R1 実行では限定 pytest **72 passed**。`R4R3_R4_HEAD_OR_PINS_CHANGED` は R4 本実行レポートの HEAD `c77a26fd` と実行中 HEAD `20622a30` を文字列で直接比較したために発生した。実際には前者で監査を行った直後に R4 監査パッケージが後者としてコミットされ、18 Source PIN の対象は変更されていない。

同一 HEAD の場合は従来どおり受理。異なる HEAD の場合は **`c77a26fd` → `20622a30` の組だけ**を審査し、`git rev-parse HEAD`、後者の第一親、`git diff --name-status --no-renames` を使って9ファイルの status を完全一致検査する。`phase175_r4_pi95_audit/audit.py` のその後の変更、本番の証明コードの更新、他コミットへの拡張、消去・改名・予期しないファイル増加は拒否する。

`validate_r4_report()` の HEAD 完全一致契約は弱めない。Git の実体を検証した **元の R4 レポート HEAD** を引数として渡し、従来の R4 Gate・Open Goals・先行群 trust・出典証拠の全検査を保つ。`report.json` に HEAD 移行の証拠を追加する。

### 完了条件と次段階の境界

- 限定 pytest：`tests/test_rule.py`、R4R3/R4 の同名 `tests/test_audit.py` の3ファイルのみ。`--import-mode=importlib`、cache provider 無効化を維持。
- DryRun `PASS_R4R3_ISOLATED_RULE_DRYRUN`、本実行 `PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC`。数学的事実としての $\pi_9^5$ 完成は主張しない。
- 新規 GIVEN 0件、既存隔離一般推論規則1件（**今回追加なし**）、共有 Provider への配線なし。全体 pytest 未実施。
- 次段階では出典から6前提の ProofStep を独立に導出して共有探索に接続する。今回の修正は HEAD 系譜監査のみ。

## 前段 R4R3R1 の変更対象（今回は変更なし）

- `phase175_r4r3_two_summand_quotient/run.ps1` の pytest 起動行全体：`--import-mode=importlib` を追加。
- `phase175_r4r3_two_summand_quotient/README.md`：英語の全文を更新。
- `phase175_r4r3_two_summand_quotient/AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`：日本語の全文を更新。
- `rule.py`、`audit.py`、`tests/test_rule.py`、`tests/test_audit.py`、`__init__.py`：変更しない。
- クラス・関数・メソッド・import の変更なし。既存の推論規則・証明目標・出典登録・テストケースを変更しない。

## 観測した失敗と修正

利用者の Windows `develop` では、異なるテストディレクトリに `test_audit.py` が2個あるため、pytest の既定の `prepend` import mode（import方式）によって、先に import 済みの `test_audit` と後の `test_audit.py` のパスが一致せず `import file mismatch` が発生した。

限定 pytest の実行コマンド全体に `--import-mode=importlib` を適用すると、各テストをパスに基づく固有のモジュール名で import する。ファイル名の変更、キャッシュ削除、既存テストの収集対象縮小はいずれも不要。`-p no:cacheprovider` は維持する。

**原因はテスト収集であり、数学的推論の失敗ではない。**

## 現行実装・関連テストの事前確認

- GitHub `akebono03/ehp-proof-tracer` の `develop` から `phase175_r2_k4_frontier_audit/tests/test_audit.py` と `phase174_r3_r7_r34_prior_lower_delta_source_wiring/tests/test_source.py`、`phase165_r3_recursive_search.py` を確認した。
- 今回の配布元 R4R3 ZIP 内の `run.ps1`、`tests/test_rule.py`、`tests/test_audit.py`、R4R2 の `tests/test_audit.py` を確認した。R4 パッケージは GitHub の `20622a30` にコミット済み。R4R3 の作業ファイルは直前の ZIP 実体を正とする。

## 前段 R4R3 の変更対象（今回は変更なし）

新規パッケージ `phase175_r4r3_two_summand_quotient/` のみを追加する。
既存本番ファイル、既存クラス、既存関数、既存テストは変更しない。

- `rule.py`：新規定数 `RULE_NAME`、新規関数 `two_summand_quotient_inputs()`、`two_summand_quotient_rule()`、`expand_two_summand_quotient()`。
- `audit.py`：新規関数 `r4_report_path()`、`validate_r4_report()`、`make_report_path()`、`run()`、`main()`。
- `tests/test_rule.py`：数学的型検査と ProofStep 推論照合に関する新規テスト全体。
- `tests/test_audit.py`：R4 実測報告の境界に関する新規テスト全体。
- `run.ps1`：新規の限定テスト・隔離監査実行スクリプト。
- `__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`：新規。

import は新規ファイル内の全文を `CODE_FULL_JA.md` に掲載する。
既存コードの import・クラス・関数・メソッドの差し替えはない。

## 実装前に確認した GitHub 現行コードと関連テスト

`akebono03/ehp-proof-tracer` の `develop` HEAD
`c77a26fdebe0eead67f1f7dad3a469aa446b134f` を基準とした。

- `sources/toda/Toda_05_2.tex` Proposition 5.8、(5.8)、Proposition 2.5 を使用する証明箇所。
- `phase165_r12_r2_quotient_rules.py`：既存の無限巡回群の商は今回の有限直和型には該当しない。
- `phase165_r12_r17_quotient_chain.py`：先行証明の四前提を用いる既存の商群導出。
- `phase165_r12_r5_structure_bridge.py`：巡回構造から群等式への変換は再利用可能。
- `phase165_r12_r11_prop42_unified.py`：EHP 完全列の合法な連続3項窓を検証。
- `phase169_r10e5_composite_generator_image/rule.py`：合成元の型付き端点と懸垂の連鎖を検証。
- `phase165_r52_r9_shared_math.py`：共有 Provider への既存配線を確認し、R4R3 では変更しない。
- `proof.py`：`InferenceRule`、`PremisePattern`、`ProofStep`、`apply_inference_match`、`find_inference_matches_for_rule`。
- `tests/test_phase165_r12_r2_quotient_rules.py`、`phase175_r3_pi73_hopf_lift/tests/test_rule.py`：関連テストの先行契約。
- `phase175_r4_pi95_audit/audit.py`・`tests/test_audit.py`：R4R2 の 18 Source PIN と実測境界を再利用。

## 数学的前提と一般推論

次を仮定する。

$$
C\xrightarrow{\Delta}A\xrightarrow{E}B,
\quad A=\mathbb Z/2\{a\}\oplus\mathbb Z/2\{b\},
\quad C=\mathbb Z/2\{z\}.
$$

$\Delta(z)=b$、$\operatorname{im}\Delta=\ker E$、$E$ は全射、$E(a)=y$ とする。
$C$ が $z$ で生成されるため、$\operatorname{im}\Delta=\langle b\rangle$。
ゆえに $\ker E=\langle b\rangle$ となる。
第一同型定理（first isomorphism theorem）から、

$$
B\cong A/\langle b\rangle\cong\mathbb Z/2\{y\}.
$$

$\Delta(z)=a$、$E(b)=y$ という対称な場合にも同じ推論を適用する。
この規則のコードは球面次元 $(n,k)=(5,4)$ を特別扱いしない。

## $\pi_9^5$ へ適用する際に未接続の六前提

1. 先行完成群 $\pi_8^4=\mathbb Z/2\{\nu_4\eta_7\}\oplus\mathbb Z/2\{E\nu'\eta_7\}$ の承認済み証明。
2. $\pi_{10}^9=\mathbb Z/2\{\eta_9\}$ の一般 $\eta$-family からの証明。
3. $\Delta(\eta_9)=E\nu'\eta_7$ を Proposition 2.5 と (5.8) 等から導く ProofStep。符号 $\pm$ を外す場合、該当元が位数2である根拠を必要とする。
4. Proposition 4.2 の $\pi_{10}^9\to\pi_8^4\to\pi_9^5$ に対する完全性の特殊化。
5. $E:\pi_8^4\to\pi_9^5$ の全射性。右側の $\Delta:\pi_9^9\to\pi_7^4$ の単射性と EHP 完全性から導く。
6. $E(\nu_4\eta_7)=\nu_5\eta_8$ の合成懸垂を既存の一般規則から導く。

本 R4R3 は「六前提が実際に証明されたなら結論を導く」という規則のみ追加する。
六前提の ProofStep は作成しない。公開 Group query は未完成のまま。
Toda Proposition 5.8 の結論を直接 GIVEN に追加することは禁じる。

## 出典テキストの型に関する注意

採用 TeX の Proposition 5.8 証明中で EHP 列の一項が `\pi_8^9` と表記されているが、
前後の EHP 次元との整合性を確認すると $\pi_8^4$ が対応する。
原典の文字列は編集せず、`prop42_exactness_indices()` の型検査で不正な窓を拒否する。

## R4R3R1 の実行と完了条件

限定 pytest は次の3ファイルだけを `importlib` mode で収集する。

```powershell
python -B -m pytest -q -p no:cacheprovider --import-mode=importlib `
  phase175_r4r3_two_summand_quotient/tests/test_rule.py `
  phase175_r4r3_two_summand_quotient/tests/test_audit.py `
  phase175_r4_pi95_audit/tests/test_audit.py
```

DryRun `PASS_R4R3_ISOLATED_RULE_DRYRUN`、本実行 `PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC` が完了条件。作成環境では模擬依存での全3ファイル収集が **72 passed**、独立した2個の同名 `test_audit.py` の試験でも importlib による衝突解消を確認した。実際の GitHub checkout による証明テストの実行は利用者側で確認する。

次段階は Source-first による6前提の検証可能な導出の接続であり、今回の変更に含まれない。全体 pytest は Phase 175 終了時のみ実施する。

## 検証・完了条件・次段階との境界

- 限定 pytest：新規 `tests/test_rule.py`・`tests/test_audit.py` と R4 の既存監査テスト。
- Source Guard：R3 からの ancestry、18 Source PIN、許容済み Git キャッシュだけを検査。
- R4 の本実行 Gate、HEAD 一致、実測 Open Goals 3件、$\pi_8^4$ trust verified を検証。
- Gate：`PASS_R4R3_ISOLATED_RULE_NOT_PUBLIC` は隔離一般規則の受理を意味する。
- 未実施：全体 pytest、新規 GIVEN、共有 Provider への登録、共通 Narrative 変更、$\pi_9^5$ の完成証明。
- 次段階：六前提の実際の Source-first 推論と公開接続を、個別の最小 Phase で進める。
