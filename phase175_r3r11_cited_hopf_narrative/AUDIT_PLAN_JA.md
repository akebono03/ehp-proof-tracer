# Phase 175 R3R11R1 — R3R11 の表示回帰修正

## 現行コードと既存テストの確認

- GitHub `akebono03/ehp-proof-tracer` の `develop` を確認済み。利用した既存表示フックは `phase171_r20r13_eta_sentence_layout/projection.py::format_complete_proof_sentences()`。
- 確認した既存実装・関連テスト：`phase168_r3_5_model_renderer.py`、`phase168_r3_3_proof_narrative_model.py`、`phase168_r3_37c_reference_projection.py`、`phase171_r2h_prop22_cited_hopf/source.py`、`phase171_r2i_eta_hopf_bridge/source.py`、`phase172_r3_hopf_chain_display/tests/test_projection.py`、`phase171_r20r13_eta_sentence_layout/tests/test_projection.py`、Phase 175 R3R9/R3R10 の限定テスト、Phase 174 R70 の機能テスト。
- GitHub `develop` の変更元 `phase171_r20r13_eta_sentence_layout/projection.py` blob: `77c7345f8d4c0c0c40c1059fad13de0e85e9910e`。
- R3R11 のユーザー実行：DryRun 成功、本実行で `29 passed, 3 failed`、ロールバック `RESTORED`。R3R10 の `phase168_r3_27_typed_statement_projection.py` は正当に変更された状態。

## 3 件の失敗と対処

1. **[R6] 出典本文が空**：以前は `citation.assertion_ids`・`reference_ids` の完全一致しか許していなかった。両 ID が伝搬されない引用経路でも、実際に使われた `GIVEN` の型、固有の source rule 名、`LiteratureReference.locator`、`citation.step_indices`、`step_citation_numbers` を照合して認識する。単なる同じ文字列の locator では認めない。Lemma 5.7 の厳格な ID 照合は変更しない。Proposition 2.2 の出典既知公式を正規化して表示する。
2. **Hopf 連鎖が圧縮されない**：従来は一つの定型的な中間 ProofStep の全件一致を要求していた。実際の completed root から final Hopf image を辿り、Proposition 2.2 の具体的な推論式・引用元、`H(ν′)` の `GIVEN`、`η` 懸垂の引用付き導出が祖先に含まれることを必須として緩和する。削除可能なのは同じ検証済み部分木に属する無引用の中間等式のみ。
3. **R70 の古い hash guard**：R70 は R3R10 以前の `phase168_r3_27_typed_statement_projection.py` blob を固定している。その旧 installer baseline 用テストは現在の R3R10 後の環境に適用できない。R70 のコード／テストは一切改変せず、現在も有効な R70 の７機能テストを個別指定して限定 pytest に含める。既存の Source Guard を弱めない。

## 変更対象（置換単位）

- **既存ファイル** `phase171_r20r13_eta_sentence_layout/projection.py`：`format_complete_proof_sentences()` **関数全体**の置換のみ。先頭 import・その他のクラス／関数は変更しない。これは失敗した R3R11 と同じ変更内容であり、修正版でもベースラインを保存する。
- **既存 Phase の新規パッケージ内の修正** `phase175_r3r11_cited_hopf_narrative/projection.py`：`_source_citation()`、`_reference_body_lines()`、`_verified_hopf_chain_lines()`、既存 import の `re` 追加。全関数および import の全文は `CODE_FULL_JA.md` に収録。
- 同 `audit.py`：`TEST_PATHS` と Gate を R3R11R1 用に更新。後続の `run()`・`main()` の API は変更しない。
- 同 `run.ps1`：出力 prefix を R3R11R1 に統一。
- 同 `tests/test_projection.py`：新しい出典フォールバックの陰性テストを追加。既存の失敗ケースを保持し、検証失敗時に `body` を出力する。
- 同 `README.md`、`AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`、`TEST_RESULTS_JA.md` を全文更新。
- `install.py`、`tests/test_install.py`、証明探索・出典登録・数学的推論は変更なし。

## 完了条件

- DryRun `PASS_R3R11R1_READ_ONLY_DRYRUN`、本実行限定 pytest PASS、公開 search `complete`、Trust `True`、Web `generic-complete-proof`、Reference 数 7、Lemma 5.4 の非使用。
- [R2] Lemma 5.7 の $E(\eta_2\nu')=0$ と [R6] Proposition 2.2 の $H(\alpha E\beta)=H(\alpha)E\beta$ を引用本文に表示する。
- 本文の $E(\eta_2\nu')=0$ で `\circ` を使わず、真正な Proposition 2.2 推論と最終 Hopf image を明示し、中間等式を圧縮する。
- 本実行 Gate `PASS_R3R11R1_CITED_REFERENCES_AND_HOPF_CHAIN_COMPACT`。
- 全体 pytest は Phase 175 終了時のみ行う。

## 次 Phase との境界

今回は R3R11 の表示の不具合修正だけとし、$\pi_9^5$ と $\pi_{10}^6$ の未完成証明監査や新しい一般推論規則は R4 以降に残す。
