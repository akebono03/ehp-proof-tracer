# Phase 175 R3R11R4 — 共通 Hopf 表示の回帰修正

## 前段実行結果と原因

R3R11R3 DryRun は `ALREADY_APPLIED` で PASS。しかし本実行は限定 pytest `34 passed, 1 failed`。失敗したのは既存の `phase172_r3_hopf_chain_display/tests/test_projection.py::test_real_public_narrative_shortens_hopf_chain_only`。すでに Phase 172 が整理した $\pi_6^3=\mathbb Z/4\{\nu'\}$ の証明本文から、`[R3]より, $E(\eta_{5})=\eta_{6}$.` が消えていた。

直接原因は、R3R11R2 の `projection.py::_verified_hopf_chain_lines()` が、より早い段階で圧縮済みの Hopf 連鎖にも二重圧縮を適用すること。合成式の根拠自体は正しいが、既存の公開文章を不必要に変更する。

## 実装前の現行コード・テストの確認

GitHub `akebono03/ehp-proof-tracer` の `develop` で、次を照合した。

- `phase171_r20r13_eta_sentence_layout/projection.py`：Blob `5deaa8886f36ec967d52b9fcd603d135ae290b39`。R3R11R1 のフックはコミット済み。
- `phase171_r20r13_eta_sentence_layout/tests/test_projection.py`：共有 Renderer の公開確認テスト。
- `phase172_r3_hopf_chain_display/projection.py`：出典・依存関係に基づく既存 Hopf 連鎖圧縮。
- `phase172_r3_hopf_chain_display/tests/test_projection.py`：今回失敗した `test_real_public_narrative_shortens_hopf_chain_only` を確認。
- `phase175_r3r11_cited_hopf_narrative/projection.py` と `tests/test_projection.py`：R3R11R1 までの GitHub 版、および配布済み R3R11R3 ZIP の実装を確認。
- `phase168_r3_5_model_renderer.py`、`phase168_r3_37c_reference_projection.py`：共通 Web 表示経路と出典本文の投影。

## 変更対象（クラス・import・関数）

1. `phase175_r3r11_cited_hopf_narrative/projection.py`
   - 変更する関数：`_verified_hopf_chain_lines()` **全文**。
   - 関数内に既存 `phase175_r3r9_lemma57_explicit_public.source` の import を追加。
   - 完成 Proof Tree 内に出典付き `TodaLemma57ExplicitNuPrimeZero` が一意に存在し、そこから `GeneratorImage` の零像が1ステップで導出されている場合にのみ追加圧縮する。
   - 数学的目標座標・参考文献番号・文字列の見た目による条件分岐は行わない。
2. `phase175_r3r11_cited_hopf_narrative/tests/test_projection.py`
   - 新規テスト（末尾に追加）：`test_pi63_phase172_hopf_display_survives_second_projector()`。
   - 新規テスト（末尾に追加）：`test_hopf_summary_requires_actual_lemma57_zero_image()`。
   - import 変更なし。
3. `phase175_r3r11_cited_hopf_narrative/audit.py`
   - `GATE`、`_public_gate()`、`run()`、`main()`：監査識別子を R3R11R4 に更新。実行する限定テストの範囲や公開証明の契約は維持。
4. `phase175_r3r11_cited_hopf_narrative/run.ps1`
   - EXIT_CODE の表示識別子を R3R11R4 に更新。
5. `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md` はすべて全文作成。

`install.py` と `full_functions/` は前回の固定済み基準を維持。**追跡済みの実装ファイルは変更しない**。R3R11R3 フォルダーの新規投影モジュールに対する最小修正に限定する。

## テスト対象・完了条件

- DryRun：`PHASE175_R3R11R4_PATCH_STATUS=ALREADY_APPLIED`、`PASS_R3R11R4_READ_ONLY_DRYRUN`、終了コード0。
- 本実行：`audit.py` の `TEST_PATHS` で限定 pytest。Phase 172 の既存テストを省略しない。
- $\pi_6^3$：従来の `[R3]より, $E(\eta_5)=\eta_6$.` と Hopf 計算の表示を保持。
- $\pi_7^3$：$E(\eta_2\nu')=0$ の出典と推論を維持し、[R5]・[R6]・[R7] による1本の等式連鎖を表示。
- 公開検索 complete、Web generic-complete-proof、Trust True、Reference 7件、Lemma 5.4 非依存。
- GIVEN の追加0、推論規則の追加0、Proof Tree の変更0。
- 最終 Gate：`PASS_R3R11R4_SINGLE_EQUATION_AND_PRIOR_NARRATIVE`。

## 次 Phase との境界

今回の変更は既存表示への干渉を防ぐもの。結論の重複行の削除、$\pi_9^5$ や $\pi_{10}^6$ の探索、新しい一般規則、全体 pytest は対象外。全体 pytest は Phase 175 の終了時に限定する。
