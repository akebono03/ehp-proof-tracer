# Phase 171 R20R2R3 — pytest モジュール衝突の修正

## 確認済みの原因

GitHub `develop` のルートには `phase165_r52_r15_ordered_citation.py` が存在し、`assess_citation()` と `CitationDecision.ALLOWED` に基づく正規の引用判定を実装している。

同時に、歴史的テストディレクトリ `phase165_r52_r15_ordered_citation/` の内部にも同名の `phase165_r52_r15_ordered_citation.py` が存在し、こちらは旧方式の `assess_phase164_r2_citation()` を使用している。

pytest の通常の `prepend` import では、テストを収めたディレクトリが `sys.path` の先頭に追加される。その結果、同ディレクトリ内の旧版が読み込まれ、`verified_assertion_ids=()` の場合に正当な引用が除外される。このため旧版に依存する2件が失敗した。

R20R2R2 の `KeyError: 'CitationDecision'` は診断コードが正規実装のグローバル変数の存在を仮定していたためで、旧版を読み込んだ状況と整合する。`--import-mode=importlib` では同名ディレクトリが module 名を奪う別の ImportError が出た。

## 今回の変更対象

既存の本番ファイル・既存テストは無変更。

- 新規 `phase171_r20r2r3_canonical_test_runner/anchored_pytest.py`
  - `check_canonical_import()`：正規ファイルの先読みと識別。
  - `main()`：DryRun／限定 pytest の起動。
- 新規 `phase171_r20r2r3_canonical_test_runner/run.ps1`：PowerShell 起動、ブランチ検査、終了コードの伝播。
- 新規 `README.md`（英語全文）、`IMPLEMENTATION_NOTES_JA.md`（日本語全文）、`CHANGED_CODE.md`（全文コード）。

実装上の import は全て `anchored_pytest.py` 冒頭に記載した。推論器の import や証明・引用規則は変更していない。

## 限定テスト

`-Quick` では既存テストの `test_ordered_reference_requires_only_prior_order` と `test_ordered_reference_integrates_with_backward_search` の2件のみ。

通常実行では R20R2 と同じ4ファイル：

- `phase171_r20r2_first_successful_search/tests/test_first_successful_search.py`
- `tests/test_phase165_r3_recursive_search.py`
- `phase165_r52_r15_ordered_citation/test_phase165_r52_r15_ordered_citation.py`
- `phase165_r12_r33_proof_tree_dedup/test_phase165_r12_r33_proof_tree_dedup.py`

全体 pytest は Phase 終了時まで実行しない。

## 完了条件と次工程

最初に `PHASE171_R20R2R3_CANONICAL_ANCHOR=PASS` が表示され、Quick 2件、限定26件が PASS になることを確認する。

次工程は先行する $\pi_6^5$ の証明を普通の Web 探索で再評価し、その後 $|\pi_6^3|=4$、$\nu'$ の位数4・巡回構造を検証すること。R20R2R3 はこの数学的証明の完成を宣言しない。
