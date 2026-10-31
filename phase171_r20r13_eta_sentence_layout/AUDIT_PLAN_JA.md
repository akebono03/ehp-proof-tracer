# Phase 171 R20R13 — 監査と実装の境界

## 対象

- 既存変更: `phase168_r3_5_model_renderer.py` の `render_model_backed_narrative_markdown` のみ。
- 追加: `phase171_r20r13_eta_sentence_layout/projection.py` の表示用関数。
- 新規テスト: `tests/test_install.py`, `tests/test_projection.py`。
- 監査: `audit.py` は公開探索を再実行するが、数学的な証明を作らない。

## 表示仕様

連続した `GeneratorSuspension` または `GeneratorImage` の `INFERENCE` であり、証明木の根まで到達する経路に含まれ、同じ `TodaEtaFamilyGeneralDefinition` の引用が確定している場合に、既存の `E(\eta)=\eta` 表示だけを結合する。新たな式は作らない。結合位置が非連続、Reference が異なる、未証明、または数式表示が異なる場合は結合しない。

完成証明の「証明」セクションに限り、数式外のピリオドと半角空白で区切られた複数文を別段落にする。Reference セクションと部分証明は従来どおり。

## テストと完了条件

- 限定 pytest のみ実行する。
- $\pi_6^3=\mathbb{Z}/4\{\nu'\}$ の公開探索が `complete`。
- [R3] に基づく3つの懸垂等式が1つの数式行にまとめられる。
- 文献番号や数式中のピリオドを改変しない。
- 証明済みの位数4・非零性と Reference 8件が維持される。
- 新規 `GIVEN` は0、証明済み Proof Tree の移入は行わない。

次の Phase 171 Closeout までは全体 pytest を実行しない。
