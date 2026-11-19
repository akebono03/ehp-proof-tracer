# R13R8R3 出典本文の最小修正

## 対象

- 変更対象: `phase168_r3_37c_reference_projection.py` の `_verified_source_sentence` 関数全体のみ。
- 追加: 本パッケージの `installer.py`、`verified_function_FULL.py`、`run.ps1`、テスト。

## 根拠と境界

R13R8R2 の実証で、(5.11) と (5.8) は登録 assertion と ProofStep を持つが statement_bodies が空だった。型付き wrapper を canonical source の値と厳密照合し、採用済み TeX の blob と文献位置を既存の出典ガードにより検査した場合だけ表示する。文献番号のみから新事実を導出しない。

既存の EHP 推論、GIVEN、モデル、共通 Renderer の本体、引用番号を変えない。R7 の「[R7]より」はこのパッケージの完了条件ではなく、次の引用接続監査の対象。全体 pytest は Phase 175 終了時のみ。

## 完了条件

対象 Reference の数式本文が型付き出典から正しく生成されること、誤った locator の wrapper が拒否されること、完成証明が引き続き COMPLETE であること、限定 pytest が通過すること。
