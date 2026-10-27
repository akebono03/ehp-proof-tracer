# Phase 169 R7 — 任意回数の安定輸送規則

## 変更対象

本番変更ファイルは `phase165_r52_r9_shared_math.py` のみ。変更対象関数は `shared_expansion_provider()` の全体。新規追加は `phase169_r7_general_stable_transport/rule.py` と本パッケージのテスト、監査、パッチ・実行ファイル。

既存ファイルのトップレベル import は変更しない。`shared_expansion_provider()` の内部に新規 `from phase169_r7_general_stable_transport.rule import ...` を追加する。追加する関数は新規 `rule.py` の全文で提示し、変更後の共通 Provider 関数全文とファイル全文は実行時に `output` に保存する。

## 数学的な根拠

安定範囲 $n\ge k+2$ において、Toda (4.5) を引用して任意の正整数 $r$ の懸垂同型

$$
E^r:\pi_{n+k}^{n}\xrightarrow{\cong}\pi_{n+k+r}^{n+r}
$$

を証明する。$r=0$ は同一写像であり、新規の輸送規則の根候補は不要。

同型のもとで $\alpha$ の像は $E^r\alpha$ である。有限巡回群の生成元は同型で生成元に移る。ただし DB の特定の記号 $\beta$ と $E^r\alpha$ の一致は一般に自動的に従わない。

R7 は、DB 上の目標記号の同定が必要な場合、$r$ 個の `GeneratorImage` を独立の証明サブゴールとして要求する。中間元は `GeneratorSymbol.family/index`、`HomotopyElement` の次元、合成、和、係数を利用して候補を作るだけであり、対応を証明済みとみなさない。

## 従来処理との関係

- R5B（$r=1$）と R6A（$r=2$）の Provider は維持する。
- 共通 Provider でこれらの候補が生成されたときは、それらを優先する。多重導出による既存証明の曖昧化を避ける。
- 数学的な共通輸送規則は stem で分岐しない。
- 今回の本番接続の対象は 2-stem の有限巡回群の根目標のみ。1-stem と 3-stem は型と安定範囲の単体テストだけを追加する。
- 2-stem 以外の公開ルート切り替え、直和群全般の輸送、任意の元への命名・正規化は次 Phase の課題とする。

## 安全条件と失敗時の処理

文献順で先行している群構造は `resolve_prior_group_result()` で判定する。DB の関係式を GIVEN にしない。Toda (4.5) の具体的同型と各画像の証明は `ProofRule.INFERENCE` を要求する。前提の一つでも未解決であれば証明を complete としない。

`preflight.py` が必要な関数の位置と関連テストを検査する。適用前のソースはバイト列として保存し、限定 pytest または監査の失敗時は復元する。無関係な本番ファイル、テスト、主要文書は変更しない。R6B は実行しない。

## 実施する限定テスト

```powershell
python -m pytest -q `
  phase169_r7_general_stable_transport/tests/test_r7_general_stable_transport.py `
  phase169_r5b_pi75_prior_transport/tests/test_r5b_pi75_transport.py `
  phase169_r6a_pi86_two_step_transport/tests/test_r6a_two_step_transport.py `
  phase169_r3m_prior_result_catalog/tests/test_prior_results.py `
  phase165_r57_r7_toda45_backward_connection/test_phase165_r57_r7_toda45_backward_connection.py
```

`run.ps1` はこの限定テストの後、$\pi_7^5$、$\pi_8^6$、$\pi_9^7$、$\pi_{10}^8$ の共通 Web / Proof Tree 監査を実行する。前二者は既存 complete を維持することが必須。後二者は未完成でもよく、検証が成功した場合のみ complete とする。全体 pytest は Phase 169 最後にだけ実行する。

## 完了条件

1. 任意の $r=1,2,3,4,7$ について共通の推論規則が型付き画像サブゴールを構成する。
2. 安定範囲外を拒否し、違う生成元系列を等しいと推定しない。
3. 引用順と具体的同型が不足する場合は候補を生成しない。
4. 既存 $\pi_7^5$、$\pi_8^6$ が Proof Tree と Web で complete のままである。
5. 限定 pytest と監査が PASS し、変更ファイルは予定範囲のみである。

## 次 Phase との境界

この Phase の目的は専用 $r=3,4$ 処理を作らない一般規則の導入である。任意の stable 元の DB 名称同定、任意の群表示、すべての stem での公開接続を完成したとは主張しない。先行文献情報・画像の証明が不十分な場合は partial を維持する。
