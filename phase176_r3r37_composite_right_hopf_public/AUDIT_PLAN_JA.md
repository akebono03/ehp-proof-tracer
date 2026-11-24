# Phase 176 R3R37 — 監査計画と実装境界

## 1. 対象と事前確認

GitHub `akebono03/ehp-proof-tracer` の `develop` を確認したうえで、次のコードと関連テストを確認した。

- `phase165_r52_r9_shared_math.py`：`shared_expansion_provider()` の `expand()` に R3R31 と R3R35 の公開接続がある。
- `phase176_r3r36_composite_right_hopf_isolated/source.py`：合成右因子の型検査、出典付き公式の特殊化、Hopf 値代入、共有 Provider 向け候補生成。
- `phase176_r3r36_composite_right_hopf_isolated/tests/test_source.py`：出典ガード・二前提・型安全性の独立テスト。
- `phase176_r3r35_composite_suspension_public/installer.py`：既存の additive なインストーラーの方式。
- `phase176_r3r34_composite_suspension_isolated/source.py`：懸垂合成の型付き等式。
- `phase171_r2h_prop22_cited_hopf/source.py` および `tests/test_cited_formula.py`：単一右因子の従来経路。

## 2. 変更対象

既存ファイルの変更は、`phase165_r52_r9_shared_math.py` の `shared_expansion_provider()` 内にある `expand()` に以下を追加する5行に限定する。トップレベル import は変更しない。

```python
        # Phase 176 R3R37: source-screened composite-right Hopf candidates.
        from phase176_r3r36_composite_right_hopf_isolated.source import (
            expand_cited_composite_right_hopf,
        )
        options.extend(expand_cited_composite_right_hopf(goal, tuple(available)))
```

新設位置は R3R35 の `options.extend(expand_composite_suspension_equality(goal))` の直後である。

新規ディレクトリ `phase176_r3r37_composite_right_hopf_public/` に以下を追加する。

- `installer.py`：インストール、ガード、完全な変更関数の出力、バックアップ。
- `audit.py`：選別済み出典からの公開候補と局所推論再生。
- `tests/test_installer.py`：idempotency、既存接続の保持、境界違反拒否、CRLF。
- `tests/test_public.py`：実リポジトリへの接続と回帰。
- `run.ps1`：DryRun、本実行、限定 pytest。
- `README.md`：英語。
- `AUDIT_PLAN_JA.md`、`CODE_FULL_JA.md`：日本語。

`installer.py` と `audit.py` の import は各ファイルで完結する。新規関数全文・テスト関数全文は `CODE_FULL_JA.md` に記載する。変更後の既存関数全文はインストーラーが実際の作業ツリーを読み取ったうえで `CHANGED_FUNCTION_FULL_JA.md` に出力する。

## 3. 完了条件

1. DryRun が変更なしで終了する。
2. 本実行が5行だけを追加し、二度目以降は変更しない。
3. 選別済みの Proposition 2.2 と Toda (5.3) の GIVEN から、合成右因子の公式特殊化・値代入それぞれ1候補を得る。
4. 必須の2前提を含む inference replay（局所的推論の再生）が成立する。
5. R3R35 の合成懸垂 Provider と従来の単一右因子 Provider が残る。
6. 限定 pytest と `git diff --check` が成功する。

## 4. 誤った完成宣言の防止

- `shared_dfs_source_order_gate_verified` は `False` のままとする。局所再生だけでは引用順序の検証を保証しない。
- `transport_to_eta_cube_proved`、`hopf_image_goal_proved`、`root_group_proved` は `False` のままとする。
- 新規 GIVEN・文献登録・数学規則・専用 Narrative は追加しない。
- 全体 pytest は Phase 176 の最後まで実施しない。

## 5. 次 Phase との境界

R3R38 以降で、証明済みの合成懸垂等式を Hopf 写像の引数に移す一般的な等式保存・移送と、Proposition 2.2 から最終的な Hopf 像へ至る検証を扱う。群構造の根の Goal は、EHP 完全性と核・像・生成元・位数の検証が終わるまで完成としない。
