# Phase 176 R3R4 — Zero Image and Hopf Lift Frontier Audit

## 対象・経緯

Phase 176 R3R3 では、$(n,k)=(3,5)$ の共有 Proof Search が未完成（Open Goals 3件）、巡回構造への候補0件、懸垂零像への候補0件であることを観測した。古い Hopf lift は終域全体の位数が目標群の位数と一致する場合に限定されるため、$\pi_8^5\cong\mathbb Z/8$ の真部分群 $\operatorname{im}H\cong\mathbb Z/2$ の持ち上げにはそのまま使用できない。

## 数学的な境界

Toda Lemma 5.7 は $E(\eta_2\nu')=0$ を明記する。以前に証明済みの $\pi_7^2=\mathbb Z/2\{\eta_2\nu'\eta_6\}$ を先行結果として利用し、懸垂と右合成の互換性から $E(\eta_2\nu'\eta_6)=0$ を導き、生成元が零に写ることから $\operatorname{im}(E:\pi_7^2\to\pi_8^3)=0$ を導くのが自然な順序である。その上で EHP 完全性から $H:\pi_8^3\to\pi_8^5$ の単射性が従う。

別途、$\Delta:\pi_8^5\to\pi_6^2$ の核と $H(\nu'\eta_6\eta_7)$ の一致を証明する必要がある。今回の監査は、これらを**証明済みとは扱わない**。

## 検査範囲

1. 既存共有 Proof Search の現在の Open Goals を再観測する。
2. 対象の Hopf 単射性から求められる `ImageZeroStatement` を厳密な型付き EHP で得る。
3. 既存 `expand_zero_image_from_cyclic_generator` を、先行 DB 結果を**未検証の候補 Goal**として呼び出す。
4. 生成元の `GeneratorImage` が Lemma 5.7 の明示部分に直接一致するか、右合成の transport（移送）が必要かを区別する。
5. 既存共有 Provider が零像・生成元零像・Hopf 単射性に返す候補を記録する。

## 非対象

既存 Provider 接続、数学規則・GIVEN・専用 Narrative の追加、root の直接登録、Phase 174 既知 Source Guard 4失敗の修正、全体 pytest は行わない。証明に関する断定はレポートの `proof_complete=false` として抑制する。

## 完了条件と次工程

DryRun PASS、限定 pytest PASS、source anchors の確認、実環境での読み取り専用監査 PASS、report.json への未証明前提の保存が R3R4 完了条件。次工程は、実測された不足が「一般的な右合成移送」か「共有 Provider の接続」か「出典証明欠落」かを判断し、必要最小限の実装のみ行う。
