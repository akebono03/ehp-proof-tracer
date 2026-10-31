# Phase 172 R6：終了監査・全体テスト Gate

## 目的と境界

R2（懸垂関係の重複）、R3（Hopf 導出の冗長な途中式）、R4（全射性の重複）、R5（先行データベース Reference の表示）の改善がすべて適用された完成済み証明の状態を監査する。数学的な ProofStep、GIVEN、推論規則、DB、Reference の内部 locator は変更しない。外部から未検証の証明を導入しない。

## 事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` で現行 Renderer、Web adapter、Proof Narrative Model、R2〜R4 の Projection と関連テスト、R5 の導入済み前段、Phase 169 DB prior 検証コードとテストを確認した。ユーザーの R5 実行は `f244321029e6073d93cc8334f1780bb2988dd7af`、`PASS_R5_PRIOR_REFERENCE_DISPLAY_ONLY`、限定 pytest 6グループ PASS、既存 Renderer 1ファイルの変更のみである。

R5 は未コミット／コミット済みの両状態を検証済み Renderer バイト列で照合して受け入れる。Git の `origin/develop` とローカル HEAD の一致を要求する。レビュー済み R5 Projection、R5 テスト、R5 installer の SHA-256 一致を必須とする。

## 新規ファイル・関数

- `phase172_r6_phase_closeout/audit.py`：`command`、`checked`、`normalized`、`renderer_state`、`preflight`、`output_dir`、`env_for_pytest`、`run_focused`、`check_pi63_markdown`、`audit_public_proofs`、`count_passed_summary`、`run_full_suite_once`、`main` を新規追加する。
- `phase172_r6_phase_closeout/tests/test_gate.py`：検証部品の単体テスト6件を新規追加する。
- `phase172_r6_phase_closeout/run.ps1`：PowerShell の実行入口。
- `phase172_r6_phase_closeout/__init__.py`、`README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`：新規文書と package 定義。

既存ファイル・既存クラス・既存関数・既存 import の変更は**なし**。出力先は `%LOCALAPPDATA%\EHPProofTracerRecovery` の新規ディレクトリのみ。

## テスト順序

1. `-DryRun`：Git/Renderer/テスト事前条件のみ。pytest は実行しない。
2. `-RunCloseout`：10セットの限定 pytest を個別に実行する。R2〜R5、Phase 171 η・位数4、Phase 169 2-stem / DB prior 回帰を含む。
3. 5群 $(n,k)=(2,1),(3,1),(3,2),(4,2),(3,3)$ の実際の Web Narrative をそれぞれ照合する。`generic-complete-proof`、`partial_result=False` を要求する。
4. $\pi_6^3$ は根拠つき Backward Search、Trust Boundary、50 ProofStep、8 Reference、未解決 0、引用の不変性、R2〜R5 の表示契約、および Web 行の完全一致を確認する。
5. すべて PASS した後のみ `python -B -m pytest -q --tb=short --disable-warnings -p no:cacheprovider tests` を**1回**実行する。終了コード 0、PASS 件数が Phase 171 終了時の 3,546 件を下回らないこと、実行前後の追跡済み変更状態が不変なことを確認する。

## 記録と Gate

`closeout.json`、`focused_NN.log`、`pi_6_3_web_narrative.md`、`full_active_pytest.log` を保存する。成功時は `PHASE172_R6_RESULT=PASS_PHASE172_R6_FULL_CLOSEOUT_GATE`。失敗時は `FAIL_CLOSEOUT_GATE` とし、数学的証明や Renderer を変更せず、失敗ログを残す。

## 次 Phase と文書 Closeout の境界

R6 は証拠生成と Gate 判定だけを行い、過去の文書内容を推測して直接変更しない。結果を確認した後、`README.md`、`docs/design.md`、`docs/development_log.md`、`docs/roadmap.md`、`docs/proof_records.md` の必要な正式終了記録を**現在の全文を確認し、全文出力して**別工程で更新する。次 Phase の数学的拡張は先取りしない。
