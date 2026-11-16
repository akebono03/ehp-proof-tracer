# Phase 175 R3R5：Toda Lemma 5.7 と EHP 単射性の境界監査

## 目標と依存関係

R3R4 の独立探索では、`H(ν′η₆)=η₅²` および `π₇⁵=Z/2{η₅²}` は INFERENCE、`H:π₇³→π₇⁵` の単射性だけ UNRESOLVED となった。

数学的な必要条件は次のとおり。

$$
\pi_6^2=\mathbb Z/4\{\eta_2\nu'\},\qquad E(\eta_2\nu')=0,
$$
$$
\operatorname{im}(E:\pi_6^2\to\pi_7^3)=0,
\qquad \ker(H)=\operatorname{im}(E)=0.
$$

Toda Lemma 5.7 の一般条件は、$E^2\alpha\in2\iota_5\circ\pi_{i+2}(S^5)$ ならば $E(\eta_2\circ\alpha)=0$。$\alpha=\nu'$ の帰結は同補題の文中に明記されている。ただし、原文を見つけたことは推論木の完成と異なる。

## 変更対象（新規のみ）

リポジトリ直下に `phase175_r3r5_pi73_lemma57_frontier/` を追加する。既存ファイル・クラス・関数・import は変更しない。

- `source.py`：`source_clause_positions`、`verify_reviewed_toda_source`。
- `frontier.py`：`inspect_ehp_injectivity_frontier`。
- `audit.py`：`latest_verified_r3_report`、`scoped_preflight`、`worker`、`launch_worker`、`write_report`、`run`、`main`。
- `tests/test_source.py`、`tests/test_audit.py`、`tests/test_frontier.py`：新規の pytest。
- `run.ps1`：DryRun と本実行。
- `README.md`（英語）、この文書、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md`。

## Source Guard

1. Toda 第 V 章の Git blob `579661138928499ba04a51327f686d9b971b5314` と、作業ツリーの意味的同一性（改行差は許容）を確認する。
2. `lemma:5.7` が一意で、一般条件・特例・Lem 5.7 直後の証明が一致し、`prop:5.8` より前であることを確認する。
3. R3R4 の監査で正常な本実行が記録され、3前提のうち単射性だけが未解決だった証拠を必須とする。
4. R3R4 の R1・R2・R3 の Source Guard と Git 履歴検査を再利用し、他の追跡ファイルの変更を拒否する。
5. 実行前後で Source Guard の状態が同一であることを再検査する。

## 独立した型付き探索

1. `TodaProp42ExactnessStatement`：EHP の $E-H$ 完全性。
2. `Relation`：先行群 $\pi_6^2$ の有限巡回構造（既存結果への依存を明記）。
3. `GeneratorImage(E,\eta_2\nu',0)`：生成元の懸垂像が零。
4. `ImageZeroStatement(E)`：有限巡回群の生成元が零に写る一般規則。
5. `MapInjective(H)`：零像と完全性から Hopf 単射性を得る既存の一般規則。

どれも `SourceBoundGoal` 等を用いない限り `DIRECT_GIVEN_NOT_ACCEPTABLE` かもしれない。各前提は前提となる文献・一般命題から独立に INFERENCE で導出する必要がある。既存の `R3R4` で `π₇⁵` を source-bound にした事実と混同しない。

## pytest と完了条件

`run.ps1` が指定する新規 3 モジュールと既存の R3・R2・Hopf 単射性の限定テストだけを実行する。全体 pytest は Phase 175 終了時のみ。

- DryRun Gate：`PASS_R3R5_READ_ONLY_DRYRUN`。
- 本実行 Gate：`PASS_R3R5_LEMMA57_FRONTIER_RECORDED`。
- どちらも群の完成証明ではない。
- 新たな数学的 GIVEN、推論規則、本番 Provider、Renderer、Web 表示への変更は0件。
- 本実行後、5前提の個別 status と Open Goal は `%LOCALAPPDATA%/EHPProofTracerAudit/phase175_r3r5_pi73_lemma57_frontier/<UTC>/report.{json,md}` に保存する。

## 次工程との境界

実測に基づき、一般 Lemma 5.7 を引用つき一般命題として登録し、前提の $E^2\nu'$ に関する関係も独立に導出したうえで、$E(\eta_2\nu')=0$ の INFERENCE へ接続することを検討する。Lem 5.7 に特例が明記されているという理由だけで無検証の GIVEN を注入しない。
