# Phase 174 R3-R7-R15：残りの証明連鎖の監査

## 監査対象

- GitHub `develop` の R14 マージ済み HEAD `380a5b17414075e7ec5ebbb17c310e8dad49fa60`。
- R14 公開接続済み一般命題から $\nu_6\circ\eta_9=0$ への出典付き特殊化。
- $\pi_{10}^5$ の有限巡回構造の候補、生成元像、合成の結合、零因子、$E\pi_{10}^5=0$。
- 後続の EHP／Hopf／$\Delta$ は今回実装せず、$\pi_{12}^7=0$ の完成を宣言しない。

## 対象ファイル・関数

既存の実装ファイル・関数は変更なし。新規監査モジュール `audit.py` に `verify_git_and_sources`、`validate_r14_report`、`inspect_live_chain`、`make_report`、`main` などを追加。新規テストは `tests/test_contract.py`、`tests/test_public_frontier.py`。新規 PowerShell 実行スクリプト `run.ps1`。

## 監査の区別

1. 引用済み命題の出典付き GIVEN と、$n=6$ の INFERENCE を混同しない。
2. DB の $\pi_{10}^5$ の表示を、それだけで検証済み群構造とみなさない。
3. 隔離された一般規則の GoalExpansion を ProofStep と混同しない。
4. 公開 provider に同名規則が無い場合でも、「証明不能」とは結論しない。
5. 完全な証明木・公開目標の完成・全体 pytest の実行を宣言しない。

## 実行

PowerShell で `run.ps1 -DryRun` の後、問題なければ `run.ps1` を実行。出力の `FRONTIER_...` と `STAGE_...`、保存された JSON を確認して、次の最小一般推論規則の候補を決定する。

## 完了条件

Source Guard PASS、R14 証拠検査 PASS、限定 pytest PASS、公開・隔離ルールの型付き候補監査結果の採取。結論の証明が完成することは完了条件に含めない。
