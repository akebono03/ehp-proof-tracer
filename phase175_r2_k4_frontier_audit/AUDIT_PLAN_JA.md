# Phase 175 R2 — $k=4$ 未完成3群の Source-first Frontier Audit

## 1. 前提と範囲

Phase 175 R1 のユーザー本実行から、登録済み $k=4$ の6群のうち以下の3群が `search_failed`、`proven_steps=0` だったことが確定した。

| 群 | R1 の未解決 Goal | 数学的課題 |
|---|---|---|
| $\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ | `CyclicStructureStatement`、順・逆の `Relation`（3件） | 生成元、位数、巡回群構造の検証済み推論鎖 |
| $\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\}$ | 上記と同型の3件 | 位数2の記名生成元と非自明性を含む巡回構造の推論鎖 |
| $\pi_{10}^6=0$ | `MapSurjective(Delta)`、零群 `Goal`（2件） | $\Delta:\pi_{11}^{11}\to\pi_9^5$ の全射性、EHP 完全性との接続 |

完成済みの $\pi_6^2$、$\pi_8^4$、$\pi_{11}^7$ は R1 の証拠として保持するが、R2 では再探索しない。

## 2. 出典優先の数学的依存関係

現行 GitHub `develop` で確認済みの `phase170_r3_r6_prop58_source.py` は、Toda Proposition 5.8 の $\pi_7^3$ に関する印刷節と構造化生成元の対応を検査する。

`phase174_r3_r7_r34_prior_lower_delta_source_wiring/source.py` は、Toda Proposition 5.8 と式 (5.10) の採用 TeX、出版順序 Manifest、生成元の型を照合し、次を出典付き前提として保持している。

$$
\pi_9^5=\mathbb Z/2\{\nu_5\eta_8\},\qquad
\Delta(\iota_{11})=\nu_5\eta_8.
$$

条件付きで、もしこれらが現在の $\pi_{10}^6$ の Source-first Screen に適格な出典付き前提として残り、$\pi_{11}^{11}=\mathbb Z\{\iota_{11}\}$ と EHP 完全性も独立に検証できれば、$\Delta$ の全射性を導く余地がある。

$$
\pi_{11}^{11}\xrightarrow{\Delta}\pi_9^5\xrightarrow{E}\pi_{10}^6\xrightarrow{H}\pi_{10}^{11}=0.
$$

この列で $\Delta$ が全射なら、完全性から $E=0$。$\pi_{10}^{11}=0$ なので $E$ が全射、ゆえに $\pi_{10}^6=0$ となる。ただし、**この R2 ではこれらの INFERENCE ProofStep を作らない**。

**注意**：出典の Proposition 5.8 が $\pi_9^5$ を記述していることと、$\pi_9^5$ の対象 Goal をその記載だけで独立に証明したことは異なる。自己結論の直接 GIVEN は作らない。R1 の `search_failed` を保つ。

## 3. 対象ファイル・クラス・関数

既存本番ファイル・クラス・関数の変更はゼロ。新規パッケージ `phase175_r2_k4_frontier_audit` のみを追加する。

- `audit.py`：`git`、`preflight`、`validate_r1`、`select_r1_report`、`verify_provenance`、`source_frontier`、`source_worker`、`launch_source_worker`、`write_json`、`write_markdown`、`run`、`main` を新規追加。`source_frontier` の実行時に既存の型付き Source Screen を呼び出す。
- `tests/test_audit.py`：既存 R1 証拠の厳格検査、対象3群、出典プロヴェナンス、誤った Complete 昇格防止、PIN 不一致時の拒否、ログと報告書の各限定契約テスト。
- `run.ps1`：DryRun / 本実行と限定 pytest の Windows 実行スクリプト。
- `README.md`（英語）、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`__init__.py`。

主要5文書 `README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` は一切変更しない。ここでいう新規パッケージ内の `README.md` はプロジェクトルートの README とは別物。

## 4. 検査基準

1. Git `develop`、Phase 174 終了基点、Source Guard 11+7件、追跡済み差分ゼロ。
2. R1 の6群全部の証拠、完成3件と未完成3件、Open Goal 数 $3+3+2$、未完成 ProofStep 数0、Web 未完成表示を確認。
3. 現行 source / Manifest / 型付き `Composition` に対し、Proposition 5.8 と (5.10) の前提を照合。
4. $\pi_{10}^6$ の Source-first Screen で該当 GIVEN が何件残るかを記録。無ければゼロを報告し、補完したことにしない。
5. 自由巡回群向け既存の R18 / R56 規則を有限巡回群へ誤適用しない。
6. 全体 pytest は Phase 175 の最終段階のみ。R2 は監査であり、3群の完成証明を宣言しない。

## 5. R3 への境界

R2 の結果を見て、一般的な有限巡回群の生成元像から全射性を導く既存規則・新規規則の必要性と、Source-first provider に接続する場所を選定する。$\pi_7^3$、$\pi_9^5$ に必要な独立推論が未構築なら、その不足を個別に監査する。先の Phase を先取りした数学規則や記名群専用分岐を R2 に含めない。


## 6. R2R1 — R1 監査専用マージの系譜補正（2026-11-11）

### 発生した事象

ユーザーの R2 `-DryRun` で既存限定 pytest 52 PASS の後、`R2_R1_SOURCE_LINEAGE_CHANGED` が発生した。R1 本実行時に `phase175_r1_k4_audit/` は未追跡であり、R2 時点では追跡済みとなった。GitHub `develop` の Phase 174 最終基点 `4f87fc5722e85f7365250c07e684e959b71ae8bb` からの比較により、後続変更は R1 監査ディレクトリの **新規追加8ファイルのみ**と確認した。従来の完全 HEAD 同一条件が、正当な監査専用マージも拒否する原因となっていた。

### 変更対象

- `phase175_r2_k4_frontier_audit/audit.py`：import に `re` を追加。`verify_provenance()` を関数全文置換し、`run()` を関数全文置換。ほかの関数・クラスは変更しない。
- `phase175_r2_k4_frontier_audit/tests/test_audit.py`：import に `subprocess` を追加。既存の `test_provenance_must_match_reviewed_source_pins()` を関数全文置換。祖先履歴・R1 新規追加のみの受容、他ファイル変更、履歴分岐、無効 SHA、不正 PIN の拒否と一時 Git リポジトリでの実行テストを新規追加。
- `phase175_r2_k4_frontier_audit/README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md` を全文再出力。既存 `run.ps1` は変更しない。

### 許可条件

1. R1 レポートの従来の6群・型付き Goal・固定出典 PIN・完了状態検証を維持する。
2. R1 実行時と R2 実行時で HEAD が同一なら、従来どおり認める。
3. HEAD が異なる場合、両 HEAD を40文字16進 Git SHA として検証し、`git merge-base --is-ancestor <R1 HEAD> <R2 HEAD>` 成功を要求する。
4. `git diff --name-status --no-renames <R1 HEAD> <R2 HEAD>` の全変更が `A`（新規追加）かつ `phase175_r1_k4_audit/` の内部ファイルに限ることを要求する。変更なし、変更・削除・移動・他パス追加を拒否する。
5. R1 で確認済みの本番 Source PIN 11件と R2 追加 PIN 7件、追跡ファイル不変を引き続き要求し、数学的推論や GIVEN は追加しない。

### 検証・完了条件

R2 と R1 の監査テストのローカル限定実行58 PASS。実際の一時 Git リポジトリを使った正当な追加の受容と本番ソース変更の拒否を含む。ユーザーの Windows 本実行では、R2 と R1 と R34 の限定 pytest、`PHASE175_R2_R1_LINEAGE=AUDIT_ONLY_DESCENDANT`、出典 PIN と Source Worker のチェック、`PHASE175_R2_GATE=PASS_R2_SOURCE_FRONTIER_RECORDED`、`TRACKED_UNCHANGED=True` を確認する。全体 pytest は Phase 175 終了時のみ実施。R2R1 は $\pi_7^3$ 等の群の証明を完成と宣言しない。
