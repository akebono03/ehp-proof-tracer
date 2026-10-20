# Phase 166 R3-Q：登録位置の修正

## 変更対象

- `phase166_r3p_position_binding.py`：import 部分全文を維持し、`place_r3p_reference_positions()` 関数全体を置換。
- `phase166_r3q_position_fix/tests/test_phase166_r3q_position_fix.py`：新規テスト4関数。必要な import を全文記載。
- `phase166_r3q_position_fix/install.py`：新規導入スクリプト。
- `phase166_r3q_position_fix/restore.py`：新規復旧スクリプト。
- `phase166_r3q_position_fix/run.ps1`：新規限定テスト実行用スクリプト。

完全な変更後モジュールは `phase166_r3p_position_binding.py` に、テスト関数全文は `tests/test_phase166_r3q_position_fix.py` に収録している。コード中の省略はない。

## 変更概要

分解子主張 `finite_dimensional:component:<key>` の `component_position` を、同じ数学的内容の独立登録主張の位置に合わせる。照合できない場合は例外で停止する。複合親の位置は `None` のままとする。`pi4_3` は対象複合命題の4成分には含まれないため、子主張を新設しない。

位置の未設定なその他の出典を推測して登録しない。順序ゲートや ProofStepLink は変更しない。

## 限定テストと完了条件

```powershell
python -m pytest -q phase166_r3q_position_fix/tests/test_phase166_r3q_position_fix.py phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py phase165_r52_r12_component_bridge/test_phase165_r52_r12_component_bridge.py
```

4件の新規テスト・6件の既存 Web 回帰テスト・4件の既存 component bridge テストの合格を確認する。環境上で未実行なら PASS と断定しない。失敗時は本番ファイルをバックアップから復元する。

次段階では位置未登録の Reference を別途監査し、通常 Web 探索への順序接続を検証する。全体 pytest は Phase 166 終了時のみ実施する。
