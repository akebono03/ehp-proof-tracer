# Phase 175 R4R14R5 実装・監査計画

## 変更対象

- 新規 `phase175_r4r14r5_public_zero_transport/provider.py`: `build_public_composite_zero_transport_provider`。
- 新規 `phase175_r4r14r5_public_zero_transport/installer.py`: `git`、`expected_updated_source`、`verify_and_apply`、`main`。
- 既存 `phase165_r52_r9_shared_math.py`: `shared_expansion_provider` のみ。関数内部で Provider を追加する。import 文の追加はこの関数内部だけ。
- 新規 `tests/test_provider.py`、`tests/test_installer.py`、`run.ps1`。

## 数学的要件

既存 R4R14R4 の一般推論 $E(g)=c,\ c=0\Rightarrow E(g)=0$ のみを共有 Provider に接続する。既存 R41 のデータベース順序・出典確認は温存する。出典は Toda (5.9) に既存登録済みの一般法則 $\nu_n\eta_{n+3}=0\ (n\ge 6)$ のみ。派生命題は GIVEN にしない。

## 出典・証明ガード

Git blob と作業ツリーを照合し、既存関数1個だけを置換する。出典、生成元、写像、対象次数は型で照合する。`ProofStep` の新規注入なし。テストは限定 pytest のみ。

## 完了条件

Source Guard、追加 Provider の subgoals、共有 Provider の公開接続、型不一致の拒否、限定 pytest が PASS すること。`π_{10}^6=0` の完成証明はこの Phase の完了条件に含めない。次段階で root への EHP 接続を監査する。
