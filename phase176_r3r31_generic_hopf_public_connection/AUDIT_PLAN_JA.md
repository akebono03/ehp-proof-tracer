# Phase 176 R3R31 — 実装・監査計画

## 対象

既存 `phase165_r52_r9_shared_math.py` の関数 `shared_expansion_provider()` に、R3R30 の一般 Hopf 代入候補を追加する。module-level import は変更しない。関数内部の import と候補追加は、既存の Toda Proposition 2.2 の特殊化呼び出しの直後に配置する。

## 数学的前提

$$
H(\alpha\circ E\beta)=H(\alpha)\circ E\beta,\quad H(\alpha)=\delta
\Longrightarrow H(\alpha\circ E\beta)=\delta\circ E\beta.
$$

両前提は `ProofStep` として独立に探索される。新しい出典、GIVEN、群構造は登録しない。

## 変更一覧

1. 既存 `phase165_r52_r9_shared_math.py` — `shared_expansion_provider()`（関数内部に4行の配線追加）。適用後の関数全文は監査先 `CHANGED_FUNCTION_FULL_JA.md` に出力する。
2. 新規 `phase176_r3r31_generic_hopf_public_connection/installer.py` — パッチ適用・前提確認。
3. 新規 `audit.py` — 共有 Provider の候補と各子 Goal を検証。
4. 新規 `tests/test_installer.py` — 5限定テスト。
5. 新規 `run.ps1`、英語 `README.md`、日本語 `AUDIT_PLAN_JA.md` および `CODE_FULL_JA.md`。

既存クラス、module-level import、他の関数は変更しない。

## テスト

`pytest -q` の限定対象：R3R31 新規テスト、R3R30 規則テスト、Proposition 2.2 関連テスト。全体テストは Phase 終了時まで実施しない。

## 完了条件

DryRun、パッチ適用、公開候補監査、限定 pytest がすべて PASS。Hopf 値の独立証明義務の解消状況は別途 JSON に記録する。候補生成だけで Proof Tree 完成とはしない。

## 次段階

R3R32 は未解決の Hopf 前提、結合性、または η 懸垂の実際の探索障害を監査・修正する。群構造の完成を先取りしない。
