# Phase 170 R3-R6 — Proposition 5.8 の型付き引用接続

## 現在の事実

Phase 170 R3-R5 では、Toda (5.2) の型付き群構造輸送を一般化し、$\pi_5^2$ の検索 `COMPLETE`、Web `generic-complete-proof`、限定テスト15 PASSを確認した。

一方 $\pi_7^2=\mathbb Z/2\{\eta_2\nu'\eta_6\}$ は `SEARCH_FAILED` のままである。R3-R5 の `_eta2_right_generator()` は合成写像を型付きで処理できるが、対応する源群 $\pi_7^3=\mathbb Z/2\{\nu'\eta_6\}$ の命題台帳における `Proposition 5.8` 成分は `TodaFixedStatementComponent` であり、型付き `Relation` ではない。源群の情報は `data/sphere.csv` に存在しても、それだけで `GIVEN` にはできない。

## 変更するファイル・クラス・関数

- 既存 `phase168_r2_7_4_typed_registry_bridge/phase168_r2_7_4_literature_connection.py` の import 全文と `connect_explicit_literature_components()` 関数全文を置換。クラス変更はない。
- 新規 `phase170_r3_r6_prop58_source.py` をリポジトリ直下へ追加。`_source_checked_pi73_relation()` と `register_source_checked_prop58_pi73()` を新規追加。
- 新規限定テスト `phase170_r3_r6_prop58_pi73_source/tests/test_phase170_r3_r6_source.py` を追加。必要な import とテスト関数全文を収録。
- 実行補助として同パッケージ内に `run.ps1`、`runner.py`、`verify.py`、`tests/test_offline_contract.py` を新規追加。

## 証拠と信頼境界

Toda Proposition 5.8 の archive は `source_statement_id=toda:tex:ch5:0016`、`source_sha256=4e41470cead5382bc042b39634ae4bbc9bc184cda06801ddafa1331be6f0d124` として保存されている。登録前に archive の SHA-256 と命題ラベルと主張の原文断片を確認する。

次に `database_structured_group_goal_candidates(n=3,k=4)` と `structured_generator_from_ids(ids=(3,2), start_dimension=3)` を照合する。DB は記号を構造化する役割だけで、数学的根拠は上記印刷命題に限定する。完全な原本との独立照合が完了したと主張するものではない。

既存の `boundary:Proposition 5.8:pi7_3_group_relation` の1成分だけを `METADATA_ONLY` から `STRUCTURED` に変更し、他の Proposition 5.8 成分は変更しない。原文・型付き生成元・位置の整合性のいずれかが欠ければ変更を拒否する。文献の掲載順序は従来の Manifest を再使用し、順序を捏造しない。既存 ProofStep を再生せず、Web の Trust Boundary を通過した場合だけ成功とする。

## 実行・テスト

`Expand-Archive` で展開後、先に `-DryRun` を実行する。次に本実行し、限定 pytest と $\pi_5^2,\pi_7^2$ の Web 完成証明を確認する。出力は `%LOCALAPPDATA%\EHPProofTracerRecovery` に退避する。

独立した Python contract tests は11 PASS。Windows の実際の証明検索・Web・既存テストはユーザー側で本実行するまで未確認。失敗時には R3-R6 の2ファイルの変更だけを取り消し、R3-R5 のコミット済み実装を残す。

## 次 Phase との境界

この段階では $\pi_6^2$、$\pi_8^2$、零群、直和群の一般化は行わない。次の段階は今回の実測を踏まえた `Proposition 5.8` の他成分・型付き引用整備と、一般化した (5.2) 輸送の検証とする。全体 pytest は Phase 終了時のみ実行する。

## R3-R6 HEAD 同期補正（2026-10-29）

元の `runner.py::preflight()` は、R3-R5 が未コミットであることを前提に `HEAD=32377a9...`、作業ツリーに `phase168_r2_toda52_transport.py` の未コミット差分があることを要求していた。現行 GitHub `develop` の HEAD は `970535190e160e9f2ae9e596a3ccb13abb9c913c` で、R3-R5 の成功済み実装と配布フォルダだけが前 HEAD から追加・更新されている。したがって DryRun はコードの数学的な問題ではなく古い事前条件で停止していた。

補正後は現行 HEAD、コミット済み `phase168_r2_toda52_transport.py` の Git blob `b3e104857e3a8129fb01df65ce3a38ff188ecd1f` と SHA-256 `52a89e1ab91313c33d36253d1ce67075154503934ad5fe83d5fdf08916230afe`、引用登録ファイルの Git blob `61b13a6c486132fea1fd4a0e9fcd56b86ce98cff` を一致検査する。Git index と追跡済み作業ツリーの差分がないことも要求する。

変更対象は配布パッケージ内 `phase170_r3_r6_prop58_pi73_source/runner.py::preflight()`、同じパッケージ内のテスト・README・本資料のみ。実装用の `replacement/` ファイル、`verify.py`、`run.ps1` は変更しない。既存 API も変更しない。限定 pytest と実 Web 検証は本実行のみ行う。失敗時には R3-R6 の新規変更のみ復元し、コミット済み R3-R5 を維持する。全体 pytest は Phase 終了時のみ実施する。
